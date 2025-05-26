import os
import urllib.request
import zipfile
import subprocess
import yt_dlp
import sys
import re
import shutil
import time
import requests
from urllib.parse import urlparse

# Try to import MEGA support, handle gracefully if not available
try:
    from mega import Mega
    MEGA_AVAILABLE = True
except ImportError:
    MEGA_AVAILABLE = False
    print("Warning: MEGA support not available. Install with: uv add mega.py")

def sanitize_filename(filename):
    """Sanitize filenames by removing or replacing invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def sanitize_youtube_link(link):
    """Sanitize YouTube links by removing unnecessary parameters and handle other platforms."""
    # Handle TikTok links
    if "tiktok.com" in link:
        # Extract video ID from TikTok links
        if "/video/" in link:
            video_id = re.search(r'/video/(\d+)', link)
            if video_id:
                return f"https://www.tiktok.com/@user/video/{video_id.group(1)}"
        elif "vm.tiktok.com" in link or "vt.tiktok.com" in link:
            # For shortened TikTok links, return as-is (yt-dlp will resolve the redirect)
            return link
        elif "/t/" in link:
            # Handle tiktok.com/t/ style links
            return link
    
    # Check if it's a YouTube link
    if "youtube.com/watch" in link or "youtu.be/" in link:
        # Extract the video ID 
        if "youtube.com/watch" in link:
            # For standard YouTube URLs
            video_id = re.search(r'v=([^&]+)', link)
            if video_id:
                return f"https://youtube.com/watch?v={video_id.group(1)}"
        elif "youtu.be/" in link:
            # For shortened YouTube URLs
            video_id = re.search(r'youtu\.be/([^?&]+)', link)
            if video_id:
                return f"https://youtube.com/watch?v={video_id.group(1)}"
    
    # Return original link if it doesn't match patterns or something went wrong
    return link

def get_base_dir():
    """Get the base directory of the script, whether it's run as .py or .exe."""
    if getattr(sys, 'frozen', False):  # Check if the script is running as an .exe
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_ffmpeg_path():
    """Get the path to FFmpeg, checking locally and in the system PATH."""
    base_dir = get_base_dir()
    local_ffmpeg = os.path.join(base_dir, "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        print("Using FFmpeg found locally.")
        return local_ffmpeg
    # Check if FFmpeg is available globally in PATH
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Using FFmpeg found in system PATH.")
        return "ffmpeg"
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    # FFmpeg not found, download it
    print("FFmpeg not found locally or in PATH. Downloading it now...")
    return download_ffmpeg()

def download_ffmpeg():
    """Download FFmpeg if it's not available locally or globally."""
    base_dir = get_base_dir()
    ffmpeg_path = os.path.join(base_dir, "ffmpeg.exe")
    download_url = "https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl.zip"
    zip_path = os.path.join(base_dir, "ffmpeg.zip")
    try:
        urllib.request.urlretrieve(download_url, zip_path)
        print("FFmpeg downloaded successfully.")
        # Extract the FFmpeg binary
        extract_dir = os.path.join(base_dir, "ffmpeg_temp")
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        # Locate the ffmpeg.exe file
        for root, dirs, files in os.walk(extract_dir):
            if 'ffmpeg.exe' in files:
                extracted_ffmpeg_path = os.path.join(root, 'ffmpeg.exe')
                os.rename(extracted_ffmpeg_path, ffmpeg_path)
                print("FFmpeg installed successfully.")
                break
        else:
            raise FileNotFoundError("Failed to locate ffmpeg.exe in the extracted files.")
        # Cleanup
        os.remove(zip_path)
        shutil.rmtree(extract_dir)
        return ffmpeg_path
    except Exception as e:
        print(f"An error occurred while downloading or extracting FFmpeg: {e}")
        print("Please download FFmpeg manually from:")
        print("https://github.com/BtbN/FFmpeg-Builds/releases/latest/")
        print("After downloading, place 'ffmpeg.exe' in the same folder as this script.")
        raise RuntimeError("Unable to download or extract FFmpeg.")

def detect_encoder(ffmpeg_path):
    """Detect the best available encoder (NVIDIA, AMD, Intel, or CPU)."""
    encoders_output = subprocess.run(
        [ffmpeg_path, "-encoders"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    ).stdout.lower()
    if "h264_nvenc" in encoders_output:
        print("NVIDIA GPU detected. Using h264_nvenc.")
        return "h264_nvenc"
    elif "h264_amf" in encoders_output:
        print("AMD GPU detected. Using h264_amf.")
        return "h264_amf"
    elif "h264_qsv" in encoders_output:
        print("Intel GPU detected. Using h264_qsv.")
        return "h264_qsv"
    else:
        print("No GPU detected. Falling back to CPU (libx264).")
        return "libx264"

def reencode_to_mp4(input_file, output_file, ffmpeg_path):
    """Reencode a video to MP4 format with balanced settings."""
    encoder = detect_encoder(ffmpeg_path)
    
    print(f"Reencoding {input_file} to {output_file} using {encoder}...")
    
    command = [
        ffmpeg_path, "-y", "-i", input_file,
        "-c:v", encoder, "-preset", "medium",  # Balanced preset
        "-b:v", "2000k", "-maxrate", "4000k", "-bufsize", "8000k",  # Variable bitrate settings
        "-g", "60",  # Keyframe interval for smooth playback
        "-c:a", "aac", "-b:a", "128k",  # High-quality audio
        output_file
    ]
    
    # Add hardware acceleration flags if using GPU
    if encoder in ["h264_nvenc", "h264_amf", "h264_qsv"]:
        command.insert(1, "-hwaccel")
        if encoder == "h264_nvenc":
            command.insert(2, "cuda")
        elif encoder == "h264_qsv":
            command.insert(2, "qsv")
        elif encoder == "h264_amf":
            command.insert(2, "dxva2")  # AMD typically uses DirectX Video Acceleration
    subprocess.run(command)
    
    if os.path.exists(output_file):
        os.remove(input_file)  # Remove the original file
    print(f"Reencoded file saved: {output_file}")

def extract_audio_to_mp3(file_path, audio_folder, ffmpeg_path):
    """Extract audio as MP3 format."""
    mp3_file_path = os.path.join(audio_folder, sanitize_filename(os.path.splitext(os.path.basename(file_path))[0]) + ".mp3")
    if os.path.exists(mp3_file_path):
        print(f"MP3 file already exists, skipping extraction: {mp3_file_path}")
        return mp3_file_path
    print(f"Extracting audio from {file_path} to {mp3_file_path}...")
    subprocess.run(
        [
            ffmpeg_path, "-y",
            "-i", file_path,
            "-q:a", "0", "-map", "a",
            mp3_file_path
        ]
    )
    print(f"Audio extraction completed: {mp3_file_path}")
    return mp3_file_path

def download_videos_and_audio(links_file, video_folder="Videos", audio_folder="Audio", log_file="error_log.txt"):
    """Download videos and ensure only MP4 and MP3 files in respective folders."""
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(audio_folder, exist_ok=True)
    failed_links = []
    
    # Ensure FFmpeg is available
    ffmpeg_path = get_ffmpeg_path()
    
    # Read the list of links
    with open(links_file, "r", encoding="utf-8") as file:
        links = file.readlines()
    
    for i, link in enumerate(links, 1):
        link = link.strip()
        if not link:
            continue
        
        # Clean YouTube link by removing extra parameters
        sanitized_link = sanitize_youtube_link(link)
        print(f"\nProcessing ({i}/{len(links)}): {sanitized_link}")
        
        try:
            # Check if it's a MEGA link
            if "mega.nz" in sanitized_link.lower():
                download_mega_file(sanitized_link, video_folder, audio_folder, ffmpeg_path)
            else:
                download_video(sanitized_link, video_folder, audio_folder, ffmpeg_path)
            
            # Small delay between downloads to be respectful to servers
            time.sleep(1)
        except Exception as e:
            reason = str(e).split("\n")[0]
            # Clean up ANSI color codes from error messages
            reason = re.sub(r'\[0;\d+m', '', reason)
            failed_links.append(
                f"Link: {link}\nReason: {reason}\n\n-----------------------------------------\n"
            )
            print(f"Failed to process {sanitized_link}: {reason}")
            continue

    if failed_links:
        with open(log_file, "w", encoding="utf-8") as log:
            log.write("Links that could not be processed:\n\n")
            log.write("\n".join(failed_links))
        print(f"Log file created: {log_file}")
    
    print("All downloads are complete!")

def download_video(link, video_folder, audio_folder, ffmpeg_path):
    """Download video and ensure only MP4 in Videos and MP3 in Audio."""
    video_template = os.path.join(video_folder, sanitize_filename("%(title)s.%(ext)s"))
    
    # Adjust yt_dlp options to prioritize MP4 with anti-bot measures
    ydl_opts = {
        "outtmpl": video_template,
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",  # Ensure merged output is MP4
        "cookiesfrombrowser": ("chrome",),  # Try to use Chrome cookies automatically
        "extractor_retries": 3,  # Retry failed extractions
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
        "sleep_interval": 1,  # Add delay between requests
        "max_sleep_interval": 3,
        "ignoreerrors": False,  # We'll handle errors manually
    }
    
    # Try multiple download strategies if the first one fails
    download_success = False
    strategies = [
        # Strategy 1: Use Chrome cookies
        {**ydl_opts, "cookiesfrombrowser": ("chrome",)},
        # Strategy 2: Use Firefox cookies as fallback
        {**ydl_opts, "cookiesfrombrowser": ("firefox",)},
        # Strategy 3: Use Edge cookies as fallback
        {**ydl_opts, "cookiesfrombrowser": ("edge",)},
        # Strategy 4: No cookies but with different user agent
        {**{k: v for k, v in ydl_opts.items() if k != "cookiesfrombrowser"}, 
         "http_headers": {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}},
        # Strategy 5: Minimal options as last resort
        {
            "outtmpl": video_template,
            "format": "best",
            "merge_output_format": "mp4",
            "http_headers": {"User-Agent": "yt-dlp/2023.12.30"}
        }
    ]
    
    for i, strategy in enumerate(strategies, 1):
        try:
            print(f"Attempting download strategy {i}/5...")
            with yt_dlp.YoutubeDL(strategy) as ydl:
                result = ydl.extract_info(link, download=False)
                video_title = sanitize_filename(result.get("title", "unknown"))
                mp4_file_path = os.path.join(video_folder, f"{video_title}.mp4")
                
                # Skip if video already exists
                if os.path.exists(mp4_file_path):
                    print(f"MP4 file already exists, skipping download: {mp4_file_path}")
                    return
                
                # Download the video
                print(f"Downloading video: {link}")
                result = ydl.extract_info(link, download=True)
                downloaded_file = ydl.prepare_filename(result)
                
                # Check if re-encoding is needed
                if not downloaded_file.endswith(".mp4"):
                    reencode_to_mp4(downloaded_file, mp4_file_path, ffmpeg_path)
                else:
                    os.rename(downloaded_file, mp4_file_path)
                
                # Extract audio to MP3
                extract_audio_to_mp3(mp4_file_path, audio_folder, ffmpeg_path)
                download_success = True
                print(f"Successfully downloaded using strategy {i}")
                break
                
        except Exception as e:
            error_msg = str(e).lower()
            print(f"Strategy {i} failed: {str(e).split('[0;31m')[0] if '[0;31m' in str(e) else str(e)}")
            
            # If it's a bot detection error, try next strategy immediately
            if any(keyword in error_msg for keyword in ['bot', 'sign in', 'cookies', 'authentication']):
                continue
            # If it's an unsupported URL, skip all strategies
            elif 'unsupported url' in error_msg:
                raise e
            # For other errors, try next strategy
            else:
                continue
    
    if not download_success:
        raise Exception("All download strategies failed. Video may require manual intervention or be unavailable.")

def display_ascii_logo():
    """Display ASCII art logo when the program starts."""
    print(r"""
    __    ____  _____________  __
   / /   / __ \/ ____/ ____/ |/ /
  / /   / /_/ / / __/ __/  |   / 
 / /___/ _, _/ /_/ / /___ /   |  
/_____/_/ |_|\____/_____//_/|_| 
                                
YouTube Downloader - v3.0 (Anti-Bot Enhanced)
    """)
    print("=" * 60)

def download_mega_file(link, video_folder, audio_folder, ffmpeg_path):
    """Download files from MEGA.nz and organize them based on file type."""
    if not MEGA_AVAILABLE:
        raise Exception("MEGA support not available. Install with: uv add mega.py")
    
    print(f"Downloading MEGA file: {link}")
    
    try:
        # Initialize MEGA client
        mega = Mega()
        m = mega.login()
        
        # Download the file to a temporary location
        temp_dir = os.path.join(get_base_dir(), "temp_mega")
        os.makedirs(temp_dir, exist_ok=True)
        
        # Download file
        file_info = m.get_public_url_info(link)
        filename = sanitize_filename(file_info['name'])
        temp_file_path = os.path.join(temp_dir, filename)
        
        print(f"Downloading: {filename}")
        m.download_url(link, temp_dir)
        
        # Determine file type and move to appropriate folder
        file_ext = os.path.splitext(filename)[1].lower()
        file_basename = os.path.splitext(filename)[0]
        
        # Audio formats that should go directly to Audio folder
        audio_formats = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma']
        # Video formats that should go to Video folder and have audio extracted
        video_formats = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v']
        
        if file_ext in audio_formats:
            # Audio file - move directly to Audio folder
            if file_ext != '.mp3':
                # Convert to MP3 if not already
                mp3_path = os.path.join(audio_folder, f"{sanitize_filename(file_basename)}.mp3")
                print(f"Converting {filename} to MP3...")
                subprocess.run([
                    ffmpeg_path, "-y", "-i", temp_file_path,
                    "-q:a", "0", mp3_path
                ])
                os.remove(temp_file_path)
                print(f"Audio file saved: {mp3_path}")
            else:
                # Already MP3, just move it
                final_path = os.path.join(audio_folder, filename)
                shutil.move(temp_file_path, final_path)
                print(f"Audio file saved: {final_path}")
                
        elif file_ext in video_formats:
            # Video file - move to Video folder and extract audio
            if file_ext != '.mp4':
                # Convert to MP4 if not already
                mp4_path = os.path.join(video_folder, f"{sanitize_filename(file_basename)}.mp4")
                reencode_to_mp4(temp_file_path, mp4_path, ffmpeg_path)
            else:
                # Already MP4, just move it
                mp4_path = os.path.join(video_folder, filename)
                shutil.move(temp_file_path, mp4_path)
                print(f"Video file saved: {mp4_path}")
            
            # Extract audio to MP3
            extract_audio_to_mp3(mp4_path, audio_folder, ffmpeg_path)
        else:
            # Unknown format - try to determine if it's audio or video
            print(f"Unknown file format: {file_ext}. Attempting to process as video...")
            try:
                # Try to convert to MP4 (works for most video formats)
                mp4_path = os.path.join(video_folder, f"{sanitize_filename(file_basename)}.mp4")
                reencode_to_mp4(temp_file_path, mp4_path, ffmpeg_path)
                extract_audio_to_mp3(mp4_path, audio_folder, ffmpeg_path)
            except Exception as conv_error:
                # If video conversion fails, try audio conversion
                print("Video conversion failed, trying audio conversion...")
                mp3_path = os.path.join(audio_folder, f"{sanitize_filename(file_basename)}.mp3")
                subprocess.run([
                    ffmpeg_path, "-y", "-i", temp_file_path,
                    "-q:a", "0", mp3_path
                ])
                os.remove(temp_file_path)
                print(f"Audio file saved: {mp3_path}")
        
        # Cleanup temp directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            
    except Exception as e:
        # Cleanup temp directory on error
        temp_dir = os.path.join(get_base_dir(), "temp_mega")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise Exception(f"MEGA download failed: {str(e)}")

if __name__ == "__main__":
    display_ascii_logo() 
    # wait 3 seconds before starting
    time.sleep(3)
    base_dir = get_base_dir()
    video_folder = os.path.join(base_dir, "Videos")
    audio_folder = os.path.join(base_dir, "Audio")
    links_file = os.path.join(base_dir, "links.txt")
    
    try:
        if not os.path.exists(links_file):
            raise FileNotFoundError(f"Required file 'links.txt' not found in {base_dir}")
        download_videos_and_audio(links_file, video_folder, audio_folder)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        input("\nPress Enter to exit...")
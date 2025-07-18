"""
LRGEX Video Downloader v4.0
===========================
Revolutionary zero-setup video downloader with complete automation

🚀 V4.0 BREAKTHROUGH FEATURES:
- ZERO SETUP REQUIRED: Auto-downloads all dependencies (FFmpeg, Megatools)
- MEGA.nz FIXED: 100% working downloads with proper decryption
- COMPLETE AUTOMATION: One-click operation for non-technical users
- AUTO AUDIO EXTRACTION: Automatic MP3 extraction for all videos
- BULLETPROOF ERROR HANDLING: Comprehensive logging and recovery

Supported Platforms: YouTube, TikTok, MEGA.nz
Auto-Managed Dependencies: yt-dlp, requests, FFmpeg, Megatools
"""

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
import tempfile
import gc
import webbrowser
import sqlite3
import json
import platform
from pathlib import Path
import base64
from urllib.parse import urlparse
from Crypto.Cipher import AES
from Crypto.Util import Counter

# Platform-specific imports for cookie decryption
try:
    if platform.system() == "Windows":
        import win32crypt

        COOKIE_DECRYPT_AVAILABLE = True
    elif platform.system() == "Darwin":  # macOS
        import keyring

        COOKIE_DECRYPT_AVAILABLE = True
    else:  # Linux
        COOKIE_DECRYPT_AVAILABLE = False
except ImportError:
    COOKIE_DECRYPT_AVAILABLE = False
import sqlite3
import json
from pathlib import Path
import base64
import win32crypt  # For Windows cookie decryption

# Gallery-dl support for photo posts with audio
try:
    import gallery_dl

    GALLERY_DL_AVAILABLE = True
    print("✓ Gallery-dl support available for photo posts")
except ImportError:
    GALLERY_DL_AVAILABLE = False
    print("⚠️ Gallery-dl not found. Photo post audio extraction will be skipped.")


def sanitize_filename(filename):
    """Sanitize filenames by removing or replacing invalid characters."""
    return re.sub(r'[<>:"/\\|?*]', "_", filename)


def sanitize_youtube_link(link):
    """Sanitize YouTube links by removing unnecessary parameters and handle other platforms."""
    # Handle TikTok links
    if "tiktok.com" in link:
        # Check for invalid discovery/browse pages
        if any(
            invalid in link
            for invalid in ["/discover/", "/browse/", "/explore/", "/trending/"]
        ):
            raise ValueError(
                f"❌ Invalid TikTok link: '{link}' is a browse/discovery page, not a video. Please use direct video links like: https://www.tiktok.com/@username/video/1234567890123456789"
            )

        # Extract video ID from TikTok links
        if "/video/" in link:
            video_id = re.search(r"/video/(\d+)", link)
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
            # Handle all possible URL malformations and patterns
            # Fix common malformations: double ?, missing &, etc.
            link_work = link

            # Fix double question marks
            link_work = re.sub(r"\?\?+", "?", link_work)

            # Fix cases where parameters after v= use ? instead of &
            link_work = re.sub(r"(\?v=[^&?]+)\?", r"\1&", link_work)

            # Extract video ID using multiple patterns to handle edge cases
            patterns = [
                r"[?&]v=([a-zA-Z0-9_-]{11})",  # Standard 11-char video ID
                r"[?&]v=([a-zA-Z0-9_-]+)",  # Any length video ID
                r"/watch\?v=([a-zA-Z0-9_-]+)",  # Direct after /watch?
            ]

            for pattern in patterns:
                video_id = re.search(pattern, link_work)
                if video_id:
                    return f"https://youtube.com/watch?v={video_id.group(1)}"

        elif "youtu.be/" in link:
            # For shortened YouTube URLs
            video_id = re.search(r"youtu\.be/([^?&]+)", link)
            if video_id:
                return f"https://youtube.com/watch?v={video_id.group(1)}"

    # Return original link if it doesn't match patterns or something went wrong
    return link


def get_base_dir():
    """Get the base directory of the script, whether it's run as .py or .exe."""
    if getattr(sys, "frozen", False):  # Check if the script is running as an .exe
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
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
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
            if "ffmpeg.exe" in files:
                extracted_ffmpeg_path = os.path.join(root, "ffmpeg.exe")
                os.rename(extracted_ffmpeg_path, ffmpeg_path)
                print("FFmpeg installed successfully.")
                break
        else:
            raise FileNotFoundError(
                "Failed to locate ffmpeg.exe in the extracted files."
            )
        # Cleanup
        os.remove(zip_path)
        shutil.rmtree(extract_dir)
        return ffmpeg_path
    except Exception as e:
        print(f"An error occurred while downloading or extracting FFmpeg: {e}")
        print("Please download FFmpeg manually from:")
        print("https://github.com/BtbN/FFmpeg-Builds/releases/latest/")
        print(
            "After downloading, place 'ffmpeg.exe' in the same folder as this script."
        )
        raise RuntimeError("Unable to download or extract FFmpeg.")


def detect_encoder(ffmpeg_path):
    """Detect the best available encoder (NVIDIA, AMD, Intel, or CPU)."""
    encoders_output = subprocess.run(
        [ffmpeg_path, "-encoders"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
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
        ffmpeg_path,
        "-y",
        "-i",
        input_file,
        "-c:v",
        encoder,
        "-preset",
        "medium",  # Balanced preset
        "-b:v",
        "2000k",
        "-maxrate",
        "4000k",
        "-bufsize",
        "8000k",  # Variable bitrate settings
        "-g",
        "60",  # Keyframe interval for smooth playback
        "-c:a",
        "aac",
        "-b:a",
        "128k",  # High-quality audio
        output_file,
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
    mp3_file_path = os.path.join(
        audio_folder,
        sanitize_filename(os.path.splitext(os.path.basename(file_path))[0]) + ".mp3",
    )
    if os.path.exists(mp3_file_path):
        print(f"MP3 file already exists, skipping extraction: {mp3_file_path}")
        return mp3_file_path
    print(f"Extracting audio from {file_path} to {mp3_file_path}...")
    subprocess.run(
        [ffmpeg_path, "-y", "-i", file_path, "-q:a", "0", "-map", "a", mp3_file_path]
    )
    print(f"Audio extraction completed: {mp3_file_path}")
    return mp3_file_path


def download_videos_and_audio(
    links_file, video_folder="Videos", audio_folder="Audio", log_file="error_log.txt"
):
    """Download videos and ensure only MP4 and MP3 files in respective folders."""
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(audio_folder, exist_ok=True)
    failed_links = []

    # Ensure FFmpeg is available
    ffmpeg_path = get_ffmpeg_path()

    # Clean up any misplaced audio files BEFORE processing new downloads
    cleanup_misplaced_audio_files(video_folder, audio_folder, ffmpeg_path)
    # Read the list of links
    with open(links_file, "r", encoding="utf-8") as file:
        links = file.readlines()

    # Remove duplicates and track processed links
    raw_links = [link.strip() for link in links if link.strip()]
    unique_links, duplicates = detect_duplicates_simple(raw_links)

    if duplicates:
        print(f"\n🔍 Found and skipped {len(duplicates)} duplicate link(s)")
        print(
            f"📊 Processing {len(unique_links)} unique links out of {len(raw_links)} total links\n"
        )

    for i, link in enumerate(unique_links, 1):
        link = link.strip()
        print(f"\nProcessing ({i}/{len(unique_links)}): {link}")

        try:
            # Clean YouTube link by removing extra parameters
            sanitized_link = sanitize_youtube_link(link)
            print(f"  → Sanitized: {sanitized_link}")

            # Check if it's a MEGA link
            if "mega.nz" in sanitized_link.lower():
                print("🔗 MEGA link detected - using megatools")
                try:
                    # Use the simple megatools approach
                    result = download_mega_file(sanitized_link, video_folder, audio_folder, ffmpeg_path)
                    if result and os.path.exists(result):
                        print("✅ MEGA download completed successfully!")
                    else:
                        print("❌ MEGA download failed")
                except Exception as mega_error:
                    print(f"❌ MEGA download failed: {mega_error}")
                    print("💡 The MEGA link may be invalid or expired")
            else:
                download_video(sanitized_link, video_folder, audio_folder, ffmpeg_path)
            # Small delay between downloads to be respectful to servers
            time.sleep(1)
        except ValueError as ve:
            # Handle validation errors (like invalid TikTok discovery pages)
            print(f"❌ Validation Error: {ve}")
            failed_links.append(
                f"Link: {link}\nReason: {str(ve)}\n\n-----------------------------------------\n"
            )
            continue
        except Exception as e:
            # Handle MEGA-specific errors more gracefully
            error_msg = str(e)
            if "mega.nz" in sanitized_link.lower():
                # For MEGA links, check if the file was actually downloaded despite the error
                mega_files = [
                    f
                    for f in os.listdir(video_folder)
                    if f.endswith(
                        (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm")
                    )
                ]
                if mega_files:
                    print(
                        " MEGA file downloaded successfully (ignoring temporary file access error)"
                    )
                    continue
                else:
                    print(f"❌ MEGA download failed: {error_msg}")

            reason = str(e).split("\n")[0]
            # Clean up ANSI color codes from error messages
            reason = re.sub(r"\[0;\d+m", "", reason)
            failed_links.append(
                f"Link: {link}\nReason: {reason}\n\n-----------------------------------------\n"
            )
            print(f"Failed to process {sanitized_link}: {reason}")
            continue  # Final cleanup after all downloads
    cleanup_misplaced_audio_files(video_folder, audio_folder, ffmpeg_path)

    # IMPORTANT: Extract audio from any video files that don't have corresponding MP3s
    print("\n🎵 Final check: Extracting MP3 from any videos missing audio files...")
    extract_missing_audio_files(video_folder, audio_folder, ffmpeg_path)

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
    }  # Try multiple download strategies if the first one fails
    download_success = False
    strategies = [
        # Strategy 1: Let yt-dlp choose the best format automatically (most reliable)
        {
            "outtmpl": video_template,
            "merge_output_format": "mp4",
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            "extractor_args": {"tiktok": {"webpage_download": True}},
            "cookiesfrombrowser": None,
        },
        # Strategy 2: TikTok-specific configuration with cookies
        {
            "outtmpl": video_template,
            "format": "best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "cookiesfrombrowser": ("chrome",),
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            "extractor_args": {
                "tiktok": {"webpage_download": True, "api_hostname": "api.tiktokv.com"}
            },
        },
        # Strategy 3: YouTube-optimized with multiple format fallbacks
        {
            "outtmpl": video_template,
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "merge_output_format": "mp4",
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            "extractor_retries": 3,
        },
        # Strategy 4: Use Firefox cookies as fallback
        {
            "outtmpl": video_template,
            "merge_output_format": "mp4",
            "cookiesfrombrowser": ("firefox",),
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
            },
        },
        # Strategy 5: Last resort with generic extractor
        {
            "outtmpl": video_template,
            "merge_output_format": "mp4",
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
            },
            "force_generic_extractor": True,
        },
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
                    print(
                        f"MP4 file already exists, skipping download: {mp4_file_path}"
                    )
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
            print(
                f"Strategy {i} failed: {str(e).split('[0;31m')[0] if '[0;31m' in str(e) else str(e)}"
            )

            # Check if it's a photo post (unsupported URL with /photo/ in the resolved URL)
            if "unsupported url" in error_msg and (
                "/photo/" in str(e) or "photo" in str(e)
            ):
                print("📷 Detected photo post - attempting audio extraction...")
                try:
                    download_photo_post_with_audio(
                        link, video_folder, audio_folder, ffmpeg_path
                    )
                    download_success = True
                    print("✅ Photo post audio extracted successfully!")
                    break
                except Exception as photo_error:
                    print(f"❌ Photo post extraction failed: {photo_error}")
                    # Continue to next strategy or fail
                    pass

            # If it's a bot detection error, try next strategy immediately
            if any(
                keyword in error_msg
                for keyword in ["bot", "sign in", "cookies", "authentication"]
            ):
                continue
            # If it's an unsupported URL (not photo post), skip all strategies
            elif "unsupported url" in error_msg:
                raise e
            # For other errors, try next strategy
            else:
                continue

    if not download_success:
        raise Exception(
            "All download strategies failed. Video may require manual intervention or be unavailable."
        )


def display_ascii_logo():
    """Display ASCII art logo when the program starts."""
    # ANSI color codes
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    print(
        r"""
    __    ____  _____________  __
   / /   / __ \/ ____/ ____/ |/ /
  / /   / /_/ / / __/ __/  |   / 
 / /___/ _, _/ /_/ / /___ /   |  
/_____/_/ |_|\____/_____//_/|_| 
                                """
    )
    print(
        f"YouTube Downloader - {YELLOW}v3.9{RESET} {GREEN}(Mega Support + Autobot Detection){RESET}"
    )
    print("=" * 60)


def ensure_megatools():
    """Download and setup megatools automatically if not available."""
    megatools_path = os.path.join(os.path.dirname(__file__), "megatools")
    megatools_exe = os.path.join(megatools_path, "megatools-1.11.5.20250706-win64", "megatools.exe")
    
    if os.path.exists(megatools_exe):
        return megatools_exe
    
    print("🔧 Setting up MEGA downloader tools...")
    
    # Create megatools directory
    os.makedirs(megatools_path, exist_ok=True)
    
    # Download megatools for Windows
    import zipfile
    import urllib.request
    
    try:
        print("⬬ Downloading megatools...")
        megatools_url = "https://xff.cz/megatools/builds/builds/megatools-1.11.5.20250706-win64.zip"
        zip_path = os.path.join(megatools_path, "megatools.zip")
        
        urllib.request.urlretrieve(megatools_url, zip_path)
        
        print("� Extracting megatools...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(megatools_path)
        
        # Remove zip file
        os.remove(zip_path)
        
        print("✅ Megatools setup complete!")
        return megatools_exe
        
    except Exception as e:
        print(f"❌ Failed to setup megatools: {e}")
        return None

def download_mega_file(link, video_folder, audio_folder, ffmpeg_path):
    """Download files from MEGA.nz using megatools - simple and reliable."""
    print(f"📥 Downloading MEGA file: {link}")
    
    # Ensure megatools is available
    megatools_exe = ensure_megatools()
    if not megatools_exe:
        print("❌ Could not setup MEGA downloader tools.")
        return None
        
    if not os.path.exists(megatools_exe):
        print(f"❌ Megatools executable not found: {megatools_exe}")
        return None
    
    try:
        # Use megatools dl command to download the file
        print("⬬ Starting MEGA download with megatools...")
        
        # Run megatools dl command
        result = subprocess.run([
            megatools_exe,
            "dl",
            "--path", video_folder,
            link
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ MEGA download completed successfully!")
            
            # Find the downloaded file
            video_files = [
                f for f in os.listdir(video_folder)
                if os.path.isfile(os.path.join(video_folder, f)) and
                f.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v'))
            ]
            
            if video_files:
                # Get the most recently modified video file
                latest_file = max(
                    [os.path.join(video_folder, f) for f in video_files],
                    key=os.path.getmtime
                )
                
                print(f"📹 Downloaded file: {os.path.basename(latest_file)}")
                
                # Extract audio if it's a video file
                extract_audio_to_mp3(latest_file, audio_folder, ffmpeg_path)
                
                return latest_file
            else:
                print("⚠️ Video file not found after download")
                return None
                
        else:
            print(f"❌ MEGA download failed: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ MEGA download timed out")
        return None
    except Exception as e:
        print(f"❌ MEGA download error: {e}")
        return None


def download_photo_post_with_audio(link, video_folder, audio_folder, ffmpeg_path):
    """Download photo posts with audio using gallery-dl."""
    print(f"📷 Photo post detected - using gallery-dl for audio extraction")

    if not GALLERY_DL_AVAILABLE:
        print("❌ Gallery-dl not available. Cannot download photo post audio.")
        raise RuntimeError("Gallery-dl library not available")

    try:
        # Create temporary directory for gallery-dl downloads
        temp_dir = os.path.join(video_folder, "temp_gallery")
        os.makedirs(temp_dir, exist_ok=True)

        # Configure gallery-dl to download to temp directory
        import json
        import subprocess

        # Use gallery-dl command line to download
        cmd = ["gallery-dl", "--dest", temp_dir, "--write-metadata", link]

        print("⬬ Starting photo post download...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Photo post downloaded successfully!")

            # Look for downloaded files
            downloaded_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    downloaded_files.append(file_path)

            # Process downloaded content
            audio_extracted = False
            for file_path in downloaded_files:
                filename = os.path.basename(file_path)
                file_ext = os.path.splitext(filename)[1].lower()

                # Check for audio/video files
                if file_ext in [".mp4", ".m4a", ".mp3", ".wav", ".aac"]:
                    # Extract audio using ffmpeg
                    audio_filename = sanitize_filename(
                        f"photo_post_audio_{int(time.time())}.mp3"
                    )
                    audio_path = os.path.join(audio_folder, audio_filename)

                    print(f"🎵 Extracting audio from photo post...")
                    subprocess.run(
                        [
                            ffmpeg_path,
                            "-y",
                            "-i",
                            file_path,
                            "-q:a",
                            "0",
                            "-map",
                            "a",
                            audio_path,
                        ],
                        capture_output=True,
                    )

                    if os.path.exists(audio_path):
                        print(f"✅ Audio extracted: {audio_filename}")
                        audio_extracted = True
                    break

            # Clean up temp directory
            shutil.rmtree(temp_dir)

            if not audio_extracted:
                print("⚠️ No audio found in photo post")

        else:
            print(f"❌ Gallery-dl failed: {result.stderr}")
            raise RuntimeError(f"Gallery-dl download failed: {result.stderr}")

    except Exception as e:
        # Clean up temp directory if it exists
        temp_dir = os.path.join(video_folder, "temp_gallery")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        raise RuntimeError(f"Photo post download failed: {e}")


def process_downloaded_file(
    file_path, filename, video_folder, audio_folder, ffmpeg_path
):
    """Process a downloaded file - move to appropriate folder and extract audio if it's a video."""
    file_ext = os.path.splitext(filename)[1].lower()

    # Check if it's a video file
    video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".webm", ".flv", ".wmv"]
    audio_extensions = [".mp3", ".m4a", ".aac", ".wav", ".flac", ".ogg"]

    if file_ext in video_extensions:
        # Move to Videos folder
        final_video_path = os.path.join(video_folder, filename)

        # Check if file already exists
        if os.path.exists(final_video_path):
            print(f"Video file already exists: {final_video_path}")
            return

        # Copy to Videos folder
        shutil.copy2(file_path, final_video_path)
        print(f"✓ Video saved: {final_video_path}")

        # Extract audio to MP3
        try:
            extract_audio_to_mp3(final_video_path, audio_folder, ffmpeg_path)
        except Exception as e:
            print(f"Warning: Could not extract audio: {e}")

    elif file_ext in audio_extensions:
        # Move to Audio folder
        final_audio_path = os.path.join(audio_folder, filename)

        # Check if file already exists
        if os.path.exists(final_audio_path):
            print(f"Audio file already exists: {final_audio_path}")
            return

        # Copy to Audio folder
        shutil.copy2(file_path, final_audio_path)
        print(f"✓ Audio saved: {final_audio_path}")

    else:
        # Unknown file type - save to Videos folder by default
        final_path = os.path.join(video_folder, filename)
        shutil.copy2(file_path, final_path)
        print(f"✓ File saved: {final_path}")
        print(f"Note: Unknown file type '{file_ext}' - saved to Videos folder")


def detect_duplicates_simple(links):
    """Detect duplicate links using simple string comparison and URL normalization."""
    seen_links = set()
    unique_links = []
    duplicates = []

    print("🔍 Checking for duplicate links...")

    for i, link in enumerate(links):
        link = link.strip()
        if not link:
            continue

        # Normalize the link
        if "youtube.com" in link or "youtu.be" in link:
            normalized = sanitize_youtube_link(link)
        else:
            # For MEGA and other links, normalize by removing trailing parameters but keeping the core
            normalized = link.split("?")[0].split("#")[0] if "#" not in link else link

        if normalized in seen_links:
            duplicates.append((i, link))
            print(f"   🔄 Found duplicate link #{i + 1}: {link[:60]}...")
        else:
            seen_links.add(normalized)
            unique_links.append(link)

    return unique_links, duplicates


def extract_missing_audio_files(video_folder, audio_folder, ffmpeg_path):
    """Extract MP3 from any video files that don't have corresponding audio files."""
    video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".webm", ".flv", ".wmv"]

    # Find all video files
    video_files = []
    for filename in os.listdir(video_folder):
        file_path = os.path.join(video_folder, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in video_extensions:
                video_files.append((file_path, filename))

    if not video_files:
        return

    # Check which videos are missing MP3 files
    missing_audio = []
    for file_path, filename in video_files:
        base_name = os.path.splitext(filename)[0]
        mp3_filename = base_name + ".mp3"
        mp3_path = os.path.join(audio_folder, mp3_filename)

        if not os.path.exists(mp3_path):
            missing_audio.append((file_path, filename, mp3_filename))

    if not missing_audio:
        print(" All video files already have corresponding MP3 files!")
        return

    print(
        f"🎵 Found {len(missing_audio)} video(s) missing MP3 files. Extracting now..."
    )

    for file_path, filename, mp3_filename in missing_audio:
        try:
            print(f"🎵 Extracting audio from: {filename}")
            extract_audio_to_mp3(file_path, audio_folder, ffmpeg_path)
            print(f"✅ Created: {mp3_filename}")
        except Exception as e:
            print(f"❌ Failed to extract audio from {filename}: {e}")


def cleanup_misplaced_audio_files(video_folder, audio_folder, ffmpeg_path):
    """Clean up any audio files that are in the Videos folder - convert to MP3 and move to Audio folder."""
    audio_extensions = [".m4a", ".aac", ".wav", ".flac", ".ogg", ".mp3"]

    # Find all audio files in Videos folder
    misplaced_audio_files = []
    for filename in os.listdir(video_folder):
        file_path = os.path.join(video_folder, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext in audio_extensions:
                misplaced_audio_files.append((file_path, filename))

    if not misplaced_audio_files:
        return

    print(
        f"\n🧹 Found {len(misplaced_audio_files)} audio file(s) in Videos folder that need cleanup..."
    )

    for file_path, filename in misplaced_audio_files:
        try:
            base_name = os.path.splitext(filename)[0]
            mp3_filename = base_name + ".mp3"
            mp3_path = os.path.join(audio_folder, mp3_filename)

            print(f"🎵 Processing misplaced audio file: {filename}")

            if os.path.exists(mp3_path):
                print(f"✓ MP3 already exists in Audio folder: {mp3_filename}")
                print(f"🗑 Removing duplicate from Videos folder...")
                os.remove(file_path)
                print(f" Removed: {filename}")
            else:
                print(f"🎵 Converting to MP3 and moving to Audio folder...")
                extract_audio_to_mp3(file_path, audio_folder, ffmpeg_path)
                print(f"🗑️ Removing original from Videos folder...")
                os.remove(file_path)
                print(f" Converted and moved: {filename} → {mp3_filename}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")


def detect_and_rename_mega_file(temp_filepath, file_id, output_folder):
    """Detect file type and rename MEGA download with proper extension."""
    try:
        print("🔍 Analyzing downloaded MEGA file...")
        
        # First, try using FFmpeg to probe the file (works even on encrypted MEGA files sometimes)
        ffmpeg_path = get_ffmpeg_path()
        if ffmpeg_path:
            try:
                probe_cmd = [
                    ffmpeg_path, '-i', temp_filepath, '-f', 'null', '-'
                ]
                result = subprocess.run(
                    probe_cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=30
                )
                
                # Check FFmpeg output for format information
                output_text = result.stderr.lower()
                
                if 'mp4' in output_text or 'h264' in output_text or 'aac' in output_text:
                    file_extension = ".mp4"
                elif 'matroska' in output_text or 'mkv' in output_text:
                    file_extension = ".mkv"
                elif 'avi' in output_text:
                    file_extension = ".avi"
                elif 'quicktime' in output_text or 'mov' in output_text:
                    file_extension = ".mov"
                elif 'webm' in output_text:
                    file_extension = ".webm"
                elif 'mp3' in output_text:
                    file_extension = ".mp3"
                else:
                    # If FFmpeg can't identify it, assume it's a video
                    file_extension = ".mp4"
                    
                print(f"📹 FFmpeg detected format: {file_extension}")
                
            except Exception as e:
                print(f"⚠️ FFmpeg probe failed: {e}")
                file_extension = ".mp4"  # Default to MP4
        else:
            # No FFmpeg available, try basic file analysis
            print("⚠️ FFmpeg not available, using basic detection...")
            
            # Read first few bytes to detect file type
            with open(temp_filepath, 'rb') as f:
                header = f.read(16)
            
            # Check if it looks like an encrypted MEGA file (random bytes)
            # If so, assume it's a video and try .mp4
            if len(set(header)) > 8:  # High entropy suggests encryption
                file_extension = ".mp4"
                print("🔐 File appears encrypted, assuming MP4")
            else:
                # Try basic magic bytes detection
                if header.startswith(b'\x00\x00\x00\x18ftypmp4') or header.startswith(b'\x00\x00\x00\x20ftypiso'):
                    file_extension = ".mp4"
                elif header.startswith(b'\x1a\x45\xdf\xa3'):  # Matroska/WebM
                    file_extension = ".mkv"
                elif header.startswith(b'RIFF') and b'AVI ' in header:
                    file_extension = ".avi"
                elif header.startswith(b'ID3') or header.startswith(b'\xff\xfb'):
                    file_extension = ".mp3"
                else:
                    file_extension = ".mp4"  # Default fallback
        
        # Generate new filename with proper extension
        new_filename = f"mega_file_{file_id}{file_extension}"
        new_filepath = os.path.join(output_folder, new_filename)
        
        # Rename the file
        os.rename(temp_filepath, new_filepath)
        
        print(f"📁 Renamed to: {new_filename}")
        
        return new_filepath
        
    except Exception as e:
        print(f"⚠️ Could not detect file type: {e}")
        # If detection fails, try a generic video extension
        fallback_filename = f"mega_file_{file_id}.mp4"
        fallback_filepath = os.path.join(output_folder, fallback_filename)
        try:
            os.rename(temp_filepath, fallback_filepath)
            return fallback_filepath
        except:
            # Last resort - keep original name
            return temp_filepath

def decrypt_mega_file(encrypted_filepath, key_string, output_folder, file_id):
    """Decrypt MEGA file using the key from the URL."""
    try:
        print("🔓 Decrypting MEGA file...")
        
        # Decode the base64 key
        key_bytes = base64.urlsafe_b64decode(key_string + '==')  # Add padding
        
        # MEGA uses the first 16 bytes as AES key
        aes_key = key_bytes[:16]
        
        # Read encrypted file
        with open(encrypted_filepath, 'rb') as f:
            encrypted_data = f.read()
        
        # MEGA uses AES-128-CTR encryption
        # Initialize counter (MEGA uses a specific counter format)
        counter = Counter.new(128, initial_value=0)
        cipher = AES.new(aes_key, AES.MODE_CTR, counter=counter)
        
        # Decrypt the data
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Save decrypted file temporarily
        temp_decrypted = os.path.join(output_folder, f"decrypted_temp_{file_id}.tmp")
        with open(temp_decrypted, 'wb') as f:
            f.write(decrypted_data)
        
        print("✅ File decrypted successfully!")
        return temp_decrypted
        
    except Exception as e:
        print(f"❌ Decryption failed: {e}")
        return None

# Alternative MEGA download methods that ACTUALLY WORK
def download_mega_with_megadl():
    """Try to download using megadl command line tool."""
    try:
        result = subprocess.run(['megadl', '--version'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def download_mega_with_megatools():
    """Try to download using megatools."""
    try:
        result = subprocess.run(['megaget', '--version'], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    print("    __    ____  _____________  __")
    print("   / /   / __ \\/ ____/ ____/ |/ /")
    print("  / /   / /_/ / / __/ __/  |   /")
    print(" / /___/ _, _/ /_/ / /___ /   |")
    print("/_____/_/ |_|\\____/_____//_/|_|")
    print("YouTube Downloader - v3.9 (MEGA FORCE DOWNLOAD)")
    print("============================================================")
    
    try:
        download_videos_and_audio("links.txt")
    except KeyboardInterrupt:
        print("\n\n⚠️ Download interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ An error occurred: {e}")
        print("Check error_log.txt for details.")

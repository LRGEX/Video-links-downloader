#!/usr/bin/env python3
"""
Extract Missing MP3 Files
========================
This script checks for video files that don't have corresponding MP3 files
and extracts the audio for them.
"""

import os
import subprocess
import sys

def get_ffmpeg_path():
    """Get the path to FFmpeg, checking locally and in the system PATH."""
    # Check local ffmpeg first
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_ffmpeg = os.path.join(base_dir, "ffmpeg.exe")
    if os.path.exists(local_ffmpeg):
        print("✓ Using local FFmpeg")
        return local_ffmpeg
    
    # Check if FFmpeg is available globally in PATH
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("✓ Using system FFmpeg")
        return "ffmpeg"
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ FFmpeg not found!")
        return None

def extract_audio_to_mp3(video_path, audio_folder, ffmpeg_path):
    """Extract audio as MP3 format from a video file."""
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    mp3_path = os.path.join(audio_folder, f"{video_name}.mp3")
    
    if os.path.exists(mp3_path):
        print(f"✓ MP3 already exists: {mp3_path}")
        return mp3_path
    
    print(f"🎵 Extracting audio: {video_name}")
    try:
        subprocess.run([
            ffmpeg_path, "-y",
            "-i", video_path,
            "-q:a", "0", "-map", "a",
            mp3_path
        ], check=True, capture_output=True)
        print(f"✅ Created: {mp3_path}")
        return mp3_path
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to extract audio from {video_name}: {e}")
        return None

def main():
    # Get directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    video_folder = os.path.join(base_dir, "Videos")
    audio_folder = os.path.join(base_dir, "Audio")
    
    # Check if directories exist
    if not os.path.exists(video_folder):
        print(f"❌ Videos folder not found: {video_folder}")
        return
    
    if not os.path.exists(audio_folder):
        print(f"📁 Creating Audio folder: {audio_folder}")
        os.makedirs(audio_folder, exist_ok=True)
    
    # Get FFmpeg path
    ffmpeg_path = get_ffmpeg_path()
    if not ffmpeg_path:
        print("❌ Cannot proceed without FFmpeg")
        return
    
    # Get list of video files
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.wmv']
    video_files = []
    
    for filename in os.listdir(video_folder):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in video_extensions:
            video_files.append(filename)
    
    print(f"📁 Found {len(video_files)} video files")
    
    # Check which videos are missing MP3 files
    missing_mp3 = []
    for video_file in video_files:
        video_name = os.path.splitext(video_file)[0]
        mp3_file = f"{video_name}.mp3"
        mp3_path = os.path.join(audio_folder, mp3_file)
        
        if not os.path.exists(mp3_path):
            missing_mp3.append(video_file)
            print(f"❌ Missing MP3 for: {video_file}")
        else:
            print(f"✓ MP3 exists for: {video_file}")
    
    if not missing_mp3:
        print("🎉 All video files already have corresponding MP3 files!")
        return
    
    print(f"\n🎵 Extracting MP3 for {len(missing_mp3)} videos...")
    
    # Extract MP3 for missing files
    success_count = 0
    for video_file in missing_mp3:
        video_path = os.path.join(video_folder, video_file)
        result = extract_audio_to_mp3(video_path, audio_folder, ffmpeg_path)
        if result:
            success_count += 1
    
    print(f"\n🎉 Successfully extracted {success_count}/{len(missing_mp3)} MP3 files!")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")

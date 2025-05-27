
# Video and Audio Downloader

This Python script allows you to download videos and extract their audio from YouTube and TikTok links. The videos are saved in the MP4 format in a `Videos` folder, while the audio is extracted and saved in MP3 format in an `Audio` folder.

## Features
- **Download Videos**: Automatically downloads videos in MP4 format.
- **Extract Audio**: Extracts audio from the downloaded videos in MP3 format.
- **Format Compatibility**: Ensures that videos are always in MP4 format and audio in MP3 format.
- **Skip Existing Files**: Skips downloading or processing if a file (video or audio) already exists.
- **Error Logging**: Logs failed downloads in a `error_log.txt` file.

## Requirements
1. **Python 3.6+**
2. **FFmpeg**: Used for video conversion and audio extraction.
3. **yt-dlp**: For downloading videos and audio from YouTube, TikTok, and other platforms.

## Installation
1. Clone or download this repository.
2. Install the required Python libraries:
   ```bash
   pip install yt-dlp
   ```
3. Install FFmpeg:
   - The script automatically installs FFmpeg if it’s missing on **Windows**.
   - On **Linux/Mac**, install FFmpeg using your package manager:
     ```bash
     sudo apt install ffmpeg   # For Debian/Ubuntu
     brew install ffmpeg       # For macOS
     ```

## How to Use
1. Create a file named `links.txt` in the script directory.
2. Add your YouTube and TikTok links to `links.txt` (one link per line).

### Example `links.txt`
```
https://youtube.com/watch?v=example1
https://vt.tiktok.com/example2
https://youtube.com/watch?v=example3
```

3. How to Run the script:
   ```bash
    - double click on download_media.exe 
   or ( in case you have the main script.py)
   - python download_media.py
   ```

## Output
- **Videos Folder**: All downloaded videos are saved in the `Videos` folder in MP4 format.
- **Audio Folder**: Extracted audio files are saved in the `Audio` folder in MP3 format.
- **Error Log**: Any links that fail to process are logged in `error_log.txt` with the reason for failure.

## Notes
- Ensure that FFmpeg is correctly installed and accessible in your system's PATH.
- The script automatically skips files that already exist in the `Videos` or `Audio` folder.

---
## Link to Download the script
[LRGEX Video Downloader](https://github.com/LRGEX/Video-links-downloader/releases/download/v3.8/LRGEX.Video.Downloader.v3.8.exe)

**Developed by Hesham M. Alahdal**

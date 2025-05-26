
# Video and Audi## Requirements
1. **Python 3.10+**
2. **FFmpeg**: Used for video conversion and audio extraction
3. **yt-dlp**: For downloading videos from YouTube, TikTok, and other platforms
4. **Additional dependencies**: requests, beautifulsoup4, lxml, pycryptodome, pywin32

## Installation

### Option 1: Using UV Package Manager (Recommended)
1. Clone or download this repository
2. Install UV package manager if you don't have it:
   ```bash
   pip install uv
   ```
3. Install dependencies:
   ```bash
   uv sync
   ```

### Option 2: Using pip
1. Clone or download this repository
2. Install the required Python libraries:
   ```bash
   pip install yt-dlp requests beautifulsoup4 lxml pycryptodome pywin32
   ```

### FFmpeg Installation
- The script automatically downloads FFmpeg if it's missing on **Windows**
- On **Linux/Mac**, install FFmpeg using your package manager:
  ```bash
  sudo apt install ffmpeg   # For Debian/Ubuntu
  brew install ffmpeg       # For macOS
  ```
This Python script allows you to download videos and extract their audio from YouTube, TikTok, and MEGA.nz links. The videos are saved in the MP4 format in a `Videos` folder, while the audio is extracted and saved in MP3 format in an `Audio` folder.

## Features
- **Multi-Platform Support**: Downloads from YouTube, TikTok, and MEGA.nz
- **Anti-Bot Detection**: 5 fallback strategies with browser cookie extraction (Chrome/Firefox/Edge)
- **Download Videos**: Automatically downloads videos in MP4 format
- **Extract Audio**: Extracts audio from downloaded videos in MP3 format
- **Format Compatibility**: Ensures videos are always in MP4 format and audio in MP3 format
- **Auto-Cleanup**: Automatically organizes misplaced audio files
- **Skip Existing Files**: Skips downloading if files already exist
- **Error Logging**: Logs failed downloads in `error_log.txt` file
- **Colored ASCII Logo**: Enhanced visual interface
- **Hardware Acceleration**: GPU-accelerated encoding (NVIDIA/AMD/Intel)

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
1. Create a file named `links.txt` in the script directory
2. Add your YouTube, TikTok, and MEGA.nz links to `links.txt` (one link per line)

### Example `links.txt`
```
https://youtube.com/watch?v=example1
https://vt.tiktok.com/example2
https://mega.nz/file/example3
https://youtube.com/watch?v=example4
```

3. Run the script:
   ```bash
   # Option 1: Use the executable (recommended)
   ./VideoDownloader.exe
   
   # Option 2: Run Python script directly
   python download_media.py
   
   # Option 3: Using UV
   uv run python download_media.py
   ```

## Output
- **Videos Folder**: All downloaded videos are saved in the `Videos` folder in MP4 format
- **Audio Folder**: Extracted audio files are saved in the `Audio` folder in MP3 format
- **Error Log**: Any links that fail to process are logged in `error_log.txt` with the reason for failure

## Building Executable

To create your own executable file using PyInstaller:

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Create executable with custom icon
pyinstaller --onefile --icon="path/to/your/icon.ico" --name="VideoDownloader" --hidden-import=yt_dlp download_media.py

# Or using UV
uv run pyinstaller --onefile --icon="path/to/your/icon.ico" --name="VideoDownloader" --hidden-import=yt_dlp download_media.py
```

**PyInstaller flags explained:**
- `--onefile`: Creates a single executable file
- `--icon`: Embeds custom icon (optional)
- `--name`: Sets the executable name
- `--hidden-import=yt_dlp`: Ensures yt-dlp dynamic imports are included

## Notes
- The script automatically downloads FFmpeg if not found on Windows
- Files that already exist in `Videos` or `Audio` folders are automatically skipped
- MEGA downloads use yt-dlp as primary method with automatic fallback
- Browser cookies are automatically used for anti-bot detection
- GPU acceleration is automatically detected and used when available

---

## Download Links
- **Latest Release**: [VideoDownloader.exe](https://mega.nz/file/VxE1SCIC#s7iIWBiumPNVPBAA_-q3FNGF5pIiN4qXtYcKdGOYWco)
- **Source Code**: Available in this repository

## Version History
- **v3.7**: Added colored ASCII logo, removed MEGA.py conflicts, improved PyInstaller compatibility
- **v3.6**: Enhanced anti-bot detection, browser cookie support
- **v3.5**: Added MEGA.nz support, auto-cleanup features
- **Earlier versions**: Basic YouTube/TikTok downloading

**Developed by Hesham M. Alahdal**

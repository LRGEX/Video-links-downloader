# LRGEX Video Downloader v3.8

A powerful Python application for downloading videos and extracting audio from multiple platforms including YouTube, TikTok, and MEGA.nz. The application automatically organizes downloads into separate folders and provides advanced features like anti-bot detection and hardware acceleration.

## ⚠️ Important Legal Notice

**This tool is for educational and personal use only.**

- ✅ **Respect Copyright**: Only download content you own or have permission to download
- ✅ **Follow Platform Terms**: Comply with YouTube, TikTok, and MEGA.nz terms of service
- ✅ **Personal Use**: This tool is intended for personal, non-commercial use
- ✅ **Fair Use**: Ensure your usage complies with fair use and local copyright laws

**LRGEX is not responsible for misuse of this software. Users are solely responsible for ensuring their usage complies with applicable laws and platform terms of service.**

## ✨ Features

- **🌐 Multi-Platform Support**: Download from YouTube, TikTok, and MEGA.nz
- **🛡️ Anti-Bot Detection**: 5 fallback strategies with browser cookie extraction (Chrome/Firefox/Edge)
- **📹 Video Downloads**: Automatically downloads videos in MP4 format
- **🎵 Audio Extraction**: Extracts audio from downloaded videos in MP3 format
- **📁 Smart Organization**: Automatically organizes files into `Videos` and `Audio` folders
- **⏭️ Skip Existing Files**: Intelligently skips files that already exist
- **📝 Error Logging**: Comprehensive error logging in `error_log.txt`
- **🎨 Enhanced Interface**: Colored ASCII logo and user-friendly prompts
- **⚡ Hardware Acceleration**: GPU-accelerated encoding (NVIDIA/AMD/Intel)
- **🔄 Auto-Cleanup**: Automatically organizes misplaced audio files

## 🔧 Requirements

- **Python 3.10+**
- **FFmpeg**: For video conversion and audio extraction
- **UV Package Manager**: Modern Python package and project manager

## 📦 Installation

### 1. Install UV Package Manager
If you don't have UV installed, install it first:

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone the Repository
```bash
git clone <repository-url>
cd video-downloader
```

### 3. Install Dependencies
```bash
uv sync
```

This will automatically install all required dependencies:
- `yt-dlp`: For YouTube and TikTok downloads
- `requests`: For HTTP requests
- `mega.py`: For MEGA.nz downloads

### 4. FFmpeg Installation
- **Windows**: The script automatically downloads FFmpeg if missing
- **Linux**: `sudo apt install ffmpeg` (Debian/Ubuntu) or equivalent
- **macOS**: `brew install ffmpeg`

## 🚀 Usage

### 1. Prepare Your Links
Create a file named `links.txt` in the script directory and add your video links (one per line):

```bash
# Copy the example file and edit it
cp links.txt.example links.txt
# Edit links.txt with your video URLs
```

**Example `links.txt` content:**
```txt
https://youtube.com/watch?v=dQw4w9WgXcQ
https://vt.tiktok.com/ZSjQpFGHq/
https://mega.nz/file/ABC123XY#secretkey
https://youtube.com/watch?v=oHg5SJYRHA0
```

⚠️ **Privacy Note**: Never commit your `links.txt` file to version control as it may contain private URLs.

### 2. Run the Application

**Option 1: Using the pre-built executable (Recommended)**
```bash
./LRGEX_Video_Downloader_v3.8.exe
```

**Option 2: Run with UV**
```bash
uv run python LRGEX_Video_Downloader.py
```

**Option 3: Traditional Python execution**
```bash
python LRGEX_Video_Downloader.py
```

## 📂 Output Structure

The application creates the following directory structure:

```
project-directory/
├── Videos/           # Downloaded MP4 videos
├── Audio/            # Extracted MP3 audio files
├── links.txt         # Your input file with video links
├── error_log.txt     # Failed downloads log
└── LRGEX_Video_Downloader.py # Main application script
```

## 🛠️ Building Executable

To create your own executable using PyInstaller:

### 1. Install PyInstaller
```bash
uv add pyinstaller
```

### 2. Build the Executable
```bash
# Basic build
pyinstaller --onefile --name="LRGEX Video Downloader v3.8" LRGEX_Video_Downloader.py

# With custom icon and optimizations
pyinstaller --onefile \
    --exclude-module=pathlib \
    --icon="path/to/your/icon.ico" \
    --name="LRGEX Video Downloader v3.8" \
    LRGEX_Video_Downloader.py
```

### PyInstaller Options Explained:
- `--onefile`: Creates a single executable file
- `--exclude-module=pathlib`: Resolves MEGA.py compatibility issues
- `--icon`: Embeds a custom icon (optional)
- `--name`: Sets the executable name

## 🔧 Configuration

### Supported Platforms
| Platform | Support | Notes |
|----------|---------|--------|
| YouTube | ✅ Full | Includes shorts, playlists, live streams |
| TikTok | ✅ Full | Direct video downloads |
| MEGA.nz | ✅ Full | Direct file downloads |

### Hardware Acceleration
The application automatically detects and uses available hardware acceleration:
- **NVIDIA**: NVENC encoding
- **AMD**: AMF encoding  
- **Intel**: Quick Sync Video

## 🐛 Troubleshooting

### Common Issues

**1. "Unsupported URL" Error**
- Ensure the URL is from a supported platform
- Check if the video is private or geo-restricted

**2. FFmpeg Not Found**
- On Windows: The script auto-downloads FFmpeg
- On Linux/Mac: Install manually using package manager

**3. MEGA Download Fails**
- Check if the MEGA link is valid and accessible
- Ensure sufficient disk space

**4. Build Errors with PyInstaller**
- Use `--exclude-module=pathlib` flag for MEGA.py compatibility
- Ensure all dependencies are properly installed

### Error Logging
All failed downloads are logged in `error_log.txt` with detailed error messages for debugging.

## 📝 Dependencies

This project uses UV for dependency management. Dependencies are defined in `pyproject.toml`:

```toml
[project]
dependencies = [
    "yt-dlp>=2023.1.6",
    "requests>=2.28.0",
    "mega.py>=1.0.8"
]
```

## 🔄 Version History

- **v3.8**: Added MEGA.py integration, fixed PyInstaller compatibility
- **v3.7**: Enhanced error handling, improved UI
- **v3.6**: Added hardware acceleration support
- **v3.5**: Multi-platform support implementation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the error logs in `error_log.txt`

---

**Developed by LRGEX** | *Empowering digital content management*

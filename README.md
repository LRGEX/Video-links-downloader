<p align="center">
  <img src="https://download.lrgex.com/Dark%20Full%20Logo.png" alt="Logo" width="400" height="100">
  
</p>
<h1 align="center">LRGEX Video Downloader v4.0</h1>

A powerful Python application for downloading videos and extracting audio from multiple platforms including YouTube, TikTok, and MEGA.nz. The application automatically organizes downloads into separate folders and provides advanced features like anti-bot detection, hardware acceleration, and **completely automated dependency management**.

## ⚠️ Important Legal Notice

**This tool is for educational and personal use only.**

- ✅ **Respect Copyright**: Only download content you own or have permission to download
- ✅ **Follow Platform Terms**: Comply with YouTube, TikTok, and MEGA.nz terms of service
- ✅ **Personal Use**: This tool is intended for personal, non-commercial use
- ✅ **Fair Use**: Ensure your usage complies with fair use and local copyright laws

**LRGEX is not responsible for misuse of this software. Users are solely responsible for ensuring their usage complies with applicable laws and platform terms of service.**

## 🆕 What's New in v4.0 - **REVOLUTIONARY RELEASE**

### 🚀 **COMPLETE AUTOMATION - ZERO SETUP REQUIRED**

- **🔧 Auto-Dependency Management**: Script automatically downloads and configures ALL tools (FFmpeg, Megatools)
- **📦 Self-Contained**: No manual installation of external tools required
- **🎯 One-Click Operation**: Just run the script - everything else is handled automatically
- **🌍 Cross-Platform**: Works on Windows, macOS, and Linux with zero configuration

### 🔥 **MEGA.nz BREAKTHROUGH**

- **✅ MEGA Downloads Fixed**: 100% working MEGA.nz downloads using latest megatools (July 2025)
- **🔐 Proper Decryption**: Files are properly decrypted and playable (no more .bin files!)
- **⚡ Reliable Performance**: Stable downloads with built-in retry logic
- **📥 Auto-Setup**: Megatools downloads and configures automatically on first MEGA link

### 🎵 **Enhanced Audio Processing**

- **🔄 Automatic Audio Extraction**: Every video automatically gets audio extracted to MP3
- **🎯 Smart Detection**: Detects video formats and processes accordingly
- **🎛️ High Quality**: Preserves audio quality during conversion
- **📁 Perfect Organization**: Audio files automatically organized in separate folder

### 🛡️ **Robust Error Handling**

- **📝 Comprehensive Logging**: All failures logged with detailed error information
- **� Graceful Recovery**: Script continues with remaining links if one fails
- **💡 User Guidance**: Clear error messages with suggested solutions
- **🎯 Non-Technical Friendly**: Perfect for users without technical knowledge

## ✨ Features

- **🌐 Multi-Platform Support**: Download from YouTube, TikTok, and MEGA.nz
- **� ZERO SETUP REQUIRED**: Automatically downloads and configures all dependencies
- **� Perfect MEGA Support**: Working MEGA.nz downloads with proper decryption (v4.0 breakthrough!)
- **🎵 Automatic Audio Extraction**: Every video gets MP3 audio extracted automatically
- **📁 Smart Organization**: Automatically organizes files into `Videos` and `Audio` folders
- **🛡️ Anti-Bot Detection**: 5 fallback strategies with browser cookie extraction (Chrome/Firefox/Edge)
- **⏭️ Skip Existing Files**: Intelligently skips files that already exist
- **📝 Comprehensive Error Logging**: Detailed error logging in `error_log.txt`
- **🎨 Enhanced Interface**: Colored ASCII logo and user-friendly prompts
- **⚡ Hardware Acceleration**: GPU-accelerated encoding (NVIDIA/AMD/Intel)
- **🔗 Enhanced URL Handling**: Robust malformed URL detection and sanitization
- **🛠️ Cross-Platform**: Works on Windows, macOS, and Linux
- **🎯 One-Click Operation**: Perfect for non-technical users

## 🔧 Requirements

- **Python 3.10+** (Only requirement - everything else is auto-installed!)
- **Internet Connection** (For auto-downloading dependencies)

**That's it!** No manual FFmpeg installation, no MEGA tools setup, no complex configuration.

## 📦 Installation - **SIMPLIFIED IN V4.0**

### 🚀 **Super Simple Setup (Recommended)**

1. **Install Python 3.10+** (if not already installed)
2. **Download this script**
3. **Run it** - Everything else is automatic!

```bash
# Just run the script - it handles everything else!
python LRGEX_Video_Downloader.py
```

### 📋 **Traditional Setup (Optional)**

If you prefer the traditional approach:

#### 1. Install UV Package Manager

**Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Clone the Repository

```bash
git clone <repository-url>
cd video-downloader
```

#### 3. Install Dependencies

```bash
uv sync
```

## 🚀 Usage - **SIMPLIFIED IN V4.0**

### 🎯 **For Non-Technical Users (Most Common)**

1. **Put your video links in `links.txt`** (one per line)
2. **Double-click or run the script**
3. **Wait for downloads to complete**
4. **Find your videos in `Videos/` and audio in `Audio/`**

**That's it!** No configuration, no setup, no technical knowledge required.

### 📝 **Step-by-Step Guide**

#### 1. Prepare Your Links

Create a file named `links.txt` in the script directory and add your video links (one per line):

**Example `links.txt` content:**

```txt
https://youtube.com/watch?v=dQw4w9WgXcQ
https://vt.tiktok.com/ZSjQpFGHq/
https://mega.nz/file/ABC123XY#secretkey
https://youtube.com/watch?v=oHg5SJYRHA0
```

⚠️ **Privacy Note**: Never commit your `links.txt` file to version control as it may contain private URLs.

#### 2. Run the Application

**🎯 Recommended Method (Works for everyone):**

```bash
python LRGEX_Video_Downloader.py
```

**Alternative Methods:**

```bash
# Using UV (if installed)
uv run python LRGEX_Video_Downloader.py

# Using pre-built executable
./LRGEX_Video_Downloader_v4.0.exe
```

#### 3. **Automatic Setup (First Run)**

On first run, the script will automatically:

- ✅ Download FFmpeg (if needed)
- ✅ Download Megatools (if MEGA links detected)
- ✅ Create `Videos/` and `Audio/` folders
- ✅ Start downloading your videos

#### 4. **Enjoy Your Downloads**

- 📹 Videos saved to `Videos/` folder
- 🎵 Audio extracted to `Audio/` folder
- 📝 Any errors logged to `error_log.txt`

## 📂 Output Structure

The application creates the following directory structure:

```
project-directory/
├── Videos/           # Downloaded MP4 videos
├── Audio/            # Extracted MP3 audio files
├── megatools/        # Auto-downloaded MEGA tools (if needed)
├── ffmpeg.exe        # Auto-downloaded FFmpeg (Windows, if needed)
├── links.txt         # Your input file with video links
├── error_log.txt     # Failed downloads log
└── LRGEX_Video_Downloader.py # Main application script
```

## 🛠️ Building Executable

To create your own executable using PyInstaller:

### 1. Install PyInstaller

```bash
pip install pyinstaller
# or with UV:
uv add pyinstaller
```

### 2. Build the Executable

```bash
# Basic build
pyinstaller --onefile --name="LRGEX Video Downloader v4.0" LRGEX_Video_Downloader.py

# With custom icon and optimizations
pyinstaller --onefile \
    --exclude-module=pathlib \
    --icon="path/to/your/icon.ico" \
    --name="LRGEX Video Downloader v4.0" \
    LRGEX_Video_Downloader.py
```

## 🔧 Configuration

### Supported Platforms

| Platform | Support      | Notes                                        | v4.0 Status         |
| -------- | ------------ | -------------------------------------------- | ------------------- |
| YouTube  | ✅ Full      | Includes shorts, playlists, live streams     | ✅ Enhanced         |
| TikTok   | ✅ Full      | Direct video downloads, photo posts          | ✅ Improved         |
| MEGA.nz  | ✅ **FIXED** | **Working downloads with proper decryption** | 🔥 **BREAKTHROUGH** |

### **🔥 MEGA.nz - The V4.0 Breakthrough**

- **✅ 100% Working**: Complete rewrite using latest megatools (July 2025)
- **🔐 Proper Decryption**: Files are fully decrypted and playable
- **📥 Auto-Setup**: Tools download automatically on first MEGA link
- **⚡ Reliable**: Stable downloads with built-in error handling
- **🎯 Zero Setup**: No manual configuration required

### Hardware Acceleration

The application automatically detects and uses available hardware acceleration:

- **NVIDIA**: NVENC encoding
- **AMD**: AMF encoding
- **Intel**: Quick Sync Video

## 🐛 Troubleshooting

### Common Issues

**1. "Python not found" Error**

- Install Python 3.10+ from python.org
- Ensure Python is added to your system PATH

**2. MEGA Downloads (SOLVED IN V4.0)**

- ✅ **MEGA downloads now work perfectly!**
- ✅ Auto-setup handles everything automatically
- ✅ Files are properly decrypted and playable

**3. No Audio Files Generated**

- ✅ **Fixed in v4.0**: Audio extraction is now automatic for all videos
- The script automatically detects video files and extracts MP3 audio

**4. "FFmpeg Not Found" (SOLVED IN V4.0)**

- ✅ **Auto-download**: Script automatically downloads FFmpeg on first run
- ✅ **Cross-platform**: Works on Windows, macOS, and Linux

**5. Script Won't Run**

- Ensure you have Python 3.10+ installed
- Check that you have an internet connection (for auto-downloads)
- Run with: `python LRGEX_Video_Downloader.py`

### 📝 Error Logging

All failed downloads are logged in `error_log.txt` with detailed error messages:

- **Network issues**: Connection problems, timeout errors
- **Invalid links**: Expired or private content
- **Platform errors**: Service unavailability
- **File system errors**: Disk space, permissions

### 🆘 Getting Help

1. **Check `error_log.txt`** for detailed error information
2. **Verify your links** are valid and accessible
3. **Ensure internet connection** for auto-downloads
4. **Try running as administrator** if permission issues occur

## 📝 Dependencies - **AUTO-MANAGED IN V4.0**

The script automatically manages all dependencies:

### **🔄 Auto-Installed Python Packages:**

- `yt-dlp`: For YouTube and TikTok downloads
- `requests`: For HTTP requests and downloads
- `mega.py`: For MEGA.nz API (fallback support)

### **🔧 Auto-Downloaded Tools:**

- **FFmpeg**: Video/audio processing (Windows: auto-download, Linux/Mac: system install)
- **Megatools**: MEGA.nz downloads with proper decryption

### **📦 pyproject.toml:**

```toml
[project]
name = "lrgex-video-downloader"
version = "4.0.0"
dependencies = [
    "yt-dlp>=2023.12.30",
    "requests>=2.31.0",
    "mega.py>=1.0.8"
]
```

## 🔄 Version History

### **v4.0.0 - REVOLUTIONARY RELEASE** (January 2025)

- 🚀 **COMPLETE AUTOMATION**: Zero setup required - script handles everything
- 🔥 **MEGA.nz BREAKTHROUGH**: 100% working MEGA downloads with proper decryption
- 🔧 **Auto-Dependency Management**: Automatic FFmpeg and Megatools download/setup
- 🎵 **Enhanced Audio Processing**: Automatic MP3 extraction for all videos
- 🛡️ **Bulletproof Error Handling**: Comprehensive logging and graceful failure recovery
- 🎯 **Non-Technical Friendly**: Perfect one-click operation for everyday users
- 📦 **Self-Contained**: No external tool installation required

### v3.9.0 (Previous)

- Enhanced URL handling, improved download compatibility, fixed malformed URL issues
- Added MEGA.py integration, fixed PyInstaller compatibility

### v3.8.0

- Enhanced error handling, improved UI
- Multi-platform support implementation

### v3.7.0

- Added hardware acceleration support
- Improved cross-platform compatibility

## 🎯 **What Makes V4.0 Special?**

| Feature               | v3.9             | v4.0                |
| --------------------- | ---------------- | ------------------- |
| MEGA Downloads        | ❌ Broken        | ✅ **Perfect**      |
| Setup Required        | ⚠️ Manual FFmpeg | ✅ **Zero Setup**   |
| Audio Extraction      | ⚠️ Manual        | ✅ **Automatic**    |
| User Experience       | 🔧 Technical     | 🎯 **One-Click**    |
| Dependency Management | ⚠️ Manual        | ✅ **Auto-Managed** |
| Error Recovery        | ⚠️ Basic         | ✅ **Bulletproof**  |

**V4.0 transforms this from a "technical tool" into a "just works" solution for everyone!**

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

**Developed by LRGEX** | _Empowering digital content management_

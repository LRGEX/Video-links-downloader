# Changelog

All notable changes to LRGEX Video Downloader will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2025-01-14 - REVOLUTIONARY RELEASE 🚀

### 🔥 **BREAKTHROUGH FEATURES**

- **ZERO SETUP REQUIRED**: Complete automation - script auto-downloads and configures ALL dependencies
- **MEGA.nz FIXED**: 100% working MEGA downloads with proper decryption using latest megatools (July 2025)
- **AUTO-DEPENDENCY MANAGEMENT**: Automatic FFmpeg and Megatools download/setup on first run
- **ONE-CLICK OPERATION**: Perfect for non-technical users - just run and go
- **BULLETPROOF ERROR HANDLING**: Comprehensive logging and graceful failure recovery

### Added

- **Auto-Tool Management**: `ensure_ffmpeg()` and `ensure_megatools()` functions for automatic tool setup
- **Cross-Platform Auto-Setup**: Detects OS and downloads appropriate tools automatically
- **Enhanced MEGA Support**: Complete rewrite using megatools CLI for reliable downloads
- **Automatic Audio Extraction**: MP3 extraction for all downloaded videos
- **Smart Folder Management**: Auto-creation of Videos/ and Audio/ directories
- **Comprehensive Error Logging**: Detailed failure tracking in error_log.txt
- **Self-Contained Operation**: No manual installation of external tools required

### Changed

- **BREAKING**: Completely rewrote MEGA download logic using megatools instead of mega.py
- **BREAKING**: Removed manual FFmpeg setup requirement - now auto-managed
- **Enhanced User Experience**: Script handles all setup automatically on first run
- **Improved Error Recovery**: Script continues with remaining links if one fails
- **Updated Documentation**: Comprehensive README reflecting new zero-setup workflow

### Fixed

- **Critical**: MEGA.nz downloads now work perfectly with proper file decryption
- **Critical**: No more .bin files - all MEGA downloads are properly decrypted and playable
- **Resolved**: FFmpeg dependency issues - auto-download handles everything
- **Resolved**: Manual setup complexity - completely eliminated
- **Enhanced**: Cross-platform compatibility with auto-detection and setup

### Technical Improvements

- Implemented robust tool detection and auto-download functionality
- Added comprehensive OS detection for cross-platform tool management
- Enhanced error handling with graceful degradation and detailed logging
- Optimized download processes with retry logic and failure recovery
- Improved code organization with dedicated setup and utility functions

### Migration Notes

- **V3.x users**: Delete old megatools/ and ffmpeg installations - v4.0 manages everything automatically
- **New users**: Just run the script - zero setup required
- **All users**: Existing links.txt files work unchanged

## [3.9.0] - 2025-06-09

### Added

- Robust URL malformation handling with advanced regex patterns
- Enhanced PyInstaller executable creation with custom icon support
- Improved error handling for double question mark URL patterns

### Changed

- **BREAKING**: Removed restrictive yt-dlp format specifications for better compatibility
- Enhanced `sanitize_youtube_link()` function with multiple regex fallback patterns
- Updated yt-dlp to latest version for improved download reliability
- Improved download strategies to let yt-dlp automatically select best formats
- Updated ASCII logo to display v3.9

### Fixed

- **Critical**: Fixed malformed YouTube URLs with double question marks (e.g., `?v=VIDEO_ID?feature=shared`)
- Resolved pathlib package conflicts that caused import errors
- Fixed download failures caused by overly restrictive format selection
- Improved URL sanitization for various YouTube URL formats

### Technical Improvements

- Removed conflicting `pathlib` package from dependencies
- Enhanced regex patterns for YouTube URL validation and cleaning
- Optimized yt-dlp format selection for better success rates
- Improved PyInstaller build process with custom icon integration

## [3.8.0] - 2025-05-27

### Added

- Native MEGA.nz support via mega.py library
- Enhanced PyInstaller compatibility with `--exclude-module=pathlib`
- Professional documentation (README, CONTRIBUTING, SECURITY)
- Legal disclaimer and usage guidelines
- Sample links.txt.example file

### Changed

- Replaced yt-dlp MEGA support with dedicated mega.py integration
- Updated ASCII logo to display v3.8
- Improved error handling for MEGA downloads
- Enhanced .gitignore for better privacy protection

### Fixed

- PyInstaller pathlib conflicts resolved
- Double prompt issue in main function
- MEGA download reliability improvements

## [3.7.0] - 2024-02-20

### Added

- Multi-strategy anti-bot detection
- Browser cookie extraction support
- Colored ASCII logo interface
- Hardware acceleration support

### Changed

- Improved error handling and logging
- Enhanced file organization system

### Fixed

- Various download stability issues
- File cleanup and organization bugs

## [3.6.0] - Previous Release

### Added

- Basic multi-platform support
- TikTok download functionality
- FFmpeg auto-download for Windows

---

**Legend:**

- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes

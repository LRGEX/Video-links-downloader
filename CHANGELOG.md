# Changelog

All notable changes to LRGEX Video Downloader will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.1.0] - 2025-11-30 - CRITICAL BUG FIXES 🔧

### 🔥 **CRITICAL FIXES**

This release fixes critical bugs that made the PyInstaller-built .exe unusable. All users running v4.0 .exe should upgrade immediately.

### Fixed

#### **Critical Bug #1: EXE Spawning 30+ Processes**
- **Issue**: When running as .exe, the application spawned infinite processes (30+) causing system freeze and crash
- **Root Cause**: `subprocess.Popen([sys.executable, "-m", "gallery_dl"])` - when running as EXE, `sys.executable` points to the EXE itself, creating infinite recursion
- **Solution**:
  - Added `multiprocessing.freeze_support()` at start of main block to prevent PyInstaller process spawning
  - Replaced subprocess call with direct `gallery_dl.job.DownloadJob()` Python import
  - Updated PyInstaller spec to properly package all gallery_dl modules

#### **Critical Bug #2: TikTok Photo Posts Failing in EXE**
- **Issue**: TikTok photo posts worked perfectly in .py script but failed in .exe with `ModuleNotFoundError: No module named 'gallery_dl.extractor.2ch'`
- **Root Cause**: PyInstaller wasn't including all 100+ gallery_dl extractors (only manually listed ones in hiddenimports)
- **Solution**: Used `collect_submodules('gallery_dl')` in PyInstaller spec to auto-include all extractors

#### **Critical Bug #3: False Positive Errors in Logs**
- **Issue**: Error log (`error_log.txt`) showed failures for successfully downloaded TikTok photo posts, making debugging impossible
- **Root Cause**: Code tried yt-dlp first → failed → logged error → then switched to gallery-dl successfully
- **Solution**: Added `is_tiktok_photo_post()` function to detect photo posts BEFORE trying yt-dlp strategies, eliminating false errors

#### **Critical Bug #4: Photo Posts Downloaded Multiple Times**
- **Issue**: Running .exe multiple times re-downloaded the same photo posts (no duplicate detection)
- **Root Cause**: Filename used timestamp (`photo_post_audio_{time.time()}.mp3`) instead of photo ID, making every filename unique
- **Solution**: Extract photo ID from URL and use consistent naming (`tiktok_photo_{ID}.mp3`) with duplicate detection

### Added

- `is_tiktok_photo_post()` function for early photo post detection before download attempts
- Photo ID extraction from TikTok URLs for consistent file naming
- Duplicate detection for TikTok photo posts (checks if audio already exists before downloading)
- `multiprocessing.freeze_support()` call to prevent PyInstaller process spawning issues
- Comprehensive `collect_submodules('gallery_dl')` in PyInstaller spec for complete module inclusion

### Changed

- **Breaking**: TikTok photo post audio files now named `tiktok_photo_{ID}.mp3` instead of `photo_post_audio_{timestamp}.mp3` (consistent naming)
- Photo post detection moved from exception handler to pre-download validation (cleaner error handling)
- Gallery-dl now called directly via Python import instead of subprocess (works in both .py and .exe)
- PyInstaller spec now auto-collects all gallery_dl modules instead of manual listing

### Technical Improvements

- Eliminated subprocess-based gallery-dl execution (prevents EXE recursion)
- Improved error logging accuracy (only real errors logged, no false positives)
- Enhanced PyInstaller compatibility with proper module collection
- Optimized photo post handling with early detection and duplicate prevention
- Added proper process cleanup with `multiprocessing.freeze_support()`

### Migration Notes

- **V4.0 users**: Upgrade immediately if using .exe (critical bugs fixed)
- **Existing photo post audio files**: Old timestamp-based files will not be recognized as duplicates. Manually rename them to `tiktok_photo_{ID}.mp3` format or let script re-download with new names
- **PyInstaller builds**: Use new spec file (`LRGEX Video Downloader v4.1.spec`) for proper module inclusion

### Testing Performed

- ✅ .py script: All downloads working (YouTube, TikTok videos, TikTok photos, MEGA)
- ✅ .exe: All downloads working correctly
- ✅ .exe: Only 1-2 processes in Task Manager (not 30+)
- ✅ .exe: TikTok photo posts download successfully
- ✅ .exe: Duplicate detection works (skips re-downloads)
- ✅ Error logs: Only real errors logged (no false positives)

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

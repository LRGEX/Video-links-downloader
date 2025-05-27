# Contributing to LRGEX Video Downloader

Thank you for considering contributing to LRGEX Video Downloader! We welcome contributions from the community.

## 🤝 How to Contribute

### 1. Fork the Repository
- Click the "Fork" button on GitHub
- Clone your fork locally:
```bash
git clone https://github.com/yourusername/video-downloader.git
cd video-downloader
```

### 2. Set Up Development Environment
```bash
# Install UV package manager if you haven't already
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install dependencies
uv sync

# Create your feature branch
git checkout -b feature/amazing-feature
```

### 3. Development Guidelines

#### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and small

#### Testing
- Test your changes with multiple platforms (YouTube, TikTok, MEGA.nz)
- Ensure existing functionality isn't broken
- Test error handling scenarios

#### Documentation
- Update README.md if you add new features
- Add docstrings to new functions
- Update version history for significant changes

### 4. Types of Contributions Welcome

#### 🐛 Bug Fixes
- Fix download issues for specific platforms
- Improve error handling
- Fix compatibility issues

#### ✨ New Features
- Support for additional video platforms
- Improved user interface
- Performance optimizations
- Better file organization

#### 📚 Documentation
- Improve installation instructions
- Add troubleshooting guides
- Create usage examples

#### 🔧 Technical Improvements
- Code refactoring
- Dependency updates
- Security improvements

### 5. Submission Process

1. **Make your changes**
   - Write clean, documented code
   - Test thoroughly

2. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add support for new platform"
   ```

3. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

4. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Fill out the template with details about your changes

### 6. Pull Request Guidelines

#### Title Format
Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for code refactoring
- `test:` for adding tests

#### Description Should Include
- What changes were made
- Why the changes were necessary
- How to test the changes
- Any breaking changes

#### Example:
```
feat: add Instagram video download support

- Implemented Instagram post and reel download functionality
- Added instagram-dl dependency to pyproject.toml
- Updated README.md with Instagram usage examples
- Added error handling for private Instagram posts

Testing:
- Tested with public Instagram posts
- Tested with Instagram reels
- Verified error handling for private content
```

### 7. Code Review Process

1. **Automated checks** will run on your PR
2. **Maintainer review** - we'll review your code and provide feedback
3. **Address feedback** - make requested changes if needed
4. **Merge** - once approved, we'll merge your contribution

### 8. Platform-Specific Contributions

#### Adding New Platform Support
1. Research the platform's API/download methods
2. Implement download function following existing patterns
3. Add platform detection logic
4. Update documentation
5. Test thoroughly

#### Example structure for new platform:
```python
def download_newplatform_file(link, video_folder, audio_folder, ffmpeg_path):
    """Download videos from NewPlatform."""
    try:
        # Implementation here
        pass
    except Exception as e:
        print(f"Error downloading from NewPlatform: {e}")
        return False
    return True
```

### 9. Reporting Issues

Before creating a new issue:
- Check if the issue already exists
- Include detailed error messages
- Provide example URLs (if not private)
- Specify your operating system and Python version

### 10. Questions?

- Create an issue with the "question" label
- Check existing discussions
- Review the troubleshooting section in README.md

## 📝 Development Notes

### Project Structure
```
project/
├── download_media.py    # Main application
├── pyproject.toml      # Dependencies and project config
├── README.md           # User documentation
├── LICENSE             # MIT License
├── .gitignore          # Git ignore rules
└── links.txt.example   # Sample links file
```

### Key Dependencies
- `yt-dlp`: YouTube and TikTok downloads
- `requests`: HTTP requests
- `mega.py`: MEGA.nz downloads

### Building Executables
```bash
uv add pyinstaller
pyinstaller --onefile --exclude-module=pathlib --name="LRGEX Video Downloader v3.8" download_media.py
```

---

Thank you for contributing to LRGEX Video Downloader! 🚀

# Security Policy

## Supported Versions

We actively support the following versions of LRGEX Video Downloader:

| Version | Supported          |
| ------- | ------------------ |
| 3.8.x   | ✅ Yes             |
| 3.7.x   | ✅ Yes             |
| 3.6.x   | ⚠️ Limited support |
| < 3.6   | ❌ No              |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### 1. **DO NOT** create a public issue
Security vulnerabilities should not be disclosed publicly until they have been addressed.

### 2. Report privately
- **Email**: Create an issue with the title "SECURITY: [Brief Description]" and mark it as private
- **Include**: Detailed description, steps to reproduce, and potential impact

### 3. Information to include
- Type of vulnerability
- Steps to reproduce
- Affected versions
- Potential impact assessment
- Suggested fix (if you have one)

### 4. Response timeline
- **Initial response**: Within 48 hours
- **Status update**: Within 1 week
- **Fix deployment**: Varies by severity (1-30 days)

## Security Considerations for Users

### Safe Usage Guidelines

#### 1. **Link Sources**
- Only download content you have permission to download
- Be cautious with links from untrusted sources
- Verify link authenticity before processing

#### 2. **File Management**
- Regularly review downloaded content
- Use antivirus software to scan downloaded files
- Keep your system and dependencies updated

#### 3. **Privacy Protection**
- Don't share your `links.txt` file publicly
- Be aware that download logs may contain URLs
- Consider using VPN for additional privacy

#### 4. **Network Security**
- Downloads happen over public internet
- Some platforms may track download activity
- Consider network security implications

### Dependencies Security

Our application relies on several third-party libraries:
- `yt-dlp`: Regularly updated, actively maintained
- `requests`: Widely used, security-focused
- `mega.py`: Community maintained

**Recommendation**: Keep dependencies updated by running `uv sync` regularly.

### Platform-Specific Risks

#### YouTube/TikTok Downloads
- **Risk**: Rate limiting, IP blocking
- **Mitigation**: Built-in retry logic, respectful request timing

#### MEGA.nz Downloads
- **Risk**: Link expiration, access restrictions
- **Mitigation**: Proper error handling, user notifications

### Build Security

#### Executable Files
- Only use executables from trusted sources
- Verify checksums when available
- Be cautious with executables from unknown contributors

#### Building from Source
```bash
# Verify integrity of dependencies
uv sync --locked

# Build with security considerations
pyinstaller --onefile --exclude-module=pathlib download_media.py
```

## Known Security Limitations

### 1. **URL Validation**
- Basic URL validation is performed
- Malicious URLs could potentially cause issues
- **Mitigation**: User education, safe browsing practices

### 2. **File System Access**
- Application writes to local file system
- Potential for path traversal in filenames
- **Mitigation**: Filename sanitization implemented

### 3. **Network Requests**
- Application makes HTTP requests to external services
- DNS poisoning or man-in-the-middle attacks possible
- **Mitigation**: Use HTTPS when available, validate certificates

## Security Best Practices for Contributors

### Code Review
- All code changes require review
- Security implications are considered
- Dependencies are vetted before inclusion

### Dependency Management
- Regular dependency audits
- Prompt security updates
- Minimal dependency principle

### Error Handling
- Sensitive information not logged
- Graceful failure handling
- User-friendly error messages

## Disclosure Policy

### Responsible Disclosure
We follow responsible disclosure practices:
1. Security issues are fixed before public disclosure
2. Credit is given to security researchers (with permission)
3. Public advisories are issued for significant vulnerabilities

### Communication
- Security updates are announced in release notes
- Critical vulnerabilities trigger immediate releases
- Users are notified through appropriate channels

---

**Last Updated**: May 27, 2025
**Version**: 1.0

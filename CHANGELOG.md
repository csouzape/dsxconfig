# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-03-31

### Added
- **Complete Python implementation** — Rewritten from Go for better maintainability
- **Type hints** — Full Python type annotations for all functions and classes
- **Structured logging** — Colored, formatted logging system with proper error levels
- **Constants management** — Centralized configuration for all settings
- **Improved error handling** — Comprehensive try-catch with proper error messages
- **Shell script enhancements** — Generated scripts now include error handling and colored output
- **AUR helper detection** — Automatically detects and uses yay or paru
- **Safe package handling** — Proper shell escaping to prevent injection attacks
- **Better documentation** — Comprehensive docstrings for all modules and functions
- **Module exports** — Proper `__all__` declarations for clean APIs

### Changed
- **Script generation** — Now creates more robust restoration scripts with:
  - Color-coded logging output
  - Error handling with `set -e` and `set -u`
  - Better formatted output with progress messages
  - AUR helper auto-detection
  - Flathub remote auto-setup
- **Package manager detection** — More robust detection logic
- **FZF configuration** — Moved to constants for easier customization
- **Main menu** — Simplified and more intuitive flow

### Fixed
- **Error recovery** — System no longer crashes on missing dependencies
- **Timeout handling** — All subprocess calls now have proper timeouts
- **Distribution detection** — Better handling of ambiguous distro names (arch vs archlinux)
- **Flatpak detection** — Fixed header removal logic
- **Terminal compatibility** — Better handling of clear screen command

### Improved
- **Performance** — More efficient subprocess calls
- **User experience** — Better error messages and feedback
- **Code quality** — Proper separation of concerns with modular structure
- **Logging** — All operations now properly logged for debugging

### Deprecated
- Old bash-only script generation approach

### Removed
- N/A

## [1.0.0] - Previous Release

Initial stable release with basic functionality.

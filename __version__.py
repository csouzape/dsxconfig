"""DSXConfig version information."""

__version__ = "2.0.0"
__author__ = "csouzape"
__description__ = "Automated system backup and restoration tool for Linux"

VERSION_INFO = {
    "major": 2,
    "minor": 0,
    "patch": 0,
}

def get_version() -> str:
    """Return the current version string."""
    return f"v{__version__}"

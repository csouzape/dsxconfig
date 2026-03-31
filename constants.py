"""DSXConfig constants and configuration."""

from enum import Enum
from typing import Dict

# Version
APP_VERSION = "2.0.0"
APP_NAME = "DSXConfig"

# Supported package managers
class PackageManager(Enum):
    """Supported package managers."""
    PACMAN = "pacman"
    DNF = "dnf"
    APT = "apt"
    UNKNOWN = "unknown"


# Supported distributions
class Distribution(Enum):
    """Supported Linux distributions."""
    ARCH = "arch"
    ARCHLINUX = "archlinux"
    FEDORA = "fedora"
    RHEL = "rhel"
    CENTOS = "centos"
    DEBIAN = "debian"
    UBUNTU = "ubuntu"
    UNKNOWN = "unknown"


# Package manager commands
PKG_MGR_COMMANDS: Dict[str, list] = {
    "pacman": ["pacman", "-Qqen"],
    "dnf": ["dnf", "repoquery", "--userinstalled", "--queryformat", "%{name}"],
    "apt": ["apt-mark", "showmanual"],
}

# Update commands per distro
UPDATE_COMMANDS: Dict[str, str] = {
    "arch": "sudo pacman -Syu --noconfirm",
    "archlinux": "sudo pacman -Syu --noconfirm",
    "fedora": "sudo dnf update -y",
    "rhel": "sudo dnf update -y",
    "centos": "sudo dnf update -y",
    "debian": "sudo apt update && sudo apt upgrade -y",
    "ubuntu": "sudo apt update && sudo apt upgrade -y",
}

# Install commands per distro
INSTALL_COMMANDS: Dict[str, str] = {
    "arch": "sudo pacman -S --needed --noconfirm",
    "archlinux": "sudo pacman -S --needed --noconfirm",
    "fedora": "sudo dnf install -y",
    "rhel": "sudo dnf install -y",
    "centos": "sudo dnf install -y",
    "debian": "sudo apt install -y",
    "ubuntu": "sudo apt install -y",
}

# FZF Configuration
FZF_CONFIG = {
    "height": "40%",
    "layout": "reverse",
    "border": "rounded",
    "pointer": "▶",
    "marker": "✓",
    "color": "bg:#121212,bg+:#1e1e1e,fg:#d1d1d1,fg+:#ffffff,hl:#89b4fa,prompt:#cba6f7,pointer:#f38ba8,border:#2a2a2a",
    "header_single": "↑↓ Navigate · Enter Select · Esc Exit",
    "header_multi": "TAB Multi-select · Enter Confirm · Esc Exit",
}

# Script output settings
SCRIPT_PREFIX = "restore_dsx_"
SCRIPT_EXTENSION = ".sh"
SCRIPT_ENCODING = "utf-8"
SCRIPT_PERMISSIONS = 0o755

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "[%(levelname)s] %(message)s"

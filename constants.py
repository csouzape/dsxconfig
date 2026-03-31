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
    LINUXMINT = "linuxmint"
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
    "linuxmint": "sudo apt update && sudo apt upgrade -y",
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

# Cross-distro package name mappings (source -> target suggestion)
PACKAGE_NAME_MAP: Dict[str, Dict[str, str]] = {
    "python": {"pacman": "python", "apt": "python3", "dnf": "python3"},
    "python2": {"pacman": "python2", "apt": "python2", "dnf": "python2"},
    "python-pip": {"pacman": "python-pip", "apt": "python3-pip", "dnf": "python3-pip"},
    "pipenv": {"pacman": "pipenv", "apt": "pipenv", "dnf": "pipenv"},
    "nodejs": {"pacman": "nodejs", "apt": "nodejs", "dnf": "nodejs"},
    "npm": {"pacman": "npm", "apt": "npm", "dnf": "npm"},
    "git": {"pacman": "git", "apt": "git", "dnf": "git"},
    "git-lfs": {"pacman": "git-lfs", "apt": "git-lfs", "dnf": "git-lfs"},
    "vim": {"pacman": "vim", "apt": "vim", "dnf": "vim"},
    "neovim": {"pacman": "neovim", "apt": "neovim", "dnf": "neovim"},
    "nano": {"pacman": "nano", "apt": "nano", "dnf": "nano"},
    "zsh": {"pacman": "zsh", "apt": "zsh", "dnf": "zsh"},
    "fish": {"pacman": "fish", "apt": "fish", "dnf": "fish"},
    "htop": {"pacman": "htop", "apt": "htop", "dnf": "htop"},
    "glances": {"pacman": "glances", "apt": "glances", "dnf": "glances"},
    "gimp": {"pacman": "gimp", "apt": "gimp", "dnf": "gimp"},
    "vlc": {"pacman": "vlc", "apt": "vlc", "dnf": "vlc"},
    "firefox": {"pacman": "firefox", "apt": "firefox", "dnf": "firefox"},
    "libreoffice-fresh": {"pacman": "libreoffice-fresh", "apt": "libreoffice", "dnf": "libreoffice"},
    "docker": {"pacman": "docker", "apt": "docker.io", "dnf": "docker"},
    "docker-compose": {"pacman": "docker-compose", "apt": "docker-compose", "dnf": "docker-compose"},
    "podman": {"pacman": "podman", "apt": "podman", "dnf": "podman"},
    "openssh": {"pacman": "openssh", "apt": "openssh-server", "dnf": "openssh-server"},
    "firefox": {"pacman": "firefox", "apt": "firefox", "dnf": "firefox"},
    "chromium": {"pacman": "chromium", "apt": "chromium-browser", "dnf": "chromium"},
    "google-chrome": {"pacman": "google-chrome", "apt": "google-chrome-stable", "dnf": "google-chrome-stable"},
    "google-chrome-beta": {"pacman": "google-chrome", "apt": "google-chrome-beta", "dnf": "google-chrome-beta"},
    "brave-browser": {"pacman": "brave", "apt": "brave-browser", "dnf": "brave-browser"},
    "vivaldi": {"pacman": "vivaldi", "apt": "vivaldi", "dnf": "vivaldi"},
    "firefox": {"pacman": "firefox", "apt": "firefox", "dnf": "firefox"},
    "chromium-browser": {"pacman": "chromium", "apt": "chromium-browser", "dnf": "chromium"},
    "microsoft-edge": {"pacman": "microsoft-edge-stable", "apt": "microsoft-edge-stable", "dnf": "microsoft-edge-stable"},
    "teams": {"pacman": "teams", "apt": "teams", "dnf": "teams"},
    "slack": {"pacman": "slack-desktop", "apt": "slack-desktop", "dnf": "slack-desktop"},
    "telegram": {"pacman": "telegram-desktop", "apt": "telegram-desktop", "dnf": "telegram-desktop"},
    "signal-desktop": {"pacman": "signal-desktop", "apt": "signal-desktop", "dnf": "signal-desktop"},
    "zoom": {"pacman": "zoom", "apt": "zoom", "dnf": "zoom"},
    "wget": {"pacman": "wget", "apt": "wget", "dnf": "wget"},
    "curl": {"pacman": "curl", "apt": "curl", "dnf": "curl"},
    "tmux": {"pacman": "tmux", "apt": "tmux", "dnf": "tmux"},
    "screenfetch": {"pacman": "screenfetch", "apt": "screenfetch", "dnf": "screenfetch"},
    "exa": {"pacman": "exa", "apt": "exa", "dnf": "exa"},
    "ripgrep": {"pacman": "ripgrep", "apt": "ripgrep", "dnf": "ripgrep"},
    "fd": {"pacman": "fd", "apt": "fd-find", "dnf": "fd-find"},
    "bat": {"pacman": "bat", "apt": "bat", "dnf": "bat"},
    "fzf": {"pacman": "fzf", "apt": "fzf", "dnf": "fzf"},
    "rsync": {"pacman": "rsync", "apt": "rsync", "dnf": "rsync"},
    "make": {"pacman": "make", "apt": "make", "dnf": "make"},
    "gcc": {"pacman": "gcc", "apt": "gcc", "dnf": "gcc"},
    "clang": {"pacman": "clang", "apt": "clang", "dnf": "clang"},
    "openssl": {"pacman": "openssl", "apt": "openssl", "dnf": "openssl"},
    "sqlite": {"pacman": "sqlite", "apt": "sqlite3", "dnf": "sqlite"},
    "postgresql": {"pacman": "postgresql", "apt": "postgresql", "dnf": "postgresql"},
    "mysql": {"pacman": "mysql", "apt": "default-mysql-server", "dnf": "mysql-server"},
    "mariadb": {"pacman": "mariadb", "apt": "mariadb-server", "dnf": "mariadb-server"},
    "nodejs-legacy": {"pacman": "nodejs", "apt": "nodejs", "dnf": "nodejs"},
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

# Packages to ignore during export (system base packages, kernels, drivers, etc.)
IGNORED_PACKAGES = {
    # Base system packages
    "base", "base-devel", "linux", "linux-firmware", "linux-zen", "linux-lts",
    "linux-headers", "linux-zen-headers", "linux-lts-headers",
    
    # CPU microcode
    "intel-ucode", "amd-ucode",
    
    # GPU drivers
    "xf86-video-amdgpu", "xf86-video-ati", "xf86-video-nouveau", "xf86-video-intel",
    "vulkan-intel", "vulkan-radeon", "vulkan-nouveau", "intel-media-driver",
    "libva-intel-driver", "mesa", "lib32-mesa", "vulkan-icd-loader", "lib32-vulkan-icd-loader",
    "vulkan-radeon", "lib32-vulkan-radeon", "ocl-icd", "lib32-ocl-icd",
    
    # Desktop environments and window managers (but keep specific ones)
    "plasma-meta", "plasma-workspace", "sddm", "xdg-desktop-portal-hyprland",
    "xorg-server", "xorg-xinit", "xf86-input-libinput",
    
    # Audio/Video system components
    "pipewire", "pipewire-alsa", "pipewire-jack", "pipewire-pulse", "wireplumber",
    "alsa-utils", "alsa-plugins", "lib32-alsa-plugins", "libpulse", "lib32-libpulse",
    "gst-plugins-base-libs", "lib32-gst-plugins-base-libs", "gst-plugins-bad",
    "gst-plugins-ugly", "gst-libav", "gst-plugin-pipewire",
    
    # Network and Bluetooth system components
    "networkmanager", "network-manager-applet", "bluez", "bluez-utils", "iwd",
    "wpa_supplicant", "wireless_tools", "dnsmasq", "cups",
    
    # File systems and storage system tools
    "btrfs-progs", "efibootmgr", "zram-generator", "tlp", "smartmontools",
    
    # Virtualization system components
    "qemu-desktop", "virt-manager", "virt-viewer", "libguestfs",
    
    # Gaming and compatibility layers system components
    "wine", "gamemode", "lib32-gamemode", "mangohud", "lib32-mangohud",
    "steam", "lutris", "gamescope", "sof-firmware",
    
    # Development tools (but keep specific compilers/editors)
    "gcc", "make", "binutils", "fakeroot", "pacman", "sudo",
    
    # System utilities (but keep specific ones like htop, git, etc.)
    "bash-completion", "wget", "curl", "rsync", "tree", "nano",
    "openssh", "python", "python-pip",
    
    # Fonts (keep specific ones)
    "ttf-jetbrains-mono", "ttf-meslo-nerd",
    
    # Themes and appearance system components
    "materia-gtk-theme", "nwg-look", "xdg-utils",
    
    # Other system components
    "efibootmgr", "grub", "systemd", "dbus", "polkit", "cron", "logrotate",
    "pacman-mirrorlist", "archlinux-keyring", "ca-certificates", "openssl",
    
    # Libraries (keep specific application libraries)
    "glibc", "gcc-libs", "zlib", "bzip2", "xz", "lz4", "zstd", "libarchive",
    "readline", "ncurses", "lib32-ncurses", "sqlite", "lib32-sqlite",
    "libjpeg-turbo", "lib32-libjpeg-turbo", "libpng", "lib32-libpng",
    "giflib", "lib32-giflib", "gnutls", "lib32-gnutls", "libgcrypt", "lib32-libgcrypt",
    "libgpg-error", "lib32-libgpg-error", "libldap", "lib32-libldap",
    "libxcomposite", "lib32-libxcomposite", "libxinerama", "lib32-libxinerama",
    "libxslt", "lib32-libxslt", "mpg123", "lib32-mpg123", "v4l-utils", "lib32-v4l-utils",
    "openal", "lib32-openal", "sdl2-compat", "lib32-sdl2-compat",
}

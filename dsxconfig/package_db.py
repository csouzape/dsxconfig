from typing import Dict, Optional

# Adaptation database for common package names across distros.
# When a package has a different name on Arch, Fedora, openSUSE, etc., use this mapping.
PACKAGE_ADAPTATION_DB: Dict[str, Dict[str, str]] = {
    "python3": {"debian": "python3", "ubuntu": "python3", "arch": "python", "fedora": "python3", "opensuse": "python3"},
    "python": {"debian": "python3", "ubuntu": "python3", "arch": "python", "fedora": "python3", "opensuse": "python3"},
    "git": {"debian": "git", "ubuntu": "git", "arch": "git", "fedora": "git", "opensuse": "git"},
    "curl": {"debian": "curl", "ubuntu": "curl", "arch": "curl", "fedora": "curl", "opensuse": "curl"},
    "wget": {"debian": "wget", "ubuntu": "wget", "arch": "wget", "fedora": "wget", "opensuse": "wget"},
    "vim": {"debian": "vim", "ubuntu": "vim", "arch": "vim", "fedora": "vim", "opensuse": "vim"},
    "neovim": {"debian": "neovim", "ubuntu": "neovim", "arch": "neovim", "fedora": "neovim", "opensuse": "neovim"},
    "nodejs": {"debian": "nodejs", "ubuntu": "nodejs", "arch": "nodejs", "fedora": "nodejs", "opensuse": "nodejs"},
    "npm": {"debian": "npm", "ubuntu": "npm", "arch": "npm", "fedora": "npm", "opensuse": "npm"},
    "pip": {"debian": "python3-pip", "ubuntu": "python3-pip", "arch": "python-pip", "fedora": "python3-pip", "opensuse": "python3-pip"},
    "python-pip": {"debian": "python3-pip", "ubuntu": "python3-pip", "arch": "python-pip", "fedora": "python3-pip", "opensuse": "python3-pip"},
    "tmux": {"debian": "tmux", "ubuntu": "tmux", "arch": "tmux", "fedora": "tmux", "opensuse": "tmux"},
    "docker": {"debian": "docker.io", "ubuntu": "docker.io", "arch": "docker", "fedora": "docker", "opensuse": "docker"},
    "gimp": {"debian": "gimp", "ubuntu": "gimp", "arch": "gimp", "fedora": "gimp", "opensuse": "gimp"},
    "vlc": {"debian": "vlc", "ubuntu": "vlc", "arch": "vlc", "fedora": "vlc", "opensuse": "vlc"},
    "firefox": {"debian": "firefox", "ubuntu": "firefox", "arch": "firefox", "fedora": "firefox", "opensuse": "MozillaFirefox"},
    "code": {"debian": "code", "ubuntu": "code", "arch": "code", "fedora": "code", "opensuse": "code"},
    "chromium": {"debian": "chromium", "ubuntu": "chromium", "arch": "chromium", "fedora": "chromium", "opensuse": "chromium"},
}

SUPPORTED_DISTROS = ["debian", "ubuntu", "arch", "fedora", "opensuse"]

PACKAGE_ALIASES: Dict[str, str] = {
    "python": "python3",
    "python-pip": "pip",
}


class PackageAdaptationDB:
    @staticmethod
    def normalize_package_name(package_name: str) -> str:
        return package_name.strip().lower()

    @classmethod
    def resolve_family_name(cls, package_name: str) -> str:
        normalized = cls.normalize_package_name(package_name)
        return PACKAGE_ALIASES.get(normalized, normalized)

    @classmethod
    def adapt_package(cls, package_name: str, distro: str) -> str:
        key = cls.resolve_family_name(package_name)
        distro = distro.lower()
        package_map = PACKAGE_ADAPTATION_DB.get(key)
        if package_map and distro in package_map:
            return package_map[distro]
        return package_name

    @classmethod
    def supported_distros(cls):
        return SUPPORTED_DISTROS

    @classmethod
    def adaptation_report(cls, package_name: str) -> Dict[str, str]:
        key = cls.resolve_family_name(package_name)
        report = {distro: cls.adapt_package(package_name, distro) for distro in cls.supported_distros()}
        return report

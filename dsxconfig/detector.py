import os
import re
import shutil
import subprocess
from typing import Dict, List, Optional

from .package_db import PackageAdaptationDB


class SystemDetector:
    def __init__(self):
        self.os_release = self._parse_os_release()

    @staticmethod
    def _run_command(command: List[str]) -> str:
        try:
            completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True)
            return completed.stdout.strip()
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def command_exists(command: str) -> bool:
        return bool(shutil.which(command))

    def _parse_os_release(self) -> Dict[str, str]:
        result = {}
        try:
            with open("/etc/os-release", "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.rstrip().split("=", 1)
                        result[key.lower()] = value.strip().strip('"')
        except FileNotFoundError:
            pass
        return result

    def detect_distro(self) -> str:
        distro_id = self.os_release.get("id", "unknown").lower()
        if distro_id.startswith("ubuntu"):
            return "ubuntu"
        if distro_id.startswith("debian"):
            return "debian"
        if distro_id.startswith("arch"):
            return "arch"
        if distro_id.startswith("fedora"):
            return "fedora"
        if distro_id.startswith("opensuse") or distro_id.startswith("suse"):
            return "opensuse"
        return distro_id

    def detect_package_manager(self) -> Optional[str]:
        for candidate in ["apt", "dnf", "pacman", "zypper"]:
            if shutil.which(candidate):
                return candidate
        return None

    def list_flatpak_packages(self) -> List[str]:
        output = self._run_command(["flatpak", "list", "--app", "--columns=application"])
        return [line for line in output.splitlines() if line.strip()]

    def list_native_packages(self, manager: str) -> List[str]:
        if manager == "apt":
            output = self._run_command(["dpkg-query", "-W", "-f=${Package}\n"])
            return [line for line in output.splitlines() if line.strip()]
        if manager == "pacman":
            output = self._run_command(["pacman", "-Qq"])
            return [line for line in output.splitlines() if line.strip()]
        if manager == "dnf":
            output = self._run_command(["dnf", "repoquery", "--installed", "--queryformat", "%{name}\n"])
            if not output:
                output = self._run_command(["rpm", "-qa", "--qf", "%{NAME}\n"])
            return [line for line in output.splitlines() if line.strip()]
        if manager == "zypper":
            output = self._run_command(["rpm", "-qa", "--qf", "%{NAME}\n"])
            return [line for line in output.splitlines() if line.strip()]
        return []

    def list_aur_packages(self) -> List[str]:
        if shutil.which("pacman"):
            output = self._run_command(["pacman", "-Qm"])
            packages = []
            for line in output.splitlines():
                name = line.split()[0].strip()
                if name:
                    packages.append(name)
            return packages
        return []

    def detect_installed_apps(self) -> Dict[str, object]:
        manager = self.detect_package_manager()
        distro = self.detect_distro()
        native_packages = self.list_native_packages(manager) if manager else []
        aur_packages = self.list_aur_packages() if manager == "pacman" else []
        if manager == "pacman":
            aur_set = set(aur_packages)
            native_packages = [p for p in native_packages if p not in aur_set]
        flatpak_packages = self.list_flatpak_packages()
        return {
            "source_distro": distro,
            "package_manager": manager,
            "native_packages": sorted(set(native_packages)),
            "aur_packages": sorted(set(aur_packages)),
            "flatpak_packages": sorted(set(flatpak_packages)),
        }

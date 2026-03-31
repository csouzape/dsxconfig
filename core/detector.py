"""System detection and information gathering module."""

import os
import shutil
from typing import Optional
from constants import Distribution, PackageManager
from logger import get_logger

logger = get_logger(__name__)

__all__ = ["SystemInfo"]


class SystemInfo:
    """
    Detects and stores system information.

    Attributes:
        distro: Linux distribution ID
        name: Human-readable distribution name
        pkg_mgr: Detected package manager
    """

    distro: str
    pkg_mgr: str
    name: str

    def __init__(self) -> None:
        """Initialize SystemInfo and detect system details."""
        self.distro = "unknown"
        self.pkg_mgr = "unknown"
        self.name = "unknown"
        self.detect_system()

    def detect_system(self) -> None:
        """
        Identify the distribution and available package manager.

        Raises:
            RuntimeError: If system detection fails
        """
        try:
            self._detect_distro()
            self._detect_package_manager()
            logger.info(f"System detected: {self.name} ({self.pkg_mgr})")
        except Exception as e:
            logger.error(f"Failed to detect system: {e}")
            raise RuntimeError("Unable to detect system information") from e

    def _detect_distro(self) -> None:
        """Detect distribution from /etc/os-release."""
        if not os.path.exists("/etc/os-release"):
            logger.warning("Could not find /etc/os-release")
            return

        try:
            with open("/etc/os-release", encoding="utf-8") as f:
                info = {}
                for line in f:
                    if "=" in line:
                        key, value = line.rstrip().split("=", 1)
                        info[key] = value.strip('"')

                self.distro = info.get("ID", "unknown").lower()
                self.name = info.get("PRETTY_NAME", "Linux")
                logger.debug(f"Distribution detected: {self.distro}")
        except (IOError, OSError) as e:
            logger.error(f"Error reading os-release: {e}")

    def _detect_package_manager(self) -> None:
        """Detect available package manager."""
        managers = [
            (PackageManager.PACMAN.value, "pacman"),
            (PackageManager.DNF.value, "dnf"),
            (PackageManager.APT.value, "apt"),
        ]

        for pkg_name, cmd in managers:
            if shutil.which(cmd):
                self.pkg_mgr = pkg_name
                logger.debug(f"Package manager detected: {self.pkg_mgr}")
                return

        logger.warning("No supported package manager found")

    def __repr__(self) -> str:
        """Return string representation of SystemInfo."""
        return f"<SystemInfo: {self.name} ({self.pkg_mgr})>"

    def __str__(self) -> str:
        """Return human-readable string."""
        return f"{self.name} ({self.pkg_mgr})"


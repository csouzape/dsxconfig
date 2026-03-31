"""Package detection and retrieval module."""

import subprocess
from typing import List
from constants import PKG_MGR_COMMANDS
from logger import get_logger

logger = get_logger(__name__)

__all__ = ["get_native_packages", "get_aur_packages", "get_flatpaks"]


def get_native_packages(pkg_mgr: str) -> List[str]:
    """
    Get list of explicitly installed native packages.

    Args:
        pkg_mgr: Package manager name (pacman, dnf, apt)

    Returns:
        List of package names, empty list on error
    """
    if pkg_mgr not in PKG_MGR_COMMANDS:
        logger.warning(f"Unknown package manager: {pkg_mgr}")
        return []

    try:
        cmd = PKG_MGR_COMMANDS[pkg_mgr]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        packages = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        logger.info(f"Found {len(packages)} native packages ({pkg_mgr})")
        return packages

    except subprocess.TimeoutExpired:
        logger.error(f"Timeout while fetching packages from {pkg_mgr}")
        return []
    except subprocess.CalledProcessError as e:
        logger.error(f"Error fetching {pkg_mgr} packages: {e.stderr}")
        return []
    except FileNotFoundError:
        logger.error(f"Package manager '{pkg_mgr}' not found")
        return []
    except Exception as e:
        logger.error(f"Unexpected error getting native packages: {e}")
        return []


def get_aur_packages() -> List[str]:
    """
    Get list of AUR packages (Arch Linux only).

    Returns:
        List of AUR package names, empty list on error or non-Arch system
    """
    try:
        # -Qqm lists foreign packages (AUR/Manual)
        result = subprocess.run(
            ["pacman", "-Qqm"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        packages = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        logger.info(f"Found {len(packages)} AUR packages")
        return packages

    except subprocess.TimeoutExpired:
        logger.error("Timeout while fetching AUR packages")
        return []
    except subprocess.CalledProcessError as e:
        logger.debug(f"No AUR packages found or pacman not available: {e.stderr}")
        return []
    except FileNotFoundError:
        logger.debug("pacman not found (not Arch Linux)")
        return []
    except Exception as e:
        logger.error(f"Unexpected error getting AUR packages: {e}")
        return []


def get_flatpaks() -> List[str]:
    """
    Get list of installed Flatpak application IDs (apps only).

    Filters out runtimes and kernel modules, focusing on user applications.

    Returns:
        List of Flatpak application IDs, empty list on error or if not installed
    """
    try:
        # --app flag ignores runtimes/drivers and focuses on apps
        result = subprocess.run(
            ["flatpak", "list", "--app", "--columns=application"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )

        packages = [line.strip() for line in result.stdout.splitlines() if line.strip()]

        # Remove header if present (some flatpak versions include "Application")
        if packages and packages[0].lower() == "application":
            packages.pop(0)

        logger.info(f"Found {len(packages)} Flatpak applications")
        return packages

    except subprocess.TimeoutExpired:
        logger.error("Timeout while fetching Flatpak applications")
        return []
    except subprocess.CalledProcessError as e:
        logger.debug(f"No Flatpak applications found: {e.stderr}")
        return []
    except FileNotFoundError:
        logger.debug("flatpak not found (not installed)")
        return []
    except Exception as e:
        logger.error(f"Unexpected error getting Flatpak applications: {e}")
        return []

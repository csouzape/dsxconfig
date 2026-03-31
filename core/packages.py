"""Package detection and retrieval module."""

import subprocess
from typing import Dict, List
from constants import PKG_MGR_COMMANDS, PACKAGE_NAME_MAP, IGNORED_PACKAGES
from logger import get_logger

logger = get_logger(__name__)

__all__ = [
    "get_native_packages",
    "get_aur_packages",
    "get_flatpaks",
    "map_package_name",
    "map_packages_for_manager",
]


def map_package_name(package_name: str, target_pkg_mgr: str) -> str:
    """
    Return a target package name for the specified package manager.

    Args:
        package_name: Original package name from source system
        target_pkg_mgr: Target package manager (e.g., pacman, apt, dnf)

    Returns:
        Package name to install on target system (fallback to original)
    """
    normalized = package_name.strip().lower()
    if normalized in PACKAGE_NAME_MAP:
        alias = PACKAGE_NAME_MAP[normalized].get(target_pkg_mgr)
        if alias:
            logger.debug(
                f"Mapping package '{package_name}' -> '{alias}' for target manager {target_pkg_mgr}"
            )
            return alias
    return package_name


def map_packages_for_manager(packages: List[str], target_pkg_mgr: str) -> List[str]:
    """
    Convert a list of source packages to target package manager equivalents.

    Args:
        packages: Original package name list
        target_pkg_mgr: Target package manager

    Returns:
        Converted package name list
    """
    return [map_package_name(pkg, target_pkg_mgr) for pkg in packages]


def get_native_packages(pkg_mgr: str) -> List[str]:
    """
    Get list of explicitly installed native packages, filtering out system packages.

    Args:
        pkg_mgr: Package manager name (pacman, dnf, apt)

    Returns:
        List of package names (excluding system/base packages), empty list on error
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
        all_packages = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        
        # Filter out ignored packages (system base packages, kernels, drivers, etc.)
        filtered_packages = [pkg for pkg in all_packages if pkg not in IGNORED_PACKAGES]
        
        logger.info(f"Found {len(all_packages)} total native packages, {len(filtered_packages)} after filtering ({pkg_mgr})")
        return filtered_packages

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

"""DSXConfig main entry point."""

import os
import shutil
import subprocess
import sys
from typing import NoReturn

from __version__ import get_version
from constants import FZF_INSTALL_COMMANDS
from core.detector import SystemInfo
from core import packages
from cmd.export import ScriptExporter
from tui.interface import TUI
from logger import get_logger

logger = get_logger(__name__)

__all__ = ["main_menu", "main"]


def _ensure_fzf(sys_info: SystemInfo) -> None:
    """
    Make sure fzf is available, installing it via the system package manager
    if needed.

    fzf powers the interactive menu and is not shipped by default on
    Debian/Ubuntu/Mint. When it is missing we offer to install it using the
    detected package manager. If the user declines or the install fails, the
    menu falls back to a simple numeric selection.

    Args:
        sys_info: SystemInfo instance with the detected package manager
    """
    if shutil.which("fzf"):
        return

    print("\nfzf is required for the interactive menu but was not found.")

    cmd = FZF_INSTALL_COMMANDS.get(sys_info.pkg_mgr)
    if not cmd:
        logger.warning(f"No fzf install command for package manager: {sys_info.pkg_mgr}")
        print(
            f"Could not determine how to install fzf for '{sys_info.pkg_mgr}'.\n"
            "Please install it manually. Falling back to simple text selection."
        )
        return

    answer = input(f"Install it now with '{' '.join(cmd)}'? [Y/n] ").strip().lower()
    if answer in ("n", "no", "nao", "não"):
        logger.info("User declined fzf installation")
        print("Skipping fzf install. Falling back to simple text selection.")
        return

    try:
        logger.info(f"Installing fzf: {' '.join(cmd)}")
        result = subprocess.run(cmd)
        if result.returncode == 0 and shutil.which("fzf"):
            print("fzf installed successfully!\n")
            logger.info("fzf installed successfully")
        else:
            logger.error(f"fzf install failed (exit code {result.returncode})")
            print(
                "Failed to install fzf. Falling back to simple text selection."
            )
    except KeyboardInterrupt:
        print("\nInstallation cancelled. Falling back to simple text selection.")
    except Exception as e:
        logger.error(f"Error installing fzf: {e}")
        print(f"Error installing fzf: {e}. Falling back to simple text selection.")


def main_menu() -> NoReturn:
    """
    Display and handle the main application menu.

    Loops until the user exits. Avoids recursion to prevent stack overflow.
    """
    while True:
        try:
            TUI.clear()
            TUI.print_ascii_header()
            sys_info = SystemInfo()

            options = [
                "1 - Export System (Generate .sh)",
                "2 - View System Info",
                "3 - About",
                "0 - Exit",
            ]

            choice = TUI.run_fzf(options, prompt="DSXConfig >")

            if not choice or "0" in choice:
                logger.info("User exiting application")
                print("\nThank you for using DSXConfig!")
                sys.exit(0)

            if "1" in choice:
                _handle_export(sys_info)

            elif "2" in choice:
                _handle_system_info(sys_info)

            elif "3" in choice:
                _handle_about()

            else:
                logger.warning(f"Unknown choice: {choice}")
                input("\nInvalid option. Press Enter to continue...")

        except KeyboardInterrupt:
            logger.info("Application interrupted by user (Ctrl+C)")
            print("\n\nApplication interrupted. Exiting...")
            sys.exit(0)
        except SystemExit:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in main menu: {e}")
            input("\nAn error occurred. Press Enter to continue...")


def _handle_export(sys_info: SystemInfo) -> None:
    """
    Handle system export workflow.

    Args:
        sys_info: SystemInfo instance
    """
    try:
        print(f"\nStarting export for {sys_info.name}...")
        logger.info(f"Export started for {sys_info.distro}")

        exporter = ScriptExporter(sys_info)
        native, aur, flat = [], [], []

        # Scan native packages
        if exporter.confirm(f"Save {sys_info.pkg_mgr} packages?"):
            print(f"Scanning {sys_info.pkg_mgr}...")
            native = packages.get_native_packages(sys_info.pkg_mgr)
            print(f"   Found: {len(native)} packages")

        # Scan AUR packages (Arch only)
        if sys_info.distro in ["arch", "archlinux"]:
            if exporter.confirm("Save AUR packages?"):
                print("Scanning AUR...")
                aur = packages.get_aur_packages()
                print(f"   Found: {len(aur)} packages")

        # Scan Flatpak applications
        if exporter.confirm("Save Flatpak applications?"):
            print("Scanning Flatpak...")
            flat = packages.get_flatpaks()
            print(f"   Found: {len(flat)} applications")

        # Generate script
        if not (native or aur or flat):
            logger.warning("No packages selected for export")
            print("\nNo packages selected. Returning to menu...")
            input("Press Enter to continue...")
            return

        # Ask about system update
        include_update = exporter.confirm("Include system update in the script?")

        file_path = exporter.generate_script(native, aur, flat, include_update)

        if file_path:
            print(f"\nScript generated: {file_path}")
            print("Summary:")
            print(f"   • {len(native)} native packages")
            print(f"   • {len(aur)} AUR packages")
            print(f"   • {len(flat)} Flatpak applications")
            logger.info(
                f"Successfully generated script with "
                f"{len(native)} native, {len(aur)} AUR, {len(flat)} Flatpak packages"
            )
        else:
            print("\nFailed to generate script. Check logs for details.")
            logger.error("Script generation failed")

    except Exception as e:
        logger.error(f"Error during export: {e}")
        print(f"\nError: {e}")

    finally:
        input("\nPress Enter to return to menu...")


def _handle_system_info(sys_info: SystemInfo) -> None:
    """
    Display system information.

    Args:
        sys_info: SystemInfo instance
    """
    try:
        TUI.clear()
        TUI.print_header("System Information")

        kernel_release = os.uname().release
        print(f"  Distro:         {sys_info.name}")
        print(f"  ID:             {sys_info.distro}")
        print(f"  Kernel:         {kernel_release}")
        print(f"  Package Mgr:    {sys_info.pkg_mgr}")

        TUI.print_separator()
        logger.debug("System info displayed")

    except Exception as e:
        logger.error(f"Error displaying system info: {e}")
        print(f"\nError: {e}")

    finally:
        input("\nPress Enter to return...")


def _handle_about() -> None:
    """Display about information."""
    try:
        TUI.clear()
        TUI.print_header("About DSXConfig")

        version = get_version()
        print(f"  {version} - Automated system backup and restoration")
        print()
        print("  A tool to export your system configuration and packages,")
        print("  then restore it on a fresh installation of your OS.")
        print()
        print("  Repository: https://github.com/csouzape/dsxconfig")
        print("  License: MIT")
        TUI.print_separator()
        logger.debug("About dialog displayed")

    except Exception as e:
        logger.error(f"Error displaying about: {e}")
        print(f"\nError: {e}")

    finally:
        input("\nPress Enter to return...")


def main() -> None:
    """
    Main entry point for the application.

    Initializes the application and starts the main menu.
    """
    try:
        logger.info(f"DSXConfig starting (version {get_version()})")
        _ensure_fzf(SystemInfo())
        main_menu()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        print(f"\nFATAL ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

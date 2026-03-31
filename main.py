"""DSXConfig main entry point."""

import os
import sys
from typing import NoReturn

from __version__ import get_version
from core.detector import SystemInfo
from core import packages
from cmd.export import ScriptExporter
from tui.interface import TUI
from logger import get_logger

logger = get_logger(__name__)

__all__ = ["main_menu", "main"]


def main_menu() -> NoReturn:
    """
    Display and handle the main application menu.

    This function recursively calls itself after each action,
    creating an infinite loop until the user exits.
    """
    try:
        TUI.clear()
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

        main_menu()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user (Ctrl+C)")
        print("\n\nApplication interrupted. Exiting...")
        sys.exit(0)
    except SystemExit:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in main menu: {e}")
        input("\nAn error occurred. Press Enter to continue...")
        main_menu()


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

        file_path = exporter.generate_script(native, aur, flat)

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
        main_menu()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        print(f"\nFATAL ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

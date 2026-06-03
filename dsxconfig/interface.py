import shutil
import subprocess
from typing import List, Optional

from .detector import SystemDetector
from .generator import RestoreScriptGenerator
from .package_db import PackageAdaptationDB

ASCII_BANNER = r"""
██████╗ ███████╗██╗  ██╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗ 
██╔══██╗██╔════╝╚██╗██╔╝██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝ 
██║  ██║███████╗ ╚███╔╝ ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
██║  ██║╚════██║ ██╔██╗ ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
██████╔╝███████║██╔╝ ██╗╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝ 
"""

MENU_OPTIONS = [
    "1) export -> generate ~/dsxconfig_restore.sh",
    "2) summary -> show installed package counts",
    "3) db -> show adaptation database preview",
    "4) exit -> quit dsxconfig",
]


def run_fzf_menu(options: List[str]) -> Optional[str]:
    if not shutil.which("fzf"):
        return None

    header = f"{ASCII_BANNER}\nSelect an action"
    try:
        result = subprocess.run(
            [
                "fzf",
                "--prompt",
                "dsxconfig> ",
                "--ansi",
                "--no-sort",
                "--header",
                header,
                "--height=15",
                "--border=rounded",
            ],
            input="\n".join(options),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return result.stdout.strip() if result.stdout else None
    except Exception:
        return None


def prompt_menu(options: List[str]) -> Optional[str]:
    print(ASCII_BANNER)
    print("Choose an action:")
    for index, option in enumerate(options, start=1):
        print(f"  {index}) {option}")
    print("")

    try:
        choice = input("Enter number: ").strip()
    except KeyboardInterrupt:
        return None

    if not choice.isdigit():
        return None

    index = int(choice) - 1
    if 0 <= index < len(options):
        return options[index]
    return None


def choose_action() -> Optional[str]:
    selection = run_fzf_menu(MENU_OPTIONS)
    return selection or prompt_menu(MENU_OPTIONS)


def generate_script() -> None:
    detector = SystemDetector()
    state = detector.detect_installed_apps()
    generator = RestoreScriptGenerator()
    path = generator.generate_restore_script(state)
    print(f"Generated restore script: {path}")
    print("Use: bash ~/dsxconfig_restore.sh")


def show_summary() -> None:
    detector = SystemDetector()
    state = detector.detect_installed_apps()
    print(ASCII_BANNER)
    print("Installed package summary:")
    print(f"  Source distro: {state['source_distro']}")
    print(f"  Native packages: {len(state['native_packages'])}")
    print(f"  AUR packages: {len(state['aur_packages'])}")
    print(f"  Flatpak packages: {len(state['flatpak_packages'])}")


def show_db_preview() -> None:
    print(ASCII_BANNER)
    print("Adaptation database preview:")
    samples = ["python3", "git", "docker", "firefox"]
    for pkg in samples:
        report = PackageAdaptationDB.adaptation_report(pkg)
        print(f"  {pkg}: {report}")


def main() -> None:
    action = choose_action()
    if action is None:
        print("No selection made. Exiting.")
        return

    if action.startswith("export"):
        generate_script()
    elif action.startswith("summary"):
        show_summary()
    elif action.startswith("db"):
        show_db_preview()
    else:
        print("Exiting dsxconfig.")


if __name__ == "__main__":
    main()

import os
import stat
from pathlib import Path
from typing import Dict, List

from .package_db import PackageAdaptationDB


class RestoreScriptGenerator:
    def __init__(self, output_path: str = "~/dsxconfig_restore.sh"):
        self.output_path = os.path.expanduser(output_path)

    @staticmethod
    def _shell_list(items: List[str]) -> str:
        return "\n".join(f"{item}" for item in items)

    def _build_adapted_package_sets(self, packages: List[str]) -> Dict[str, List[str]]:
        result: Dict[str, List[str]] = {distro: [] for distro in PackageAdaptationDB.supported_distros()}
        for pkg in packages:
            for distro in PackageAdaptationDB.supported_distros():
                adapted = PackageAdaptationDB.adapt_package(pkg, distro)
                result[distro].append(adapted)
        return result

    def _quote_array(self, items: List[str]) -> str:
        return "\n".join(f"  \"{item}\"" for item in items)

    def generate_restore_script(self, state: Dict[str, object]) -> str:
        native_packages = state.get("native_packages", [])
        aur_packages = state.get("aur_packages", [])
        flatpak_packages = state.get("flatpak_packages", [])
        source_distro = state.get("source_distro", "unknown")
        package_manager = state.get("package_manager", "unknown")

        adapted_native = self._build_adapted_package_sets(native_packages)

        script_lines = [
            "#!/usr/bin/env bash",
            "set -e",
            "echo 'dsxconfig restore script starts.'",
            "echo 'This script detects the destination distribution and installs the exported apps.'",
            "echo 'If a package name cannot be adapted, the original name will be used and a warning is shown.'",
            "",
            "detect_distro() {",
            "  if [ -f /etc/os-release ]; then",
            "    . /etc/os-release",
            "    echo \"${ID}\" | tr '[:upper:]' '[:lower:]'",
            "  else",
            "    uname -s | tr '[:upper:]' '[:lower:]'",
            "  fi",
            "}",
            "",
            "detect_package_manager() {",
            "  if command -v apt >/dev/null 2>&1; then echo apt; return; fi",
            "  if command -v pacman >/dev/null 2>&1; then echo pacman; return; fi",
            "  if command -v dnf >/dev/null 2>&1; then echo dnf; return; fi",
            "  if command -v zypper >/dev/null 2>&1; then echo zypper; return; fi",
            "  echo unknown",
            "}",
            "",
            "install_native() {",
            "  local pkg_count=$#",
            "  if [ $pkg_count -eq 0 ]; then return; fi",
            "  case \"$DEST_PM\" in",
            "    apt)",
            "      sudo apt update && sudo apt install -y \"$@\";;",
            "    pacman)",
            "      sudo pacman -Sy --noconfirm \"$@\";;",
            "    dnf)",
            "      sudo dnf install -y \"$@\";;",
            "    zypper)",
            "      sudo zypper install -y \"$@\";;",
            "    *)",
            "      echo 'No known native package manager found for installation.';;",
            "  esac",
            "}",
            "",
            "install_flatpak() {",
            "  if [ $# -eq 0 ]; then return; fi",
            "  if ! command -v flatpak >/dev/null 2>&1; then",
            "    echo 'Flatpak is not installed on this system. Skipping flatpak packages.'",
            "    return",
            "  fi",
            "  for pkg in \"$@\"; do",
            "    echo 'Installing flatpak package:' $pkg",
            "    flatpak install -y flathub $pkg || echo 'Failed to install flatpak package:' $pkg",
            "  done",
            "}",
            "",
            "install_aur() {",
            "  if [ $# -eq 0 ]; then return; fi",
            "  if [ \"$DEST_PM\" != \"pacman\" ]; then",
            "    echo 'AUR packages are only supported on Arch-like destination systems. Skipping AUR packages.'",
            "    return",
            "  fi",
            "  if command -v yay >/dev/null 2>&1; then",
            "    yay -S --noconfirm \"$@\" || echo 'AUR installation failed for: $@'",
            "    return",
            "  fi",
            "  if command -v paru >/dev/null 2>&1; then",
            "    paru -S --noconfirm \"$@\" || echo 'AUR installation failed for: $@'",
            "    return",
            "  fi",
            "  echo 'No AUR helper found (yay or paru). Install AUR packages manually:' \"$@\"",
            "}",
            "",
            "warn_unadapted() {",
            "  local source_name=$1 dest_name=$2 distro=$3",
            "  if [ \"$source_name\" != \"$dest_name\" ]; then",
            "    echo \"[$distro] adapted $source_name -> $dest_name\"",
            "  else",
            "    echo \"[$distro] using $source_name\"",
            "  fi",
            "}",
            "",
            "DEST_DISTRO=$(detect_distro)",
            "DEST_PM=$(detect_package_manager)",
            "echo 'Detected destination distro:' $DEST_DISTRO",
            "echo 'Detected destination package manager:' $DEST_PM",
            "",
            "declare -a SOURCE_NATIVE_PACKAGES=(",
        ]

        for pkg in native_packages:
            script_lines.append(f"  \"{pkg}\"")
        script_lines.extend([
            ")",
            "declare -a SOURCE_FLATPAK_PACKAGES=(",
        ])
        for pkg in flatpak_packages:
            script_lines.append(f"  \"{pkg}\"")
        script_lines.extend([
            ")",
            "declare -a SOURCE_AUR_PACKAGES=(",
        ])
        for pkg in aur_packages:
            script_lines.append(f"  \"{pkg}\"")
        script_lines.extend([
            ")",
            "",
            "declare -A ADAPTER_DEBIAN=(",
        ])

        for pkg in native_packages:
            adapted = PackageAdaptationDB.adapt_package(pkg, "debian")
            script_lines.append(f"  [\"{pkg}\"]=\"{adapted}\"")
        script_lines.extend([
            ")",
            "declare -A ADAPTER_UBUNTU=(",
        ])
        for pkg in native_packages:
            adapted = PackageAdaptationDB.adapt_package(pkg, "ubuntu")
            script_lines.append(f"  [\"{pkg}\"]=\"{adapted}\"")
        script_lines.extend([
            ")",
            "declare -A ADAPTER_ARCH=(",
        ])
        for pkg in native_packages:
            adapted = PackageAdaptationDB.adapt_package(pkg, "arch")
            script_lines.append(f"  [\"{pkg}\"]=\"{adapted}\"")
        script_lines.extend([
            ")",
            "declare -A ADAPTER_FEDORA=(",
        ])
        for pkg in native_packages:
            adapted = PackageAdaptationDB.adapt_package(pkg, "fedora")
            script_lines.append(f"  [\"{pkg}\"]=\"{adapted}\"")
        script_lines.extend([
            ")",
            "declare -A ADAPTER_OPENSUSE=(",
        ])
        for pkg in native_packages:
            adapted = PackageAdaptationDB.adapt_package(pkg, "opensuse")
            script_lines.append(f"  [\"{pkg}\"]=\"{adapted}\"")
        script_lines.extend([
            ")",
            "",
            "declare -a DEST_NATIVE_PACKAGES=()",
            "for pkg in \"${SOURCE_NATIVE_PACKAGES[@]}\"; do",
            "  case \"$DEST_DISTRO\" in",
            "    debian) DEST_NATIVE_PACKAGES+=(\"${ADAPTER_DEBIAN[$pkg]}\") ;;",
            "    ubuntu) DEST_NATIVE_PACKAGES+=(\"${ADAPTER_UBUNTU[$pkg]}\") ;;",
            "    arch) DEST_NATIVE_PACKAGES+=(\"${ADAPTER_ARCH[$pkg]}\") ;;",
            "    fedora) DEST_NATIVE_PACKAGES+=(\"${ADAPTER_FEDORA[$pkg]}\") ;;",
            "    opensuse) DEST_NATIVE_PACKAGES+=(\"${ADAPTER_OPENSUSE[$pkg]}\") ;;",
            "    *) DEST_NATIVE_PACKAGES+=(\"$pkg\") ;;",
            "  esac",
            "done",
            "",
            "echo 'Native packages to install:'",
            "printf '  %s\n' \"${DEST_NATIVE_PACKAGES[@]}\"",
            "echo 'Flatpak packages to install:'",
            "printf '  %s\n' \"${SOURCE_FLATPAK_PACKAGES[@]}\"",
            "echo 'AUR candidate packages:'",
            "printf '  %s\n' \"${SOURCE_AUR_PACKAGES[@]}\"",
            "",
            "install_native \"${DEST_NATIVE_PACKAGES[@]}\"",
            "install_flatpak \"${SOURCE_FLATPAK_PACKAGES[@]}\"",
            "install_aur \"${SOURCE_AUR_PACKAGES[@]}\"",
            "",
            "echo 'dsxconfig restore finished.'",
        ])

        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(script_lines) + "\n")
        st = os.stat(self.output_path)
        os.chmod(self.output_path, st.st_mode | stat.S_IEXEC)
        return self.output_path

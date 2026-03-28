import os
from datetime import datetime

def generate_script(packages, flatpaks, configs, distro, shell):
    lines = []
    
    lines.append("#!/usr/bin/env bash")
    lines.append(f"# dsxconfig export - {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"# source distro: {distro}")
    lines.append("")
    lines.append("set -uo pipefail")
    lines.append("")
    lines.append("detect_distro() {")
    lines.append("    local id=$(grep '^ID=' /etc/os-release | cut -d= -f2 | tr -d '\"' | tr '[:upper:]' '[:lower:]')")
    lines.append("    local id_like=$(grep '^ID_LIKE=' /etc/os-release | cut -d= -f2 | tr -d '\"' | tr '[:upper:]' '[:lower:]')")
    lines.append("    if [[ \"$id\" == 'arch' ]] || [[ \"$id_like\" == *'arch'* ]]; then echo 'arch'")
    lines.append("    elif [[ \"$id\" == 'fedora' ]] || [[ \"$id_like\" == *'fedora'* ]]; then echo 'fedora'")
    lines.append("    else echo 'debian'; fi")
    lines.append("}")
    lines.append("")
    lines.append("DISTRO=$(detect_distro)")
    lines.append("")
    pkg_list = " ".join(packages)
    lines.append("install_packages() {")
    lines.append(f"    PACKAGES=\"{pkg_list}\"")
    lines.append("    case \"$DISTRO\" in")
    lines.append("        arch)   sudo pacman -S --noconfirm --needed $PACKAGES ;;")
    lines.append("        fedora) sudo dnf install -y $PACKAGES ;;")
    lines.append("        *)      sudo apt-get install -y $PACKAGES ;;")
    lines.append("    esac")
    lines.append("}")
    lines.append("")

    if flatpaks:
        lines.append("install_flatpak() {")
        for app in flatpaks:
            lines.append(f"    flatpak install -y --system flathub {app} || flatpak install -y --user flathub {app}")
        lines.append("}")
        lines.append("")

    lines.append("main() {")
    lines.append("    install_packages")
    if flatpaks:
        lines.append("    install_flatpak")
    lines.append("}")
    lines.append("")
    lines.append("main")
    
    return "\n".join(lines)
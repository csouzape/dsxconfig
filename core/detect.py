import os
import shutil 

def detect_distro():
    values = {}
    
    with open("/etc/os-release") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                values[key] = val.strip('"').lower()
    
    distro_id = values.get("ID", "")
    id_like = values.get("ID_LIKE", "")
    
    if distro_id == "arch" or "arch" in id_like:
        return "arch"
    
    if distro_id in ("debian", "ubuntu", "linuxmint", "pop") or \
        "debian" in id_like or "ubuntu" in id_like:
        return "debian"
    
    if distro_id == "fedora" or "fedora" in id_like:
        return "fedora"
    
    return "unknown"

def detect_shell():
    return os.environ.get("SHELL", "").split("/")[-1]

def detect_terminals():
    home = os.path.expanduser("~")
    terminals = {
        "alacritty": f"{home}/.config/alacritty",
        "kitty":     f"{home}/.config/kitty",
        "ghostty":   f"{home}/.config/ghostty",
        "wezterm":   f"{home}/.config/wezterm",
    }
    found = []
    for name, path in terminals.items():
        if os.path.exists(path):
            found.append(name)
    return found


def detect_fetch():
    fetches = ["fastfetch", "neofetch", "pfetch", "screenfetch"]
    found = []
    for fetch in fetches:
        if shutil.which(fetch):
            found.append(fetch)
    return found 
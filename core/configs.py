import os

def detect_configs(terminals, shell):
    home = os.path.expanduser("~")
    configs = {}

    shell_configs = {
        "bash": [f"{home}/.bashrc", f"{home}/.bash_profile"],
        "zsh":  [f"{home}/.zshrc"],
        "fish": [f"{home}/.config/fish"],
    }

    for path in shell_configs.get(shell, []):
        if os.path.exists(path):
            configs[path] = path

    terminal_configs = {
        "alacritty": f"{home}/.config/alacritty",
        "kitty":     f"{home}/.config/kitty",
        "ghostty":   f"{home}/.config/ghostty",
        "wezterm":   f"{home}/.config/wezterm",
    }

    for terminal in terminals:
        path = terminal_configs.get(terminal)
        if path and os.path.exists(path):
            configs[terminal] = path

    return configs
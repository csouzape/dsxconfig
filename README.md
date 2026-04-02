<div align="center">

```
   ██████╗ ███████╗██╗  ██╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗
   ██╔══██╗██╔════╝╚██╗██╔╝██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝
   ██║  ██║███████╗ ╚███╔╝ ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
   ██║  ██║╚════██║ ██╔██╗ ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
   ██████╔╝███████║██╔╝ ██╗╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝
```

**Backup and restore your Linux setup — fast, portable, cross-distro.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python)](https://www.python.org)
[![License](https://img.shields.io/github/license/csouzape/dsxconfig)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://github.com/csouzape/dsxconfig/releases)

</div>

---

## What is dsxconfig?

`dsxconfig` is a TUI tool that exports your Linux system package setup — native packages, AUR packages, and Flatpak applications — into a portable bash script. Restore everything on a new machine in one run.

No full disk images. No 400GB clones. Just your packages and a restoration script.

---

## Features v2.0.0 

- ** Interactive TUI** — fzf-based interface for seamless navigation
- ** Smart detection** — automatically detects your distro and package manager
- ** Multi-source backup** — captures native packages, AUR packages, and Flatpak apps
- ** Cross-distro restore** — generates portable bash scripts that work across distros
- ** Robust error handling** — comprehensive logging and error recovery
- ** Type hints** — full Python type annotations for safety and IDE support
- ** Security** — safe package name handling with proper shell escaping
- ** Beautiful output** — colored logging and formatted terminal output

---

## What's New in v2.0.0

✓ Complete rewrite with type hints and proper error handling  
✓ Centralized logging system with colored output  
✓ Constants management for easier configuration  
✓ Modular architecture with clear separation of concerns  
✓ Improved script generation with error recovery  
✓ AUR helper detection (yay/paru)  
✓ Better package shell escaping to prevent injection attacks  
✓ Comprehensive docstrings and inline documentation  

---

## Supported distros

| Distro | Package Manager | Export | Restore |
|--------|---|--------|---------|
| Arch Linux | pacman | ✓ | ✓ |
| Debian / Ubuntu / Mint | apt | ✓ | ✓ |
| Fedora / RHEL / CentOS | dnf | ✓ | ✓ |

---

## Requirements

- Python 3.8+
- `fzf` — interactive fuzzy finder
- `flatpak` (optional) — for Flatpak app support

### Install dependencies

**Arch Linux:**
```bash
sudo pacman -S fzf python
```

**Debian/Ubuntu:**
```bash
sudo apt install fzf python3
```

**Fedora:**
```bash
sudo dnf install fzf python3
```

**Install fzf:**
```bash
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
```

---

## Installation

### Clone and run
```bash
git clone https://github.com/csouzape/dsxconfig.git
cd dsxconfig
python3 main.py
```

### Create alias (optional)
```bash
alias dsxconfig="cd /path/to/dsxconfig && python3 main.py"
```

---

## Usage

Launch the application:
```bash
python3 main.py
```

### Interactive menu:
```
DSXConfig >
1 - Export System (Generate .sh)
2 - View System Info
3 - About
0 - Exit
```

### Export workflow:
1. Select "Export System"
2. Choose which package types to backup (native, AUR, Flatpak)
3. Script is generated as `restore_dsx_YYYYMMDD.sh`
4. Transfer script to your new system and run it

### Restore on new system:
```bash
chmod +x restore_dsx_*.sh
./restore_dsx_*.sh
```

---

## Generated script features

The restoration script includes:
- Automatic system update
- Safe package installation with `--needed` flag
- Error handling and logging
- Colored output (INFO, WARN, ERROR)
- Support for multiple AUR helpers (yay/paru)
- Automatic flathub remote setup



---

## Troubleshooting

### "fzf not found"
Install fzf: https://github.com/junegunn/fzf#installation

### "No supported package manager found"
Your distro may not be supported. Edit `constants.py` to add support.

### "No packages found"
Run with logging enabled to see what commands are failing:
```python
# Edit logger.py and change LOG_LEVEL to "DEBUG"
```

---

## Contributing

Issues and PRs are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT © [csouzape](https://github.com/csouzape)

---

## Changelog

### v2.0.0 (31/03/2026)
-  Complete Python implementation
-  Type hints and improved error handling
- 🔧 Modular architecture with constants management
-  Full documentation and inline comments
- Improved performance and stability


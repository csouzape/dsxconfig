<div align="center">

```
   ██████╗ ███████╗██╗  ██╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗
   ██╔══██╗██╔════╝╚██╗██╔╝██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝
   ██║  ██║███████╗ ╚███╔╝ ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
   ██║  ██║╚════██║ ██╔██╗ ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
   ██████╔╝███████║██╔╝ ██╗╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝
```

# 🔧 DSXConfig — Save Your Linux Programs in One File

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python)](https://www.python.org)
[![License](https://img.shields.io/github/license/csouzape/dsxconfig)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://github.com/csouzape/dsxconfig/releases)

**Part of the [DSXTool](https://github.com/csouzape/dsxtool) ecosystem** 🚀

</div>

---

## 🤔 What is DSXConfig?

Imagine you have a computer with **all your favorite programs installed**. Now you want to:
- Switch to a new computer
- Reinstall Linux from scratch
- Move to a different distribution
- Share your setup with friends

**Without losing a single program!**

**DSXConfig does exactly that:** it **saves a list of all your programs** in a file that can be run on any other Linux computer to automatically install everything.

### 💡 Simple Analogy:
Think of it like a **shopping list** for your installation. Instead of remembering every program you have, DSXConfig creates a complete list that you can use as many times as you want.

---

## 📦 What Programs Does It Save?

DSXConfig saves **3 types of programs**:

| Type | What is it? | Examples |
|------|-----------|----------|
| **Native Packages** | Programs from your Linux package manager | Firefox, Git, VS Code |
| **AUR** (Arch only) | Extra programs from Arch Linux community | Spotify, Discord |
| **Flatpak** | Portable programs that work on any Linux | Blender, OBS |

---

## 🚀 Part of DSXTool

**DSXConfig is built into [DSXTool](https://github.com/csouzape/dsxtool)** — a comprehensive Linux management suite. You can use:

- ✅ **Standalone** — Use DSXConfig directly with `python3 main.py`
- ✅ **Integrated** — Use it as part of DSXTool for advanced features
- ✅ **Full Control** — All features available in both modes

Learn more at [DSXTool GitHub](https://github.com/csouzape/dsxtool)

---

## ✨ What Makes It Special?

✅ **Easy to use** — Interactive menus with fzf  
✅ **Fast** — Automatic save and restore  
✅ **Safe** — Doesn't touch system files  
✅ **Portable** — Works on any Linux distribution  
✅ **Automatic** — Just click and let it do the work  
✅ **Cross-distro** — Ubuntu → Fedora → Arch (no problem!)  

---

## 🖥️ Supported Linux Distributions

| Linux | Support |
|-------|---------|
| **Arch Linux** | ✅ Full Support |
| **Ubuntu / Debian / Linux Mint** | ✅ Full Support |
| **Fedora / Red Hat / CentOS** | ✅ Full Support |

---

## 📋 Requirements

You need only **2 things**:

### 1️⃣ Python 3.8+
Most Linux distributions come with Python pre-installed. Check:
```bash
python3 --version
```

If not installed:

**Arch Linux:**
```bash
sudo pacman -S python
```

**Ubuntu/Debian:**
```bash
sudo apt install python3
```

**Fedora:**
```bash
sudo dnf install python3
```

### 2️⃣ FZF (Interactive Finder)
A small tool that makes the interface interactive. Install it:

**Arch Linux:**
```bash
sudo pacman -S fzf
```

**Ubuntu/Debian:**
```bash
sudo apt install fzf
```

**Fedora:**
```bash
sudo dnf install fzf
```

---

## 🚀 Installation

### Step 1: Download
```bash
git clone https://github.com/csouzape/dsxconfig.git
cd dsxconfig
```

If you don't have `git`:
```bash
sudo apt install git    # Ubuntu/Debian
sudo pacman -S git      # Arch
sudo dnf install git    # Fedora
```

### Step 2: Run
```bash
python3 main.py
```

That's it! No installation needed.

---

## 📖 How to Use — Step by Step

### 🎯 Goal 1: Save Your Programs

#### Step 1: Launch the program
```bash
python3 main.py
```

You'll see a menu:
```
================================================
  DSXConfig System Restoration
  Target: Ubuntu 22.04 LTS
================================================

DSXConfig >
  1 - Export System (Generate .sh)
  2 - View System Info
  3 - About
  0 - Exit
```

> 📸 **Screenshot Tip:** This is a good place to take a screenshot of the main menu for documentation.

#### Step 2: Choose "Export System"
Press **1** and then **Enter**

#### Step 3: Select which programs to save

The program will ask:
- **"Save native packages?"** → Choose **Yes** to save main programs
- **"Save AUR packages?"** → Choose **Yes** if you're on Arch Linux
- **"Save Flatpak applications?"** → Choose **Yes** if you have Flatpak

> 📸 **Screenshot Tip:** Take a screenshot of the selection prompts to show how interactive the process is.

#### Step 4: Save the file
The program creates a file named **`restore_dsx_20260519.sh`**

**Done! All your programs are saved in one file!**

---

### 🔄 Goal 2: Restore Programs on Another Computer

#### Step 1: Copy the file
Copy the `restore_dsx_*.sh` file to a **USB stick** or **cloud storage** and transfer it to your new computer.

#### Step 2: Give execute permission
Open a terminal and type:
```bash
chmod +x restore_dsx_*.sh
```

(This allows the file to be executed)

#### Step 3: Run the file
```bash
./restore_dsx_*.sh
```

The program will:
1. 🔄 Ask if you want to update the system (you choose)
2. 📦 Install all your programs automatically
3. ✅ Show installation progress
4. 🎉 Notify you when everything is done

> 📸 **Screenshot Tip:** Capture the progress output showing packages being installed. This demonstrates the automation in action.

**Done! All your programs are installed!**

---

## ❓ Frequently Asked Questions

### Q: Will I lose my data?
**A:** No! DSXConfig only **saves the list of programs**, not your files or documents.

### Q: Do I need to be an administrator?
**A:** Yes, when **installing** programs you'll need admin permissions. The program will ask for your password when needed.

### Q: Can I use the file on a different Linux distribution?
**A:** **Yes!** A file from Ubuntu can be used on Fedora, Arch, etc. The program automatically adapts program names for each distribution.

### Q: What if a program doesn't exist on another Linux?
**A:** The program warns you and tries to continue with others. Most programs are available everywhere, so this is rare.

### Q: How long does it take?
**A:** Depends on how many programs you have and your internet speed. Usually 5-30 minutes.

### Q: Can I edit the file afterward?
**A:** **Yes!** Open the `.sh` file with any text editor and remove lines for programs you don't want to install.

### Q: What if I don't want to install everything?
**A:** You have 2 options:
1. Edit the file and remove programs you don't want
2. Let it run and skip individual installations when prompted

### Q: Can I use this on servers?
**A:** **Yes!** DSXConfig works great on servers for cloning installations across multiple machines.

### Q: Will this work on different desktop environments (KDE, GNOME, etc.)?
**A:** **Yes!** It only installs programs, not desktop environments. It works regardless of your desktop.

---

## 🔧 Troubleshooting

### Error: "fzf not found"
```bash
# Install fzf:
sudo apt install fzf      # Ubuntu/Debian
sudo pacman -S fzf        # Arch
sudo dnf install fzf      # Fedora
```

### Error: "No packages found"
This means no programs were detected. Verify:
1. Your package manager is working
2. You have internet connection
3. Try: `sudo pacman -Q` (Arch) or `apt list --installed` (Ubuntu)

### Error: "Permission denied"
Run with sudo:
```bash
sudo python3 main.py
```

### The script fails to restore a program
Some programs might have different names or not be available. The script will:
- Try to find an alternative
- Skip if not available
- Continue with the next program

You can manually install problematic programs later.

---

## 💡 Practical Use Cases

### Case 1: New Computer Setup
1. On your old computer, run `python3 main.py` and choose "Export"
2. Save the file to a USB stick
3. On your new computer, run the file and everything is installed!

### Case 2: Fresh Linux Installation
1. Before reinstalling, create a backup
2. Save the file to cloud storage or USB
3. After reinstalling, run the file and restore everything

### Case 3: Development Environment Setup
Clone your entire development setup to other machines with one command.

### Case 4: Lab/School Machines
Set up multiple computers identically without manual installation.

---

## 📸 Screenshots & Documentation

For better documentation, here are recommended places to take screenshots:

| Location | Why | Impact |
|----------|-----|--------|
| **Main Menu** | Shows the interface is simple and friendly | Shows ease of use |
| **Selection Prompts** | Demonstrates interactive choices | Highlights user control |
| **Progress Output** | Shows automation in action | Proves efficiency |
| **Restored System** | Final result with all programs | Demonstrates success |

> Tip: Use tools like `gnome-screenshot`, `flameshot`, or `scrot` to capture screenshots.

---

## 🔄 Integration with DSXTool

DSXConfig is part of the DSXTool ecosystem and can be:

- **Used independently** — Run directly from this repo
- **Integrated into DSXTool** — Access from DSXTool's main interface
- **Combined with other tools** — Works with DSXTool's other utilities

For DSXTool integration, see: [https://github.com/csouzape/dsxtool](https://github.com/csouzape/dsxtool)

---

## 📝 Generated Restoration Script

The generated `.sh` file includes:

- ✅ Automatic system detection
- ✅ Optional system update
- ✅ Safe package installation with `--needed` flag
- ✅ Error handling and logging
- ✅ Colored output (INFO, WARN, ERROR)
- ✅ Support for multiple AUR helpers (yay/paru)
- ✅ Automatic Flathub setup for Flatpak
- ✅ Cross-distro package mapping

---

## 📊 Version History

### v2.0.0 (May 19, 2026)
- ✅ Enhanced and educational documentation
- ✅ Optional system updates
- ✅ Improved package detection
- ✅ Better cross-distro compatibility
- ✅ Interactive configuration options
- ✅ DSXTool integration support

### Features:
- Full type hints in Python code
- Comprehensive error handling
- Modular architecture
- Color-coded logging
- Security-focused design

---

## 🤝 Contributing

Found a bug or have an idea? Help is welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT © [csouzape](https://github.com/csouzape)

---

## 🙋 Need Help?

- 📖 **Documentation**: Check this README
- 🐛 **Found a bug?**: [Open an Issue](https://github.com/csouzape/dsxconfig/issues)
- 💬 **Have a question?**: [Start a Discussion](https://github.com/csouzape/dsxconfig/discussions)
- 🔗 **More tools**: Visit [DSXTool](https://github.com/csouzape/dsxtool)
- 🌐 **Portuguese version**: [README_PT.md](README_PT.md)

---

**Happy backing up! 🎉**

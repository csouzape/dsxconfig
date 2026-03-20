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

[![Go](https://img.shields.io/badge/Go-1.22+-00ADD8?style=flat&logo=go)](https://golang.org)
[![License](https://img.shields.io/github/license/csouzape/dsxconfig)](LICENSE)
[![Powered By: DSX](https://img.shields.io/badge/part%20of-DSX%20ecosystem-cba6f7)](https://dsxtool.vercel.app)

</div>

---

## What is dsxconfig?

`dsxconfig` is a TUI tool that exports your Linux system package setup — installed packages and Flatpak apps — into a single portable archive. Restore everything on a new machine in one run.

No full disk images. No 400GB clones. Just your packages.

Part of the **DSX** ecosystem — *Direct System eXtensions*.

---

## Features

- **Interactive TUI** — navigate and select what to export
- **Smart export** — captures only explicitly installed packages, not base dependencies
- **Cross-distro restore** — installs what it can, logs what it can't
- **Flatpak support** — exports and restores your Flatpak apps
- **Single binary** — no runtime dependencies, written in Go
- **Transparent** — generates `not_found.log` and a final summary

---

## Supported distros

| Distro | Export | Restore |
|--------|--------|---------|
| Arch Linux | ✓ | ✓ |
| Debian / Ubuntu / Mint | ✓ | ✓ |
| Fedora | ✓ | ✓ |

---

## Installation

### Via dsxtool
`dsxconfig` is integrated into [dsxtool](https://dsxtool.vercel.app) — just select it from the menu and it will be cloned and launched automatically.

### Standalone
```bash
curl -fsSL https://raw.githubusercontent.com/csouzape/dsxconfig/main/install.sh | bash
```

### Build from source
```bash
git clone https://github.com/csouzape/dsxconfig.git
cd dsxconfig
go build -o dsxconfig .
sudo mv dsxconfig /usr/local/bin/
```

---

## Usage

Launch the TUI:
```bash
dsxconfig
```

From the TUI you can:
- **Export** — select packages and Flatpak apps to backup
- **Restore** — point to an existing archive and restore packages/apps

---

## Export archive format

``` 
dsxconfig-2026-03-15.tar.gz
└── metadata.json       # distro, date, hostname, version, packages, aur, flatpak
```

---

## Restore summary

At the end of a restore run, dsxconfig shows:

```
  ✓  142 packages installed
  -  36 packages already installed (skipped)
  ✓  9 Flatpak apps installed
  ✗  8 packages not found → see not_found.log
```

---

## Project structure

```
dsxconfig/
├── main.go
├── cmd/
│   ├── export.go
│   └── restore.go
├── core/
│   ├── detect.go       # distro detection
│   ├── packages.go     # package list export/install
│   ├── flatpak.go      # flatpak export/install
│   └── mapping.go      # cross-distro package name mapping
├── tui/
│   └── ui.go           # interactive TUI
└── install.sh          # standalone installer
```

---

## Contributing

Issues and PRs are welcome. See [contributing.md](contributing.md).

---

## License

MIT © [csouzape](https://github.com/csouzape)

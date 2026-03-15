package core

import (
	"bufio"
	"os"
	"strings"
)

type Distro string

// supported distros
const (
	Arch    Distro = "arch"
	Debian  Distro = "debian"
	Fedora  Distro = "fedora"
	Unknown Distro = "unknown"
)

type SystemInfo struct {
	Distro Distro
	PkgMgr string
	Name   string
}

func Detect() SystemInfo {
	f, err := os.Open("/etc/os-release")
	if err != nil {
		return SystemInfo{Distro: Unknown}
	}
	defer f.Close()

	vals := map[string]string{}
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.SplitN(line, "=", 2)
		if len(parts) == 2 {
			vals[parts[0]] = strings.Trim(parts[1], `"`)
		}
	}

	id := strings.ToLower(vals["ID"])
	idLike := strings.ToLower(vals["ID_LIKE"])
	name := vals["PRETTY_NAME"]

	switch {
	case id == "arch" || strings.Contains(idLike, "arch"):
		return SystemInfo{Distro: Arch, PkgMgr: "pacman", Name: name}
	case id == "fedora" || strings.Contains(idLike, "fedora"):
		return SystemInfo{Distro: Fedora, PkgMgr: "dnf", Name: name}
	case id == "debian" || id == "ubuntu" || id == "linuxmint" ||
		strings.Contains(idLike, "debian") || strings.Contains(idLike, "ubuntu"):
		return SystemInfo{Distro: Debian, PkgMgr: "apt", Name: name}
	default:
		return SystemInfo{Distro: Unknown, PkgMgr: "", Name: name}
	}
}

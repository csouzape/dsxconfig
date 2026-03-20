package core

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
)

func ExportPackages(distro Distro) ([]string, error) {
	var cmd *exec.Cmd

	switch distro {
	case Arch:
		cmd = exec.Command("pacman", "-Qn")
	case Debian:
		cmd = exec.Command("apt-mark", "showmanual")
	case Fedora:
		cmd = exec.Command("dnf", "repoquery", "--userinstalled", "--queryformat", "%{name}\n")
	default:
		return nil, nil
	}

	out, err := cmd.Output()
	if err != nil {
		return nil, err
	}

	var packages []string
	for _, line := range strings.Split(string(out), "\n") {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		if distro == Arch {
			parts := strings.Fields(line)
			if len(parts) > 0 {
				packages = append(packages, parts[0])
			}
		} else {
			packages = append(packages, line)
		}
	}
	filtered := filterMainPackages(packages)
	return filtered, nil
}

func InstallPackages(distro Distro, packages []string) (installed []string, failed []string, skipped []string) {
	mapped := make([]string, len(packages))
	for i, pkg := range packages {
		mapped[i] = MapPackage(pkg, distro)
	}

	var toInstall []string
	seenInstall := map[string]struct{}{}
	for _, pkg := range mapped {
		key := normalizePkg(pkg)
		if _, ok := seenInstall[key]; ok {
			continue
		}
		seenInstall[key] = struct{}{}

		if !isReasonablePackageName(pkg) {
			failed = append(failed, pkg+" (invalid package entry)")
			continue
		}

		if isPackageInstalled(distro, pkg) {
			skipped = append(skipped, pkg)
			continue
		}
		toInstall = append(toInstall, pkg)
	}

	if len(toInstall) == 0 {
		return nil, failed, skipped
	}

	if distro == Arch {
		installed, failed = installArch(toInstall)
	} else {
		if err := bulkInstall(distro, toInstall); err == nil {
			return toInstall, nil, skipped
		}
		fmt.Println("  Bulk install failed, retrying one by one...")
		for _, pkg := range toInstall {
			if tryInstallWithFallback(distro, pkg) {
				installed = append(installed, pkg)
			} else {
				failed = append(failed, failWithSuggestion(distro, pkg))
			}
		}
	}
	return installed, failed, skipped
}

func installArch(packages []string) (installed []string, failed []string) {
	args := append([]string{"pacman", "-S", "--noconfirm", "--needed"}, packages...)
	cmd := exec.Command("sudo", args...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if cmd.Run() == nil {
		return packages, nil
	}

	fmt.Println("  Retrying failed packages via pacman and AUR...")
	var aurFallback []string

	for _, pkg := range packages {
		if isInstalled(pkg) {
			installed = append(installed, pkg)
			continue
		}
		if tryInstallWithFallback(Arch, pkg) {
			installed = append(installed, pkg)
		} else {
			aurFallback = append(aurFallback, pkg)
		}
	}

	if len(aurFallback) > 0 && hasYay() {
		fmt.Printf("  Trying %d package(s) via AUR (yay)...\n", len(aurFallback))
		aurArgs := append([]string{"-S", "--noconfirm", "--needed"}, aurFallback...)
		aurCmd := exec.Command("yay", aurArgs...)
		aurCmd.Stdout = os.Stdout
		aurCmd.Stderr = os.Stderr

		if aurCmd.Run() == nil {
			installed = append(installed, aurFallback...)
		} else {
			for _, pkg := range aurFallback {
				if isInstalled(pkg) {
					installed = append(installed, pkg)
				} else if tryAUR(pkg) {
					installed = append(installed, pkg)
				} else {
					failed = append(failed, failWithSuggestion(Arch, pkg))
				}
			}
		}
	} else {
		for _, pkg := range aurFallback {
			failed = append(failed, failWithSuggestion(Arch, pkg))
		}
	}

	return
}

func bulkInstall(distro Distro, packages []string) error {
	var cmd *exec.Cmd
	switch distro {
	case Arch:
		args := append([]string{"pacman", "-S", "--noconfirm", "--needed"}, packages...)
		cmd = exec.Command("sudo", args...)
	case Debian:
		args := append([]string{"apt-get", "install", "-y"}, packages...)
		cmd = exec.Command("sudo", args...)
	case Fedora:
		args := append([]string{"dnf", "install", "-y"}, packages...)
		cmd = exec.Command("sudo", args...)
	default:
		return fmt.Errorf("unsupported distro")
	}
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

func tryInstall(distro Distro, pkg string) bool {
	var cmd *exec.Cmd
	switch distro {
	case Arch:
		cmd = exec.Command("sudo", "pacman", "-S", "--noconfirm", "--needed", pkg)
	case Debian:
		cmd = exec.Command("sudo", "apt-get", "install", "-y", pkg)
	case Fedora:
		cmd = exec.Command("sudo", "dnf", "install", "-y", pkg)
	default:
		return false
	}
	return cmd.Run() == nil
}

func tryAUR(pkg string) bool {
	if !hasYay() {
		return false
	}
	cmd := exec.Command("yay", "-S", "--noconfirm", "--needed", pkg)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run() == nil
}

func tryInstallWithFallback(distro Distro, pkg string) bool {
	if tryInstall(distro, pkg) {
		return true
	}

	for _, alt := range PackageFallbacks(pkg, distro) {
		if isPackageInstalled(distro, alt) {
			fmt.Printf("  Fallback resolved: %s -> %s (already installed)\n", pkg, alt)
			return true
		}
		if tryInstall(distro, alt) {
			fmt.Printf("  Fallback installed: %s -> %s\n", pkg, alt)
			return true
		}
	}

	return false
}

func failWithSuggestion(distro Distro, pkg string) string {
	suggestion := RecommendPackage(pkg, distro)
	if suggestion == "" {
		return pkg
	}
	return fmt.Sprintf("%s (suggested: %s)", pkg, suggestion)
}

func isInstalled(pkg string) bool {
	return exec.Command("pacman", "-Qi", pkg).Run() == nil
}

func hasYay() bool {
	_, err := exec.LookPath("yay")
	return err == nil
}

func isPackageInstalled(distro Distro, pkg string) bool {
	switch distro {
	case Arch:
		return exec.Command("pacman", "-Qi", pkg).Run() == nil
	case Debian:
		return exec.Command("dpkg", "-s", pkg).Run() == nil
	case Fedora:
		return exec.Command("rpm", "-q", pkg).Run() == nil
	default:
		return false
	}
}

func pkgListStr(pkgs []string) string {
	return strings.Join(pkgs, " ")
}

func ExportAURPackages() ([]string, error) {
	cmd := exec.Command("pacman", "-Qm")
	out, err := cmd.Output()
	if err != nil {
		return nil, err
	}

	var packages []string
	for _, line := range strings.Split(string(out), "\n") {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		parts := strings.Fields(line)
		if len(parts) > 0 {
			packages = append(packages, parts[0])
		}
	}
	return packages, nil
}

func filterMainPackages(packages []string) []string {
	seen := map[string]struct{}{}
	var filtered []string

	for _, pkg := range packages {
		name := strings.TrimSpace(strings.ToLower(pkg))
		if name == "" {
			continue
		}
		if !isMainPackage(name) {
			continue
		}
		if _, ok := seen[name]; ok {
			continue
		}
		seen[name] = struct{}{}
		filtered = append(filtered, pkg)
	}

	return filtered
}

func isMainPackage(name string) bool {
	exactDeny := map[string]struct{}{
		"linux":                 {},
		"linux-lts":             {},
		"linux-zen":             {},
		"linux-hardened":        {},
		"linux-headers":         {},
		"linux-firmware":        {},
		"base":                  {},
		"base-devel":            {},
		"systemd":               {},
		"systemd-libs":          {},
		"systemd-sysvcompat":    {},
		"grub":                  {},
		"shim":                  {},
		"initramfs-tools":       {},
		"dracut":                {},
		"mkinitcpio":            {},
		"networkmanager":        {},
		"network-manager":       {},
		"network-manager-applet": {},
	}
	if _, denied := exactDeny[name]; denied {
		return false
	}

	denyPrefixes := []string{
		"linux-image",
		"linux-headers",
		"kernel",
		"nvidia-kernel",
		"xorg-x11-drv",
	}
	for _, prefix := range denyPrefixes {
		if strings.HasPrefix(name, prefix) {
			return false
		}
	}

	allowPrefixes := []string{
		"firefox",
		"chrom",
		"brave",
		"opera",
		"vivaldi",
		"librewolf",
		"tor-browser",
		"vlc",
		"mpv",
		"spotify",
		"obs",
		"kdenlive",
		"audacity",
		"gimp",
		"inkscape",
		"blender",
		"steam",
		"lutris",
		"discord",
		"telegram",
		"code",
		"codium",
		"jetbrains",
		"intellij",
		"pycharm",
		"goland",
		"webstorm",
		"clion",
		"android-studio",
		"neovim",
		"vim",
		"emacs",
		"tmux",
		"alacritty",
		"kitty",
		"zsh",
		"fish",
		"git",
		"docker",
		"podman",
		"kubectl",
		"k9s",
		"python",
		"pip",
		"node",
		"npm",
		"yarn",
		"pnpm",
		"go",
		"golang",
		"rust",
		"cargo",
		"gcc",
		"clang",
		"java",
		"openjdk",
		"dotnet",
		"ruby",
		"php",
		"lua",
		"deno",
		"bun",
		"postgres",
		"mysql",
		"mariadb",
		"mongodb",
		"redis",
		"sqlite",
		"flatpak",
	}

	for _, prefix := range allowPrefixes {
		if strings.HasPrefix(name, prefix) {
			return true
		}
	}

	allowExact := map[string]struct{}{
		"code":        {},
		"git":         {},
		"curl":        {},
		"wget":        {},
		"ffmpeg":      {},
		"thunderbird": {},
		"libreoffice": {},
		"fzf":         {},
		"ripgrep":     {},
		"bat":         {},
		"fd":          {},
		"fd-find":     {},
		"eza":         {},
	}
	_, allowed := allowExact[name]
	return allowed
}

func isReasonablePackageName(name string) bool {
	n := strings.TrimSpace(name)
	if n == "" {
		return false
	}
	if len(n) > 120 {
		return false
	}
	if strings.ContainsAny(n, " \t\r\n") {
		return false
	}
	return true
}

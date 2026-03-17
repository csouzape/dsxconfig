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
		cmd = exec.Command("dnf", "repoquery", "--userinstalled", "--queryformat", "%{name}")
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
	return packages, nil
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

func InstallPackages(distro Distro, packages []string) (installed []string, failed []string) {
	mapped := make([]string, len(packages))
	for i, pkg := range packages {
		mapped[i] = MapPackage(pkg, distro)
	}

	if distro == Arch {
		return installArch(mapped)
	}

	if err := bulkInstall(distro, mapped); err == nil {
		return mapped, nil
	}

	fmt.Println("  Bulk install failed, retrying one by one...")
	for _, pkg := range mapped {
		if tryInstall(distro, pkg) {
			installed = append(installed, pkg)
		} else {
			failed = append(failed, pkg)
		}
	}
	return
}

// InstallAURPackages installs AUR packages via yay (Arch only)
func InstallAURPackages(packages []string) (installed []string, failed []string) {
	if !hasYay() {
		fmt.Println("  [warn] yay not found — skipping AUR packages.")
		return nil, packages
	}

	// Bulk AUR install
	args := append([]string{"-S", "--noconfirm", "--needed"}, packages...)
	cmd := exec.Command("yay", args...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if cmd.Run() == nil {
		return packages, nil
	}

	// Fallback one by one
	fmt.Println("  AUR bulk failed, retrying one by one...")
	for _, pkg := range packages {
		if isInstalled(pkg) {
			installed = append(installed, pkg)
		} else if tryAUR(pkg) {
			installed = append(installed, pkg)
		} else {
			failed = append(failed, pkg)
		}
	}
	return
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
		if tryInstall(Arch, pkg) {
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
					failed = append(failed, pkg)
				}
			}
		}
	} else {
		failed = append(failed, aurFallback...)
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

func isInstalled(pkg string) bool {
	return exec.Command("pacman", "-Qi", pkg).Run() == nil
}

func hasYay() bool {
	_, err := exec.LookPath("yay")
	return err == nil
}
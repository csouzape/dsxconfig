package core

import (
	"os/exec"
	"strings"
)

func ExportFlatpak() ([]string, error) {
	if _, err := exec.LookPath("flatpak"); err != nil {
		return nil, nil 
	}

	out, err := exec.Command("flatpak", "list", "--app", "--columns=application").Output()
	if err != nil {
		return nil, err
	}

	var apps []string
	for _, line := range strings.Split(strings.TrimSpace(string(out)), "\n") {
		line = strings.TrimSpace(line)
		if line != "" {
			apps = append(apps, line)
		}
	}
	return apps, nil
}

func InstallFlatpak(apps []string) (installed []string, notFound []string) {
	for _, app := range apps {
		cmd := exec.Command("flatpak", "install", "-y", "flathub", app)
		if err := cmd.Run(); err != nil {
			notFound = append(notFound, app)
		} else {
			installed = append(installed, app)
		}
	}
	return
}

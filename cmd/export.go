package cmd

import (
	"archive/tar"
	"compress/gzip"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/csouzape/dsxconfig/core"
)

type Metadata struct {
	Version  string   `json:"dsxconfig_version"`
	Distro   string   `json:"distro"`
	Date     string   `json:"date"`
	Hostname string   `json:"hostname"`
	Packages []string `json:"packages"`
	AUR      []string `json:"aur_packages"`
	Flatpak  []string `json:"flatpak"`
}

func RunExport(sys core.SystemInfo) error {
	fmt.Println("\n  Exporting system configuration...")
	fmt.Printf("  Distro: %s (%s)\n\n", sys.Name, sys.Distro)

	var packages, aurPackages, flatpaks []string

	if confirm(fmt.Sprintf("  Save %s packages?", sys.PkgMgr)) {
		fmt.Printf("  Collecting %s packages...\n", sys.PkgMgr)
		pkgs, err := core.ExportPackages(sys.Distro)
		if err != nil {
			fmt.Printf("  [warn] Failed to collect packages: %v\n", err)
		} else {
			packages = pkgs
			fmt.Printf("  Found %d packages\n", len(packages))
		}
	}

	if sys.Distro == core.Arch {
		if confirm("  Save AUR packages?") {
			fmt.Println("  Collecting AUR packages...")
			aur, err := core.ExportAURPackages()
			if err != nil {
				fmt.Printf("  [warn] Failed to collect AUR packages: %v\n", err)
			} else {
				aurPackages = aur
				fmt.Printf("  Found %d AUR packages\n", len(aurPackages))
			}
		}
	}

	if confirm("  Save Flatpak apps?") {
		fmt.Println("  Collecting Flatpak apps...")
		fp, err := core.ExportFlatpak()
		if err != nil {
			fmt.Printf("  [warn] Failed to collect Flatpak apps: %v\n", err)
		} else {
			flatpaks = fp
			fmt.Printf("  Found %d Flatpak apps\n", len(flatpaks))
		}
	}

	hostname, _ := os.Hostname()
	meta := Metadata{
		Version:  "1.0.0",
		Distro:   string(sys.Distro),
		Date:     time.Now().Format(time.RFC1123),
		Hostname: hostname,
		Packages: packages,
		AUR:      aurPackages,
		Flatpak:  flatpaks,
	}

	home, _ := os.UserHomeDir()
	archivePath, err := createArchive(meta, home)
	if err != nil {
		return fmt.Errorf("failed to create archive: %w", err)
	}

	fmt.Printf("\n  ✓ Export complete: %s\n", archivePath)
	fmt.Printf("  ✓ %d packages  ·  %d AUR  ·  %d Flatpak\n\n",
		len(packages), len(aurPackages), len(flatpaks))
	return nil
}

func confirm(prompt string) bool {
	result, err := runFzfInline([]string{"Yes", "No"}, prompt, "")
	if err != nil {
		return false
	}
	return result == "Yes"
}

func runFzfInline(items []string, prompt, header string) (string, error) {
	tmpIn, err := os.CreateTemp("", "dsxconfig-in-*")
	if err != nil {
		return "", err
	}
	tmpOut, err := os.CreateTemp("", "dsxconfig-out-*")
	if err != nil {
		_ = os.Remove(tmpIn.Name())
		return "", err
	}
	defer os.Remove(tmpIn.Name())
	defer os.Remove(tmpOut.Name())

	if _, err := tmpIn.WriteString(strings.Join(items, "\n")); err != nil {
		tmpIn.Close()
		return "", err
	}
	if err := tmpIn.Close(); err != nil {
		return "", err
	}

	inFile, err := os.Open(tmpIn.Name())
	if err != nil {
		return "", err
	}
	defer inFile.Close()
	outFile, err := os.OpenFile(tmpOut.Name(), os.O_WRONLY, 0600)
	if err != nil {
		return "", err
	}
	defer outFile.Close()

	args := []string{
		"--header=↑↓ navigate   Enter select   Esc skip",
		"--prompt=" + prompt + " ",
		"--height=6",
		"--layout=reverse",
		"--border=rounded",
		"--pointer=▶",
		"--color=bg:#121212,bg+:#1e1e1e,fg:#d1d1d1,fg+:#ffffff,hl:#89b4fa,prompt:#cba6f7,pointer:#f38ba8,border:#2a2a2a",
		"--no-info",
	}
	if header != "" {
		args = append(args, "--header="+header)
	}

	fzfCmd := exec.Command("fzf", args...)
	fzfCmd.Stdin = inFile
	fzfCmd.Stdout = outFile
	fzfCmd.Stderr = os.Stderr
	if err := fzfCmd.Run(); err != nil {
		return "", err
	}

	result, err := os.ReadFile(tmpOut.Name())
	if err != nil {
		return "", err
	}
	return strings.TrimSpace(string(result)), nil
}

func createArchive(meta Metadata, outDir string) (string, error) {
	filename := fmt.Sprintf("dsxconfig-%s.tar.gz", time.Now().Format("2006-01-02"))
	outPath := filepath.Join(outDir, filename)

	f, err := os.Create(outPath)
	if err != nil {
		return "", err
	}
	defer f.Close()

	gz := gzip.NewWriter(f)
	defer gz.Close()
	tw := tar.NewWriter(gz)
	defer tw.Close()

	metaBytes, err := json.MarshalIndent(meta, "", "  ")
	if err != nil {
		return "", err
	}
	if err := writeBytesToTar(tw, "metadata.json", metaBytes); err != nil {
		return "", err
	}

	return outPath, nil
}

func writeBytesToTar(tw *tar.Writer, name string, data []byte) error {
	hdr := &tar.Header{Name: name, Mode: 0644, Size: int64(len(data))}
	if err := tw.WriteHeader(hdr); err != nil {
		return err
	}
	_, err := tw.Write(data)
	return err
}

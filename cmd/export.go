package cmd

import (
	"archive/tar"
	"compress/gzip"
	"encoding/json"
	"fmt"
	"io"
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
	result, _ := runFzfInline([]string{"Yes", "No"}, prompt)
	return result == "Yes"
}

func runFzfInline(items []string, prompt string) (string, error) {
	tmpIn, _ := os.CreateTemp("", "dsxconfig-in-*")
	tmpOut, _ := os.CreateTemp("", "dsxconfig-out-*")
	defer os.Remove(tmpIn.Name())
	defer os.Remove(tmpOut.Name())

	tmpIn.WriteString(strings.Join(items, "\n"))
	tmpIn.Close()

	inFile, _ := os.Open(tmpIn.Name())
	defer inFile.Close()
	outFile, _ := os.OpenFile(tmpOut.Name(), os.O_WRONLY, 0600)
	defer outFile.Close()

	fzfCmd := exec.Command("fzf",
		"--prompt="+prompt+"  ",
		"--height=6",
		"--layout=reverse",
		"--border=rounded",
		"--pointer=▶",
		"--color=bg:#121212,bg+:#1e1e1e,fg:#d1d1d1,fg+:#ffffff,hl:#89b4fa,prompt:#cba6f7,pointer:#f38ba8,border:#2a2a2a",
		"--no-info",
		"--header=  ↑↓ navigate   Enter select",
	)
	fzfCmd.Stdin = inFile
	fzfCmd.Stdout = outFile
	fzfCmd.Stderr = os.Stderr
	fzfCmd.Run()

	result, _ := os.ReadFile(tmpOut.Name())
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

	hdr := &tar.Header{Name: "metadata.json", Mode: 0644, Size: int64(len(metaBytes))}
	if err := tw.WriteHeader(hdr); err != nil {
		return "", err
	}
	if _, err := tw.Write(metaBytes); err != nil {
		return "", err
	}

	return outPath, nil
}

// writeBytesToTar kept for future use
func writeBytesToTar(tw *tar.Writer, name string, data []byte) error {
	hdr := &tar.Header{Name: name, Mode: 0644, Size: int64(len(data))}
	if err := tw.WriteHeader(hdr); err != nil {
		return err
	}
	_, err := tw.Write(data)
	return err
}

// addPathToTar kept for future use (configs - v1.2.0)
func addPathToTar(tw *tar.Writer, src, dst string) error {
	return filepath.Walk(src, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return nil
		}
		if info.IsDir() && info.Name() == ".git" {
			return filepath.SkipDir
		}
		rel, _ := filepath.Rel(src, path)
		tarPath := dst
		if rel != "." {
			tarPath = filepath.Join(dst, rel)
		}
		if info.Mode()&os.ModeSymlink != 0 {
			linkTarget, err := os.Readlink(path)
			if err != nil {
				return nil
			}
			return tw.WriteHeader(&tar.Header{
				Typeflag: tar.TypeSymlink,
				Name:     tarPath,
				Linkname: linkTarget,
			})
		}
		if info.IsDir() {
			return tw.WriteHeader(&tar.Header{
				Typeflag: tar.TypeDir,
				Name:     tarPath + "/",
				Mode:     int64(info.Mode()),
			})
		}
		file, err := os.Open(path)
		if err != nil {
			return nil
		}
		defer file.Close()
		stat, err := file.Stat()
		if err != nil {
			return nil
		}
		hdr := &tar.Header{Name: tarPath, Mode: int64(info.Mode()), Size: stat.Size()}
		if err := tw.WriteHeader(hdr); err != nil {
			return err
		}
		_, err = io.Copy(tw, file)
		return err
	})
}
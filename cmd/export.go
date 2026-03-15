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
	Configs  []string `json:"configs"`
}

func RunExport(sys core.SystemInfo) error {
	fmt.Println("\n  Exporting system configuration...")
	fmt.Printf("  Distro: %s (%s)\n\n", sys.Name, sys.Distro)

	var packages, aurPackages, flatpaks []string

	// Ask what to save
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

	// Config files
	fmt.Println("\n  Select config files to backup (TAB to select, ENTER to confirm):")
	selectedConfigs, err := selectConfigs()
	if err != nil {
		return fmt.Errorf("config selection failed: %w", err)
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
		Configs:  selectedConfigs,
	}

	home, _ := os.UserHomeDir()
	archivePath, err := createArchive(meta, selectedConfigs, home)
	if err != nil {
		return fmt.Errorf("failed to create archive: %w", err)
	}

	fmt.Printf("\n  ✓ Export complete: %s\n", archivePath)
	fmt.Printf("  ✓ %d packages  ·  %d AUR  ·  %d Flatpak  ·  %d configs\n\n",
		len(packages), len(aurPackages), len(flatpaks), len(selectedConfigs))
	return nil
}

func confirm(prompt string) bool {
	result, _ := runFzfInline([]string{"Yes", "No"}, prompt, "")
	return result == "Yes"
}

func runFzfInline(items []string, prompt, header string) (string, error) {
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
	fzfCmd.Run()

	result, _ := os.ReadFile(tmpOut.Name())
	return strings.TrimSpace(string(result)), nil
}

func selectConfigs() ([]string, error) {
	candidates := core.DefaultConfigPaths()
	var existing []string
	for _, p := range candidates {
		if _, err := os.Stat(p); err == nil {
			existing = append(existing, p)
		}
	}
	if len(existing) == 0 {
		fmt.Println("  No config files found.")
		return nil, nil
	}

	tmpIn, _ := os.CreateTemp("", "dsxconfig-in-*")
	tmpOut, _ := os.CreateTemp("", "dsxconfig-out-*")
	defer os.Remove(tmpIn.Name())
	defer os.Remove(tmpOut.Name())

	tmpIn.WriteString(strings.Join(existing, "\n"))
	tmpIn.Close()

	inFile, _ := os.Open(tmpIn.Name())
	defer inFile.Close()
	outFile, _ := os.OpenFile(tmpOut.Name(), os.O_WRONLY, 0600)
	defer outFile.Close()

	fzfCmd := exec.Command("fzf", "-m",
		"--prompt=  configs > ",
		"--header=[TAB] select   [ENTER] confirm   [ESC] skip configs",
		"--height=12",
		"--layout=reverse",
		"--border=rounded",
		"--pointer=▶",
		"--color=bg:#121212,bg+:#1e1e1e,fg:#d1d1d1,fg+:#ffffff,hl:#89b4fa,prompt:#cba6f7,pointer:#f38ba8,marker:#a6e3a1,header:#f9e2af,border:#2a2a2a",
		"--no-info",
	)
	fzfCmd.Stdin = inFile
	fzfCmd.Stdout = outFile
	fzfCmd.Stderr = os.Stderr
	fzfCmd.Run()

	result, _ := os.ReadFile(tmpOut.Name())
	home, _ := os.UserHomeDir()
	var selected []string
	for _, line := range strings.Split(string(result), "\n") {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		rel := strings.TrimPrefix(line, home+"/")
		selected = append(selected, rel)
	}
	return selected, nil
}

func createArchive(meta Metadata, configPaths []string, outDir string) (string, error) {
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

	home, _ := os.UserHomeDir()
	for _, rel := range configPaths {
		src := filepath.Join(home, rel)
		if _, err := os.Lstat(src); err != nil {
			continue
		}
		if err := addPathToTar(tw, src, filepath.Join("configs", rel)); err != nil {
			fmt.Printf("  [warn] could not add %s: %v\n", rel, err)
		}
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
		f, err := os.Open(path)
		if err != nil {
			return nil
		}
		defer f.Close()
		stat, err := f.Stat()
		if err != nil {
			return nil
		}
		hdr := &tar.Header{
			Name: tarPath,
			Mode: int64(info.Mode()),
			Size: stat.Size(),
		}
		if err := tw.WriteHeader(hdr); err != nil {
			return err
		}
		_, err = io.Copy(tw, f)
		return err
	})
}
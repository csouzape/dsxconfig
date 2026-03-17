package cmd

import (
	"archive/tar"
	"compress/gzip"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"

	"github.com/csouzape/dsxconfig/core"
)

func RunRestore(archivePath string, sys core.SystemInfo) error {
	fmt.Println("\n  Restoring system configuration...")
	fmt.Printf("  Extracting %s...\n", filepath.Base(archivePath))

	staging, err := extractArchive(archivePath)
	if err != nil {
		return fmt.Errorf("failed to extract archive: %w", err)
	}
	defer os.RemoveAll(staging)

	meta, err := readMetadata(staging)
	if err != nil {
		return fmt.Errorf("failed to read metadata: %w", err)
	}

	fmt.Printf("\n  Archive info:\n")
	fmt.Printf("    Source distro : %s\n", meta.Distro)
	fmt.Printf("    Exported on   : %s\n", meta.Date)
	fmt.Printf("    Hostname      : %s\n\n", meta.Hostname)

	if meta.Distro != string(sys.Distro) {
		fmt.Printf("  [warn] Source distro (%s) differs from current (%s)\n", meta.Distro, sys.Distro)
		fmt.Println("         Will attempt cross-distro package mapping.\n")
	}

	var installedPkgs, failedPkgs []string
	if len(meta.Packages) > 0 {
		fmt.Printf("  Installing %d packages...\n", len(meta.Packages))
		installedPkgs, failedPkgs = core.InstallPackages(sys.Distro, meta.Packages)
	}

	var installedAUR, failedAUR []string
	if len(meta.AUR) > 0 {
		fmt.Printf("  Installing %d AUR packages...\n", len(meta.AUR))
		installedAUR, failedAUR = core.InstallAURPackages(meta.AUR)
	}

	var installedFp, failedFp []string
	if len(meta.Flatpak) > 0 {
		fmt.Printf("  Installing %d Flatpak apps...\n", len(meta.Flatpak))
		installedFp, failedFp = core.InstallFlatpak(meta.Flatpak)
	}

	allFailed := append(append(failedPkgs, failedAUR...), failedFp...)
	if len(allFailed) > 0 {
		home, _ := os.UserHomeDir()
		logPath := filepath.Join(home, "dsxconfig-not_found.log")
		_ = os.WriteFile(logPath, []byte(strings.Join(allFailed, "\n")), 0644)
		fmt.Printf("\n  [warn] %d items not found — see %s\n", len(allFailed), logPath)
	}

	fmt.Println("\n  ─────────────────────────────────────────")
	fmt.Printf("  ✓  %d packages installed\n", len(installedPkgs))
	if len(meta.AUR) > 0 {
		fmt.Printf("  ✓  %d AUR packages installed\n", len(installedAUR))
	}
	fmt.Printf("  ✓  %d Flatpak apps installed\n", len(installedFp))
	if len(allFailed) > 0 {
		fmt.Printf("  ✗  %d not found → dsxconfig-not_found.log\n", len(allFailed))
	}
	fmt.Println("  ─────────────────────────────────────────\n")
	return nil
}

func extractArchive(archivePath string) (string, error) {
	tmpDir, err := os.MkdirTemp("", "dsxconfig-restore-*")
	if err != nil {
		return "", err
	}
	f, err := os.Open(archivePath)
	if err != nil {
		return "", err
	}
	defer f.Close()

	gz, err := gzip.NewReader(f)
	if err != nil {
		return "", err
	}
	defer gz.Close()

	tr := tar.NewReader(gz)
	for {
		hdr, err := tr.Next()
		if err == io.EOF {
			break
		}
		if err != nil {
			return "", err
		}
		target := filepath.Join(tmpDir, hdr.Name)
		if hdr.Typeflag == tar.TypeDir {
			os.MkdirAll(target, os.FileMode(hdr.Mode))
			continue
		}
		os.MkdirAll(filepath.Dir(target), 0755)
		out, err := os.Create(target)
		if err != nil {
			continue
		}
		io.Copy(out, tr)
		out.Close()
	}
	return tmpDir, nil
}

func readMetadata(dir string) (Metadata, error) {
	var meta Metadata
	data, err := os.ReadFile(filepath.Join(dir, "metadata.json"))
	if err != nil {
		return meta, err
	}
	err = json.Unmarshal(data, &meta)
	return meta, err
}
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
		fmt.Println("         Will attempt cross-distro package mapping.")
	}

	var installedPkgs, failedPkgs, skippedPkgs []string
	if len(meta.Packages) > 0 {
		if sys.Distro == core.Unknown {
			fmt.Println("  [warn] Unsupported distro for package restore. Skipping packages.")
		} else {
			fmt.Printf("  Checking %d packages...\n", len(meta.Packages))
			installedPkgs, failedPkgs, skippedPkgs = core.InstallPackages(sys.Distro, meta.Packages)
			if len(skippedPkgs) > 0 {
				fmt.Printf("  Skipping %d package(s) already installed.\n", len(skippedPkgs))
			}
		}
	}

	var installedFp, failedFp []string
	if len(meta.Flatpak) > 0 {
		if !core.HasFlatpak() {
			fmt.Println("  [warn] Flatpak not found. Skipping Flatpak restore.")
		} else {
			fmt.Printf("  Installing %d Flatpak apps...\n", len(meta.Flatpak))
			installedFp, failedFp = core.InstallFlatpak(meta.Flatpak)
		}
	}

	home, _ := os.UserHomeDir()
	allFailed := append(failedPkgs, failedFp...)
	if len(allFailed) > 0 {
		logPath := filepath.Join(home, "dsxconfig-not_found.log")
		_ = os.WriteFile(logPath, []byte(strings.Join(allFailed, "\n")), 0644)
		fmt.Printf("\n  [warn] %d items not found — see %s\n", len(allFailed), logPath)
	}

	fmt.Println("\n  ─────────────────────────────────────────")
	fmt.Printf("  ✓  %d packages installed\n", len(installedPkgs))
	fmt.Printf("  -  %d packages already installed (skipped)\n", len(skippedPkgs))
	fmt.Printf("  ✓  %d Flatpak apps installed\n", len(installedFp))
	if len(allFailed) > 0 {
		fmt.Printf("  ✗  %d not found → dsxconfig-not_found.log\n", len(allFailed))
	}
	fmt.Println("  ─────────────────────────────────────────")
	fmt.Println()
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
		name := filepath.Clean(hdr.Name)
		if name == "." || name == "" {
			continue
		}
		if filepath.IsAbs(name) || name == ".." || strings.HasPrefix(name, ".."+string(os.PathSeparator)) {
			return "", fmt.Errorf("invalid path in archive: %s", hdr.Name)
		}
		target := filepath.Join(tmpDir, name)
		if !strings.HasPrefix(target, tmpDir+string(os.PathSeparator)) && target != tmpDir {
			return "", fmt.Errorf("invalid path in archive: %s", hdr.Name)
		}

		switch hdr.Typeflag {
		case tar.TypeDir:
			if err := os.MkdirAll(target, os.FileMode(hdr.Mode)); err != nil {
				return "", err
			}
		case tar.TypeReg, tar.TypeRegA:
			if err := os.MkdirAll(filepath.Dir(target), 0755); err != nil {
				return "", err
			}
			out, err := os.OpenFile(target, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, os.FileMode(hdr.Mode))
			if err != nil {
				return "", err
			}
			if _, err := io.Copy(out, tr); err != nil {
				out.Close()
				return "", err
			}
			if err := out.Close(); err != nil {
				return "", err
			}
		}
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

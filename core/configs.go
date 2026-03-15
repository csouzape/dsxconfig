package core

import (
	"io"
	"os"
	"path/filepath"
	"strings"
)

func DefaultConfigPaths() []string {
	home, _ := os.UserHomeDir()
	return []string{
		filepath.Join(home, ".zshrc"),
		filepath.Join(home, ".bashrc"),
		filepath.Join(home, ".bash_profile"),
		filepath.Join(home, ".gitconfig"),
	}
}

func RestoreConfigs(srcDir, destHome string) error {
	return filepath.Walk(srcDir, func(path string, info os.FileInfo, err error) error {
		if err != nil || path == srcDir {
			return nil
		}
		rel, _ := filepath.Rel(srcDir, path)
		if strings.Contains(rel, ".git/") || strings.HasSuffix(rel, ".git") {
			if info.IsDir() {
				return filepath.SkipDir
			}
			return nil
		}
		dest := filepath.Join(destHome, rel)
		if info.IsDir() {
			return os.MkdirAll(dest, info.Mode())
		}
		return copyFile(path, dest)
	})
}

func copyFile(src, dst string) error {
	if err := os.MkdirAll(filepath.Dir(dst), 0755); err != nil {
		return err
	}
	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()

	out, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, in)
	return err
}
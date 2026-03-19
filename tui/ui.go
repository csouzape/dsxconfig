package tui

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/csouzape/dsxconfig/cmd"
	"github.com/csouzape/dsxconfig/core"
)

const banner = `
  ██████╗ ███████╗██╗  ██╗ ██████╗ ██████╗ ███╗   ██╗███████╗██╗ ██████╗ 
  ██╔══██╗██╔════╝╚██╗██╔╝██╔════╝██╔═══██╗████╗  ██║██╔════╝██║██╔════╝ 
  ██║  ██║███████╗ ╚███╔╝ ██║     ██║   ██║██╔██╗ ██║█████╗  ██║██║  ███╗
  ██║  ██║╚════██║ ██╔██╗ ██║     ██║   ██║██║╚██╗██║██╔══╝  ██║██║   ██║
  ██████╔╝███████║██╔╝ ██╗╚██████╗╚██████╔╝██║ ╚████║██║     ██║╚██████╔╝
  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝ ╚═════╝`

func Run() error {
	sys := core.Detect()

	for {
		clearScreen()
		printHeader(sys)

		choice, err := showMainMenu()
		if err != nil || choice == "" {
			continue
		}

		switch strings.TrimSpace(choice) {
		case "Export":
			if err := cmd.RunExport(sys); err != nil {
				fmt.Printf("\n  [error] %v\n", err)
			}
			pause()

		case "Restore":
			archivePath, err := selectArchive()
			if err != nil || archivePath == "" {
				continue
			}
			if err := cmd.RunRestore(archivePath, sys); err != nil {
				fmt.Printf("\n  [error] %v\n", err)
			}
			pause()

		case "Exit":
			return nil
		}
	}
}

func showMainMenu() (string, error) {
	items := []string{"Export", "Restore", "Exit"}
	return runFzf(items,
		"  ➜  ",
		"  ↑↓ navigate   Enter select   Esc exit",
		"20%",
	)
}

func selectArchive() (string, error) {
	home, _ := os.UserHomeDir()
	entries, _ := filepath.Glob(filepath.Join(home, "dsxconfig-*.tar.gz"))

	if len(entries) == 0 {
		fmt.Println("\n  No dsxconfig archives found in ~/")
		fmt.Println("  Run Export first or move the archive to ~/")
		pause()
		return "", nil
	}

	return runFzf(entries,
		"  archive > ",
		"  ↑↓ navigate   Enter select   Esc cancel",
		"20%",
	)
}

func runFzf(items []string, prompt, header, height string) (string, error) {
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

	fzfCmd := exec.Command("fzf",
		"--prompt="+prompt,
		"--header="+header,
		"--height="+height,
		"--layout=reverse",
		"--border=rounded",
		"--pointer=▶",
		"--color=bg:#121212,bg+:#1e1e1e,fg:#d1d1d1,fg+:#ffffff,hl:#89b4fa,prompt:#cba6f7,pointer:#f38ba8,header:#f9e2af,border:#2a2a2a",
		"--no-info",
	)
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

func printHeader(sys core.SystemInfo) {
	fmt.Println(banner)
	fmt.Println()
	fmt.Printf("  distro: %s\n", sys.Name)
	fmt.Println("  ─────────────────────────────────────────────")
	fmt.Println()
}

func clearScreen() {
	fmt.Print("\033[H\033[2J")
}

func pause() {
	fmt.Print("\n  Press Enter to continue...")
	fmt.Scanln()
}

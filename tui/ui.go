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
	fzfCmd.Run()

	result, _ := os.ReadFile(tmpOut.Name())
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
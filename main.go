package main

import (
	"fmt"
	"os"

	"github.com/csouzape/dsxconfig/tui"
)

const version = "1.0.0"

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--version" {
		fmt.Println(version)
		os.Exit(0)
	}

	if err := tui.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}
}
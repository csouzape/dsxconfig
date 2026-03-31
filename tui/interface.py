"""Terminal User Interface module using fzf."""

import subprocess
import os
from typing import List, Optional, Union
from constants import FZF_CONFIG
from logger import get_logger

logger = get_logger(__name__)

__all__ = ["TUI"]


class TUI:
    """Terminal User Interface using fzf."""

    @staticmethod
    def run_fzf(
        items: List[str], prompt: str = "Select", multi: bool = False
    ) -> Optional[Union[str, List[str]]]:
        """
        Run fzf with custom DSXConfig styling.

        Args:
            items: List of strings to display in fzf
            prompt: Text to show in the prompt
            multi: Allow multiple selection (TAB)

        Returns:
            Selected string, list of strings (if multi=True), or None if cancelled

        Raises:
            FileNotFoundError: If fzf is not installed
        """
        if not items:
            logger.warning("No items provided to fzf")
            return None

        try:
            input_str = "\n".join(items)

            args = [
                "fzf",
                f"--prompt={prompt} ",
                f"--height={FZF_CONFIG['height']}",
                f"--layout={FZF_CONFIG['layout']}",
                f"--border={FZF_CONFIG['border']}",
                f"--pointer={FZF_CONFIG['pointer']}",
                f"--marker={FZF_CONFIG['marker']}",
                f"--color={FZF_CONFIG['color']}",
                f"--header={FZF_CONFIG['header_single']}",
            ]

            if multi:
                args.append("--multi")
                header_idx = next(
                    i for i, arg in enumerate(args) if arg.startswith("--header=")
                )
                args[header_idx] = f"--header={FZF_CONFIG['header_multi']}"

            process = subprocess.run(
                args,
                input=input_str,
                text=True,
                capture_output=True,
                timeout=60,
            )

            if process.returncode == 0:
                result = process.stdout.strip()
                if multi:
                    return result.split("\n") if result else []
                return result if result else None

            logger.debug(f"fzf cancelled or errored (exit code: {process.returncode})")
            return None

        except subprocess.TimeoutExpired:
            logger.error("fzf operation timed out")
            return None
        except FileNotFoundError:
            logger.error(
                "fzf not found. Please install it: "
                "https://github.com/junegunn/fzf"
            )
            raise
        except Exception as e:
            logger.error(f"Unexpected error in fzf: {e}")
            return None

    @staticmethod
    def clear() -> None:
        """
        Clear the terminal screen.

        Works on both POSIX (Linux, macOS) and Windows systems.
        """
        try:
            os.system("clear" if os.name == "posix" else "cls")
            logger.debug("Terminal screen cleared")
        except Exception as e:
            logger.warning(f"Failed to clear terminal: {e}")

    @staticmethod
    def print_header(title: str) -> None:
        """
        Print a formatted header.

        Args:
            title: Header text to display
        """
        width = 60
        print()
        print("=" * width)
        print(f"  {title.center(width - 4)}")
        print("=" * width)
        print()

    @staticmethod
    def print_separator() -> None:
        """Print a separator line."""
        print("-" * 60)

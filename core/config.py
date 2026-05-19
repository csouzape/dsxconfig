"""System configuration detection and backup module."""

import os
import pwd
import subprocess
from pathlib import Path
from logger import get_logger

logger = get_logger(__name__)

__all__ = ["ConfigDetector", "SystemConfig"]

class SystemConfig:
    """
    Represents detected system configuration.

    Attributes:
        shell: Current user's shell
        terminal: Current terminal emulator
    """

    def __init__(self) -> None:
        self.shell: str = ""
        self.terminal: str = ""

class ConfigDetector:
    """
    Detects and collects system configuration for backup/restore.

    Focuses on user-specific configurations that can be restored
    across different Linux distributions.
    """



    def __init__(self) -> None:
        self.home = Path.home()
        self.config = SystemConfig()

    def detect_all(self) -> SystemConfig:
        """
        Detect all system configurations.

        Returns:
            SystemConfig with detected settings
        """
        logger.info("Detecting system configuration...")

        self._detect_shell()
        self._detect_terminal()

        logger.info(f"Configuration detected: shell={self.config.shell}, terminal={self.config.terminal}")

        return self.config

    def _detect_shell(self) -> None:
        """Detect current user's shell."""
        try:
            # Try $SHELL first
            shell = os.environ.get("SHELL", "")
            if shell:
                self.config.shell = Path(shell).name
                logger.debug(f"Shell detected from $SHELL: {self.config.shell}")
                return

            # Fallback to /etc/passwd
            uid = os.getuid()
            pw_entry = pwd.getpwuid(uid)
            shell_path = pw_entry.pw_shell
            self.config.shell = Path(shell_path).name
            logger.debug(f"Shell detected from passwd: {self.config.shell}")

        except Exception as e:
            logger.warning(f"Could not detect shell: {e}")
            self.config.shell = "bash"  # Default fallback

    def _detect_terminal(self) -> None:
        """Detect current terminal emulator."""
        try:
            # Try $TERM_PROGRAM
            term_program = os.environ.get("TERM_PROGRAM", "")
            if term_program:
                self.config.terminal = term_program.lower()
                logger.debug(f"Terminal detected from TERM_PROGRAM: {self.config.terminal}")
                return

            # Try $TERM
            term = os.environ.get("TERM", "")
            if term and term != "linux":
                # Map common TERM values to terminal names
                term_mapping = {
                    "xterm": "xterm",
                    "rxvt": "rxvt",
                    "screen": "screen",
                    "tmux": "tmux",
                }
                self.config.terminal = term_mapping.get(term, term)
                logger.debug(f"Terminal detected from TERM: {self.config.terminal}")
                return

            # Try to detect from parent processes
            self.config.terminal = self._detect_from_process()
            if self.config.terminal:
                logger.debug(f"Terminal detected from process: {self.config.terminal}")
                return

        except Exception as e:
            logger.warning(f"Could not detect terminal: {e}")

        self.config.terminal = "unknown"

    def _detect_from_process(self) -> str:
        """Try to detect terminal from parent process."""
        try:
            # Get parent PID
            ppid = os.getppid()

            # Read /proc/<ppid>/comm
            comm_file = f"/proc/{ppid}/comm"
            if os.path.exists(comm_file):
                with open(comm_file, "r") as f:
                    comm = f.read().strip()
                    # Map common terminal processes
                    terminal_mapping = {
                        "gnome-terminal": "gnome-terminal",
                        "konsole": "konsole",
                        "xfce4-terminal": "xfce4-terminal",
                        "lxterminal": "lxterminal",
                        "alacritty": "alacritty",
                        "kitty": "kitty",
                        "terminator": "terminator",
                        "tilix": "tilix",
                    }
                    return terminal_mapping.get(comm, "")

        except Exception:
            pass

        return ""
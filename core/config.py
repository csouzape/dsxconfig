"""System configuration detection and backup module."""

import os
import pwd
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from logger import get_logger

logger = get_logger(__name__)

__all__ = ["ConfigDetector", "SystemConfig"]

class SystemConfig:
    """
    Represents detected system configuration.

    Attributes:
        shell: Current user's shell
        terminal: Current terminal emulator
        config_files: Dict of config file paths and their contents
        environment_vars: Dict of important environment variables
    """

    def __init__(self) -> None:
        self.shell: str = ""
        self.terminal: str = ""
        self.config_files: Dict[str, str] = {}
        self.environment_vars: Dict[str, str] = {}

class ConfigDetector:
    """
    Detects and collects system configuration for backup/restore.

    Focuses on user-specific configurations that can be restored
    across different Linux distributions.
    """

    # Common config files to backup
    COMMON_CONFIG_FILES = [
        ".bashrc",
        ".zshrc",
        ".profile",
        ".bash_profile",
        ".config/starship.toml",  # Starship prompt
        ".config/fish/config.fish",  # Fish shell
        ".tmux.conf",  # Tmux
        ".vimrc",  # Vim
        ".config/nvim/init.vim",  # Neovim
        ".config/Code/User/settings.json",  # VS Code
        ".gitconfig",  # Git
        ".ssh/config",  # SSH config (without keys)
    ]

    # Important environment variables to preserve
    IMPORTANT_ENV_VARS = [
        "EDITOR",
        "VISUAL",
        "LANG",
        "LC_ALL",
        "TZ",
        "PATH",  # Custom PATH additions
    ]

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
        self._collect_config_files()
        self._collect_environment_vars()

        logger.info(f"Configuration detected: shell={self.config.shell}, terminal={self.config.terminal}")
        logger.info(f"Found {len(self.config.config_files)} config files")

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

    def _collect_config_files(self) -> None:
        """Collect contents of important config files."""
        for config_path in self.COMMON_CONFIG_FILES:
            full_path = self.home / config_path

            if full_path.exists() and full_path.is_file():
                try:
                    # Skip binary files and very large files
                    if full_path.stat().st_size > 1024 * 1024:  # 1MB limit
                        logger.debug(f"Skipping large config file: {config_path}")
                        continue

                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # Skip if it looks like binary
                    if "\0" in content:
                        logger.debug(f"Skipping binary config file: {config_path}")
                        continue

                    self.config.config_files[str(full_path)] = content
                    logger.debug(f"Collected config file: {config_path}")

                except (OSError, UnicodeDecodeError) as e:
                    logger.debug(f"Could not read config file {config_path}: {e}")

    def _collect_environment_vars(self) -> None:
        """Collect important environment variables."""
        for var_name in self.IMPORTANT_ENV_VARS:
            value = os.environ.get(var_name, "")
            if value:
                self.config.environment_vars[var_name] = value
                logger.debug(f"Collected env var: {var_name}")

    def get_backup_paths(self) -> List[Path]:
        """
        Get list of paths that should be backed up.

        Returns:
            List of Path objects for config files that exist
        """
        paths = []
        for config_path in self.COMMON_CONFIG_FILES:
            full_path = self.home / config_path
            if full_path.exists():
                paths.append(full_path)

        return paths
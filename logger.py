"""DSXConfig logging configuration."""

import logging
import sys
from typing import Optional
from constants import LOG_LEVEL, LOG_FORMAT

# Color codes for terminal output
class Colors:
    """ANSI color codes."""
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"


class ColoredFormatter(logging.Formatter):
    """Formatter with color support."""

    COLORS = {
        "DEBUG": Colors.CYAN,
        "INFO": Colors.BLUE,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED,
        "CRITICAL": Colors.RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, Colors.RESET)
        record.levelname = f"{color}{record.levelname}{Colors.RESET}"
        return super().format(record)


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with proper configuration.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding multiple handlers
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    formatter = ColoredFormatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


# Create a global logger instance
logger = get_logger("dsxconfig")

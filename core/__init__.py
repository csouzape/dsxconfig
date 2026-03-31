"""Core functionality module."""

from .detector import SystemInfo
from .config import ConfigDetector, SystemConfig
from . import packages

__all__ = ["SystemInfo", "ConfigDetector", "SystemConfig", "packages"]

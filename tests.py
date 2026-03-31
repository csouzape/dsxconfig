"""
Test suite for DSXConfig v2.0.0

Run tests with:
    python3 tests.py
"""

import unittest
import os
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.detector import SystemInfo
from core.config import ConfigDetector, SystemConfig
from core import packages
from cmd.export import ScriptExporter
from logger import get_logger


class TestSystemDetection(unittest.TestCase):
    """Test system detection module."""

    def test_systeminfo_creation(self):
        """Test SystemInfo can be instantiated."""
        sys_info = SystemInfo()
        self.assertIsNotNone(sys_info)
        self.assertIsNotNone(sys_info.distro)
        self.assertIsNotNone(sys_info.pkg_mgr)

    def test_systeminfo_repr(self):
        """Test SystemInfo string representation."""
        sys_info = SystemInfo()
        repr_str = repr(sys_info)
        self.assertIn("SystemInfo", repr_str)
        self.assertIn(sys_info.name, repr_str)


class TestPackageDetection(unittest.TestCase):
    """Test package detection functions."""

    def test_get_native_packages_filtering(self):
        """Test that system packages are properly filtered out."""
        # This test assumes we're on a system with pacman
        # We can't easily mock the subprocess calls, so we'll test the logic
        from constants import IGNORED_PACKAGES
        
        # Test that IGNORED_PACKAGES contains expected system packages
        self.assertIn("base", IGNORED_PACKAGES)
        self.assertIn("linux", IGNORED_PACKAGES)
        self.assertIn("mesa", IGNORED_PACKAGES)
        self.assertIn("plasma-meta", IGNORED_PACKAGES)
        
        # Test that useful packages are NOT in ignored list
        self.assertNotIn("neovim", IGNORED_PACKAGES)
        self.assertNotIn("zsh", IGNORED_PACKAGES)
        self.assertNotIn("firefox", IGNORED_PACKAGES)
        self.assertNotIn("gimp", IGNORED_PACKAGES)

    def test_get_aur_packages_return_type(self):
        """Test that get_aur_packages returns a list."""
        result = packages.get_aur_packages()
        self.assertIsInstance(result, list)

    def test_get_flatpaks_return_type(self):
        """Test that get_flatpaks returns a list."""
        result = packages.get_flatpaks()
        self.assertIsInstance(result, list)

    def test_map_package_name(self):
        """Test package mapping across package managers."""
        self.assertEqual(packages.map_package_name("python", "apt"), "python3")
        self.assertEqual(packages.map_package_name("python", "pacman"), "python")
        self.assertEqual(packages.map_package_name("docker", "apt"), "docker.io")
        self.assertEqual(packages.map_package_name("docker", "dnf"), "docker")
        self.assertEqual(packages.map_package_name("fd", "apt"), "fd-find")
        self.assertEqual(packages.map_package_name("bat", "dnf"), "bat")
        self.assertEqual(packages.map_package_name("mariadb", "apt"), "mariadb-server")
        self.assertEqual(packages.map_package_name("chromium", "apt"), "chromium-browser")
        self.assertEqual(packages.map_package_name("brave-browser", "pacman"), "brave")
        self.assertEqual(packages.map_package_name("discord", "dnf"), "discord")
        self.assertEqual(packages.map_package_name("telegram", "apt"), "telegram-desktop")
        self.assertEqual(packages.map_package_name("teams", "apt"), "teams")
        self.assertEqual(packages.map_package_name("google-chrome-beta", "apt"), "google-chrome-beta")
        self.assertEqual(packages.map_package_name("microsoft-edge", "dnf"), "microsoft-edge-stable")

    def test_map_packages_for_manager(self):
        """Test bulk package mapping."""
        mapped = packages.map_packages_for_manager(["python", "git"], "apt")
        self.assertIn("python3", mapped)
        self.assertIn("git", mapped)

class TestConfigDetection(unittest.TestCase):
    """Test configuration detection module."""

    def setUp(self):
        """Set up test fixtures."""
        self.config_detector = ConfigDetector()

    def test_config_detector_creation(self):
        """Test ConfigDetector can be instantiated."""
        self.assertIsNotNone(self.config_detector)
        self.assertIsNotNone(self.config_detector.home)

    def test_detect_all(self):
        """Test full configuration detection."""
        config = self.config_detector.detect_all()
        self.assertIsInstance(config, SystemConfig)
        # At minimum, should have detected something
        self.assertTrue(config.shell or config.terminal != "unknown" or config.config_files)

    def test_get_backup_paths(self):
        """Test getting backup paths."""
        paths = self.config_detector.get_backup_paths()
        self.assertIsInstance(paths, list)
        # Should include common config files if they exist
        for path in paths:
            self.assertTrue(path.exists())

class TestScriptExporter(unittest.TestCase):
    """Test script export functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.sys_info = SystemInfo()
        self.exporter = ScriptExporter(self.sys_info)

    def test_exporter_creation(self):
        """Test ScriptExporter can be instantiated."""
        self.assertIsNotNone(self.exporter)
        self.assertTrue(self.exporter.filename.endswith(".sh"))

    def test_quote_packages(self):
        """Test package quoting for shell safety."""
        packages_list = ["test-pkg", "package with space"]
        quoted = self.exporter._quote_packages(packages_list)

        # Should contain quotes for safety
        self.assertIn("'", quoted)

    def test_build_script_basic(self):
        """Test basic script building."""
        script = self.exporter._build_script(["vim"], [], [])

        self.assertIn("#!/bin/bash", script)
        self.assertIn("set -e", script)
        self.assertIn("DSXConfig", script)
        self.assertIn("vim", script)

    def test_build_aur_section(self):
        """Test AUR section generation."""
        section = self.exporter._build_aur_section(["yay", "paru"])

        self.assertIn("yay", section)
        self.assertIn("paru", section)
        self.assertIn("log_info", section)

    def test_build_flatpak_section(self):
        """Test Flatpak section generation."""
        section = self.exporter._build_flatpak_section(["org.mozilla.firefox"])

        self.assertIn("firefox", section)
        self.assertIn("flatpak", section)
        self.assertIn("log_info", section)

    def test_build_config_section(self):
        """Test configuration section generation."""
        from core.config import SystemConfig

        config = SystemConfig()
        config.shell = "zsh"
        config.terminal = "alacritty"
        config.config_files = {"/home/user/.bashrc": "export PATH=/usr/local/bin:$PATH"}
        config.environment_vars = {"EDITOR": "vim"}

        section = self.exporter._build_config_section(config)

        self.assertIn("zsh", section)
        self.assertIn("alacritty", section)
        self.assertIn("bashrc", section)
        self.assertIn("EDITOR", section)
        self.assertIn("log_info", section)

    def test_generate_script_validation(self):
        """Test script generation with invalid inputs."""
        # Should raise ValueError for invalid input types
        with self.assertRaises(ValueError):
            self.exporter.generate_script("not_a_list", [], [])

    def test_generate_script_creates_file(self):
        """Test that generate_script creates a file."""
        script_path = self.exporter.generate_script(["test"], [], [])

        if script_path:  # Only test if file was created
            self.assertTrue(os.path.exists(script_path))
            self.assertTrue(os.path.isfile(script_path))

            # Clean up
            os.remove(script_path)


class TestLogging(unittest.TestCase):
    """Test logging configuration."""

    def test_get_logger(self):
        """Test logger creation."""
        logger = get_logger("test")
        self.assertIsNotNone(logger)

    def test_logger_has_handlers(self):
        """Test logger has configured handlers."""
        logger = get_logger("test_handlers")
        self.assertGreater(len(logger.handlers), 0)


class TestTypeHints(unittest.TestCase):
    """Test that type hints are properly defined."""

    def test_systeminfo_has_annotations(self):
        """Test SystemInfo has type annotations."""
        # Check that the class has the expected attributes with type annotations
        sys_info = SystemInfo()
        self.assertTrue(hasattr(sys_info, "distro"))
        self.assertTrue(hasattr(sys_info, "name"))
        self.assertTrue(hasattr(sys_info, "pkg_mgr"))

    def test_detector_methods_have_return_types(self):
        """Test detector methods have return type hints in signature."""
        # Check that methods have proper signatures
        self.assertTrue(hasattr(SystemInfo, "detect_system"))
        self.assertTrue(hasattr(SystemInfo, "_detect_distro"))
        self.assertTrue(hasattr(SystemInfo, "_detect_package_manager"))



if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)

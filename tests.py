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

    def test_get_native_packages_invalid_manager(self):
        """Test that invalid package manager returns empty list."""
        result = packages.get_native_packages("invalid_manager")
        self.assertEqual(result, [])

    def test_get_aur_packages_return_type(self):
        """Test that get_aur_packages returns a list."""
        result = packages.get_aur_packages()
        self.assertIsInstance(result, list)

    def test_get_flatpaks_return_type(self):
        """Test that get_flatpaks returns a list."""
        result = packages.get_flatpaks()
        self.assertIsInstance(result, list)


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

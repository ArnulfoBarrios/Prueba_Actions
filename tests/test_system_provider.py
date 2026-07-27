"""
Unit tests for SystemProvider class using unittest standard library.
Follows testing naming rule: should [action] when [condition].
"""

import unittest
from unittest.mock import patch
from system_inspector.system_provider import SystemProvider


class TestSystemProvider(unittest.TestCase):

    def setUp(self):
        self.provider = SystemProvider()

    def test_should_return_os_name_when_called(self):
        os_name = self.provider.get_os_name()
        self.assertIsInstance(os_name, str)
        self.assertTrue(len(os_name) > 0)

    def test_should_return_os_release_when_called(self):
        release = self.provider.get_os_release()
        self.assertIsInstance(release, str)

    def test_should_return_architecture_when_called(self):
        arch = self.provider.get_architecture()
        self.assertIsInstance(arch, str)

    def test_should_return_python_version_when_called(self):
        version = self.provider.get_python_version()
        self.assertIsInstance(version, str)
        self.assertIn(".", version)

    def test_should_return_path_separator_when_called(self):
        sep = self.provider.get_path_separator()
        self.assertIn(sep, ["/", "\\"])

    def test_should_return_disk_usage_when_valid_path(self):
        disk = self.provider.get_disk_usage()
        self.assertIn("total_gb", disk)
        self.assertIn("used_gb", disk)
        self.assertIn("free_gb", disk)
        self.assertGreaterEqual(disk["total_gb"], 0)

    def test_should_fallback_disk_usage_when_shutil_raises_exception(self):
        with patch("shutil.disk_usage", side_effect=Exception("Disk error")):
            disk = self.provider.get_disk_usage("/invalid_path")
            self.assertEqual(disk, {"total_gb": 0.0, "used_gb": 0.0, "free_gb": 0.0})

    def test_should_return_environment_summary_when_requested(self):
        summary = self.provider.get_environment_summary()
        self.assertIn("os_name", summary)
        self.assertIn("architecture", summary)
        self.assertIn("disk_usage", summary)


if __name__ == "__main__":
    unittest.main()

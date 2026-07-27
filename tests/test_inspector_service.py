"""
Unit tests for InspectorService class using unittest standard library.
Follows testing naming rule: should [action] when [condition].
"""

import unittest
from unittest.mock import MagicMock
from system_inspector.inspector_service import InspectorService


class TestInspectorService(unittest.TestCase):

    def test_should_categorize_as_windows_when_os_is_windows(self):
        mock_provider = MagicMock()
        mock_provider.get_os_name.return_value = "Windows"
        service = InspectorService(system_provider=mock_provider)

        category = service.get_platform_category()
        self.assertEqual(category, "Windows OS")

    def test_should_categorize_as_linux_when_os_is_linux(self):
        mock_provider = MagicMock()
        mock_provider.get_os_name.return_value = "Linux"
        service = InspectorService(system_provider=mock_provider)

        category = service.get_platform_category()
        self.assertEqual(category, "Linux OS")

    def test_should_categorize_as_macos_when_os_is_darwin(self):
        mock_provider = MagicMock()
        mock_provider.get_os_name.return_value = "Darwin"
        service = InspectorService(system_provider=mock_provider)

        category = service.get_platform_category()
        self.assertEqual(category, "macOS")

    def test_should_categorize_as_unknown_when_os_unrecognized(self):
        mock_provider = MagicMock()
        mock_provider.get_os_name.return_value = "CustomOS"
        service = InspectorService(system_provider=mock_provider)

        category = service.get_platform_category()
        self.assertEqual(category, "Sistema Desconocido")

    def test_should_mark_healthy_when_free_disk_above_threshold(self):
        mock_provider = MagicMock()
        mock_provider.get_environment_summary.return_value = {
            "disk_usage": {"free_gb": 5.0}
        }
        service = InspectorService(system_provider=mock_provider)

        health = service.evaluate_system_health()
        self.assertTrue(health["healthy"])
        self.assertIn("suficiente", health["status_message"])

    def test_should_mark_unhealthy_when_free_disk_below_threshold(self):
        mock_provider = MagicMock()
        mock_provider.get_environment_summary.return_value = {
            "disk_usage": {"free_gb": 0.5}
        }
        service = InspectorService(system_provider=mock_provider)

        health = service.evaluate_system_health()
        self.assertFalse(health["healthy"])
        self.assertIn("Alerta", health["status_message"])

    def test_should_format_text_report_when_requested(self):
        mock_provider = MagicMock()
        mock_provider.get_os_name.return_value = "Linux"
        mock_provider.get_environment_summary.return_value = {
            "os_name": "Linux",
            "os_release": "5.15.0",
            "architecture": "x86_64",
            "python_version": "3.11.0",
            "path_separator": "/",
            "disk_usage": {"total_gb": 100.0, "used_gb": 40.0, "free_gb": 60.0},
        }
        service = InspectorService(system_provider=mock_provider)

        output = service.format_text_report()
        self.assertIn("INSPECTOR DE SISTEMA MULTIPLATAFORMA", output)
        self.assertIn("Linux OS", output)
        self.assertIn("60.0 GB", output)


if __name__ == "__main__":
    unittest.main()

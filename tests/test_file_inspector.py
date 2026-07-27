"""
Unit tests for FileInspectorService using unittest.
Follows testing naming rule: should [action] when [condition].
"""

import os
import tempfile
import unittest
from system_inspector.file_inspector import FileInspectorService


class TestFileInspectorService(unittest.TestCase):

    def setUp(self):
        self.service = FileInspectorService()

    def test_should_return_error_when_file_does_not_exist(self):
        result = self.service.inspect_file("non_existent_file_path_12345.txt")
        self.assertFalse(result["valid"])
        self.assertIn("File not found", result["error"])

    def test_should_return_error_when_path_is_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.service.inspect_file(temp_dir)
            self.assertFalse(result["valid"])
            self.assertIn("not a regular file", result["error"])

    def test_should_inspect_crlf_windows_file_when_valid_text_file(self):
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".txt") as temp_file:
            temp_file.write(b"Line 1\r\nLine 2\r\nLine 3\r\n")
            temp_path = temp_file.name

        try:
            result = self.service.inspect_file(temp_path)
            self.assertTrue(result["valid"])
            self.assertEqual(result["line_endings"], "Windows (CRLF)")
            self.assertTrue(result["mvp_ready"])
            self.assertIn("Apto para MVP", result["mvp_verdict"])
            self.assertEqual(result["line_count"], 4)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_should_inspect_lf_unix_file_when_valid_text_file(self):
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".txt") as temp_file:
            temp_file.write(b"Line 1\nLine 2\nLine 3\n")
            temp_path = temp_file.name

        try:
            result = self.service.inspect_file(temp_path)
            self.assertTrue(result["valid"])
            self.assertEqual(result["line_endings"], "Linux / macOS (LF)")
            self.assertTrue(result["mvp_ready"])
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_should_detect_binary_file_when_contains_null_bytes(self):
        with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".bin") as temp_file:
            temp_file.write(b"\x00\x01\x02BinaryData\x00")
            temp_path = temp_file.name

        try:
            result = self.service.inspect_file(temp_path)
            self.assertTrue(result["valid"])
            self.assertEqual(result["encoding"], "Binario")
            self.assertEqual(result["line_endings"], "Binario")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()

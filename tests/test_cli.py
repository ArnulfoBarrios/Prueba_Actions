"""
Integration and CLI tests for system inspector using unittest standard library.
Follows testing naming rule: should [action] when [condition].
"""

import io
import json
import tempfile
import unittest
from unittest.mock import patch
from system_inspector.cli import main, create_parser


class TestCLI(unittest.TestCase):

    def test_should_parse_flags_when_created(self):
        parser = create_parser()
        args = parser.parse_args(["--json", "--gui", "--folder", "."])
        self.assertTrue(args.json)
        self.assertTrue(args.gui)
        self.assertEqual(args.folder, ".")
        self.assertFalse(args.summary)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_should_output_text_summary_when_default_execution(self, mock_stdout):
        exit_code = main([])
        output = mock_stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("INSPECTOR DE SISTEMA MULTIPLATAFORMA", output)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_should_output_valid_json_when_json_flag_passed(self, mock_stdout):
        exit_code = main(["--json"])
        output = mock_stdout.getvalue()
        self.assertEqual(exit_code, 0)

        parsed = json.loads(output)
        self.assertIn("platform_category", parsed)
        self.assertIn("system_info", parsed)
        self.assertIn("health_status", parsed)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_should_inspect_file_when_file_flag_passed(self, mock_stdout):
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False) as temp_file:
            temp_file.write("Hello World\nLine 2")
            temp_path = temp_file.name

        exit_code = main(["--file", temp_path])
        output = mock_stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("ANÁLISIS DE ARCHIVO", output)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_should_inspect_folder_when_folder_flag_passed(self, mock_stdout):
        exit_code = main(["--folder", "."])
        output = mock_stdout.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("EVALUACIÓN DE PROYECTO MVP", output)


if __name__ == "__main__":
    unittest.main()

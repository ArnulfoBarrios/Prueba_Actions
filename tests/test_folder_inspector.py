"""
Unit tests for FolderInspectorService using unittest.
Follows testing naming rule: should [action] when [condition].
"""

import os
import tempfile
import unittest
from system_inspector.folder_inspector import FolderInspectorService


class TestFolderInspectorService(unittest.TestCase):

    def setUp(self):
        self.service = FolderInspectorService()

    def test_should_return_error_when_folder_does_not_exist(self):
        result = self.service.inspect_folder("non_existent_folder_xyz_12345")
        self.assertFalse(result["valid"])
        self.assertIn("Folder not found", result["error"])

    def test_should_return_error_when_path_is_file(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            result = self.service.inspect_folder(temp_path)
            self.assertFalse(result["valid"])
            self.assertIn("not a directory", result["error"])
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_should_evaluate_full_mvp_folder_when_all_criteria_present(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            open(os.path.join(temp_dir, "pyproject.toml"), "w").close()
            open(os.path.join(temp_dir, "README.md"), "w").close()
            open(os.path.join(temp_dir, ".gitignore"), "w").close()
            open(os.path.join(temp_dir, "LICENSE"), "w").close()
            open(os.path.join(temp_dir, ".editorconfig"), "w").close()

            tests_dir = os.path.join(temp_dir, "tests")
            os.makedirs(tests_dir)
            open(os.path.join(tests_dir, "test_app.py"), "w").close()

            ci_dir = os.path.join(temp_dir, ".github", "workflows")
            os.makedirs(ci_dir)
            open(os.path.join(ci_dir, "ci.yml"), "w").close()

            result = self.service.inspect_folder(temp_dir)
            self.assertTrue(result["valid"])
            self.assertEqual(result["mvp_score"], 100)
            self.assertIn("APTO PARA MVP", result["mvp_verdict"])
            self.assertEqual(len(result["recommendations"]), 0)

    def test_should_detect_secret_key_when_hardcoded_in_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "config.py")
            with open(file_path, "w", encoding="utf-8") as fh:
                fh.write("AWS_KEY = 'AKIA1234567890ABCDEF'\n")

            result = self.service.inspect_folder(temp_dir)
            self.assertTrue(result["valid"])
            self.assertGreater(len(result["secret_findings"]), 0)

    def test_should_detect_syntax_error_when_python_corrupted(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "broken.py")
            with open(file_path, "w", encoding="utf-8") as fh:
                fh.write("def broken_func(\n")  # Syntax error

            result = self.service.inspect_folder(temp_dir)
            self.assertTrue(result["valid"])
            self.assertGreater(len(result["syntax_findings"]), 0)

    def test_should_detect_repo_bloat_when_unignored_folder_present(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            venv_dir = os.path.join(temp_dir, "node_modules")
            os.makedirs(venv_dir)

            result = self.service.inspect_folder(temp_dir)
            self.assertTrue(result["valid"])
            self.assertGreater(len(result["bloat_findings"]), 0)


if __name__ == "__main__":
    unittest.main()

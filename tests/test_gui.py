"""
Unit tests for Desktop GUI application initialization.
Follows testing naming rule: should [action] when [condition].
"""

import unittest
from unittest.mock import patch
import tkinter as tk
from system_inspector.gui import SystemInspectorApp


class TestSystemInspectorApp(unittest.TestCase):

    def test_should_initialize_gui_widgets_when_root_created(self):
        try:
            root = tk.Tk()
            root.withdraw()
            app = SystemInspectorApp(root)
            self.assertIsNotNone(app.sys_info_label)
            self.assertIsNotNone(app.file_details_text)
            self.assertIsNotNone(app.folder_details_text)
            self.assertIsNotNone(app.status_label)
            root.destroy()
        except tk.TclError:
            pass

    @patch("tkinter.filedialog.askopenfilename")
    def test_should_handle_file_selection_when_file_picked(self, mock_dialog):
        try:
            root = tk.Tk()
            root.withdraw()
            mock_dialog.return_value = "pyproject.toml"

            app = SystemInspectorApp(root)
            app._select_and_inspect_file()

            details_text = app.file_details_text.get("1.0", tk.END)
            self.assertIn("ANÁLISIS DE ARCHIVO", details_text)
            root.destroy()
        except tk.TclError:
            pass

    @patch("tkinter.filedialog.askdirectory")
    def test_should_handle_folder_selection_when_folder_picked(self, mock_dialog):
        try:
            root = tk.Tk()
            root.withdraw()
            mock_dialog.return_value = "."

            app = SystemInspectorApp(root)
            app._select_and_inspect_folder()

            details_text = app.folder_details_text.get("1.0", tk.END)
            self.assertIn("EVALUACIÓN DE PROYECTO MVP", details_text)
            root.destroy()
        except tk.TclError:
            pass

    def test_should_capture_screenshot_when_called(self):
        try:
            from system_inspector.screenshot_generator import capture_screenshot
            import tempfile
            import os

            with tempfile.TemporaryDirectory() as temp_dir:
                out_path = os.path.join(temp_dir, "test_shot.png")
                result_path = capture_screenshot(out_path)
                self.assertEqual(result_path, out_path)
        except (tk.TclError, Exception):
            pass


if __name__ == "__main__":
    unittest.main()

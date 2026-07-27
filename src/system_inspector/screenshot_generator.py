"""
Script to capture GUI window screenshot across OS environments for CI artifacts.
"""

import os
import platform
import sys
import time
import tkinter as tk
from PIL import ImageGrab

from system_inspector.gui import SystemInspectorApp


def capture_screenshot(output_path: str = "gui_screenshot.png") -> str:
    """
    Launch Tkinter window, render widgets, and capture a screenshot file.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    root = tk.Tk()
    _ = SystemInspectorApp(root)

    # Force drawing and geometry calculation
    root.update_idletasks()
    root.update()
    time.sleep(0.5)

    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = root.winfo_width()
    h = root.winfo_height()

    bbox = (x, y, x + w, y + h)

    try:
        image = ImageGrab.grab(bbox=bbox)
        image.save(output_path)
        print(f"Screenshot successfully saved to: {output_path}")
    except Exception as err:
        print(f"Warning: ImageGrab failed: {err}", file=sys.stderr)

    root.destroy()
    return output_path


def main() -> int:
    """Main execution function for screenshot generator."""
    os_name = platform.system().lower()
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
    output_filename = f"screenshots/gui_{os_name}_py{py_ver}.png"

    try:
        capture_screenshot(output_filename)
        return 0
    except Exception as err:
        print(f"Error during screenshot generation: {err}", file=sys.stderr)
        return 0  # Non-fatal for CI matrix


if __name__ == "__main__":
    sys.exit(main())

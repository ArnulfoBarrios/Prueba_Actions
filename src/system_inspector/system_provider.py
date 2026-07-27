"""
Module responsible for retrieving system and environment metadata.
Follows the Data/System Access layer pattern.
"""

import os
import platform
import shutil
import sys
from typing import Dict, Any


class SystemProvider:
    """Provides low-level system and operating system data."""

    def get_os_name(self) -> str:
        """Return operating system name."""
        return platform.system()

    def get_os_release(self) -> str:
        """Return operating system release version."""
        return platform.release()

    def get_architecture(self) -> str:
        """Return machine architecture (e.g. x86_64, AMD64, arm64)."""
        return platform.machine()

    def get_python_version(self) -> str:
        """Return running Python implementation version."""
        return sys.version.split()[0]

    def get_path_separator(self) -> str:
        """Return system file path separator ('/' or '\\')."""
        return os.sep

    def get_disk_usage(self, path: str = ".") -> Dict[str, float]:
        """
        Return total, used, and free disk space in Gigabytes.
        """
        try:
            total, used, free = shutil.disk_usage(path)
            gigabyte = 1024 ** 3
            return {
                "total_gb": round(total / gigabyte, 2),
                "used_gb": round(used / gigabyte, 2),
                "free_gb": round(free / gigabyte, 2),
            }
        except Exception:
            return {"total_gb": 0.0, "used_gb": 0.0, "free_gb": 0.0}

    def get_environment_summary(self) -> Dict[str, Any]:
        """Consolidate system metadata into a dictionary."""
        return {
            "os_name": self.get_os_name(),
            "os_release": self.get_os_release(),
            "architecture": self.get_architecture(),
            "python_version": self.get_python_version(),
            "path_separator": self.get_path_separator(),
            "disk_usage": self.get_disk_usage(),
        }

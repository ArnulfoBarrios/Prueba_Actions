"""
System Inspector package initialization module.
"""

from system_inspector.file_inspector import FileInspectorService
from system_inspector.inspector_service import InspectorService
from system_inspector.system_provider import SystemProvider

__version__ = "0.1.0"
__all__ = ["SystemProvider", "InspectorService", "FileInspectorService"]

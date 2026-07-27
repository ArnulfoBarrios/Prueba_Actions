"""
Service module for processing and formatting system info reports.
Follows SOLID business logic separation.
"""

from typing import Dict, Any
from system_inspector.system_provider import SystemProvider


class InspectorService:
    """Business logic service for evaluating system health and building reports."""

    def __init__(self, system_provider: SystemProvider | None = None) -> None:
        self._provider = system_provider or SystemProvider()

    def get_platform_category(self) -> str:
        """Determine human-friendly OS category in Spanish."""
        os_name = self._provider.get_os_name().lower()
        if "windows" in os_name:
            return "Windows OS"
        elif "linux" in os_name:
            return "Linux OS"
        elif "darwin" in os_name:
            return "macOS"
        return "Sistema Desconocido"

    def evaluate_system_health(self) -> Dict[str, Any]:
        """
        Evaluate system health metrics such as free disk space availability.
        """
        env = self._provider.get_environment_summary()
        free_gb = env.get("disk_usage", {}).get("free_gb", 0.0)

        is_healthy = free_gb > 1.0  # At least 1 GB free
        status_message = (
            "Espacio en disco suficiente"
            if is_healthy
            else "Alerta: Espacio en disco bajo"
        )

        return {
            "healthy": is_healthy,
            "status_message": status_message,
        }

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate a complete system report payload.
        """
        env_summary = self._provider.get_environment_summary()
        health = self.evaluate_system_health()
        category = self.get_platform_category()

        return {
            "platform_category": category,
            "system_info": env_summary,
            "health_status": health,
        }

    def format_text_report(self) -> str:
        """
        Format the system report as human-readable Spanish text output for CLI display.
        """
        report = self.generate_report()
        info = report["system_info"]
        health = report["health_status"]
        disk = info["disk_usage"]

        lines = [
            "==========================================",
            "   INSPECTOR DE SISTEMA MULTIPLATAFORMA   ",
            "==========================================",
            f" Categoría de S.O.: {report['platform_category']}",
            f" Nombre del S.O.  : {info['os_name']}",
            f" Versión/Release  : {info['os_release']}",
            f" Arquitectura     : {info['architecture']}",
            f" Versión Python   : {info['python_version']}",
            f" Separador Ruta   : '{info['path_separator']}'",
            "------------------------------------------",
            " USO DE DISCO:",
            f"   - Total : {disk['total_gb']} GB",
            f"   - Usado : {disk['used_gb']} GB",
            f"   - Libre : {disk['free_gb']} GB",
            "------------------------------------------",
            f" ESTADO DE SALUD  : {health['status_message']}",
            "==========================================",
        ]
        return "\n".join(lines)

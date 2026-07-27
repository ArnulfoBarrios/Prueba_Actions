"""
Module for analyzing files and evaluating cross-platform MVP readiness.
Follows SOLID business logic separation.
"""

import hashlib
import os
from typing import Dict, Any


class FileInspectorService:
    """Service to inspect file properties and cross-platform compatibility."""

    def inspect_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a file for size, integrity hash, line endings, and MVP compatibility.
        """
        if not os.path.exists(file_path):
            return {
                "valid": False,
                "error": f"File not found: {file_path}",
                "mvp_verdict": "Archivo no encontrado",
            }

        if not os.path.isfile(file_path):
            return {
                "valid": False,
                "error": f"Path is not a regular file: {file_path}",
                "mvp_verdict": "La ruta no es un archivo válido",
            }

        try:
            file_size_bytes = os.path.getsize(file_path)
            file_size_kb = round(file_size_bytes / 1024, 2)

            sha256_hash = self._calculate_sha256(file_path)
            line_ending_info = self._analyze_line_endings(file_path)
            encoding_info = "Texto / Utf-8" if line_ending_info["is_text"] else "Binario"

            mvp_ready = True
            warnings = []

            if line_ending_info["has_crlf"] and line_ending_info["has_lf"]:
                warnings.append("Saltos de línea mixtos (CRLF y LF) detectados")

            if file_size_bytes > 50 * 1024 * 1024:  # > 50MB
                warnings.append("El archivo supera los 50MB (Posible impacto en CI/CD)")

            verdict = "Apto para MVP Multiplataforma" if mvp_ready else "Atención Requerida"
            if warnings:
                verdict = f"Apto con advertencias: {', '.join(warnings)}"

            return {
                "valid": True,
                "file_name": os.path.basename(file_path),
                "file_path": os.path.abspath(file_path),
                "size_kb": file_size_kb,
                "size_bytes": file_size_bytes,
                "sha256": sha256_hash,
                "encoding": encoding_info,
                "line_endings": line_ending_info["type"],
                "line_count": line_ending_info["line_count"],
                "mvp_ready": mvp_ready,
                "mvp_verdict": verdict,
                "warnings": warnings,
            }
        except Exception as err:
            return {
                "valid": False,
                "error": str(err),
                "mvp_verdict": f"Error al procesar el archivo: {err}",
            }

    def _calculate_sha256(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as file_handle:
            while chunk := file_handle.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _analyze_line_endings(self, file_path: str) -> Dict[str, Any]:
        """Analyze file for text line endings (CRLF vs LF) and line count."""
        try:
            with open(file_path, "rb") as file_handle:
                sample = file_handle.read(1024 * 1024)  # Read up to 1MB sample

            # Check if binary file (contains null bytes)
            if b"\x00" in sample:
                return {
                    "is_text": False,
                    "type": "Binario",
                    "has_crlf": False,
                    "has_lf": False,
                    "line_count": 0,
                }

            has_crlf = b"\r\n" in sample
            # Replace CRLF to check for standalone LF
            sample_no_crlf = sample.replace(b"\r\n", b"")
            has_lf = b"\n" in sample_no_crlf

            if has_crlf and has_lf:
                ending_type = "Mixto (CRLF y LF)"
            elif has_crlf:
                ending_type = "Windows (CRLF)"
            elif has_lf:
                ending_type = "Linux / macOS (LF)"
            else:
                ending_type = "Línea Única / Sin Saltos"

            line_count = sample.count(b"\n") + 1
            return {
                "is_text": True,
                "type": ending_type,
                "has_crlf": has_crlf,
                "has_lf": has_lf,
                "line_count": line_count,
            }
        except Exception:
            return {
                "is_text": False,
                "type": "Desconocido",
                "has_crlf": False,
                "has_lf": False,
                "line_count": 0,
            }

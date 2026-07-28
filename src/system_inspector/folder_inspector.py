"""
Module for scanning project directories and evaluating MVP readiness.
Follows SOLID business logic separation.
"""

import os
from typing import Dict, Any, List


class FolderInspectorService:
    """Service to analyze full project directories for MVP compliance."""

    CONFIG_FILES = [
        "pyproject.toml", "setup.py", "package.json", "requirements.txt",
        "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "Pipfile"
    ]
    DOC_FILES = ["README.md", "README.txt", "README", "readme.md"]
    VCS_FILES = [".gitignore", ".gitattributes", ".hgignore"]

    def inspect_folder(self, folder_path: str) -> Dict[str, Any]:
        """
        Analyze a folder for project structure, required MVP files, and line endings.
        """
        if not os.path.exists(folder_path):
            return {
                "valid": False,
                "error": f"Folder not found: {folder_path}",
                "mvp_verdict": "Carpeta no encontrada",
            }

        if not os.path.isdir(folder_path):
            return {
                "valid": False,
                "error": f"Path is not a directory: {folder_path}",
                "mvp_verdict": "La ruta no es un directorio válido",
            }

        abs_path = os.path.abspath(folder_path)
        items = os.listdir(abs_path)
        lower_items = [item.lower() for item in items]

        has_config = any(cfg.lower() in lower_items for cfg in self.CONFIG_FILES)
        has_docs = any(doc.lower() in lower_items for doc in self.DOC_FILES)
        has_vcs = any(vcs.lower() in lower_items for vcs in self.VCS_FILES)
        has_tests = self._check_for_tests(abs_path, lower_items)
        has_ci = self._check_for_ci(abs_path)

        line_ending_scan = self._scan_directory_line_endings(abs_path)

        criteria = [
            {"name": "Archivo de Configuración / Dependencias", "status": has_config, "weight": 20},
            {"name": "Documentación (README.md)", "status": has_docs, "weight": 20},
            {"name": "Control de Versiones (.gitignore)", "status": has_vcs, "weight": 15},
            {"name": "Suite de Pruebas (tests/)", "status": has_tests, "weight": 25},
            {"name": "Integración Continua (.github/workflows)", "status": has_ci, "weight": 20},
        ]

        score = sum(c["weight"] for c in criteria if c["status"])
        recommendations = self._generate_recommendations(criteria, line_ending_scan)

        if score >= 80:
            verdict = "🟢 APTO PARA MVP MULTIPLATAFORMA"
        elif score >= 50:
            verdict = "🟡 PARCIALMENTE VIABLE (Requiere mejoras)"
        else:
            verdict = "🔴 NO APTO COMO MVP (Faltan elementos esenciales)"

        return {
            "valid": True,
            "folder_name": os.path.basename(abs_path) or abs_path,
            "folder_path": abs_path,
            "mvp_score": score,
            "mvp_verdict": verdict,
            "criteria_checklist": criteria,
            "line_ending_issues": line_ending_scan["has_mixed"],
            "recommendations": recommendations,
        }

    def _check_for_tests(self, abs_path: str, lower_items: List[str]) -> bool:
        """Check if tests folder or test files exist."""
        if any(t in lower_items for t in ["tests", "test", "spec", "specs"]):
            return True

        for root, _, files in os.walk(abs_path):
            if ".git" in root or "__pycache__" in root or ".venv" in root:
                continue
            for file in files:
                f_lower = file.lower()
                if f_lower.startswith("test_") or f_lower.endswith("_test.py"):
                    return True
        return False

    def _check_for_ci(self, abs_path: str) -> bool:
        """Check for CI/CD workflow configuration files."""
        github_dir = os.path.join(abs_path, ".github", "workflows")
        if os.path.exists(github_dir) and os.path.isdir(github_dir):
            if os.listdir(github_dir):
                return True
        ci_files = [".gitlab-ci.yml", "jenkinsfile", ".circleci"]
        return any(os.path.exists(os.path.join(abs_path, ci)) for ci in ci_files)

    def _scan_directory_line_endings(self, abs_path: str) -> Dict[str, Any]:
        """Scan text files in directory for mixed CRLF and LF line endings."""
        crlf_count = 0
        lf_count = 0
        skip_dirs = ["__pycache__", "venv", "node_modules", ".git"]

        for root, dirs, files in os.walk(abs_path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
            for file in files:
                if file.endswith((".py", ".md", ".json", ".toml", ".yml", ".yaml", ".txt")):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "rb") as fh:
                            content = fh.read(1024 * 128)
                            if b"\r\n" in content:
                                crlf_count += 1
                            elif b"\n" in content:
                                lf_count += 1
                    except Exception:
                        pass

        has_mixed = crlf_count > 0 and lf_count > 0
        return {
            "crlf_files": crlf_count,
            "lf_files": lf_count,
            "has_mixed": has_mixed,
        }

    def _generate_recommendations(
        self, criteria: List[Dict[str, Any]], line_scan: Dict[str, Any]
    ) -> List[str]:
        """Generate human-readable Spanish recommendations for missing items."""
        recs = []
        for c in criteria:
            if not c["status"]:
                if "Configuración" in c["name"]:
                    recs.append("Agregar configuración (`pyproject.toml` o `requirements.txt`).")
                elif "Documentación" in c["name"]:
                    recs.append("Crear `README.md` explicando cómo ejecutar el proyecto.")
                elif "Control de Versiones" in c["name"]:
                    recs.append("Agregar `.gitignore` para omitir temporales y credenciales.")
                elif "Suite de Pruebas" in c["name"]:
                    recs.append("Crear carpeta `tests/` con pruebas automatizadas unitarias.")
                elif "Integración Continua" in c["name"]:
                    recs.append("Configurar GitHub Actions en `.github/workflows/ci.yml` para CI.")

        if line_scan["has_mixed"]:
            recs.append("Normalizar saltos de línea mixtos (CRLF y LF) usando `.gitattributes`.")

        return recs

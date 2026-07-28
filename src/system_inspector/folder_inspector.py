"""
Module for scanning project directories and evaluating advanced MVP readiness.
Detects security vulnerabilities, syntax errors, repo bloat, and language composition.
Follows SOLID business logic separation.
"""

import ast
import json
import os
import re
from typing import Dict, Any, List


class FolderInspectorService:
    """Service to analyze full project directories for MVP compliance and issues."""

    CONFIG_FILES = [
        "pyproject.toml", "setup.py", "package.json", "requirements.txt",
        "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "Pipfile"
    ]
    DOC_FILES = ["README.md", "README.txt", "README", "readme.md"]
    VCS_FILES = [".gitignore", ".gitattributes", ".hgignore"]
    LICENSE_FILES = ["LICENSE", "LICENSE.txt", "LICENSE.md", "license"]
    EDITOR_FILES = [".editorconfig"]

    SECRET_PATTERNS = [
        (re.compile(r"AKIA[0-9A-Z]{16}"), "Llave AWS Access Key ID"),
        (
            re.compile(r"(?i)(api[_-]?key|secret[_-]?key)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
            "API Key / Secret hardcodeada",
        ),
        (re.compile(r"(?i)bearer\s+[A-Za-z0-9_\-\.]{20,}"), "Token de autenticación Bearer"),
        (re.compile(r"(?i)password\s*=\s*['\"][^'\"]{8,}['\"]"), "Contraseña hardcodeada"),
    ]

    LANGUAGE_EXTENSIONS = {
        ".py": "Python",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".dart": "Dart",
        ".html": "HTML",
        ".htm": "HTML",
        ".css": "CSS",
        ".scss": "CSS",
        ".cpp": "C++",
        ".c": "C",
        ".h": "C/C++ Header",
        ".java": "Java",
        ".go": "Go",
        ".rs": "Rust",
        ".php": "PHP",
        ".rb": "Ruby",
        ".json": "JSON / Config",
        ".yaml": "YAML / Config",
        ".yml": "YAML / Config",
        ".toml": "TOML / Config",
        ".md": "Markdown",
    }

    def inspect_folder(self, folder_path: str) -> Dict[str, Any]:
        """
        Analyze a folder for project structure, security, syntax, and language breakdown.
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
        has_license = any(lic.lower() in lower_items for lic in self.LICENSE_FILES)
        has_editorconfig = any(edf.lower() in lower_items for edf in self.EDITOR_FILES)
        has_tests = self._check_for_tests(abs_path, lower_items)
        has_ci = self._check_for_ci(abs_path)

        secret_findings = self._scan_for_secrets(abs_path)
        syntax_findings = self._validate_syntax(abs_path)
        bloat_findings = self._check_repo_bloat(abs_path)
        line_ending_scan = self._scan_directory_line_endings(abs_path)
        language_breakdown = self._analyze_language_breakdown(abs_path)

        criteria = [
            {"name": "Configuración de Proyecto", "status": has_config, "weight": 15},
            {"name": "Documentación (README.md)", "status": has_docs, "weight": 15},
            {"name": "Control de Versiones (.gitignore)", "status": has_vcs, "weight": 10},
            {"name": "Licencia del Proyecto (LICENSE)", "status": has_license, "weight": 10},
            {
                "name": "Estándar de Edición (.editorconfig)",
                "status": has_editorconfig,
                "weight": 10,
            },
            {"name": "Suite de Pruebas (tests/)", "status": has_tests, "weight": 20},
            {"name": "Integración Continua (.github/workflows)", "status": has_ci, "weight": 20},
        ]

        score = sum(c["weight"] for c in criteria if c["status"])

        if secret_findings:
            score = max(0, score - 20)
        if syntax_findings:
            score = max(0, score - 15)

        recommendations = self._generate_recommendations(
            criteria, secret_findings, syntax_findings, bloat_findings, line_ending_scan
        )

        if score >= 80 and not secret_findings and not syntax_findings:
            verdict = "APTO PARA MVP MULTIPLATAFORMA"
        elif score >= 50:
            verdict = "PARCIALMENTE VIABLE (Requiere mejoras)"
        else:
            verdict = "NO APTO COMO MVP (Faltan elementos esenciales)"

        return {
            "valid": True,
            "folder_name": os.path.basename(abs_path) or abs_path,
            "folder_path": abs_path,
            "mvp_score": score,
            "mvp_verdict": verdict,
            "criteria_checklist": criteria,
            "secret_findings": secret_findings,
            "syntax_findings": syntax_findings,
            "bloat_findings": bloat_findings,
            "line_ending_issues": line_ending_scan["has_mixed"],
            "language_breakdown": language_breakdown["percentages"],
            "total_scanned_files": language_breakdown["total_files"],
            "primary_language": language_breakdown["primary_language"],
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

    def _scan_for_secrets(self, abs_path: str) -> List[str]:
        """Scan text source files for hardcoded secrets or API keys."""
        findings = []
        skip_dirs = ["__pycache__", "venv", ".venv", "node_modules", ".git"]
        extensions = (".py", ".json", ".yml", ".yaml", ".env", ".toml", ".js", ".ts", ".txt")

        for root, dirs, files in os.walk(abs_path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for file in files:
                if file.endswith(extensions):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, abs_path)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
                            content = fh.read(1024 * 256)
                            for pattern, desc in self.SECRET_PATTERNS:
                                if pattern.search(content):
                                    findings.append(f"{desc} detectada en `{rel_path}`")
                    except Exception:
                        pass
        return findings

    def _validate_syntax(self, abs_path: str) -> List[str]:
        """Validate syntax for Python (.py) and JSON (.json) files."""
        syntax_errors = []
        skip_dirs = ["__pycache__", "venv", ".venv", "node_modules", ".git"]

        for root, dirs, files in os.walk(abs_path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, abs_path)
                if file.endswith(".py"):
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
                            ast.parse(fh.read(), filename=file_path)
                    except SyntaxError as err:
                        syntax_errors.append(
                            f"Error de sintaxis Python en `{rel_path}` (Línea {err.lineno})"
                        )
                    except Exception:
                        pass
                elif file.endswith(".json"):
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fh:
                            json.load(fh)
                    except json.JSONDecodeError as err:
                        syntax_errors.append(
                            f"JSON inválido en `{rel_path}` (Línea {err.lineno})"
                        )
                    except Exception:
                        pass
        return syntax_errors

    def _check_repo_bloat(self, abs_path: str) -> List[str]:
        """Detect large files (>10MB) or unignored temporary/environment folders."""
        bloat = []
        unignored_candidates = ["node_modules", ".venv", "venv", "__pycache__", ".DS_Store"]

        items = os.listdir(abs_path)
        for item in items:
            if item in unignored_candidates:
                bloat.append(f"Carpeta/archivo temporal `{item}` presente en la raíz.")

        for root, dirs, files in os.walk(abs_path):
            dirs[:] = [d for d in dirs if d not in ["venv", ".venv", "node_modules", ".git"]]
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    size_bytes = os.path.getsize(file_path)
                    if size_bytes > 10 * 1024 * 1024:  # > 10MB
                        size_mb = round(size_bytes / (1024 * 1024), 2)
                        rel_path = os.path.relpath(file_path, abs_path)
                        bloat.append(f"Archivo pesado `{rel_path}` ({size_mb} MB).")
                except Exception:
                    pass
        return bloat

    def _scan_directory_line_endings(self, abs_path: str) -> Dict[str, Any]:
        """Scan text files in directory for mixed CRLF and LF line endings."""
        crlf_count = 0
        lf_count = 0
        skip_dirs = ["__pycache__", "venv", ".venv", "node_modules", ".git"]

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

    def _analyze_language_breakdown(self, abs_path: str) -> Dict[str, Any]:
        """Calculate programming language composition percentages across files."""
        counts: Dict[str, int] = {}
        total_files = 0
        skip_dirs = ["__pycache__", "venv", ".venv", "node_modules", ".git"]

        for root, dirs, files in os.walk(abs_path):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for file in files:
                _, ext = os.path.splitext(file.lower())
                if ext in self.LANGUAGE_EXTENSIONS:
                    lang = self.LANGUAGE_EXTENSIONS[ext]
                    counts[lang] = counts.get(lang, 0) + 1
                    total_files += 1

        if total_files == 0:
            return {
                "percentages": {"Otros": 100.0},
                "total_files": 0,
                "primary_language": "N/A",
            }

        percentages: Dict[str, float] = {}
        for lang, count in counts.items():
            percentages[lang] = round((count / total_files) * 100, 1)

        primary = max(percentages, key=percentages.get) if percentages else "Otros"

        return {
            "percentages": percentages,
            "total_files": total_files,
            "primary_language": primary,
        }

    def _generate_recommendations(
        self,
        criteria: List[Dict[str, Any]],
        secrets: List[str],
        syntax: List[str],
        bloat: List[str],
        line_scan: Dict[str, Any],
    ) -> List[str]:
        """Generate human-readable Spanish recommendations for missing items or issues."""
        recs = []

        if secrets:
            recs.append(f"🔐 SEGURIDAD: Remover credenciales ({len(secrets)} halladas).")

        if syntax:
            recs.append(f"⚠️ SINTAXIS: Corregir errores de sintaxis ({len(syntax)} archivos).")

        for c in criteria:
            if not c["status"]:
                if "Configuración" in c["name"]:
                    recs.append("Agregar configuración (`pyproject.toml` o `requirements.txt`).")
                elif "Documentación" in c["name"]:
                    recs.append("Crear `README.md` explicando cómo ejecutar el proyecto.")
                elif "Control de Versiones" in c["name"]:
                    recs.append("Agregar `.gitignore` para omitir temporales y credenciales.")
                elif "Licencia" in c["name"]:
                    recs.append("Agregar un archivo `LICENSE` (ej. MIT, Apache 2.0).")
                elif "Estándar de Edición" in c["name"]:
                    recs.append("Agregar `.editorconfig` para estandarizar sangrías.")
                elif "Suite de Pruebas" in c["name"]:
                    recs.append("Crear carpeta `tests/` con pruebas automatizadas.")
                elif "Integración Continua" in c["name"]:
                    recs.append("Configurar GitHub Actions en `.github/workflows/ci.yml`.")

        if bloat:
            recs.append("📦 OPTIMIZACIÓN: Omitir o eliminar archivos pesados no ignorados.")

        if line_scan["has_mixed"]:
            recs.append("Normalizar saltos de línea mixtos (CRLF y LF) usando `.gitattributes`.")

        return recs

"""
Desktop Graphical User Interface (GUI) module using Tkinter.
Provides interactive window, system status dashboard, file inspector, and folder MVP evaluator.
"""

import sys
import tkinter as tk
from tkinter import filedialog, ttk

from system_inspector.file_inspector import FileInspectorService
from system_inspector.folder_inspector import FolderInspectorService
from system_inspector.inspector_service import InspectorService


class SystemInspectorApp:
    """Main Desktop Window application for System Inspector."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Inspector de Sistema & Evaluador MVP Multiplataforma")
        self.root.geometry("860x680")
        self.root.minsize(740, 540)

        self._inspector_service = InspectorService()
        self._file_service = FileInspectorService()
        self._folder_service = FolderInspectorService()

        self._configure_styles()
        self._build_ui()
        self._load_system_info()

    def _configure_styles(self) -> None:
        """Configure TTK widget styling."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("Header.TFrame", background="#1e293b")
        style.configure(
            "Header.TLabel",
            background="#1e293b",
            foreground="#f8fafc",
            font=("Helvetica", 13, "bold"),
        )
        style.configure(
            "SubHeader.TLabel",
            background="#1e293b",
            foreground="#94a3b8",
            font=("Helvetica", 10),
        )

        style.configure("Card.TLabelframe", font=("Helvetica", 11, "bold"))
        style.configure("Action.TButton", font=("Helvetica", 10, "bold"), padding=6)
        style.configure("Close.TButton", font=("Helvetica", 10, "bold"), padding=6)

    def _build_ui(self) -> None:
        """Construct application widgets."""
        header_frame = ttk.Frame(self.root, style="Header.TFrame", padding=15)
        header_frame.pack(fill="x", side="top")

        ttk.Label(
            header_frame,
            text="💻 Inspector de Sistema & Evaluador de Proyectos MVP",
            style="Header.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            header_frame,
            text="Validador de entorno y diagnostico de carpetas MVP para Windows, Linux y macOS",
            style="SubHeader.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        main_container = ttk.Frame(self.root, padding=10)
        main_container.pack(fill="both", expand=True)

        # Tabbed Notebook Interface
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True, pady=(0, 10))

        # Tab 1: System Dashboard
        self.tab_sys = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_sys, text=" 📊 Estado del Sistema ")
        self._build_system_tab()

        # Tab 2: Folder MVP Inspector
        self.tab_folder = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_folder, text=" 📂 Evaluador de Carpeta MVP ")
        self._build_folder_tab()

        # Tab 3: File Inspector
        self.tab_file = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_file, text=" 📄 Inspector de Archivo ")
        self._build_file_tab()

        # Bottom Bar
        bottom_frame = ttk.Frame(main_container)
        bottom_frame.pack(fill="x", side="bottom")

        self.status_label = ttk.Label(bottom_frame, text="Listo.", font=("Helvetica", 9, "italic"))
        self.status_label.pack(side="left")

        ttk.Button(
            bottom_frame,
            text="❌ Cerrar Aplicación",
            style="Close.TButton",
            command=self.root.destroy,
        ).pack(side="right")

    def _build_system_tab(self) -> None:
        """Build System Status Tab."""
        system_card = ttk.LabelFrame(
            self.tab_sys,
            text=" 📊 Métricas del Sistema Operativo ",
            style="Card.TLabelframe",
            padding=10,
        )
        system_card.pack(fill="both", expand=True)

        self.sys_info_label = ttk.Label(
            system_card, text="Cargando información del sistema...", font=("Consolas", 9)
        )
        self.sys_info_label.pack(anchor="w")

    def _build_folder_tab(self) -> None:
        """Build Folder MVP Evaluator Tab."""
        folder_actions_frame = ttk.Frame(self.tab_folder)
        folder_actions_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            folder_actions_frame,
            text="📂 Seleccionar Carpeta de Proyecto",
            style="Action.TButton",
            command=self._select_and_inspect_folder,
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            folder_actions_frame,
            text="🔄 Limpiar",
            command=self._clear_folder_info,
        ).pack(side="left")

        self.folder_details_text = tk.Text(
            self.tab_folder,
            wrap="word",
            font=("Consolas", 10),
            bg="#f8fafc",
            fg="#0f172a",
            relief="solid",
            bd=1,
            height=16,
        )
        self.folder_details_text.pack(fill="both", expand=True)
        self.folder_details_text.insert(
            "1.0",
            "Haz clic en 'Seleccionar Carpeta' para evaluar si el proyecto es un MVP "
            "y obtener la lista de recomendaciones para completarlo...",
        )

    def _build_file_tab(self) -> None:
        """Build File Inspector Tab."""
        file_actions_frame = ttk.Frame(self.tab_file)
        file_actions_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            file_actions_frame,
            text="📄 Seleccionar Archivo",
            style="Action.TButton",
            command=self._select_and_inspect_file,
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            file_actions_frame,
            text="🔄 Limpiar",
            command=self._clear_file_info,
        ).pack(side="left")

        self.file_details_text = tk.Text(
            self.tab_file,
            wrap="word",
            font=("Consolas", 10),
            bg="#f8fafc",
            fg="#0f172a",
            relief="solid",
            bd=1,
            height=16,
        )
        self.file_details_text.pack(fill="both", expand=True)
        self.file_details_text.insert(
            "1.0",
            "Haz clic en 'Seleccionar Archivo' para analizar su formato y saltos de línea...",
        )

    def _load_system_info(self) -> None:
        """Retrieve system details and populate dashboard."""
        try:
            report_text = self._inspector_service.format_text_report()
            self.sys_info_label.config(text=report_text)
            self.status_label.config(text="Información del sistema cargada correctamente.")
        except Exception as err:
            self.sys_info_label.config(text=f"Error al cargar metadatos: {err}")

    def _select_and_inspect_folder(self) -> None:
        """Open folder dialog and evaluate folder MVP score."""
        folder_path = filedialog.askdirectory(title="Seleccionar carpeta de proyecto MVP")

        if not folder_path:
            return

        result = self._folder_service.inspect_folder(folder_path)
        self.folder_details_text.delete("1.0", tk.END)

        if not result.get("valid"):
            err_msg = f"❌ ERROR AL INSPECCIONAR CARPETA:\n{result.get('error')}"
            self.folder_details_text.insert("1.0", err_msg)
            self.status_label.config(text="Error al analizar la carpeta.")
            return

        output_lines = [
            "============================================================",
            f" 📂 EVALUACIÓN DE PROYECTO MVP: {result['folder_name']}",
            "============================================================",
            f" Ruta Absoluta : {result['folder_path']}",
            f" Puntaje MVP   : {result['mvp_score']} / 100",
            f" VEREDICTO     : {result['mvp_verdict']}",
            "------------------------------------------------------------",
            " CHECKLIST DE REQUISITOS MVP:",
        ]

        for item in result["criteria_checklist"]:
            icon = "  [✅ CUMPLIDO]" if item["status"] else "  [❌ FALTANTE]"
            output_lines.append(f"{icon} {item['name']}")

        output_lines.append("------------------------------------------------------------")

        if result.get("recommendations"):
            output_lines.append(" 💡 DIAGNÓSTICO Y RECOMENDACIONES PARA SER UN MVP:")
            for rec in result["recommendations"]:
                output_lines.append(f"   👉 {rec}")
        else:
            output_lines.append(" 🎉 ¡El proyecto cumple con todos los requisitos para ser un MVP!")

        output_lines.append("============================================================")

        status_msg = f"Carpeta '{result['folder_name']}' evaluada: {result['mvp_score']}/100"
        self.status_label.config(text=status_msg)

    def _clear_folder_info(self) -> None:
        """Clear folder details panel."""
        self.folder_details_text.delete("1.0", tk.END)
        self.folder_details_text.insert(
            "1.0",
            "Haz clic en 'Seleccionar Carpeta' para evaluar si el proyecto es un MVP...",
        )
        self.status_label.config(text="Listo.")

    def _select_and_inspect_file(self) -> None:
        """Open file dialog and run file inspection service."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo para inspección",
            filetypes=[
                ("Todos los archivos", "*.*"),
                ("Archivos de Texto", "*.txt *.md *.py *.json"),
            ],
        )

        if not file_path:
            return

        result = self._file_service.inspect_file(file_path)
        self.file_details_text.delete("1.0", tk.END)

        if not result.get("valid"):
            err_msg = f"❌ ERROR AL INSPECCIONAR ARCHIVO:\n{result.get('error')}"
            self.file_details_text.insert("1.0", err_msg)
            self.status_label.config(text="Error al analizar el archivo.")
            return

        output_lines = [
            "============================================================",
            f" 📄 ANÁLISIS DE ARCHIVO: {result['file_name']}",
            "============================================================",
            f" Ruta Absoluta      : {result['file_path']}",
            f" Tamaño             : {result['size_kb']} KB ({result['size_bytes']} bytes)",
            f" Codificación       : {result['encoding']}",
            f" Saltos de Línea    : {result['line_endings']}",
            f" Cantidad de Líneas : {result['line_count']}",
            f" Hash SHA-256       : {result['sha256']}",
            "------------------------------------------------------------",
            f" VEREDICTO MVP      : {result['mvp_verdict']}",
            "============================================================",
        ]

        if result.get("warnings"):
            output_lines.append("\n⚠️ ADVERTENCIAS:")
            for warn in result["warnings"]:
                output_lines.append(f"   - {warn}")

        self.file_details_text.insert("1.0", "\n".join(output_lines))
        self.status_label.config(text=f"Archivo '{result['file_name']}' analizado con éxito.")

    def _clear_file_info(self) -> None:
        """Clear file details panel."""
        self.file_details_text.delete("1.0", tk.END)
        self.file_details_text.insert(
            "1.0", "Haz clic en 'Seleccionar Archivo' para analizar su formato..."
        )
        self.status_label.config(text="Listo.")


def launch_gui() -> None:
    """Initialize and run the Tkinter desktop GUI event loop."""
    try:
        root = tk.Tk()
        _ = SystemInspectorApp(root)
        root.mainloop()
    except Exception as err:
        print(f"Error starting GUI application: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    launch_gui()

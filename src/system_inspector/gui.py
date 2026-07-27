"""
Desktop Graphical User Interface (GUI) module using Tkinter.
Provides interactive window, system status dashboard, and file inspector picker.
"""

import sys
import tkinter as tk
from tkinter import filedialog, ttk

from system_inspector.file_inspector import FileInspectorService
from system_inspector.inspector_service import InspectorService


class SystemInspectorApp:
    """Main Desktop Window application for System Inspector."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Inspector de Sistema Multiplataforma - MVP")
        self.root.geometry("820x620")
        self.root.minsize(700, 500)

        self._inspector_service = InspectorService()
        self._file_service = FileInspectorService()

        self._configure_styles()
        self._build_ui()
        self._load_system_info()

    def _configure_styles(self) -> None:
        """Configure TTK widget styling."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Custom colors
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
            text="💻 Inspector de Sistema Multiplataforma (GitHub Actions MVP)",
            style="Header.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            header_frame,
            text="Validador de entorno y compatibilidad de archivos para Windows, Linux y macOS",
            style="SubHeader.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        main_container = ttk.Frame(self.root, padding=15)
        main_container.pack(fill="both", expand=True)

        system_card = ttk.LabelFrame(
            main_container,
            text=" 📊 Estado del Sistema Operativo ",
            style="Card.TLabelframe",
            padding=10,
        )
        system_card.pack(fill="x", side="top", pady=(0, 10))

        self.sys_info_label = ttk.Label(
            system_card, text="Cargando información del sistema...", font=("Consolas", 9)
        )
        self.sys_info_label.pack(anchor="w")

        file_card = ttk.LabelFrame(
            main_container,
            text=" 📁 Inspector de Archivos MVP ",
            style="Card.TLabelframe",
            padding=10,
        )
        file_card.pack(fill="both", expand=True, pady=(0, 10))

        file_actions_frame = ttk.Frame(file_card)
        file_actions_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            file_actions_frame,
            text="📂 Seleccionar Archivo para Inspeccionar",
            style="Action.TButton",
            command=self._select_and_inspect_file,
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            file_actions_frame,
            text="🔄 Limpiar",
            command=self._clear_file_info,
        ).pack(side="left")

        self.file_details_text = tk.Text(
            file_card,
            wrap="word",
            font=("Consolas", 10),
            bg="#f8fafc",
            fg="#0f172a",
            relief="solid",
            bd=1,
            height=12,
        )
        self.file_details_text.pack(fill="both", expand=True)
        self.file_details_text.insert(
            "1.0",
            "Haz clic en 'Seleccionar Archivo' para analizar compatibilidad...",
        )

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

    def _load_system_info(self) -> None:
        """Retrieve system details and populate dashboard."""
        try:
            report_text = self._inspector_service.format_text_report()
            self.sys_info_label.config(text=report_text)
            self.status_label.config(text="Información del sistema cargada correctamente.")
        except Exception as err:
            self.sys_info_label.config(text=f"Error al cargar metadatos del sistema: {err}")

    def _select_and_inspect_file(self) -> None:
        """Open file dialog and run file inspection service."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo para inspección MVP",
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
            self.status_label.config(text="Error al analizar el archivo seleccionado.")
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
            "1.0", "Haz clic en 'Seleccionar Archivo' para analizar compatibilidad..."
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

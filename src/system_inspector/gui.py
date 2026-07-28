"""
Desktop Graphical User Interface (GUI) module designed with Apple macOS HIG aesthetic.
Provides modern, minimal dark graphite layout, system status dashboard, file inspector,
and advanced folder MVP evaluator.
"""

import sys
import tkinter as tk
from tkinter import filedialog, ttk

from system_inspector.file_inspector import FileInspectorService
from system_inspector.folder_inspector import FolderInspectorService
from system_inspector.inspector_service import InspectorService


class SystemInspectorApp:
    """Main Desktop Window application styled following Apple macOS HIG principles."""

    # Apple Dark Graphite Palette Tokens
    COLOR_BG = "#1c1c1e"
    COLOR_CARD = "#2c2c2e"
    COLOR_BORDER = "#3a3a3c"
    COLOR_PRIMARY_TEXT = "#f2f2f7"
    COLOR_SECONDARY_TEXT = "#8e8e93"
    COLOR_ACCENT = "#0a84ff"
    COLOR_SUCCESS = "#30d158"
    COLOR_WARNING = "#ffd60a"
    COLOR_DANGER = "#ff453a"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("System Inspector & MVP Evaluator")
        self.root.geometry("880x700")
        self.root.minsize(760, 560)
        self.root.configure(bg=self.COLOR_BG)

        self._inspector_service = InspectorService()
        self._file_service = FileInspectorService()
        self._folder_service = FolderInspectorService()

        self._configure_apple_styles()
        self._build_ui()
        self._load_system_info()

    def _configure_apple_styles(self) -> None:
        """Configure TTK widgets with clean Apple HIG dark Graphite aesthetic."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Global backgrounds
        style.configure(".", background=self.COLOR_BG, foreground=self.COLOR_PRIMARY_TEXT)

        # Header Frame
        style.configure("Header.TFrame", background=self.COLOR_CARD)
        style.configure(
            "HeaderTitle.TLabel",
            background=self.COLOR_CARD,
            foreground=self.COLOR_PRIMARY_TEXT,
            font=("Segoe UI", 14, "bold"),
        )
        style.configure(
            "HeaderSubtitle.TLabel",
            background=self.COLOR_CARD,
            foreground=self.COLOR_SECONDARY_TEXT,
            font=("Segoe UI", 10),
        )

        # Notebook Tabs
        style.configure(
            "TNotebook",
            background=self.COLOR_BG,
            borderwidth=0,
            tabmargins=[2, 5, 2, 0],
        )
        style.configure(
            "TNotebook.Tab",
            background=self.COLOR_CARD,
            foreground=self.COLOR_SECONDARY_TEXT,
            padding=[14, 8],
            font=("Segoe UI", 10, "bold"),
            borderwidth=1,
            focuscolor="",
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.COLOR_ACCENT)],
            foreground=[("selected", "#ffffff")],
        )

        # Cards & Labelframes
        style.configure(
            "AppleCard.TLabelframe",
            background=self.COLOR_CARD,
            foreground=self.COLOR_PRIMARY_TEXT,
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "AppleCard.TLabelframe.Label",
            background=self.COLOR_CARD,
            foreground=self.COLOR_PRIMARY_TEXT,
            font=("Segoe UI", 11, "bold"),
        )
        style.configure("CardInner.TFrame", background=self.COLOR_CARD)

        # Buttons
        style.configure(
            "ApplePrimary.TButton",
            font=("Segoe UI", 10, "bold"),
            background=self.COLOR_ACCENT,
            foreground="#ffffff",
            borderwidth=0,
            padding=[14, 8],
        )
        style.map("ApplePrimary.TButton", background=[("active", "#0071e3")])

        style.configure(
            "AppleSecondary.TButton",
            font=("Segoe UI", 10),
            background=self.COLOR_BORDER,
            foreground=self.COLOR_PRIMARY_TEXT,
            borderwidth=0,
            padding=[10, 6],
        )

        style.configure(
            "AppleClose.TButton",
            font=("Segoe UI", 10, "bold"),
            background=self.COLOR_DANGER,
            foreground="#ffffff",
            borderwidth=0,
            padding=[12, 6],
        )

    def _build_ui(self) -> None:
        """Construct Apple-styled application widgets."""
        header_frame = ttk.Frame(self.root, style="Header.TFrame", padding=18)
        header_frame.pack(fill="x", side="top")

        ttk.Label(
            header_frame,
            text="System Inspector & MVP Evaluator",
            style="HeaderTitle.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            header_frame,
            text="Multi-platform environment diagnostics and project MVP validator",
            style="HeaderSubtitle.TLabel",
        ).pack(anchor="w", pady=(3, 0))

        main_container = ttk.Frame(self.root, padding=15)
        main_container.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True, pady=(0, 10))

        # Tab 1: System Status
        self.tab_sys = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_sys, text="System Health")
        self._build_system_tab()

        # Tab 2: Folder Evaluator
        self.tab_folder = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_folder, text="Folder MVP Evaluator")
        self._build_folder_tab()

        # Tab 3: File Inspector
        self.tab_file = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.tab_file, text="File Inspector")
        self._build_file_tab()

        # Bottom Status Bar
        bottom_frame = ttk.Frame(main_container)
        bottom_frame.pack(fill="x", side="bottom")

        self.status_label = ttk.Label(
            bottom_frame,
            text="Ready.",
            font=("Segoe UI", 9),
            foreground=self.COLOR_SECONDARY_TEXT,
        )
        self.status_label.pack(side="left")

        ttk.Button(
            bottom_frame,
            text="Exit Application",
            style="AppleClose.TButton",
            command=self.root.destroy,
        ).pack(side="right")

    def _build_system_tab(self) -> None:
        """Build System Status Tab."""
        system_card = ttk.LabelFrame(
            self.tab_sys,
            text=" Operating System Metrics ",
            style="AppleCard.TLabelframe",
            padding=15,
        )
        system_card.pack(fill="both", expand=True)

        self.sys_info_label = ttk.Label(
            system_card,
            text="Loading system info...",
            font=("Consolas", 9),
            background=self.COLOR_CARD,
            foreground=self.COLOR_PRIMARY_TEXT,
        )
        self.sys_info_label.pack(anchor="w")

    def _build_folder_tab(self) -> None:
        """Build Folder MVP Evaluator Tab."""
        folder_card = ttk.LabelFrame(
            self.tab_folder,
            text=" Project Directory Analysis ",
            style="AppleCard.TLabelframe",
            padding=12,
        )
        folder_card.pack(fill="both", expand=True)

        actions_frame = ttk.Frame(folder_card, style="CardInner.TFrame")
        actions_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            actions_frame,
            text="Select Project Folder...",
            style="ApplePrimary.TButton",
            command=self._select_and_inspect_folder,
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            actions_frame,
            text="Clear",
            style="AppleSecondary.TButton",
            command=self._clear_folder_info,
        ).pack(side="left")

        self.folder_details_text = tk.Text(
            folder_card,
            wrap="word",
            font=("Consolas", 9.5),
            bg="#1e1e20",
            fg=self.COLOR_PRIMARY_TEXT,
            insertbackground=self.COLOR_PRIMARY_TEXT,
            relief="solid",
            bd=1,
            highlightthickness=0,
            height=16,
        )
        self.folder_details_text.pack(fill="both", expand=True)
        self.folder_details_text.insert(
            "1.0",
            "Click 'Select Project Folder' to evaluate project MVP status, security, and issues...",
        )

    def _build_file_tab(self) -> None:
        """Build File Inspector Tab."""
        file_card = ttk.LabelFrame(
            self.tab_file,
            text=" Single File Inspection ",
            style="AppleCard.TLabelframe",
            padding=12,
        )
        file_card.pack(fill="both", expand=True)

        actions_frame = ttk.Frame(file_card, style="CardInner.TFrame")
        actions_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            actions_frame,
            text="Select File...",
            style="ApplePrimary.TButton",
            command=self._select_and_inspect_file,
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            actions_frame,
            text="Clear",
            style="AppleSecondary.TButton",
            command=self._clear_file_info,
        ).pack(side="left")

        self.file_details_text = tk.Text(
            file_card,
            wrap="word",
            font=("Consolas", 9.5),
            bg="#1e1e20",
            fg=self.COLOR_PRIMARY_TEXT,
            insertbackground=self.COLOR_PRIMARY_TEXT,
            relief="solid",
            bd=1,
            highlightthickness=0,
            height=16,
        )
        self.file_details_text.pack(fill="both", expand=True)
        self.file_details_text.insert(
            "1.0",
            "Click 'Select File' to inspect format, encoding, SHA-256 hash, and line endings...",
        )

    def _load_system_info(self) -> None:
        """Retrieve system details and populate dashboard."""
        try:
            report_text = self._inspector_service.format_text_report()
            self.sys_info_label.config(text=report_text)
            self.status_label.config(text="System details loaded.")
        except Exception as err:
            self.sys_info_label.config(text=f"Error loading system details: {err}")

    def _select_and_inspect_folder(self) -> None:
        """Open folder dialog and evaluate folder MVP score."""
        folder_path = filedialog.askdirectory(title="Select Project Directory")

        if not folder_path:
            return

        result = self._folder_service.inspect_folder(folder_path)
        self.folder_details_text.delete("1.0", tk.END)

        if not result.get("valid"):
            err_msg = f"ERROR SCANNING DIRECTORY:\n{result.get('error')}"
            self.folder_details_text.insert("1.0", err_msg)
            self.status_label.config(text="Folder analysis failed.")
            return

        output_lines = [
            "============================================================",
            f" PROJECT MVP EVALUATION: {result['folder_name']}",
            "============================================================",
            f" Absolute Path : {result['folder_path']}",
            f" MVP Score     : {result['mvp_score']} / 100",
            f" VERDICT       : {result['mvp_verdict']}",
            "------------------------------------------------------------",
            " STANDARDS & STRUCTURE CHECKLIST:",
        ]

        for item in result["criteria_checklist"]:
            icon = "  [PASS]" if item["status"] else "  [FAIL]"
            output_lines.append(f"{icon} {item['name']}")

        output_lines.append("------------------------------------------------------------")

        if result.get("secret_findings"):
            output_lines.append(" 🔐 SECURITY ALERTS (Hardcoded Credentials/Tokens):")
            for sec in result["secret_findings"]:
                output_lines.append(f"   ! {sec}")
            output_lines.append("------------------------------------------------------------")

        if result.get("syntax_findings"):
            output_lines.append(" ⚠️ SYNTAX ERRORS (Python / JSON):")
            for syn in result["syntax_findings"]:
                output_lines.append(f"   ! {syn}")
            output_lines.append("------------------------------------------------------------")

        if result.get("bloat_findings"):
            output_lines.append(" 📦 REPOSITORY BLOAT WARNINGS:")
            for blt in result["bloat_findings"]:
                output_lines.append(f"   ! {blt}")
            output_lines.append("------------------------------------------------------------")

        if result.get("recommendations"):
            output_lines.append(" 💡 DIAGNOSTICS & ACTIONABLE RECOMMENDATIONS:")
            for rec in result["recommendations"]:
                output_lines.append(f"   -> {rec}")
        else:
            output_lines.append(" CONGRATULATIONS: Project meets all MVP standards!")

        output_lines.append("============================================================")

        self.folder_details_text.insert("1.0", "\n".join(output_lines))
        status_msg = f"Folder '{result['folder_name']}' evaluated: {result['mvp_score']}/100"
        self.status_label.config(text=status_msg)

    def _clear_folder_info(self) -> None:
        """Clear folder details panel."""
        self.folder_details_text.delete("1.0", tk.END)
        self.folder_details_text.insert(
            "1.0",
            "Click 'Select Project Folder' to evaluate project MVP status...",
        )
        self.status_label.config(text="Ready.")

    def _select_and_inspect_file(self) -> None:
        """Open file dialog and run file inspection service."""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                ("All files", "*.*"),
                ("Text files", "*.txt *.md *.py *.json"),
            ],
        )

        if not file_path:
            return

        result = self._file_service.inspect_file(file_path)
        self.file_details_text.delete("1.0", tk.END)

        if not result.get("valid"):
            err_msg = f"ERROR INSPECTING FILE:\n{result.get('error')}"
            self.file_details_text.insert("1.0", err_msg)
            self.status_label.config(text="File analysis failed.")
            return

        output_lines = [
            "============================================================",
            f" FILE ANALYSIS: {result['file_name']}",
            "============================================================",
            f" Absolute Path : {result['file_path']}",
            f" Size          : {result['size_kb']} KB ({result['size_bytes']} bytes)",
            f" Encoding      : {result['encoding']}",
            f" Line Endings  : {result['line_endings']}",
            f" Line Count    : {result['line_count']}",
            f" SHA-256 Hash  : {result['sha256']}",
            "------------------------------------------------------------",
            f" VERDICT       : {result['mvp_verdict']}",
            "============================================================",
        ]

        if result.get("warnings"):
            output_lines.append("\nWARNINGS:")
            for warn in result["warnings"]:
                output_lines.append(f"   - {warn}")

        self.file_details_text.insert("1.0", "\n".join(output_lines))
        self.status_label.config(text=f"File '{result['file_name']}' inspected successfully.")

    def _clear_file_info(self) -> None:
        """Clear file details panel."""
        self.file_details_text.delete("1.0", tk.END)
        self.file_details_text.insert(
            "1.0", "Click 'Select File' to inspect format..."
        )
        self.status_label.config(text="Ready.")


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

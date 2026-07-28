"""
Command line interface entry point for system inspector.
Presentation layer handling arguments, printing results, or launching desktop GUI.
"""

import argparse
import json
import sys
from typing import List, Optional

from system_inspector.file_inspector import FileInspectorService
from system_inspector.folder_inspector import FolderInspectorService
from system_inspector.inspector_service import InspectorService


def create_parser() -> argparse.ArgumentParser:
    """Create and configure command-line argument parser in Spanish."""
    parser = argparse.ArgumentParser(
        description="Inspector de Sistema Multiplataforma - Prueba GitHub Actions."
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Iniciar la aplicación gráfica de escritorio (GUI).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Imprimir el reporte en formato JSON.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Imprimir un resumen formateado legible por humanos.",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Ruta de archivo para inspeccionar su compatibilidad multiplataforma.",
    )
    parser.add_argument(
        "--folder",
        type=str,
        help="Ruta de carpeta/proyecto para evaluar su nivel de MVP y diagnósticos.",
    )
    return parser


def main(args_list: Optional[List[str]] = None) -> int:
    """Main execution function for CLI."""
    parser = create_parser()
    args = parser.parse_args(args_list)

    if args.gui:
        from system_inspector.gui import launch_gui
        launch_gui()
        return 0

    if args.folder:
        folder_service = FolderInspectorService()
        result = folder_service.inspect_folder(args.folder)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if not result.get("valid"):
                print(f"Error: {result.get('error')}")
            else:
                print("==========================================")
                print(f" 📂 EVALUACIÓN DE PROYECTO MVP: {result['folder_name']}")
                print("==========================================")
                print(f" Ruta         : {result['folder_path']}")
                print(f" Puntaje MVP  : {result['mvp_score']} / 100")
                print(f" Veredicto    : {result['mvp_verdict']}")
                print("------------------------------------------")
                print(" CHECKLIST DE CRITERIOS:")
                for item in result["criteria_checklist"]:
                    icon = "✅" if item["status"] else "❌"
                    print(f"  {icon} {item['name']}")
                print("------------------------------------------")
                if result.get("recommendations"):
                    print(" ⚠️ RECOMENDACIONES PARA SER UN MVP:")
                    for rec in result["recommendations"]:
                        print(f"   - {rec}")
                print("==========================================")
        return 0

    if args.file:
        file_service = FileInspectorService()
        result = file_service.inspect_file(args.file)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if not result.get("valid"):
                print(f"Error: {result.get('error')}")
            else:
                print("==========================================")
                print(f" 📄 ANÁLISIS DE ARCHIVO: {result['file_name']}")
                print("==========================================")
                print(f" Ruta       : {result['file_path']}")
                print(f" Tamaño     : {result['size_kb']} KB")
                print(f" Codificación: {result['encoding']}")
                print(f" Saltos Linea: {result['line_endings']}")
                print(f" SHA-256    : {result['sha256']}")
                print(f" Veredicto  : {result['mvp_verdict']}")
                print("==========================================")
        return 0

    service = InspectorService()

    if args.json:
        report_data = service.generate_report()
        print(json.dumps(report_data, indent=2, ensure_ascii=False))
    else:
        print(service.format_text_report())

    return 0


if __name__ == "__main__":
    sys.exit(main())

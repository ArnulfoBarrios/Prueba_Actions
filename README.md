# System Inspector & Evaluador de Proyectos MVP Multiplataforma

Este proyecto es una **aplicación de software de escritorio** y **suite CLI** escrita en Python, configurada para compilar **ejecutables nativos (`.exe` en Windows y `.app` en macOS)** y evaluar carpetas completas de proyectos para determinar su nivel de **Producto Mínimo Viable (MVP)**.

---

## 🚀 Características Principales

1. **Evaluador y Diagnóstico de Carpetas/Proyectos MVP**:
   - Analiza cualquier carpeta de proyecto y evalúa los 6 pilares esenciales de un MVP:
     - 📄 **Configuración**: Presencia de `pyproject.toml`, `setup.py`, `package.json` o `requirements.txt`.
     - 📖 **Documentación**: Presencia de `README.md`.
     - 🛡️ **Control de Versiones**: Presencia de `.gitignore`.
     - 🧪 **Suite de Pruebas**: Existencia de carpeta `tests/` o archivos de prueba.
     - ⚙️ **Integración Continua**: Configuración de GitHub Actions en `.github/workflows/`.
     - 🌐 **Compatibilidad Multiplataforma**: Detección de saltos de línea mixtos (`CRLF` vs `LF`).
   - Genera un **Puntaje MVP (0-100%)**, veredicto visual y **lista de recomendaciones específicas** con lo que falta para llegar a ser un MVP.

2. **Compilación de Ejecutables Nativos (.exe / .app)**:
   - Empacado autónomo con `PyInstaller` para ejecutar la aplicación sin requerir Python instalado.
   - En **GitHub Actions**, cada push compila automáticamente el ejecutable **`SystemInspector.exe`** en Windows y **`SystemInspector.app`** en macOS, dejándolos disponibles para descarga inmediata.

3. **Software de Escritorio (GUI)**:
   - Ventana con pestañas interactivas desarrolladas en `tkinter`:
     - 📊 Tablero de métricas del S.O.
     - 📂 Evaluador visual de carpetas de proyecto.
     - 📄 Inspector de archivos individuales.

---

## 📁 Estructura del Proyecto

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml               # Matriz de CI/CD y compilador de .exe / .app
├── src/
│   └── system_inspector/
│       ├── __init__.py
│       ├── system_provider.py    # Metadatos del S.O.
│       ├── inspector_service.py # Lógica de salud y métricas
│       ├── file_inspector.py    # Servicio de inspección de archivos
│       ├── folder_inspector.py  # Evaluador de carpetas y diagnósticos MVP
│       ├── gui.py               # Aplicación gráfica de escritorio (GUI Tkinter)
│       ├── screenshot_generator.py # Capturador de imágenes para CI
│       └── cli.py               # Interfaz de línea de comandos (CLI)
├── tests/                       # Suite de 33 pruebas unitarias e integración
├── pyproject.toml               # Empaquetado y dependencias
└── README.md                    # Documentación
```

---

## 🖥️ Cómo Usar el Software

### 1. Iniciar la Ventana de Escritorio (GUI)
```bash
system-inspector --gui
```
*O usando Python:*
```bash
python -m system_inspector.gui
```

### 2. Evaluar una Carpeta de Proyecto desde la Consola
```bash
python -m system_inspector.cli --folder .
```

### 3. Inspeccionar un Archivo Específico desde Consola
```bash
python -m system_inspector.cli --file pyproject.toml
```

### 4. Compilar Ejecutable Localmente con PyInstaller
- **En Windows (`SystemInspector.exe`)**:
  ```powershell
  pyinstaller --noconfirm --onefile --windowed --name SystemInspector src/system_inspector/cli.py
  ```
- **En macOS (`SystemInspector.app`)**:
  ```bash
  pyinstaller --noconfirm --onefile --windowed --name SystemInspector src/system_inspector/cli.py
  ```
*El ejecutable final se guardará en la carpeta `dist/`.*

---

## 🧪 Pruebas Automatizadas y Cobertura

Para ejecutar las 33 pruebas unitarias y verificar la cobertura de código:

```bash
pytest --cov=src/system_inspector --cov-report=term-missing tests/
```

Para verificar el linter de código:
```bash
flake8 src tests --max-line-length=100
```

---

## 📦 Descargar los Ejecutables (.exe / .app) desde GitHub Actions

1. Entra a tu repositorio: 👉 [https://github.com/ArnulfoBarrios/Prueba_Actions](https://github.com/ArnulfoBarrios/Prueba_Actions)
2. Haz clic en la pestaña **`Actions`**.
3. Selecciona la última ejecución del workflow **`Cross-Platform CI Matrix & Executable Builder`**.
4. En la sección **`Artifacts`** encontrarás los ejecutables listos para descargar:
   - 🪟 **`SystemInspector-Windows-Executable`** (`.exe`)
   - 🍏 **`SystemInspector-macOS-Executable`** (`.app` / ejecutable mac)
   - 🐧 **`SystemInspector-Linux-Executable`**

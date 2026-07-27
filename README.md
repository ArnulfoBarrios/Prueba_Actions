# Inspector de Sistema Multiplataforma & Validador de Archivos MVP

Este proyecto es una **aplicación de software de escritorio** y **herramienta CLI** escrita en Python, diseñada específicamente para probar el funcionamiento de aplicaciones en **Windows**, **Linux** y **macOS** mediante **GitHub Actions**.

---

## 🚀 Características Principales

1. **Software de Escritorio (GUI)**:
   - Ventana gráfica con botones de **Abrir y Cerrar**, panel de estado del sistema operativo y selector interactivo de archivos.
   - Desarrollado con `tkinter` para ejecutarse de forma nativa e idéntica en cualquier sistema operativo sin dependencias externas pesadas.

2. **Inspector de Archivos Multiplataforma para MVP**:
   - Inspección de archivos seleccionados por el usuario.
   - Identificación de saltos de línea (`CRLF` de Windows vs `LF` de Linux/macOS) para detectar posibles problemas de compatibilidad.
   - Cálculo de tamaño, codificación (UTF-8 / Binario), hash de integridad SHA-256 y cantidad de líneas.
   - **Veredicto de preparación para MVP**.

3. **Matriz de CI/CD en GitHub Actions**:
   - Ejecución automática de pruebas unitarias y linters en 9 entornos en paralelo (**Ubuntu, Windows, macOS** con **Python 3.10, 3.11, 3.12**).

---

## 📁 Estructura del Proyecto

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml               # Matriz de CI/CD para GitHub Actions
├── src/
│   └── system_inspector/
│       ├── __init__.py
│       ├── system_provider.py    # Proveedor de metadatos de hardware y S.O.
│       ├── inspector_service.py # Lógica de salud y diagnósticos
│       ├── file_inspector.py    # Servicio de inspección de archivos y veredicto MVP
│       ├── gui.py               # Aplicación gráfica de escritorio (GUI Tkinter)
│       └── cli.py               # Interfaz de línea de comandos (CLI)
├── tests/
│   ├── __init__.py
│   ├── test_system_provider.py  # Tests del proveedor de datos
│   ├── test_inspector_service.py # Tests de la lógica de salud
│   ├── test_file_inspector.py   # Tests del analizador de archivos
│   ├── test_gui.py              # Tests de componentes GUI
│   └── test_cli.py              # Tests de la interfaz CLI
├── pyproject.toml               # Empaquetado y dependencias del proyecto
└── README.md                    # Guía del software
```

---

## 🖥️ Cómo Ejecutar el Software

### 1. Iniciar la Aplicación de Escritorio (GUI Window)
Puedes abrir la ventana interactiva del software ejecutando:

```bash
system-inspector --gui
```
*O alternativamente con Python:*
```bash
python -m system_inspector.gui
```

### 2. Inspeccionar un Archivo desde la CLI
Si prefieres analizar un archivo directamente por consola:
```bash
python -m system_inspector.cli --file pyproject.toml
```

### 3. Ver Resumen del Sistema en Consola
```bash
system-inspector --summary
```

### 4. Salida en formato JSON
```bash
system-inspector --json
```

---

## 🧪 Pruebas Automatizadas y Cobertura

Para verificar la suite de 26 pruebas unitarias y la cobertura de código:

```bash
pytest --cov=src/system_inspector --cov-report=term-missing tests/
```

Para ejecutar el linter de código:
```bash
flake8 src tests --max-line-length=100
```

---

## ⚙️ Cómo subirlo y probarlo en GitHub Actions

1. Inicializar git e ingresar los cambios:
   ```bash
   git init
   git add .
   git commit -m "feat: add desktop gui window and file inspector mvp"
   ```

2. Vincular tu repositorio de GitHub y subirlo:
   ```bash
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   git push -u origin main
   ```

3. Revisa la pestaña **Actions** en tu repositorio de GitHub para ver las pruebas ejecutándose en Windows, Ubuntu y macOS.

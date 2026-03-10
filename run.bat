@echo off
echo === Iniciando Aplicación Flask: Verbos Castellanos ===

REM Crear entorno virtual si no existe
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate

REM Instalar dependencias
pip install -r requirements.txt

REM Crear estructura de carpetas
mkdir static\css 2>nul
mkdir static\js 2>nul
mkdir data 2>nul
mkdir templates 2>nul
mkdir instance 2>nul

REM Inicializar base de datos
python init_db.py

REM Ejecutar aplicación
echo Aplicación iniciada. Abre http://localhost:5000
python app.py

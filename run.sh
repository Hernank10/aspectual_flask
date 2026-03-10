#!/bin/bash

echo "=== Iniciando Aplicación Flask: Verbos Castellanos ==="

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Crear estructura de carpetas
mkdir -p static/css static/js data templates instance

# Inicializar base de datos
echo "Inicializando base de datos..."
python init_db.py

# Ejecutar aplicación
echo "Aplicación iniciada. Abre http://localhost:5000"
python app.py

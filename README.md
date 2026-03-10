# 📚 Aprendizaje de Verbos Castellanos

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)](https://flask.palletsprojects.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Aplicación web interactiva para el aprendizaje de **100 verbos españoles** con sistema de flashcards Leitner y ejercicios de contraste aspectual (infinitivo, gerundio, participio).

![Demo de la aplicación](screenshot.png)
*Captura de pantalla de la aplicación (agrega una imagen real)*

## ✨ Características Principales

### 🎯 **100 Verbos Completos**
- 50 verbos irregulares (tener, hacer, decir, venir, etc.)
- 50 verbos regulares (-ar, -er, -ir)
- Todas las formas: gerundio, participio, presente indicativo, presente subjuntivo, imperfecto subjuntivo
- Ejemplos de uso contextualizados

### 🃏 **Sistema Leitner de Flashcards**
- 5 cajas de repaso espaciado
- Algoritmo de intervalos crecientes (1, 3, 7, 14, 30 días)
- Seguimiento individual de progreso
- Estadísticas detalladas por caja

### 📝 **Ejercicios Interactivos**
- **Contraste aspectual**: infinitivo vs gerundio vs participio
- **Llegara vs Llegase**: contexto histórico y moderno
- **Selección múltiple** con retroalimentación
- **Completar oraciones** con corrección automática
- **Creación de contenido** con ejemplos guía
- **Adaptación contextual** para diferentes registros

### 📊 **Seguimiento de Progreso**
- Estadísticas en tiempo real
- Gráficos de distribución por cajas
- Historial de sesiones de estudio
- Porcentajes de acierto por categoría

### 🌐 **Interfaz Moderna**
- Diseño responsive con Bootstrap 5
- Modo claro/oscuro automático
- Animaciones suaves
- Feedback visual inmediato
- Emojis para mejor experiencia

## 🚀 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.13 | Lenguaje principal |
| Flask | 2.3.2 | Framework web |
| SQLAlchemy | 3.0.5 | ORM para base de datos |
| Bootstrap | 5 | Frontend y diseño |
| JavaScript | ES6 | Interactividad |
| SQLite | 3 | Base de datos |
| Git | - | Control de versiones |

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes)
- Git (opcional)

### Pasos de Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/Hernank10/aspectual_flask.git
cd aspectual_flask

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Inicializar base de datos (100 verbos)
python init_db.py
# Cuando pregunte: ¿Deseas eliminarlos y volver a cargarlos? (s/n): 
# Responde: s

# 6. Ejecutar la aplicación
python app.py --port=5001

Verificación de Instalación
bash
# Verificar que los verbos se cargaron correctamente
python -c "
from app import app
from models import Verb
with app.app_context():
    total = Verb.query.count()
    print(f'✅ Total de verbos: {total}')
    print('✅ Primeros 5 verbos:')
    for v in Verb.query.limit(5).all():
        print(f'   - {v.infinitivo} ({v.categoria})')
"
🎮 Uso de la Aplicación
Abre tu navegador en: http://localhost:5001

Explora las secciones:

Teoría: Explicaciones detalladas sobre contraste aspectual y uso de "llegara/llegase"

Contraste Aspectual: Ejercicios con infinitivo, gerundio y participio

Llegara vs Llegase: Práctica de contexto histórico y moderno

100 Verbos: Ejercicios aleatorios con todos los verbos

Flashcards: Sistema Leitner para repaso espaciado

Recursos: Material adicional y ejemplos

Sistema de Flashcards Leitner
Caja	Intervalo	Descripción
1	1 día	Verbos nuevos o difíciles
2	3 días	En proceso de aprendizaje
3	7 días	Conocimiento intermedio
4	14 días	Casi dominados
5	30 días	Dominados (revisión mensual)
📁 Estructura del Proyecto
text
aspectual_flask/
├── app.py                 # Aplicación principal Flask
├── models.py              # Modelos de base de datos
├── flashcards.py          # Sistema Leitner
├── init_db.py             # Inicializador de BD
├── requirements.txt       # Dependencias
├── README.md              # Este archivo
├── .gitignore             # Archivos ignorados por Git
├── data/
│   ├── ejercicios.json    # 100 ejercicios de contraste aspectual
│   └── verbos_completos.json # 100 verbos con todas sus formas
├── templates/             # Plantillas HTML
│   ├── base.html          # Plantilla base
│   ├── index.html         # Página principal
│   ├── teoria.html        # Teoría lingüística
│   ├── ejercicios.html    # Ejercicios de contraste aspectual
│   ├── llegara_vs_llegase.html # Ejercicios de llegara/llegase
│   ├── verbos_practicar.html # Práctica de 100 verbos
│   ├── flashcards.html    # Sistema de flashcards
│   ├── study_session.html # Sesión de estudio
│   ├── add_flashcard.html # Añadir flashcards
│   └── recursos.html      # Recursos adicionales
├── static/
│   ├── css/
│   │   └── style.css      # Estilos personalizados
│   └── js/
│       └── main.js        # JavaScript personalizado
└── instance/              # Base de datos SQLite
    └── verbos.db          # Base de datos (se crea al iniciar)
📊 Estadísticas del Proyecto
100 verbos totales (50 irregulares + 50 regulares)

20+ formas verbales por verbo

100+ ejercicios interactivos

5 cajas en sistema Leitner

10+ plantillas HTML

1000+ líneas de código Python

500+ líneas de JavaScript

100% responsive

🎯 Ejemplos de Verbos Incluidos
Verbos Irregulares (50)
Infinitivo	Gerundio	Participio	Ejemplo
tener	teniendo	tenido	"Siempre tengo que estudiar"
hacer	haciendo	hecho	"¿Qué haces esta tarde?"
decir	diciendo	dicho	"Siempre dice la verdad"
venir	viniendo	venido	"Vengo a visitarte"
poner	poniendo	puesto	"Pongo la mesa"
Verbos Regulares (50)
Infinitivo	Gerundio	Participio	Ejemplo
hablar	hablando	hablado	"Hablo español"
comer	comiendo	comido	"Como frutas"
vivir	viviendo	vivido	"Vivo en Madrid"
cantar	cantando	cantado	"Canta muy bien"
beber	bebiendo	bebido	"Bebo agua"
🚀 Despliegue en PythonAnywhere
Sube el código a GitHub (ya está hecho)

Crea una cuenta en PythonAnywhere

Abre una consola Bash y clona el repositorio:

bash
git clone https://github.com/Hernank10/aspectual_flask.git
cd aspectual_flask
Crea un entorno virtual:

bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configura la web app desde el dashboard

Configura el archivo WSGI para apuntar a app.py

🤝 Cómo Contribuir
Las contribuciones son bienvenidas. Por favor:

Fork el proyecto

Crea una rama para tu función (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add some AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

Reportar Issues
Si encuentras un error, por favor abre un issue incluyendo:

Descripción del error

Pasos para reproducirlo

Comportamiento esperado

Capturas de pantalla (si aplica)

📄 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

text
MIT License

Copyright (c) 2024 Hernank10

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
👨‍💻 Autor
Hernank10

GitHub: @Hernank10

Proyecto: aspectual_flask

🙏 Agradecimientos
A todos los contribuyentes de Flask y Bootstrap

A la comunidad de PythonAnywhere

A los lingüistas que estudian el contraste aspectual

A los usuarios que prueban y mejoran la aplicación

📞 Contacto Hernank10
Para preguntas o sugerencias:

Abre un issue en GitHub

Contacta vía GitHub

⭐ Si te gusta este proyecto, ¡no olvides darle una estrella en GitHub! ⭐

¡Disfruta aprendiendo verbos castellanos! 🎉

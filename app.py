from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(days=7)

# Cargar datos de ejercicios
def load_exercises():
    try:
        with open('data/ejercicios.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Datos por defecto si no existe el archivo
        return {
            "aspectual": [
                {
                    "id": 1,
                    "type": "multiple_choice",
                    "question": "La escuché ______ en el escenario.",
                    "options": ["cantar", "cantando", "cantado"],
                    "correct": 0,
                    "explanation": "'Cantar' es infinitivo, presenta el evento como totalidad (valor perfectivo)."
                },
                {
                    "id": 2,
                    "type": "multiple_choice",
                    "question": "Los vi ______ por el parque.",
                    "options": ["correr", "corriendo", "corrido"],
                    "correct": 1,
                    "explanation": "'Corriendo' es gerundio, presenta el evento en desarrollo (valor imperfectivo)."
                },
                {
                    "id": 3,
                    "type": "completion",
                    "question": "Encontré la puerta ______ (abrir).",
                    "correct": "abierta",
                    "explanation": "'Abierta' es participio, presenta el evento como culminado (valor perfectivo/perfecto)."
                }
            ],
            "llegara": [
                {
                    "id": 4,
                    "type": "multiple_choice",
                    "question": "En el siglo XV: 'Cuando el rey ______ a la ciudad, todos celebraron.'",
                    "options": ["llegara", "llegase", "llegaría"],
                    "correct": 0,
                    "explanation": "'Llegara' es la forma histórica correcta, con valor de pluscuamperfecto indicativo."
                },
                {
                    "id": 5,
                    "type": "completion",
                    "question": "Si ______ a verlo, dile la verdad (hipótesis).",
                    "correct": "llegaras",
                    "alternatives": ["llegases"],
                    "explanation": "Ambas formas son posibles en contexto de hipótesis: 'llegaras' o 'llegases'."
                },
                {
                    "id": 6,
                    "type": "completion",
                    "question": "Nadie imaginó que ______ a ganar (hecho pasado).",
                    "correct": "llegara",
                    "explanation": "'Llegara' mantiene su valor indicativo residual en este contexto."
                }
            ],
            "creacion": [
                {
                    "id": 7,
                    "type": "creation",
                    "prompt": "Escribe una oración usando 'llegara' en contexto histórico-narrativo",
                    "example": "Cuando el mensajero llegara, se inició la ceremonia"
                },
                {
                    "id": 8,
                    "type": "creation",
                    "prompt": "Crea una frase con 'llegase' en estilo formal literario",
                    "example": "El embajador solicitó que llegase puntualmente a la audiencia"
                }
            ],
            "contexto": [
                {
                    "id": 9,
                    "type": "context",
                    "sentence": "El profesor exigió que el alumno ______ antes del examen",
                    "solution": "llegara/llegase",
                    "explanation": "Ambas formas son posibles en contexto de exigencia"
                },
                {
                    "id": 10,
                    "type": "context",
                    "sentence": "En el medievo, cuando el mensajero ______, se encendían hogueras",
                    "solution": "llegara",
                    "explanation": "Contexto histórico requiere 'llegara' con valor indicativo"
                }
            ]
        }

exercises_data = load_exercises()

# Estadísticas de usuario (en producción usarías una base de datos)
user_stats = {
    'total_attempts': 0,
    'correct_answers': 0,
    'completed_exercises': set()
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teoria')
def teoria():
    return render_template('teoria.html')

@app.route('/ejercicios')
def ejercicios():
    return render_template('ejercicios.html', exercises=exercises_data['aspectual'])

@app.route('/llegara-vs-llegase')
def llegara_vs_llegase():
    return render_template('llegara_vs_llegase.html', exercises=exercises_data['llegara'])

@app.route('/recursos')
def recursos():
    return render_template('recursos.html')

@app.route('/api/check-exercise', methods=['POST'])
def check_exercise():
    data = request.json
    exercise_id = data.get('exercise_id')
    user_answer = data.get('answer', '').strip().lower()
    exercise_type = data.get('exercise_type')
    
    # Buscar el ejercicio
    exercise = None
    for category in exercises_data.values():
        for ex in category:
            if ex['id'] == exercise_id:
                exercise = ex
                break
        if exercise:
            break
    
    if not exercise:
        return jsonify({'error': 'Ejercicio no encontrado'}), 404
    
    # Actualizar estadísticas
    user_stats['total_attempts'] += 1
    
    # Verificar respuesta según tipo
    if exercise_type == 'multiple_choice':
        correct_index = exercise.get('correct')
        is_correct = (int(user_answer) == correct_index)
    elif exercise_type == 'completion':
        correct = exercise.get('correct', '').lower()
        alternatives = [alt.lower() for alt in exercise.get('alternatives', [])]
        is_correct = (user_answer == correct) or (user_answer in alternatives)
    elif exercise_type == 'context':
        solution = exercise.get('solution', '').lower()
        is_correct = (user_answer == solution) or (user_answer in solution.split('/'))
    else:
        is_correct = False
    
    if is_correct:
        user_stats['correct_answers'] += 1
        user_stats['completed_exercises'].add(exercise_id)
    
    return jsonify({
        'correct': is_correct,
        'explanation': exercise.get('explanation', ''),
        'correct_answer': exercise.get('correct', exercise.get('solution', '')),
        'stats': {
            'total': user_stats['total_attempts'],
            'correct': user_stats['correct_answers'],
            'percentage': round((user_stats['correct_answers'] / user_stats['total_attempts']) * 100 if user_stats['total_attempts'] > 0 else 0, 1)
        }
    })

@app.route('/api/save-creation', methods=['POST'])
def save_creation():
    data = request.json
    exercise_id = data.get('exercise_id')
    sentence = data.get('sentence')
    
    # Aquí podrías guardar las creaciones en una base de datos
    # Por ahora solo las devolvemos
    return jsonify({
        'success': True,
        'message': 'Oración guardada correctamente',
        'sentence': sentence
    })

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'total_attempts': user_stats['total_attempts'],
        'correct_answers': user_stats['correct_answers'],
        'percentage': round((user_stats['correct_answers'] / user_stats['total_attempts']) * 100 if user_stats['total_attempts'] > 0 else 0, 1),
        'completed': len(user_stats['completed_exercises'])
    })

if __name__ == '__main__':
    app.run(debug=True)

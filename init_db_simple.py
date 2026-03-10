import json
import os
import sqlite3
from datetime import datetime

def create_database():
    """Crea la base de datos SQLite directamente"""
    
    print("=== Inicializando Base de Datos (versión simplificada) ===\n")
    
    # Conectar a la base de datos (se creará si no existe)
    conn = sqlite3.connect('instance/verbos.db')
    cursor = conn.cursor()
    
    # Crear tabla Verb
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS verb (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            infinitivo VARCHAR(50) NOT NULL,
            gerundio VARCHAR(50),
            participio VARCHAR(50),
            presente_indicativo_1s VARCHAR(50),
            presente_indicativo_2s VARCHAR(50),
            presente_indicativo_3s VARCHAR(50),
            presente_subjuntivo_1s VARCHAR(50),
            imperfecto_subjuntivo_1 VARCHAR(50),
            futuro_subjuntivo VARCHAR(50),
            ejemplo_uso VARCHAR(200),
            categoria VARCHAR(50),
            dificultad INTEGER DEFAULT 1
        )
    ''')
    
    # Crear tabla User
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(80) UNIQUE NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password_hash VARCHAR(200),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Crear tabla Flashcard
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            verb_id INTEGER NOT NULL,
            box INTEGER DEFAULT 1,
            next_review TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            review_count INTEGER DEFAULT 0,
            correct_count INTEGER DEFAULT 0,
            incorrect_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_reviewed TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user (id),
            FOREIGN KEY (verb_id) REFERENCES verb (id)
        )
    ''')
    
    print("✅ Tablas creadas correctamente")
    
    # Verificar si ya hay verbos
    cursor.execute("SELECT COUNT(*) FROM verb")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print(f"⚠️  La base de datos ya contiene {count} verbos")
        respuesta = input("¿Deseas eliminarlos y volver a cargarlos? (s/n): ")
        if respuesta.lower() == 's':
            cursor.execute("DELETE FROM verb")
            cursor.execute("DELETE FROM flashcard")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='verb'")
            conn.commit()
            print("✅ Datos eliminados")
        else:
            print("Manteniendo datos existentes")
            conn.close()
            print(f"\n✅ Base de datos lista con {count} verbos")
            return
    
    # Cargar verbos desde JSON
    json_path = 'data/verbos_completos.json'
    
    if not os.path.exists(json_path):
        print(f"❌ Error: No se encuentra el archivo {json_path}")
        conn.close()
        return
    
    print(f"\nCargando verbos desde {json_path}...")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        contador = 0
        
        # Insertar verbos irregulares
        if 'verbos_irregulares' in data:
            for verb in data['verbos_irregulares']:
                cursor.execute('''
                    INSERT INTO verb (
                        id, infinitivo, gerundio, participio,
                        presente_indicativo_1s, presente_indicativo_2s, presente_indicativo_3s,
                        presente_subjuntivo_1s, imperfecto_subjuntivo_1, futuro_subjuntivo,
                        ejemplo_uso, categoria, dificultad
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    verb['id'], verb['infinitivo'], verb['gerundio'], verb['participio'],
                    verb['presente_indicativo_1s'], verb['presente_indicativo_2s'], verb['presente_indicativo_3s'],
                    verb['presente_subjuntivo_1s'], verb['imperfecto_subjuntivo_1'], verb['futuro_subjuntivo'],
                    verb['ejemplo_uso'], verb['categoria'], verb['dificultad']
                ))
                contador += 1
            print(f"✅ {len(data['verbos_irregulares'])} verbos irregulares cargados")
        
        # Insertar verbos regulares
        if 'verbos_regulares' in data:
            for verb in data['verbos_regulares']:
                cursor.execute('''
                    INSERT INTO verb (
                        id, infinitivo, gerundio, participio,
                        presente_indicativo_1s, presente_indicativo_2s, presente_indicativo_3s,
                        presente_subjuntivo_1s, imperfecto_subjuntivo_1, futuro_subjuntivo,
                        ejemplo_uso, categoria, dificultad
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    verb['id'], verb['infinitivo'], verb['gerundio'], verb['participio'],
                    verb['presente_indicativo_1s'], verb['presente_indicativo_2s'], verb['presente_indicativo_3s'],
                    verb['presente_subjuntivo_1s'], verb['imperfecto_subjuntivo_1'], verb['futuro_subjuntivo'],
                    verb['ejemplo_uso'], verb['categoria'], verb['dificultad']
                ))
                contador += 1
            print(f"✅ {len(data['verbos_regulares'])} verbos regulares cargados")
        
        conn.commit()
        
        print(f"\n🎉 ¡Base de datos inicializada correctamente!")
        print(f"📊 Total de verbos cargados: {contador}")
        print(f"📁 Base de datos guardada en: instance/verbos.db")
        
        # Mostrar algunos ejemplos
        cursor.execute("SELECT infinitivo, categoria FROM verb LIMIT 5")
        verbos = cursor.fetchall()
        print(f"\n📝 Primeros 5 verbos cargados:")
        for v in verbos:
            print(f"   - {v[0]} ({v[1]})")
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al leer el archivo JSON: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        conn.rollback()
    finally:
        conn.close()

def reset_database():
    """Elimina y recrea completamente la base de datos"""
    
    print("\n=== Reiniciando Base de Datos ===\n")
    
    db_path = 'instance/verbos.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Base de datos eliminada: {db_path}")
    else:
        print("⚠️  No existe base de datos previa")
    
    print("\nEjecuta 'python init_db_simple.py' para crear la base de datos nuevamente")

if __name__ == '__main__':
    import sys
    
    # Crear directorio instance si no existe
    os.makedirs('instance', exist_ok=True)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        create_database()
    
    print("\n" + "="*40)
    print("Comandos útiles:")
    print("  python init_db_simple.py          # Inicializar/cargar datos")
    print("  python init_db_simple.py --reset  # Reiniciar base de datos")

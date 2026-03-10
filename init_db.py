from app import app, db
from models import Verb
import json
import os

def init_database():
    """Inicializa la base de datos con los verbos del archivo JSON"""
    
    print("=== Inicializando Base de Datos ===\n")
    
    with app.app_context():
        # Crear todas las tablas
        print("Creando tablas en la base de datos...")
        db.create_all()
        print("✅ Tablas creadas correctamente")
        
        # Verificar si ya hay datos
        if Verb.query.count() > 0:
            print(f"⚠️  La base de datos ya contiene {Verb.query.count()} verbos")
            respuesta = input("¿Deseas eliminarlos y volver a cargarlos? (s/n): ")
            if respuesta.lower() == 's':
                print("Eliminando datos existentes...")
                db.session.query(Verb).delete()
                db.session.commit()
                print("✅ Datos eliminados")
            else:
                print("Manteniendo datos existentes")
                print(f"\n✅ Base de datos lista con {Verb.query.count()} verbos")
                return
        
        # Cargar verbos desde JSON
        json_path = 'data/verbos_completos.json'
        
        if not os.path.exists(json_path):
            print(f"❌ Error: No se encuentra el archivo {json_path}")
            print("Creando archivo de ejemplo...")
            
            # Crear archivo de ejemplo si no existe
            ejemplo_data = {
                "verbos_irregulares": [
                    {
                        "id": 1,
                        "infinitivo": "tener",
                        "gerundio": "teniendo",
                        "participio": "tenido",
                        "presente_indicativo_1s": "tengo",
                        "presente_indicativo_2s": "tienes",
                        "presente_indicativo_3s": "tiene",
                        "presente_subjuntivo_1s": "tenga",
                        "imperfecto_subjuntivo_1": "tuviera/tuviese",
                        "futuro_subjuntivo": "tuviere",
                        "ejemplo_uso": "Siempre tengo que estudiar",
                        "categoria": "irregular",
                        "dificultad": 2
                    }
                ],
                "verbos_regulares": [
                    {
                        "id": 21,
                        "infinitivo": "hablar",
                        "gerundio": "hablando",
                        "participio": "hablado",
                        "presente_indicativo_1s": "hablo",
                        "presente_indicativo_2s": "hablas",
                        "presente_indicativo_3s": "habla",
                        "presente_subjuntivo_1s": "hable",
                        "imperfecto_subjuntivo_1": "hablara/hablase",
                        "futuro_subjuntivo": "hablare",
                        "ejemplo_uso": "Hablo español",
                        "categoria": "regular_ar",
                        "dificultad": 1
                    }
                ]
            }
            
            os.makedirs('data', exist_ok=True)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(ejemplo_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Archivo de ejemplo creado en {json_path}")
        
        print(f"\nCargando verbos desde {json_path}...")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            contador = 0
            
            # Cargar verbos irregulares
            if 'verbos_irregulares' in data:
                for verb_data in data['verbos_irregulares']:
                    verb = Verb(**verb_data)
                    db.session.add(verb)
                    contador += 1
                print(f"✅ {len(data['verbos_irregulares'])} verbos irregulares cargados")
            
            # Cargar verbos regulares
            if 'verbos_regulares' in data:
                for verb_data in data['verbos_regulares']:
                    verb = Verb(**verb_data)
                    db.session.add(verb)
                    contador += 1
                print(f"✅ {len(data['verbos_regulares'])} verbos regulares cargados")
            
            # Guardar todos los cambios
            db.session.commit()
            
            print(f"\n🎉 ¡Base de datos inicializada correctamente!")
            print(f"📊 Total de verbos cargados: {contador}")
            print(f"📁 Base de datos guardada en: instance/")
            
            # Mostrar algunos ejemplos
            print(f"\n📝 Primeros 5 verbos cargados:")
            for verb in Verb.query.limit(5).all():
                print(f"   - {verb.infinitivo} ({verb.categoria})")
            
        except json.JSONDecodeError as e:
            print(f"❌ Error al leer el archivo JSON: {e}")
            print("El archivo no tiene formato JSON válido")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            db.session.rollback()

def reset_database():
    """Elimina y recrea completamente la base de datos"""
    
    print("\n=== Reiniciando Base de Datos ===\n")
    
    with app.app_context():
        print("Eliminando tablas...")
        db.drop_all()
        print("✅ Tablas eliminadas")
        
        print("Creando tablas nuevamente...")
        db.create_all()
        print("✅ Tablas creadas")
        
        print("\nAhora ejecuta 'python init_db.py' para cargar los verbos")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    else:
        init_database()
    
    print("\n" + "="*40)
    print("Comandos útiles:")
    print("  python init_db.py          # Inicializar/cargar datos")
    print("  python init_db.py --reset  # Reiniciar base de datos")

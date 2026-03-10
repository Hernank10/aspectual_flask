from datetime import datetime, timedelta
from models import db, Flashcard, StudySession

class LeitnerSystem:
    """Implementación del sistema Leitner para flashcards"""
    
    # Intervalos en días para cada caja
    BOX_INTERVALS = {
        1: 1,    # Caja 1: revisar cada 1 día
        2: 3,    # Caja 2: revisar cada 3 días
        3: 7,    # Caja 3: revisar cada 7 días
        4: 14,   # Caja 4: revisar cada 14 días
        5: 30    # Caja 5: revisar cada 30 días
    }
    
    @staticmethod
    def calculate_next_review(box):
        """Calcula la próxima fecha de revisión basada en la caja"""
        interval_days = LeitnerSystem.BOX_INTERVALS.get(box, 1)
        return datetime.utcnow() + timedelta(days=interval_days)
    
    @staticmethod
    def process_review(flashcard, correct):
        """Procesa una revisión de flashcard según el sistema Leitner"""
        if correct:
            # Respuesta correcta: subir de caja (máximo 5)
            flashcard.box = min(flashcard.box + 1, 5)
            flashcard.correct_count += 1
        else:
            # Respuesta incorrecta: bajar a caja 1
            flashcard.box = 1
            flashcard.incorrect_count += 1
        
        flashcard.review_count += 1
        flashcard.last_reviewed = datetime.utcnow()
        flashcard.next_review = LeitnerSystem.calculate_next_review(flashcard.box)
        
        db.session.commit()
        return flashcard
    
    @staticmethod
    def get_due_cards(user_id):
        """Obtiene las flashcards que deben ser revisadas hoy"""
        return Flashcard.query.filter(
            Flashcard.user_id == user_id,
            Flashcard.next_review <= datetime.utcnow()
        ).order_by(Flashcard.box).all()
    
    @staticmethod
    def get_stats(user_id):
        """Obtiene estadísticas del sistema de flashcards"""
        cards = Flashcard.query.filter_by(user_id=user_id).all()
        total = len(cards)
        
        if total == 0:
            return {
                'total': 0,
                'by_box': {},
                'mastered': 0,
                'accuracy': 0
            }
        
        by_box = {}
        for box in range(1, 6):
            by_box[box] = len([c for c in cards if c.box == box])
        
        mastered = len([c for c in cards if c.box >= 4])
        
        total_reviews = sum(c.review_count for c in cards)
        total_correct = sum(c.correct_count for c in cards)
        accuracy = (total_correct / total_reviews * 100) if total_reviews > 0 else 0
        
        return {
            'total': total,
            'by_box': by_box,
            'mastered': mastered,
            'accuracy': round(accuracy, 1)
        }

class StudySessionManager:
    @staticmethod
    def start_session(user_id):
        """Inicia una nueva sesión de estudio"""
        session = StudySession(
            user_id=user_id,
            start_time=datetime.utcnow()
        )
        db.session.add(session)
        db.session.commit()
        return session
    
    @staticmethod
    def end_session(session_id):
        """Finaliza una sesión de estudio"""
        session = StudySession.query.get(session_id)
        if session:
            session.end_time = datetime.utcnow()
            db.session.commit()
        return session

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    study_sessions = db.relationship('StudySession', backref='user', lazy=True)
    flashcards = db.relationship('Flashcard', backref='user', lazy=True)
    exercise_results = db.relationship('ExerciseResult', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Verb(db.Model):
    __tablename__ = 'verb'
    
    id = db.Column(db.Integer, primary_key=True)
    infinitivo = db.Column(db.String(50), nullable=False)
    gerundio = db.Column(db.String(50))
    participio = db.Column(db.String(50))
    presente_indicativo_1s = db.Column(db.String(50))
    presente_indicativo_2s = db.Column(db.String(50))
    presente_indicativo_3s = db.Column(db.String(50))
    presente_subjuntivo_1s = db.Column(db.String(50))
    imperfecto_subjuntivo_1 = db.Column(db.String(50))
    futuro_subjuntivo = db.Column(db.String(50))
    ejemplo_uso = db.Column(db.String(200))
    categoria = db.Column(db.String(50))
    dificultad = db.Column(db.Integer, default=1)
    
    # Relaciones
    flashcards = db.relationship('Flashcard', backref='verb', lazy=True)
    exercise_results = db.relationship('ExerciseResult', backref='verb', lazy=True)

    def __repr__(self):
        return f'<Verb {self.infinitivo}>'

class Flashcard(db.Model):
    __tablename__ = 'flashcard'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    verb_id = db.Column(db.Integer, db.ForeignKey('verb.id'), nullable=False)
    box = db.Column(db.Integer, default=1)  # Leitner system box (1-5)
    next_review = db.Column(db.DateTime, default=datetime.utcnow)
    review_count = db.Column(db.Integer, default=0)
    correct_count = db.Column(db.Integer, default=0)
    incorrect_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_reviewed = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Flashcard {self.verb_id} - Box {self.box}>'

class StudySession(db.Model):
    __tablename__ = 'study_session'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    cards_reviewed = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<StudySession {self.id} - {self.start_time}>'

class ExerciseResult(db.Model):
    __tablename__ = 'exercise_result'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    verb_id = db.Column(db.Integer, db.ForeignKey('verb.id'), nullable=False)
    exercise_type = db.Column(db.String(50))  # 'multiple_choice', 'completion', 'context'
    correct = db.Column(db.Boolean)
    answer_time = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent = db.Column(db.Integer)  # in seconds

    def __repr__(self):
        return f'<ExerciseResult {self.id} - {self.correct}>'

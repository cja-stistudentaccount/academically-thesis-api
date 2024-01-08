import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.String, primary_key=True, unique=True)
    account_type = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    primary_learning_pattern = db.Column(db.String, nullable=True)
    secondary_learning_pattern = db.Column(db.String, nullable=True)

class Student(db.Model):
    student_id = db.Column(db.String, primary_key=True, unique=True)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String)
    course = db.Column(db.String)
    summary = db.Column(db.String)

class Course(db.Model):
    course_id = db.Column(db.String, primary_key=True, unique=True)
    course_name = db.Column(db.String, unique=True)
    course_description = db.Column(db.String, unique=True)

class Attempt(db.Model):
    attempt_id = db.Column(db.String, primary_key=True, unique=True)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    score = db.Column(db.Float, nullable=True)

class QuestionAttempt(db.Model):
    question_attempt_id = db.Column(db.String, primary_key=True, unique=True)
    attempt_id = db.Column(db.String, db.ForeignKey('attempt.attempt_id'), nullable=False)
    question_id = db.Column(db.String, db.ForeignKey('question.question_id'), nullable=False)
    selected_choice_id = db.Column(db.String, db.ForeignKey('choice.choice_id'), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=False)

class Question(db.Model):
    question_id = db.Column(db.String, primary_key=True, unique=True)
    question_text = db.Column(db.String, nullable=False)
    course_id = db.Column(db.String, db.ForeignKey('course.course_id'), nullable=False)
    course = db.relationship('Course', backref=db.backref('questions', lazy=True))

class Choice(db.Model):
    choice_id = db.Column(db.String, primary_key=True, unique=True)
    question_id = db.Column(db.String, db.ForeignKey('question.question_id'), nullable=False)
    choice_text = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

class Appointment(db.Model):
    appointment_id = db.Column(db.String, primary_key=True, unique=True)
    tutor_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)
    student_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)
    application_status = db.Column(db.String, nullable=True)
    datetime = db.Column(db.DateTime)
    expiry = db.Column(db.DateTime)
    tutor_feedback = db.Column(db.String, nullable=True)
    is_complete = db.Column(db.Boolean, nullable=False)
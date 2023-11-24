import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.String, primary_key=True, unique=True)
    account_type = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

class Student(db.Model):
    student_id = db.Column(db.String, primary_key=True, unique=True)
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String)
    course = db.Column(db.String)
    summary = db.Column(db.String)

def init_db():
    with db.app.app_context():
        db.init_app(db.app)
        db.create_all()
from flask import Flask
from db import db, Course, Question, Choice
from blueprints import course_bp, unauth_bp, user_bp
from config import Config
from routes import web_bp
import uuid

api = Flask(__name__)
api.config.from_object(Config)

#: register api endpoints
api.register_blueprint(course_bp, url_prefix='/course')
api.register_blueprint(unauth_bp)
api.register_blueprint(user_bp, url_prrefix='/user')

#: register backend components
api.register_blueprint(web_bp)

# Initialize the database
db.init_app(api)

def add_question(course_id, question_text, choices):
    question = Question(
        question_id=str(uuid.uuid4()),
        course_id=course_id,
        question_text=question_text
    )
    db.session.add(question)

    for choice_text, is_correct in choices:
        choice = Choice(
            choice_id=str(uuid.uuid4()),
            question_id=question.question_id,
            choice_text=choice_text,
            is_correct=is_correct
        )
        db.session.add(choice)
    
    #: always remember to commit tapno gumana
    db.session.commit()


with api.app_context():

    #: temporary cleanup, on final run remove this
    db.drop_all()
    db.create_all()

    # Add sample courses
    sample = Course(
        course_id="COMPROG1", 
        course_name='Computer Programming 1', 
        course_description='This course covers the use of general-purpose programming languages to solve problems. The emphasis is to train students to design, implement, test, and debug programs intended to solve computing problems using fundamental programming constructs.'
    )
    db.session.add(sample)
    db.session.commit()

    sample = Course(
        course_id="ADVWEBPROG", 
        course_name='Advanced Web Programming', 
        course_description='This advanced-level program delves into sophisticated concepts and techniques essential for creating dynamic and interactive web applications. Participants will explore advanced topics such as server-side scripting, asynchronous programming, and the integration of APIs.'
    )
    db.session.add(sample)
    db.session.commit()

    # Add multiple questions with choices
    questions_data = [
        {
            'question_text': 'Sample Question 1?',
            'choices': [('Option A', True), ('Option B', False), ('Option C', False), ('Option D', False)]
        },
        {
            'question_text': 'Sample Question 2?',
            'choices': [('Option A', True), ('Option B', False), ('Option C', False), ('Option D', False)]
        },
        # Add more questions as needed
    ]

    for question_data in questions_data:
        add_question("COMPROG1", question_data['question_text'], question_data['choices'])


if __name__ == '__main__':
    api.run(debug=True)

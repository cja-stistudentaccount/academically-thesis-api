from flask import Flask
from db import db, Course, Question, Choice
from blueprints import course_bp, unauth_bp, user_bp, analytics_bp, learning_bp
from flask_migrate import Migrate
from config import Config
from routes import web_bp
import uuid
import secrets

secret_key_file = open('.secret_key', 'wb')
secret_key_file.write(secrets.token_hex(2048).encode())
secret_key_file.close()

api = Flask(__name__)
api.config.from_object(Config)

#: register api endpoints
api.register_blueprint(course_bp, url_prefix='/course')
api.register_blueprint(unauth_bp)
api.register_blueprint(user_bp, url_prefix='/user')
api.register_blueprint(analytics_bp, url_prefix='/analytics')
api.register_blueprint(learning_bp, url_prefix='/learning_assessment')

#: register backend components
api.register_blueprint(web_bp)

# Initialize the database
db.init_app(api)
migrate = Migrate(api, db)

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

    """#: temporary cleanup, on final run remove this
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
            'question_text': 'What are the two types of type casting in Java?',
            'choices': [
                ('widening conversion and narrowing conversion', True),
                ('implicit casting and explicit casting', False),
                ('automatic casting and manual casting', False),
                ('all of the above', False)
            ]
        },
        {
            'question_text': 'Which of the following reserved words is not used in a selection structure?',
            'choices': [
                ('if', False),
                ('else', False),
                ('for', True),
                ('switch', False)
            ]
        },
        {
            'question_text': 'Which of the following is a format specifier for the printf() method?',
            'choices': [
                ('%c', True),
                ('%i', False),
                ('%n', False),
                ('%l', False)
            ]
        },
        {
            'question_text': 'Which of the following is a logical expression?',
            'choices': [
                ('&&', True),
                ('/', False),
                ('x = 6 > 5 && 12!=20', False),
                ('>-', False)
            ]
        },
        {
            'question_text': 'Returns the largest of x and y',
            'choices': [
                ('ceil()', False),
                ('max()', True),
                ('round()', False),
                ('abs()', False)
            ]
        },
        {
            'question_text': 'Which of the following is a low-level language?',
            'choices': [
                ('Java', False),
                ('C++', False),
                ('Machine Language', True),
                ('Python', False)
            ]
        },
        {
            'question_text': 'How many main methods can a Java class have?',
            'choices': [
                ('one', True),
                ('two', False),
                ('three', False),
                ('more than three', False)
            ]
        },
        {
            'question_text': 'This statement terminates the loop or switch and transfers the flow of the program to the statements following it',
            'choices': [
                ('break', True),
                ('continue', False),
                ('goto', False),
                ('default', False)
            ]
        },
        {
            'question_text': 'What is the Java Runtime Environment?',
            'choices': [
                ('A complete set of tools for debugging, developing, and monitoring Java applications', True),
                ('A virtual machine that executes Java bytecode', False),
                ('A collection of related classes that have been grouped together into a folder.', False),
                ('A reserved keyword in Java used to access the classes in a package.', False)
            ]
        },
        {
            'question_text': 'Which of the following is a logical operator?',
            'choices': [
                ('%', False),
                ('&&', True),
                ('<=', False),
                ('*=', False)
            ]
        },
        {
            'question_text': 'Which of the following is a valid example of a named constant declaration and initialization in Java?',
            'choices': [
                ('final int HOURS_PER_DAY = 24;', True),
                ('const int HOURS_PER_DAY = 24;', False),
                ('HOURS_PER_DAY = 24;', False),
                ('int HOURS_PER_DAY = 24;', False)
            ]
        },
        {
            'question_text': 'Which of the following primitive data types is used to store floating point numbers?',
            'choices': [
                ('float', True),
                ('double', True),
                ('both float and double', False),
                ('neither float nor double', False)
            ]
        },
        {
            'question_text': 'Which of the following primitive data types has the smallest range of values?',
            'choices': [
                ('byte', True),
                ('short', False),
                ('int', False),
                ('long', False)
            ]
        },
        {
            'question_text': 'What is the role of an interpreter in programming?',
            'choices': [
                ('translates high-level language to machine language', False),
                ('translates assembly language to machine language', False),
                ('executes one program statement at a time', True),
                ('corrects syntax errors in a program', False)
            ]
        },
        {
            'question_text': 'What is the value of the "c" variable: char c = "String".charAt(3)',
            'choices': [
                ('R', True),
                ('r', False),
                ('I', False),
                ('i', False)
            ]
        },
        # Add more questions as needed
    ]


    for question_data in questions_data:
        add_question("COMPROG1", question_data['question_text'], question_data['choices'])
"""

if __name__ == '__main__':
    api.run(debug=True)

from flask import render_template, request, jsonify
from flask import Blueprint
from db import db, Attempt, QuestionAttempt, Question, Choice, Course
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import unquote
import uuid
import random
from blueprints.auth_wrapper import auth_required
import requests

course_bp = Blueprint('course', __name__)

@course_bp.route('/get_courses', methods=['GET'])
@auth_required
def get_courses(user):
    courses = [
        "21st Century Literature from the Philippines and the World",
        "Advanced",
        "Advanced Web Programming",
        "Application Development and Emerging Technologies",
        "Artificial intelligence",
        "Baking and Pastry Production",
        "Basic Calculus",
        "Computer Programming 1",
        "Computer Systems Architecture",
        "Culinary of Asian Countries",
        "Earth Sciences",
        "Ethics",
        "Game Programming",
        "General biology 1",
        "Information Assurance and Security (Cybersecurity Fundamentals)",
        "Intermediate Web Programming",
        "Komunikasyon at Pananaliksik sa Wika at Kulturang Pilipino",
        "Modeling and Simulation",
        "Sanitation and Hygiene",
        "Software Engineering",
        "The Contemporary World"
    ]

    return jsonify({'courses': courses})

@course_bp.route('/get_course_details/<course_id>', methods=['GET'])
@auth_required
def get_course_details(user, course_id):
    print(course_id, type(course_id))
    description = Course.query.filter_by(course_id=course_id).first()
    if description:
        return jsonify({"course_name": description.course_name, "course_description": description.course_description})
    else:
        return jsonify({"error": "Course not found"}), 404
    
@course_bp.route('/get_questions/<course_id>', methods=['GET'])
#@auth_required
def get_questions(course_id):
    questions = Question.query.filter_by(course_id=course_id).all()
    
    # Create a response object
    response = []

    for question in questions:
        print(question.question_id)
        choices = Choice.query.filter_by(question_id=question.question_id).all()
        choice_list = [(choice.choice_id, choice.choice_text) for choice in choices]
        random.shuffle(choice_list)
        #print(choice_list)
        
        question_data = {
            'question_id': question.question_id,
            'question_text': question.question_text,
            'choices': choice_list
        }
        response.append(question_data)

    return jsonify(response)

@course_bp.route('/submit_knowledge_assessment', methods=['POST'])
@auth_required
def submit_assessment(current_user):
    data = request.get_json()
    score = 0 
    
    user_id = current_user.user_id
    # Create or retrieve the Attempt for the user
    attempt = Attempt(attempt_id=str(uuid.uuid4()), user_id=user_id)
    db.session.add(attempt)

    for question_id in data:
        selected_choice = data[question_id]

        # Retrieve the corresponding Question and Choice
        print(question_id)
        question = Question.query.filter_by(question_id=question_id).first()
        ##print(question)
        #print(question.question_text)
        if not question:
            return jsonify({"error": "Invalid question_id"}), 400

        # Check if the selected answer is correct
        selected_choice = Choice.query.filter_by(question_id=question_id, choice_id=selected_choice).first()
        print(selected_choice.choice_id, selected_choice.is_correct)
        #is_correct = True if selected_choice.is_correct == 'True' else False

        # Create the QuestionAttempt entry
        question_attempt = QuestionAttempt(
            question_attempt_id=str(uuid.uuid4()),
            attempt_id=attempt.attempt_id,
            question_id=question_id,
            selected_choice_id=selected_choice.choice_id if selected_choice else None,
            is_correct=selected_choice.is_correct
        )
        db.session.add(question_attempt)

        # Calculate scores and check eligibility
        total_questions = len(Question.query.filter_by(course_id=question.course_id).all())
        correct_answers = QuestionAttempt.query.filter_by(attempt_id=attempt.attempt_id, is_correct=True).count()
        score = (correct_answers / total_questions) * 100
        attempt.score = score
        # Commit changes to the database
        db.session.commit()

    result_message = 'Passed. Eligible as Tutor' if score >= 80 else 'Failed. Continue as Student'

    return jsonify({
        "message": "Assessment submitted successfully",
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "score": score,
        "result": result_message
    })

@course_bp.route('/submit_knowledge_assessment_test', methods=['POST'])
def submit_test():
    resp = requests.get('http://localhost:5000/course/get_questions/COMPROG1').json()
    answers = {}
    for item in resp:
        print(item['question_id'])
        choice_list = [choice[0] for choice in item['choices']]
        random.shuffle(choice_list)
        answers[item['question_id']] = choice_list[random.randrange(0,4)]

    print(answers) 
    #print(resp.json())

    #resp = requests.post('http://localhost:5000/course/get_questions/COMPROG1', json=answers)
    return jsonify({"error": "Check responses"}), 200
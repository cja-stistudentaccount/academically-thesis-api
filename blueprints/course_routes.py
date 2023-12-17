from flask import render_template, request, jsonify
from flask import Blueprint
from db import db, Attempt, QuestionAttempt, Question, Choice, Course
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import unquote
import uuid
from blueprints.auth_wrapper import auth_required

course_bp = Blueprint('course', __name__)

@course_bp.route('/get_courses', methods=['GET'])
@auth_required
def get_courses():
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
def get_course_details(course_id):
    description = Course.query.filter_by(course_id=course_id).first()
    if description:
        return jsonify({"course_name": description.course_name, "course_description": description.course_description})
    else:
        return jsonify({"error": "Course not found"}), 404
    
@course_bp.route('/get_questions/<course_id>', methods=['GET'])
@auth_required
def get_questions(course_id):
    questions = Question.query.filter_by(course_id=course_id).all()
    
    # Create a response object
    response = []

    for question in questions:

        choices = Choice.query.filter_by(question_id=question.question_id).all()

        question_data = {
            'question_id': question.question_id,
            'question_text': question.question_text,
            'choices': [choice.choice_text for choice in choices]
        }
        response.append(question_data)

    return jsonify(response)

@course_bp.route('/submit_assessment', methods=['POST'])
@auth_required
def submit_assessment(current_user):
    data = request.get_json()

    # Extract data from the request JSON
    question_id = data.get('question_id')
    selected_answer = data.get('selected_answer')

    # Assume user_id is available in your authentication (you may need to modify this part)
    user_id = current_user.user_id

    # Retrieve the corresponding Question and Choice
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"error": "Invalid question_id"}), 400

    # Check if the selected answer is correct
    selected_choice = Choice.query.filter_by(question_id=question_id, choice_text=selected_answer).first()
    is_correct = selected_choice.is_correct if selected_choice else False

    # Create or retrieve the Attempt for the user
    attempt = Attempt.query.filter_by(user_id=user_id).first()
    if not attempt:
        attempt = Attempt(attempt_id=str(uuid.uuid4()), user_id=user_id)
        db.session.add(attempt)

    # Create the QuestionAttempt entry
    question_attempt = QuestionAttempt(
        question_attempt_id=str(uuid.uuid4()),
        attempt_id=attempt.attempt_id,
        question_id=question_id,
        selected_choice_id=selected_choice.choice_id if selected_choice else None,
        is_correct=is_correct
    )
    db.session.add(question_attempt)

    # Commit changes to the database
    db.session.commit()

    # Calculate scores and check eligibility
    total_questions = len(Question.query.filter_by(course_id=question.course_id).all())
    correct_answers = QuestionAttempt.query.filter_by(attempt_id=attempt.attempt_id, is_correct=True).count()
    score = (correct_answers / total_questions) * 100

    result_message = 'Eligible as Tutor' if score >= 80 else 'Continue as Student'

    return jsonify({
        "message": "Assessment submitted successfully",
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "score": score,
        "result": result_message
    })
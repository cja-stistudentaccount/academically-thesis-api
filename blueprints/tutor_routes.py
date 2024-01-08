from flask import render_template, request, jsonify
from flask import Blueprint
from db import db, Attempt, QuestionAttempt, Question, Choice, Course, User, Appointment
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import unquote
import uuid
import random
from blueprints.auth_wrapper import auth_required

# we tried to implement a tensorflow solution, but unfortunately our hardware cannot handle the operations
tutor_bp = Blueprint('tutor_routes', __name__)

@tutor_bp.route('/analyze_student_weakness', methods=['POST'])
@auth_required
def analyze_student_weakness(current_user):
    
    if User.query.filter_by(user_id=current_user.user_id).first().account_type != 'Tutor':
        return 'Forbidden', 403
    
    data = request.json
    student_id = data['student_id']
    student_info = User.query.filter_by(user_id=student_id).first()
    weakness_list = Attempt.query.filter_by(user_id=student_id).all()
    weak_answers = []
    for attempts in weakness_list:
        answers = QuestionAttempt.query.filter_by(attempt_id=attempts.attempt_id).all()
        for ans in answers:
            question = Question.query.filter_by(question_id=ans.question_id).first()
            weak_answers.append((question.question_text, Choice.query.filter_by(question_id=question.question_id, is_correct=True).first().choice_text, Choice.query.filter_by(choice_id=ans.selected_choice_id).first().choice_text))
    weak_answers = list(set(weak_answers))
    return weak_answers, 200

@tutor_bp.route('/get_applicant_list', methods=['GET'])
@auth_required
def get_applicant_list(current_user):
    if User.query.filter_by(user_id=current_user.user_id).first().account_type != 'Tutor':
        return 'Forbidden', 403
    
    appointments = Appointment.query.filter_by(tutor_id=current_user.user_id).all()
    application_list_status = {}

    for appointment in appointments:
        application_list_status[appointment.appointment_id] = {
            'tutor' : appointment.tutor_id,
            'datetime' : appointment.datetime,
            'application_status': appointment.application_status
        }

    return application_list_status, 200

@tutor_bp.route('/update_application', methods=['PUT'])
@auth_required
def update_application(current_user):
    data = request.json
    appointment_id = data['appointment_id']
    status = data['status']

    appointment = Appointment.query.filter_by(appointment_id=appointment_id).first()
    if status in ['Accepted', 'Rejected']:
        appointment.application_status = status
    
    db.session.commit()
    return 'Application status updated', 200

@tutor_bp.route('/finish_tutoring_session', methods=['PUT'])
@auth_required
def finish_tutoring_session(current_user):
    data = request.json
    feedback = data['feedback']
    appointment_id = data['appointment_id']

    appointment = Appointment.query.filter_by(appointment_id=appointment_id).first()
    appointment.is_complete = True
    appointment.tutor_feedback = feedback
    
    db.session.commit()
    return 'Application status updated', 200
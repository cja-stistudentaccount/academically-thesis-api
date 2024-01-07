from flask import render_template, request, jsonify
from flask import Blueprint
from db import db, Attempt, QuestionAttempt, Question, Choice, Course, User, Appointment
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import unquote
import uuid
import random
import datetime
from blueprints.auth_wrapper import auth_required

# we tried to implement a tensorflow solution, but unfortunately our hardware cannot handle the operations
student_bp = Blueprint('student_routes', __name__)

@student_bp.route('/find_tutors', methods=['POST'])
@auth_required
def find_tutors(current_user):

    user = User.query.filter_by(user_id=current_user.user_id).first()
    tutor_list = User.query.filter(User.account_type == 'Tutor').filter((User.primary_learning_pattern == user.primary_learning_pattern) | (User.secondary_learning_pattern == user.secondary_learning_pattern)).all()
    possible_tutors = [tutor.email for tutor in tutor_list]
    return possible_tutors, 200

@student_bp.route('/send_application', methods=['POST'])
@auth_required
def send_application(current_user):

    data = request.json
    tutor = data['tutor']
    month = data['month']
    day = data['day']
    hour = data['hour']
    minute = data['minute']

    user = User.query.filter_by(user_id=current_user.user_id).first()
    tutor_list = User.query.filter(User.account_type == 'Tutor').filter((User.primary_learning_pattern == user.primary_learning_pattern) | (User.secondary_learning_pattern == user.secondary_learning_pattern)).all()
    possible_tutors = [tutor.email for tutor in tutor_list]

    if tutor not in possible_tutors:
        return 'No possible tutor matches your preferred learning style', 404

    new_appointment = Appointment(
        appointment_id = str(uuid.uuid4()),
        tutor_id = User.query.filter_by(email=tutor).first().user_id,
        student_id=user.user_id,
        datetime = datetime.datetime(2024, month, day, hour, minute),
        application_status = 'Pending',
        is_complete = False
    )

    db.session.add(new_appointment)
    db.session.commit()

    return 'Appointment sent. Wait for tutor to review', 200

@student_bp.route('/get_application_status', methods=['GET'])
@auth_required
def get_application_status(current_user):
    
    appointment_list = Appointment.query.filter_by(student_id=current_user.user_id).all()
    application_list_status = {}

    for appointment in appointment_list:
        application_list_status[appointment.appointment_id] = {
            'tutor' : appointment.tutor_id,
            'datetime' : appointment.datetime,
            'application_status': appointment.application_status
        }
    
    return application_list_status, 200

@student_bp.route('/get_tutoring_schedules', methods=['GET'])
@auth_required
def get_tutoring_schedules(current_user):

    appointment_list = Appointment.query.filter(Appointment.student_id == current_user.user_id).filter(Appointment.application_status == 'Accepted').all()
    schedules_list = {}

    for appointment in appointment_list:
        schedules_list[appointment.appointment_id] = {
            'tutor' : appointment.tutor_id,
            'datetime' : appointment.datetime,
            'application_status': appointment.application_status
        }
    
    return schedules_list, 200

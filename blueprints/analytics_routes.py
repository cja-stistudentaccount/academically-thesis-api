from flask import render_template, request, jsonify
from flask import Blueprint
from db import db, Attempt, QuestionAttempt, Question, Choice, Course, User, Student
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import unquote
import uuid
import random
from blueprints.auth_wrapper import auth_required
import requests

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/get_student_leaderboard_score', methods=['GET'])
def get_student_leaderboard_score():
    users = User.query.all()
    leaderboard = {}

    for user in users:

        if user.account_type == 'Tutor':
            continue

        final_score = 0
        
        scores = Attempt.query.filter_by(user_id=user.user_id).all()
        for score in scores:
            final_score += score.score
        print(user.user_id, final_score)

        leaderboard[user.user_id] = final_score
    
    print(leaderboard)
    return jsonify(leaderboard), 200

@analytics_bp.route('/get_student_leaderboard_improvement', methods=['GET'])
def get_student_leaderboard_improvement():
    pass

# todo: no tutor yet
@analytics_bp.route('/get_tutor_leaderboard', methods=['GET'])
def get_tutor_leaderboard():
    users = User.query.all()
    leaderboard = {}

    for user in users:

        if user.account_type == 'Student':
            continue
        
        final_score = 0
        
        scores = Attempt.query.filter_by(user_id=user.user_id).all()
        for score in scores:
            final_score += score.score
        print(user.user_id, final_score)

        leaderboard[user.user_id] = final_score
    
    print(leaderboard)
    return jsonify(leaderboard), 200

@analytics_bp.route('/get_analytics', methods=['GET'])
@auth_required
def get_analytics(current_user):

    rates = []
    latest_attempts = Attempt.query.filter_by(user_id=current_user.user_id).order_by(Attempt.timestamp.desc()).limit(5).all()
    latest_scores = [attempt.score for attempt in latest_attempts]
    for i in range(len(latest_scores) - 1):
        rates.append(latest_scores[i] - latest_scores[i+1])

    average_improvement_rate = sum(rates) / len(rates)
    return str(average_improvement_rate), 200
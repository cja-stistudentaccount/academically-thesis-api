from flask import render_template, request, jsonify
from flask import Blueprint
from db import db, User, Student, Course
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import unquote
import uuid
import jwt
import bcrypt
from blueprints.auth_wrapper import auth_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/get_user_info', methods=['GET'])
@auth_required
def get_user_info(current_user):

    print('hello?')
    print(current_user)
    # Check if the user is a student or tutor
    if current_user.account_type == 'Student':
        # Return student details
        return jsonify({"message": "Student Details", "username": current_user.username, 'user_id' : current_user.user_id})
    elif current_user.account_type == 'Tutor':
        # Return tutor details
        return jsonify({"message": "Tutor Details", "username": current_user.username, 'user_id' : current_user.user_id})
    else:
        # Handle other account types if needed
        return jsonify({"message": "Invalid account type"}), 400

from flask import render_template, request, jsonify
from app import api
from db import db, User, Student, Course
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import unquote
import uuid
import jwt
import bcrypt
from blueprints.auth_wrapper import auth_required

#: web routes
@api.route("/register_user_page", methods=['GET'])
def register_user_page():
    return render_template("register_user.html")

@api.route("/login_page", methods=['GET'])
def login_page():
    return render_template("login_user.html")

##########################################
### Authenticated API Endpoints ##########
##########################################

@api.route('/get_user_info', methods=['GET'])
@auth_required
def get_user_info(current_user):

    print('hello?')
    print(current_user)
    # Check if the user is a student or tutor
    if current_user.account_type == 'Student':
        # Return student details
        return jsonify({"message": "Student Details", "username": current_user.username})
    elif current_user.account_type == 'Tutor':
        # Return tutor details
        return jsonify({"message": "Tutor Details", "username": current_user.username})
    else:
        # Handle other account types if needed
        return jsonify({"message": "Invalid account type"}), 400


    

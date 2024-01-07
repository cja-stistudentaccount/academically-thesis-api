from flask import render_template, request, jsonify
from flask import Blueprint
from db import db, User, Student, Course
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import unquote
import uuid
import jwt
import bcrypt
from config import Config

unauth_bp = Blueprint('unauth', __name__)

@unauth_bp.route("/register_user", methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        print(data)

        whitelisted_emails = ['test@laoag.sti.edu.ph', 'avila@laoag.sti.edu.ph', 'test2@laoag.sti.edu.ph', 'tutor@laoag.sti.edu.ph', 'tutor2@laoag.sti.edu.ph']
        if data['email'] not in whitelisted_emails:
            return jsonify({"error": "Invalid email. Please use your official STI student email if you are currently enrolled."}), 400

        # Check if the username already exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({"error": "Username already exists. Choose a different username."}), 400

        # If username is unique, proceed to create a new user
        new_user = User(
            user_id = str(uuid.uuid4()),
            account_type = data['account_type'],
            username = data['username'],
            email = data['email'],
            password = bcrypt.hashpw(data['password'].encode(), Config.SALT).decode()
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@unauth_bp.route("/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Retrieve user by username from the database
        user = User.query.filter_by(username=data['username']).first()

        # Check if the user exists and the password is correct
        password = data['password']
        print(password, bcrypt.hashpw(data['password'].encode(), Config.SALT).decode())
        print(user.password)
        print(password == user.password)
        print(bcrypt.checkpw(password.encode(), user.password.encode()))
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            # Generate a JWT token
            expiration_time = datetime.utcnow() + timedelta(hours=1)  # Set the token expiration time
            token = jwt.encode({'user_id': user.user_id, 'exp': expiration_time}, Config.SECRET_KEY, algorithm='HS256')

            # Return the token in the response
            return jsonify(access_token=token), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
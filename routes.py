from flask import render_template, request, jsonify
from app import api
from db import db, User, Student
from datetime import datetime, timedelta
import uuid
import jwt
import bcrypt

#: web routes
@api.route("/register_user_page", methods=['GET'])
def register_user_page():
    return render_template("register_user.html")

@api.route("/login_page", methods=['GET'])
def login_page():
    return render_template("login_user.html")

#: api routes
@api.route("/register_user", methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        print(data)

        # Check if the username already exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({"error": "Username already exists. Choose a different username."}), 400

        # If username is unique, proceed to create a new user
        new_user = User(
            user_id = str(uuid.uuid4()),
            account_type = data['account_type'],
            username = data['username'],
            password = bcrypt.hashpw(data['password'].encode(), api.config['SALT']).decode()
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
@api.route("/login", methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Retrieve user by username from the database
        user = User.query.filter_by(username=data['username']).first()

        # Check if the user exists and the password is correct
        password = data['password']
        print(password)
        print(user.password)
        print(password == user.password)
        print(bcrypt.checkpw(password.encode(), user.password.encode()))
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            # Generate a JWT token
            expiration_time = datetime.utcnow() + timedelta(hours=1)  # Set the token expiration time
            token = jwt.encode({'user_id': user.user_id, 'exp': expiration_time}, api.config['SECRET_KEY'], algorithm='HS256')

            # Return the token in the response
            return jsonify(access_token=token), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

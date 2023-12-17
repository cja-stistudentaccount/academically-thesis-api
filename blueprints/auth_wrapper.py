from flask import render_template, request, jsonify
from db import db, User, Student, Course
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import unquote
import uuid
import jwt
import bcrypt

# Authentication decorator
def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        # ensure the jwt-token is passed with the headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            print(token)

        if not token: # throw error if no token provided
            return jsonify({"message": "A valid token is missing!"}), 401
        
        try:
           # decode the token to obtain user public_id
            data = jwt.decode(token, api.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(user_id=data['user_id']).first()
        except:
            print('invalid token')
            return jsonify({"message": "Invalid token!"}), 401
        
         # Return the user information attached to the token
        return f(current_user, *args, **kwargs)
    
    return decorator


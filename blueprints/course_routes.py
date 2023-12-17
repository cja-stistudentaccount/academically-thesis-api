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
def get_course_details(course_id):
    description = Course.query.filter_by(course_id=course_id).first()
    if description:
        return jsonify({"course_name": description.course_name, "course_description": description.course_description})
    else:
        return jsonify({"error": "Course not found"}), 404
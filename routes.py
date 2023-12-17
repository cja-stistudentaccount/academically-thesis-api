from flask import render_template, request, jsonify, Blueprint
from blueprints.auth_wrapper import auth_required

web_bp = Blueprint('web', __name__)

#: web routes
@web_bp.route("/register_user_page", methods=['GET'])
def register_user_page():
    return render_template("register_user.html")

@web_bp.route("/login_page", methods=['GET'])
def login_page():
    return render_template("login_user.html")
    

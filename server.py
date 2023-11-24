from flask import Flask

api = Flask(__name__)

@api.route("/health_check", methods = ['GET'])
def health_check:
    return "Server is up and running"

@api.route("/register_user", methods = ['POST'])
def health_check:
    return "Server is up and running"
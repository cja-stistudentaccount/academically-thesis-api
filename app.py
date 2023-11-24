from flask import Flask
from db import db
import secrets
import bcrypt 

api = Flask(__name__)

api.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api.config['SECRET_KEY'] = secrets.token_hex(2048)
api.config['SALT'] = b'$2b$12$uKi/mA8OhSLT49V1Bqk0Ke'
#print(api.config['SECRET_KEY'])

# Initialize the database
db.init_app(api)
with api.app_context():
    db.create_all()
    
# Import routes after initializing app to avoid circular imports
from routes import register_user_page, register_user

if __name__ == '__main__':
    api.run(debug=True)

import secrets

class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(2048)
    SALT = b'$2b$12$uKi/mA8OhSLT49V1Bqk0Ke'

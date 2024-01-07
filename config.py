class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = open('.secret_key', 'rb').read()
    SALT = b'$2b$12$uKi/mA8OhSLT49V1Bqk0Ke'
    JSON_SORT_KEYS = False

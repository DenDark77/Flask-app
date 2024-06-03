import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key'
    SECURITY_PASSWORD_SALT = 'security_password_salt'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

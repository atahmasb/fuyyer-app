import os


class Config(object):
    SECRET_KEY = os.urandom(32)
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgres://amirtahmasbi@localhost:5432/fuyyerapp'



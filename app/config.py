import os
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    basedir = os.path.abspath(os.path.dirname(__file__))

# Developer config
class DevelopmentConfig(Config):
    #Please set DEBUG to False in production
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.basedir, os.pardir, 'instance', 'application.db')

# Test config
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

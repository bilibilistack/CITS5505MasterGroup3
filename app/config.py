import os
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.pardir, 'instance', 'application.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, os.pardir, 'instance', 'application.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'PerthRegionalWeather' #  Secret key NEED TO BE PUT IN ENV !TODO
'''
Use a class to store configuration variables. It's extensible.
'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    '''
    flask-WTF extension uses the SECRET_KEY to protect against Cross-Site
    Request Forgery (CSRF) attacks
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-string-is-hard-to-guess'
    fallback_db_uri = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # Flask-SQLAlchemy extension uses this config variable to get the location
    # of the application's DB
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or fallback_db_uri
    # signals the application every time a change to the DB is made. Not needed.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
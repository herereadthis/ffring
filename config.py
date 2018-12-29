'''
Use a class to store configuration variables. It's extensible.
'''
import os

class Config(object):
    '''
    flask-WTF extension uses the SECRET_KEY to protect against Cross-Site
    Request Forgery (CSRF) attacks
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-string-is-hard-to-guess'
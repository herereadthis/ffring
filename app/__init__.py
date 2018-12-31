'''
__init__.py file is a package, and defines what symbols the package exposes to
the outside world.
'''
from flask import Flask
# lowercase c is the file, uppercase C is the class name
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# app object is an instance of Flask class
# __name__ configures app
# Flask uses lcoation of the module passed here as a starting point
app = Flask(__name__)
# You could defined configuration here, e.g.,
# app.config['SECRET_KEY'] = 'my-secret-key'
# but it's better to put configuration in a separate file.
# leave this file's concern be creating the app
# this is better: 
app.config.from_object(Config)
# this DB object represents the database.
# This is basically the pattern for initilizing Flask extensions
db = SQLAlchemy(app)
# This object represents the migration engine.
migrate = Migrate(app, db)
# initialize login extension
login = LoginManager(app)
# this is how you do protected pages, e.g. pages that cannot be seen unless
# user is authenticated.
# then, in routes.py, add @login_required decorator
login.login_view = 'login'

# bottom import is a workaround to circular imports, a common problem with Flask
# applications
# the models module defines the structure of the database
from app import routes, models
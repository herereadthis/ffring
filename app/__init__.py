'''
__init__.py file is a package, and defines what symbols the package exposes to
the outside world.
'''
from flask import Flask

# app object is an instance of Flask class
# __name__ configures app
# Flask uses lcoation of the module passed here as a starting point
app = Flask(__name__)
# You could defined configuration here, e.g.,
# app.config['SECRET_KEY'] = 'my-secret-key'
# but it's better to put configuration in a separate file.
# leave this file's concern be creating the app

# bottom import is a workaround to circular imports, a common problem with Flask
# applications
from app import routes
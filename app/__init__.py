'''
__init__.py file is a package, and defines what symbols the package exposes to
the outside world.
'''
from flask import Flask

# app object is an instance of Flask class
# __name__ configures app
# Flask uses lcoation of the module passed here as a starting point
app = Flask(__name__)

# bottom import is a workaround to circular imports, a common problem with Flask
# applications
from app import routes
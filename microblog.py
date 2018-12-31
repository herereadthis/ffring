'''
Define the Flask application instance, at the top-level
The Flask application instance is called app (in the __init__.py file) and is a
member of the app package (the app package is the folder)
'''
from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    '''
    Create the shell context which adds the database instance and models to the
    shell session.
    '''
    return {
        'db': db,
        'User': User,
        'Post': Post
    }
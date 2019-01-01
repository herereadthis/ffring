'''
add a custom error handler using the errorhandler decorator
'''
from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    '''
    Note: this function returns a second value after the template, which is the
    error code number.
    '''
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
from flask import render_template
from app import app

# these are decorators
# whenever the browser requests either of these two routes, flask invokes the 
# next function
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'herereadthis'}
    title = 'Home'
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Washington, DC!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title=title, user=user, posts=posts)
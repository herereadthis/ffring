from flask import render_template, flash, redirect, url_for
from app import app
# import the LoginForm class from forms.py
from app.forms import LoginForm

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


# The methods argument in the route decorator only accepts GET requests by
# default.
@app.route('/login', methods=['GET', 'POST'])
def login():
    # form is new instance of LoginForm class
    form = LoginForm()
    if form.validate_on_submit():
        # flask.flash shows a message to the user
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        # flash.redirect sends user to a different location
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
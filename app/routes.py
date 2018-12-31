from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app import app
# import the LoginForm class from forms.py
from app.forms import LoginForm
# import the User model
from app.models import User

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
    return render_template('index.html', title=title, posts=posts)


# The methods argument in the route decorator only accepts GET requests by
# default.
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current user is already authenticated, and goes to login screen, that
    # will be considered a mistake. Redirect by to homepage.
    # current_user comes from Flash-Login
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # form is new instance of LoginForm class
    form = LoginForm()
    if form.validate_on_submit():
        # query the db to find the user, by username
        # use first() because there's either going to 1 or zero users that match
        user = User.query.filter_by(username=form.username.data).first()
        # error if user does not exist, or password hash does not match
        if user is None or not user.check_password(form.password.data):
            # flask.flash shows a message to the user
            flash('Invalid username or password')
            # flash.redirect sends user to a different location
            return redirect(url_for('login'))
        # login_user() registers the user as logged in. This user is now
        # curent_user
        login_user(user, remember=form.remember_me.data)
        # next_page handles visiting a protected page. You get redirected to
        # login, then after you log in, it takes you back to where you were
        # before, instead of going to index page
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

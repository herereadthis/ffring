from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
# login_required is a decorator which restricts a route to logged-in users
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
# import the LoginForm and Registration form classes from forms.py
from app.forms import LoginForm, RegistrationForm, EditProfileForm
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

'''
<username> represents a dynamic part of the route.
@login_required decorator makes this view restricted to logged-in users
'''
@app.route('/user/<username>')
@login_required
def user(username):
    '''
    first_or_404() method handles <username> that does not exist
    '''
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    # this form checker is different because the GET request pre-populates the
    # form.
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

'''
before_request decorator from Flask tells this function to run right before the
view function. Here is a single place where code can run before any view
'''
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
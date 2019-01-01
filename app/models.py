from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
# import the instances of DB and Login, which are instances of Flask extensions
from app import db, login



class User(UserMixin, db.Model):
    '''
    UserMixin adds these to the user model
    is_authenticated: True if the user has valid credentials, False otherwise.
    is_active: True if the user's account is active, False otherwise.
    is_anonymous: False for regular users, True for a special, anonymous user.
    get_id(): returns a unique identifier for the user as a string.
    '''
    # id is primary key
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # posts is not a field in the Users table. It is a high-level relationship.
    # then you can do user.posts, which grabs all posts by a user, and 
    # author will return user, given a post
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        '''
        Generating the hash will give a different hash every time.
        '''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        '''
        encode the string as bytes because  MD5 support in Python works on bytes
        and not on strings
        Since only this method determines what is an avatar. The template is not
        concerned.
        '''
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user_id is foreign key to id from user model. Notice that it's lowercase.
    # one to many relationship: one user, many posts
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}, {}>'.format(self.body, self.user_id)

@login.user_loader
def load_user(id):
    '''
    Flask-login tracks the logged-in user by storing its unique identifier in
    Flask's user session, which is a storage space assigned to each user who
    uses the application.

    Each time the logged-in user navigates to a new page, Flask-Login retrieves
    the session ID of the use, and then loads that user into memory.
    
    Flask-Login knows nothing about the DB, so the application has to help it.
    This extension expects the app to configure a user-loader function, below:
    '''
    return User.query.get(int(id))
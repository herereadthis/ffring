from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
# import the instances of DB and Login, which are instances of Flask extensions
from app import db, login


'''
Create followers association table, which represents a many-to-many relationship
between different users.
A user has many followers, and a user may follow other users. 
'''
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

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

    '''
    This is a tricky because it's a self-referential relationship.
    Left-side is User (the class)
    '''
    followed = db.relationship(
        # 'User' is right side of relationship
        'User', 
        # secondary configures the association table
        secondary=followers,
        # primaryjoin indicates the condition that links the left side entity 
        # (the follower user) with the association table
        primaryjoin=(followers.c.follower_id == id),
        # secondaryjoin indicates the condition that links the right side entity
        # (the followed user) with the association table
        secondaryjoin=(followers.c.followed_id == id),
        # backref defines how this relationship will be accessed from the right
        # side entity
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


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
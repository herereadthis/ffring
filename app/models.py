from datetime import datetime
from app import db

class User(db.Model):
    # id is primary key
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # posts is not a field in the Users table. It is a high-level relationship.
    # then you can do user.posts, which grabs all posts by a user, and 
    # author will return user, given a post
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user_id is foreign key to id from user model. Notice that it's lowercase.
    # one to many relationship: one user, many posts
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}, {}>'.format(self.body, self.user_id)
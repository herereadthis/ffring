# Ffring!

*Exploring Python Flask*

```bash
# create a virtual environment
# venv is the commmand
# venv is the virtual environment folder
python3 -m venv venv
# activate the virtual environment
# any changes made here will not persist after closing terminal window
source venv/bin/activate
# do this inside the virtual environment
(venv) $ pip install flask
# set the environment variable
# where microblog.py is the top-level module
# This is for DEMO only, don't do it because there's a better way.
(venv) $ export FLASK_APP=microblog.py
# run it
(venv) $ flask run
# create the migration repository
(venv) $ flask db init
# run the first migration
(venv) $ flask db migrate -m "users table"
# apply changes to the DB
(venv) $ flask db upgrade

```

### Packages

```bash
# WARNING: RUN THESE INSIDE THE VIRTUAL ENV!
# DO NOT RUN GLOBALLY!

# Flask is a micro framework for building web applications
pip install flask
# python-dotenv sets environment variables
# environment variables are in .flaskenv
pip install python-dotenv
# flask-wtf is a flask extension that is wrapper for WTForms
# WTForms is a forms framework for python
pip install flask-wtf
# SQLAlchemy is a Python ORM for PostgreSQL, MySQL, and SQLite
# Flask-SQLAlchemy is the extension for Flask
# Object Relational Mapper or ORM allows apps to manage DBs using OOP instead of
# straight SQL
pip install flask-sqlalchemy
# Alembic is a DB migration tool for SQLAlchemy
# Flask-Migrate is the Flask extension for migrations
pip install flask-migrate
# Flask-Login is an extension which handles a user's logged in state.
pip install flask-login
```

### DB migration workflow

```bash
# do everything in virtual env
# after modifying models, generate new migration script
flask db migrate
# apply changes to DB
flask db upgrade
# the new migration script will be part of the new version of application when 
# it is released to the production server, Just run upgrade on prod.
flask db upgrade
# undo the last migration
flask db downgrade
```

### querying the DB

```bash
# start python in virtual env
python 3
# import the DB
>>> from app import db
# import the User and Post model
>>> from app.models import User, Post
# create a new User instance and add to the DB
>>> u = User(username='john', email='john@example.com')
>>> db.session.add(u)
>>> db.session.commit()
# create another User instance and add to the DB
>>> u = User(username='susan', email='susan@example.com')
>>> db.session.add(u)
>>> db.session.commit()
# query the users
>>> users = User.query.all()
# print them out
# you will see ['john', 'susan']
>>> result = [user.username for user in users]
>>> print(result)
# query by ID
>>> user = User.query.get(1)

# add a post by user 1
>>> u = User.query.get(1)
# author is a virtual field created in user model to make foreign keys easier
# you don't have to deal with IDs, just have the user object
>>> p = Post(body='My first post!', author=u)
>>> db.session.add(p)
>>> db.session.commit()
# get all posts written by a user
>>> u = User.query.get(1)
>>> posts = u.posts.all()

# show posts
>>> posts = Post.query.all()
>>> output = [[p.id, p.body, p.author] for p in posts]
>>> print(output)

# get users in reverse alphabetical order
>>> User.query.order_by(User.username.desc()).all()
```

```bash
# delete all users and posts
>>> users = User.query.all()
>>> for u in users:
...     db.session.delete(u)
...
>>> posts = Post.query.all()
>>> for p in posts:
...     db.session.delete(p)
...
>>> db.session.commit()
```

```bash
# there's a better way than having to import a bunch of stuff into the python
# shell. Use this in virtual env
flask shell
```

### Passwords

```bash
# Werkzeug implements password hashing. It's a core dependency of Flask, so it
# is aleady included. do this in python shell:
from werkzeug.security import generate_password_hash
hash = generate_password_hash('foobar')
print(hash)
# notice that every time you hash it, you get different results, so you can't
# determine whether 2 users share the same password if they have the same hash
# verify hash
from werkzeug.security import check_password_hash
check_password_hash(hash, 'foobar')

# set the password
>>> u = User(username='susan', email='susan@example.com')
>>> u.set_password('mypassword')
>>> u.check_password('anotherpassword')
False
>>> u.check_password('mypassword')
True
```

## Debug mode

```bash
# in virtual env
# this allows reloading after any save
export FLASK_DEBUG=1
# turn it off
export FLASK_DEBUG=0
```

```bash
# test email in virtual env in 1 terminal
python -m smtpd -n -c DebuggingServer localhost:8025
# in running terminal
export MAIL_SERVER=localhost
export MAIL_PORT=8025
# then attempt an error
```

## Unit testing

```bash
# do this in the virtual env
python tests.py
```
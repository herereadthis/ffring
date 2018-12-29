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
```
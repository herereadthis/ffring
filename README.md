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
# okay ignore setting the environment variable
(venv) $ pip install python-dotenv
# environment variables are in .flaskenv
```
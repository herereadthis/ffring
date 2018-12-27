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
pip install flask
# set the environment variable
# where microblog.py is the top-level module
export FLASK_APP=microblog.py
```
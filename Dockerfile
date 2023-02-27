# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /python-docker

COPY . .
RUN pip3 install -r requirements.txt


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" "--port=8083"]

# # Install dependencies:
# COPY requirements.txt .
# RUN /opt/venv/bin/pip install -r requirements.txt

# copy app app


# WORKDIR /app
# COPY requirements.txt .
# RUN python -m venv venv
# RUN source venv/bin/activate
# RUN venv/bin/pip install -r requirements.txt
# COPY app app
# CMD ["venv/bin/python", "-m", "app"]
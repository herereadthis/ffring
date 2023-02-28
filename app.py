import json
from flask import Flask, jsonify, render_template
app = Flask(__name__)


@app.route('/')
def hello_geek():
    return render_template('index.html')


@app.route('/users/<username>')
def get_user(username):
    with open('static/users.json') as f:
        users = json.load(f)
        user = users.get(username)
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8083", debug=True)


from flask import Flask

app = Flask(__name__)

# the minimal Flask application
@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

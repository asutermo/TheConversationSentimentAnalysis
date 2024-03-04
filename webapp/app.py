import datetime

from flask import Flask, render_template


app = Flask(__name__)

# the minimal Flask application
@app.route('/')
def index():
    return render_template('index.html', utc_dt=datetime.datetime.utcnow())

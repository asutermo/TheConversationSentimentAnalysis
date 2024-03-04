import datetime

from flask import Flask, render_template

from scripts import basic_sentiment, test

app = Flask(__name__)

# the minimal Flask application
@app.route('/')
def index():
    return render_template('index.html', utc_dt=test.get_datetime(), summaries=basic_sentiment.analyze_rss_feed_titles())

@app.route('/about/')
def about():
    return render_template('about.html')
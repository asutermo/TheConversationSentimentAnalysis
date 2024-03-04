from flask import Flask, render_template

from scripts import basic_sentiment, test

app = Flask(__name__)

# the minimal Flask application
@app.route('/')
async def index():
    summaries = await basic_sentiment.analyze_rss_feed_titles()
    return render_template('index.html', utc_dt=test.get_datetime(), summaries=summaries)

@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
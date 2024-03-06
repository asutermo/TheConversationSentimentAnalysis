from flask import Flask, abort, render_template, request

from scripts import basic_sentiment, test
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    original = getattr(e, "original_exception", None)
    return render_template("500.html"), 500

    # could check original and show unhandled error

@app.route('/')
async def index():
    summaries = await basic_sentiment.analyze_rss_feed_titles()
    return render_template('index.html', utc_dt=test.get_datetime(), summaries=summaries), 200

@app.route('/about/')
def about():
    return render_template('about.html'), 200

@app.route('/article/<title>')
async def article(title: str):
    true_link = request.args.get('link')
    summary = await basic_sentiment.analyze_article(title=title, url=true_link)
    if summary:
        return render_template('article.html', summary=summary), 200
    else:
        app.logger.info('User tried to access %s which didn\'t exist.', true_link)
        abort(404)


if __name__ == '__main__':
    app.run()
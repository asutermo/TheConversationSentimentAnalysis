import json

from flask import Flask, abort, render_template, request

from scripts import basic_sentiment, test
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.route('/')
async def index():
    summaries = await basic_sentiment.analyze_rss_feed_titles()
    return render_template('index.html', utc_dt=test.get_datetime(), summaries=summaries)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/article/<title>')
async def article(title: str):
    true_link = request.args.get('link')
    summary = await basic_sentiment.analyze_article(title=title, url=true_link)
    if summary:
        return render_template('article.html', summary=summary)
    else:
        abort(404)

if __name__ == '__main__':
    app.run()
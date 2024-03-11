from quart import Quart, abort, render_template, request
from quart_schema import QuartSchema

from scripts import basic_sentiment

app = Quart(__name__)
QuartSchema(app)

@app.errorhandler(404)
async def not_found(e):
    """This will 'catch' 404's and show a page not found."""
    return await render_template('404.html'), 404

@app.errorhandler(500)
async def internal_server_error(e):
    """This will 'catch' 500's and show user a 500 page. TODO: more info where it makes sense"""
    original = getattr(e, "original_exception", None)
    return await render_template("500.html"), 500

    # could check original and show unhandled error

@app.route('/')
async def index():
    """Just show article titles, and polarity/subjectivity"""
    summaries = await basic_sentiment.analyze_rss_feed_titles()
    return await render_template('index.html', summaries=summaries), 200

@app.route('/about/')
async def about():
    """Basic about page"""
    return await render_template('about.html'), 200

@app.route('/article/<title>')
async def article(title: str):
    """Take an article, and do a deep dive on the content."""
    true_link = request.args.get('link')
    summary = await basic_sentiment.analyze_article(title=title, url=true_link)
    if summary:
        return await render_template('article.html', summary=summary), 200
    else:
        app.logger.info('User tried to access %s which didn\'t exist.', true_link)
        abort(404)


if __name__ == '__main__':
    app.run()
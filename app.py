from flask import Flask, render_template, request

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

@app.route('/article/<title>')
async def article(title: str):
    true_link = request.args.get('link')
    summary = await basic_sentiment.analyze_article(title=title, url=true_link)
    if summary:
        return render_template('article.html', summary=summary)
    else:
        return render_template('404.html', summary=summary)

if __name__ == '__main__':
    app.run()
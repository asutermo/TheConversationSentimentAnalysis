from dataclasses import dataclass
import requests
from typing import List
import urllib

from bs4 import BeautifulSoup
import feedparser

from quart import Quart, abort, render_template, request
from quart_schema import QuartSchema
from textblob import TextBlob
from transformers import pipeline

app = Quart(__name__)
QuartSchema(app)

@dataclass
class ArticleSentiment:
    title: str
    internal_link: str
    original_link: str
    polarity: float
    subjectivity: float
    text: str = None
    summarization: str = None

    def __str__(self):
        return f"{self.title} - Polarity: {self.polarity}, Subjectivity: {self.subjectivity}"

FEED_URL = 'https://theconversation.com/articles.atom?language=en'
SUMMARIZER = pipeline("summarization", model="facebook/bart-large-cnn")

async def analyze_rss_feed_titles() -> List[ArticleSentiment]:
    """Takes an RSS feed, checks title for subjectivity and polarity and returns a list of ArticleSentiments"""
    feed = feedparser.parse(FEED_URL)
    title_blobs =  [(entry.title, entry.link, TextBlob(entry.title)) for entry in feed.entries]
    return [(ArticleSentiment(title, urllib.parse.quote_plus(title), link, blob.sentiment.polarity, blob.sentiment.subjectivity)) for title, link, blob in title_blobs]

async def analyze_article(title:str, url: str) -> ArticleSentiment:
    """Takes an article from The Conversation, grabs article text, and does both TextBlob and T5 analysis on it"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_body_html = soup.find('div', itemprop='articleBody')

    if article_body_html:
        article_body = article_body_html.get_text(strip=False)
    else:
        return None
    
    blob = TextBlob(article_body)
    summary = summarize_light(article_body)
    return ArticleSentiment(title, url, url, blob.sentiment.polarity, blob.sentiment.subjectivity, article_body, summary)

# Could use transformers.js for heavy lifting, but for now the model is loaded on launch
def summarize_light(article_text: str) -> str:
    """Uses FB Bart Large for text summaries"""
    art_len = len(article_text)
    article_text_trim = article_text[:min(art_len, 1024)]
    results = SUMMARIZER(article_text_trim, max_length=min(art_len, 1024), min_length=30, do_sample=False)
    entry = results[0]
    return entry['summary_text']

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
    summaries = await analyze_rss_feed_titles()
    for summary in summaries:
        summary.internal_link = urllib.parse.quote_plus(summary.internal_link)
        summary.original_link = urllib.parse.quote_plus(summary.original_link)
    return await render_template('index.html', summaries=summaries[1:]), 200

@app.route('/about/')
async def about():
    """Basic about page"""
    return await render_template('about.html'), 200

@app.route('/article/<title>')
async def article(title: str):
    """Take an article, and do a deep dive on the content."""
    true_link = urllib.parse.unquote_plus(request.args.get('link'))
    title = urllib.parse.unquote_plus(urllib.parse.unquote_plus(title))
    summary = await analyze_article(title=title, url=true_link)
    if summary:
        return await render_template('article.html', summary=summary), 200
    else:
        app.logger.info('User tried to access %s which didn\'t exist.', true_link)
        abort(404)


if __name__ == '__main__':
    app.run()
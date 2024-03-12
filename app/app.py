from dataclasses import dataclass, asdict
import requests
from typing import List

from bs4 import BeautifulSoup
import feedparser

from quart import Quart, abort, render_template, request, websocket
from quart_schema import QuartSchema
from textblob import TextBlob
from transformers import pipeline

app = Quart(__name__)
QuartSchema(app)

@dataclass
class ArticleSentiment:
    title: str
    original_link: str
    polarity: float
    subjectivity: float
    text: str = None
    summarization: str = None

@dataclass
class ArticleSummarizationRequest:
    title: str
    url: str

FEED_URL = 'https://theconversation.com/articles.atom?language=en'
SUMMARIZER = pipeline("summarization", model="facebook/bart-large-cnn")

async def analyze_rss_feed_titles() -> List[ArticleSentiment]:
    """Takes an RSS feed, checks title for subjectivity and polarity and returns a list of ArticleSentiments"""
    feed = feedparser.parse(FEED_URL)
    title_blobs =  [(entry.title, entry.link, TextBlob(entry.title)) for entry in feed.entries]
    return [(asdict(ArticleSentiment(title, link, blob.sentiment.polarity, blob.sentiment.subjectivity))) for title, link, blob in title_blobs]

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
    return ArticleSentiment(title, url, blob.sentiment.polarity, blob.sentiment.subjectivity, article_body, summary)

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
    """Just show base index page. /ws/feed is responsible for populating"""
    return await render_template('index.html'), 200

@app.route('/about/')
async def about():
    """Basic about page"""
    return await render_template('about.html'), 200

@app.route('/article/<title>')
async def article(title: str):
    """Take an article, and do a deep dive on the content."""
    return await render_template('article.html'), 200

@app.websocket('/ws/feed')
async def feed():
    summaries = await analyze_rss_feed_titles()
    await websocket.send_json(summaries)

@app.websocket('/ws/summarize')

async def summarize():
    while True:
        data = await websocket.receive_as(ArticleSummarizationRequest)
        summary = await analyze_article(title=data.title, url=data.url)
        await websocket.send_as(summary, ArticleSentiment)

if __name__ == '__main__':
    app.run()
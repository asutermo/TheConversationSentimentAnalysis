from dataclasses import dataclass
from logging.config import dictConfig
from typing import List

import feedparser
import requests
from bs4 import BeautifulSoup
from quart import Quart, render_template, websocket
from quart_schema import QuartSchema
from textblob import TextBlob
from transformers import pipeline

app = Quart(__name__)
QuartSchema(app)


dictConfig(
    {
        "version": 1,
        "loggers": {
            "quart.app": {
                "level": "ERROR",
            },
        },
    }
)


@dataclass
class ArticleSentiment:
    title: str
    original_link: str
    polarity: float
    subjectivity: float
    text: str = ''
    summarization: str = ''


@dataclass
class ArticleSentimentList:
    articles: List[ArticleSentiment] = []


@dataclass
class ArticleSummarizationRequest:
    title: str
    url: str


FEED_URL = "https://theconversation.com/articles.atom?language=en"


SUMMARIZER = pipeline("summarization", model="facebook/bart-large-cnn")


async def analyze_rss_feed_titles() -> ArticleSentimentList:
    """Takes an RSS feed, checks title for subjectivity and polarity and returns a list of ArticleSentiments"""
    feed = feedparser.parse(FEED_URL)
    title_blobs = [
        (entry.title, entry.link, TextBlob(entry.title)) for entry in feed.entries
    ]
    return ArticleSentimentList(
        [
            (
                ArticleSentiment(
                    title=title,
                    original_link=link,
                    polarity=blob.sentiment.polarity,
                    subjectivity=blob.sentiment.subjectivity,
                )
            )
            for title, link, blob in title_blobs
        ]
    )


async def analyze_article(title: str, url: str) -> ArticleSentiment:
    """Takes an article from The Conversation, grabs article text, and does both TextBlob and T5 analysis on it"""
    response = requests.get(url)
    if response.status_code == 403:
        app.logger.error("Unable to access content.")
        raise Exception("Unable to access content.")
    soup = BeautifulSoup(response.text, "html.parser")
    article_body_html = soup.find("div", itemprop="articleBody")
    if article_body_html:
        article_body = article_body_html.get_text(strip=False)
    else:
        app.logger.error("No article body found.")
        raise Exception("No article body found.")

    blob = TextBlob(article_body)
    summary = summarize_light(article_body)
    return ArticleSentiment(
        title=title,
        original_link=url,
        polarity=blob.sentiment.polarity,
        subjectivity=blob.sentiment.subjectivity,
        text=article_body,
        summarization=summary,
    )


# Could use transformers.js for heavy lifting, but for now the model is loaded on launch
def summarize_light(article_text: str) -> str:
    """Uses FB Bart Large for text summaries"""
    art_len = len(article_text)
    article_text_trim = article_text[: min(art_len, 1024)]
    results = SUMMARIZER(
        article_text_trim, max_length=min(art_len, 1024), min_length=30, do_sample=False
    )
    entry = results[0]
    return entry["summary_text"]


@app.errorhandler(404)
async def not_found(e):
    """This will 'catch' 404's and show a page not found."""
    return await render_template("404.html"), 404


@app.errorhandler(500)
async def internal_server_error(e):
    """This will 'catch' 500's and show user a 500 page. TODO: more info where it makes sense"""
    app.logger.error(e)
    _ = getattr(e, "original_exception", None)
    return await render_template("500.html"), 500

    # could check original and show unhandled error


@app.route("/")
async def index():
    """Just show base index page. /ws/feed is responsible for populating"""
    return await render_template("index.html"), 200


@app.route("/about/")
async def about():
    """Basic about page"""
    return await render_template("about.html"), 200


@app.route("/article/<title>")
async def article(title: str):
    """Take an article, and do a deep dive on the content."""
    return await render_template("article.html"), 200


@app.websocket("/ws/feed")
async def feed() -> None:
    summaries = await analyze_rss_feed_titles()
    await websocket.send_as(summaries, ArticleSentimentList)


@app.websocket("/ws/summarize")
async def summarize() -> None:
    while True:
        data = await websocket.receive_as(ArticleSummarizationRequest)
        summary = await analyze_article(title=data.title, url=data.url)
        await websocket.send_as(summary, ArticleSentiment)


async def test_coverage():
    pass


if __name__ == "__main__":
    app.run()

import requests
from typing import List

from bs4 import BeautifulSoup
import feedparser
from textblob import TextBlob

from . import ArticleSentiment
from .summarize import summarize

# Set feed url, parse it, then check polarity and subjectivity of each article's title
FEED_URL = 'https://theconversation.com/articles.atom?language=en'

async def analyze_rss_feed_titles() -> List[ArticleSentiment]:
    """Takes an RSS feed, checks title for subjectivity and polarity and returns a list of ArticleSentiments"""
    feed = feedparser.parse(FEED_URL)
    title_blobs =  [(entry.title, entry.link, TextBlob(entry.title)) for entry in feed.entries]
    return [(ArticleSentiment(title, link, blob.sentiment.polarity, blob.sentiment.subjectivity)) for title, link, blob in title_blobs]

   
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
    summary = summarize(article_body)
    return ArticleSentiment(title, url, blob.sentiment.polarity, blob.sentiment.subjectivity, article_body, summary)
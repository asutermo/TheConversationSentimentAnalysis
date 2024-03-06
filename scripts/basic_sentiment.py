import requests
from typing import List

from bs4 import BeautifulSoup
import feedparser
from textblob import TextBlob

from . import TextBlobArticleSentiment

# Set feed url, parse it, then check polarity and subjectivity of each article's title
FEED_URL = 'https://theconversation.com/articles.atom?language=en'

async def analyze_rss_feed_titles() -> List[TextBlobArticleSentiment]:
    feed = feedparser.parse(FEED_URL)
    title_blobs =  [(entry.title, entry.link, TextBlob(entry.title)) for entry in feed.entries]
    return [(TextBlobArticleSentiment(title, link, blob.sentiment.polarity, blob.sentiment.subjectivity, None)) for title, link, blob in title_blobs]

   
async def analyze_article(title:str, url: str) -> TextBlobArticleSentiment:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_body_html = soup.find('div', itemprop='articleBody')
    
    if article_body_html:
        article_body = article_body_html.get_text(strip=False)
    else:
        print("The specified div was not found.")
        return None
    
    blob = TextBlob(article_body)
    return TextBlobArticleSentiment(title, url, blob.sentiment.polarity, blob.sentiment.subjectivity, article_body)
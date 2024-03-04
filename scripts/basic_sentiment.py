import feedparser
from typing import List

from textblob import TextBlob

from . import TextBlobArticleSentiment

# Set feed url, parse it, then check polarity and subjectivity of each article's title
FEED_URL = 'https://theconversation.com/articles.atom?language=en'

def analyze_rss_feed_titles() -> List[str]:
    feed = feedparser.parse(FEED_URL)
    title_blobs =  [(entry.title, TextBlob(entry.title)) for entry in feed.entries]
    return [str(TextBlobArticleSentiment(title, blob.sentiment.polarity, blob.sentiment.subjectivity)) for title, blob in title_blobs]

   

import feedparser
from textblob import TextBlob

# Set feed url, parse it, then check polarity and subjectivity of each article's title
FEED_URL = 'https://theconversation.com/articles.atom?language=en'
feed = feedparser.parse(FEED_URL)

for entry in feed.entries:
    print(entry)
    print(f"Title: {entry.title}")
    analysis = TextBlob(entry.title)
    print(f"Polarity: {analysis.sentiment.polarity}, Subjectivity: {analysis.sentiment.subjectivity}")
    print('-' * 40)
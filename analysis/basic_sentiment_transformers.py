import feedparser
from transformers import pipeline

# Set feed url, parse it
FEED_URL = 'https://theconversation.com/articles.atom?language=en'
feed = feedparser.parse(FEED_URL)

data = [entry.title for entry in feed.entries]
specific_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
specific_model(data)
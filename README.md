# TheConversationSentimentAnalysis

This is just a sample project built around Quart to do summarization and sentiment analysis of news articles from [The Conversation](https://theconversation.com/us/feeds). The Conversation uses a Creative Commons NoDerivatives license. Please note, that this site will not be officially hosted as summarization may fall under a 'remix' or 'transform' of the original material.

## Flask / Quart

Quart is an async reimplementation of Flask. This is useful, especially for things like inference which may take some time.

## Running

To run locally:

```sh
cd app
hypercorn --reload --bind 0.0.0.0:5000 --workers 1 app:app
```

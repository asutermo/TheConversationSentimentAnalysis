# TheConversationSentimentAnalysis
Sentiment Analysis on TheConversation. Very, very early in-progress

## RSS Feed

[The Conversation](https://theconversation.com/us/feeds)

## Flask / Quart

Quart is an async reimplementation of Flask. This is useful, especially for things like inference which may take some time.

## Running

To run locally:

```sh
cd app
hypercorn --reload --bind 0.0.0.0:5000 --workers 1 app:app
```

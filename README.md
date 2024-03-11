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
hypercorn --reload --bind 0.0.0.0:8000 --workers 1 app:app
```

http://localhost:8000/article/As%20the%20air-raid%20sirens%20sound,%20I%20am%20studying%20Ukrainian%20culture%20with%20new%20fervour.%20I%E2%80%99m%20far%20from%20alone?link=https://theconversation.com/as-the-air-raid-sirens-sound-i-am-studying-ukrainian-culture-with-new-fervour-im-far-from-alone-224508
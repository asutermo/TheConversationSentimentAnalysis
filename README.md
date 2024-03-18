# TheConversationSentimentAnalysis

This is just a sample project built around Quart to do summarization and sentiment analysis of news articles from [The Conversation](https://theconversation.com/us/feeds). The Conversation uses a Creative Commons NoDerivatives license. Please note, that this site will not be officially hosted as summarization may fall under a 'remix' or 'transform' of the original material.

## Technologies Used

I chose to use Quart for this. Quart is an async reimplementation of Flask. This is useful, especially for things like inference which may take some time.

I also utilize websockets to handle sending of information.

## Running

To run locally:

```sh
cd app
hypercorn --reload --bind 0.0.0.0:5000 --workers 1 app:app
```

## Tests and Formatting

I utilize tox for formatting and cleanliness. To run, go to the root of the repo and run 'tox' to run the tests/formatting.

## TODO:

- Add an example of CI/CD
- Improved tests and code coverage
- Have all tox formatting stuff pass

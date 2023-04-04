import re
from textblob import TextBlob
import snscrape.modules.twitter as sntwitter

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) # type: ignore

def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0.3: # type: ignore
        return 'positive'
    elif analysis.sentiment.polarity == 0: # type: ignore
        return 'neutral'
    else:
        return 'negative'
    
def bot(content, depth = 1000):
    scraper = sntwitter.TwitterSearchScraper(content)
    pos = 0
    neg = 0
    for i, tweet in enumerate(scraper.get_items()):
        if i>depth:
            break
        if get_tweet_sentiment(tweet.rawContent) == 'positive': # type: ignore
            pos += 1
        if get_tweet_sentiment(tweet.rawContent) == 'negative': # type: ignore
            neg += 1
    if pos >= neg:
        answer = 'The web has a positive opinion on the topic'
    else:
        answer = 'The web has a negative opinion on the topic'
    return answer


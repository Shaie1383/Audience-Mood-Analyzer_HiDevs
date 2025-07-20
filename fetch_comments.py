# fetch_comments.py
import tweepy

def get_twitter_comments(api_key, api_secret, bearer_token, keyword="#AI", max_results=20):
    client = tweepy.Client(bearer_token=bearer_token)
    response = client.search_recent_tweets(query=keyword, max_results=max_results)

    comments = []
    for tweet in response.data:
        comments.append(tweet.text)
    return comments

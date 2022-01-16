# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 12:49:31 2022

@author: mmaso

TODO:
    Scale username up. Test list of usernames.
    Where is this all going? DB? Email?
    What does it mean to be ratioed? Enough likes to be relevant, but lower than usual? Compare to average?
"""

import tweepy
import requests
from config import api_key, api_secret_key, bearer_token

# API v2 Client
client = tweepy.Client(bearer_token, api_key, api_secret_key, return_type= requests.Response)

username = 'WillyMacShow' # This will be a list, potential user input?

# API request for User Lookup
user = client.get_user(username = username).json()

# Twitter ID
user_id = user['data']['id']

print(f"{username}'s user ID is {user_id}\n")

# API request for Tweets using Twitter ID
user_tweets = client.get_users_tweets(user_id, expansions = ['author_id', 'referenced_tweets.id'], max_results = 5).json()

#print(user_tweets_list)

print(f"{username} has made the following Tweets:\n")

for tweet in user_tweets['data']:
    # print(f"Author ID: {tweet['author_id']}")
    
    # API request for Tweet Likes
    tweet_likes = client.get_liking_users(tweet['id']).json() #Tweet ID
    
    # API request for Tweet Retweets
    tweet_rt = client.get_retweeters(tweet['id']).json() #Tweet ID
    
    # Tweet ID
    print(f"Tweet ID: {tweet['id']}")
    
    # Tweet Type (Retweet, quoted, or replied_to, original tweet) ### Update Retweet based on real output
    try:
        print(f"{tweet['referenced_tweets'][0]['type']}: {tweet['referenced_tweets'][0]['id']}") # 'referenced_tweets' key does not appear for original tweets
    except:
        print('original tweet') # Not sure about the naming convention here
    
    # Tweet text
    print(f"{tweet['text']}")
    
    # Tweet Like and Retweet Counts
    print(f"Likes: {len(tweet_likes['data'])}     Retweets: {tweet_rt['meta']['result_count']}\n")
    
    # Retweeter usernames and Twitter IDs (where applicable)
    try:
        print(f"Retweeted by:\n{tweet_rt['data'][0]['username']}: {tweet_rt['data'][0]['id']}\n") # 'data' key does not appear in dicts w/o rts
    except:
        pass
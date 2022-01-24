# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 12:49:31 2022

@author: mmaso

TODO:
    Scale username up. Test list of usernames.
    Inconsistencies between Twiiter app and API results, i.e. likes not matching for tweets
    Where is this all going? DB? Email?
    What does it mean to be ratioed? Enough likes to be relevant, but lower than usual? Compare to average?
"""

import tweepy
import requests
import datetime as dt
from config import api_key, api_secret_key, bearer_token

username = 'WillyMacShow' # This will be a list, potential user input?

# API v2 Client
client = tweepy.Client(bearer_token, api_key, api_secret_key, return_type= requests.Response)

# API request for User Lookup
user = client.get_user(username = username).json()

# Twitter ID
user_id = user['data']['id']

print(f"{username}'s user ID is {user_id}\n")

# Year-to-Date    
ytd_time = dt.datetime.now() - dt.timedelta(days = 1) # Time variable

# Adjusts YTD to rfc3339 format
str_year3339 = (ytd_time.isoformat())
ymd_str_year3339 = str_year3339.split('T')
adj_3339 = ymd_str_year3339[0] + 'T00:00:00Z'

# API request for Tweets using Twitter ID
user_tweets = client.get_users_tweets(user_id, expansions = ['author_id', 'referenced_tweets.id'], start_time = adj_3339, tweet_fields = ['created_at']).json()
# print(user_tweets) # use this to navigate request structure when adding new fields

print(f"{username} has made the following Tweets:\n")

tweet_likes = []
tweet_retweets = []

for tweet in user_tweets['data']:
    # print(f"Author ID: {tweet['author_id']}")
    
    # API request for Tweet Likes
    tweet_likes_user = client.get_liking_users(tweet['id']).json() #Tweet ID
    
    # API request for Tweet Retweets
    tweet_rt_user = client.get_retweeters(tweet['id']).json() #Tweet ID
    
    # Tweet ID
    print(f"Tweet ID: {tweet['id']}")
    
    # Tweet Timestamp
    print(f"Created at {tweet['created_at']}")
    
    # Tweet Type (retweeted, quoted, or replied_to, original tweet)
    try:
        ref_tweet_id = str(tweet['referenced_tweets'][0]['id'])
        user = client.get_tweet(id = ref_tweet_id, expansions = ['author_id']).json()
        print(f"{tweet['referenced_tweets'][0]['type']}: {user['includes']['users'][0]['username']}") # 'referenced_tweets' key does not appear for original tweets
    except:
        print('original tweet') # Not sure about the naming convention here
    
    # Tweet text
    print(f"{tweet['text']}")
    
    # Tweet Like and Retweet Counts
    likes = tweet_likes_user['meta']['result_count']
    retweet = tweet_rt_user['meta']['result_count']
    
    tweet_likes.append(likes)
    tweet_retweets.append(retweet)
    print(f"Likes: {likes}     Retweets: {retweet}\n")
    
    # Retweeter usernames and Twitter IDs (where applicable)
    try:
        print(f"Retweeted by:\n{tweet_rt_user['data'][0]['username']}: {tweet_rt_user['data'][0]['id']}\n") # 'data' key does not appear in dicts w/o rts
    except:
        pass

# Descriptive stats on selected Tweets
print(f"Total Tweets returned: {len(user_tweets['data'])}")
print(f"Total Likes: {sum(tweet_likes)}      Likes/Tweet: {sum(tweet_likes)/len(user_tweets['data'])}")
print(f"Total Retweets: {sum(tweet_retweets)}     Retweets/Tweet: {sum(tweet_retweets)/len(user_tweets['data'])}")
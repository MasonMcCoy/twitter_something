# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 12:49:31 2022

@author: mmaso
"""


import tweepy
import requests
from config import api_key, api_secret_key, bearer_token

client = tweepy.Client(bearer_token, api_key, api_secret_key, return_type= requests.Response)

username = 'WillyMacShow'

user = client.get_user(username = username)
user_json = user.json()

user_id = user_json['data']['id']

print(f"{username}'s user ID is {user_id}\n")

user_tweets = client.get_users_tweets(user_id, expansions = ['author_id', 'referenced_tweets.id'], max_results = 5)
user_tweets_json = user_tweets.json()

user_tweets_list = user_tweets_json['data']
#print(user_tweets_list)

print(f"{username} has made the following Tweets:\n")

for tweet in user_tweets_list:
    # print(f"Author ID: {tweet['author_id']}")
    print(f"Tweet ID: {tweet['id']}")
    
    try:
        print(f"{tweet['referenced_tweets'][0]['type']}: {tweet['referenced_tweets'][0]['id']}")
    except:
        print('tweet') # Not sure about the naming convention here
    
    print(f"{tweet['text']}\n")
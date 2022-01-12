# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 12:49:31 2022

@author: mmaso
"""

import tweepy
from config import api_key, api_secret_key, bearer_token

# print(api_key)


# auth = tweepy.OAuthHandler(bearer_token, api_key, api_secret_key)
client = tweepy.Client(bearer_token, api_key, api_secret_key)

username = 'WillyMacShow'
user = client.get_user(username = username)

print(user)

# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 12:49:31 2022

@author: mmaso

TODO:
    Pagination for replies? get_recent_tweets
    Scale username up. Test list of usernames.
    Inconsistencies between Twiiter app and API results, i.e. likes not matching for tweets
    Where is this all going? DB? Email?
    What does it mean to be ratioed? Enough likes to be relevant, but lower than usual? Compare to average?
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 11:46:42 2022

@author: mmaso
"""

import tweepy
import requests
import datetime as dt
from config import api_key, api_secret_key, bearer_token

# Username(s) to be input into API request(s)
#username = 'WillyMacShow' # Potential user input?

# API v2 Client
client = tweepy.Client(bearer_token, api_key, api_secret_key, return_type= requests.Response)

# One Day    
day_1 = dt.datetime.now() - dt.timedelta(days = 1) # Time variable

def time_to_rfc3339(time_variable):
    # Adjusts input time to rfc3339 format for API request
    str_year3339 = time_variable.isoformat().split('T')
    
    return str_year3339[0] + 'T00:00:00Z'


def rfc3339_to_date(rfc3339_variable):
    # Splits returned 'created_at' field into date and time, converts to readable date
    date, time = rfc3339_variable.split('T')
    
    return date

def rfc3339_to_time(rfc3339_variable):
    # Splits returned 'created_at' field into date and time, converts to readable time
    date, time = rfc3339_variable.split('T')
    time, zone = time.split('.')
    
    return time


class TwitterUser:
    def __init__(self, username):
        self.username = username
        self.tweets = []
        
    def getUserID(self):
        user = client.get_user(username = self.username).json()
        user_id = user['data']['id']
        
        return user_id
    
    def getTweets(self, pagination = False, token = ''):
        
        if pagination is True:
            twitter_response = client.get_users_tweets(self.getUserID(), expansions = ['referenced_tweets.id'], pagination_token = token, start_time = time_to_rfc3339(day_1), tweet_fields = ['created_at']).json()
        
        else:
            twitter_response = client.get_users_tweets(self.getUserID(), expansions = ['referenced_tweets.id'], start_time = time_to_rfc3339(day_1), tweet_fields = ['created_at']).json()
        
        for tweet in twitter_response['data']:
            self.tweets.append(tweet)
        
        if 'next_token' in twitter_response['meta']:
            '''YOU NEED TO PAGINATE'''
                
            token = twitter_response['meta']['next_token']
            self.getTweets(pagination = True, token = token)
                
        else:
            '''NO PAGINATION/PAGINATION COMPLETE'''
            for tweet in self.tweets:
                tweet_likes = client.get_liking_users(tweet['id']).json()
                tweet_rt = client.get_retweeters(tweet['id']).json()
                tweet_replies = client.search_recent_tweets(f"conversation_id:{tweet['id']}").json()
                
                tweet['likes'] = tweet_likes['meta']['result_count']
                tweet['retweets'] = tweet_rt['meta']['result_count']
                tweet['replies'] = tweet_replies['meta']['result_count']
    
    def formatTweets(self):
        for tweet in self.tweets:
            print(f"Tweet ID: {tweet['id']}")
            print(f"{rfc3339_to_date(tweet['created_at'])} at {rfc3339_to_time(tweet['created_at'])} GMT")
            
            try:
                print(f"{tweet['referenced_tweets'][0]['type']} Twitter ID: {tweet['referenced_tweets'][0]['id']}")
            except:
                print('original tweet')
            
            print(tweet['text'], '\n')
            print(f"Replies: {tweet['replies']}          Retweets: {tweet['retweets']}          Likes: {tweet['likes']}\n")
        
        print(f"Total Tweets Requested: {len(self.tweets)}")
        
    def getDrama(self):
        """
        look at replies, find likes, compare reply likes to tweet likes
        """
        for tweet in self.tweets:
            replies = client.search_recent_tweets(f"conversation_id:{tweet['id']}").json()
            
            print(tweet['text'])
            
            try:
                for reply in replies['data']:
                    print(f"# {reply['text']}")
            except:
                print("No replies :(")
                
            print('\n')

    
    def __repr__(self):
        return f"{self.username}'s Twitter ID is {self.getUserID()}\n\nThey have made the following Tweets in the past 24 hours:\n{self.tweets}"
    
wms = TwitterUser('WillyMacShow')

#print(wms.getUserID())
#print(wms.getTweets())
#print(wms)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 17:58:31 2018

@author: xiuye
"""

import tweepy 
from tweepy import OAuthHandler
import re
import pickle
  
# load sensitive info
from dotenv import load_dotenv
import os
load_dotenv()
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_secret = os.getenv('TWITTER_ACCESS_SECRET')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)


# Empty Array 
itemlist=[]  

# search for keyword
keyword = "😍" # "😋"
numberOfTweets = 5000
n = 0;
for tweet in tweepy.Cursor(api.search, keyword, lang="en").items(numberOfTweets):
    dc = tweet._json
    str = dc.get('text')
    #list_all = re.split('( )', str) # this is a list
    #list_a = re.findall(r'[@]\S*', str) #[2,4,7]
    #list_b = [1,2,3,4,5,6]
    #list_a = [n for n in list_a if n not in list_b]

    # remove the following
    #print(re.findall(r'[@]\S*', str)) # Twitter user names
    #print(re.findall(r'[RT]\S*', str)) # "RT"
    
    itemlist.append(str) 
    n = n+1
    print(n)


with open('outfile', 'wb') as fp:
    pickle.dump(itemlist, fp)

 
  
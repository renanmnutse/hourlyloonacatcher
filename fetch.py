# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 00:09:57 2021

@author: Renan
"""
import tweepy
import urllib.request
import pandas as pd
# Authenticate to Twitter
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)



deukae = {
  "jiu": "hourlyjiu",
  "sua": "suahours",
  "siyeon": "siyeonhours",
  "handong": "hourlydong",
  "yoohyeon": "hourlyoohyoen",
  "dami": "hourly_dami",
  "gahyeon": "hourlygahyeon"
}

loona = {
  'heejin': 'hourlyheejin', 
  'hyunjin': 'hourlyaeong', 
  'haseul': 'seulhour', 
  'yeojin': 'hourlyyeojin', 
  'vivi': 'vivihourly', 
  'kimlip': 'kimliphourly', 
  'jinsoul': 'hourlyjinsoul', 
  'choerry': 'hourlychoerry', 
  'yves': 'yveshourly', 
  'chuu': 'chuuhour', 
  'gowon': 'hourlywon',
  'oliviahye': 'hourlyolivia'
}

count = pd.Series()
# Create a tweet

#api.update_status("k")
api.me()
tweets = api.home_timeline(include_entities='true')
#public_tweets = api.user_timeline('hyejoohour', count = 5000, include_rts = 'false', exclude_replies = 'true')
def fetch(dict, folder):    
  for key,value in dict.items():
    public_tweets = api.user_timeline(value, count = 10000, include_rts = 'false', exclude_replies = 'true')
    url = []
    for tweet in public_tweets:
      #url.append(tweet.entities["media"][0]['media_url_https'])
      if "media" in tweet.entities:
          if "thumb" in tweet.entities["media"][0]['media_url_https']:         
              url.append(tweet.entities["media"][0]['media_url_https'])
    i=1
    for image in url:
      name = "images" + "/" + folder + "/" + key + str(i)+".jpg"
      urllib.request.urlretrieve(image, name)
      count[key] = i
      i+=1

fetch(deukae, 'deukae')
fetch(loona, 'loona')
#urllib.request.urlretrieve("https://pbs.twimg.com/media/EqxwHtBXcAUE_7B.jpg", "local-filename.jpg")

#x = urllib.request.urlretrieve("https://pbs.twimg.com/media/EqxwHtBXcAUE_7B.jpg", "asda.jpg")

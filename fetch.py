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
  "jiu": "minjihourly",
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

image_count = pd.read_csv('image_count.csv', index_col='Unnamed: 0').to_dict()['0']

first_id = {
  "jiu": 0,
  "sua": 0,
  "siyeon": 0,
  "handong": 0,
  "yoohyeon": 0,
  "dami": 0,
  "gahyeon": 0,
  'heejin': 0, 
  'hyunjin': 0,
  'haseul': 0, 
  'yeojin': 0, 
  'vivi': 0, 
  'kimlip': 0, 
  'jinsoul': 0, 
  'choerry': 0, 
  'yves': 0, 
  'chuu': 0,  
  'gowon': 0,
  'oliviahye': 0
}

last_id = pd.read_csv('last_id.csv', index_col='Unnamed: 0').to_dict()['0']

def fetch(dict, folder):    
  for key,value in dict.items():
    public_tweets = api.user_timeline(value, count = 200, include_rts = 'false', exclude_replies = 'true')
    url = []
    for tweet in public_tweets:
      if "media" in tweet.entities:
          if "thumb" not in tweet.entities["media"][0]['media_url']:         
              first_id[key] = tweet.id
              break
    for tweet in public_tweets:
      print(tweet.id)
      print(str(key)+str(last_id[key]))
      if (tweet.id == last_id[key]):
          break
      if "media" in tweet.entities:
          if "thumb" not in tweet.entities["media"][0]['media_url']:         
              url.append(tweet.entities["media"][0]['media_url'])
    for image in url:
      image_count[key] += 1
      name = "images" + "/" + folder + "/" + key + str(image_count[key])+".jpg"
      print(name)
      urllib.request.urlretrieve(image, name)


fetch(deukae, 'deukae')
fetch(loona, 'loona')

pd.DataFrame.from_dict(first_id, orient='index').to_csv('last_id.csv')
pd.DataFrame.from_dict(image_count, orient='index').to_csv('image_count.csv')

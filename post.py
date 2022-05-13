# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 23:46:12 2021

@author: Renan
"""
import tweepy
import pandas as pd
import random
from os import environ
import ast

import pickle
import os.path
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

SERVICE_ACCOUNT = ast.literal_eval(environ['SERVICE_ACCOUNT'])

def drive_auth():
    credentials = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)
    return service

def download_file(service, filename):
  phrase = "name contains '" + filename + "'"
  # Call the Drive v3 API
  results = service.files().list(q=phrase,
      pageSize=10, fields="nextPageToken, files(id, name)").execute()
  print(results)

  import io
  from googleapiclient.http import MediaIoBaseDownload
  # if you get the shareable link, the link contains this id, replace the file_id below
  file_id = results['files'][0]['id']
  request = service.files().get_media(fileId=file_id)
  # replace the filename and extension in the first field below
  fh = io.FileIO(filename, mode='w')
  downloader = MediaIoBaseDownload(fh, request)
  done = False
  while done is False:
      status, done = downloader.next_chunk()
      print("Download %d%%." % int(status.progress() * 100))
  return file_id

def upload_file(service, filename, file_id):
    from googleapiclient.http import MediaFileUpload
    file_metadata = {'name': filename}
    media = MediaFileUpload(filename, resumable=True)
    file = service.files().update(fileId=file_id, body=file_metadata,
                                    media_body=media).execute()
      
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)
#api.update_status(status='auth works')
 
accounts = {
  "jiu": "jiuhourly",
  "sua": "suahours",
  "siyeon": "siyeonhourly",
  "handong": "hourlydong",
  "yoohyeon": "HourlyYoohyeon",
  "dami": "hourly_dami",
  "gahyeon": "hourlygah",
  'heejin': 'heeukis', 
  'hyunjin': 'hourlyaeong', 
  'haseul': 'hourseul', 
  'yeojin': 'yeojinhours', 
  'vivi': 'vivigraphy', 
  'kimlip': 'kimliphourly', 
  'jinsoul': 'hoursouler', 
  'choerry': 'choerryhour', 
  'yves': 'yveryhour', 
  'chuu': 'hourIychuu', 
  'gowon': 'pgwnhour',
  'oliviahye': 'oliviahyehourly'
}


def hloonacatcher():
  fuso = timezone(timedelta(hours = 9), 'KST')
  print(datetime.now(fuso))
  service = drive_auth()
  file_id = download_file(service, 'images_to_post.csv')
  images = pd.read_csv('images_to_post.csv').drop(columns='Unnamed: 0')
  image_loona = images["loona"][0]
  image_deukae = images["deukae"][0]


  download_file(service, image_loona)
  download_file(service, image_deukae)

  files = [image_loona, image_deukae]
  file1 = random.choices(files, weights=[70,30], k=1)
  filenames = file1 + list(set(files) - set(file1))
  status = '@' + accounts[''.join([i for i in filenames[0].partition(".")[0] if not i.isdigit()])]+' ✨ '+'@'+accounts[''.join([i for i in filenames[1].partition(".")[0] if not i.isdigit()])]
  media_ids = []
  for filename in filenames:
      res = api.media_upload(filename)
      media_ids.append(res.media_id)

  api.update_status(status=' ✨ '+status+' ✨ ', media_ids=media_ids)
  os.system('rm ' + image_loona)
  os.system('rm ' + image_deukae)

  images = images.drop([0])
  images = images.reset_index().drop(columns='index')
  images.to_csv('images_to_post.csv')
  upload_file(service, 'images_to_post.csv', file_id)

  file_id_log = download_file(service, 'post_log.csv')
  log = pd.read_csv('post_log.csv').drop(columns='Unnamed: 0')
  log.loc[''] = [''.join([i for i in files[0].partition(".")[0] if not i.isdigit()]), ''.join([i for i in files[1].partition(".")[0] if not i.isdigit()])]
  log = log.reset_index().drop(columns='index')
  log.to_csv('post_log.csv')
  upload_file(service, 'post_log.csv', file_id_log)

import schedule
import time

schedule.every().hour.at(":00").do(hloonacatcher)

while True:
  schedule.run_pending()
  time.sleep(1)

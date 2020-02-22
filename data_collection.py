import pandas as pd
import numpy as np
import os
import tweepy
import json
from datetime import datetime

# Read tokens from external file (security reasons) - Explain how users can enter their own details
with open('../Twitter_api_keys.txt', 'r') as f:
    user_tokens = json.load(f)

# Authenticate 
auth = tweepy.OAuthHandler(user_tokens['consumer_key'], user_tokens['consumer_secret'])
auth.set_access_token(user_tokens['access_token'], user_tokens['access_token_secret'])

# Build the API access point
api = tweepy.API(auth)

# Get current date and format
date = datetime.now().strftime('%d/%m/%Y')

# Parse followers list from Tweepy JSON payload
followers = ['@'+user.screen_name for user in api.followers()]
print(followers)

# Create payload for Postgres db - insert daily follower count as row into db table
num_followers = len(followers)
day_summary = (date, num_followers)
print(day_summary)
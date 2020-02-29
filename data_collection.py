import pandas as pd
import numpy as np
import os
import tweepy
import json
from datetime import datetime
import psycopg2

###             EXTRACT TWITTER DATA            ###
authentication_file = '../Twitter_api_keys.txt'

# Read file for authentication
def read_auth_file(filepath): # Test if input can be passed into kwargs
    with open(filepath, 'r') as f:
        user_tokens = json.load(f)
    return user_tokens

# Authenticate and return api object
def authenticate(auth_data):    
    auth = tweepy.OAuthHandler(auth_data['consumer_key'], 
                            auth_data['consumer_secret'])

    auth.set_access_token(auth_data['access_token'], 
                            auth_data['access_token_secret'])
    
    api = tweepy.API(auth)
    return api

# Get number of followers
def get_followers(api_object):
    followers = ['@'+user.screen_name for user in api_object.followers()]
    return len(followers)

# Get the current date 
def get_current_date():
    return datetime.now().strftime('%d/%m/%Y')

# Function to find difference between current date and date of starting -> this depends on "get_current_date()"
def challenge_day_number(current_date):
    start = datetime.strptime('22/02/2020', "%d/%m/%Y") # Can alter start date later by including as a parameter but hard coding for now
    current_date = datetime.strptime(current_date, "%d/%m/%Y")
    return (abs((current_date - start).days))

def create_data_payload(date, num_followers, day_of_challenge):
    print((date, num_followers, day_of_challenge))
    return (date, num_followers, day_of_challenge)

pipeline1 = get_followers(authenticate(read_auth_file('/home/bogdan/Documents/Twitter_api_keys.txt'))) # returns work as intended

pipeline2 = get_current_date()

pipeline3 = challenge_day_number(pipeline2)

task_end = (pipeline2, pipeline1, pipeline3)

f = open('/home/bogdan/Documents/log.txt', 'a')
f.write(str(datetime.now())+" --> "+str(task_end)+"\n")
f.close()

###             INSERT DATA INTO POSTGRES                  ###
def update_db():
    # depends on the task_end and should read task end
    try:
        # Connect to existing database 
        conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='pass'")
        cursor = conn.cursor()

        # Verify the results
        cursor.execute("SELECT date FROM twitter_followers.followers")
        records = cursor.fetchall()

        # Iterate through all the dates within the table
        for i in records:
            if i[0] == task_end[0]:
                print("date already exists")
                continue
            else:
                # Insert the day summary payload as a row into the db table 
                print('safe to insert')
                cursor.execute("INSERT INTO twitter_followers.followers (date, follower_count, day) VALUES (%s, %s, %s)", task_end)
                # Commit the changes
                conn.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from postgres", error)    
    finally:
        if(conn):
            # Close connection
            cursor.close()
            conn.close()

# Call the postgres database update and check if entry for todays date has already been created
update_db()


# Function to find difference between current date and date of starting
# def challenge_day_number(start, current_date):
#     start = datetime.strptime(start, "%d/%m/%Y")
#     current_date = datetime.strptime(current_date, "%d/%m/%Y")
#     return (abs((current_date - start).days))

# Declare the start date of the 100DaysOfCode challenge
# first_day = '22/02/2020'

# # Read tokens from external file (security reasons) - Explain how users can enter their own details
# with open('../Twitter_api_keys.txt', 'r') as f:
#     user_tokens = json.load(f)

# # Authenticate 
# auth = tweepy.OAuthHandler(user_tokens['consumer_key'], 
#                             user_tokens['consumer_secret'])

# auth.set_access_token(user_tokens['access_token'], 
#                             user_tokens['access_token_secret'])

# # Build the API access point
# api = tweepy.API(auth)
# print(api)

# # authenticate('../Twitter_api_keys.txt')

# # Get current date and format
# date = datetime.now().strftime('%d/%m/%Y')

# # Calculate days since starting challenge
# days_since_start = challenge_day_number(first_day, date)

# # Parse followers list from Tweepy JSON payload
# followers = ['@'+user.screen_name for user in api.followers()]
# num_followers = len(followers)

# # Create payload for Postgres db - insert daily follower count as row into db table
# day_summary = (date, num_followers, days_since_start)

# print(day_summary)


import pandas as pd
import numpy as np
import os
import tweepy
import json
from datetime import datetime
import psycopg2

###             EXTRACT TWITTER DATA            ###

# Function to find difference between current date and date of starting
def challenge_day_number(start, current_date):
    start = datetime.strptime(start, "%d/%m/%Y")
    current_date = datetime.strptime(current_date, "%d/%m/%Y")
    return (abs((current_date - start).days))

# Declare the start date of the 100DaysOfCode challenge
first_day = '22/02/2020'

# Read tokens from external file (security reasons) - Explain how users can enter their own details
with open('../Twitter_api_keys.txt', 'r') as f:
    user_tokens = json.load(f)

# Authenticate 
auth = tweepy.OAuthHandler(user_tokens['consumer_key'], 
                            user_tokens['consumer_secret'])

auth.set_access_token(user_tokens['access_token'], 
                            user_tokens['access_token_secret'])

# Build the API access point
api = tweepy.API(auth)

# Get current date and format
date = datetime.now().strftime('%d/%m/%Y')

# Calculate days since starting challenge
days_since_start = challenge_day_number(first_day, date)

# Parse followers list from Tweepy JSON payload
followers = ['@'+user.screen_name for user in api.followers()]
num_followers = len(followers)

# Create payload for Postgres db - insert daily follower count as row into db table
day_summary = (date, num_followers, days_since_start)

print(day_summary)

###             INSERT DATA INTO POSTGRES                  ###


def update_db():
    try:
        # Connect to existing database 
        conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='pass'")
        cursor = conn.cursor()

        # Verify the results
        cursor.execute("SELECT date FROM twitter_followers.followers")
        records = cursor.fetchall()

        # Iterate through all the dates within the table
        for i in records:
            if i[0] == date:
                print("date already exists")
                continue
            else:
                # Insert the day summary payload as a row into the db table
                print('safe to insert')
                try:
                    cursor.execute("INSERT INTO twitter_followers.followers (date, follower_count, day) VALUES (%s, %s, %s)", day_summary)
                   # Commit the changes
                    conn.commit()
                except(Exception, psycopg2.Error) as error:
                    print("Error while attempting to insert row into table", error)
                finally:
                    # Close connection
                    cursor.close()
                    conn.close()
                    print("postgres connection closed")

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from postgres", error)    
    finally:
        if(conn):
            # Close connection
            cursor.close()
            conn.close()

# Call the postgres database update and check if entry for todays date has already been created
update_db()
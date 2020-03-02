# Twitter followers ETL pipeline

## Purpose of the project 
Starting the #100DaysOfCode challenge, I wanted to explore and learn more about data engineering and also investigate if this challenge is a good way to build a good network over Twitter, and meet new people. 

## What was developed
As such, I developed this program - an ETL pipeline to extract data from Twitter (list of followers), count the number of followers my account has, computes the day of the challenge and the date at runtime, and uses this data to populate a PostgreSQL database table (each day has its own row). This entire process is scheduled to run at 10:24 PM EST with a cronjob.

## Skills aimed at being developed
The aim of this project was to further develop my skills as a data engineer with regards to:
+ Extracting data from services using an API.
+ Writing pipelines using functional programming principles (pure tasks, reproducibility, immutable objects).
+ Setting up a relational database.
+ Using SQL and Python for validating data insertions into a database table. 
+ Using cronjobs to schedule the ETL process to execute and update the database.

## Learnings
Although simple, this project was a great introduction into the #100DaysOfCode and has allowed to develop my skills as a data engineer. Firstly, I took this opportunity to learn to write pipelines in a functional programming way. This involved writing pure tasks that are [idempotent](https://en.wikipedia.org/wiki/Idempotence) and [deterministic](https://en.wikipedia.org/wiki/Deterministic_system), so the result of each task will produce the same result each time it is run. This has also resulted in the code being easier to read and understand since each function only has one purpose. 

This project was also my first attempt at using Postgres on a Linux operating system (Ubuntu). I took this opportunity to learn how to configure Postgres and interact with it using both the terminal and pgadmin. In addition to this, I also used this project as a means to practice my SQL skills and develop validation protocols to ensure that the database can only be updated once per day.

I also wanted to use this project to learn how to use Apache Airflow and schedule the tasks using DAG's. However, I decided that due to its simplistic nature, a cronjob would suffice and I could always come back and implement Airflow at a later date. This was also my first exposure to cronjobs, and as such learnt how to schedule bash scripts using crontab and using bash scripts to activate virtual environments and run python scripts.

Lastly, I also used this project as a means of learning how to use and interact with the Twitter API, as well as using external means (file located outside of git repository) to store API keys, and parsing them into the program instead of hard coding values.

# Required installations
+ Postgres (and pgadmin if you prefer using the GUI)
+ Python3
+ psycopg2
+ tweepy

This project was also developed in Linux (Ubuntu)

# Deeper explanation of the program
Tweepy requires 4 unique keys to authenticate, these can be found in your app within your Twitter developer account. For the purpose of this project, a file with JSON formatting was created locally outside the repository and its contents are parsed into the program using the JSON module (done for security reasons). Using the data parsed from this file, the connection to the API is authenticated and an API object is created.

The three main data points used for this project are:
+ The current date (collected via datetime)
+ The number of followers at the time the API is called (collected via finding the length of the list of followers)
+ The challenge day (finding the difference in days between the day of execution and the start date of the challenge)

This data is then stored within a tuple. This data is also parsed to a logfile along with the date of execution.

The tuple containing all of the data is then sent to the Postgres database. The configuration for this project is as follows:
+ dbname = postgres
+ user = postgres
+ host = localhost
+ password = pass
+ schema = twitter_followers
+ tablename = followers

To ensure that each day only has one entry, a validation protocol was developed using psycopg2. This involves extracting the current table contents from the table "followers" and iterating through the rows to check if the date data from the tuple being inserted into the table doesn't already exist in the table. 

This entire process is then scheduled to execute every night using a cronjob via crontab on Ubuntu. This involved developing a shell script that runs the "data_collection.py" script using the Python version within the virtual environment. This was done to ensure that all of the pip packages installed would also be loaded when executing the file through the cron job. This shell script was then added to the crontab file for my logged in user and scheduled to run at 10:35 PM EST. This process ensures that the database is as up to date as possible and automates the update process. It also means the database is updated at the same time every night.

## TODO
+ Flow diagram




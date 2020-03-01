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

# TODO
+ Include installation instructions
+ Include pip list
+ Deeper explanation of the program itself
+ Flow diagram




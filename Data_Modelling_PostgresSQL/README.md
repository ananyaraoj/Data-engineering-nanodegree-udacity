# Data Modelling with PostGres: Sparkify ETL using Python
=====================================================================================================================================
## Introduction
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.<br> 

Your role is to create a database schema and ETL pipeline for this analysis. 

## Datasets

There are 2 datasets provided, **song** and **log** datasets. Using them, you have to design a star schema optimized for queries on song play analysis.
### Song dataset: 
Each file is in JSON format and contains metadata about a song and the artist of that song. You can find it in data/song_data. For instance, the file TRAABJL12903CDCF1A.json, looks like
>{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
### Log dataset:
This dataset consists of logfiles generated based on the song data. The files are in JSON format, partitioned by year and month. Below is an example of what the data in a log file, 2018-11-12-events.json, looks like.<br>
>{"artist":"Mr Oizo","auth":"Logged In","firstName":"Kaylee","gender":"F","itemInSession":3,"lastName":"Summers","length":144.03873,"level":"free","location":"Phoenix-Mesa-Scottsdale, AZ","method":"PUT","page":"NextSong","registration":1540344794796.0,"sessionId":139,"song":"Flat 55","status":200,"ts":1541106352796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/35.0.1916.153 Safari\/537.36\"","userId":"8"}

## Database Schema Design:
Using the song and log datasets, you'll need to create a star schema optimized for queries on song play analysis. This includes the following tables.
### Fact Table: 
**1. songplays**:
Records in log data associated with song plays i.e. records with page NextSong.<br>songplay_id(*serial*), start_time(*timestamp*), user_id(*int*), level(*varchar*), song_id(*varchar*), artist_id(*varchar*), session_id(*varchar*), location(*varchar*), user_agent(*varchar*).
### Dimension Table: 
**2. users** -  users in the app<br>
user_id(*int*), first_name(*varchar*), last_name(*varchar*), gender(*varchar*), level(*varchar*)<br>
**3. songs** - songs in music database<br>
song_id(*varchar*), title(*varchar*), artist_id(*varchar*), year(*int*), duration(*float*)<br>
**4. artists** - artists in music database<br>
artist_id(*varchar*), name(*varchar*), location(*varchar*), latitude(*numeric*), longitude(*numeric*)<br>
**5. time** - timestamps of records in songplays broken down into specific units<br>
start_time(*timestamp*), hour(*int*), day(*int*), week(*int*), month(*int*), year(*int*), weekday(*varchar*)<br>

**ER diagram of schema design**:
![](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/33760/1594690245/Song_ERD.png)

## Project Structure:
The following files can be found in the dashboard in the left.
1. **data** : You can find all the song data and log data JSON files here. 
2. **sql_queries.py** : All the SQL queries pertaining to creating, insering and dropping tables will be written by you in this file.
3. **create_tables.py** : drops and creates tables. You run this file to reset your tables before each time you run your ETL scripts.
4. **etl.ipynb** : reads and processes a single file from song_data and log_data and loads the data into your tables.
5. **etl.py** : reads and processes all files from song_data and log_data and loads them into your tables.You can fill this out based on your work in the ETL notebook.
6. **README.md** : The document you are currently viewing, has all the information about this project.

## Project Steps involved:
1. Firstly, I wrote DROP, CREATE and INSERT query statements in sql_queries.py
2. I then ran create_tables.py using the terminal provided to create tables
> **python create_tables.py**
3. Ran test.ipynb to confirm the creation of tables as I progressed.
4. Developed ETL processes by by following given instructions in etl.ipynb and completing it. Confirmed it by running test.ipynb.
5. Filled in etl.py by referring to etl.ipynb to build the ETL pipeline and ran it in the terminal.
> **python etl.py**
6. Verified and confirmed the insertion of records into each table by running test.ipynb






# PROJECT - DATA WAREHOUSE 

## 1. Project description: 

Sparkify, a music streaming app wants to move their processes and data onto the cloud as their user base and song base is increasing. Their data is curretnly stored in S3 buckets in the form of JSON files of songs and user activity on their app. 

The aim of the project is to build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for further analysis.

## 2. Datasets

There are 2 datasets provided, **song** and **log** datasets that reside in S3. Using them, you have to design a star schema optimized for queries on song play analysis.<br>
Link for the datasets: <br>

  1) **Song data**         :  s3://udacity-dend/song_data <br>
  2) **Log data**          :  s3://udacity-dend/log_data<br>
  3) **Log data json path**:  s3://udacity-dend/log_json_path.json<br> <br>
  
* ###  Song dataset: 

    Each file is in JSON format and contains metadata about a song and the artist of that song. You can find it in data/song_data. For instance, the     file TRAABJL12903CDCF1A.json, looks like:<br>
    >{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name":      "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}<br> <br>
<br>
* ###  Log dataset:

    This dataset consists of logfiles generated based on the song data. The files are in JSON format, partitioned by year and month. Below is an      example of what the data in a log file, 2018-11-12-events.json, looks like:<br>
> {"artist":"MrOizo","auth":"LoggedIn","firstName":"Kaylee","gender":"F","itemInSession":3,"lastName":<br>"Summers","length":144.03873,"level":"free",
    "location":"Phoenix-Mesa-Scottsdale, AZ","method":"PUT","page":"NextSong","registration":1540344794796.0,"sessionId":139,"song":"Flat  55","status":200,"ts":1541106352796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/35.0.1916.153  Safari\/537.36\"","userId":"8"}

## 3.  Database Schema Design:
Using the song and event datasets, you'll need to create a star schema optimized for queries on song play analysis. This includes the following tables.
* ### Staging tables:
These are the initial tables used to copy data from S3. These are further used to insert data into fact and dimension tables.
 * **staging_events**:<br>
  Log data records in s3 bucket are copied into this table.<br>
  >  artist(*varchar*), auth(*varchar*), firstName(*varchar*), gender(*varchar*), itemInSession(*varchar*), lastName(*varchar*), length(*FLOAT*), level(*varchar*), location(*varchar*), method(*varchar*),page(*varchar*), registration(*float*), sessionId(*int*), song(*varchar*), status(*int*),
  ts(*timestamp*), userAgent(*varchar*), userId(*int*).<br><br>
  * **staging_songs**: <br>
  Song data records in s3 bucket are copied into this table.<br>
  > numsongs(*int*), artist_id(*varchar*),  artist_latitude(*float*), artist_longitude(*float*), artist_location(*varchar*), artist_name(*varchar*), song_id(*varchar*), title(*varchar*), duration(*float*), year(*int*)<br><br>
 
* ### Fact Table: 
 * **songplays**:<br>
Records in staging tables associated with song plays i.e. records with page NextSong.<br>
> songplay_id(*int*), start_time(*timestamp*), user_id(*int*), level(*varchar*), song_id(*varchar*), artist_id(*varchar*), session_id(*int*), location(*varchar*), user_agent(*varchar*).
* ### Dimension Tables: 
 * **users** -  users in the app<br>
> user_id(*int*), first_name(*varchar*), last_name(*varchar*), gender(*varchar*), level(*varchar*)<br>
 * **songs** - songs in music database<br>
> song_id(*varchar*), title(*varchar*), artist_id(*varchar*), year(*int*), duration(*float*)<br>
 * **artists** - artists in music database<br>
> artist_id(*varchar*), name(*varchar*), location(*varchar*), latitude(*numeric*), longitude(*numeric*)<br>
 * **time** - timestamps of records in songplays broken down into specific units<br>
> start_time(*timestamp*), hour(*int*), day(*int*), week(*int*), month(*int*), year(*int*), weekday(*varchar*)<br>


## 4. Project Structure:
The following files can be found in the dashboard in the left.
1. **sql_queries.py** : All the SQL queries pertaining to creating, staging, inserting and dropping tables will be written by you in this file.
2. **create_tables.py** : drops and creates tables including staging tables, fact and dimension tables.
3. **etl.py** : Data gets loaded from S3 onto the staging tables on Redshift cluster and then gets inserted into the final tables on the cluster.
4. **README.md** : The document you are currently viewing, has all the information about this project.
5. **dwh.cfg** : This document stores all the values pertaining to cluster, IAM role, endpoint etc. Both  create_tables.py and etl.py read this file inorder to make necessary connection with the cluster to perform operations defined in sql_queries.py file.

## Project procedure breakdown: 
1. Firstly, write DROP, CREATE, COPY and INSERT query statements in sql_queries.py
2. Go to <https://aws.amazon.com> and create an IAM role with read access to S3.
3. Create a security group which authorizes access to cluster.
4. Create a cluster and configure it with the IAM role and security group.
5. Fill in the dwh.cfg file with the associated values.
6. Run create_tables.py using the terminal provided to create tables.
7. Use the query editor in the redshift console to verify the schemas that just got created.
> **python create_tables.py**
8. Upnext, we build the ETL pipeline by running etl.py. This leads to copying data from s3 to the staging tables, staging tables to the fact and dimension tables and finally into the cluster. 
> **python etl.py**
9. Create a postgressql database in the aws RDS.
9. Run the analytic queries on your redshift database using the query editor in the RDS to view the data.
10. Delete your cluster and other instances that you have created.

## Queries and results:

Run this query on every table and obtain the results.

> SELECT COUNT(*) from table

### Results obtained :

**Table name**   | **Number of records**
-------------- | -------------
staging_events | 8056
staging_songs  | 14896
song_plays     | 333 
user           | 105
songs          | 14896
artists        | 10025
time           | 8023








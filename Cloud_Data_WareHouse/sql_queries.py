import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')


# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES
print(" Creating staging events table............")
staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events(
        artist              VARCHAR,
        auth                VARCHAR,
        firstName           VARCHAR,
        gender              VARCHAR,
        itemInSession       INTEGER,
        lastName            VARCHAR,
        length              FLOAT,
        level               VARCHAR,
        location            VARCHAR,
        method              VARCHAR,
        page                VARCHAR,
        registration        FLOAT,
        sessionId           INTEGER,
        song                VARCHAR,
        status              INTEGER,
        ts                  TIMESTAMP,
        userAgent           VARCHAR,
        userId              INTEGER )

""")

print(" staging events table is created!")
print(" \n Creating staging songs table............")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs
    (
        num_songs           INTEGER,
        artist_id           VARCHAR,
        artist_latitude     FLOAT,
        artist_longitude    FLOAT,
        artist_location     VARCHAR,
        artist_name         VARCHAR,
        song_id             VARCHAR,
        title               VARCHAR,
        duration            FLOAT,
        year                INTEGER
    )
""")
print(" songs table is created.")
print(" \n Creating songplay table............")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays
    (
        songplay_id         INTEGER         IDENTITY(0,1) PRIMARY KEY,
        start_time          TIMESTAMP       NOT NULL SORTKEY DISTKEY,
        user_id             INTEGER         NOT NULL,
        level               VARCHAR,
        song_id             VARCHAR         NOT NULL,
        artist_id           VARCHAR         NOT NULL,
        session_id          INTEGER,
        location            VARCHAR,
        user_agent          VARCHAR
    )
""")
print(" songplay table is created.")
print(" \n Creating user table............")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (
        user_id             INTEGER         NOT NULL SORTKEY PRIMARY KEY,
        first_name          VARCHAR         NOT NULL,
        last_name           VARCHAR         NOT NULL,
        gender              VARCHAR         NOT NULL,
        level               VARCHAR         NOT NULL
    )
""")

print("User table is created")
print(" \n Creating song table............")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS song
    (
        song_id             VARCHAR         NOT NULL SORTKEY PRIMARY KEY,
        title               VARCHAR         NOT NULL,
        artist_id           VARCHAR         NOT NULL,
        year                INTEGER         NOT NULL,
        duration            FLOAT
    )
""")

print(" song table is created")
print(" \n Creating artist table............")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artist 
    (
        artist_id           VARCHAR         NOT NULL SORTKEY PRIMARY KEY,
        name                VARCHAR         NOT NULL,
        location            VARCHAR,
        latitude            FLOAT,
        longitude           FLOAT
    )
""")

print(" Artist table is created.")
print(" \n Creating time table............")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time 
    (
        start_time          TIMESTAMP       NOT NULL DISTKEY SORTKEY PRIMARY KEY,
        hour                INTEGER         NOT NULL,
        day                 INTEGER         NOT NULL,
        week                INTEGER         NOT NULL,
        month               INTEGER         NOT NULL,
        year                INTEGER         NOT NULL,
        weekday             VARCHAR(20)     NOT NULL 
    )
""")

print(" time table is created............")
print(" \n Staging tables : Copying data from S3 bucket into the staging table: ")

# STAGING TABLES
print(" 1. Copying data from S3 bucket into the staging  events table: ")
staging_events_copy = ("""
    copy staging_events from {data_bucket}
    credentials 'aws_iam_role={redshift_role}'
    region 'us-west-2' format as JSON {log_json_path}
    timeformat as 'epochmillisecs';
""").format(data_bucket=config['S3']['LOG_DATA'], redshift_role=config['IAM_ROLE']['ARN'], log_json_path=config['S3']['LOG_JSONPATH'])

print(" Data copied into staging events table!")
print(" 2. Copying data from S3 bucket into the staging  events table: ")


staging_songs_copy = ("""
    copy staging_songs from {data_bucket}
    credentials 'aws_iam_role={redshift_role_2112}'
    region 'us-west-2' format as JSON 'auto';
""").format(data_bucket=config['S3']['SONG_DATA'], redshift_role_2112=config['IAM_ROLE']['ARN'])

print(" Data copied into staging events table!")
print(" Data insertion from staging tables into final tables")

# FINAL TABLES

print(" \n \n 1. Inserting data into songplays table from staging events table....")

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT  DISTINCT(e.ts)  AS start_time, 
            e.userId        AS user_id, 
            e.level         AS level, 
            s.song_id       AS song_id, 
            s.artist_id     AS artist_id, 
            e.sessionId     AS session_id, 
            e.location      AS location, 
            e.userAgent     AS user_agent
    FROM staging_events e
    JOIN staging_songs  s   ON (e.song = s.title AND e.artist = s.artist_name);
    
""")
print(" Data inserted into songplays.")
print(" \n 2. Inserting data into user table from staging events table.... ")
user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT  DISTINCT(userId)    AS user_id,
            firstName           AS first_name,
            lastName            AS last_name,
            gender,
            level
    FROM staging_events
    WHERE user_id IS NOT NULL
   
""")

print(" Data inserted into user table.")
print(" \n 3.Inserting data into song table from staging songs table............")

song_table_insert = ("""
    INSERT INTO song (song_id, title, artist_id, year, duration)
    SELECT  DISTINCT(song_id) AS song_id,
            title,
            artist_id,
            year,
            duration
    FROM staging_songs
    WHERE song_id IS NOT NULL;

""")

print(" Data inserted into song table")
print(" \n 4. Inserting data into artist table from staging songs table............")

artist_table_insert = ("""
    INSERT INTO artist (artist_id, name, location, latitude, longitude)
    SELECT  DISTINCT(artist_id) AS artist_id,
            artist_name         AS name,
            artist_location     AS location,
            artist_latitude     AS latitude,
            artist_longitude    AS longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
""")
print(" Data inserted into artist table.")
print(" \n 5. Inserting data into time table from songplays table............")


time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT  DISTINCT(start_time)                AS start_time,
            EXTRACT(hour FROM start_time)       AS hour,
            EXTRACT(day FROM start_time)        AS day,
            EXTRACT(week FROM start_time)       AS week,
            EXTRACT(month FROM start_time)      AS month,
            EXTRACT(year FROM start_time)       AS year,
            EXTRACT(dayofweek FROM start_time)  as weekday
    FROM songplays;
""")
print(" \n Data inserted into the time table.")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

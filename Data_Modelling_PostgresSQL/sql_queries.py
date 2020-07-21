# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS user_table"
song_table_drop = "DROP TABLE IF EXISTS song_table"
artist_table_drop = "DROP TABLE IF EXISTS artist_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES

# start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays(
        songplay_id serial PRIMARY KEY,
        start_time timestamp NOT NULL,
        user_id int NOT NULL,
        level varchar,
        song_id varchar,
        artist_id varchar,
        session_id varchar,
        location varchar,
        user_agent varchar
    )
""")

# user_id,first_name, lastName, gender, level
user_table_create = ("""
    CREATE TABLE IF NOT EXISTS user_table(
        user_id int PRIMARY KEY,
        first_name varchar NOT NULL,
        lastName varchar NOT NULL,
        gender varchar,
        level varchar
   )
""")

# song_id, title, artist_id,year, duration
song_table_create = ("""
    CREATE TABLE IF NOT EXISTS song_table(
        song_id varchar PRIMARY KEY,
        title varchar NOT NULL,
        artist_id varchar NOT NULL,
        year int,
        duration float NOT NULL
    )
""")

# artist_id, artist_name, artist_location, artist_latitude, artist_longitude
artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artist_table(
        artist_id varchar PRIMARY KEY,
        artist_name varchar NOT NULL,
        artist_location varchar,
        artist_latitude numeric,
        artist_longitude numeric
    )
""")

#start_time, hour, day , week , month , year , weekday
time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time_table(
        start_time timestamp PRIMARY KEY,
        hour int,
        day int,
        week int,
        month int,
        year int,
        weekday varchar
    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays(
        start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
    INSERT INTO user_table(
        user_id,first_name, lastName, gender, level
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT(user_id) DO UPDATE SET level = excluded.level
""")

song_table_insert = ("""
    INSERT INTO song_table(
        song_id, title, artist_id,year, duration
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING;
""")
    
artist_table_insert = ("""
    INSERT INTO artist_table(
        artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    )
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING;
""")


time_table_insert = ("""
    INSERT INTO time_table(
        start_time, hour, day , week , month , year , weekday 
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS

song_select = ("""
    SELECT song_id, artist_table.artist_id
    FROM song_table JOIN artist_table ON song_table.artist_id = artist_table.artist_id
    WHERE song_table.title = %s
    AND artist_table.artist_name = %s
    AND song_table.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
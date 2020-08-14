import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

# Load data onto the staging tables created in sql_queries.py from S3 buckets. 
def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

# Insert records into the fact and dimension tables from staging tables by running the insert queries defined in sql_queries.py.
def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    # Connect to the database by reading the file dwh.cfg.
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()
    
    print ("End of mains")


if __name__ == "__main__":
    main()
import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

# Drop pre-existing tables to create them again from scratch
def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

# Creates staging, fact and dimension tables by running the query in sql_queries.py file.
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    # Read dwh.cfg file and fetch cluster details to connect to the cluster
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
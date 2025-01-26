#!/usr/bin/env python
# coding: utf-8

# Import libraries
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from time import time
import argparse
import os


#function to load in data
def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.csv'

    # Import csv

    os.system(f"wget {url} -O {csv_name}")

    # Telling pandas that we want to use this schema in postgres using sqlalchemy library
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Load taxi dataset into postgres bdatabase in chunks (as data set is 1.5M rows)
    df_iter = pd.read_csv(csv_name, iterator=True, compression='gzip', chunksize=100000)
#, 
    df = next(df_iter)

    # setting the date datatypes
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Inserting just the column names (i.e. head n=0)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # create loop to add all chunks to the postgres table
    while True:
        try:
            # Returns time stamp at start
            t_start = time()
        
            # Get next chunk
            df = next(df_iter)
        
            # Update datetime data types
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
            # Insert chunk into the database
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        
            # Returns time stamp at end
            t_end = time()
            print('Another chunk inserted..., took %.3f seconds' % (t_end - t_start))
        
        except StopIteration:
            print("All chunks processed.")
            break

if __name__ == '__main__':
    # Set up argparse
    parser = argparse.ArgumentParser(description='Ingest csv data to Postgres')
    parser.add_argument('--user', help='Username for Postgres')
    parser.add_argument('--password', help='Password for Postgres')
    parser.add_argument('--host', help='Host for Postgres')
    parser.add_argument('--port', help='Port for Postgres')
    parser.add_argument('--db', help='Database name for Postgres')
    parser.add_argument('--table_name', help='Name of the table we will write results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)


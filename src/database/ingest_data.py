import pandas as pd
from db_helper import *

import time

def ingest_zones(data_path):
    engine = get_engine(load_config())
    df = pd.read_csv(data_path, index_col='LocationID')
    print (f"Ammount of data: {len(df)}")
    # print(df.head())
    df.to_sql('taxi_zones', engine, if_exists = 'replace')

def ingest_data(data_path, record_rate = 10):
    
    engine = get_engine(load_config())
    df = pd.read_parquet(data_path)
    print (f"Ammount of data: {len(df)}")
    # print(df.head())
    df.head(0).to_sql('yellow_taxi', engine, if_exists = 'replace', index=False, index_label='tpep_pickup_datetime')

    for iter in range(0,len(df),record_rate):
        start_time = time.time() 
        sql_query = 'SELECT * FROM yellow_taxi'
        df_batch = df.iloc[iter:(iter+record_rate)]
        print(f"Ingesting {len(df_batch)} records at {start_time}.", end='\t')
        df_batch.to_sql('yellow_taxi', engine, if_exists = 'append', index=False, index_label='tpep_pickup_datetime')
        df_sql = pd.read_sql(sql_query, engine)
        print(f'Found {len(df_sql)} records in db.')
        elapsed_time = time.time() - start_time
        sleep_time = max(1.0 - elapsed_time, 0) 
        time.sleep(sleep_time)


if __name__ == '__main__':
    path = '/workspaces/local-data-streaming/rides_data/'
    name = 'taxi_data.parquet'
    zones= 'taxi_zone_lookup.csv'

    ingest_zones(data_path=path+zones)
    ingest_data(data_path=path+name)
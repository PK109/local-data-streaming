import pandas as pd
from db_helper import *
import time

def ingest_data(data_path, record_rate = 100):
    engine = get_engine(load_config())
    df = pd.read_parquet(data_path)
    df.head(0).to_sql('yellow_taxi', engine, if_exists = 'replace')
    for iter in range(0,len(df),record_rate):
        start_time = time.time() 
        sql_query = 'SELECT * FROM yellow_taxi'
        df_batch = df.iloc[iter:(iter+record_rate)]
        print(f"Ingesting {len(df_batch)} records at {start_time}.", end='\t')
        df_batch.to_sql('yellow_taxi', engine, if_exists = 'append')
        df_sql = pd.read_sql(sql_query, engine)
        print(f'Found {len(df_sql)} records in db.')
        elapsed_time = time.time() - start_time
        sleep_time = max(1.0 - elapsed_time, 0) 
        time.sleep(sleep_time)


if __name__ == '__main__':
    path = '/workspaces/local-data-streaming/data/'
    name = 'taxi_data.parquet'
    ingest_data(data_path=path+name)
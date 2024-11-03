import pandas as pd
from db_helper import *
import time

def ingest_data(data_path, record_rate = 10):
    
    engine = get_engine(load_config())
    df = pd.read_parquet(data_path)
    
    for iter in range(0,len(df),record_rate):
        start_time = time.time() 
        sql_query = 'SELECT * FROM yellow_taxi'
        df_batch = df.iloc[iter:(iter+record_rate)]
        print(f"Ingesting {len(df_batch)} records at {start_time}.", end='\t')
        df_batch.to_sql('yellow_taxi', engine, if_exists = 'append', index=True, index_label='tpep_pickup_datetime')
        df_sql = pd.read_sql(sql_query, engine)
        print(f'Found {len(df_sql)} records in db.')
        elapsed_time = time.time() - start_time
        sleep_time = max(1.0 - elapsed_time, 0) 
        time.sleep(sleep_time)


if __name__ == '__main__':
    # path = '/workspaces/local-data-streaming/rides_data/'
    path = '/rides_data/'
    name = 'taxi_data.parquet'
    print("DB Ingest is working.")  
    ingest_data(data_path=path+name)

# Filtrowanie po:
# 'tpep_pickup_datetime',
# 'tpep_dropoff_datetime', 
# 'trip_distance',
# 'PULocationID',
# 'DOLocationID',
# 'total_amount',
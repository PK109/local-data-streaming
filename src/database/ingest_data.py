import pandas as pd
from dotenv import load_dotenv
from db_helper import *
import time

def ingest_data(data_path, record_rate = 10):
    
    engine = get_engine(load_config())
    df = pd.read_parquet(data_path)
    df.head(0).to_sql('yellow_taxi', engine, if_exists = 'replace', index=False, index_label='tpep_pickup_datetime')
    
    for iter in range(0,len(df),record_rate):
        start_time = time.time() 
        sql_query = 'SELECT * FROM yellow_taxi'
        df_batch = df.iloc[iter:(iter+record_rate)]
        print(f"Ingesting {len(df_batch)} records at {round(start_time) % 1000}.", end='\t')
        df_batch.to_sql('yellow_taxi', engine, if_exists = 'append', index=False, index_label='tpep_pickup_datetime')
        df_sql = pd.read_sql(sql_query, engine)
        print(f'Found {len(df_sql)} records in db.')
        elapsed_time = time.time() - start_time
        sleep_time = max(1.0 - elapsed_time, 0) 
        time.sleep(sleep_time)


if __name__ == '__main__':
    env_path = '/app/.env'
    load_dotenv(dotenv_path=env_path)
    try:
        record_rate = int(os.getenv("RECORD_RATE"))
        print(f"\nSimulation with the rate of {record_rate} records per second.")
    except:
        record_rate = 10
        print("\nSimulation with default 10 record rate.")

    path = '/rides_data/'
    name = 'taxi_data.parquet'
    print("DB Ingest is working.")  
    ingest_data(data_path=path+name, record_rate=record_rate)
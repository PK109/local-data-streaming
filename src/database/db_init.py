import pandas as pd
from db_helper import *


def init_data(data_path):
    engine = get_engine(load_config())
    df = pd.read_parquet(data_path)
    df.head(0).to_sql('yellow_taxi', engine, if_exists = 'replace', index=False, index_label='tpep_pickup_datetime')

def ingest_zones(data_path):
    engine = get_engine(load_config())
    df = pd.read_csv(data_path, index_col='LocationID')
    df.to_sql('taxi_zones', engine, if_exists = 'replace')

if __name__ == '__main__':
    # path = '/workspaces/local-data-streaming/rides_data/'
    path = '/rides_data/'
    name = 'taxi_data.parquet'
    zones= 'taxi_zone_lookup.csv'
    print("DB Init is working.")  
    init_data(data_path=path+name)
    ingest_zones(data_path=path+zones)
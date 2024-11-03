import pandas as pd
from db_helper import *
import time

def data_aggregation(data_path):

    df = pd.read_parquet(data_path)
    df.reset_index(inplace=True, names='ServiceID')
    df= df[df['trip_distance']>0]
    df_duplicates = df[df.duplicated(subset=['tpep_pickup_datetime','tpep_dropoff_datetime'], keep=False)]
    print(len(df_duplicates))
    print(df_duplicates.columns)
    print(df_duplicates.sort_values(by='tpep_pickup_datetime'))
    df_filtered = df_duplicates.groupby(
        by=['tpep_pickup_datetime','tpep_dropoff_datetime']).agg(
            sum_of_totals=pd.NamedAgg(column="total_amount", aggfunc=lambda x: round(sum(x),2)),
            sum_of_tips=pd.NamedAgg(column="tip_amount", aggfunc="sum"),
            distance_equality=pd.NamedAgg(column="trip_distance", aggfunc=lambda x: len(set(x))==1),
            PULocation_equality=pd.NamedAgg(column="PULocationID", aggfunc=lambda x: len(set(x))==1),
            DOLocation_equality=pd.NamedAgg(column="DOLocationID", aggfunc=lambda x: len(set(x))==1),
            sum_of_trips=pd.NamedAgg(column="VendorID", aggfunc="count"),
            index_distance=pd.NamedAgg(column="ServiceID", aggfunc=lambda x: str([j-i for i, j in zip(x[:-1], x[1:])])[1:-1])
        )

    df_filtered.to_csv("aggregation_file.csv")
    df_duplicates.to_csv('duplication_file.csv')

if __name__ == '__main__':
    path = '/workspaces/local-data-streaming/rides_data/'
    name = 'taxi_data.parquet'
    data_aggregation(data_path=path+name)
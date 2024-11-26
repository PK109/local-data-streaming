import pandas as pd
import numpy as np
from db_helper import *
import matplotlib.pyplot as plt


def max_deviation(value):
    output = (value - max_deviation.max).total_seconds()
    max_deviation.count += 1

    #drop highly deviated values (mimics watermark behaviour)
    if output > 3600 or output < -14400:
        return None
    if output > 0: #increase max value 
        max_deviation.increments += 1
        max_deviation.max = value
    return output


def data_aggregation(data_path):

    #read file
    df = pd.read_parquet(data_path)
    len_df = len(df)
    #initial filters
    df= df[df['trip_distance']>0]
    df= df[df['tpep_pickup_datetime'].dt.year==2024]
    
    #calculate time deviation for pickup time
    #dropoff value have more deviation and would be harder to handle it by streaming analysis
    max_deviation.max = df['tpep_pickup_datetime'].iloc[0]
    max_deviation.increments = 0
    max_deviation.count = 0
    df['time_deviation'] = df['tpep_pickup_datetime'].apply(max_deviation)
    df.dropna(subset='time_deviation', inplace=True)

    # Summary of output
    min_dev = min(df['time_deviation'])
    max_dev = max(df['time_deviation'])

    print(f"Max value have changed {max_deviation.increments} times. Cleaned dataset length: {len(df)}, while original length: {len_df}")
    print(f"Deviation range: {min_dev} to {max_dev}")

    #graphical representation
    fig = plt.figure()
    bin_step = 1000
    xbins = np.arange(round(min_dev,-3), round(max_dev,-3) + bin_step, bin_step)
    counts, bins, bars = plt.hist(df['time_deviation'], bins= xbins, edgecolor= "white")
    
    plt.ylim([0, 1.2 * max(counts)])
    plt.bar_label(bars, fontsize=10, rotation=60)
    plt.xticks(ticks=bins, rotation=60)
    plt.xlabel("Time [in seconds]")
    plt.title("Time deviation from last max pickup time")
    fig.savefig('time_deviation.png')

if __name__ == '__main__':
    path = '/workspaces/local-data-streaming/rides_data/'
    name = 'taxi_data.parquet'
    data_aggregation(data_path=path+name)
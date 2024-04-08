import pandas as pd
import numpy as np

def parse_csv(input_file):
    # check for the correct opening of the file
    try:
        data = pd.read_csv(input_file, header=0, sep=',')
    except:
        print("Error opening the file")
        return None

    return data

def period_checker(data, time_column):
    # take the first perdiod and apply to the rest of the data
    period = data[time_column][1] - data[time_column][0]
    print("Period: ", period)

    data[time_column] = pd.Series(range(0, len(data)*period, period))

    return data
    # for i in range(2, len(data)):
    #     data.loc[i, time_column] = data[time_column][i-1] + period
    # return data

def nan_correction (data, column):
    data.replace('nan', np.NaN, inplace=True)
    data.dropna(subset=column, ignore_index=True,  inplace=True)
    return data

def time_conversion(data, time_column):
    # need to convert any type of time to a timestamp in seconds 
    data[time_column] = pd.to_datetime(data[time_column])
    data[time_column] = data[time_column].dt.strftime('%s')
    data[time_column] = pd.to_numeric(data[time_column])
    return data

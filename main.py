import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from csv_parser import parse_csv
from csv_parser import period_checker
from csv_parser import nan_correction
from csv_parser import time_conversion
from data_reconstruct import interpol_data
from adaptive_sampling import adaptive_sampling
from error_calc import mean_relative_error

if __name__ == '__main__':
    # -------------------------------- Globals --------------------------------
    new_data = []
    new_t = []
    pd.set_option('display.max_columns', None)

    # -------------------------------- Get input ------------------------------
    print("Adaptive Sampling")
    print("---------------")
    print("Enter the values for W, c and h, by default we will use the values from the paper: W = 200, c = 2.1, h = 20")
    W = input("W: ")
    c = input("c: ")
    h = input("h: ")

    if W == "":
        W = 200
    else:
        W = int(W)

    if c == "":
        c = 2.1
    else:
        c = float(c)

    if h == "":
        h = 20
    else:
        h = int(h)

    print("Enter the multiplier for the threshold factor, by default we will use 0.5")
    threshold_factor = input("Threshold factor: ")

    if threshold_factor == "":
        threshold_factor = 0.5
    else:
        threshold_factor = float(threshold_factor)


    print("Enter the path to the csv file containing the data, by default use the file weather.csv")
    
    while True:
        path = input("Path: datasets/")
        if path == "":
            path = './datasets/sensor-data.csv'
        else:
            path = './datasets/' + path

        data = parse_csv(path)
        if data is not None:
            break

    print("Chosse from the following columns the Time column and the column to be reconstructed:")

    to_print = data.columns.tolist()
    for i in range(len(to_print)):
        print("- ", to_print[i])

    while True:
        time_column = input("Time column: ")
        column = input("Data column: ")

        if time_column == "":
            time_column = 'timestamp'

        if column == "":
            column = 'raw_acc:magnitude_stats:mean'
        
        if time_column in to_print and column in to_print:
            break

    data = nan_correction(data, column)

    print("Is the time column in seconds? (y/n)")
    print("First row of the time column: ", data[time_column][0])

    time_in_seconds = input("Is time in seconds: ")

    while time_in_seconds != "y" and time_in_seconds != "n":
        print("Please enter y or n")
        time_in_seconds = input("Is time in seconds: ")

    if time_in_seconds == "n":
        data = time_conversion(data, time_column)

    data = period_checker(data, time_column)


    # -------------------------------- Actual program --------------------------------

    # get the starting time from the first row of the data
    starting_time = data[time_column][0]



    sampling_times = data[time_column]
    F_sampling = 1 / (sampling_times[1] - sampling_times[0])

    print("sampling times: ", sampling_times)



    # get the data from the location:min_altitude column
    data_list = data[column].tolist()


    adaptive_sampling(data[column], W, c, h, F_sampling, new_data, new_t, threshold_factor, starting_time)


    # -------------------------------- Plotting and interpolating ------------------------

    plt.figure(1)
    plt.plot(sampling_times, data[column], 'bo')
    plt.grid(True)
    plt.draw()


    interp_data = interpol_data(new_data, new_t, data[time_column])

        # plt.figure(2)
    plt.plot(data[time_column], interp_data, 'y+')
    plt.draw()
    plt.plot(new_t, new_data, 'rx')
    plt.draw()

    # -------------------------------- Error calculation --------------------------------
    print("Data sizes:")
    print("Original data: ", len(data))
    print("New data: ", len(new_data))

    mre = mean_relative_error(data[column], interp_data, len(data[column]))
    print("Mean relative error: ", mre)

    plt.show()


import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from csv_parser import parse_csv
from data_reconstruct import interpol_data



# W is the initial windows size while c a confidence parameter

def max_frequency(data, start, W, F_sampling):
    y_f = np.fft.fft(data[start:start + W])
    y_f[0] = 0

    max_index = 1
    for i in range(1,len(y_f)):
        if y_f[i] > 0:
            max_index = i
    
    return F_sampling * max_index / W
    # x_f = np.fft.fftfreq(W)

    # # discard negative frequencies
    # x_f = x_f[0:len(x_f)-1]
    # #take the absolute value of the fft
    # y_f = np.abs(y_f[0:len(y_f)-1])
    # # get last x index value for wich the y value is higher than a certain threshold compared to the max magnitude
    # # plt.plot(x_f, y_f)
    # # plt.show()
    # max_y = np.max(y_f)
    # max_index = 1
    # for i in range(len(y_f)):
    #     if y_f[i] > 0:
    #         max_index = i
    # max_f = x_f[max_index]

    # return the frequency of the maximum value
    return max_f



def adaptive_sampling(data, W, c, h, F_sampling, periods, samples, new_data, new_sampling_times):


    F_max = max_frequency(data, 0, W, F_sampling)
    F_c = c * F_max
    F_up = (1 + (c - 2) / 4) * F_max
    F_down = (1 - (c - 2) / 4) * F_max

    h1 = 0
    h2 = 0
    data = data.tolist()


    for i in range(W):
        new_data.append(data[i])

    for i in range(W):
        new_sampling_times.append(i*1/F_sampling)

    i = W

    while True:

        F_max_curr = max_frequency(data, i - W, W, F_sampling) # estimate the frequency of the current window

        if abs(F_max_curr - F_up) < abs(F_max_curr - F_max):
            h1 += 1
            h2 = 0
        elif abs(F_max_curr - F_down) < abs(F_max_curr - F_max):
            h2 += 1
            h1 = 0
        else:
            h1 = 0
            h2 = 0
        if (h1 > h or h2 > h):
            F_c = c * F_max_curr
            F_up = (1 + (c - 2) / 4) * F_max_curr
            F_down = (1 - (c - 2) / 4) * F_max_curr
            # at sample i change the frequency to F_c
            print("New period: ", 1/F_c, " at sample: ", i)


        normalized_period = 1/F_c / (1 / F_sampling)
        if (normalized_period < 1):
            normalized_period = 1
        
        j = i + int(normalized_period)
        i = j

        if(j >= len(data)):
            break
        periods.append(normalized_period)
        samples.append(j)
        print("j: ", j)
        new_data.append(data[j])
        new_sampling_times.append(j*1/F_sampling)




periods = []
samples = []

new_data = []
new_sampling_times = []

print("Adaptive Sampling")
print("---------------")
print("Enter the values for W, c and h, by default we will use the values from the paper: W = 400, c = 2.1, h = 40")

W = input("W: ")
c = input("c: ")
h = input("h: ")

if W == "":
    W = 400
else:
    W = int(W)

if c == "":
    c = 2.1
else:
    c = float(c)

if h == "":
    h = 40
else:
    h = int(h)




print("Enter the path to the csv file containing the data, by default use the file 0A986513-7828-4D53-AA1F-E02D6DF9561B.features_labels.csv")
path = input("Path: ")
if path == "":
    path = './datasets/0A986513-7828-4D53-AA1F-E02D6DF9561B.features_labels.csv'


data = parse_csv('./datasets/0A986513-7828-4D53-AA1F-E02D6DF9561B.features_labels.csv')

# sin wave as test data 
time = data.iloc[:,0]
data__ = np.sin(2 * np.pi * time)

# the time stamps are the first column of the dataframe so we can calculate the sampling frequency
F_sampling = 1 / (data.iloc[1,0] - data.iloc[0,0])
# pass the second column of the dataframe as the data (raw accelerometer data)
# adaptive_sampling(data['location:min_altitude'], W, c, h, F_sampling, periods, samples, new_data, new_sampling_times)
adaptive_sampling(data__, W, c, h, F_sampling, periods, samples, new_data, new_sampling_times)
print("New data: ", len(new_data))
print("New sampling times: ", len(new_sampling_times))

print( len(data['location:min_altitude'].tolist()))
new_data = interpol_data(new_data, new_sampling_times, len(data['location:min_altitude'].tolist()))

normalized_period = periods / (1 / F_sampling)

# get only the samples every new period
old_samples = data['raw_acc:magnitude_stats:mean']
new_samples = []

fig, axes = plt.subplots(3)

# axes[0].plot(data['location:min_altitude'])
axes[0].plot(data__)

axes[1].plot(new_data)
axes[2].plot(samples, periods, 'ro')
plt.show()
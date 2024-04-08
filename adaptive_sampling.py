import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from csv_parser import parse_csv
from csv_parser import period_checker
from csv_parser import nan_correction
from csv_parser import time_conversion
from data_reconstruct import interpol_data
from error_calc import mean_relative_error

def max_frequency(data, start, W, F_sampling, threshold_factor):
    data_actual = data[start:start + W]
    N = len(data_actual)
    sampling_period = 1/F_sampling

    y_f = np.fft.fft(data_actual)
    y_f[0] = 0
    y_f = y_f/N
    y_f = np.abs(y_f)
    x_f = np.fft.fftfreq(N, sampling_period)


    max_mag = np.max(y_f)
    thr_mag = max_mag * threshold_factor
    max_f = 0.0


    for i in range(len(x_f)//2-1):
        if y_f[i] >= thr_mag:
            max_f = x_f[i]

    if (max_f < 0):
        max_f = 0
        print("Max frequency is negative, setting it to 0")

    return max_f




def adaptive_sampling(data, W, c, h, F_sampling, new_data, new_t, threshold_factor, starting_time):


    F_max = max_frequency(data, 0, W, F_sampling, threshold_factor)
    F_c = c * F_max
    F_up = (1 + (c - 2) / 4) * F_max
    F_down = (1 - (c - 2) / 4) * F_max

    print("F_max: ", F_max, "F_up: ", F_up, "F_down: ", F_down)
    print("F_sampling: ", F_sampling)
    h1 = 0
    h2 = 0



    for z in range(W):
        new_data.append(data[z])
        new_t.append(z/F_sampling + starting_time)

    i = W
    j = i

    if 10 * F_c < F_sampling:
        F_c = 0.1 * F_sampling

    period = 1 / F_c

    if (period < 1/F_sampling):
        period = 1/F_sampling
        
    normalized_period = period / (1 / F_sampling) 

    if (normalized_period <= 1):
        normalized_period = 1
    else:
        normalized_period = int(normalized_period) + 1

    while True:
        F_max_curr = max_frequency(data, i - W, W, F_sampling, threshold_factor) # estimate the frequency of the current window
        #print("@time: ", float(i/F_sampling + starting_time), " F_max_curr: ", F_max_curr)
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
            if (F_c > F_sampling):
                F_c = F_sampling
            F_max = F_max_curr
            F_up = (1 + (c - 2) / 4) * F_max
            F_down = (1 - (c - 2) / 4) * F_max
            h1 = 0
            h2 = 0
            # at sample i change the frequency to F_c
            #print("New sampling frequency: ", F_c, " at time: ", float(i/F_sampling + starting_time))
            # can skip the next new_period samples for the new data
            if 10 * F_c < F_sampling:
                F_c = 0.1 * F_sampling

            period = 1 / F_c

            if (period < 1/F_sampling):
                period = 1/F_sampling
                
            normalized_period = period / (1 / F_sampling) 

            if (normalized_period <= 1):
                normalized_period = 1
            else:
                normalized_period = int(normalized_period) + 1
            
            print("New sampling period: ", period, " at time: ", float(i/F_sampling + starting_time), "Normalized period: ", normalized_period)
        
        j = i + int(normalized_period)
        i = j
        
        if(i >= len(data)):
            break
        new_data.append(data[j])
        new_t.append(j/F_sampling + starting_time)
        #print("@time: ", float(i/F_sampling + starting_time), " j: ", j, "Period: ", period, "data[i]: ", data[i], "h1: ", h1, "h2: ", h2)

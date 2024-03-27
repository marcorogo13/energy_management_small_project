import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt

# W is the initial windows size while c a confidence parameter

def max_frequency(data, start, W, F_sampling):
    y_f = np.fft.fft(data.iloc[start:start + W])
    y_f[0] = 0
    x_f = np.fft.fftfreq(W, 1 / F_sampling)
    # discard negative frequencies
    x_f = x_f[0:W // 2]
    #take the absolute value of the fft
    y_f = np.abs(y_f[0:W // 2])
    # get last x index value for wich the y value is higher than a certain threshold compared to the max magnitude
    max_y = np.max(y_f)
    threshold = 0.35 * max_y
    max_index = 0
    for i in range(len(y_f)):
        if y_f[i] > threshold:
            max_index = i
    
    max_f = x_f[max_index]

    # return the frequency of the maximum value
    return max_f



def adaptive_sampling(data, W, c, h, F_sampling):
    
    # estimate F max looking at the first W samples

    # The algorithm initially estimates, through a Fast
    # Fourier Transform (FFT), the maximum frequency
    # maxF of the signal by relying on the first W samples
    # coming from the process (e.g., W =400 samples). The
    # estimated maxF
    F_max = max_frequency(data, 0, W, F_sampling)
    F_c = c * F_max
    F_up = (1 + (c - 2) / 4) * F_max
    F_down = (1 - (c - 2) / 4) * F_max

    h1 = 0
    h2 = 0
    # initial sampling frequency at sample 0 is F_c

    for i in range(W, len(data)):

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
            print("New period: ", 1 / F_c)





data = pd.read_csv('datasets/0A986513-7828-4D53-AA1F-E02D6DF9561B.features_labels.csv', header=0, sep=',')


# the time stamps are the first column of the dataframe so we can calculate the sampling frequency
F_sampling = 1 / (data.iloc[1,0] - data.iloc[0,0])
# pass the second column of the dataframe as the data (raw accelerometer data)
adaptive_sampling(data.iloc[:, 1], 400, 2.1, 20, F_sampling)



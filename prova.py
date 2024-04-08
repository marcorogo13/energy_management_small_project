
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from data_reconstruct import interpol_data

DEBUG = False

def max_frequency(data, start, W, F_sampling):
    data_actual = data[start:start + W]
    N = len(data_actual)
    sampling_period = 1/F_sampling

    y_f = np.fft.fft(data_actual)
    y_f[0] = 0
    y_f = y_f/N
    y_f = np.abs(y_f)
    x_f = np.fft.fftfreq(N, sampling_period)



    max_mag = np.max(y_f)
    thr_mag = max_mag * 0.9
    max_f = 0.0

    for i in range(len(x_f)//2+1):
        if y_f[i] >= thr_mag:
            # 
            max_f = x_f[i]

    if DEBUG:
        
        print("Max frequency: ", max_f)
        plt.figure()
        plt.scatter(x_f, y_f)
        plt.draw()

    return max_f




def adaptive_sampling(data, W, c, h, F_sampling, new_data, new_t):


    F_max = max_frequency(data, 0, W, F_sampling)
    F_c = c * F_max
    F_up = (1 + (c - 2) / 4) * F_max
    F_down = (1 - (c - 2) / 4) * F_max

    h1 = 0
    h2 = 0

    print ("Initial frequency: ", F_max, "initial Period: ", 1/F_max)


    for z in range(W):
        new_data.append(data[z])
        new_t.append(z/F_sampling)

    i = W
    j = i
    while True:

        F_max_curr = max_frequency(data, i - W, W, F_sampling) # estimate the frequency of the current window

        # if abs(F_max_curr - F_up) < abs(F_max_curr - F_max):
        #     h1 += 1
        #     h2 = 0
        # elif abs(F_max_curr - F_down) < abs(F_max_curr - F_max):
        #     h2 += 1
        #     h1 = 0
        
        if F_max_curr > 1.1 * F_max:
            h1 += 1
            h2 = 0
        elif F_max_curr < 0.9 * F_max:
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
            # at sample i change the frequency to F_c
            print("New frequency: ", F_c, " at time: ", i/F_sampling)
            # can skip the next new_period samples for the new data

        period = 1/F_c 
        normalized_period = period / (1 / F_sampling)
        if (normalized_period < 1):
            normalized_period = 1
        
        j = i + int(normalized_period)
        print("j: ", j, "normalized period: ", normalized_period, "period: ", period, "F_c: ", F_c, "F_max: ", F_max, "F_max_curr: ", F_max_curr, "F_up: ", F_up, "F_down: ", F_down, "h1: ", h1, "h2: ", h2)
        i = j
        

        if(i >= len(data)):
            break
        new_data.append(data[j])
        new_t.append(j/F_sampling)






# h value
h = 5
# initial window size
W = 120
# confidence parameter
c = 2.2
# sampling frequency
sample_frequency = 100

signal_duration = 20 # seconds
signal_duration_ = 10 # seconds
signal_frequency = 4.2 # Hz

# sin wave with two components, one with frequency 1 and the other with frequency 2, 1000 samples with a sampling frequency of 100 Hz
t = np.linspace(0, signal_duration, sample_frequency * signal_duration)
data = np.sin(2 * np.pi * signal_frequency * t)

data_ = np.sin(2 * np.pi * signal_frequency/2 * t)


t_ = np.linspace(0, signal_duration_, sample_frequency * signal_duration_)
data__ = np.sin(2 * np.pi * signal_frequency*2 * t_)

data = np.concatenate((data, data_))
t = np.linspace(0, 2*signal_duration, sample_frequency * signal_duration * 2)

data = np.concatenate((data, data__))
t = np.linspace(0, 2*signal_duration + signal_duration_, sample_frequency * (signal_duration * 2 + signal_duration_))


plt.figure()
plt.plot(t, data, )
plt.grid(True)
plt.draw()

new_data = []
new_t = []
adaptive_sampling(data, W, c, h, sample_frequency, new_data, new_t)

interp_data = interpol_data(new_data, new_t, t)

plt.scatter(new_t, new_data)
plt.grid(True)
plt.draw()

plt.plot(t, interp_data)
plt.grid(True)
plt.draw()

#max_frequency(data, 420, W, sample_frequency)
#max_f = max_frequency(data, 0, W, sample_frequency)
plt.show()
# print("Max frequency: ", max_f)

print("Data sizes:")
print("Original data: ", len(data))
print("New data: ", len(new_data))
import numpy as np
import pandas as pd

# W is the initial windows size while c a confidence parameter
# data is a pandas dataframe
def max_frequency(data, start, W, c):
    fft_data = np.fft.fft(data[start:W+start])  # Compute FFT of the data (first W samples
    fft_data[0] = 0  # Remove the DC component
    F_max_pos = np.argmax(np.abs(fft_data))  # Find the maximum frequency position
    F_max = fft_data[F_max_pos]  # Find the maximum frequency
    F_max = np.abs(F_max)  # Get the absolute value of the maximum frequency
    return F_max

def adaptive_sampling(data, W, c, h):
    
    # estimate F max looking at the first W samples

    # The algorithm initially estimates, through a Fast
    # Fourier Transform (FFT), the maximum frequency
    # maxF of the signal by relying on the first W samples
    # coming from the process (e.g., W =400 samples). The
    # estimated maxF
    F_max = max_frequency(data, 0, W, c)
    F_c = c * F_max
    F_up = (1 + (c - 2) / 4) * F_max
    F_down = (1 - (c - 2) / 4) * F_max

    h1 = 0
    h2 = 0
    sampled_indices = []

    for i in range(W, len(data)):
        F__max_curr = max_frequency(data, i - W, W, c) 
        if abs(F__max_curr - F_up) < abs(F__max_curr - F_max):
            h1 += 1
            h2 = 0
        elif abs(F__max_curr - F_up) < abs(F__max_curr - F_max):
            h2 += 1
            h1 = 0
        else:
            h1 = 0
            h2 = 0

        if (h1 > h or h2 > h):
            F_c = c * F__max_curr
            F_up = (1 + (c - 2) / 4) * F__max_curr
            F_down = (1 - (c - 2) / 4) * F__max_curr
            # print new F_up and F_down
        sampled_indices.append(i)

    return np.array(sampled_indices)



data = pd.read_csv('0A986513-7828-4D53-AA1F-E02D6DF9561B.features_labels.csv', header=0, sep=',')

# pass the second column of the dataframe as the data to the adaptive sampling algorithm
adaptive_sampling(data.iloc[:, 1], 400, 2.1, 20)
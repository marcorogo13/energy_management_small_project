
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt


# create pandas dataframe with time column and data column 

time = np.arange(0, 10, 0.001)
data = np.ones(len(time))

df = pd.DataFrame(data, columns=['data'])
df['time'] = time






#fourier transform of data 
y_f = np.fft.fft(df['data'])
x_f = np.fft.fftfreq(len(df['data']), 1 / 0.001)


plt.plot(x_f, y_f)
plt.show()
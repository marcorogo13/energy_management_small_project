import numpy as np  


def interpol_data(y_values, x_values, x_new):

    y_new = np.interp(x_new, x_values, y_values)
    
    return y_new


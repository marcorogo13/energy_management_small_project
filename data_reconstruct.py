import numpy as np  


def interpol_data(y_values, x_values, x_new):
    """
    Interpolate the data to a new set of x values.
    
    Parameters:
    y_values: array
        Original y values.
    x_values: array
        Original x values.
    x_new: array
        New x values.
        
    Returns:
    y_new: array
        New y values.
    """
    
    y_new = np.interp(x_new, x_values, y_values)
    
    return y_new
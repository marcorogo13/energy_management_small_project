
import numpy as np

def mean_relative_error (y_orig, y_recon, N):
    """
    Calculate the mean relative error between two arrays.
    
    Parameters:
    y_orig: array
        Original array.
    y_recov: array
        Reconstructed array.
        
    Returns:
    mre: float
        Mean relative error.
    """
    sum = 0 
    mre = 0
    for i in range(N):
        if(np.abs(y_orig[i]) != 0):
            sum = sum + np.abs(y_recon[i] - y_orig[i]) / max(np.abs(y_orig[i]), np.abs(y_recon[i]))

    mre = sum / N
    return mre
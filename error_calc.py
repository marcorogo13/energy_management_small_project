
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
    
    for i in range(N):
        sum = np.abs(y_recon[i] - y_orig[i]) / np.abs(y_orig[i])
    
    mre = sum / N
    
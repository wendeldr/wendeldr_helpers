import numpy as np

def tukey_outlier(array, wiskerlength=5):
    array = np.array(array)
    nanlessarray = array[np.isfinite(array)]
    q25 = np.quantile(nanlessarray, 0.25)
    q50 = np.quantile(nanlessarray, 0.5)
    q75 = np.quantile(nanlessarray, 0.75)
    lower_bound = q25 - 2 * wiskerlength * (q50 - q25)
    upper_bound = q75 + 2 * wiskerlength * (q75 - q50)

    return ((array < lower_bound) | (array > upper_bound) | ~np.isfinite(array))
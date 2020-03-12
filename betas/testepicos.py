import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, ifft
import pywt
import pandas as pd
import peakutils
from scipy.signal import find_peaks


def ___main___():

    #Abrindo o arquivo com os dados ECG
    data = pd.read_csv("p000020-2183-04-28-17-471.csv", header=None)
    x = data[1:10000][1]  # Get the second column in the csv file
    x = x[0:10000]
    print(x)
    x = x.astype(int)
    # indices are the index of the points where peaks appear
    peaks = peakutils.indexes(x, thres=0.02 / max(x), min_dist=100)
    # [ 333  693 1234 1600]

    #interpolatedIndexes = peakutils.interpolate(range(0, len(x)), x, ind=peaks)
    # [  332.61234263   694.94831376  1231.92840845  1600.52446335]
    #peaks, _ = find_peaks(x, height=0)
    print(peaks)
    plt.plot(x)
    plt.plot(peaks+1, x[peaks+1], "x")
    plt.plot(np.zeros_like(x), "--", color="gray")
    plt.show()
___main___()
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack
import pywt
import pandas as pd
import peakutils
from scipy.signal import find_peaks
import hashlib


def plotarSF(xlabel, ylabel, data):
    plt.title(xlabel+' X '+ylabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(np.arange(len(data)), data)
    plt.savefig('graficos/bruto.png')
    plt.show()

def plotar(xlabel, ylabel, data):
    plt.title(xlabel+' X '+ylabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.yticks(np.arange(100))
    #plt.plot(np.arange(len(data)), data)
    #print("\n\n\n")
    #print(data)
    #peaks, _ = find_peaks(data, height=3)
    #print("\n\n\n")
    #print(peaks)
    plt.plot(data)
    #plt.plot(peaks, data[peaks], "x")
    #plt.plot(np.zeros_like(data), "--", color="gray")
    plt.savefig('graficos/filtrado.png')
    plt.show()


def filtro(data, max, min):
    auxData = []
    for i in range(len(data)):
        if int(data[i]) < max and int(data[i]) > min:
            auxData.append(data[i])
    return np.array(auxData)

'''
def quantization(data, qBlocks, bits):
    f_s = 125
    qtDados = len(data)
    #print(data)
    qCoef = qtDados/qBlocks
    quantized_coeffs = []
        
    for key in data:
        sig = key * (2 ** bits - 1)
        sig = np.round(sig)
        sig = np.array(sig).astype(int)
        print(sig)
        quantized_coeffs.append(sig%16)
    quantized_coeffs = np.array(quantized_coeffs)

    print(quantized_coeffs)


    return  quantized_coeffs
    #quant = np.binary_repr(data/bits*8)


    #for i in range(len(data)):
    #    auxData.append(data[i])
    #return np.array(auxData)
'''

def quantization(data, qBlocks, bits):
    f_s = 125
    qtDados = len(data)
    # print(data)
    quantized_coeffs = []
    #data = np.split(data,qBlocks)
    #print(data)
    #print(len(data))
    for key in data:
        sig = key * (2 ** bits - 1)
        sig = np.round(sig)
        sig = np.array(sig).astype(int)
        #print(sig)
        quantized_coeffs.append(sig)
    quantized_coeffs = np.array(quantized_coeffs)

    #print(quantized_coeffs)
    w = quantized_coeffs%16
    #print(w)

    quant = np.binary_repr(w)
    print(quant)
    # for i in range(len(data)):
    #    auxData.append(data[i])
    # return np.array(auxData)
    return quantized_coeffs, w


def divideSamples(data, frequency, sec):
    auxData = []
    concat = []
    f = 10  # Frequency, in cycles per second, or Hertz
    f_s = frequency  # Sampling rate, or number of measurements per second
    for i in range(sec):
        for j in range(frequency):
            auxData.append(data[(i+1)*j])
        np.array(auxData)
        plt.plot(auxData)
        #plt.plot(peaks, data[peaks], "x")
        #plt.plot(np.zeros_like(data), "--", color="gray")
        plt.savefig('graficos/parte' + str(i) +'.png')
        plt.show()

        X = fftpack.fft(auxData, 128)
        #print(X)
        #print(len(X))
        concat = np.concatenate((concat,X[0:64]))

        freqs = fftpack.fftfreq(len(X)) * f_s
        fig, ax = plt.subplots()

        ax.stem(freqs, np.abs(X), use_line_collection=True)
        ax.set_xlabel('Frequency in Hertz [Hz]')
        ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
        ax.set_xlim(-f_s / 2, f_s / 2)
        ax.set_ylim(-5, 125)
        auxData.clear()
        plt.savefig('graficos/fftparte' + str(i) + '.png')
        plt.show()
    concat = np.array(concat)
    plt.plot(concat)
    # plt.plot(peaks, data[peaks], "x")
    # plt.plot(np.zeros_like(data), "--", color="gray")
    plt.savefig('graficos/fftcompleto.png')
    plt.show()
    #print(concat)
    #print(len(concat))

    return concat


def hamdist(str1, str2):
    """Count the # of differences between equal length strings str1 and str2"""

    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs


def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def ___main___():

    #Abrindo o arquivo com os dados ECG
    data = pd.read_csv("p000020-2183-04-28-17-47.csv", header=None)
    x = data[1:10000][1]  # Get the second column in the csv file
    x = np.array(x).astype(int)

    #Extraindo as linhas do arquivo

    print(x[1])
    plotarSF('Sample', 'II', x)
    data = filtro(x, 10, -10)
    plotar('Sample', 'II w/ Filter', data)
    data1 = np.array(data[100:725])
    data2 = np.array(data[225:850])

    concat1 = divideSamples(data1, 125, 5)
    #print(concat1)
    plt.plot(concat1)
    plt.savefig('graficos/concatenado.png')
    plt.show()

    concat2 = divideSamples(data2, 125, 5)
    quant1, w1 = quantization(concat1, 20, 4)
    plt.plot(quant1)
    plt.savefig('graficos/quantizado.png')
    plt.show()
    quant2, w2 = quantization(concat2, 20, 4)
    plt.plot(quant1)
    plt.plot(quant2)
    plt.savefig('graficos/cruzamento.png')
    plt.show()


    '''
    freqs = fftpack.fftfreq(len(quant1)) * 125
    fig, ax = plt.subplots()
    ax.stem(freqs, np.abs(quant1), use_line_collection=True)
    ax.set_xlabel('Frequency in Hertz [Hz]')
    ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
    ax.set_xlim(-125 / 2, 125 / 2)
    ax.set_ylim(-5, 20)
    plt.show()
    freqs = fftpack.fftfreq(len(quant2)) * 125
    fig, ax = plt.subplots()
    ax.stem(freqs, np.abs(quant2), use_line_collection=True)
    ax.set_xlabel('Frequency in Hertz [Hz]')
    ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
    ax.set_xlim(-125 / 2, 125 / 2)
    ax.set_ylim(-5, 20)
    plt.show()
    #plotar('Sample', 'II w/ Filter', data)
    #plotar('Sample', 'II w/ Filter Ordered', sample, sorted(data))
    '''
    '''
    plotar('Sample', 'AVF', sampleAVF, AVF)
    sample, data = filtro(sampleAVF, AVF, 50, -50)
    plotar('Sample', 'AVF w/ Filter', sample, data)
    #plotar('Sample', 'AVF w/ Filter Ordered', sample, sorted(data))

    plotar('Sample', 'ABP', sampleABP, ABP)
    sample, data = filtro(sampleABP, ABP, 150, 50)
    plotar('Sample', 'ABP w/ Filter', sample, data)
    #plotar('Sample', 'ABP w/ Filter Ordered', sample, sorted(data))

    plotar('Sample', 'PAP', samplePAP, PAP)
    sample, data = filtro(samplePAP, PAP, 150, 30)
    plotar('Sample', 'PAP w/ Filter', sample, data)
    #plotar('Sample', 'PAP w/ Filter Ordered', sample, sorted(data))
    '''

___main___()


'''
0  4  4  2 11 15  9  9 12  4 15 10 11 11 10 13  8 12 14  3  3 12 13 12
  8 15  5 14 14  8  3  4 13 14 15 14  6  8 11 12  0 11 10 13  6  3  8 12
 11  9 10 13 14  7  5 11  1 14  8 14  1 10  6  6 15  1  3  8  1 10 13 15
  8 15  7  4  6 10  8 11  7  5  8 10 13 13  9 11  3  8  2 11 14 10  5  7
 10  0  5  4  2 12  6  6 11  8  7  8  7 11 15 15  0 13  6 14 14 11 13 15
  1  6 10  1  3  7  4  4  0 15  6  5 11  7 10 13  0  5 13  1  3 14  0 15
  3  3 14  5 12 14  5  9 14  1  2  4 11  8 14 12 10 14  4 12  1 11  0  6
  9 10 15 12 12  4 10 15 10  9  3  8  3  6  1 12  3 14  7 15 11  5  1  1
 13  7  1  3  3 15  7  5  0  3  7  7  4  0  0  7 13 12  6  2 15  3  1  8
 12 10  2 15  2  1 12 15  9  8  5  3  9  7  6 12  0  0 11  1 15  4  8 11
 14  6  2  0  8 15  5  7 11  8 12 14  0 11 13 13  6  0  5  3  7  4  5 14
  6 10  6  3 14 11 12 11 14  2 14  2 10  2  3  6  3  8  8  0 14 12  8  0
  9  3 11  7 13  6 10 15  3 15  0 14 12 14  4 11  9  8 12 12  2  1  0  0
  2 13 10  6 11  4  0  0
  
1  6  4  6  1  5  6  0  4 13  1  7 10  3 13  3  6 15  2  4  7  3  4  4
  7 13  7 12  7  2  6  9  0 12  2  7  2  6  6 10  9 13  9 12 13  4 13  5
  9 10  9  7  6  2  1  9 11  9  1  3  9 10 15 15 15  3  9 11 12  6 12  1
 15  2 11  7 14  8  6 11 11 14 14  2 10  4 13 15  2  5 10  0  8  1  4 10
  2  6  8  1 13  5 10  7 10  5 13  4  4 10  8  3  5 11  9  5  5  4  1 13
  3  9  9  0 14 15  4  4 10  1  0 15 14 13 10  4  7 10 11 12  5  6 12 15
  1  4  7 15  6 11 13  9  2  4 15  7  1  8  5  1  3  9  1  5 11  9 14  9
 13  1  6 13 13  3 14  0 14 14  9  2 13 10 15 11 10  3  6  9  6  6 12 12
  0  3  7  1 10  9  5  4  7  8 12 12 12  2  3 11  2 11 11  8 13 15  1  9
  6  1  8 15  9  3  7  6 15 10 11  1  9  7  8  1 10  2 14 15  1 10  5 15
 12 10 13  9 14 13 13  6  4  2 14  3  8 14 14 14 15  3 12  7  2 13 13 15
 13 10  5  1 10  7  8  7  6  2 15  0 15  4  1 15  3  3  4  5  1  7  6 14
 15  1  4 14  2  7  1  1  4 11  3  7  5  3 11  3 15  8 15 12  4  2 14  0
  7  5 11 10  4 13 10 10

'''
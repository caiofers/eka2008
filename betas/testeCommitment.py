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
    plt.title(xlabel + ' X ' + ylabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(np.arange(len(data)), data)
    plt.savefig('graficos/bruto.png')
    #plt.show()


def plotar(xlabel, ylabel, data):
    plt.title(xlabel + ' X ' + ylabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.yticks(np.arange(100))
    # plt.plot(np.arange(len(data)), data)
    # print("\n\n\n")
    # print(data)
    # peaks, _ = find_peaks(data, height=3)
    # print("\n\n\n")
    # print(peaks)
    plt.plot(data)
    # plt.plot(peaks, data[peaks], "x")
    # plt.plot(np.zeros_like(data), "--", color="gray")
    plt.savefig('graficos/filtrado.png')
    #plt.show()


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
    # data = np.split(data,qBlocks)
    # print(data)
    # print(len(data))
    for key in data:
        sig = key * (2 ** bits - 1)
        sig = np.round(sig)
        sig = np.array(sig).astype(int)
        # print(sig)
        quantized_coeffs.append(sig)
    quantized_coeffs = np.array(quantized_coeffs)

    # print(quantized_coeffs)
    w = quantized_coeffs % 16
    # print(w)
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
            auxData.append(data[(i + 1) * j])
        np.array(auxData)
        plt.plot(auxData)
        # plt.plot(peaks, data[peaks], "x")
        # plt.plot(np.zeros_like(data), "--", color="gray")
        plt.savefig('graficos/parte' + str(i) + '.png')
        #plt.show()

        X = fftpack.fft(auxData, 128)
        # print(X)
        # print(len(X))
        concat = np.concatenate((concat, X[0:64]))

        freqs = fftpack.fftfreq(len(X)) * f_s
        fig, ax = plt.subplots()

        ax.stem(freqs, np.abs(X), use_line_collection=True)
        ax.set_xlabel('Frequency in Hertz [Hz]')
        ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
        ax.set_xlim(-f_s / 2, f_s / 2)
        ax.set_ylim(-5, 125)
        auxData.clear()
        plt.savefig('graficos/fftparte' + str(i) + '.png')
        #plt.show()
    concat = np.array(concat)
    plt.plot(concat)
    # plt.plot(peaks, data[peaks], "x")
    # plt.plot(np.zeros_like(data), "--", color="gray")
    plt.savefig('graficos/fftcompleto.png')
    #plt.show()
    # print(concat)
    # print(len(concat))

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

def binaryRep(matriz):
    binaryMat = []
    for i in matriz:
        binaryMat.append(np.binary_repr(i, width=4))
    print(binaryMat)
    return binaryMat

def ___main___():
    # Abrindo o arquivo com os dados ECG
    data = pd.read_csv("p000020-2183-04-28-17-47.csv", header=None)
    x = data[1:10000][1]  # Get the second column in the csv file
    x = np.array(x).astype(int)

    # Extraindo as linhas do arquivo

    print(x[1])
    plotarSF('Sample', 'II', x)
    data = filtro(x, 10, -10)
    plotar('Sample', 'II w/ Filter', data)
    data1 = np.array(data[100:725])
    data2 = np.array(data[100:725])
    #data2 = np.array(data[225:850])

    concat1 = divideSamples(data1, 125, 5)
    # print(concat1)
    plt.plot(concat1)
    plt.savefig('graficos/concatenado.png')
    #plt.show()

    concat2 = divideSamples(data2, 125, 5)
    quant1, w1 = quantization(concat1, 20, 4)
    plt.plot(quant1)
    plt.savefig('graficos/quantizado.png')
    #plt.show()
    quant2, w2 = quantization(concat2, 20, 4)
    plt.plot(quant1)
    plt.plot(quant2)
    plt.savefig('graficos/cruzamento.png')
    #plt.show()

    binW1 = binaryRep(w1)
    binW2 = binaryRep(w2)

    binW1 = np.split(np.array(binW1), 20)
    binW2 = np.split(np.array(binW2), 20)
    np.array(binW1)

    matrizU = []
    matrizV = []
    for i in binW1:
        #print(i)
        i = ''.join(i)
        #print(i)
        matrizU.append(encrypt_string(i))
    for i in binW2:
        #print(i)
        i = ''.join(i)
        #print(i)
        matrizV.append(encrypt_string(i))
    print(matrizU)
    print(matrizV)

    matrizW = []
    for i in range(20):
        for j in range(20):
            matrizW.append(hamdist(matrizU[i], matrizV[j]))

    print(matrizW)

    '''
    freqs = fftpack.fftfreq(len(quant1)) * 125
    fig, ax = plt.subplots()
    ax.stem(freqs, np.abs(quant1), use_line_collection=True)
    ax.set_xlabel('Frequency in Hertz [Hz]')
    ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
    ax.set_xlim(-125 / 2, 125 / 2)
    ax.set_ylim(-5, 20)
    #plt.show()
    freqs = fftpack.fftfreq(len(quant2)) * 125
    fig, ax = plt.subplots()
    ax.stem(freqs, np.abs(quant2), use_line_collection=True)
    ax.set_xlabel('Frequency in Hertz [Hz]')
    ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
    ax.set_xlim(-125 / 2, 125 / 2)
    ax.set_ylim(-5, 20)
    #plt.show()
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

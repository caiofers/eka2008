import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft, ifft
import pywt

import pandas as pd

def plotar(xlabel, ylabel, samples, data):
    plt.title(xlabel+' X '+ylabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.yticks(np.arange(100))
    plt.plot(np.arange(len(samples)), data)
    print("\n\n\n")
    print(data)
    #plt.plot(pywt.threshold(data, 0.5, 'soft'))
    '''
    # Number of sample points
    N = len(data)
    # sample spacing
    T = 1.0
    x = np.linspace(0.0, N * T, N)
    y = np.sin(50.0 * 2.0 * np.pi * x) + 0.5 * np.sin(80.0 * 2.0 * np.pi * x)
    yf = fft(y)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    plt.plot(xf, 2.0 / N * np.abs(yf[0:N // 2]))
    '''
    # (cA, cD) = pywt.dwt(data, 'db1')
    # plt.plot(pywt.threshold(cA, 0.5, 'soft'))
    # print(cA)
    plt.show()

def filtro(samples, data, max, min):
    auxSamples = []
    auxData = []
    for i in range(len(data)):
        if int(data[i]) < max and int(data[i]) > min:
            auxSamples.append(samples[i])
            auxData.append(data[i])

    #data.clear()
    #samples.clear()
    #samples = auxSamples
    #data = auxData
    return auxSamples, auxData

def ___main___():

    #Abrindo o arquivo com os dados ECG
    arquivo = open('p000020-2183-04-28-17-47.csv')

    #Extraindo as linhas do arquivo
    linhas = csv.reader(arquivo)

    #Inicializando as listas
    sampleII = []
    sampleAVF = []
    sampleABP = []
    samplePAP = []
    II = []
    AVF = []
    ABP = []
    PAP = []
    i = 0
    for linha in linhas:
        if i != 0:
                sampleII.append(int(linha[0]))
                sampleAVF.append(int(linha[0]))
                sampleABP.append(int(linha[0]))
                samplePAP.append(int(linha[0]))

                II.append(int(linha[1]))
                AVF.append(int(linha[2]))
                ABP.append(int(linha[3]))
                PAP.append(int(linha[4]))
                #if len(sample) > 300:
                #    break
        i = i + 1
        print(linha)

    plotar('Sample', 'II', sampleII, II)
    sample, data = filtro(sampleII, II, 10, -10)
    plotar('Sample', 'II w/ Filter', sample, data)
    #plotar('Sample', 'II w/ Filter Ordered', sample, sorted(data))
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
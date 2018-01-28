import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.polynomial.polynomial import Polynomial


import filterEKG
import featsEKG
import plotEKG



def ___main___():
    # Abrindo o arquivo com os dados ECG
    data = pd.read_csv("p000020-2183-04-28-17-47.csv", header=None)
    
    # Extraindo as linhas do arquivo, pegando a segunda coluna (II - ECG)
    x = data[1:10000][1]
    x = np.array(x).astype(int)

    #Definindo máx e min dos dados para filtar
    vMin = -10
    vMax = 10

    # Aplicando filtro nos dados
    data = filterEKG.filterEKG(x, vMin, vMax)

     # Definindo frequencia e quantidade de tempo para coleta das amostras
    frequency = 125
    seconds = 5

    # Definindo numero de blocos
    nBlocks = 20

    vault, key = sender(data, nBlocks, frequency, seconds, vMin, vMax)
    #receiver(vault, key, data, frequency, seconds, vMin, vMax, nBlocks)


def sender(data, nBlocks, frequency, seconds, vMin, vMax):

    # Pegando 625 amostras dos dados filtrados (125hz durante 5 segundos) 
    data1 = np.array(data[100:725])
    
    # Dividindo as amostras em 5 janelas de 125 amostras (1 janela para cada segundo) 
    division = featsEKG.divideSamples(data1, frequency, seconds)

    # Cálculo das características
    featVectorBin1, featVectorInt1 = featsEKG.calcFeats(division, nBlocks, frequency)


    return featVectorBin1, featVectorInt1


def receiver(vault, key, data, frequency, seconds, vMin, vMax, nBlocks):
    # Pegando mais 625 amostras dos dados filtrados (Simulando a parte do receptor)
    data2 = np.array(data[110:740])

    # Dividindo as amostras em 5 janelas de 125 amostras (1 janela para cada segundo) 
    division = featsEKG.divideSamples(data2, frequency, seconds)

    # Cálculo das características
    featVectorBin2, featVectorInt2 = featsEKG.calcFeats(division, nBlocks, frequency)


    if ():
        print("Accepted")
    else:
        print("Not Accepted")




___main___()
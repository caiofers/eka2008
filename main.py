import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import hashlib


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

    featVectorBinSender = senderFeats(data, nBlocks, frequency, seconds, vMin, vMax)
    featVectorBinReceiver = receiverFeats(data, nBlocks, frequency, seconds, vMin, vMax)

    resultWSender = commitmentPhase(featVectorBinSender, featVectorBinReceiver)
    resultWReceiver = commitmentPhase(featVectorBinSender, featVectorBinReceiver)

    keySender = keyGen(resultWSender, featVectorBinSender)
    keyReceiver = keyGen(resultWReceiver, featVectorBinReceiver)


def senderFeats(data, nBlocks, frequency, seconds, vMin, vMax):

    # Pegando 625 amostras dos dados filtrados (125hz durante 5 segundos) 
    data1 = np.array(data[100:725])
    
    # Dividindo as amostras em 5 janelas de 125 amostras (1 janela para cada segundo) 
    division = featsEKG.divideSamples(data1, frequency, seconds)

    # Cálculo das características
    featVectorBin1 = featsEKG.calcFeats(division, nBlocks, frequency)

    return featVectorBin1


def receiverFeats(data, nBlocks, frequency, seconds, vMin, vMax):
    # Pegando mais 625 amostras dos dados filtrados (Simulando a parte do receptor)
    data2 = np.array(data[100:725])

    # Dividindo as amostras em 5 janelas de 125 amostras (1 janela para cada segundo) 
    division = featsEKG.divideSamples(data2, frequency, seconds)

    # Cálculo das características
    featVectorBin2 = featsEKG.calcFeats(division, nBlocks, frequency)

    return featVectorBin2

def commitmentPhase(featVectorBinSender, featVectorBinReceiver):
    matrizU = []
    matrizV = []
    for i in featVectorBinSender:
        matrizU.append(encrypt_string(i))
    for i in featVectorBinReceiver:
        matrizV.append(encrypt_string(i))
    matrizW = []
    for i in range(20):
        listaW = []
        for j in range(20):
            listaW.append(hamdist(matrizU[i], matrizV[j]))
        matrizW.append(listaW)
    return matrizW

def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def hamdist(str1, str2):
    """Count the # of differences between equal length strings str1 and str2"""

    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs

def keyGen(resultW, feats):
    keyMatList = []
    while(verificarMatrizW(resultW)):
        minElement, minI, minJ = positionMinMatriz(resultW)
        if(minElement == 0):
            keyMatList.append(feats[minI])
            for k in range(len(resultW[minI])):
                resultW[minI][k] = 1
            for u in range(len(resultW)):
                resultW[u][minJ] = 1
        else:
            pass
    print("KeyMat")
    keyMat = []
    #for element in KeyMatList:
    #    for el in element:

    #    element = ''.join(str(element))
    #    print(element)
    keyMatList = ''.join(keyMatList)
    return encrypt_string(keyMatList)

def verificarMatrizW(resultW):
    for i in resultW:
        for j in i:
            if j != 1:
                return True
    return False

def positionMinMatriz(resultW):
    minI = 0
    minJ = 0
    minElement = resultW[minI][minJ]
    for i in range(len(resultW)):
        for j in range(len(resultW[i])):
            if resultW[i][j] < 1:
                minElement = resultW[i][j]
                minI = i
                minJ = j
    return minElement, minI, minJ
___main___()
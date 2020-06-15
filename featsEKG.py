import matplotlib.pyplot as plt
import numpy as np

import quantizationEKG
import fftEKG

def calcFeats(division, nBlocks, frequency, verbose=False, plot=False, save=False):
    featVectorBin = []
    index = 0

    if verbose: print("\nCALCÚLO DAS FEATS - START")

    for data in division:
        # Aplicando Fast Fourier Transform para 128 pontos
        X = fftEKG.fftAply(data, 128, frequency)

        # Definindo numero de bits da quantização
        nQuantBits = 4

        #Aplicando a quantização para discretizar os pontos
        quantizedArray = quantizationEKG.quantization(X, nQuantBits, verbose=verbose)

        if plot:
            plt.plot(quantizedArray)
            if save: plt.savefig('graficos/quantpeaks' + str(index) + '.png')
            plt.show()
            index = index + 1

        # Construindo vetor de caracteristicas com cada ponto (Cada ponto resulta em 4 bits)
        for k in range(len(quantizedArray)):
            featVectorBin.append(np.binary_repr(quantizedArray[k], width=4))

    if verbose:
        print("Vetor de características (binário): ")
        print(featVectorBin)
        print("\nCALCÚLO DAS FEATS - END")

    blocksBin = []

    lenFeats = len(featVectorBin)
    for i in range(nBlocks):
        start = int(i*lenFeats/nBlocks)
        end = int((i+1)*lenFeats/nBlocks)
        blocksBin.append(''.join(featVectorBin[start:end]))
    print("blocksBin")
    print(blocksBin)
    return blocksBin


def divideSamples(data, frequency, sec):
    auxData = []
    division = []
    #Dividindo as amostras em janelas (sec é a quantidade de segundos/janelas)
    for i in range(sec):
        for j in range(frequency): #(frequency é a quantidade de amostras que tem em cada segundo)
            auxData.append(data[(i + 1) * j])
        np.array(auxData)
        division.append(auxData.copy())
        auxData.clear()
    return division


def converterb_d(n):
    decimal = 0
    n = str(n)
    n = n[::-1]
    tam = len(n)
    for i in range(tam):
        if n[i] == "1":
            decimal = decimal + 2**i
    return decimal
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from scipy import signal
import pandas as pd
import hashlib
import random
import hmac
import base64
import binascii

class Sensor:

    # Inicialização do sensor com número de bloco e ID
    def __init__(self, frequency, seconds, numberOfBlocks, IDSensor):
        self.__frequency = frequency
        self.__seconds = seconds
        self.__numberOfBlocks = numberOfBlocks
        self.__IDSensor = IDSensor
        self.__verbose = False
        self.__plot = False
        self.__savePlot = False
    
    def setVerbose(self, verbose=False):
        self.__verbose = verbose
    
    def setPlot(self, plot=False, savePlot=False):
        self.__plot = plot
        self.__savePlot = savePlot

    def extractFeats(self, record):
        data =[]
        for i in range(len(record.d_signal)):
            data.extend(record.d_signal[i])

        # Pegando amostras dos dados 
        data = data[0:(self.__frequency*self.__seconds)]

        # Aplicando filtro nos dados
        data = np.array(self.__filter(data))

        # Dividindo os dados filtrados em janelas
        division = self.__divideSamples(data)

        # Cálculo das características
        self.__featsVectorBin = self.__calcFeats(division)
        return self.__featsVectorBin

    def __filter(self, data):
        b, a = signal.butter(3, 0.05)
        filtered = signal.filtfilt(b, a, data)
    
        if self.__verbose:
            print("\nDados sem filtro: ")
            print(data)
            print("\nDados filtrados: ")
            print(filtered)

        if self.__plot:
            self.__plotPy('Sample', 'Signal', data)
            self.__plotPy('Sample', 'Signal w/ Filter', filtered)

        return filtered

    def __plotPy(self, xlabel, ylabel, data):
        plt.title(xlabel + ' X ' + ylabel)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.plot(data)
        if self.__savePlot: plt.savefig('graficos/filtrado.png')
        plt.show()

        plt.plot(np.arange(len(data)), data)
        if self.__savePlot: plt.savefig('graficos/bruto.png')
        plt.show()

    def __divideSamples(self, data):
        auxData = []
        division = []

        #Definindo numero de janelas
        numOfWindows = 8

        #Dividindo as amostras em janelas de controlada 
        for i in range(numOfWindows):
            for j in range(int(len(data)/numOfWindows)):
                auxData.append(data[(i + 1) * j])
            np.array(auxData)
            division.append(auxData.copy())
            auxData.clear()

        return division

    def __calcFeats(self, division):
        featVectorBin = []
        index = 0

        if self.__verbose: print("\nCALCÚLO DAS FEATS - INÍCIO")

        for data in division:
            # Aplicando Fast Fourier Transform para 128 pontos
            X = self.__fftAply(data, 128, index)

            # Definindo numero de bits da quantização
            nQuantBits = 4

            #Aplicando a quantização para discretizar os pontos
            quantizedArray = self.__quantization(X, nQuantBits)

            if self.__plot:
                plt.plot(quantizedArray)
                if self.__savePlot: plt.savefig('graficos/quantpeaks' + str(index) + '.png')
                plt.show()
                index = index + 1

            # Construindo vetor de caracteristicas com cada ponto (Cada ponto resulta em 4 bits)
            for k in range(len(quantizedArray)):
                featVectorBin.append(np.binary_repr(quantizedArray[k], width=4))

        if self.__verbose:
            print("Vetor de características (binário): ")
            print(featVectorBin)
            print("\nCALCÚLO DAS FEATS - FIM")

        return featVectorBin

        
    
    def __fftAply(self, data, nOfPoints, index=None):
        if self.__verbose: print("\nFFT - INÍCIO")
        
        # Aplicando Fast Fourier Transform para 128 pontos
        X = fftpack.fft(data, n=nOfPoints)

        #Coletando a metade dos pontos da FFT, já que os pontos tem caracteristica espelhada
        X = X[0:64]

        if self.__verbose:
            print("\nPontos da FFT:")
            print(X)
            print("\nFFT - FIM\n")

        if self.__plot:
            freqs = fftpack.fftfreq(len(X)) * self.__frequency
            __, ax = plt.subplots()

            ax.stem(freqs, np.abs(X), use_line_collection=True)
            ax.set_xlabel('Frequency in Hertz [Hz]')
            ax.set_ylabel('Frequency Domain (Spectrum) Magnitude')
            ax.set_xlim(-self.__frequency / 2, self.__frequency / 2)
            ax.set_ylim(-5, 125)
            if self.__savePlot: plt.savefig('graficos/fftfreqparte' + str(index) + '.png')
            plt.show()

            plt.plot(X)
            if self.__savePlot: plt.savefig('graficos/fftparte' + str(index) + '.png')
            plt.show()

        return X
    
    def __quantization(self, data, nQuantBits):
        if self.__verbose: print("\nQUANTIZAÇÃO - INÍCIO")
        
        # Definindo limite superior e inferior dos dados a serem quantizados
        vMax = max(data)
        vMin = min(data)

        # Criação de uma lista vazia para armazenar os coeficientes quantizados
        quantized_coeffs = []

        # Definindo o número de níveis de acordo com a quantidade de bits
        nLevels = 2^nQuantBits

        # Definindo distância entre os níveis
        distLevels = (vMax-vMin)/nLevels

        # Quantização de cada um dos valores da lista de dados 
        for key in data:
            level = 0
            limiar = vMin+(level+1)*distLevels
            while(key > limiar and limiar < vMax):
                level = level + 1
                limiar = vMin+(level+1)*distLevels
            quantized_coeffs.append(level)

        if self.__verbose:
            print("\nDados:")
            print(data)
            print("\nDados Quantizados:")
            print(quantized_coeffs)
            print("\nQUANTIZAÇÃO - FIM\n")
        
        return quantized_coeffs
    
    def getCommitmentMessage(self):
        # Criação da mensagem de compromisso
        message = {}
        self.__keyPrivate = random.getrandbits(128)
        self.__createBlocks()
        self.__hashBlocks()
        self.__Nounce = random.randint(0, 100)
        message["ID"] = self.__IDSensor
        message["Nounce"] = self.__Nounce
        message["HASHEDBLOCKS"] = self.__matrixU
        message["MAC"] = self.__macHMAC(str(self.__IDSensor)+str(self.__Nounce)+str(self.__matrixU), str(self.__keyPrivate))
        return message

    # Dividindo as características em blocos
    def __createBlocks(self):
        blocksBin = []

        lenFeats = len(self.__featsVectorBin)
        for i in range(self.__numberOfBlocks):
            start = int(i*lenFeats/self.__numberOfBlocks)
            end = int((i+1)*lenFeats/self.__numberOfBlocks)
            blocksBin.append(''.join(self.__featsVectorBin[start:end]))

        if self.__verbose:
            print("\nCRIAÇÃO DOS BLOCOS - INÍCIO")
            for i in range(self.__numberOfBlocks):
                print("Bloco:" + str(i+1))
                print(blocksBin[i])
            print("\nCALCÚLO DAS FEATS - FIM")

        self.__blocksBin = blocksBin

        return blocksBin

    # Gerando uma matriz de hash dos blocos
    def __hashBlocks(self):
        self.__matrixU = []
        for i in self.__blocksBin:
            self.__matrixU.append(self.__hashSHA256(i))
        
        return self.__matrixU
    
    def __hashSHA256(self, hash_string):
        sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature
    
    # Geração da Message Authentication Code (MAC) com HMAC
    def __macHMAC(self, message, key):
        key = bytes(key, 'UTF-8')
        message = bytes(message, 'UTF-8')
        digester = hmac.new(key, message, hashlib.sha1)
        signature1 = digester.digest()
        signature2 = base64.urlsafe_b64encode(signature1)
        
        return str(signature2, 'UTF-8')

    # Desmembrando a mensagem de compromisso recebida do outro sensor
    def receiveCommitmentMessage(self, message):
        self.__IDReceived = message["ID"] 
        self.__NounceReceived = message["Nounce"]
        self.__matrixV = message["HASHEDBLOCKS"]
        self.__receivedCommitmentMAC = message["MAC"]

    # Gerando a chave comum
    def processCommomKey(self):
        matrixW = self.__calcMatrixW(self.__matrixV)
        self.__keyCommon = self.__keyGen(matrixW)

    def __calcMatrixW(self, matrixV):
        matrixW = []
        for i in range(self.__numberOfBlocks):
            listW = []
            for j in range(self.__numberOfBlocks):
                listW.append(self.__hammingDistance(self.__matrixU[i], matrixV[j]))
            matrixW.append(listW)
        return matrixW
    
    def __hammingDistance(self, str1, str2):
        diffs = 0
        for ch1, ch2 in zip(str1, str2):
            if ch1 != ch2:
                diffs += 1
        return diffs

    def __keyGen(self, matrixW):
        keyMatList = []
        while(self.__checkMatrixW(matrixW)):
            minElement, minI, minJ = self.__positionMinMatriz(matrixW)
            if(minElement == 0):
                keyMatList.append(self.__blocksBin[minI])
                for k in range(len(matrixW[minI])):
                    matrixW[minI][k] = 1
                for u in range(len(matrixW)):
                    matrixW[u][minJ] = 1
            else:
                return self.__hashSHA256('error')
        keyMatList = ''.join(keyMatList)
        return self.__hashSHA256(keyMatList)

    def __checkMatrixW(self, matrixW):
        for i in matrixW:
            for j in i:
                if j != 1:
                    return True
        return False

    def __positionMinMatriz(self, matrixW):
        minI = 0
        minJ = 0
        minElement = matrixW[minI][minJ]
        for i in range(len(matrixW)):
            for j in range(len(matrixW[i])):
                if matrixW[i][j] < minElement:
                    minElement = matrixW[i][j]
                    minI = i
                    minJ = j
        return minElement, minI, minJ
    
    # Gerando a mensagem de descompromisso
    def getDecommitmentMessage(self):
        message = {}
        G = np.bitwise_xor(self.__keyPrivate, int(self.__keyCommon, 16))
        message["G"] = G
        message["MAC"] = self.__macHMAC(str(G), str(int(self.__keyCommon, 16)))
        return message

    # Desmembrando a mensagem de descompromisso 
    def receiveDecommitmentMessage(self, message):
        receivedDecommitmentG = message["G"]
        receivedDecommitmentMAC = message["MAC"]
        return self.__checkMAC(receivedDecommitmentG, receivedDecommitmentMAC)
    
    # Checando o MAC recebido
    def __checkMAC(self, receivedDecommitmentG, receivedDecommitmentMAC):
        if(self.__keyCommon != self.__hashSHA256('error')):
            checkMAC1 = self.__macHMAC(str(receivedDecommitmentG), str(int(self.__keyCommon, 16)))
            if(checkMAC1 == receivedDecommitmentMAC):
                keyPrivateReceived = np.bitwise_xor(receivedDecommitmentG, int(self.__keyCommon, 16))
                checkMAC2 = self.__macHMAC(str(self.__IDReceived)+str(self.__NounceReceived)+str(self.__matrixV), str(keyPrivateReceived))
                if(checkMAC2 == self.__receivedCommitmentMAC):
                    #print("Accepted")
                    return True
                else:
                    #print("Not Accepted")
                    return False
            else:
                    #print("Not Accepted")
                    return False
        else:
           #print("Not Accepted")
            return False 
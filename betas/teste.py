from scipy.fftpack import fft
import numpy as np
import csv



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
            sampleII.append(linha[0])
            sampleAVF.append(linha[0])
            sampleABP.append(linha[0])
            samplePAP.append(linha[0])

            II.append(linha[1])
            AVF.append(linha[2])
            ABP.append(linha[3])
            PAP.append(linha[4])
            #if len(sample) > 300:
            #    break
    i = i + 1

# Number of sample points
N = len(II)
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
yf = fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

import matplotlib.pyplot as plt
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.grid()
plt.show()
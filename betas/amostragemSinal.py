import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import peakutils
# Abrindo o arquivo com os dados ECG
arquivo = open('p000020-2183-04-28-17-471.csv')

# Extraindo as linhas do arquivo
linhas = csv.reader(arquivo)

# Inicializando as listas
sampleII = []
sampleAVF = []
sampleABP = []
samplePAP = []
x = []
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

        x.append(int(linha[1]))
        AVF.append(int(linha[2]))
        ABP.append(int(linha[3]))
        PAP.append(int(linha[4]))
        # if len(sample) > 300:
        #    break
    i = i + 1
x = np.array(x)
print(x)
# indices are the index of the points where peaks appear
peaks = peakutils.indexes(x, thres=0.02 / max(x), min_dist=100)
# [ 333  693 1234 1600]

#interpolatedIndexes = peakutils.interpolate(range(0, len(x)), x, ind=peaks)
# [  332.61234263   694.94831376  1231.92840845  1600.52446335]
#peaks, _ = find_peaks(x, height=0)
print(peaks)
plt.plot(x)
plt.plot(peaks, x[peaks], "x")
plt.plot(np.zeros_like(x), "--", color="gray")
plt.show()
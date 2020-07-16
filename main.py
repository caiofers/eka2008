import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import hashlib
from Sensor import Sensor

def main():
    frequency = 125
    seconds = 5
    numberOfBlocks = 20
    filterMin = -15
    filterMax = 15

    data = pd.read_csv("p000020-2183-04-28-17-471.csv", header=None)
    
    # Extraindo as linhas do arquivo, pegando a segunda coluna (II - ECG)
    data = data[1:10000][1]
    data = np.array(data).astype(int)

    sensorTransmitter = Sensor(frequency, seconds, numberOfBlocks, filterMin, filterMax)
    sensorTransmitter.extractFeats(data)

    sensorReceiver = Sensor(frequency, seconds, numberOfBlocks, filterMin, filterMax)
    sensorReceiver.extractFeats(data)

    sensorTransmitter.receiveCommitmentMessage(sensorReceiver.getCommitmentMessage())
    sensorReceiver.receiveCommitmentMessage(sensorTransmitter.getCommitmentMessage())

    sensorTransmitter.processCommomKey()
    sensorReceiver.processCommomKey()

    sensorTransmitter.receiveDecommitmentMessage(sensorReceiver.getDecommitmentMessage())
    sensorReceiver.receiveDecommitmentMessage(sensorTransmitter.getDecommitmentMessage())

main()
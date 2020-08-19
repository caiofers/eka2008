import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import hashlib
import wfdb

from Sensor import Sensor

def main():
    recordNum = 1
    recordTransmitter = wfdb.rdrecord('samples/'+str(recordNum), physical=False, sampfrom=0, channel_names=['avf'])
    recordReceiver = wfdb.rdrecord('samples/'+str(recordNum), physical=False, sampfrom=0, channel_names=['avf'])

    EKAPROTOCOL(recordTransmitter, recordReceiver)
    

def EKAPROTOCOL(recordTransmitter, recordReceiver):

    frequency = 125
    seconds = 5

    numberOfBlocks = 20

    sensorTransmitter = Sensor(frequency, seconds, numberOfBlocks)
    sensorReceiver = Sensor(frequency, seconds, numberOfBlocks)

    sensorTransmitter.extractFeats(recordTransmitter)
    sensorReceiver.extractFeats(recordReceiver)

    sensorTransmitter.receiveCommitmentMessage(sensorReceiver.getCommitmentMessage())
    sensorReceiver.receiveCommitmentMessage(sensorTransmitter.getCommitmentMessage())

    sensorTransmitter.processCommomKey()
    sensorReceiver.processCommomKey()

    sensorTransmitter.receiveDecommitmentMessage(sensorReceiver.getDecommitmentMessage())
    sensorReceiver.receiveDecommitmentMessage(sensorTransmitter.getDecommitmentMessage())
main()
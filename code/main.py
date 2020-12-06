import wfdb
from classes.Sensor import Sensor

def main():
    recordNum = 1
    recordTransmitter = wfdb.rdrecord('samples/'+str(recordNum), physical=False, sampfrom=0, channel_names=['avf'])
    recordReceiver = wfdb.rdrecord('samples/'+str(recordNum), physical=False, sampfrom=0, channel_names=['avf'])
    EKAPROTOCOL(recordTransmitter, recordReceiver)

def EKAPROTOCOL(recordTransmitter, recordReceiver):
    # Definindo frequência e quantidade de tempo para coleta das amostras
    frequency = 500
    seconds = 10

    # Quantidade de blocos de características que devem ser gerados
    numberOfBlocks = 20

    # Identificadores para o transmissor e receptor, respectivamente 
    IDt = 1
    IDr = 2

    sensorTransmitter = Sensor(frequency, seconds, numberOfBlocks, IDt)
    sensorReceiver = Sensor(frequency, seconds, numberOfBlocks, IDr)

    sensorTransmitter.extractFeats(recordTransmitter)
    sensorReceiver.extractFeats(recordReceiver)

    sensorTransmitter.receiveCommitmentMessage(sensorReceiver.getCommitmentMessage())
    sensorReceiver.receiveCommitmentMessage(sensorTransmitter.getCommitmentMessage())

    sensorTransmitter.processCommomKey()
    sensorReceiver.processCommomKey()

    sensorTransmitter.receiveDecommitmentMessage(sensorReceiver.getDecommitmentMessage())
    sensorReceiver.receiveDecommitmentMessage(sensorTransmitter.getDecommitmentMessage())

main()
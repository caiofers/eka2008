import wfdb
import random
import time

from classes.Sensor import Sensor

def featStatistics():
    ARArray = []
    FRRArray = []
    RRArray = []
    FARArray = []
    random.seed(time.time())

    for i in range(50):
        AR, FRR = testFRR(i+1, 100, 50)
        ARArray.append(AR)
        FRRArray.append(FRR)

        RR, FAR = testFAR(i+1, 100, 50)
        RRArray.append(RR)
        FARArray.append(FAR)

        print("Acceptance Rate")
        print(str(AR*100)+"%")
        print("False Rejection Rate")
        print(str(FRR*100)+"%")
        print("---------------------")
        print("Rejection Rate")
        print(str(RR*100)+"%")
        print("False Acceptance Rate")
        print(str(FAR*100)+"%")
        print("------------------------------------------")

    print("------------------------------------------")
    print("------------------------------------------")
    print("------------------------------------------")
    print("Acceptance Rate: " + str((sum(ARArray)/len(ARArray))*100) + "%")
    print(str((sum(ARArray)/len(ARArray))*100)+"%")
    print("False Rejection Rate: " + str((sum(FRRArray)/len(FRRArray))*100) + "%")
    print("---------------------")
    print("Rejection Rate: " + str((sum(RRArray)/len(RRArray))*100) + "%")
    print("False Acceptance Rate: " + str((sum(FARArray)/len(FARArray))*100) + "%")

    # Gerar arquivo com as análises na pasta analysis
    archive = open('analysis/featStatistics.txt', 'w')
    
    archive.write("\nTotal Statistics")
    archive.write("\nAcceptance Rate: " + str((sum(ARArray)/len(ARArray))*100) + "%")
    archive.write("\nFalse Rejection Rate: " + str((sum(FRRArray)/len(FRRArray))*100) + "%")
    archive.write("\n---------------------")
    archive.write("\nRejection Rate: " + str((sum(RRArray)/len(RRArray))*100) + "%")
    archive.write("\nFalse Acceptance Rate: " + str((sum(FARArray)/len(FARArray))*100) + "%")
    archive.close()

def testFRR(recordNum, iterations, sampleVariation):
    count = 0
    countFRR = 0
    for i in range(iterations):
        sampleFromT = random.randint(sampleVariation, 1000)
        randSampleFromR = random.randint(0, 1)
        if(randSampleFromR == 0): sampleFromR = sampleFromT - sampleVariation
        else: sampleFromR = sampleFromT + sampleVariation
        recordTransmitter = wfdb.rdrecord('samples/'+str(recordNum), physical=False, sampfrom=0, channel_names=['avf'])
        recordReceiver = wfdb.rdrecord('samples/'+str(recordNum), physical=False, sampfrom=0, channel_names=['avf'])
        if(EKAPROTOCOL(recordTransmitter, recordReceiver)):
            count = count + 1
        else:
            countFRR = countFRR + 1
    return count/iterations, countFRR/iterations

def testFAR(recordNum, iterations, sampleVariation):
    count = 0
    countFAR = 0
    recordNumT = recordNum
    for i in range(iterations):
        sampleFromT = random.randint(sampleVariation, 500)
        randSampleFromR = random.randint(0, 1)
        if(randSampleFromR == 0): sampleFromR = sampleFromT - sampleVariation
        else: sampleFromR = sampleFromT + sampleVariation
        recordNumR = random.randint(1, 200)
        while recordNumR == recordNumT:
            recordNumR = random.randint(1, 200) 
        recordTransmitter = wfdb.rdrecord('samples/'+str(recordNumT), physical=False, sampfrom=0, channel_names=['avf'])
        recordReceiver = wfdb.rdrecord('samples/'+str(recordNumR), physical=False, sampfrom=0, channel_names=['avf'])
        if(EKAPROTOCOL(recordTransmitter, recordReceiver)):
            countFAR = countFAR + 1
        else:
            count = count + 1
    return count/iterations, countFAR/iterations


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

    if (sensorTransmitter.receiveDecommitmentMessage(sensorReceiver.getDecommitmentMessage()) and sensorReceiver.receiveDecommitmentMessage(sensorTransmitter.getDecommitmentMessage())):
        return True
    else:
        return False

featStatistics()
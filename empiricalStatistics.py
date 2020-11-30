import wfdb
import time
import statistics
import tracemalloc

from Sensor import Sensor

def timeStatistics():
    timeExtractFeatTransmitterArray = []
    timeExtractFeatReceiverArray = []
    timeCommitmentPhaseTransmitterArray = []
    timeCommitmentPhaseReceiverArray = []
    timeProcessCommomKeyTransmitterArray = []
    timeProcessCommomKeyReceiverArray = []
    timeDeCommitmentPhaseTransmitterArray = []
    timeDeCommitmentPhaseReceiverArray = []
    totalTimeTransmitterArray = []
    totalTimeReceiverArray = []
    memoryPeakArray = []

    for i in range(50):
        recordTransmitter = wfdb.rdrecord('samples/'+str(i+1), physical=False, sampfrom=0, channel_names=['avf'])
        recordReceiver = wfdb.rdrecord('samples/'+str(i+1), physical=False, sampfrom=0, channel_names=['avf'])
        
        tracemalloc.start()
        timeExtractFeatTransmitter, timeExtractFeatReceiver, timeCommitmentPhaseTransmitter, timeCommitmentPhaseReceiver, timeProcessCommomKeyTransmitter, timeProcessCommomKeyReceiver, timeDeCommitmentPhaseTransmitter, timeDeCommitmentPhaseReceiver = EKAPROTOCOL(recordTransmitter, recordReceiver)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        timeExtractFeatTransmitterArray.append(timeExtractFeatTransmitter)
        timeExtractFeatReceiverArray.append(timeExtractFeatReceiver)
        timeCommitmentPhaseTransmitterArray.append(timeCommitmentPhaseTransmitter)
        timeCommitmentPhaseReceiverArray.append(timeCommitmentPhaseReceiver)
        timeProcessCommomKeyTransmitterArray.append(timeProcessCommomKeyTransmitter)
        timeProcessCommomKeyReceiverArray.append(timeProcessCommomKeyReceiver)
        timeDeCommitmentPhaseTransmitterArray.append(timeDeCommitmentPhaseTransmitter)
        timeDeCommitmentPhaseReceiverArray.append(timeDeCommitmentPhaseReceiver)
        totalTimeTransmitterArray.append(timeExtractFeatTransmitter + timeCommitmentPhaseTransmitter + timeProcessCommomKeyTransmitter + timeDeCommitmentPhaseTransmitter)
        totalTimeReceiverArray.append(timeExtractFeatReceiver + timeCommitmentPhaseReceiver + timeProcessCommomKeyReceiver + timeDeCommitmentPhaseReceiver)

        memoryPeakArray.append(peak)

        print("\nTime to Extract Features on Transmitter: "+str(timeExtractFeatTransmitter))
        print("Time to Extract Features on Receiver: "+str(timeExtractFeatReceiver))
        print("Time of commitment phase on Transmitter: "+str(timeCommitmentPhaseTransmitter))
        print("Time of commitment phase on Receiver: "+str(timeCommitmentPhaseReceiver))
        print("Time to process common key on Transmitter: "+str(timeProcessCommomKeyTransmitter))
        print("Time to process common key on Receiver: "+str(timeProcessCommomKeyReceiver))
        print("Time of de-commitment phase on Transmitter: "+str(timeDeCommitmentPhaseTransmitter))
        print("Time of de-commitment phase on Receiver: "+str(timeDeCommitmentPhaseReceiver))
        print("Current memory usage is " + str(current) + " Bytes; Peak was " + str(peak) + " Bytes");
        print("Total time Transmitter: "+str(timeExtractFeatTransmitter + timeCommitmentPhaseTransmitter + timeProcessCommomKeyTransmitter + timeDeCommitmentPhaseTransmitter))
        print("Total time Receiver: "+str(timeExtractFeatReceiver + timeCommitmentPhaseReceiver + timeProcessCommomKeyReceiver + timeDeCommitmentPhaseReceiver))

    print("\n---------------------")
    print("\nTotal statistics")

    print("\nTime to Extract Features on Transmitter")
    print("Mean: " + str(statistics.mean(timeExtractFeatTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeExtractFeatTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(timeExtractFeatTransmitterArray)))

    print("\nTime to Extract Features on Receiver")
    print("Mean: " + str(statistics.mean(timeExtractFeatReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeExtractFeatReceiverArray)))
    print("Variance: " + str(statistics.pvariance(timeExtractFeatReceiverArray)))

    print("\nTime of commitment phase on Transmitter")
    print("Mean: " + str(statistics.mean(timeCommitmentPhaseTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeCommitmentPhaseTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(timeCommitmentPhaseTransmitterArray)))

    print("\nTime of commitment phase on Receiver")
    print("Mean: " + str(statistics.mean(timeCommitmentPhaseReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeCommitmentPhaseReceiverArray)))
    print("Variance: " + str(statistics.pvariance(timeCommitmentPhaseReceiverArray)))

    print("\nTime to process common key on Transmitter")
    print("Mean: " + str(statistics.mean(timeProcessCommomKeyTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeProcessCommomKeyTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(timeProcessCommomKeyTransmitterArray)))

    print("\nTime to process common key on Receiver")
    print("Mean: " + str(statistics.mean(timeProcessCommomKeyReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeProcessCommomKeyReceiverArray)))
    print("Variance: " + str(statistics.pvariance(timeProcessCommomKeyReceiverArray)))

    print("\nTime of de-commitment phase on Transmitter")
    print("Mean: " + str(statistics.mean(timeDeCommitmentPhaseTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeDeCommitmentPhaseTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(timeDeCommitmentPhaseTransmitterArray)))

    print("\nTime of de-commitment phase on Receiver")
    print("Mean: " + str(statistics.mean(timeDeCommitmentPhaseReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(timeDeCommitmentPhaseReceiverArray)))
    print("Variance: " + str(statistics.pvariance(timeDeCommitmentPhaseReceiverArray)))

    print("\nTotal Time Transmmiter")
    print("Mean: " + str(statistics.mean(totalTimeTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(totalTimeTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(totalTimeTransmitterArray)))

    print("\nTotal Time Receiver")
    print("Mean: " + str(statistics.mean(totalTimeReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(totalTimeReceiverArray)))
    print("Variance: " + str(statistics.pvariance(totalTimeReceiverArray)))

    print("\nPeak Memory Usage")
    print("Mean: " + str(statistics.mean(memoryPeakArray)) + " Bytes")
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakArray)) + " Bytes")
    print("Variance: " + str(statistics.pvariance(memoryPeakArray)) + " Bytes")

    archive = open('empiricalStatistics', 'w')
    
    archive.write("\nTotal statistics")

    archive.write("\n\nTime to Extract Features on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(timeExtractFeatTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeExtractFeatTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeExtractFeatTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nTime to Extract Features on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(timeExtractFeatReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeExtractFeatReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeExtractFeatReceiverArray), 2)).replace('.', ','))

    archive.write("\n\nTime of commitment phase on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(timeCommitmentPhaseTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeCommitmentPhaseTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeCommitmentPhaseTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nTime of commitment phase on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(timeCommitmentPhaseReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeCommitmentPhaseReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeCommitmentPhaseReceiverArray), 2)).replace('.', ','))

    archive.write("\n\nTime to process common key on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(timeProcessCommomKeyTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeProcessCommomKeyTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeProcessCommomKeyTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nTime to process common key on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(timeProcessCommomKeyReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeProcessCommomKeyReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeProcessCommomKeyReceiverArray), 2)).replace('.', ','))

    archive.write("\n\nTime of de-commitment phase on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(timeDeCommitmentPhaseTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeDeCommitmentPhaseTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeDeCommitmentPhaseTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nTime of de-commitment phase on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(timeDeCommitmentPhaseReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(timeDeCommitmentPhaseReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(timeDeCommitmentPhaseReceiverArray), 2)).replace('.', ','))

    archive.write("\n\nTotal Time Transmmiter")
    archive.write("\nMean: " + str(round(statistics.mean(totalTimeTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(totalTimeTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(totalTimeTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nTotal Time Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(totalTimeReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(totalTimeReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(totalTimeReceiverArray), 2)).replace('.', ','))

    archive.write()

    archive.close()


def EKAPROTOCOL(recordTransmitter, recordReceiver):

    # Definindo frequencia e quantidade de tempo para coleta das amostras
    frequency = 500
    seconds = 10

    # Definindo ordem do polinômio
    numberOfBlocks = 20

    IDt = 1
    IDr = 2

    # Definindo variáveis para coletar tempo
    timeExtractFeatTransmitter = 0
    timeExtractFeatReceiver = 0
    timeCommitmentPhaseTransmitter = 0
    timeCommitmentPhaseReceiver = 0
    timeProcessCommomKeyTransmitter = 0
    timeProcessCommomKeyReceiver = 0
    timeDeCommitmentPhaseTransmitter = 0
    timeDeCommitmentPhaseReceiver = 0

    sensorTransmitter = Sensor(frequency, seconds, numberOfBlocks)

    #sensorTransmitter.setPlot(True)
    sensorReceiver = Sensor(frequency, seconds, numberOfBlocks)

    inicio = time.time()
    sensorTransmitter.extractFeats(recordTransmitter)
    fim = time.time()
    timeExtractFeatTransmitter = fim - inicio


    inicio = time.time()
    sensorReceiver.extractFeats(recordReceiver)
    fim = time.time()
    timeExtractFeatReceiver = fim - inicio

    inicio = time.time()
    message = sensorReceiver.getCommitmentMessage()
    sensorTransmitter.receiveCommitmentMessage(message)    
    fim = time.time()
    timeCommitmentPhaseReceiver = fim - inicio


    inicio = time.time()
    message = sensorTransmitter.getCommitmentMessage()
    sensorReceiver.receiveCommitmentMessage(message)
    fim = time.time()
    timeCommitmentPhaseTransmitter = fim - inicio

    
    inicio = time.time()
    sensorTransmitter.processCommomKey()
    fim = time.time()
    timeProcessCommomKeyTransmitter = fim - inicio
    
    inicio = time.time()
    sensorReceiver.processCommomKey()
    fim = time.time()
    timeProcessCommomKeyReceiver = fim - inicio
    
    inicio = time.time()
    sensorReceiver.receiveDecommitmentMessage(sensorTransmitter.getDecommitmentMessage())
    fim = time.time()
    timeDeCommitmentPhaseReceiver = fim - inicio


    inicio = time.time()
    sensorTransmitter.receiveDecommitmentMessage(sensorReceiver.getDecommitmentMessage())
    fim = time.time()
    timeDeCommitmentPhaseTransmitter = fim - inicio
    
    return timeExtractFeatTransmitter*1000, timeExtractFeatReceiver*1000, timeCommitmentPhaseTransmitter*1000, timeCommitmentPhaseReceiver*1000, timeProcessCommomKeyTransmitter*1000, timeProcessCommomKeyReceiver*1000, timeDeCommitmentPhaseTransmitter*1000, timeDeCommitmentPhaseTransmitter*1000


timeStatistics()
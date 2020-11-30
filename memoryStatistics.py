import wfdb
import statistics
import tracemalloc

from Sensor import Sensor

def memoryPeakStatistics():
    memoryPeakExtractFeatTransmitterArray = []
    memoryPeakExtractFeatReceiverArray = []
    memoryPeakCommitmentPhaseTransmitterArray = []
    memoryPeakCommitmentPhaseReceiverArray = []
    memoryPeakProcessCommomKeyTransmitterArray = []
    memoryPeakProcessCommomKeyReceiverArray = []
    memoryPeakDeCommitmentPhaseTransmitterArray = []
    memoryPeakDeCommitmentPhaseReceiverArray = []
    totalMemoryPeakTransmitterArray = []
    totalMemoryPeakReceiverArray = []

    for i in range(50):
        recordTransmitter = wfdb.rdrecord('samples/'+str(i+1), physical=False, sampfrom=0, channel_names=['avf'])
        recordReceiver = wfdb.rdrecord('samples/'+str(i+1), physical=False, sampfrom=0, channel_names=['avf'])
        
        memoryPeakExtractFeatTransmitter, memoryPeakExtractFeatReceiver, memoryPeakCommitmentPhaseTransmitter, memoryPeakCommitmentPhaseReceiver, memoryPeakProcessCommomKeyTransmitter, memoryPeakProcessCommomKeyReceiver, memoryPeakDeCommitmentPhaseTransmitter, memoryPeakDeCommitmentPhaseReceiver = EKAPROTOCOL(recordTransmitter, recordReceiver)

        memoryPeakExtractFeatTransmitterArray.append(memoryPeakExtractFeatTransmitter/1024)
        memoryPeakExtractFeatReceiverArray.append(memoryPeakExtractFeatReceiver/1024)
        memoryPeakCommitmentPhaseTransmitterArray.append(memoryPeakCommitmentPhaseTransmitter/1024)
        memoryPeakCommitmentPhaseReceiverArray.append(memoryPeakCommitmentPhaseReceiver/1024)
        memoryPeakProcessCommomKeyTransmitterArray.append(memoryPeakProcessCommomKeyTransmitter/1024)
        memoryPeakProcessCommomKeyReceiverArray.append(memoryPeakProcessCommomKeyReceiver/1024)
        memoryPeakDeCommitmentPhaseTransmitterArray.append(memoryPeakDeCommitmentPhaseTransmitter/1024)
        memoryPeakDeCommitmentPhaseReceiverArray.append(memoryPeakDeCommitmentPhaseReceiver/1024)
        totalMemoryPeakTransmitterArray.append(memoryPeakExtractFeatTransmitter/1024 + memoryPeakCommitmentPhaseTransmitter/1024 + memoryPeakProcessCommomKeyTransmitter/1024 + memoryPeakDeCommitmentPhaseTransmitter/1024)
        totalMemoryPeakReceiverArray.append(memoryPeakExtractFeatReceiver/1024 + memoryPeakCommitmentPhaseReceiver/1024 + memoryPeakProcessCommomKeyReceiver/1024 + memoryPeakDeCommitmentPhaseReceiver/1024)

        print("\nMemory Peak to Extract Features on Transmitter: "+str(memoryPeakExtractFeatTransmitter/1024))
        print("Memory Peak to Extract Features on Receiver: "+str(memoryPeakExtractFeatReceiver/1024))
        print("Memory Peak of commitment phase on Transmitter: "+str(memoryPeakCommitmentPhaseTransmitter/1024))
        print("Memory Peak of commitment phase on Receiver: "+str(memoryPeakCommitmentPhaseReceiver/1024))
        print("Memory Peak to process common key on Transmitter: "+str(memoryPeakProcessCommomKeyTransmitter/1024))
        print("Memory Peak to process common key on Receiver: "+str(memoryPeakProcessCommomKeyReceiver/1024))
        print("Memory Peak of de-commitment phase on Transmitter: "+str(memoryPeakDeCommitmentPhaseTransmitter/1024))
        print("Memory Peak of de-commitment phase on Receiver: "+str(memoryPeakDeCommitmentPhaseReceiver/1024))
        print("Total memory peak Transmitter: "+str(memoryPeakExtractFeatTransmitter/1024 + memoryPeakCommitmentPhaseTransmitter/1024 + memoryPeakProcessCommomKeyTransmitter/1024 + memoryPeakDeCommitmentPhaseTransmitter/1024))
        print("Total memory peak Receiver: "+str(memoryPeakExtractFeatReceiver/1024 + memoryPeakCommitmentPhaseReceiver/1024 + memoryPeakProcessCommomKeyReceiver/1024 + memoryPeakDeCommitmentPhaseReceiver/1024))

    print("\n---------------------")
    print("\nTotal statistics")

    print("\nMemory Peak to Extract Features on Transmitter")
    print("Mean: " + str(statistics.mean(memoryPeakExtractFeatTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakExtractFeatTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakExtractFeatTransmitterArray)))

    print("\nMemory Peak to Extract Features on Receiver")
    print("Mean: " + str(statistics.mean(memoryPeakExtractFeatReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakExtractFeatReceiverArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakExtractFeatReceiverArray)))

    print("\nMemory Peak of commitment phase on Transmitter")
    print("Mean: " + str(statistics.mean(memoryPeakCommitmentPhaseTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakCommitmentPhaseTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakCommitmentPhaseTransmitterArray)))

    print("\nMemory Peak of commitment phase on Receiver")
    print("Mean: " + str(statistics.mean(memoryPeakCommitmentPhaseReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakCommitmentPhaseReceiverArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakCommitmentPhaseReceiverArray)))

    print("\nMemory Peak to process common key on Transmitter")
    print("Mean: " + str(statistics.mean(memoryPeakProcessCommomKeyTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakProcessCommomKeyTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakProcessCommomKeyTransmitterArray)))

    print("\nMemory Peak to process common key on Receiver")
    print("Mean: " + str(statistics.mean(memoryPeakProcessCommomKeyReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakProcessCommomKeyReceiverArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakProcessCommomKeyReceiverArray)))

    print("\nMemory Peak of de-commitment phase on Transmitter")
    print("Mean: " + str(statistics.mean(memoryPeakDeCommitmentPhaseTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakDeCommitmentPhaseTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakDeCommitmentPhaseTransmitterArray)))

    print("\nMemory Peak of de-commitment phase on Receiver")
    print("Mean: " + str(statistics.mean(memoryPeakDeCommitmentPhaseReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(memoryPeakDeCommitmentPhaseReceiverArray)))
    print("Variance: " + str(statistics.pvariance(memoryPeakDeCommitmentPhaseReceiverArray)))

    print("\nTotal Memory Peak Transmmiter")
    print("Mean: " + str(statistics.mean(totalMemoryPeakTransmitterArray)))
    print("Standard Deviation: " + str(statistics.pstdev(totalMemoryPeakTransmitterArray)))
    print("Variance: " + str(statistics.pvariance(totalMemoryPeakTransmitterArray)))

    print("\nTotal Memory Peak Receiver")
    print("Mean: " + str(statistics.mean(totalMemoryPeakReceiverArray)))
    print("Standard Deviation: " + str(statistics.pstdev(totalMemoryPeakReceiverArray)))
    print("Variance: " + str(statistics.pvariance(totalMemoryPeakReceiverArray)))

    archive = open('memoryStatistics', 'w')

    archive.write("\nTotal statistics")

    archive.write("\n\nMemory Peak to Extract Features on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakExtractFeatTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakExtractFeatTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakExtractFeatTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nMemory Peak to Extract Features on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakExtractFeatReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakExtractFeatReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakExtractFeatReceiverArray), 2)).replace('.', ','))

    archive.write("\n\nMemory Peak of commitment phase on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakCommitmentPhaseTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakCommitmentPhaseTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakCommitmentPhaseTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nMemory Peak of commitment phase on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakCommitmentPhaseReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakCommitmentPhaseReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakCommitmentPhaseReceiverArray), 2)).replace('.', ','))

    archive.write("\n\nMemory Peak to process common key on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakProcessCommomKeyTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakProcessCommomKeyTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakProcessCommomKeyTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nMemory Peak to process common key on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakProcessCommomKeyReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakProcessCommomKeyReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakProcessCommomKeyReceiverArray), 2)).replace('.', ','))

    archive.write("\n\nMemory Peak of de-commitment phase on Transmitter")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakDeCommitmentPhaseTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakDeCommitmentPhaseTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakDeCommitmentPhaseTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nMemory Peak of de-commitment phase on Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(memoryPeakDeCommitmentPhaseReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(memoryPeakDeCommitmentPhaseReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(memoryPeakDeCommitmentPhaseReceiverArray), 2)).replace('.', ','))

    archive.write("\n\nTotal Memory Peak Transmmiter")
    archive.write("\nMean: " + str(round(statistics.mean(totalMemoryPeakTransmitterArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(totalMemoryPeakTransmitterArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(totalMemoryPeakTransmitterArray), 2)).replace('.', ','))

    archive.write("\n\nTotal Memory Peak Receiver")
    archive.write("\nMean: " + str(round(statistics.mean(totalMemoryPeakReceiverArray), 2)).replace('.', ','))
    archive.write("\nStandard Deviation: " + str(round(statistics.pstdev(totalMemoryPeakReceiverArray), 2)).replace('.', ','))
    archive.write("\nVariance: " + str(round(statistics.pvariance(totalMemoryPeakReceiverArray), 2)).replace('.', ','))

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
    memoryPeakExtractFeatTransmitter = 0
    memoryPeakExtractFeatReceiver = 0
    memoryPeakCommitmentPhaseTransmitter = 0
    memoryPeakCommitmentPhaseReceiver = 0
    memoryPeakProcessCommomKeyTransmitter = 0
    memoryPeakProcessCommomKeyReceiver = 0
    memoryPeakDeCommitmentPhaseTransmitter = 0
    memoryPeakDeCommitmentPhaseReceiver = 0

    sensorTransmitter = Sensor(frequency, seconds, numberOfBlocks)

    #sensorTransmitter.setPlot(True)
    sensorReceiver = Sensor(frequency, seconds, numberOfBlocks)

    tracemalloc.start()
    sensorTransmitter.extractFeats(recordTransmitter)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakExtractFeatTransmitter = peak


    tracemalloc.start()
    sensorReceiver.extractFeats(recordReceiver)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakExtractFeatReceiver = peak

    tracemalloc.start()
    message = sensorReceiver.getCommitmentMessage()
    sensorTransmitter.receiveCommitmentMessage(message)    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakCommitmentPhaseReceiver = peak


    tracemalloc.start()
    message = sensorTransmitter.getCommitmentMessage()
    sensorReceiver.receiveCommitmentMessage(message)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakCommitmentPhaseTransmitter = peak

    
    tracemalloc.start()
    sensorTransmitter.processCommomKey()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakProcessCommomKeyTransmitter = peak
    
    tracemalloc.start()
    sensorReceiver.processCommomKey()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakProcessCommomKeyReceiver = peak
    
    tracemalloc.start()
    sensorReceiver.receiveDecommitmentMessage(sensorTransmitter.getDecommitmentMessage())
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakDeCommitmentPhaseReceiver = peak


    tracemalloc.start()
    sensorTransmitter.receiveDecommitmentMessage(sensorReceiver.getDecommitmentMessage())
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    memoryPeakDeCommitmentPhaseTransmitter = peak
    
    return memoryPeakExtractFeatTransmitter, memoryPeakExtractFeatReceiver, memoryPeakCommitmentPhaseTransmitter, memoryPeakCommitmentPhaseReceiver, memoryPeakProcessCommomKeyTransmitter, memoryPeakProcessCommomKeyReceiver, memoryPeakDeCommitmentPhaseTransmitter, memoryPeakDeCommitmentPhaseTransmitter


memoryPeakStatistics()
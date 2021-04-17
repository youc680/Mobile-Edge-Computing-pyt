from config import Config
import os


def processObject(locations):
    if len(locations) < 2:
        return 3
    else:
        return locations[-2]

def dumpOutputPerCycle(network, currentTime):
    if not network.output:
        return

    f = open(f"{os.getcwd()}/{Config.resultsFolder}/{Config.dumpDelayDetail}", "a")
    totalDelayRemain = 0
    for mes in network.output:
        delay = mes.currentTime - mes.startTime
        network.maxDelay = max(delay, network.maxDelay)
        if mes.isDrop:
            network.countDrop += 1
        else:
            network.meanDelay += delay

        # Record type
        mes.setType()
        if processObject(mes.locations) == 0 or processObject(mes.locations) == 3:
            network.processAtCar += 1
        elif processObject(mes.locations) == 1:
            network.processAtRsu += 1
        else:
            network.processAtGnb += 1

        # Record average delay remain
        delayRemain = mes.maxDelay - delay
        totalDelayRemain += delayRemain
        # f.write(f"{mes.sendTime[0]} \t {mes.currentTime} \t {delay} \t {mes.type} \t {network.maxDelay} \n")

    # Average delay remain cumulative
    network.averageRemainDelay = network.totalOutsize * network.averageRemainDelay + totalDelayRemain
    network.totalOutsize += len(network.output)
    network.averageRemainDelay /= network.totalOutsize

    meanDelay = (network.meanDelay + network.countDrop * network.maxDelay) / network.totalOutsize
    f.write(f"{currentTime} \t {meanDelay} \t {network.maxDelay} \t {network.averageRemainDelay} \
            \t {network.countDrop} \t {network.processAtCar} \
            \t {network.processAtRsu} \t {network.processAtGnb}\n")
    print(f"{currentTime} \t {meanDelay} \t {network.maxDelay} \t {network.averageRemainDelay} \
            \t {network.countDrop} \t {network.processAtCar} \
            \t {network.processAtRsu} \t {network.processAtGnb}")
    network.output = []

def dumpOutputFinal(network):
    network.meanDelay = (network.meanDelay + \
            network.countDrop * network.maxDelay) / network.totalOutsize
    f = open(f"{os.getcwd()}/{Config.resultsFolder}/{Config.dumpDelayGeneral}", "a")
    f.write(f"{Config.carPacketStrategy} \t {Config.carAppearStrategy} \t \
        {Config.rsuNumbers} \t {network.meanDelay} \t {network.averageRemainDelay} \
        \t {network.countDrop} \t {network.totalOutsize} \t {network.processAtCar} \
        \t {network.processAtRsu} \t {network.processAtGnb}\n")
    f.close()
    print("Done dumping final output!!!") 

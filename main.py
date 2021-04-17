import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
from network.network import Network
from vehicle.carSimulator import CarSimulator
from rsu.rsuSimulator import RsuSimulator
from gnb.gnbSimulator import GnbSimulator
# from optimizers.DQN import DQN
# from optimizers.MAB import MAB
# from optimizers.MAB_DQN import MAB_DQN
# from optimizers.PBased import PBased
from optimizers.DeepPolicy.DeepPolicy_Vehicle import DeepPolicy_Vehicle
from optimizers.DeepPolicy.DeepPolicy_Rsu import DeepPolicy_Rsu
from config import Config
from behaviorPolicy.DeepPolicy.PG_Net import DeepNet


def main():
    Rnet = DeepNet(numInput=3, hiddenUnits=10, numOutput=3)
    Vnet = DeepNet(numInput=4, hiddenUnits=15, numOutput=4)
    gnb = GnbSimulator()
    rsuList= getRsuList()
    print(len(rsuList))
    carList = carAppear()
    print(len(carList))
    listTimeMessages = prepareTimeMessages()
    print(len(listTimeMessages))
    network = Network(
        gnb=gnb,
        rsuList=rsuList,
        carList=carList,
        listTimeMessages=listTimeMessages,
        globalObject={
            "RSU network": Rnet,
            "Vehicle network": Vnet
        }
    )
    network.run()

def getRsuList():
    res = []
    for i in range(Config.rsuNumbers):
        rsu = RsuSimulator(
            id=i,
            xcord=Config.xList[i],
            ycord=Config.yList[i],
            zcord=Config.zList[i],
            optimizer=DeepPolicy_Rsu(
                agent_name=f"rsu{i}"
            )
        )
        res.append(rsu)
    return res

def prepareTimeMessages():
    try:
        f = open(Config.carPacketStrategy, "r")
    except:
        print("File packet not found !!!")
        exit()
    currentTime = 0
    res = []
    for x in f:
        tmp = float(x)
        timeStartFromCar = currentTime + tmp
        currentTime = timeStartFromCar
        res.append(timeStartFromCar)
    return res

def carAppear():
    try:
        f = open(Config.carAppearStrategy, "r")
    except:
        print("File car not found")
        exit()
    res = []
    currentTime = 0
    index = 0
    for x in f:
        tmp = float(x)
        timeStartCar = currentTime + tmp
        if timeStartCar > Config.simTime:
            return res
        car = CarSimulator(
            id=index, 
            startTime=timeStartCar,
            optimizer=DeepPolicy_Vehicle(
                agent_name=f"car_{index}"
            )
        )
        res.append(car)
        index += 1
        currentTime = timeStartCar
    return res


if __name__=="__main__":
    from datetime import datetime
    start = datetime.now()
    if not os.path.exists(f"{os.getcwd()}/{Config.weightsFolder}"):
        os.mkdir(f"{os.getcwd()}/{Config.weightsFolder}")
    if not os.path.exists(f"{os.getcwd()}/{Config.resultsFolder}"):
        os.mkdir(f"{os.getcwd()}/{Config.resultsFolder}")
    main()
    end = datetime.now()
    print(start)
    print(end)

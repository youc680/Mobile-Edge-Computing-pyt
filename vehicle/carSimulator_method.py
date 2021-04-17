import random
import numpy as np
import math
import copy
from config import Config
from utils import calculateTaskInQueue

def getNeighborCarInfo(car):
    def sortFunc(e):
        return e[1]
    tmp = []
    for car_ in car.neighborCars:
        expectedTime = calculateTaskInQueue(car_) / Config.carProcessPerSecond
        tmp.append((expectedTime, car_.meanDelay, car_))
    tmp.sort(key=sortFunc)
    if not tmp:
        # print("Don't has neighbor car")
        return (0.0, 0.0, None)
    rand = random.random()
    if rand < 0.5:
        return tmp[0]
    else:
        return tmp[random.randint(0, len(tmp)-1)] 
    
def getNeighborRsuInfo(car):
    neighborRsu = car.neighborRsu
    if neighborRsu:
        expectedTime = calculateTaskInQueue(neighborRsu) / Config.rsuProcessPerSecond
        return (expectedTime, neighborRsu.meanDelay, neighborRsu)
    else:
        print("Don't has neighbor rsu")
        input()
        return (0.0, 0.0, None)

def getState(car, message, network):
    # print("car_{} get state for message id {}".format(car.id, message.stt))
    # print("len waitList of this car {}".format(len(car.waitList)))
    # Info of this message
    res = [message.size, message.cpuCycle]
    # Info of this car
    # res.append(calculateTaskInQueue(car))
    res.append(car.meanDelayProcess)
    res.append(car.meanDelaySendToCar)
    res.append(car.meanDelaySendToRsu)
    res.append(car.meanDelaySendToGnb)
    # Info of it's neighbor car
    neighborCarInfo = getNeighborCarInfo(car)
    # res.append(neighborCarInfo[0])
    res.append(neighborCarInfo[1])
    # Info of it's neighbor rsu
    neighborRsuInfo = getNeighborRsuInfo(car)
    # res.append(neighborRsuInfo[0])
    res.append(neighborRsuInfo[1])
    # Info of gnb
    res.append(network.gnb.meanDelay)
    res = np.reshape(res, (1, len(res)))
    # print(res)
    return (res, neighborCarInfo[2], neighborRsuInfo[2])

def getAction(car, message, currentTime, network):
    """Gat action of this car for the message

    Args:
        car ([CarSimulator]): [description]
        message ([Message]): [description]
        currentTime ([float]): [description]
        network ([Network]): [description]

    Returns:
        action: [0:sendToCar, 1:sendToRsu, 2:sendToGnb or 3:process]
        nextLocation: [The location where the message will be sent to]
    """    
    # 0: car, 1:rsu, 2:gnb, 3:process
    currentState = None
    # Change for fit with your optimize
    # ************************************************************************
    # With MAB
    # neighborCar = getNeighborCarInfo(car)[2]
    # neighborRsu = getNeighborRsuInfo(car)[2]

    # With MAB_DQN
    stateInfo = getState(car, message, network)
    currentState = stateInfo[0]
    neighborCar = stateInfo[1]
    neighborRsu = stateInfo[2]
    # car.optimizer.DQN.updateState(message, currentState)
    # *************************************************************************
    # Constant
    # get values of all actions
    # allActionValues = car.optimizer.getAllActionValues(currentState)
    # exclude actions can't choose
    exclude_actions = []
    if neighborCar is None or len(message.indexCar) >= 2:
        exclude_actions.append(0)
    if neighborRsu is None:
        exclude_actions.append(1)
    # get action by policy

    actionByPolicy = car.optimizer.policy(exclude_actions, car.optimizer.probVector, message, Vnet=network.Vnet)
    # Update memory
    # car.optimizer.addToMemoryTmp(message, currentState, actionByPolicy)
    # return tuple of action and object the message will be in
    if actionByPolicy == 0:
        res = (0, neighborCar)
    elif actionByPolicy == 1:
        res = (1, neighborRsu)
    elif actionByPolicy == 2:
        res = (2, network.gnb)
    else:
        res = (3, None)
    return res


def getPosition(car, currentTime):    
    return Config.carSpeed * (currentTime - car.startTime)

def distanceToCar(car1, car2, currentTime):
    return abs(car1.getPosition(currentTime) - car2.getPosition(currentTime))

def distanceToRsu(car, rsu, currentTime):
    position = car.getPosition(currentTime)
    return math.sqrt(
        pow(position - rsu.xcord, 2) + pow(rsu.ycord, 2) + pow(rsu.zcord, 2)
    )  


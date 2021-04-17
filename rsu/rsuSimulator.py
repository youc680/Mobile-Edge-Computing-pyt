import math
from object import Object
from message import Message
from config import Config
from rsuSimulator_method import (
    getAction, distanceToCar, distanceToRsu
)
from utils import update


class RsuSimulator(Object):

    def __init__(self, id, xcord, ycord, zcord, optimizer=None):
        Object.__init__(self)
        self.id = id
        self.xcord = xcord
        self.ycord = ycord
        self.zcord = zcord
        self.optimizer = optimizer
        self.neighbors = []

    def sendToCar(self, car, message, currentTime, network):
        """Simulate send message from rsu to car

        Args:
            car ([CarSimulator]): [description]
            message ([Message]): [description]
            currentTime ([float]): [description]
            network ([Network]): [description]
        """        
        # Add index car to list indexCar of message
        message.indexCar.append(car.id)

        # Simulate tranfer time to car
        self.simulateTranferTime(
            preReceive=car.preReceiveFromRsu,
            meanTranfer=Config.rsuCarMeanTranfer,
            message=message,
        )

        # Add current location to list locations of message 
        # and change preReceiveFromRsu of this car
        message.locations.append(0)
        car.preReceiveFromRsu = message.currentTime
        
        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            car.waitList.append(message)
        else:
            network.addToHeap(message)
    
    def sendToRsu(self, rsu, message, currentTime, network):
        """Simualte send message from rsu to rsu

        Args:
            rsu ([RsuSimulator]): [description]
            message ([Message]): [description]
            currentTime ([float]): [description]
            network ([Network]): [description]
        """        
        # Add index rsu to list indexRsu of message
        message.indexRsu.append(rsu.id)

        # Simulate tranfer time to rsu
        self.simulateTranferTime(
            preReceive=rsu.preReceiveFromRsu,
            meanTranfer=Config.rsuRsuMeanTranfer,
            message=message,
        )

        # Add current location to list locations of message 
        # and change preReceiveFromRsu of this rsu
        message.locations.append(1)
        rsu.preReceiveFromRsu = message.currentTime
        
        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            rsu.waitList.append(message)
        else:
            network.addToHeap(message)

    def sendToGnb(self, gnb, message, currentTime, network):
        """Simualte send message from rsu to gnb

        Args:
            gnb ([GnbSimulator]): [description]
            message ([Message]): [description]
            currentTime ([float]): [description]
            network ([Network]): [description]
        """        

        # Simulate tranfer time to rsu
        self.simulateTranferTime(
            preReceive=gnb.preReceiveFromRsu,
            meanTranfer=Config.rsuGnbMeanTranfer,
            message=message,
        )

        # Add current location to list locations of message 
        # and change preReceiveFromRsu of gnb
        message.locations.append(2)
        gnb.preReceiveFromRsu = message.currentTime
        
        # Check the currentTime of message
        if message.currentTime > currentTime + Config.cycleTime:
            gnb.waitList.append(message)
        else:
            network.addToHeap(message)

    def process(self, message, currentTime,network):
        # Simulate process time
        self.simulateProcessTime(
            processPerSecond=Config.rsuProcessPerSecond,
            message=message,
        )
        if message.currentTime > currentTime + Config.cycleTime:
            self.waitList.append(message)
        else:
            network.addToHeap(message)

    def distanceToCar(self, car, currentTime, func=distanceToCar):
        return func(self, car, currentTime)

    def distanceToRsu(self, rsu, func=distanceToRsu):
        return func(self, rsu)  

    def working(self, message, currentTime, network, getAction=getAction):
        if message.isDone:
            rsu_id = message.indexRsu[0]
            if rsu_id != self.id:
                self.sendToRsu(network.rsuList[rsu_id], message, currentTime, network)
                return
            startCar = network.carList[message.indexCar[0]]
            if startCar.getPosition(currentTime) > Config.roadLength or \
                self.distanceToCar(startCar, currentTime) > Config.rsuCoverRadius:
                message.isDrop = True
                network.output.append(message)
                if self.optimizer is not None:
                    update(message, network, code="rsu")
            else:
                self.sendToCar(startCar, message, currentTime, network)
        else:
            action, nextLocation = getAction(self, message, currentTime, network)
            # 0: sendToRsu, 1:sendToGnb, 2:process
            if action == 1: 
                self.sendToRsu(nextLocation, message, currentTime, network)
            elif action == 2:
                self.sendToGnb(nextLocation, message, currentTime, network)
            else:
                self.process(message, currentTime, network)

        


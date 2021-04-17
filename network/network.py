from queue import PriorityQueue
from utils import PrioritizedItem
from config import Config
from network_method import dumpOutputPerCycle, dumpOutputFinal


class Network:
    def __init__(self, gnb, rsuList, carList, listTimeMessages, globalObject=None):
        self.gnb = gnb
        self.rsuList = rsuList
        self.carList = carList
        self.listTimeMessages = listTimeMessages
        self.q = PriorityQueue()
        self.output = []
        self.meanDelay = 0.0
        self.countDrop = 0
        self.totalOutsize = 0
        self.maxDelay = 0
        self.setNeighborRsu()

        # insight package counter print to file
        self.processAtRsu = 0
        self.processAtGnb = 0
        self.processAtCar = 0

        # insight related to delay
        self.validDelay = 0     # delay < max delay
        self.averageRemainDelay = 0

        # global network to train
        self.Rnet = globalObject["RSU network"]
        self.Vnet = globalObject["Vehicle network"]


    def setNeighborRsu(self):
        for i, rsu in enumerate(self.rsuList):
            for j, rsu_ in enumerate(self.rsuList):
                if j == i:
                    continue
                rsu.neighbors.append(rsu_)

    def collectMessages(self, currentTime):
        res = []
        for car in self.carList:
            if car.getPosition(currentTime) > Config.roadLength \
            or car.startTime > currentTime:
                continue
            res.append(car.collectMessages(
                currentTime, self.listTimeMessages))
        for rsu in self.rsuList:
            res.append(rsu.collectMessages(currentTime))
        res.append(self.gnb.collectMessages(currentTime))
        res = [i for sublist in res for i in sublist]
        for mes in res:
            self.addToHeap(mes)

    def addToHeap(self, message):
        self.q.put(PrioritizedItem(
            priority=(message.currentTime,message.stt),
            item=message))

    def setNeighborCar(self, car, currentTime):
        # Set neighbor car
        car.neighborCars = []
        for car_ in self.carList:
            if car_.getPosition(currentTime) > Config.roadLength \
            or car_.startTime > currentTime or car_.id == car.id:
                continue
            distance = car.distanceToCar(car_, currentTime)
            if distance < Config.carCoverRadius:
                car.neighborCars.append(car_)
        # Set neighbor rsu
        if car.neighborRsu is not None:
            if car.distanceToRsu(car.neighborRsu, currentTime) <= Config.rsuCoverRadius:
                return
        minDistance = Config.rsuCoverRadius
        neighborRsu = None
        for rsu in self.rsuList:
            distance = car.distanceToRsu(rsu, currentTime)
            if distance < minDistance:
                minDistance = distance
                neighborRsu = rsu
        car.neighborRsu = neighborRsu                

    def working(self, currentTime):
        # Set neighbor list for this cars
        for car in self.carList:
             # If car isn't in road, continue
            if car.getPosition(currentTime) > Config.roadLength \
            or car.startTime > currentTime:
                continue
            self.setNeighborCar(car, currentTime)

        self.collectMessages(currentTime)
        while not self.q.empty():
            mes = self.q.get().item
            # print(type(mes.currentObject))
            currentLocation = mes.locations[-1]
            if currentLocation == 0:
                car = self.carList[mes.indexCar[-1]]
                car.working(
                    message=mes, 
                    currentTime=currentTime, 
                    network=self,
                ) 
            elif currentLocation == 1:
                rsu = self.rsuList[mes.indexRsu[-1]]
                rsu.working(mes, currentTime, self)
            else:
                self.gnb.working(mes, currentTime, self)

    def run(self):
        currentTime = 0
        while(currentTime < Config.simTime):
            self.working(currentTime)
            self.dumpOutputPerCycle(currentTime)
            currentTime += Config.cycleTime
        self.dumpOutputFinal()

    def dumpOutputPerCycle(self, currentTime, func=dumpOutputPerCycle):
        func(self, currentTime)

    def dumpOutputFinal(self, func=dumpOutputFinal):
        func(self)

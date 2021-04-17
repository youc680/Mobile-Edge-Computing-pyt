from config import Config


class Message:
    cnt = 0

    def __init__(self, indexCar, time, size=1, cpuCycle=1, ttl=Config.ttl):
        self.size = size
        self.cpuCycle = cpuCycle
        self.ttl = ttl
        self.stt = Message.cnt
        Message.cnt += 1
        self.indexCar = [indexCar]
        self.indexRsu = []
        self.sendTime = []
        self.receiveTime = []
        self.locations = [0]  # locations 0: car, 1:rsu, 2:gnb
        self.startTime = time
        self.currentTime = time
        self.isDone = False
        self.isDrop = False
        self.type = ""
        self.maxDelay = Config.maxDelay
        self.message_id = Message.cnt

        # car sends information onto rsu
        self.rsuDelay_sendup = 0
        self.gnbDelay_sendup = 0

    def setType(self):
        for location in self.locations:
            if location == 0:
                self.type += "car_"
            elif location == 1:
                self.type += "rsu_"
            else:
                self.type += "gnb_"
        self.type = self.type[:-1]

    def getDelayNow(self):
        return self.currentTime - self.startTime

    def getDelayRemain(self):
        return self.maxDelay - self.getDelayNow()

    def getTotalDelay(self):
        if (len(self.receiveTime) > 1):
            # print(self.receiveTime)
            return self.receiveTime[-1] - self.startTime
        else:
            return 0

    def getProcessor(self):
        if self.locations[-1]:
            return self.locations[-1]
        elif len(self.locations) == 1:
            return 3
        else:
            return self.locations[-2]

    """
    Car action = {0 : send to other car,
                  1 : send to Rsu,
                  2 : send to gnb,
                  3 : self process}
    """
    def getCarAction(self):
        if len(self.locations) >= 2:
            return self.locations[1]
        return False

    """
    Rsu action = {1 : send to other Rsu,
                  2 : send to gnb,
                  3 : self process}
    """
    def getRsuAction(self):
        if len(self.locations) >= 3 and self.locations[1] == 1:
            delayFromRsu = self.getTotalDelay() - (self.sendTime[1] - self.sendTime[0])
            if self.locations[2] == 0:
                return 3, delayFromRsu
            else:
                return self.locations[2], delayFromRsu
        return False, None


# a = Message(indexCar=1, time=2)
# a.locations.append(1)
# a.locations.append(1)
# a.locations.append(2)
# a.locations.append(0)
# #print(a.stt)
# a.setType()
# print(a.type)
# print(a.getCarAction())
# print(a.getRsuAction())
# print(a.getProcessor())

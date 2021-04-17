from config import Config
from utils import getNext

class Object:

    def __init__(self):
        self.waitList = []
        self.preProcess = 0.0
        self.preReceiveFromCar = 0.0
        self.preReceiveFromRsu = 0.0
        self.preReceiveFromGnb = 0.0
        self.maxDelay = 0.0
        self.meanDelay = 0.0
        self.meanDelayProcess = 0.0
        self.meanDelaySendToCar = 0.0
        self.meanDelaySendToRsu = 0.0
        self.meanDelaySendToGnb = 0.0
        self.cnt = 0 
        self.cntProcess = 0
        self.cntSendToCar = 0
        self.cntSendToRsu = 0
        self.cntSendToGnb = 0
        self.cntDrop = 0

    def collectMessages(self, currentTime):
        """Collect the messages in waitList which have the current time
        in [currentTime, currentTime + cycleTime]

        Args:
            currentTime ([float]): [description]

        Returns:
            [list(Message)]: [description]
        """        
        tmp = self.waitList
        self.waitList = []
        res = []
        for mes in tmp:
            if mes.currentTime > currentTime + Config.cycleTime:
                self.waitList.append(mes)
            else:
                res.append(mes)
        return res

    def simulateTranferTime(self, preReceive, meanTranfer, message):
        """Simulate the tranfer time from here to another object

        Args:
            preReceive ([float]): [description]
            meanTranfer ([float]): [description]
            message ([Message]): [description]
        """        
        # Add currentTime to list sendTime of message
        message.sendTime.append(message.currentTime)

        #  calculate tranfer time and receive time
        tranferTime = getNext(1.0/meanTranfer) * message.size
        selectedTime = max(preReceive, message.currentTime)
        receiveTime = tranferTime + selectedTime

        # Set receive time to list receiveTime of message and change current time
        message.receiveTime.append(receiveTime)
        message.currentTime = receiveTime

    def simulateProcessTime(self, processPerSecond, message):
        """Simulate the process time 

        Args:
            processPerSecond ([float]): [description]
            message ([Message]): [description]
        """        
        # calculate process time
        selectedTime = max(message.currentTime, self.preProcess)
        processTime = getNext(processPerSecond) * message.cpuCycle
        processedTime = selectedTime + processTime

        # Change currentTime of message and set is done
        message.currentTime = processedTime
        message.isDone = True

        # Change preprocess time of this object
        self.preProcess = processedTime


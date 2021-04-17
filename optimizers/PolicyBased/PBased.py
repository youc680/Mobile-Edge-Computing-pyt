import numpy as np
from optimizers.optimizer import Optimizer
import config
from behaviorPolicy.PolicyBased import PB_policy
from optimizers.utils import Vector_processing


class PBased(Optimizer):
    def __init__(self, agent_name, p_init, learning_rate, fuzzy_system=None):
        super().__init__(agent_name)
        self.agent_name = agent_name
        self.probVector = p_init
        self.learning_rate = learning_rate
        self.policy = PB_policy.PB_policy(config.Config.decision_factor).getPolicy(fuzzy_system)

    def addToMemoryTmp(self, message, state, action):
        pass

    def updateReward(self, message, delay, code="car"):
        assert code == "car" or code == "rsu", "Invalid arguments, updateReward function called"
        if code == "car":
            delay_vector = Vector_processing.softmax(self.getDelayVect(message) * (-1))
        else:
            delay_vector = np.array([0, message.rsuDelay_sendup, message.gnbDelay_sendup, message.rsuDelay_sendup]).reshape([4, 1])
            delay_vector = Vector_processing.percentage(delay_vector)
        self.probVector = (1 - self.learning_rate) * self.probVector + self.learning_rate * delay_vector

    def getAllActionValues(self, state):
        pass

    def getTraceDict(self, message):
        if len(message.locations) > 1:
            if message.locations[-1] == 0:
                return {"car": message.locations.count(0) - 2, "rsu": message.locations.count(1),
                        "gnb": message.locations.count(2), "self": 0}
            else:
                return {"car": message.locations.count(0) - 1, "rsu": message.locations.count(1),
                        "gnb": message.locations.count(2), "self": 0}
        else:
            return {"car": 0, "rsu": 0, "gnb": 0, "self": 1}

    def getDelayVect(self, message):
        delay = message.getTotalDelay()
        if len(message.locations) > 1:
            index = message.locations[1]
        else:
            index = 3
        #print("index: " + str(index))
        returnVector = np.zeros([4, 1])
        returnVector[index] = delay
        return returnVector


# pb = PBased(agent_name="agent_" + str(1),
#             p_init=config.Config.p_init_car,
#             learning_rate=config.Config.learning_rate_car)
#
# ms = Message(1, 0)
# ms.startTime = 0.5
# ms.sendTime = [1, 2, 3, 4]
# ms.receiveTime = [1.2, 2.15, 3.84, 4.15]
# ms.currentTime = 6.15
# ms.locations = [0, 0, 1, 1, 0]
# ms.setType()
# ms.maxDelay = 6.153
# ms.size = 1
#
# print("type: " + ms.type)
# print(pb.getTraceDict(ms))
# print("vect: \n" + str(pb.getDelayVect(ms)))
# pb.updateReward(message=ms, delay=0)
# print(pb.probVector)

#policy = PB_policy.PB_policy(size_pad=config.Config.size_pad_car,
#                             delay_remain_pad=config.Config.delay_remain_pad_car).getPolicy()
# for i in range(1, 5):
#     ms.size = i
#     print(ms.size)
#     policy(pb.probVector, ms)

# for i in range(7, 10):
#     ms.maxDelay = i
#     print(i)
#     policy(pb.probVector, ms)

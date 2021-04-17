import numpy as np
# from config import Config
# from message import Message
# from fuzzy_inference_vehicle import FuzzyVehicleInference
# from fuzzy_inference_rsu import FuzzyRsuInference

class PB_policy():
    def __init__(self, decision_factor=None):
        self.decision_factor = decision_factor

    def getPolicy(self, fuzzy_system):
        """
        probVector =    [[Pcar],
                         [Prsu],
                         [Pgnb],
                         [Pself]]
        delay_pad = array of (4x1)
        size_pad = array of (4x1)
        """

        def chooseAction(probVector, message):
            assert probVector.shape == (4, 1), "Unfit probability Vector to choosingAction function"
            # delay remain vector, sum = 1, softmax called
            delayRemain = message.getDelayRemain()
            size = message.size
            newVect = fuzzy_system.Inference(delayRemain=delayRemain, packageSize=size)

            # fix sum array not equals to 1
            newVect[-1] = 1 - newVect[0:-1].sum()
            probVector[-1] = 1 - probVector[0:-1].sum()

            # print("fuzzy: " + str(newVect))
            # print("prob: " + str(probVector))
            newVect = (1 - self.decision_factor) * probVector + self.decision_factor * newVect.reshape([4, 1])
            # print("now: " + str(newVect))
            return np.random.choice([0, 1, 2, 3], p=newVect.reshape([4, ]))

        return chooseAction


# pb = PB_policy(0.2).getPolicy(FuzzyRsuInference(MAX_DELAY_REMAIN=5, MAX_PACKET_SIZE=10))
#
# ms = Message(1, 0)
# ms.startTime = 0.5
# ms.sendTime = [1]
# ms.receiveTime = [1.2]
# ms.currentTime = 1.2
# ms.locations = [0, 0, 0, 1, 1, 0]
# ms.setType()
# print(pb(probVector=np.array([[0.251], [0.251], [0.239], [0.258]]),
#          message=ms))

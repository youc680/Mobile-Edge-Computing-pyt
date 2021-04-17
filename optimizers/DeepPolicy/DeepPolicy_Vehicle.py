import numpy as np
from config import Config as cf
from optimizers import utils
from optimizers.optimizer import Optimizer
from behaviorPolicy.DeepPolicy.PG_policy_Vehicle import PG_policy_car


class DeepPolicy_Vehicle(Optimizer):
    """
    init delay Vector of (1, 4) = [[0, 0, 0, 0]]
    this vector is used to train output Vnet

    also, init delay vector of (1, 3) = [[0, 0, 0]]
    this vector is sent to RSUs, RSUs use this vector
    to train output Rnet
    """
    def __init__(self, agent_name=None):
        super().__init__(agent_name)
        self.agent_name = agent_name
        self.delayForCar = np.zeros([1, 4])
        self.delayForRsu = np.zeros([1, 3])
        self.policy = PG_policy_car().getPolicy()

    def updateDelayCar(self, newVect):
        self.delayForCar = (1 - cf.dp_decay) * self.delayForCar + cf.dp_decay * newVect

    def updateDelayRsu(self, newVect):
        self.delayForRsu = (1 - cf.dp_decay) * self.delayForRsu + cf.dp_decay * newVect

    def getDelayVectCar(self, message):
        message_id = message.id
        newVect = [0, 0, 0, 0]
        delay = message.getTotalDelay()
        actor = message.getAction()
        newVect[actor] = delay
        return message_id, newVect

    def updateReward(self, message, Vnet, Rnet):
        message_id, newVectCar = self.getDelayVectCar(message=message)
        self.updateDelayCar(newVect=np.array(newVectCar).reshape([1, 4]))
        Vnet.updateNet(
            message_id=message_id,
            delayVector=utils.Vector_processing.softmax((-1) * self.delayForCar).reshape([1, 4])
        )
        # If the message was first sent to a rsu then create a vector
        isRsuNext, delayFromRsu = message.getRsuAction()
        if isRsuNext:
            newVect = [0, 0, 0]
            # getRsuAction() is either = {1,2}
            newVect[message.getRsuAction() - 1] = delayFromRsu
            self.updateDelayRsu(newVect=np.array(newVect).reshape([1, 3]))
            Rnet.updateNet(
                message_id=message_id,
                delayVector=utils.Vector_processing.softmax((-1) * self.delayForRsu).reshape([1, 4])
            )




#
# delayVector = [0, 0, 0, 0]
# delay = 0.5
# processor = 3
# delayVector[processor] = delay
# print(np.array(delayVector).reshape([1, 4]))

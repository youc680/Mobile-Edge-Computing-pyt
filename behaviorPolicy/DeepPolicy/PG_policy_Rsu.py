from config import Config
from optimizers.Fuzzy.fuzzy_inference_rsu import FuzzyRsuInference
import numpy as np


class PG_policy_rsu:
    rsu_fuzzy_system = FuzzyRsuInference(Config.maxDelay, Config.maxSize)

    """
    With decay = 0.995, starts at 0.3, it takes ~1140 times update
    to decay almost all fuzzy system
    """
    def __init__(self):
        self.Fuzzy_factor = 0.3
        self.Fuzzy_decay = 0.995

    def getPolicy(self):
        def chooseAction(exclude_actions=None, queue_infor=None, message=None, Rnet=None):
            dR = message.getDelayRemain()
            size = message.size
            queue_rsu = queue_infor["rsu"]
            queue_gnb = queue_infor["gnb"]
            queue_self = queue_infor["self"]

            FuzzyInput = {
                "dR": dR,
                "size": size,
                "qR": queue_rsu,
                "qG": queue_gnb,
                "qS": queue_self
            }
            FuzzyOutput = 0
            if self.Fuzzy_factor > 0.001:
                FuzzyOutput = PG_policy_rsu.rsu_fuzzy_system.Inference(fuzzy_input=FuzzyInput)

            NetInput = np.array(FuzzyInput.values()).reshape([1, Rnet.numInput])
            NetOutput = Rnet.predict(message_id=message.message_id, vector=NetInput)

            probVector = self.Fuzzy_factor * FuzzyOutput + (1 - self.Fuzzy_factor) * NetOutput
            self.Fuzzy_factor *= self.Fuzzy_decay
            # make action by Fuzzy choice
            action = np.random.choice(a=[1, 2, 3], p=probVector)
            while action in exclude_actions:
                action = np.random.choice(a=[1, 2, 3], p=probVector)

            return action
        return chooseAction
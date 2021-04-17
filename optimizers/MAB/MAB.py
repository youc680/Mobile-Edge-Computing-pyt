from config import Config
from optimizers.optimizer import Optimizer
from optimizers.MAB.MAB_method import (
    getBehaviorPolicy,
    addToMemoryTmp, 
    updateReward,
)

class MAB(Optimizer):
    def __init__(self, agent_name, n_actions, policy_func=getBehaviorPolicy):
        self.agent_name = agent_name
        self.nActions = n_actions
        self.policy = policy_func(parameters=Config.policyParamatersMAB).getPolicy()
        self.values = [0] * self.nActions 
        self.memory = {}

    def addToMemoryTmp(self, message, state, action, func=addToMemoryTmp):
        func(self, message, state, action)

    def updateReward(self, message, delay, func=updateReward):
        func(self, message, delay)

    def getAllActionValues(self, state=None):
        return list(self.values)
        
        

    

      
    



        

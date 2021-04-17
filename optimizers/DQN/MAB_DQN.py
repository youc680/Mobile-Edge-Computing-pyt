import random
from optimizers.optimizer import Optimizer
from optimizers.DQN import DQN
from optimizers.MAB import MAB
from config import Config
from optimizers.DQN.MAB_DQN_method import (
    getBehaviorPolicy,
    updateReward,
    addToMemoryTmp,
)

class MAB_DQN(Optimizer):
    def __init__(self, agent_name, n_states, n_actions, policy_func=getBehaviorPolicy):
        super().__init__(agent_name, n_states, n_actions, policy_func)
        self.agent_name = agent_name
        self.nStates = n_states
        self.nActions = n_actions
        self.probChooseF = 1
        self.decayRateProbChooseF = 0.95
        self.policy = policy_func(parameters=Config.policyParamaters).getPolicy()
        self.MAB = MAB(agent_name, n_actions, getBehaviorPolicy)
        self.DQN = DQN(agent_name, n_states, n_actions, getBehaviorPolicy)

    def chooseOptimizer(self):
        prob = random.random()
        if prob < self.probChooseF:
            optimize = self.MAB
        else:
            optimize = self.DQN
        self.probChooseF *= self.decayRateProbChooseF
        return optimize

    def addToMemoryTmp(self, message, state, action, func=addToMemoryTmp):
        func(self, message, state, action)

    def updateReward(self, message, delay, func=updateReward):
        func(self, message, delay)

    def getAllActionValues(self, state):
        optimizer = self.chooseOptimizer()
        return optimizer.getAllActionValues(state)
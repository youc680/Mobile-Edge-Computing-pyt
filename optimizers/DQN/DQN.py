import os
import numpy as np
from config import Config
from optimizers.optimizer import Optimizer
from optimizers.DQN.DQN_method import (
    getBehaviorPolicy,
    updateState, addToMemoryTmp,
    updateReward, buildModel
)
from optimizers.utils import SequentialDequeMemory

class DQN(Optimizer):
    def __init__(self, agent_name, n_states, n_actions, policy_func=getBehaviorPolicy):
        super().__init__(agent_name, n_states, n_actions, policy_func)
        self.agent_name = agent_name
        self.nStates = n_states
        self.nActions = n_actions
        self.alpha = Config.learningRate
        self.gamma = Config.disCountingFactor
        self.policy = policy_func(parameters=Config.policyParamaters).getPolicy()
        self.onlineModel = buildModel(self, n_states=n_states, n_actions=n_actions)
        self.targetModel = buildModel(self, n_states=n_states, n_actions=n_actions)
        self.memory = SequentialDequeMemory(Config.queueCapacity)
        self.cnt = 0
        self.model_file = f"{os.getcwd()}/{Config.weightsFolder}/{agent_name}.h5"
        # self.loadModelWeights()

    def updateOnlineModel(self, experiences):
        X_train = []
        Y_train = [] 
        for experience in experiences:
            currentState, action, instantaneousReward, nextState = experience
            actionTargetValues = self.onlineModel.predict(currentState)
            actionValuesForState = actionTargetValues[0]
            actionValuesForNextState = self.targetModel.predict(nextState)[0]
            maxNextStateValue = np.max(actionValuesForNextState)
            targetActionValue = instantaneousReward + self.gamma * maxNextStateValue
            actionValuesForState[action] = targetActionValue
            actionTargetValues[0] = actionValuesForState
            X_train.append(currentState)
            Y_train.append(actionTargetValues)
        X_train = np.vstack(X_train)
        Y_train = np.vstack(Y_train)
        self.onlineModel.fit(X_train, Y_train, epochs=1, batch_size=Config.batchSize)


    def loadModelWeights(self):
        if os.path.exists(self.model_file):
            self.onlineModel.load_weights(self.model_file)
            self.targetModel.load_weights(self.model_file)


    def saveModelWeights(self):
        # self.onlineModel.save_weights(self.model_file, overwrite=True)
        pass

    def updateState(self, message, currentState, func=updateState):
        func(self, message, currentState)

    def updateReward(self, message, delay, func=updateReward):
        func(self, message, delay)
        self.update()

    def addToMemoryTmp(self, message, state, action, func=addToMemoryTmp):
        func(self, message, state, action)  

    def getAllActionValues(self, state):
        return self.onlineModel.predict(state)[0]

    def replayExperienceFromMemory(self):
        if self.memory.getMemorySize() < Config.batchSize:
            return
        experienceBatch = self.memory.getRandomBatchForReplay(batchSize=Config.batchSize)
        print("{} replay experience with {} experience".format(self.agent_name, len(experienceBatch)))
        self.updateOnlineModel(experienceBatch)

    def update(self):
        if self.cnt % Config.timeToUpdateOnlineModel == 0:
            self.replayExperienceFromMemory()
        if self.cnt % Config.timeToUpdateTargetModel == 0:
            # self.saveModelWeights()
            self.targetModel.set_weights(self.onlineModel.get_weights())
        

    

      
    



        

from behaviorPolicy.epsilonGreedy import EpsilonGreedy
from config import Config
import random
import math
import numpy as np
from behaviorPolicy.epsilonGreedy import EpsilonGreedy
from behaviorPolicy.epsilonDecay import EpsilonDecay
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import mean_squared_error

def getBehaviorPolicy(parameters):
    policy = EpsilonDecay( 
        epsilon=parameters["epsilon"],
        min_epsilon=parameters["min_epsilon"],
        epsilon_decay_rate=parameters["epsilon_decay_rate"],
    )
    return policy

def buildModel(DQN, n_states, n_actions):
    model = Sequential()
    hidden_layers = Config.hiddenLayerConfig
    model.add(Dense(hidden_layers[0], input_dim=n_states, activation="relu"))
    for layer_size in hidden_layers[1:]:
        model.add(Dense(layer_size, activation="relu"))
    model.add(Dense(n_actions, activation="linear"))
    model.compile(loss=mean_squared_error, optimizer=Adam(lr=Config.learningRate))
    return model


def updateState(DQN, message, currentState):
    print("Update State {} with message id {}".format(DQN.agent_name, message.stt))
    if DQN.memory.memoryTmp:
        preStateInfo = DQN.memory.memoryTmp[-1]
        # Update nextState in experience
        preStateInfo[0][3] = currentState
        if preStateInfo[0][2] is not None: # Reward not None
            DQN.memory.addToMemory(preStateInfo[0])
            del DQN.memory.memoryTmp[-1]
            DQN.cnt += 1

    print("Len memory Tmp:", len(DQN.memory.memoryTmp))
    # print(DQN.memory.memoryTmp)

def updateReward(DQN, message, delay):
    print("Update Reward {} with message id {}".format(DQN.agent_name, message.stt))
    for i, stateInfo in enumerate(DQN.memory.memoryTmp):
        if message.stt == stateInfo[1]:
            # Calculate reward
            reward = 1.0 / (delay + 0.01)
            # Update reward in experience
            print("Reward:", reward)
            stateInfo[0][2] = reward
            if stateInfo[0][3] is not None: # Next State not None
                DQN.memory.addToMemory(stateInfo[0])
                DQN.cnt += 1
                del DQN.memory.memoryTmp[i]
            break
    
    print("Len memory Tmp:",len(DQN.memory.memoryTmp))
    # print(DQN.memory.memoryTmp)

def addToMemoryTmp(DQN, message, state, action):
    experience = [state, action, None, None]
    DQN.memory.addToMemoryTmp([experience, message.stt])

    





            











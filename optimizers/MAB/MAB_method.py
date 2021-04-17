from config import Config
from behaviorPolicy.epsilonDecay import EpsilonDecay

def getBehaviorPolicy(parameters):
    policy = EpsilonDecay( 
        epsilon=parameters["epsilon"],
        min_epsilon=parameters["min_epsilon"],
        epsilon_decay_rate=parameters["epsilon_decay_rate"],
    )
    return policy

def addToMemoryTmp(MAB, message, state, action):
    MAB.memory[message.stt] = action

def updateReward(MAB, message, delay):
    print("Update reward for {}".format(MAB.agent_name))
    print("Pre update reward")
    print(MAB.memory)
    print(MAB.values)
    action = MAB.memory[message.stt]
    reward = 1 / (delay + 0.01)
    print(reward)
    MAB.values[action] = (1 - Config.learningRateMAB) * MAB.values[action] + Config.learningRateMAB * reward
    del MAB.memory[message.stt]
    print("After update reward")
    print(MAB.memory)
    print(MAB.values)

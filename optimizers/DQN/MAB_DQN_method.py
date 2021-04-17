from behaviorPolicy.epsilonDecay import EpsilonDecay

def getBehaviorPolicy(parameters):
    policy = EpsilonDecay( 
        epsilon=parameters["epsilon"],
        min_epsilon=parameters["min_epsilon"],
        epsilon_decay_rate=parameters["epsilon_decay_rate"],
    )
    return policy

def addToMemoryTmp(MAB_DQN, message, state, action):
    MAB_DQN.MAB.addToMemoryTmp(message, state, action)
    MAB_DQN.DQN.addToMemoryTmp(message, state, action)

def updateReward(MAB_DQN, message, delay):
    MAB_DQN.MAB.updateReward(message, delay)
    MAB_DQN.DQN.updateReward(message, delay)


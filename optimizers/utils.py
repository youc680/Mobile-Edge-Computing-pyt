from collections import deque
import numpy as np
import random

class SequentialDequeMemory:
    def __init__(self, queueCapacity=2000):
        self.queueCapacity = 2000
        self.memory = deque(maxlen=self.queueCapacity)
        self.memoryTmp = []

    def addToMemory(self, experienceTuple):
        self.memory.append(experienceTuple)

    def getRandomBatchForReplay(self, batchSize=32):
        return random.sample(self.memory, batchSize)

    def getMemorySize(self):
        return len(self.memory)

    def addToMemoryTmp(self, tmpTuple):
        self.memoryTmp.append(tmpTuple)


class Vector_processing:
    @staticmethod
    def softmax(vector):
        e_x = np.exp(np.array(vector))
        return e_x/e_x.sum()

    @staticmethod
    def percentage(vector):
        return np.array(vector)/np.array(vector).sum()


# print(Vector_processing.softmax(np.array([0.5, 0.6, 0.4, 0.1])))
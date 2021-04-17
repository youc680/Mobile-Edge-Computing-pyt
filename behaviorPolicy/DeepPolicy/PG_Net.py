import tensorflow as tf

"""
@notice: only call use following method:
1. predict(message_id, vector)
2. updateNet(message_id, delayVector)
3. summary()
"""


class DeepNet:
    def __init__(self, numInput=None, hiddenUnits=None, numOutput=None):
        assert numInput > 1, "Invalid input size"
        assert numOutput > 1, "Invalid output size"
        self.numInput = numInput
        self.numOutput = numOutput
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(units=numInput, activation='relu',
                                  kernel_regularizer=tf.keras.regularizers.l2(0.01),
                                  bias_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.LayerNormalization(),
            tf.keras.layers.Dense(units=hiddenUnits, activation='relu',
                                  kernel_regularizer=tf.keras.regularizers.l2(0.01),
                                  bias_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Dense(units=hiddenUnits, activation='relu',
                                  kernel_regularizer=tf.keras.regularizers.l2(0.01),
                                  bias_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(units=numOutput, activation='softmax')
        ])
        self.model.compile(optimizer=tf.keras.optimizers.Adam(),
                           loss=tf.keras.losses.categorical_crossentropy,
                           metrics=['accuracy'])
        self.storage = {}

    """
    inputData is a dictionary:
    {
      'x' : numpy array of size (*, numInput)
      'y' : numpy array of size (*, numOutput)
    }
    """

    def __feed(self, inputData=None):
        assert inputData['x'].shape[1] == self.numInput, "Invalid input x size"
        assert inputData['y'].shape[1] == self.numOutput, "Invalid input y size"
        self.model.fit(inputData['x'], inputData['y'], epochs=3)
        return True

    """
    When a vector is called in predict, it's truth-ground value is yet unknown,
    thus be stored in Net's storage: {message_id: vectorInput}.
    When a message received successfully at a vehicle, the message_id is sent 
    to Vnet for feeding the Net
    """

    def __store(self, message_id=None, vectorInput=None):
        self.storage[message_id] = vectorInput
        return True

    """
    Getting model information
    """

    def summary(self):
        self.model.summary()
        return True

    """
    Vector is a numpy vector of size (1, numInput)
    """

    def predict(self, message_id=None, vector=None):
        self.__store(message_id=message_id, vectorInput=vector)
        vector = vector.reshape([1, self.numInput])
        return self.model.predict(x=vector)

    """
    Updating weights
    delayVector = [[delayCar, delayRsu, delayGnb, delaySelf]]
    """

    def updateNet(self, message_id=None, delayVector=None):
        if len(self.storage.keys()) == 0:
            print("Storage empty !")
            return False
        retrieved_vector = self.storage.get(message_id)
        if retrieved_vector:
            self.__feed(inputData={
                'x': retrieved_vector,
                'y': delayVector
            })
            self.storage.pop(message_id)
            return True
        return False

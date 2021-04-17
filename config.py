import numpy as np

class Config:
    # gnb config
    gnbProcessPerSecond = 1280
    gnbCarMeanTranfer = 0.0009765625

    # rsu config
    rsuNumbers = 6
    xList = [125, 375, 625, 875, 1125, 1375]
    yList = [1, 1, 1, 1, 1, 1]
    zList = [10, 10, 10, 10, 10, 10]
    rsuCoverRadius = 151
    rsuProcessPerSecond = 320
    rsuRsuMeanTranfer = 0.00001
    rsuCarMeanTranfer = 0.0004768371582
    rsuGnbMeanTranfer = 0.00004768371582
    nActionsRsu = 3
    nStatesRsu = 7

    # car config
    carSpeed = 12
    carCoverRadius = 75
    carProcessPerSecond = 100
    carCarMeanTranfer = 0.00001
    carRsuMeanTranfer = 0.0009765625
    carGnbMeanTranfer = 0.0004768371582
    nActionsCar = 4
    nStatesCar = 9

    # DQN
    hiddenLayerConfig = [16, 8]
    policyParamaters = {
        "epsilon": 0.5,
        "min_epsilon": 0.05,
        "epsilon_decay_rate": 0.95
    }
    queueCapacity = 2000
    batchSize = 16
    learningRate = 0.001
    disCountingFactor = 0.9
    timeToUpdateOnlineModel = 10
    timeToUpdateTargetModel = 100

    # MAB
    learningRateMAB = 0.1
    policyParamatersMAB = {
        "epsilon": 0.5,
        "min_epsilon": 0.05,
        "epsilon_decay_rate": 0.95
    }
    # MAB + DQN
    probChooseF = 1
    decayRateProbChooseF = 0.95

    # message config
    ttl = 5
    maxDelay = 0.01
    maxSize = 8

    # other
    decayRateMean = 0.8
    carAppearStrategy = "inputFiles/car_deu6.inp"
    carPacketStrategy = "inputFiles/poisson_70.inp"
    simTime = 60
    cycleTime = 0.5
    roadLength = 1500
    dumpDelayDetail = "delayDetail.txt"
    dumpDelayGeneral = "delayGeneral.txt"
    weightsFolder = "weights"
    resultsFolder = "results"

    # policy based
    delay_factor_pad_car = np.array([0.4, 0.6])                  # delay factor = [factor waitTime, factor comTime]
    delay_factor_pad_rsu = np.array([0.4, 0.6])                  # delay factor = [factor waitTime, factor comTime]

    decision_factor = 0.2
    learning_rate_car = 0.1
    learning_rate_rsu = 0.2

    p_init_car = np.array([[0.25], [0.25], [0.25], [0.25]])
    p_init_rsu = np.array([[0], [0.3], [0.3], [0.4]])

    # Deep Policy
    dp_alpha = 0.2
    dp_decay = 0.05

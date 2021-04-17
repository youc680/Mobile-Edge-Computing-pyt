from fuzzy_system.fuzzy_variable_output import FuzzyOutputVariable
from fuzzy_system.fuzzy_variable_input import FuzzyInputVariable
from fuzzy_system.fuzzy_system import FuzzySystem
from optimizers.utils import Vector_processing


class FuzzyVehicleInference:
    def __init__(self, MAX_DELAY_REMAIN, MAX_PACKET_SIZE):
        self.MAX_DELAY_REMAIN = MAX_DELAY_REMAIN
        self.MAX_PACKET_SIZE = MAX_PACKET_SIZE
        self.system = None
        self.initFuzzySystem()
        self.vehicleRule()

    def initFuzzySystem(self):
        ### INPUT
        delayRemain = FuzzyInputVariable('Delay Remain', 0, self.MAX_DELAY_REMAIN, 100)
        delayRemain.add_trapezoidal('S', 0, 0, 0.003, 0.005)
        delayRemain.add_trapezoidal('M', 0, 0.004, 0.006, 0.008)
        delayRemain.add_trapezoidal('H', 0.007, 0.009, self.MAX_DELAY_REMAIN, self.MAX_DELAY_REMAIN)

        packageSize = FuzzyInputVariable('Package Size', 0, self.MAX_PACKET_SIZE, 100)
        packageSize.add_trapezoidal('S', 0, 0, 1, 2)
        packageSize.add_trapezoidal('M', 1, 3, 4, 6)
        packageSize.add_trapezoidal('H', 5, 6, self.MAX_PACKET_SIZE, self.MAX_PACKET_SIZE)

        ### OUTPUT
        p_car = FuzzyOutputVariable('Car Probability', 0, 1, 100)
        p_car.add_trapezoidal('S', 0, 0, 0.1, 0.2)
        p_car.add_trapezoidal('MS', 0.1, 0.2, 0.3, 0.4)
        p_car.add_trapezoidal('M', 0.3, 0.4, 0.5, 0.6)
        p_car.add_trapezoidal('MH', 0.5, 0.6, 0.7, 0.8)
        p_car.add_trapezoidal('H', 0.7, 0.8, 1, 1)

        p_RSU = FuzzyOutputVariable('RSU Probability', 0, 1, 100)
        p_RSU.add_trapezoidal('S', 0, 0, 0.1, 0.2)
        p_RSU.add_trapezoidal('MS', 0.1, 0.2, 0.3, 0.4)
        p_RSU.add_trapezoidal('M', 0.3, 0.4, 0.5, 0.6)
        p_RSU.add_trapezoidal('MH', 0.5, 0.6, 0.7, 0.8)
        p_RSU.add_trapezoidal('H', 0.7, 0.8, 1, 1)

        p_gnb = FuzzyOutputVariable('GNB Probability', 0, 1, 100)
        p_gnb.add_trapezoidal('S', 0, 0, 0.1, 0.2)
        p_gnb.add_trapezoidal('MS', 0.1, 0.2, 0.3, 0.4)
        p_gnb.add_trapezoidal('M', 0.3, 0.4, 0.5, 0.6)
        p_gnb.add_trapezoidal('MH', 0.5, 0.6, 0.7, 0.8)
        p_gnb.add_trapezoidal('H', 0.7, 0.8, 1, 1)

        p_self = FuzzyOutputVariable('Self Probability', 0, 1, 100)
        p_self.add_trapezoidal('S', 0, 0, 0.1, 0.2)
        p_self.add_trapezoidal('MS', 0.1, 0.2, 0.3, 0.4)
        p_self.add_trapezoidal('M', 0.3, 0.4, 0.5, 0.6)
        p_self.add_trapezoidal('MH', 0.5, 0.6, 0.7, 0.8)
        p_self.add_trapezoidal('H', 0.7, 0.8, 1, 1)

        ### INIT FUZZY SYSTEM
        self.system = FuzzySystem()
        self.system.add_input_variable(delayRemain)
        self.system.add_input_variable(packageSize)
        self.system.add_output_variable(p_car)
        self.system.add_output_variable(p_RSU)
        self.system.add_output_variable(p_gnb)
        self.system.add_output_variable(p_self)

    def vehicleRule(self):
        self.system.add_rule(
            {'Delay Remain': 'S',
             'Package Size': 'S'},
            {'Car Probability': 'MS',
             'RSU Probability': 'S',
             'GNB Probability': 'S',
             'Self Probability': 'H'}
        )

        self.system.add_rule(
            {'Delay Remain': 'S',
             'Package Size': 'M'},
            {'Car Probability': 'MS',
             'RSU Probability': 'M',
             'GNB Probability': 'S',
             'Self Probability': 'M'}
        )

        self.system.add_rule(
            {'Delay Remain': 'S',
             'Package Size': 'H'},
            {'Car Probability': 'S',
             'RSU Probability': 'H',
             'GNB Probability': 'MS',
             'Self Probability': 'MS'}
        )

        self.system.add_rule(
            {'Delay Remain': 'M',
             'Package Size': 'S'},
            {'Car Probability': 'M',
             'RSU Probability': 'M',
             'GNB Probability': 'MS',
             'Self Probability': 'M'}
        )

        self.system.add_rule(
            {'Delay Remain': 'M',
             'Package Size': 'M'},
            {'Car Probability': 'MS',
             'RSU Probability': 'MH',
             'GNB Probability': 'MS',
             'Self Probability': 'MS'}
        )

        self.system.add_rule(
            {'Delay Remain': 'M',
             'Package Size': 'H'},
            {'Car Probability': 'S',
             'RSU Probability': 'H',
             'GNB Probability': 'MH',
             'Self Probability': 'S'}
        )

        self.system.add_rule(
            {'Delay Remain': 'H',
             'Package Size': 'S'},
            {'Car Probability': 'MH',
             'RSU Probability': 'M',
             'GNB Probability': 'MS',
             'Self Probability': 'MH'}
        )

        self.system.add_rule(
            {'Delay Remain': 'H',
             'Package Size': 'M'},
            {'Car Probability': 'MS',
             'RSU Probability': 'MH',
             'GNB Probability': 'M',
             'Self Probability': 'S'}
        )

        self.system.add_rule(
            {'Delay Remain': 'H',
             'Package Size': 'H'},
            {'Car Probability': 'MS',
             'RSU Probability': 'MH',
             'GNB Probability': 'M',
             'Self Probability': 'S'}
        )

    def Inference(self, fuzzy_input=None, showResult=False, plot=False):
        delayRemain = fuzzy_input["dR"]
        packageSize = fuzzy_input["size"]

        if delayRemain > self.MAX_DELAY_REMAIN:
            delayRemain = self.MAX_DELAY_REMAIN
        if packageSize > self.MAX_PACKET_SIZE:
            packageSize = self.MAX_PACKET_SIZE

        #print("delayRemain: " + str(delayRemain))
        #print("packageSize: " + str(packageSize))

        output = self.system.evaluate_output({
            'Delay Remain': delayRemain,
            'Package Size': packageSize
        })

        outputVector = [output['Car Probability'], output['RSU Probability'],
                        output['GNB Probability'], output['Self Probability']]

        # def softmax(x):
        #     """Compute softmax values for each sets of scores in x."""
        #     print("x " + str(x))
        #     e_x = np.exp(x - np.max(x))
        #     print("e_x = " + str(e_x))
        #     return e_x / e_x.sum(axis=0)

        outputVector = Vector_processing.percentage(outputVector)

        if showResult:
            print(outputVector)
        if plot:
            self.system.plot_system()

        return outputVector


### TEST
#FuzzySystemTest = FuzzyVehicleInference(1, 10)
#FuzzySystemTest.Inference(0.1, 10, True, False)

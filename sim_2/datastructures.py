# ANTONIOU CHRISTODOULOS
# AM 2641
# MICROPROCESSORS ΜΥE021


from signalprobs import spNOT
from signalprobs import spAND
from signalprobs import spOR
from signalprobs import spXOR
from signalprobs import spNAND
from signalprobs import spNOR
from signalprobs import spXNOR


class Element:
     def __init__(self, type, input, output):
         self.type = type
         self.input = input
         self.output = output
         self.marked = False


class Signal:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @classmethod
    def create(cls, name, index, isTopInput):
        signal = cls(name, 0)
        signal.index = index
        signal.isTopInput = isTopInput
        signal.marked = False
        return signal


class Simulation:
    def __init__(self):
        self.elements = []
        self.signals = []


    def process(self, element):
        signals = self.signals
        if element.type == 'NOT':
            sp = spNOT(signals[element.input[0]].value)
        else:
            inputs = self.getElementInputs(element)

            if element.type == 'AND':
                sp = spAND(inputs)
            elif element.type == 'OR':
                sp = spOR(inputs)
            elif element.type == 'XOR':
                sp = spXOR(inputs)
            elif element.type == 'NAND':
                sp = spNAND(inputs)
            elif element.type == 'NOR':
                sp = spNOR(inputs)
            elif element.type == 'XNOR':
                sp = spXNOR(inputs)

        signals[element.output].value = sp
        self.signals = signals


    def getElementInputs(self, element):
        inputs = []
        for input in element.input:
            inputs.append(self.signals[input].value)
        return inputs
    

    def findSignal(self, name):
        for signal in self.signals:
            if name == signal.name:
                return signal


    def runSimulation(self, inputs):
        self.setTopInputValues(inputs)
        validOutputs = self.checkValidOutputs()
        if not validOutputs:
            return

        for element in self.elements:
            self.process(element)
        return self


    def setTopInputValues(self, inputs):
        topInputsCount = self.countTopInputs()
        if len(inputs ) != topInputsCount:
            print("Number of inputs does not match top level inputs of the model.")
            return

        count = 0
        for signal in self.signals:
            if signal.isTopInput:
                signal.value = inputs[count]
                count += 1


    def countTopInputs(self):
        count = 0
        for signal in self.signals:
            if signal.isTopInput:
                count += 1
        return count


    def checkValidOutputs(self):
        for e1 in self.elements:
            count = 0
            for e2 in self.elements:
                if e1.output == e2.output:
                    count += 1
            if count > 1:
                print("Duplicate output found in model for element:\n", 
                        e1.type, e1.input, e1.output)
                return False
        return True


    def resetSignals(self):
        for signal in self.signals:
            signal.value = 0


class Individual:
    def __init__(self):
        self.workload = []
        self.score = -1
        self.isParent = False


class Population:
    def __init__(self):
        self.individuals = []
        self.bestScore = -1
        self.bestIndividual = []
        self.secondBestScore = -1
        self.secondBestIndividual = []
        
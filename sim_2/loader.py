# ANTONIOU CHRISTODOULOS
# AM 2641
# MICROPROCESSORS ΜΥE021
#
# Loads a logic circuit from the given model file.
# Model examples can be found in the models directory.
#
# run command:
# python3 loader.py <model file>
#   <model file>: path of the model file to be loaded
#
# run example:
# python3 loader.py models/model1


from datastructures import Element
from datastructures import Signal
from datastructures import Simulation

import signalprobs as SP
import sys


SUPPORTED_GATE_TYPES = ['NOT', 'AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR']


def loadModelFromFile(MODEL):
    simulation = Simulation()
    words = readWordsFromFile(MODEL)

    topInputsFound = checkTopInputs(words, simulation.signals)
    if topInputsFound:
        del words[0]

    buildModel(words, simulation)
    if not topInputsFound:
        findTopInputs(simulation)

    sortElements(simulation)

    return simulation


def readWordsFromFile(MODEL):
    file = open(MODEL, 'r')
    contents = file.read()
    file.close()
    lines = contents.split("\n")

    words = []
    for line in lines:
        words.append(line.split(" "))
    return words


def checkTopInputs(words, signals):
    if words[0][0] == 'top_inputs':
        for i in range(1, len(words[0])):
            name = words[0][i]
            if not isNameInSignals(name, signals):
                signal = Signal.create(name, len(signals), True)
                signals.append(signal)        
        return True
    return False


def isNameInSignals(name, signals):
    for signal in signals:
        signalName = signal.name
        if name == signalName:
            return True
    return False


def buildModel(words, simulation):
    for line in words:
        inputs = []
        isFirstSignal = False
        for word in line:
            if word in SUPPORTED_GATE_TYPES:
                type = word
                isFirstSignal = True
            else:
                if not isNameInSignals(word, simulation.signals):
                    index = len(simulation.signals)
                    signal = Signal.create(word, index, False)
                    simulation.signals.append(signal)        
                signal = simulation.findSignal(word)

                if isFirstSignal:
                    output = signal.index
                    isFirstSignal = False   
                else:
                    inputs.append(signal.index)
                
        element = Element(type, inputs, output)
        simulation.elements.append(element)


def findTopInputs(simulation):
    for signal in simulation.signals:
        isTopInput = True
        for element in simulation.elements:
            if signal.index == element.output:
                isTopInput = False
        signal.isTopInput = isTopInput


def setTopInputValues(simulation, inputs):
    topInputsCount = countTopInputs(simulation.signals)
    if len(inputs ) != topInputsCount:
        print("Number of inputs does not match top level inputs of the model.")
        return

    count = 0
    for signal in simulation.signals:
        if signal.isTopInput:
            signal.value = inputs[count]
            count += 1
    

def countTopInputs(signals):
    count = 0
    for signal in signals:
        if signal.isTopInput:
            count += 1
    return count


def checkValidOutputs(elements):
    for e1 in elements:
        count = 0
        for e2 in elements:
            if e1.output == e2.output:
                count += 1
        if count > 1:
            print("Duplicate output found in model for element:\n", 
                    e1.type, e1.input, e1.output)
            return False
    return True


def printModel(simulation):
    print("\n***********  MODEL LOADED  ************\n")
    print("SIGNALS:\nname | index | is top input? | initial value | marked?")
    for signal in simulation.signals:
        print('',signal.name, '\t', signal.index, '\t', signal.isTopInput, '\t\t', signal.value, '\t\t', signal.marked)

    print("\nELEMENTS:\ntype | marked? | output index | input indexes")
    for element in simulation.elements:
        print('',element.type, '\t', element.marked, '\t  ', element.output, '\t\t', element.input)


def printElementsWithNames(simulation):
    print("\nELEMENTS:\ntype | output | inputs")
    for element in simulation.elements:
        inputs = []
        for input in element.input:
            inputs.append(simulation.signals[input].name)
        output = simulation.signals[element.output].name
        print('',element.type, '\t', output, '\t', ', '.join(inputs), '\t')


def printSignalValues(simulation):
    message = ''
    for signal in simulation.signals:
        message += str(signal.value) + ' ' 
    print('\nSignals:', message)


def testbench(simulation):
    # works only for model1
    print("a b c | e f | d")
    for a in range(2):
        for b in range(2):
            for c in range(2):
                simulation.runSimulation([a, b, c])
                e = simulation.findSignal('e')
                f = simulation.findSignal('f')
                d = simulation.findSignal('d')
                print(str(a), str(b), str(c) , "|", str(e.value), str(f.value), "|", str(d.value))


def switchingActivity(simulation, spA, spB, spC):
    simulation.runSimulation([spA, spB, spC])

    e = simulation.findSignal('e')
    f = simulation.findSignal('f')
    d = simulation.findSignal('d')

    switch_act_e = SP.switchingActivity(e.value)
    switch_act_f = SP.switchingActivity(f.value)
    switch_act_d = SP.switchingActivity(d.value)

    print("Switching activity of signal e:", switch_act_e, "\n"
        "Switching activity of signal f:", switch_act_f, "\n"
        "Switching activity of signal d:", switch_act_d, "\n")


def sortElements(simulation):
    elementsSorted = []
    markTopInputs(simulation.signals)
    while unmarkedElementsRemaining(simulation.elements):
        markElements(simulation, elementsSorted)

    simulation.elements = elementsSorted


def markTopInputs(signals):
    for signal in signals:
        if signal.isTopInput:
            signal.marked = True


def markElements(simulation, elementsSorted):
    for element in simulation.elements:
        inputsMarked = True
        for index in element.input:
            if not simulation.signals[index].marked:
                inputsMarked = False
                break

        if not element in elementsSorted:
            if inputsMarked:
                element.marked = inputsMarked
                elementsSorted.append(element)
                simulation.signals[element.output].marked = True


def unmarkedElementsRemaining(elements):
    for element in elements:
        if not element.marked:
            return True
    return False



if __name__ == '__main__':
    args = sys.argv[1:]
    MODEL = args[0]

    simulation = loadModelFromFile(MODEL)
    printModel(simulation)
    printElementsWithNames(simulation)

    if MODEL == 'model1':
        print("\n***********  TRUTH TABLE  ************\n")
        testbench(simulation)

        print("\n*****  AVERAGE SWITCHING ACTIVITY  *****\n")
        switchingActivity(simulation, 0.5, 0.5, 0.5)

        print("\n*****  SWITCHING ACTIVITY WITH AM *****\n")
        switchingActivity(simulation, 0.2641, 0.2641, 0.2641)


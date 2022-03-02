# ANTONIOU CHRISTODOULOS
# AM 2641
# MICROPROCESSORS ΜΥE021
#
# Stress test input generation for a given logic circuit using random workload.
# Outputs a graph with the score of each individual workload, variance and mean.
# The logic circuit model is loaded using loader.py.
#
# run command:
# python3 random_workload.py <model file>
#   <model file>: path of the model file to be loaded
#
# run example:
# python3 random_workload.py models/model2


from loader import loadModelFromFile
from loader import printModel
from loader import printElementsWithNames
from loader import countTopInputs

import random as R
import matplotlib.pyplot as plot
import sys

from copy import deepcopy
from numpy import var
from numpy import mean



def generateRandomWorkload(inputsNumber, length):
    workload = []
    for row in range(length):
        row = []
        for column in range(inputsNumber):
            row.append(R.randint(0, 1))
        workload.append(row)
    return workload


def runTest(REPS, simulation):
    scores = []
    for i in range(REPS):
        workload = generateRandomWorkload(topInputsCount, length)

        simulation.runSimulation(workload[0])
        signalsBefore = deepcopy(simulation.signals)
        simulation.runSimulation(workload[1])
        signalsAfter = deepcopy(simulation.signals)

        switchesCounter = countSwitches(signalsBefore, signalsAfter)
        scores.append(switchesCounter)
    return scores


def countSwitches(signalsBefore, signalsAfter):
    switches = 0
    for i in range(len(signalsBefore)):
        if signalsBefore[i].isTopInput:
            continue
        if signalsBefore[i].value != signalsAfter[i].value:
            switches += 1
            
    return switches



if __name__ == '__main__':
    args = sys.argv[1:]
    MODEL = args[0]

    simulation = loadModelFromFile(MODEL)
    printModel(simulation)
    printElementsWithNames(simulation)

    topInputsCount = countTopInputs(simulation.signals)
    length = 2
    REPS = 2000
    scores = runTest(REPS, simulation)

    averageSwitches = mean(scores)
    varianceSwitches = var(scores)

    plot.plot(scores)
    plot.title('Mean: '+str(averageSwitches)+'\nVariance: '+str(varianceSwitches))
    plot.xlabel('Individuals')
    plot.ylabel('Scores')
    plot.show()


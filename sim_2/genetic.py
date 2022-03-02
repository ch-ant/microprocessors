# ANTONIOU CHRISTODOULOS
# AM 2641
# MICROPROCESSORS ΜΥE021
#
# Stress test input generation for a given logic circuit using a genetic algorithm.
# Three tests are performed for each execution.
# Outputs generation scores and best individual workload.
# Outputs a graph with the best generation score per generation for each of the three executions.
#
# run command:
# python3 genetic.py <model file> <N> <L> <m> <g>
#   <model file>: path of the model file to be loaded
#   <N>: population size
#   <L>: workload size
#   <m>: mutate rate
#   <g>: generations size
#
#  run example:
#  python3 genetic.py models/model2 30 2 0.05 100


from loader import loadModelFromFile, printSignalValues
from loader import printModel
from loader import printElementsWithNames
from loader import countTopInputs

from datastructures import Individual
from datastructures import Population

from random_workload import generateRandomWorkload
from random_workload import countSwitches
from random import randint
from random import random
from copy import deepcopy

import matplotlib.pyplot as plot
import sys



def runAlgorithm(simulation, populationSize, workloadSize, generationsSize):
    generations = []
    topInputsCount = countTopInputs(simulation.signals)
    population = seedPopulation(populationSize, workloadSize, topInputsCount)

    for i in range(generationsSize):
        print('Running for generation:', (i+1), end='\r')
        measurePopulation(simulation, population)
        generations.append(population)
        population = crossoverParents(population, workloadSize)
        population = mutatePopulation(population, mutateRate)

    print('\nExecution finished\n')
    return generations


def seedPopulation(populationSize, workloadSize, topInputsCount):
    population = Population()
    for i in range(populationSize):
        individual = Individual()
        individual.workload = generateRandomWorkload(topInputsCount, workloadSize)
        population.individuals.append(individual)
    return population


def measurePopulation(simulation, population):
    for individual in population.individuals:
        switchesCounter = 0
        simulation.resetSignals()

        for input in individual.workload:
            signalsBefore = deepcopy(simulation.signals)
            simulation.runSimulation(input)
            signalsAfter = deepcopy(simulation.signals)
            switchesCounter += countSwitches(signalsBefore, signalsAfter)

        individual.score = switchesCounter
        updateBestIndividuals(population, individual)


def updateBestIndividuals(population, individual):
    if individual.score > population.bestScore:
        population.secondBestScore = population.bestScore
        population.secondBestIndividual = population.bestIndividual
        population.bestScore = individual.score
        population.bestIndividual = individual
    elif individual.score >= population.secondBestScore:
        population.secondBestScore = individual.score
        population.secondBestIndividual = individual


def selectParents(individualScores, population):
    best = sbest = -1
    besti = sbesti = -1
    for i in range(len(individualScores)):
        if individualScores[i] > best:
            sbest = best
            sbesti = besti
            best = individualScores[i]
            besti = i
        elif individualScores[i] >= sbest:
            sbest = individualScores[i]
            sbesti = i

    parent1 = population[besti]
    parent2 = population[sbesti]

    return [parent1, parent2]


def crossoverParents(population, workloadSize):
    newPopulation = Population()
    addParents(population, newPopulation)

    while len(newPopulation.individuals) < len(population.individuals):
        individual = Individual()

        crossoverLine = randint(0, workloadSize-1)
        parent1, parent2 = setParentsOrder(population)
        individual.workload = generateChild(parent1, parent2, crossoverLine, workloadSize)

        newPopulation.individuals.append(individual)

    return newPopulation


def addParents(population, newPopulation):
    newPopulation.individuals.append(population.bestIndividual)
    newPopulation.individuals[0].isParent = True
    newPopulation.individuals[0].score = population.bestScore
    newPopulation.individuals.append(population.secondBestIndividual)
    newPopulation.individuals[1].isParent = True
    newPopulation.individuals[1].score = population.secondBestScore
        

def generateChild(parent1, parent2, crossoverLine, workloadSize):
    child = []
    for i in range(workloadSize):
        if i <= crossoverLine:
            child.append(parent1.workload[i])
        else:
            child.append(parent2.workload[i])
    return child


def mutatePopulation(population, mutateRate):
    mutatedPopulation = Population()
    mutatedPopulation.individuals.append(population.individuals[0])
    mutatedPopulation.individuals.append(population.individuals[1])

    for individual in population.individuals:
        if individual.isParent:
            continue

        mutatedIndividual = Individual()
        for input in individual.workload:
            mutatedInput = []
            for value in input:
                chance = random()
                if chance <= mutateRate:
                    value = changeBit(value)

                mutatedInput.append(value)
            mutatedIndividual.workload.append(mutatedInput)
        mutatedPopulation.individuals.append(mutatedIndividual)
    return mutatedPopulation


def changeBit(bit):
    if bit == 0:
        return 1
    else: return 0


def setParentsOrder(population):
    chance = randint(0, 1)
    if chance == 0:
        return population.bestIndividual, population.secondBestIndividual
    else:
        return population.secondBestIndividual, population.bestIndividual


def printIndividual(individual):
    print('Individual: ( score:', individual.score, ', Parent?', individual.isParent, ')')
    for row in individual.workload:
        print(row)


def printPopulation(population):
    print('\n')
    for individual in population.individuals:
        printIndividual(individual)


def printSignalValuesEcxludingTopInputs(simulation):
    message = ''
    for signal in simulation.signals:
        if signal.isTopInput:
            continue
        message += str(signal.value) + ' ' 
    print('Signals:', message)


def printExecutionResults(generations, genScores, i):
    print('\n\n***********  EXECUTION ' + i + '  ************')
    print('\nGeneration scores:', genScores)
    print('\nBest individual:', generations[-1].bestIndividual.workload)


def getGenScores(generations):
    genScores =[]
    for pop in generations:
        genScores.append(pop.bestScore)
    return genScores



if __name__ == '__main__':
    args = sys.argv[1:]
    MODEL = args[0]
    populationSize = int(args[1])   # N
    workloadSize = int(args[2])     # L
    mutateRate = float(args[3])     # m
    generationsSize = int(args[4])  # g

    simulation = loadModelFromFile(MODEL)
    printModel(simulation)
    # printElementsWithNames(simulation)

    generations_1 = runAlgorithm(simulation, populationSize, workloadSize, generationsSize)
    generations_2 = runAlgorithm(simulation, populationSize, workloadSize, generationsSize)
    generations_3 = runAlgorithm(simulation, populationSize, workloadSize, generationsSize)

    genScores_1 = getGenScores(generations_1)
    genScores_2 = getGenScores(generations_2)
    genScores_3 = getGenScores(generations_3)

    printExecutionResults(generations_1, genScores_1, '1')
    printExecutionResults(generations_2, genScores_2, '2')
    printExecutionResults(generations_3, genScores_3, '3')

    plot.plot(genScores_1, label = 'Execution 1')
    plot.plot(genScores_2, label = 'Execution 2')
    plot.plot(genScores_3, label = 'Execution 3')

    plot.xlabel('Generation')
    plot.ylabel('Generation score')
    plot.legend(loc = 'best')
    plot.show()


import copy
import math
import random

from multiprocessing.dummy import Pool as ThreadPool

from algorithms.Algorithm import Algorithm


class SimulatedAnnealingAlgorithm(Algorithm):

    def __init__(self, problem, popSize, initialTemp):
        super().__init__(problem, popSize)
        self._initialTemp = initialTemp

    def findSolution(self, maxIter):
        # init and run threads
        pool = ThreadPool(self._popSize)
        args = [(maxIter, True) if random.random() < 0.4 else (maxIter, False) for _ in range(self._popSize)]

        results = pool.starmap(self.simulatedAnnealing, args)
        # get the best solution
        best = min(results)[1]
        return best


    def simulatedAnnealing(self, maxIter, isGreedy):

        if isGreedy:
            currentSol = self._problem.generateGreedyVec()
        else:
            currentSol = self._problem.generateRandomVec()

        globalSolution = copy.deepcopy(currentSol)
        currFitness = globalFitness = self._problem.calculateFitness(currentSol)

        iterCounter = 0
        while globalFitness > 0 and iterCounter < maxIter:
            neighbor = self._problem.generateOneNeighbor(currentSol)
            neighborFitness = self._problem.calculateFitness(neighbor)

            # check for new global best
            if neighborFitness < globalFitness:
                globalSolution, globalFitness = copy.deepcopy(neighbor), neighborFitness

            delta = neighborFitness - currFitness
            currentTemp = self._initialTemp / float(iterCounter + 1)
            if delta > 0:
                a = math.exp(- delta / currentTemp)
                b = 3

            if delta < 0 or random.random() < math.exp(- delta / currentTemp):
                currentSol, currFitness = neighbor, neighborFitness

            iterCounter += 1


        return globalFitness, globalSolution

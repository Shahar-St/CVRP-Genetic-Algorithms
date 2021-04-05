import copy
import threading
from multiprocessing.pool import ThreadPool

from algorithms.Algorithm import Algorithm
from entities.IndividualEntity import IndividualEntity


class TabuSearchAlgorithm(Algorithm):

    def __init__(self, problem, popSize, maxTabuSize):
        super().__init__(problem, popSize)

        self._problem = problem
        self._maxTabuSize = maxTabuSize
        self._tabuList = []

    def findSolution(self, maxIter):
        # init and run threads
        pool = ThreadPool(self._popSize)
        args = [(maxIter, False) for _ in range(self._popSize - 1)]
        args.append((maxIter, True))

        results = pool.starmap(self.tabuSearch, args)
        # get the best solution
        best = min(results)[1]
        return best

    def tabuSearch(self, maxIter, isGreedy):

        # init initial state
        if isGreedy:
            currentSol = IndividualEntity(self._problem.generateGreedyVec())
        else:
            currentSol = IndividualEntity(self._problem.generateRandomVec())
        globalSolution = copy.deepcopy(currentSol)
        globalFitness = self._problem.calculateFitness(currentSol.getVec())

        # iterative improvement
        iterCounter = 0
        while globalFitness != 0 and iterCounter < maxIter:

            currentSol = self._findBestNeighbor(currentSol)
            if currentSol is None:
                return globalSolution

            currentFitness = self._problem.calculateFitness(currentSol.getVec())

            # check for best overall solution
            if currentFitness < globalFitness:
                globalSolution, globalFitness = copy.deepcopy(currentSol), currentFitness

            iterCounter += 1

        return globalFitness, globalSolution.getVec()

    # finding the best neighbor from all neighbors
    def _findBestNeighbor(self, currentSol):

        neighborsVectors = self._problem.generateNeighbors(currentSol.getVec())
        neighbors = [IndividualEntity(vec) for vec in neighborsVectors]
        for i in range(len(neighbors)):
            neighbors[i].setFitness(self._problem.calculateFitness(neighbors[i].getVec()))
        neighbors.sort()

        for nei in neighbors:
            if self._problem.calculateFitness(nei.getVec()) < self._problem.calculateFitness(
                    currentSol.getVec()) or nei not in self._tabuList:
                if nei not in self._tabuList:
                    self._addToTabuList(nei)
                return nei

        return None

    # adding neighbor that its fitness worse than current to the tabu list
    def _addToTabuList(self, nei):
        if len(self._tabuList) >= self._maxTabuSize:
            self._tabuList.pop(0)
        self._tabuList.append(nei)

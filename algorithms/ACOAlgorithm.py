import itertools
import random

from algorithms.Algorithm import Algorithm


class ACOAlgorithm(Algorithm):

    def __init__(self, problem, popSize, heuristicIntensity, historyIntensity, decayRate, localPheRate):
        super().__init__(problem, popSize)
        self._heuristicIntensity = heuristicIntensity
        self._historyIntensity = historyIntensity
        self._pheromoneDict = None
        self._decayRate = decayRate
        self._localPheRate = localPheRate

    def findSolution(self, maxIter):

        globalAnt = self._problem.generateGreedyVec()
        globalFitness = self._problem.calculateFitness(globalAnt)
        problemSize = self._problem.getTargetSize()
        initialPheromone = 1 / (problemSize * globalFitness)
        self._initPheromoneDict(initialPheromone)

        iterCounter = 0
        while iterCounter < maxIter and globalFitness > 0:

            for i in range(self._popSize):

                antVec = self._createAntVector()
                antFitness = self._problem.calculateFitness(antVec)

                if antFitness < globalFitness:
                    globalAnt, globalFitness = antVec, antFitness

                self._updateLocalPheromone(antVec, initialPheromone)
            self._updateGlobalPheromone(globalAnt, globalFitness)
            iterCounter += 1

        return globalAnt

    def _initPheromoneDict(self, initialPheromone):
        edges = list(itertools.combinations(range(1, self._problem.getTargetSize() + 1), 2))
        self._pheromoneDict = {frozenset(edge): initialPheromone for edge in edges}

    def _createAntVector(self):

        problemSize = self._problem.getTargetSize()
        # set first city
        vec = [random.randint(1, problemSize)]
        cities = [i for i in range(1, problemSize + 1) if i != vec[0]]

        greedyProb = 0.5
        while len(cities) != 0:
            choices = self._calculateChoices(vec[-1], cities, vec)
            if random.random() < greedyProb:
                # greedy selection
                nextCity = max(choices, key=choices.get)
            else:
                # prob choice
                sumOfChoices = sum(choices.values())
                distribution = [i / sumOfChoices for i in choices.values()]
                nextCity = random.choices(list(choices.keys()), weights=distribution)[0]
            vec.append(nextCity)
            cities.remove(nextCity)

        return vec

    def _calculateChoices(self, lastCity, cities, currPath):

        choices = {}
        for city in cities:
            # get path w stops without 0 in the beginning and end
            currPathWithStops = self._problem.getVecWithStops(currPath + [city])
            currPathWithStops.pop()
            currPathWithStops.pop(0)

            if currPathWithStops[-2] == 0:
                distance = self._problem.calcDist(lastCity, 0) + self._problem.calcDist(0, city)
            else:
                distance = self._problem.calcDist(lastCity, city)

            history = self._pheromoneDict[frozenset((lastCity, city))] ** self._historyIntensity
            heuristic = (1 / distance) ** self._heuristicIntensity
            prob = history * heuristic
            choices[city] = prob

        return choices

    def _updateLocalPheromone(self, antVec, initialPheromone):

        for i in range(len(antVec) - 1):
            followingNode = antVec[i + 1]
            edge = frozenset((antVec[i], followingNode))
            newPheromone = ((1 - self._localPheRate) * self._pheromoneDict[edge]) + (
                        self._localPheRate * initialPheromone)
            self._pheromoneDict[edge] = newPheromone

    def _updateGlobalPheromone(self, globalAntVec, globalFitness):

        for i in range(len(globalAntVec) - 1):
            followingNode = globalAntVec[i + 1]
            edge = frozenset((globalAntVec[i], followingNode))
            newPheromone = ((1 - self._decayRate) * self._pheromoneDict[edge]) + (self._decayRate * (1 / globalFitness))
            self._pheromoneDict[edge] = newPheromone

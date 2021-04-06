import copy
import importlib
import itertools
import math
import os
import random

import numpy as np

from util.Consts import X, Y
from util.Util import getValidIndexes


class CVRP:

    def __init__(self, target):
        filePath = os.getcwd() + '\\util\\inputfiles\\' + str(target) + '.txt'
        inputFile = open(filePath, 'r')

        coordinatesSection = 7
        content = inputFile.readlines()
        content = [line.strip('\n') for line in content]

        # get optimal solution
        self._optimalVal = int(''.join(content[1].strip(')')[content[1].find('value:') + 7:]))

        # get dim
        self._dim = int(''.join(content[3][content[3].find(':') + 2:]))

        # get vehicle capacity
        self._vehicleCapacity = int(''.join(content[5][content[5].find(':') + 2:]))

        nodesCoordinates = []
        # get coords
        for i in range(coordinatesSection, coordinatesSection + self._dim):
            nodeCoordsStr = content[i][content[i].find(' ') + 1:]
            coordsList = nodeCoordsStr.split(' ')
            nodeX = int(coordsList[X])
            nodeY = int(coordsList[Y])
            nodesCoordinates.append((nodeX, nodeY))

        # get capacity
        nodesDemands = []
        for i in range(coordinatesSection + self._dim + 1, coordinatesSection + self._dim * 2 + 1):
            nodeWeight = content[i].split(' ')
            nodesDemands.append(int(nodeWeight[1]))

        self._nodesCoordinates = np.array(nodesCoordinates)
        self._nodesDemands = np.array(nodesDemands)

    def generateRandomVec(self):
        # each solution is represented by a permutation [1, dim - 1]
        vec = np.random.permutation(list(range(1, self._dim)))
        return vec.tolist()

    def _getVecWithStops(self, vec):

        vecWithStops = [0, vec[0]]
        currentTruckCapacity = self._nodesDemands[vec[0]]

        for i in range(len(vec) - 1):
            # update route capacity
            currentTruckCapacity += self._nodesDemands[vec[i + 1]]
            # check if exceeded capacity
            if currentTruckCapacity > self._vehicleCapacity:
                vecWithStops.append(0)
                currentTruckCapacity = self._nodesDemands[vec[i + 1]]

            vecWithStops.append(vec[i + 1])

        vecWithStops.append(0)
        return vecWithStops


    def calculateFitness(self, vec):

        vecWithStops = self._getVecWithStops(vec)

        distance = 0
        for i in range(len(vecWithStops) - 1):
            distance += self._calcDist(vecWithStops[i], vecWithStops[i + 1])

        return int(distance - self._optimalVal)

    def _calcDist(self, node1, node2):
        return math.dist(self._nodesCoordinates[node1], self._nodesCoordinates[node2])

    def translateVec(self, vec):

        routesStr = f'{self.calculateFitness(vec) + self._optimalVal}\n0 '
        vecWithStops = self._getVecWithStops(vec)
        for i in range(1, len(vecWithStops) - 1):
            routesStr += f'{vecWithStops[i]} '
            if vecWithStops[i] == 0:
                routesStr += '\n0 '

        routesStr += '0\n'

        return routesStr

    def _sumOfDemands(self, vec):
        demands = 0
        for node in vec:
            demands += self._nodesDemands[node]

        return demands

    def generateGreedyVec(self):
        allCities = [i for i in range(1, self._dim)]
        greedyVec = []
        minCity = self._getCityWithMinDistanceToCurrent(0, allCities)
        greedyVec.append(minCity)
        allCities.remove(minCity)

        while len(allCities) > 0:
            minCity = self._getCityWithMinDistanceToCurrent(greedyVec[-1], allCities)
            greedyVec.append(minCity)
            allCities.remove(minCity)

        return greedyVec

    def _getCityWithMinDistanceToCurrent(self, current, cities):

        minCity = cities[0]
        minDis = self._calcDist(current, cities[0])
        for city in cities:
            currDis = self._calcDist(current, city)
            if currDis < minDis:
                minCity = city
                minDis = currDis

        return minCity

    def generateOneNeighbor(self, vec):
        index1, index2 = getValidIndexes(len(vec))
        neighbor = vec[:index1] + np.flip(vec[index1:index2]).tolist() + vec[index2:]
        return neighbor

    def generateNeighbors(self, vec):

        pairsList = list(itertools.combinations(range(self._dim - 1), 2))
        random.shuffle(pairsList)
        pairsList = pairsList[:int(len(pairsList) / 2)]
        neighbors = []
        for pair in pairsList:
            neighbor = vec[:pair[0]] + np.flip(vec[pair[0]:pair[1]]).tolist() + vec[pair[1]:]

            neighbors.append(neighbor)

        return neighbors

    @staticmethod
    def factory(cvrpName, target):
        module = importlib.import_module('problems.' + cvrpName)
        cvrp = getattr(module, cvrpName)

        return cvrp(target)

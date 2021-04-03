import importlib
import math
import os
import random

import numpy as np

from util.Consts import X, Y


class CVRP:

    def __init__(self, target):
        filePath = os.getcwd() + '\\util\\inputfiles\\' + str(target) + '.txt'
        inputFile = open(filePath, 'r')

        coordinatesSection = 7
        content = inputFile.readlines()
        content = [line.strip('\n') for line in content]

        # get num of trucks
        self._numOfTrucks = int(''.join(content[0][content[0].find('k') + 1:]))

        # get optimal solution
        self._optimalVal = int(''.join(content[1].strip(')')[content[1].find('Optimal value:') + 15:]))

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
        self._separator = self._dim + 1

    def calculateFitness(self, vec):

        distance = self._calcDist(0, vec[0])

        for i in range(len(vec) - 1):
            distance += self._calcDist(vec[i], vec[i + 1])

        distance += self._calcDist(vec[len(vec) - 1], 0)

        return int(distance - self._optimalVal)

    def translateVec(self, vec):

        routesStr = f'{self.calculateFitness(vec) + self._optimalVal}\n0 '

        for i in vec:
            routesStr += f'{i} '
            if i == 0:
                routesStr += '\n0 '

        routesStr += '0\n'
        return routesStr

    def generateRandomVec(self):
        # each solution is represented by a permutation [1, dim] with 0 in between to mark new routes
        vec = np.random.permutation(list(range(1, self._dim)))
        return self._addStopsToVec(vec.tolist())

    # get a vec (with no stops at all) and add returns to depot to make it valid
    def _addStopsToVec(self, vec):
        if self._sumOfDemands(vec) <= self._vehicleCapacity:
            return vec

        # choose random location in vec
        index = random.randrange(1, len(vec))
        return self._addStopsToVec(vec[:index]) + [0] + self._addStopsToVec(vec[index:])

    # check if a vec is a valid solution and add stops if needed
    def _validateVec(self, vec):
        if 0 not in vec:
            return self._addStopsToVec(vec)

        indexOfStop = vec.index(0)
        return self._validateVec(vec[:indexOfStop]) + [0] + self._validateVec(vec[indexOfStop + 1:])

    def _sumOfDemands(self, vec):
        demands = 0
        for node in vec:
            demands += self._nodesDemands[node]

        return demands


    def _calcDist(self, node1, node2):
        return math.dist(self._nodesCoordinates[node1], self._nodesCoordinates[node2])

    def _removeTrailingStops(self, vec):

        while vec[0] == 0:
            vec.pop(0)

        while vec[-1] == 0:
            vec.pop()

        i = 0
        while i < len(vec) - 1:
            if vec[i] == vec[i + 1]:
                vec.pop(i)
            else:
                i += 1

        return vec

    @staticmethod
    def factory(cvrpName, target):
        module = importlib.import_module('problems.' + cvrpName)
        cvrp = getattr(module, cvrpName)

        return cvrp(target)













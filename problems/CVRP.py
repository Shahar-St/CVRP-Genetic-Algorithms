import math
import os

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

    def calculateFitness(self, vec):
        self.translateVec(vec)
        numOfUsedTrucks = 1

        # dist of first 0->first
        distance = self._calcDist(0, vec[0])
        currentTruckUnloads = self._nodesDemands[vec[0]]

        for i in range(self._dim - 2):

            # check if we exceeded capacity
            if currentTruckUnloads + self._nodesDemands[vec[i + 1]] > self._vehicleCapacity:
                # return to warehouse and send a new truck
                distance += self._calcDist(vec[i], 0) + self._calcDist(0, vec[i + 1])
                currentTruckUnloads = self._nodesDemands[vec[i + 1]]
                numOfUsedTrucks += 1
            else:
                distance += self._calcDist(vec[i], vec[i + 1])
                currentTruckUnloads += self._nodesDemands[vec[i + 1]]

        distance += self._calcDist(vec[self._dim - 2], 0)
        # check if a valid solution
        if numOfUsedTrucks > self._numOfTrucks:
            return distance ** 2

        return distance - self._optimalVal

    def getTargetSize(self):
        raise NotImplementedError

    def translateVec(self, vec):
        numOfUsedTrucks = 1

        # dist of first 0->first
        distance = self._calcDist(0, vec[0])
        currentTruckUnloads = self._nodesDemands[vec[0]]
        totalRoutes = []
        currentTruckRoute = [vec[0]]

        for i in range(self._dim - 2):

            # check if we exceeded capacity
            if currentTruckUnloads + self._nodesDemands[vec[i + 1]] > self._vehicleCapacity:
                # return to warehouse and send a new truck
                distance += self._calcDist(vec[i], 0) + self._calcDist(0, vec[i + 1])
                currentTruckUnloads = self._nodesDemands[vec[i + 1]]
                numOfUsedTrucks += 1
                totalRoutes.append([0] + currentTruckRoute + [0])
                currentTruckRoute = [vec[i + 1]]
            else:
                distance += self._calcDist(vec[i], vec[i + 1])
                currentTruckUnloads += self._nodesDemands[vec[i + 1]]
                currentTruckRoute.append(vec[i + 1])

        totalRoutes.append([0] + currentTruckRoute + [0])

        # check if a valid solution
        if numOfUsedTrucks > self._numOfTrucks:
            return None

        solutionStr = f'{distance:.2f}\n'
        for truck in totalRoutes:
            solutionStr += ' '.join(map(str, truck)) + '\n'

        if len(totalRoutes) < self._numOfTrucks:
            solutionStr += '0 0\n' * (self._numOfTrucks - len(totalRoutes))

        return solutionStr

    def generateRandomVec(self):
        # each solution is represented by a permutation [1, dim]
        # which is being translated to a route (assuming an ordered permutation) 0->1->...->dim->0
        # if during the route the sum of distances exceeds the capacity another trucks is being dispatched
        # i.e: if we exceeded the capacity between nodes i,j then the route will be 0->1->...->i->0->j->..->dim->0
        return np.random.permutation(list(range(1, self._dim)))

    def _calcDist(self, node1, node2):
        return math.dist(self._nodesCoordinates[node1], self._nodesCoordinates[node2])

import random

from entities.GeneticEntity import GeneticEntity
from problems.CVRP import CVRP


class GeneticCVRP(CVRP):

    def crossover(self, parent1Vec, parent2Vec):

        parent1Routes = []
        parent1routesDeltas = []
        i = 0
        while i < len(parent1Vec):
            if 0 not in parent1Vec[i:]:
                # last route
                indexOfStop = len(parent1Vec)
            else:
                indexOfStop = parent1Vec.index(0, i)

            route = parent1Vec[i:indexOfStop]
            sumOfRoute = self._sumOfDemands(route)
            delta = self._vehicleCapacity - sumOfRoute
            parent1Routes.append(route)
            parent1routesDeltas.append(delta)

            i = indexOfStop + 1

        # sort the routes based on their deltas
        sortedRoutes = [route + [0] for _, route in sorted(zip(parent1routesDeltas, parent1Routes))]

        # move half the routes to new child
        newChildVec = sum(sortedRoutes[:int(len(sortedRoutes) / 2)], [])

        # complete the rest with parent2
        for node in parent2Vec:
            # if node not in newChildVec or (
            #         node == 0 and newChildVec[-1] != 0 and len(set(newChildVec)) < self._dim):
            #     newChildVec.append(node)
            if node not in newChildVec:
                newChildVec.append(node)

        newChildVec = self._validateVec(newChildVec)

        return GeneticEntity(newChildVec)

    def mutate(self, vec):

        if random.random() < 0.5:
            return self._swapMutation(vec)
        else:
            return self._insertionMutation(vec)


    def _swapMutation(self, vec):
        vecSize = len(vec)
        index1 = random.randint(0, vecSize - 1)
        index2 = random.choice([i for i in range(vecSize) if i != index1])

        temp = vec[index1]
        vec[index1] = vec[index2]
        vec[index2] = temp

        vec = self._removeTrailingStops(vec)
        vec = self._validateVec(vec)
        return vec

    def _insertionMutation(self, vec):

        vecSize = len(vec)
        index1 = random.randint(0, vecSize - 1)
        insertionIndex = random.choice([i for i in range(vecSize) if i != index1])

        indexVal = vec[index1]
        vec.pop(index1)
        vec.insert(insertionIndex, indexVal)
        vec = self._removeTrailingStops(vec)
        vec = self._validateVec(vec)
        return vec
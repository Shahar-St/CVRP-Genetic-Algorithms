from abc import ABC


# An abstract class that implements and declares common functionality to all entities
class IndividualEntity(ABC):

    def __init__(self, vec):
        self._fitness = 0
        self._vec = vec

    def setVec(self, newVec):
        self._vec = newVec

    def getFitness(self):
        return self._fitness

    def setFitness(self, fitness):
        self._fitness = fitness

    def getVec(self):
        return self._vec

    def __lt__(self, other):
        return self._fitness < other.getFitness()

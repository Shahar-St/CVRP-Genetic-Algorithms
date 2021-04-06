import importlib
from abc import ABC, abstractmethod


# An abstract class that implements and declares common functionality to all algorithms
class Algorithm(ABC):

    def __init__(self, problem, popSize):
        self._popSize = popSize
        self._problem = problem

    # This function should run the algorithm
    @abstractmethod
    def findSolution(self, maxIter):
        raise NotImplementedError

    @staticmethod
    def factory(algoName, popSize, eliteRate, mutationRate, problem, maxTabuSize, initialTemp):
        module = importlib.import_module('algorithms.' + algoName)

        algo = getattr(module, algoName)

        if algoName == 'GeneticAlgorithm':
            return algo(
                problem=problem,
                popSize=popSize,
                eliteRate=eliteRate,
                mutationRate=mutationRate,
            )

        if algoName == 'TabuSearchAlgorithm':
            return algo(
                problem=problem,
                popSize=popSize,
                maxTabuSize=maxTabuSize
            )

        if algoName == 'SimulatedAnnealingAlgorithm':
            return algo(
                problem=problem,
                popSize=popSize,
                initialTemp=initialTemp
            )

        else:
            raise Exception('Unknown algorithm')


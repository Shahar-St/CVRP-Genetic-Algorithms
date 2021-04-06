import argparse
import time
import traceback

from algorithms.Algorithm import Algorithm
from util.Consts import *

from problems.CVRP import CVRP


def main():
    startTime = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algo', default=DEFAULT_ALGORITHM)
    parser.add_argument('-ps', '--popSize', type=int, default=GA_POP_SIZE)
    parser.add_argument('-t', '--target', type=int, default=DEFAULT_TARGET)
    parser.add_argument('-ts', '--tabuSize', type=int, default=MAX_TABU_SIZE)
    parser.add_argument('-it', '--initialTemp', type=int, default=DEFAULT_INITIAL_TEMP)
    parser.add_argument('-heu', '--heuristicIntensity', type=float, default=DEFAULT_HEUR_INTEN)
    parser.add_argument('-his', '--historyIntensity', type=float, default=DEFAULT_HIST_INTEN)
    parser.add_argument('-dr', '--decayRate', type=float, default=DEFAULT_DECAY_RATE)
    parser.add_argument('-lf', '--localPheRate', type=float, default=DEFAULT_LOCAL_PHE_RATE)

    args = parser.parse_args()

    # validate input
    if args.algo not in ALLOWED_ALGO_NAMES:
        print("invalid algo!\n")
        exit(1)

    # get params
    algoName = args.algo
    popSize = args.popSize
    target = args.target
    tabuSize = args.tabuSize
    initialTemp = args.initialTemp
    historyIntensity = args.historyIntensity
    heuristicIntensity = args.heuristicIntensity
    decayRate = args.decayRate
    localPheRate = args.localPheRate
    if algoName == 'GeneticAlgorithm':
        cvrpName = 'GeneticCVRP'
    else:
        cvrpName = 'CVRP'

    cvrp = CVRP.factory(cvrpName, target)

    algo = Algorithm.factory(algoName=algoName,
                             popSize=popSize,
                             eliteRate=GA_ELITE_RATE,
                             problem=cvrp,
                             mutationRate=GA_MUTATION_RATE,
                             maxTabuSize=tabuSize,
                             initialTemp=initialTemp,
                             heuristicIntensity=heuristicIntensity,
                             historyIntensity=historyIntensity,
                             decayRate=decayRate,
                             localPheRate=localPheRate
                             )

    # declare the run parameters
    print(
        '\nRun parameters:\n'
        f'Target: {target}\n'
        f'Algo: {algoName}\n'
        f'Pop size: {popSize}\n'
    )
    if algoName == 'TabuSearchAlgorithm':
        print(f'Tabu size: {tabuSize}\n')

    # find a solution and print it
    solVec = algo.findSolution(GA_MAX_ITER)
    print(f'Solution = {cvrp.translateVec(solVec)}\n')

    # print summery of run
    endTime = time.time()
    elapsedTime = endTime - startTime
    print(f'Total elapsed time in seconds: {elapsedTime}')
    print(f'This process took {elapsedTime * CLOCK_RATE} clock ticks')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc()

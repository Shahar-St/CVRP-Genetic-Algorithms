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
    parser.add_argument('-ps', '--popSize', default=GA_POP_SIZE)
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET)
    parser.add_argument('-ts', '--tabuSize', default=MAX_TABU_SIZE)
    parser.add_argument('-it', '--initialTemp', default=DEFAULT_INITIAL_TEMP)

    args = parser.parse_args()

    # validate input
    if args.algo not in ALLOWED_ALGO_NAMES:
        print("invalid algo!\n")
        exit(1)

    if type(args.popSize) != int and not args.popSize.isdigit():
        print('Invalid population size, must be an int')
        exit(1)

    if type(args.target) != int and not args.popSize.isdigit():
        print('Invalid target, must be an int')
        exit(1)

    if type(args.tabuSize) != int and not args.tabuSize.isdigit():
        print('Invalid tabu size, must be an int')
        exit(1)

    if type(args.initialTemp) != int and not args.initialTemp.isdigit():
        print('Invalid initial temp, must be an int')
        exit(1)

    # get params
    algoName = args.algo
    popSize = int(args.popSize)
    target = int(args.target)
    tabuSize = int(args.tabuSize)
    initialTemp = int(args.initialTemp)
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
                             initialTemp=initialTemp
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

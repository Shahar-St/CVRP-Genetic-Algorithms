import psutil

GA_POP_SIZE = 20  # ga population size
GA_MAX_ITER = 250  # maximum iterations

CLOCK_RATE = psutil.cpu_freq().current * (2 ** 20)  # clock ticks per second

BEST = 0
X = 0
Y = 1
DEFAULT_TARGET = 2

'''------------------GA-------------------'''
GA_ELITE_RATE = 0.2  # elitism rate
GA_MUTATION_RATE = 0.4  # mutation rate

'''------------------TS-------------------'''
MAX_TABU_SIZE = 500

'''------------------SA-------------------'''
DEFAULT_INITIAL_TEMP = 5000

'''------------------ACO-------------------'''
DEFAULT_HEUR_INTEN = 1  # how strong is the heuristic part (beta)
DEFAULT_HIST_INTEN = 2  # how strong is the history (pheromone) part (alpha)
DEFAULT_DECAY_RATE = 0.2  # how much will decay in each iteration
DEFAULT_LOCAL_PHE_RATE = 0.1

'''------------------DEFAULT_PARSER-------------------'''

DEFAULT_ALGORITHM = 'ACOAlgorithm'

'''------------------ALLOWED_PARSER_NAMES-------------------'''

ALLOWED_ALGO_NAMES = ('GeneticAlgorithm', 'TabuSearchAlgorithm', 'SimulatedAnnealingAlgorithm', 'ACOAlgorithm')

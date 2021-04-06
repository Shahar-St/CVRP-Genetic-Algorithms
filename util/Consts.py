import psutil

GA_POP_SIZE = 15  # ga population size
GA_MAX_ITER = 500  # maximum iterations

CLOCK_RATE = psutil.cpu_freq().current * (2 ** 20)  # clock ticks per second

BEST = 0
X = 0
Y = 1
DEFAULT_TARGET = 4

'''------------------GA-------------------'''
GA_ELITE_RATE = 0.2  # elitism rate
GA_MUTATION_RATE = 0.4  # mutation rate

'''------------------TS-------------------'''
MAX_TABU_SIZE = 500

'''------------------SA-------------------'''
DEFAULT_INITIAL_TEMP = 5000

'''------------------DEFAULT_PARSER-------------------'''

DEFAULT_ALGORITHM = 'SimulatedAnnealingAlgorithm'


'''------------------ALLOWED_PARSER_NAMES-------------------'''

ALLOWED_ALGO_NAMES = ('GeneticAlgorithm', 'TabuSearchAlgorithm', 'SimulatedAnnealingAlgorithm')

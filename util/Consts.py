import psutil

GA_POP_SIZE = 300  # ga population size
GA_MAX_ITER = 300  # maximum iterations

CLOCK_RATE = psutil.cpu_freq().current * (2 ** 20)  # clock ticks per second

BEST = 0
X = 0
Y = 1
DEFAULT_TARGET = 1

'''------------------GA-------------------'''
GA_ELITE_RATE = 0.1  # elitism rate
GA_MUTATION_RATE = 0.25  # mutation rate

'''------------------DEFAULT_PARSER-------------------'''

DEFAULT_ALGORITHM = 'GeneticAlgorithm'


'''------------------ALLOWED_PARSER_NAMES-------------------'''

ALLOWED_ALGO_NAMES = ('GeneticAlgorithm')
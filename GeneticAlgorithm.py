import sys
from queue import PriorityQueue

from chromosome import *


def main():

    crossRate = 0.7
    mutRate = 0.001
    poolSize = 40
    if len(sys.argv) == 2:
        target = int(sys.argv[1])
    else:
        target = 42
    generation = 0
    emptyChromosomes = PriorityQueue()

    for i in range(poolSize):
        chromo = Chromosome(target)

        emptyChromosomes.put((chromo.scoreChromo(), chromo))
    checker = True

    while checker:
        newPool = PriorityQueue()
        generation += 1
        for j in range(emptyChromosomes.qsize()-1,0,-2):
            p1 = emptyChromosomes.get()[1]
            p2 = emptyChromosomes.get()[1]
            p1.crossover(p2, crossRate)
            p1.mutate(mutRate)
            p2.mutate(mutRate)
            if(p1.scoreChromo() == 0 and p1.isValid()):
                print("the generation is: ", generation)
                print(p1.decodeChromo())
                checker = False
                break

            elif (p2.scoreChromo() == 0 and p2.isValid()):
                print("the generation is: ", generation)
                print(p1.decodeChromo())
                checker = False
                break

            else:
                newPool.put((p1.getScore(), p1))
                newPool.put((p2.getScore(), p2))

        for i in range(newPool.qsize()):
            var = newPool.get()

            emptyChromosomes.put(var)
main()


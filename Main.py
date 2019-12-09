# -*- coding: utf-8 -*-

from Graphe import *
from Optimization import *
from multiprocessing import Process, Manager

NUM_THREADS = 2

if len(sys.argv) == 2:  # Présence d'un argument
	graph = buildGraph(sys.argv[1])
else:
	graph = buildGraph("graph.txt")

def ga(procnum, return_dict):
	return_dict[procnum] = geneticAlgorithm(graph, 1400, 0.9, 0.95)

def printValues(values):
	for i in range(0, len(values)):
		print("La partition trouvée est la suivante: ", values[i][0])
		print("Sa modularité vaut: ", values[i][1])

if __name__ == '__main__':
	manager = Manager()
	returnValues = manager.dict()

	processes = []
	for i in range(0, NUM_THREADS):
		p = Process(target = ga, args = (i, returnValues))
		processes.append(p)
		p.start()

	for p in processes:
		p.join()

	values = returnValues.values()

	index = 0
	
	for i in range(1, NUM_THREADS):
		if values[index][1] < values[i][1]:
			index = i

	print("La meilleur partition trouvée est la suivante: ", values[index][0])
	print("Sa modularité vaut: ", values[index][1])

from Population import *
import random
import copy

def grasp(a, n, pop):
	Cmin = pop.getMinModularity()
	Cmax = pop.getMaxModularity()
	Sol = Population(pop.graph, [])
	while(n > 0):
		RCL = calculRCL(pop, Cmin, Cmax, a)
		index_S = randRCL(RCL)
		if index_S == -1:
			index_S = random.randint(0, len(pop)-1)
		Sol.addPartition(pop.partitionList[index_S])
		n -= 1
	return Sol

def calculRCL(C, Cmin, Cmax, a):
	tab = []
	for i in range(C.realLength):
		res = C.modularityList[i]
		if res >= Cmin + a * (Cmax - Cmin) :
			tab.append(i)
	return tab

def randRCL(tabRCL):
	if len(tabRCL) == 0:
		return -1

	rand = random.randint(0, len(tabRCL)-1)
	return tabRCL[rand]

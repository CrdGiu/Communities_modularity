# -*- coding: utf-8 -*-

import math
import random
import sys

from Population import *
from Grasp import *
from SimulAnnealing import *

def geneticAlgorithm(graph, n, alpha, beta):
	"""
	Algorithme génétique

	:param graph: Le graphe correspondant
	:param n: Taille de la population initiale
	:param alpha: Taux de croisement
	:param beta: Taux de mutation
	:return: La partition calculée qui a la plus grande modularité ainsi que sa modularité
	"""

	population = initializePopulation(math.floor(n * 1.5), graph)
	population = grasp(0.2, n, population)

	i = population.getIndexOfPartitionMaxModularity(False)
	best = (population.partitionList[i], population.modularityList[i])

	counter = 1
	while n > 0:
		print("counter = ", counter)
		print("n = ", n)

		parents = selectParentsCollection(population, n)
		parents0 = phenoToGeno(parents, population, graph)
		children0 = crossOver(parents0, alpha)
		n = len(children0)
		if n == 0:
			return best
		children = genoToPheno(children0, population, graph)
		print("Mutation\n")
		children = mutation(graph, children, beta)
		population = Population(graph, children)
		i = population.getIndexOfPartitionMaxModularity(False)
		temp = (population.partitionList[i], population.modularityList[i])
		if (best[1] < temp[1]):
			best = temp

		counter += 1

	return best

def initializePopulation(n, graph):
	"""
	Créer une population

	:param n: La taille de la population
	:param graph: Le graphe correspondant
	:return: Une polulation
	"""

	partitionList = [0] * n

	for i in range(0, n):
		partitionList[i] = createCompletelyRamdomPartition(1, graph)

	return Population(graph, partitionList)

def createPartitionSplittingNodeList(n, graph):
	"""
	Créer une partition en subdivisant la liste des sommets par n

	:param n: Divise par n la liste des sommets
	:param graph: Le graphe correspondant
	:return: Une partition
	"""

	partition = [0] * n
	subpartitionSize = math.floor(graph.size / n)

	counter = 1
	for i in range(0, n - 1):
		subPartition = [0] * subpartitionSize
		for j in range(0, subpartitionSize):
			subPartition[j] = counter
			counter += 1

		partition[i] = subPartition

	subPartition = [0] * (graph.size - counter + 1)
	for i in range(0, (graph.size - counter + 1)):
		subPartition[i] = counter
		counter += 1

	partition[n-1] = subPartition

	return partition

def createPartiallyRamdomPartition(p, graph):
	"""
	Créer une partition partiellement aléatoire. La taille des sous-partition est réglable par le paramètre p, qui est une fraction du nombre de sommets
	
	:param p: pourcentage du nombre de sommets
	:param graph: Le graphe correspondant
	:return: Une partition aléatoire
	"""

	sizeMax = math.ceil(p * graph.size)

	partition = []

	counter = 1
	while counter <= graph.size:
		subpartitionSize = random.randint(1, sizeMax)
		if (subpartitionSize + counter - 1) > graph.size:
			subpartitionSize = graph.size - counter + 1

		subPartition = [0] * subpartitionSize
		for j in range(0, subpartitionSize):
			subPartition[j] = counter
			counter += 1

		partition.append(subPartition)

	return partition

def createCompletelyRamdomPartition(p, graph):
	"""
	Créer une partition complétement aléatoire. La taille des sous-partition est réglable par le paramètre p, qui est une fraction du nombre de sommets
	
	:param p: pourcentage du nombre de sommets
	:param graph: Le graphe correspondant
	:return: Une partition aléatoire
	"""

	sizeMax = math.ceil(p * graph.size)

	partition = []
	nodes = [0] * graph.size
	for i in range(0, graph.size):
		nodes[i] = i + 1
	nFictitious = graph.size

	while nFictitious > 0:
		subpartitionSize = random.randint(1, sizeMax)
		if subpartitionSize > nFictitious:
			subpartitionSize = nFictitious

		subPartition = [0] * subpartitionSize
		for i in range(0, subpartitionSize):
			n = random.randint(0, nFictitious-1)
			temp = nodes[nFictitious-1]
			nodes[nFictitious-1] = nodes[n]
			nodes[n] = temp
			nFictitious -= 1

			subPartition[i] = nodes[nFictitious]

		partition.append(subPartition)

	return partition

def selectParentsCollection(population, n):
	"""
	Forme un ensemble de pairs d'index de deux parents (ici un parent représente une partition)

	:param population: La population (les parents à considérer)
	:param n: La taille de la population
	:return: Un ensemble de pairs d'index de deux parents. Si un des indices vaut -1, cela signifie qu'une pair de parents ne contient qu'un parent (taille de population impaire)
	"""

	parents = []

	while len(parents) < (n / 2):
		p1 = selectParent(population)
		if p1 != None:
			index1 = population.removePartitionFictitiouslyFromIndex(p1[0])
		else:
			index1 = -1

		p2 = selectParent(population)
		if p2 != None:
			index2 = population.removePartitionFictitiouslyFromIndex(p2[0])
		else:
			index2 = -1

		parents.append([index1, index2])

	population.addAllPartitionsRemovedFictitiously()

	return parents

def selectParent(population):
	"""
	Sélectionne un parent dans la population (sélection par tournoi)

	:param population: La population
	:return: La partition choisi
	"""

	populationSize = population.fictitiousLength

	if(populationSize == 0):
		return None

	population.evaluatePopulation()

	#proba = 1/populationSize
	proba = 1 / 3.0
	k = math.floor(populationSize * 0.05) # On prend un certain poucentage de la population

	if(k == 0):
		i = random.randint(0, (populationSize - 1))
		return (i, population.partitionList[i], population.modularityList[i])

	subPopulation = [None] * k
	fictitiousLengthTemp = populationSize
	for i in range(0, k):
		x = random.randint(0, fictitiousLengthTemp - 1)
		subPopulation[i] = [(fictitiousLengthTemp-1), population.partitionList[x], population.modularityList[x]]
		population.removePartitionFictitiouslyFromIndex(x)
		fictitiousLengthTemp -= 1

	population.addNLastRemovedFictitiously(populationSize - fictitiousLengthTemp)

	subPopulation.sort(key = lambda x: x[2], reverse = True)

	i = 0
	parent = None
	while (parent == None) and (i < (k - 1)):
		if (random.random() < proba):
			parent = (subPopulation[i][0], subPopulation[i][1], subPopulation[i][2])

		i += 1

	if parent == None:
		parent = (subPopulation[i][0], subPopulation[i][1], subPopulation[i][2])

	return parent

def phenoToGeno(parents, population, graph):
	"""
	Converti un ensemble de pairs d'index de deux parents en un ensemble de pairs de deux parents convertis en binaire

	:param parents: Un ensemble de pairs d'index de deux parents
	:param population: La population à considérer
	:param graph: Le graphe correspondant
	:return: Un ensemble de pairs de deux parents convertis en binaires. Si un des indices vaut None, cela signifie qu'une pair de parents ne contient qu'un parent (taille de population impaire)
	"""

	parents0 = [None] * len(parents)
	for i in range(0, len(parents)):
		pairParents = parents[i]
		p1Index = pairParents[0]
		p2Index = pairParents[1]

		p1Bin = None
		p2Bin = None
		if p1Index >= 0:
			p1Bin = population.getGenooBin(population.partitionList[p1Index], graph)
		if p2Index >= 0:
			p2Bin = population.getGenooBin(population.partitionList[p2Index], graph)

		parents0[i] = [p1Bin, p2Bin]

	return parents0

def crossOver(parents0, alpha):
	"""
	Croise un ensemble de pairs de deux parents convertis en binaires

	:param parents0: Un ensemble de pairs de deux parents convertis en binaires
	:param alpha: Taux de croisement
	:return: Un ensemble d'enfants en binaire
	"""

	children0List = []
	for pairParents0 in parents0:
		if (random.random() <= alpha) and (len(pairParents0) >=2):
			pairChildren0 = crossOverHelper(pairParents0)
			c1 = pairChildren0[0]
			c2 = pairChildren0[1]
			if c1 != None:
				children0List.append(c1)
			if c2 != None:
				children0List.append(c2)

	return children0List

def crossOverHelper(pairParents0):
	"""
	Croise deux parents

	:param: Une liste de deux parents en binaire
	:return: Une liste de deux enfants en binaire
	"""

	p1 = pairParents0[0]
	p2 = pairParents0[1]
	c1 = None
	c2 = None
	
	if (p1 != None) and (p2 != None):
		cr1 = random.randint(1, len(p1[0]) - 2)
		cr2 = random.randint(cr1 + 1, len(p1[0]) - 1)
		
		if(len(p1[0]) > 2) and (len(p2[0]) > 2):
			c1 = []
			c2 = []
			i = 0
			while ((i + 1) < len(p1)):
				c1.append(p1[i][:cr1] + p1[i+1][cr1:cr2] + p1[i][cr2:])
				c1.append(p1[i+1][:cr1] + p1[i][cr1:cr2] + p1[i+1][cr2:])
				i += 2
			if len(c1) != len(p1):
				c1.append(p1[-1])
			i = 0
			
			while ((i + 1) < len(p2)):
				c2.append(p2[i][:cr1] + p2[i+1][cr1:cr2] + p2[i][cr2:])
				c2.append(p2[i+1][:cr1] + p2[i][cr1:cr2] + p2[i+1][cr2:])
				i += 2
			if len(c2) != len(p2):
				c2.append(p2[-1])

	return [c1, c2]

def genoToPheno(children0, population, graph):
	"""
	Converti un ensemble d'enfants en binaire en un ensemble d'enfants en partiton

	:param children0: Un ensemble d'enfants en binaire
	:param population: La population à considérer
	:param graph: Le graphe correspondant
	:return: Un ensemble d'enfants en partiton
	"""

	children = [None] * len(children0)
	for i in range(0, len(children0)):
		children[i] = population.getPhenooBin(children0[i])

	return children

def mutation(graph, childrenList, beta):
	"""
	Mute une liste d'enfants (utilise le recuit simulé)

	:param graph: Le graphe correspondant
	:param childrenList: Liste d'enfants
	:param beta: Taux de mutation
	:return: Liste d'enfants mutés
	"""

	newChildrenList = []
	population = Population(graph, childrenList)

	for i in range(0, len(childrenList)):
		if random.random() <= beta:
			newChildrenList.append(simulatedAnnealing(20, 0.9, 5, i, population))
		else:
			newChildrenList.append(population.partitionList[i])

	return newChildrenList

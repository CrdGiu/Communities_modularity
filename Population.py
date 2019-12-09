import math
import random
import sys

class Population:
	"""
	Représente une population
	Cette classe utilise une longeur de partitions fictive permettant de supprimer temporairement des partitions (celles-ci peuvent être récupérées par la suite)
	"""

	def __init__(self, graph, partitionList, modularityList = None):
		"""
		:param graph: Le graphe correspondant
		:param partitionList: Liste de partitions
		:param modularityList: Liste des modularités qui doit avoir été évaluée (paramètre optionnel)
		"""

		self.partitionList = partitionList
		if modularityList == None:
			self.modularityList = [0] * len(self.partitionList)
			self.evaluated = False
		else:
			self.modularityList = modularityList
			self.evaluated = True
		self.realLength = len(partitionList)
		self.fictitiousLength = len(partitionList)
		self.graph = graph

	def __str__(self):
		s = ""

		for partition in self.partitionList:
			s += str(partition) + "\n"

		return s

	def evaluatePopulation(self):
		"""
		Évalue une population
		"""

		if self.evaluated == False:
			for i in range(0, self.realLength):
				self.modularityList[i] = evaluate(self.partitionList[i], self.graph)
			self.evaluated = True

	def addPartition(self, partition):
		"""
		Ajoute une partition dans la population

		partition: Partition à ajouter
		"""

		self.partitionList.append(partition)
		if self.evaluated == True:
			self.modularityList.append(evaluate(partition))
		else:
			self.modularityList.append(0.0)

		self.realLength += 1
		self.fictitiousLength += 1

	def removePartition(self, i):
		"""
		Supprime une partition dans la population à partir de son index
		"""

		p = self.partitionList.pop(i)
		self.modularityList.pop(i)

		self.realLength -= 1
		self.fictitiousLength -= 1

		return p

	def getGeno(self):
		t = []
		for i in range(len(self.partitionList)):
			t.append(self.getGenoo(self.partitionList[i]))

		return t
			
	def getGenoo(self, l, graph):
		t =[]
		for i in range(len(l)):
			t.append('0' * graph.size)
			for j in range(len(l[i])):
				t[i] = t[i][:len(t[i]) - l[i][j]] + '1' + t[i][len(t[i])-l[i][j]+1:]
			t[i]=int(t[i], 2)

		return t
	
	def getGenoBin(self):
		t = []
		for i in range(len(self.partitionList)):
			t.append(self.getGenooBin(self.partitionList[i]))

		return t
			
	def getGenooBin(self, l, graph):
		t = []
		for i in range(len(l)):
			t.append('0' * graph.size)
			for j in range(len(l[i])):
				t[i] = t[i][:len(t[i]) - l[i][j]] + '1' + t[i][len(t[i])-l[i][j]+1:]

		return t
	
	def getPheno(self, geno):
		t = []
		for i in range(len(geno)):
			t.append(self.getPhenoo(geno[i]))

		return t
	
	def getPhenoo(self, geno):
		t = []
		for i in range(len(geno)):
			t.append([])
			st = bin(geno[i])
			for j in range(len(st)):
				if(st[len(st)-j-1] == '1'):
					t[i].append(j+1)

		return t
	
	def getPhenoBin(self, geno):
		t = []
		for i in range(len(geno)):
			t.append(self.getPhenoo(geno[i]))

		return t
	
	def getPhenooBin(self, geno):
		t = []
		if(geno!=None):
			for i in range(len(geno)):
				t.append([])
				st=geno[i]
				for j in range(len(st)):
					if(st[len(st)-j-1] == '1'):
						t[i].append(j+1)

		return t
				
	
	def getMaxModularity(self, fictitiousPartitionsOnly = True):
		"""
		Obtenir la plus grande modularité de la population

		:param fictitiousPartitionsOnly: Considère uniquement les partitions dans la population fictive (par défaut, ce paramètre est à vrai)
		:return: La plus grande modularité de la population
		"""

		if self.evaluated == False:
			self.evaluatePopulation()

		return self.modularityList[self.getIndexOfPartitionMaxModularity(fictitiousPartitionsOnly)]

	def getMinModularity(self, fictitiousPartitionsOnly = True):
		"""
		Obtenir la plus petite modularité de la population

		:param fictitiousPartitionsOnly: Considère uniquement les partitions dans la population fictive (par défaut, ce paramètre est à vrai)
		:return: La plus petite modularité de la population
		"""

		if self.evaluated == False:
			self.evaluatePopulation()

		return self.modularityList[self.getIndexOfPartitionMinModularity(fictitiousPartitionsOnly)]

	def getIndexOfPartitionMaxModularity(self, fictitiousPartitionsOnly = True):
		"""
		Obtenir l'index de la partition qui a la plus grande modularité

		:param fictitiousPartitionsOnly: Considère uniquement les partitions dans la population fictive (par défaut, ce paramètre est à vrai)
		:return: La plus grande modularité de la population ou -1 si la population est vide
		"""

		if self.evaluated == False:
			self.evaluatePopulation()

		if fictitiousPartitionsOnly == True:
			n = self.fictitiousLength
		else:
			n = self.realLength

		if n == 0:
			return -1

		indexMax = 0
		maximum = self.modularityList[0]
		for i in range(1, n):
			modularityi = self.modularityList[i]
			if(modularityi > maximum):
				indexMax = i
				maximum = modularityi

		return indexMax

	def getIndexOfPartitionMinModularity(self, fictitiousPartitionsOnly = True):
		"""
		Obtenir l'index de la partition qui a la plus petite modularité

		:param fictitiousPartitionsOnly: Considère uniquement les partitions dans la population fictive (par défaut, ce paramètre est à vrai)
		:return: La plus petite modularité de la population ou -2 si la population est vide
		"""

		if self.evaluated == False:
			self.evaluatePopulation()

		if fictitiousPartitionsOnly == True:
			n = self.fictitiousLength
		else:
			n = self.realLength

		if n == 0:
			return -1

		indexMin = 0
		minimum = self.modularityList[0]
		for i in range(1, n):
			modularityi = self.modularityList[i]
			if(modularityi < minimum):
				indexMin = i
				minimum = modularityi

		return indexMin

	def removeLastPartitionFictitiously(self):
		"""
		Supprime de manière fictive la dernière partition

		:return: La nouvelle position de la partiton supprimée
		"""
		
		return self.removePartitionFictitiouslyFromIndex(self.fictitiousLength-1)

	def removePartitionFictitiouslyFromIndex(self, i):
		"""
		Supprime de manière fictive partition en ième position

		:param i: Partition i à supprimer de manière fictive
		:return: La nouvelle position de la partiton supprimée
		"""
		
		if(self.fictitiousLength > 0):
			ficLen = self.fictitiousLength
			tempPartition = self.partitionList[ficLen-1]
			tempModularity = self.modularityList[ficLen-1]
			self.partitionList[ficLen-1] = self.partitionList[i]
			self.modularityList[ficLen-1] = self.modularityList[i]
			self.partitionList[i] = tempPartition
			self.modularityList[i] = tempModularity

			self.fictitiousLength -= 1

			return (ficLen - 1)
		else:
			return -1

	def addAllPartitionsRemovedFictitiously(self):
		"""
		Ajoute toutes les partitions supprimées de manière fictive
		"""

		self.fictitiousLength = self.realLength

	def addLastRemovedFictitiously(self):
		"""
		Ajoute les n dernières partitions supprimées de manière fictive

		:param n: Nombre de partitons supprimées de manière fictive à ajouter
		"""

		self.addNLastRemovedFictitiously(1)


	def addNLastRemovedFictitiously(self, n):
		"""
		Ajoute les n dernières partitions supprimées de manière fictive

		:param n: Nombre de partitons supprimées de manière fictive à ajouter
		"""

		self.fictitiousLength += n

		if(self.fictitiousLength > self.realLength):
			self.fictitiousLength = self.realLength

	def modularityMean(self):
		if self.evaluated == False:
			self.evaluatePopulation()

		res = 0
		for i in self.modularityList:
			res += i
			
		return res/len(self.modularityList)

def evaluate(partition, graph):
	"""
	Évalue la fonction objective

	:param partition: Une partition
	:param graph: Le graphe correspondant
	:return: La modularité de la partition
	"""

	modularity = 0.0
	twoTimesArcs = graph.arcs * 2

	for p in partition:
		for i in range(0, len(p)):
			for j in range(0, len(p)):
				arcExist = 0

				nodeI = p[i]
				nodeJ = p[j]
				for k in range(graph.head[nodeI - 1], graph.head[nodeI]):
					if graph.succ[k - 1] == nodeJ:
						arcExist = 1
						break

				modularity += arcExist - ((graph.degre(nodeI) * graph.degre(nodeJ)) / twoTimesArcs)

	modularity /= twoTimesArcs

	return modularity

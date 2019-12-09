# -*- coding: utf-8 -*-

class UndirectedGraph:
	"""
	Representation des Graphes Non-Orienté selon le cours de théorie des graphes et optimisation combinatoire
	Les tableaux sont indexés de 0 à n-1
	"""

	def __init__(self, head=[0], succ=[]):
		"""
		Constructeur de la classe Graphe

		Paramètres:
		head -- Liste d'adjacance du graphe, tel que head[i] = position du premier successeur du noeud i
		        Le dernier élément head[n] indique la fin du Graphe
		succ -- Liste d'adjacance des successeur du graphe, tel que succ[i] = numéros du successeur du noeud qui pointe vers i
		        Le dernier élément doit être -1 avant d'indiquer la fin du Graphe
		"""
		self.head = head
		self.succ = succ
		self.w = []
		self.size = len(head)-1
		self.arcs = int(len(succ)/2)

	def __str__(self):
		ret = "Head: " + str(self.head[:self.size + 1]) + "\n"	# On affiche le dernier l'élément n du head, même si il ne représente aucun noeud
		ret += "Succ: " + str(self.succ[:2*self.arcs]) + "\n\n"	# -1 n'est pas affiché
		node = 0
		for i,j in enumerate(self.head[:self.size]):
			succ = "[ "
			for w in self.succ[j:self.head[i+1]]:
				succ += str(w) + ", "
			succ += "]"
			ret += str(i) + "--" + succ + "\n"
		return ret

	def addNode(self):
		"""Ajoute un nouveau noeud au Graphe"""
		self.head.insert(self.size, len(self.succ))
		self.size += 1

	def addSuccDirecterd(self, n, m):
		self.succ.insert(self.head[n+1],m)
		i = n+1
		while(i < self.size + 1):
			self.head[i] += 1
			i += 1

	def addSucc(self, nA, nB):
		"""Ajoute un nouveau successeur a Graphe tel que nA --- nB

		Paramètres:
		nA -- Numéros du noeud A, entre 0 et n-1
		nB -- Numéros du noeud B, entre 0 et n-1"""
		if nA != nB:
			self.addSuccDirecterd(nA,nB)
			self.addSuccDirecterd(nB,nA)
			self.arcs += 1

	def degre(self, n):
		"""Retourne le degré du du noeud n
		
		Le degrès étant le nombre d'arc entrant/sortant du noeud"""
		return self.head[n] - self.head[n-1]

def buildGraph(fname):
	"""Génere un graphe à partir d'un fichier

		Paramètres:
			fname -- le nom du fichier
		Retourne:
			le graphe décrit dans le fichier

		Note : Ici, on lit les 2 premières lignes même si on en a pas besoin
	"""
	f = open(fname,'r')
	head = []
	succ = []
	i = 1
	for line in f:
		j = 0
		while line[j] != '\n': #line[j] correspond à un caractère
			numstr = ""
			if line[j].isdigit():
				while line[j] != ' ' and line[j] != '\n':
					numstr += line[j]
					j += 1
				if i == 3:
					head.insert(len(head),int(numstr))
				elif i == 4:
					succ.insert(len(succ),int(numstr))
			if line[j] != '\n': #condition ici sinon on incrémente quand on arrive à la fin
				j += 1
		i += 1
	return UndirectedGraph(head, succ)

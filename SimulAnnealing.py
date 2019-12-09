import random
import math

def simulatedAnnealing(t, alpha, p, e, pop): #e est l'index
	pop.evaluatePopulation()
	s = best = e
	while True:
		for i in range(1, p):
			n = neighbour(s, pop)
			r1 = random.sample(n,1)
			s_prime = r1[0]
			if ((pop.modularityList[s] <= pop.modularityList[s_prime]) or (acceptation(s, s_prime, t, pop))):
				s = s_prime
			if (pop.modularityList[s] >= pop.modularityList[best]):
				best = s

		t = t * alpha
		if end(t):
			return pop.partitionList[best]

def end(t, eps = 0.1):
	return t < eps

def neighbour(s, pop):
	found = False
	v = []
	j1 = j2 = s
	i = 0
	l = pop.partitionList
	while i < 4:
		if j1 not in v and j1 != s:
			v.append(j1)
		if j2 not in v and j2 != s:
			v.append(j2)
		if j1 != 0:
			j1 -= 1
		if j2 != len(l)-1:
			j2 += 1
		i += 2
	return v

def prob_acceptation(s, s_prime, t, pop):
	p = (pop.modularityList[s] - pop.modularityList[s_prime]) / t
	if p > 0:
		return math.exp(-p)
	else:
		return math.exp(p)


def acceptation(s, s_prime, t, pop):
	p = prob_acceptation(s, s_prime, t, pop)
	r = random.random()

	return r < p

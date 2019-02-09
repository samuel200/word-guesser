import math
import random

### Global Variables ####

target = "Hello World"
geneSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .!?"
capitals = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
smalls = "abcdefghijklmnopqrstuvwxyz"
punctuation = ".!?"
space = " "


class DNA:

	def __init__(self, length, genes=None):

		self.length = length
		self.fitness = 0

		if genes:

			self.genes = genes

		else:

			self.genes = [random.choice(list(geneSet)) for _ in range(self.length)]


	def __str__(self):

		return "DNA: {}\tFitness: {}".format("".join(self.genes), self.fitness)

	def crossover(self, parent):

		start = random.randint(0, math.floor(self.length/2.0))
		end = random.randint(math.floor(self.length/2.0), self.length)
		newGenes = []

		for i in range(self.length):

			if i < start:
				# Caution********
				newGenes.append(parent.genes[i])

			elif i >= start and i < end:

				newGenes.append(self.genes[i])

			elif i >= end:

				newGenes.append(self.genes[i])

		return DNA(self.length, newGenes)


	def mutate(self, mut_rate):

		index = random.randint(0, self.length)
		count = 0
		newList = []

		if random.random() < mut_rate:

			for i in self.genes:

				if count == index:

					newList.append(random.choice(list(geneSet)))

				else:

					newList.append(i)
					count += 1

			self.genes = newList


	def calcFitness(self):

		fitness_level = 0

		for k, j in zip(self.genes, target):
			if k == j:

				fitness_level += 1.0

		self.fitness = fitness_level/float(self.length)



class Population:

	def __init__(self, pop_width, mutation_rate, target, population=None):


		self.pop_width = pop_width
		self.mutation_rate = mutation_rate
		self.target = target
		self.completed = False
		self.maxFitness = 0
		self.matingpool = []

		if population:

			self.population = population

		else:

			self.population = [DNA(len(self.target)) for _ in range(self.pop_width)]


	def calcFitness(self):

		for i in self.population:

			i.calcFitness()

			if i.fitness > self.maxFitness:

				self.maxFitness = i.fitness


	def evalutation(self):

		self.matingpool = []

		for i in self.population:

			n = math.floor((i.fitness/self.maxFitness) * 100)

			for _ in range(n):

				self.matingpool.append(i)


	def naturalSelection(self):

		new_population = []


		for i in range(self.pop_width):

			partnerA = random.choice(self.matingpool)
			partnerB = random.choice(self.matingpool)

			child = partnerA.crossover(partnerB)
			child.mutate(self.mutation_rate)

			new_population.append(child)

		return Population(self.pop_width, self.mutation_rate, self.target, new_population)





def main():

	population = Population(1000, 0.01, target)

	while not population.completed:

		population.calcFitness()
		
		for i in population.population:

			print(i)


		if "".join(i.genes) == population.target:

			population.completed = True
		
		population.evalutation()

		if not population.completed:

			population = population.naturalSelection()



if __name__ == '__main__':

	main()

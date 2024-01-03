import time
from functools import reduce
import random
import numpy

from .Graph import Graph

class AntColony:

    def __init__(self):
        """
        Initializes the AntColony.

        This class represents the Ant Colony Optimization algorithm.
        """
        # Ant algorithm coefficients
        self.alfa = 2
        self.beta = 5
        self.sigm = 3
        self.ro = 0.8 #evaporation rate
        self.th = 80

        print('''
        Available files:
            1 - E-n16-k8.txt
            2 - E-n19-k2.txt              
            3 - E-n22-k4.txt
            4 - E-n33-k4.txt        
        ''')

        self.file_name = ''
        
        while True:
            # User input for file selection
            file_num = input("Type in your file number:")
            if int(file_num) not in [1, 2, 3, 4, 5, 6, 7]:
                continue
            else:
                file_mapping = {
                    '1': "./datasets/E-n16-k8.txt",
                    '2': "./datasets/E-n19-k2.txt",
                    '3': "./datasets/E-n22-k4.txt",
                    '4': "./datasets/E-n33-k4.txt",
                }
                self.file_name = file_mapping[file_num]
                break

        file_path = f"./datasets/{self.file_name}"
        duration_string = input("Type the total duration of the algorithm: ")
        # Algorithm data variables
        self.total_duration = float(duration_string)  # Total duration of the run in seconds
        self.start_time = time.time()  # Current time in seconds
        self.ants = 0

    def solutionOfOneAnt(self, vertices, edges, capacityLimit, demand, pheromones):
        """
        Generates a solution for a single ant.

        Parameters:
        - vertices: List of remaining vertices to visit.
        - edges: Dictionary of distances between vertices.
        - capacityLimit: Capacity limit for the ant's route.
        - demand: Dictionary of demand for each vertex.
        - pheromones: Dictionary of feromone levels on edges.

        Returns:
        - solution: List representing the ant's route.
        """
        solution = list()

        while(len(vertices)!=0):
            path = list()
            # Randomly choose a city
            city = numpy.random.choice(vertices)
            initial_city = city
            capacity = capacityLimit - demand[city]
            path.append(city)
            vertices.remove(city)
            while(len(vertices)!=0):
                # Calculate probabilities based on pheromones and edge distances
                probabilities = list(map(lambda x: ((pheromones[(min(x,city), max(x,city))])**self.alfa)*((1/edges[(min(x,city), max(x,city))])**self.beta), vertices))
                probabilities = probabilities/numpy.sum(probabilities)
                
                # Randomly choose the next city based on probabilities
                city = numpy.random.choice(vertices, p=probabilities)
                capacity = capacity - demand[city]

                if(capacity>0):
                    path.append(city)
                    vertices.remove(city)
                else:
                    break
            solution.append(path)
        return solution

    def rateSolution(self, solution, edges):
        """
        Rates the quality of a solution.

        Parameters:
        - solution: List representing the ant's route.
        - edges: Dictionary of distances between vertices.

        Returns:
        - s: Total distance of the solution.
        """
        s = 0
        # Iterate through each path in the solution
        for i in solution:
            a = 1
            # Iterate through each city in the path
            for j in i:
                b = j
                # Accumulate distance between consecutive cities
                s = s + edges[(min(a,b), max(a,b))]
                a = b
            # Add distance from the last city back to the starting city
            b = 1
            s = s + edges[(min(a,b), max(a,b))]
        return s

    def updateFeromone(self, pheromones, solutions, bestSolution):
        """
        Updates feromone levels based on solutions.

        Parameters:
        - pheromones: Dictionary of feromone levels on edges.
        - solutions: List of ant solutions.
        - bestSolution: Best solution found so far.

        Returns:
        - bestSolution: Updated best solution.
        """
        # Calculate average route length
        Lavg = reduce(lambda x,y: x+y, (i[1] for i in solutions))/len(solutions)
        # Update pheromones using the formula
        pheromones = { k : (self.ro + self.th/Lavg)*v for (k,v) in pheromones.items() }
        # Sort solutions by route length
        solutions.sort(key = lambda x: x[1])
        if(bestSolution!=None):
            if(solutions[0][1] < bestSolution[1]):
                bestSolution = solutions[0]
            # Update pheromones based on the best solution
            for path in bestSolution[0]:
                for i in range(len(path)-1):
                    pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = self.sigm/bestSolution[1] + pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
        else:
            bestSolution = solutions[0]
        # Update pheromones using a formula for all solutions
        for l in range(self.sigm):
            paths = solutions[l][0]
            L = solutions[l][1]
            for path in paths:
                for i in range(len(path)-1):
                    pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = (self.sigm-(l+1)/L**(l+1)) + pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
        return bestSolution

    def add_city_to_route(self, route):
        """
        Adds the starting and ending city to a route.

        Parameters:
        - route: List representing the ant's route.

        Returns:
        - route: Modified route with the starting and ending city.
        """
        route.insert(0, 1)  
        route.append(1)     
        return route

    def iterate(self):
        """
        Iterates through ant colony optimization algorithm.

        Returns:
        - bestSolution: Best solution found during iterations.
        """
        
        bestSolution = None
        graph_wrapper = Graph(self.file_name)

        vertices, edges, capacityLimit, demand, pheromones, optimalValue = graph_wrapper.generateGraph()
        
        i=0
        # Iterate until the specified duration is reached
        while time.time() - self.start_time < self.total_duration:
            solutions = list()
            for _ in range(self.ants):
                solution = self.solutionOfOneAnt(vertices.copy(), edges, capacityLimit, demand, pheromones)
                solutions.append((solution, self.rateSolution(solution, edges)))
            bestSolution = self.updateFeromone(pheromones, solutions, bestSolution)
            print(str(time.time() - self.start_time)+":\t"+str(int(bestSolution[1]))+"\t"+str(optimalValue))
        return bestSolution

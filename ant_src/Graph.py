import re, numpy

class Graph:

    def __init__(self, source_file_path):
        # Source file
        f = open(source_file_path, "r")
        content = f.read()
        
        # Data variables (raw)
        optimalValue = re.search("Optimal value: (\d+)", content, re.MULTILINE)
        if(optimalValue != None):
            optimalValue = optimalValue.group(1)
        else:
            optimalValue = re.search("Best value: (\d+)", content, re.MULTILINE)
            if(optimalValue != None):
                optimalValue = optimalValue.group(1)
        capacity = re.search("^CAPACITY : (\d+)$", content, re.MULTILINE).group(1)
        dimension = re.search("^DIMENSION : (\d+)$", content, re.MULTILINE).group(1)
        graph = re.findall(r"^(\d+) (\d+) (\d+)$", content, re.MULTILINE)
        demand = re.findall(r"^(\d+) (\d+)$", content, re.MULTILINE)
        
        # Data variables (casted)
        self.graph = {int(a):(int(b),int(c)) for a,b,c in graph}
        self.demand = {int(a):int(b) for a,b in demand}
        self.capacity = int(capacity)
        self.dimension = int(dimension)
        self.optimalValue = int(optimalValue)

    def getData(self):
        return self.capacity, self.graph, self.demand, self.optimalValue, self.dimension
        
    def generateGraph(self):
        vertices = list(self.graph.keys())
        vertices.remove(1)
        edges = { (min(a,b),max(a,b)) : numpy.sqrt((self.graph[a][0]-self.graph[b][0])**2 + (self.graph[a][1]-self.graph[b][1])**2) for a in self.graph.keys() for b in self.graph.keys()}
        feromones = { (min(a,b),max(a,b)) : 1 for a in self.graph.keys() for b in self.graph.keys() if a!=b }
        
        return vertices, edges, self.capacity, self.demand, feromones, self.optimalValue
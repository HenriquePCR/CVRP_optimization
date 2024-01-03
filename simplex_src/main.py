import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import re



print('''
    Available files:
        1 - E-n16-k8.txt
        2 - E-n19-k2.txt              
        3 - E-n22-k4.txt
        4 - E-n33-k4.txt        
    ''')

file_name = ''
    
while True:
    # User input for file selection
    file_num = input("Type in your file number:")
    if int(file_num) not in [1, 2, 3, 4, 5, 6, 7]:
        continue
    else:
        file_mapping = {
            '1': ".././datasets/E-n16-k8.txt",
            '2': ".././datasets/E-n19-k2.txt",
            '3': ".././datasets/E-n22-k4.txt",
            '4': ".././datasets/E-n33-k4.txt",
        }
        file_name = file_mapping[file_num]
        break

file_path = os.path.join(file_name)

def getData(fileName):
    f = open(file_path, "r")
    content = f.read()
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
    graph = {int(a):(int(b),int(c)) for a,b,c in graph}
    demand = {int(a):int(b) for a,b in demand}
    capacity = int(capacity)
    dimension = int(dimension)
    optimalValue = int(optimalValue)
    return capacity, graph, demand, optimalValue, dimension

capacityLimit, graph, demand, optimalValue, dimension = getData(file_name)

x_coordinates, y_coordinates = zip(*graph.values())
x_array = np.array(x_coordinates)
y_array = np.array(y_coordinates)

n = dimension-1 
xc = x_array
yc = y_array

N = [i for i in range(1, n+1)]
V = [0] + N
A = [(i, j) for i in V for j in V if i != j]
c = {(i, j): np.hypot(xc[i]-xc[j], yc[i]-yc[j]) for i, j in A}
Q = capacityLimit
q = list(demand.values())


from gurobipy import Model, GRB, quicksum

start_time = time.time()

mdl = Model('CVRP')
x = mdl.addVars(A, vtype=GRB.BINARY)
u = mdl.addVars(N, vtype=GRB.CONTINUOUS)

mdl.modelSense = GRB.MINIMIZE
mdl.setObjective(quicksum(x[i, j]*c[i, j] for i, j in A))

mdl.addConstrs(quicksum(x[i, j] for j in V if j != i) == 1 for i in N)
mdl.addConstrs(quicksum(x[i, j] for i in V if i != j) == 1 for j in N)
mdl.addConstrs((x[i, j] == 1) >> (u[i]+q[j] == u[j])
               for i, j in A if i != 0 and j != 0)
mdl.addConstrs(u[i] >= q[i] for i in N)
mdl.addConstrs(u[i] <= Q for i in N)

mdl.Params.MIPGap = 0
mdl.Params.TimeLimit = 5

mdl.optimize()

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Time Used: {elapsed_time} seconds")

active_arcs = [a for a in A if x[a].x > 0.99]

solution_value = mdl.objVal

for i, j in active_arcs:
    plt.plot([xc[i], xc[j]], [yc[i], yc[j]], c='g', zorder=0)
plt.plot(xc[0], yc[0], c='r', marker='s')
plt.scatter(xc[1:], yc[1:], c='b')
plt.title(f'Linear Programming Solution - Total Distance: {solution_value:.2f}')
plt.show()
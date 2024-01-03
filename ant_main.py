from ant_src.AntColony import AntColony
from ant_src.Exhibitor import Exhibitor
from ant_src.Graph import Graph

def main():
    # Instantiates ant colony
    ant_colony = AntColony()

    # Generates graph
    graph_wrapper = Graph(ant_colony.file_name)
    capacityLimit, graph, demand, optimalValue, dimension = graph_wrapper.getData()
    ant_colony.ants = dimension
    solution = ant_colony.iterate()
    xc, yc = zip(*graph.values())        
    modified_routes = [ant_colony.add_city_to_route(route) for route in solution[0]]

    # Exhibitor instance
    exhibitor = Exhibitor(solution[0], solution[1], xc, yc)
    exhibitor.plot_solution()


if __name__ == "__main__":
    main()
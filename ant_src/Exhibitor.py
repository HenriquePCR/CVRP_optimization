from matplotlib import pyplot as plt

class Exhibitor:

    def __init__(self, edges, total_distance, x_points, y_points):
        # Data variables
        self.edges = edges
        self.total_distance = total_distance
        # Must be extracted from graph with zip
        self.x_points = x_points
        self.y_points = y_points

    def plot_solution(self):
        # Plot active edges
        for edge in self.edges:
            for i in range(len(edge) - 1):
                plt.plot([self.x_points[edge[i] - 1], self.x_points[edge[i + 1] - 1]],\
                    [self.y_points[edge[i] - 1], self.y_points[edge[i + 1] - 1]], c='g', zorder=0)

        # Plot arrival/departure point
        plt.plot(self.x_points[0], self.y_points[0], c='r', marker='s', label='Arrival/Departure')

        # Plot other points
        plt.scatter(self.x_points[1:], self.y_points[1:], c='b', label='Points')

        plt.title(f'Ant Colony Solution - Total Distance: {self.total_distance:.2f}')
        plt.legend()
        plt.show()
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter


class Visualizacao:
    def __init__(self, routes, aco_vrp):
        self.routes = routes
        self.aco_vrp = aco_vrp
        self.coordinates = routes.coordinates
        self.demand = routes.demand
        self.distance_matrix = routes.distance_matrix
        self.best_solution = aco_vrp.best_solution
        self.solutions = aco_vrp.history["solution"]
        self.hist_costs = aco_vrp.history["cost"]

    def exibir_iteracoes_animado(self, file_name):
        colors = ["blue", "green", "red", "cyan", "magenta", "yellow", "black"]
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.grid(True)

        def init():
            self.identify_cities(ax)
            return []

        def update(frame):
            ax.clear()
            self.identify_cities(ax)
            ax.set_xlabel('Coordenada X')
            ax.set_ylabel('Coordenada Y')
            ax.grid(True)
            solution = self.solutions[frame]
            for vehicle_index, route in enumerate(solution):
                self.plot_vectors(ax, colors, route, vehicle_index)
            ax.set_title(f'Solução {frame + 1}')
            return []

        ani = FuncAnimation(fig, update, frames=len(self.solutions), init_func=init, blit=True, repeat=False)
        ani.save(f'Animacoes/{file_name}.gif', writer=PillowWriter(fps=1))

    def identify_cities(self, ax):
        for i, coord in enumerate(self.coordinates):
            ax.annotate(str(i), (coord[0], coord[1]),
                        fontsize=16, textcoords="offset points", xytext=(0, 10), ha='center')

    def plot_vectors(self, ax, colors, route, vehicle_index):
        route_coordinates = [self.coordinates[location] for location in route]
        route_coordinates = np.array(route_coordinates)
        for i in range(len(route_coordinates) - 1):
            atual_coord_x = float(route_coordinates[i][0])
            atual_coord_y = float(route_coordinates[i][1])
            proximo_coord_x = float(route_coordinates[i + 1][0])
            proximo_coord_y = float(route_coordinates[i + 1][1])
            ax.arrow(atual_coord_x, atual_coord_y, proximo_coord_x - atual_coord_x,
                     proximo_coord_y - atual_coord_y,
                     color=colors[vehicle_index % len(colors)], length_includes_head=True, head_width=5, width=1)
        ax.plot(route_coordinates[:, 0], route_coordinates[:, 1],
                color=colors[vehicle_index % len(colors)], marker='o', label=f'Veículo {vehicle_index + 1}')
        ax.legend()

    def plot_cost(self):
        plt.figure(figsize=(10, 8))
        iterations = []
        best_costs = []

        for _, iteration, best_cost in self.hist_costs:
            iterations.append(iteration)
            best_costs.append(best_cost)
        plt.plot(iterations, best_costs)

        plt.xlabel('Iteração')
        plt.ylabel('Custo')
        plt.title('Custo x Iteração')
        plt.grid()
        plt.show()

    def plot_cities(self):
        plt.figure(figsize=(10, 8))

        # Plotando as cidades
        for i, coord in enumerate(self.coordinates):
            if i == 0:  # Destacar o ponto inicial
                plt.scatter(coord[0], coord[1], s=100, c='green', marker='o')
            else:
                plt.scatter(coord[0], coord[1], c='blue', marker='o')
            plt.text(coord[0], coord[1], f' {i} (D: {self.demand[i]})', fontsize=16, ha='right')

        # Plotando as distâncias
        for i in range(len(self.coordinates)):
            for j in range(i + 1, len(self.coordinates)):
                if self.distance_matrix[i][j] != 0:
                    x_values = [self.coordinates[i][0], self.coordinates[j][0]]
                    y_values = [self.coordinates[i][1], self.coordinates[j][1]]
                    plt.plot(x_values, y_values, 'k--', alpha=0.5)
                    mid_x = (self.coordinates[i][0] + self.coordinates[j][0]) / 2
                    mid_y = (self.coordinates[i][1] + self.coordinates[j][1]) / 2
                    plt.text(mid_x, mid_y, f'{self.distance_matrix[i][j]:.1f}', fontsize=16, ha='center', va='center')

        plt.xlabel('Coordenada X')
        plt.ylabel('Coordenada Y')
        plt.title('Visualização das Cidades com Distâncias e Demandas')
        plt.grid()
        plt.show()

    def plot_solution(self):
        colors = ["blue", "green", "red", "cyan", "magenta", "yellow", "black"]

        plt.figure(figsize=(10, 8))
        for vehicle_index, route in enumerate(self.best_solution):
            self.plot_vectors(plt, colors, route, vehicle_index)
        self.identify_cities(plt)

        plt.xlabel('Coordenada X')
        plt.ylabel('Coordenada Y')
        plt.title('Rotas dos Veículos')
        plt.legend()
        plt.grid()
        plt.show()

    def pareto_plot(self):
        pareto_front = self.aco_vrp.best_pareto_front
        obj1 = [value[0] for value in pareto_front]
        obj2 = [value[1] for value in pareto_front]

        plt.figure(figsize=(10, 8))

        plt.scatter(obj1, obj2)

        plt.xlabel('Distância (Km)')
        plt.ylabel('Tempo (H)')
        plt.title('Fronte de Pareto: Distância x Tempo')
        plt.legend()
        plt.grid()
        plt.show()

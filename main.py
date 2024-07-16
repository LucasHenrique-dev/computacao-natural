import numpy as np

from aco import ACO_VRP
from rotas import Route
from visualizacao import Visualizacao

cities = 10
vehicle_capacity = 10
min_capacity_factor, max_capacity_factor = [0.2, 0.8]
min_coord, max_coord = [0, 50]
num_ants = 10
num_iterations = 100
max_stagnation = 10
random_seed = 1

np.random.seed(random_seed)

routes = Route(cities, vehicle_capacity)

aco = ACO_VRP(routes, vehicle_capacity, num_ants=num_ants, num_iterations=num_iterations, max_stagnation=max_stagnation)
best_solution, best_cost = aco.run()

visualizacao = Visualizacao(routes, aco)

visualizacao.plot_cities()
visualizacao.plot_solution()
visualizacao.plot_cost()
visualizacao.exibir_iteracoes_animado(file_name="teste")

print('Melhor solução:', best_solution)
print('Custo da melhor solução:', best_cost)

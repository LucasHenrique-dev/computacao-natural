import numpy as np

from aco import ACO_VRP, MO_ACO_VRP, MO_ACO_VRPT
from ortools_google import Google_OR_VRP
from rotas import Route, Route_Time
from visualizacao import Visualizacao

cities = 17  # 15
vehicle_capacity = 12
min_capacity_factor, max_capacity_factor = [0.2, 0.8]
min_coord, max_coord = [10, 50]
num_ants = 20
num_iterations = 300
max_stagnation = 20
max_time = 12
random_seed = 42

np.random.seed(random_seed)

routes = Route(cities, vehicle_capacity, min_deposit_coord=min_coord, max_deposit_coord=max_coord)
routes_time = Route_Time(cities, vehicle_capacity, max_time=max_time,
                         min_deposit_coord=min_coord, max_deposit_coord=max_coord)
routes.create_routes()
routes_time.create_routes()

# ACO BASE
# aco = ACO_VRP(routes, vehicle_capacity, num_ants=num_ants, num_iterations=num_iterations, max_stagnation=max_stagnation)
# best_solution, best_cost = aco.run()
#
# visualizacao = Visualizacao(routes, aco)
#
# visualizacao.plot_cities()
# visualizacao.plot_solution()
# visualizacao.plot_cost()
# visualizacao.exibir_iteracoes_animado(file_name="teste")
#
# print('Melhor solução:', best_solution)
# print('Custo da melhor solução:', best_cost)


# ACO MULTIOBJETIVO: VEÍCULOS X DISTÂNCIA
# mo_aco = MO_ACO_VRP(routes, vehicle_capacity, num_ants=num_ants, num_iterations=num_iterations,
#                     max_stagnation=max_stagnation)
# mo_aco.run()
#
# print(mo_aco.history["solution"])


# ACO MULTIOBJETIVO: DISTÂNCIA X TEMPO
# mo_aco_2 = MO_ACO_VRPT(routes_time, vehicle_capacity, num_ants=num_ants, num_iterations=num_iterations,
#                        max_stagnation=max_stagnation)
# pareto, solutions = mo_aco_2.run()
# solution_index = 0
# solution = pareto[solution_index]
#
# visualizacao = Visualizacao(routes_time, mo_aco_2)
#
# visualizacao.plot_cities_time()
# visualizacao.pareto_plot()
# visualizacao.plot_solution_index(solution_index)
#
# print(f"|Solution Index: {solution_index}| Distance: {solution[0]}| Time: {solution[1]}|")
# print("-="*100, "\nPareto: ", pareto)
# print("Routes:", solutions)


# GOOGLE OR (Operation Research)
# google_or = Google_OR_VRP(routes, 3)
# solucao, custo = google_or.solve_problem()
#
# if solucao:
#     solution_Google_OR = google_or.get_routes(solucao)
#     google_or.print_solution(solucao)
#
#     visualizacao = Visualizacao(routes, solution=solution_Google_OR)
#     visualizacao.plot_solution()
#     print(f'Custo: {custo} Km')
# else:
#     print('Não foi encontrada uma solução viável.')


# COMPARAR SOLUÇÕES
aco = ACO_VRP(routes, vehicle_capacity, num_ants=num_ants, num_iterations=num_iterations, max_stagnation=max_stagnation)
best_solution, best_cost = aco.run()
google_or = Google_OR_VRP(routes, 6)
solucao, custo = google_or.solve_problem()
print('Melhor solução:', best_solution)
print('Custo da melhor solução:', best_cost)

print("-="*100)

if solucao:
    solution_Google_OR = google_or.get_routes(solucao)
    google_or.print_solution(solucao)
    print(f'Custo: {custo} Km')

    visualizacao = Visualizacao(routes, aco_vrp=aco, solution=solution_Google_OR)
    visualizacao.plot_cities()
    visualizacao.plot_solution()
    visualizacao.plot_cost()
    visualizacao.comparar_graficos(best_solution, solution_Google_OR,
                                   titulo1="Solução ACO", titulo2="Solução Google OR")
else:
    print('Google OR: não foi encontrada uma solução viável.')

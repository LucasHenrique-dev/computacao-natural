from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from rotas import Route


class Google_OR_VRP:
    def __init__(self, route, num_vehicles):
        self.route = route
        self.num_vehicles = num_vehicles
        self.distance_matrix = self.route.distance_matrix
        self.deposit = 0
        self.data = self.create_data_model()
        self.manager, self.routing = self.create_route_model()
        self.search_parameters = self.define_OR()

    def create_data_model(self):
        """Stores the data for the problem."""
        data = {'distance_matrix': self.distance_matrix, 'num_vehicles': self.num_vehicles, 'depot': self.deposit,
                'demands': self.route.demand, 'vehicle_capacities': [self.route.capacity] * self.num_vehicles}

        return data

    def create_route_model(self):
        manager = pywrapcp.RoutingIndexManager(len(self.data['distance_matrix']), self.data['num_vehicles'],
                                               self.data['depot'])
        routing = pywrapcp.RoutingModel(manager)

        return manager, routing

    def distance_callback(self, from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = self.manager.IndexToNode(from_index)
        to_node = self.manager.IndexToNode(to_index)

        return self.data['distance_matrix'][from_node][to_node]

    def demand_callback(self, from_index):
        """Returns the demand of the node."""
        from_node = self.manager.IndexToNode(from_index)
        return self.data['demands'][from_node]

    def set_distances_and_demands(self):
        transit_callback_index = self.routing.RegisterTransitCallback(self.distance_callback)
        self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        demand_callback_index = self.routing.RegisterUnaryTransitCallback(self.demand_callback)
        self.routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # Null capacity slack
            self.data['vehicle_capacities'],  # Vehicle maximum capacities
            True,  # Start cumul to zero
            'Capacity'
        )

    def define_OR(self):
        # ABORDAGEM TRADICIONAL
        # search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        # search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()

        # ABORDAGEM DE BUSCA LOCAL (FOGE DE MINIMOS LOCAIS)
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        search_parameters.time_limit.seconds = 10
        # search_parameters.log_search = True  # DEBUG

        return search_parameters

    def get_routes(self, solution):
        """Get vehicle routes from a solution and store them in an array."""
        routes = []
        for route_nbr in range(self.data['num_vehicles']):
            index = self.routing.Start(route_nbr)
            route = []
            while not self.routing.IsEnd(index):
                route.append(self.manager.IndexToNode(index))
                index = solution.Value(self.routing.NextVar(index))
            route.append(self.manager.IndexToNode(index))  # Adiciona o depósito ao final da rota
            routes.append(route)
        return routes

    def print_solution(self, solution):
        """Prints solution on console."""
        print('Objective: {} Km'.format(solution.ObjectiveValue()))
        for vehicle_id in range(self.data['num_vehicles']):
            index = self.routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            route_distance = 0
            while not self.routing.IsEnd(index):
                plan_output += ' {} ->'.format(self.manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(self.routing.NextVar(index))
                route_distance += self.routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            plan_output += ' {}\n'.format(self.manager.IndexToNode(index))
            plan_output += 'Distance of the route: {} Km\n'.format(route_distance)
            print(plan_output)

    def solve_problem(self):
        self.set_distances_and_demands()
        solution = self.routing.SolveWithParameters(self.search_parameters)
        if solution:
            custo_Google_OR = solution.ObjectiveValue()
            return solution, custo_Google_OR
        else:
            print('No solution found!')
            return None, None


if __name__ == '__main__':
    rota = Route(10, 5)
    rota.create_routes()

    print(rota.get_coordinates())
    print(rota.get_demand())
    print(rota.get_distance_matrix())

    print(f"\n{'-='*100}\n")

    google_or = Google_OR_VRP(rota, 3)
    solucao, custo = google_or.solve_problem()

    if solucao:
        solution_Google_OR = google_or.get_routes(solucao)
        google_or.print_solution(solucao)
        print(f'Custo: {custo} Km')
    else:
        print('Não foi encontrada uma solução viável.')

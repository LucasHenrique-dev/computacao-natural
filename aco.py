import numpy as np


class ACO_VRP:
    def __init__(self, routes, vehicle_capacity, num_ants, num_iterations, alpha=1.0, beta=2.0, rho=0.5, Q=10,
                 max_stagnation=5):
        coordinates, demand, distance_matrix = routes.create_routes()
        self.vehicle_capacity = vehicle_capacity
        self.demand = demand
        self.distance_matrix = distance_matrix
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.num_customers = len(demand)
        self.pheromone = np.ones((self.num_customers, self.num_customers))
        self.best_solution = None
        self.best_cost = float('inf')
        self.max_stagnation = max_stagnation
        self.history = {"cost": [], "solution": []}

    def run(self):
        num_vehicles = int(np.ceil(sum(self.demand)/self.vehicle_capacity))
        stagnation = True

        while stagnation:
            print(f'Trying with {num_vehicles} vehicles')
            try:
                for iteration in range(self.num_iterations):
                    solutions = self.construct_solutions(num_vehicles)
                    self.update_pheromone(solutions)
                    self.update_best_solution(solutions)
                    self.history["cost"].append((num_vehicles, iteration, self.best_cost))
                    print(f'Iteration {iteration + 1}: Best cost = {self.best_cost}')
                stagnation = False
            except ValueError:
                stagnation = True
                pass
            num_vehicles += 1
            self.pheromone = np.ones((self.num_customers, self.num_customers))
        return self.best_solution, self.best_cost

    def construct_solutions(self, num_vehicles):
        solutions = []
        for _ in range(self.num_ants):
            solution = self.construct_solution(num_vehicles)
            solutions.append(solution)
        return solutions

    def construct_solution(self, num_vehicles):
        stagnation_counter = 0
        remaining_customers = set(range(1, self.num_customers))
        vehicle_loads = [0] * num_vehicles
        vehicle_routes = [[0] for _ in range(num_vehicles)]

        while stagnation_counter < self.max_stagnation:
            if not remaining_customers:
                break
            while remaining_customers:
                progress_made = False
                for vehicle in range(num_vehicles):
                    if not remaining_customers:
                        break
                    current_location = vehicle_routes[vehicle][-1]
                    next_customer = self.select_next_customer(current_location, remaining_customers,
                                                              vehicle_loads[vehicle])
                    if next_customer is not None:
                        vehicle_routes[vehicle].append(next_customer)
                        vehicle_loads[vehicle] += self.demand[next_customer]
                        remaining_customers.remove(next_customer)
                        progress_made = True
                    else:
                        vehicle_routes[vehicle].append(0)

                if not progress_made:
                    stagnation_counter += 1

                    if stagnation_counter >= self.max_stagnation:
                        raise ValueError("Não é possível construir uma solução com o número atual de veículos.")

                    remaining_customers = set(range(1, self.num_customers))
                    vehicle_loads = [0] * num_vehicles
                    vehicle_routes = [[0] for _ in range(num_vehicles)]

        for route in vehicle_routes:
            if route[-1] != 0:
                route.append(0)

        return vehicle_routes

    def select_next_customer(self, current_location, remaining_customers, current_load):
        probabilities = []
        for customer in remaining_customers:
            if current_load + self.demand[customer] <= self.vehicle_capacity:
                prob = ((self.pheromone[current_location][customer] ** self.alpha) *
                        ((1.0 / self.distance_matrix[current_location][customer]) ** self.beta))
                probabilities.append((customer, prob))

        if not probabilities:
            return None

        total_prob = sum(prob for _, prob in probabilities)
        probabilities = [(customer, prob / total_prob) for customer, prob in probabilities]
        r = np.random.rand()
        cumulative_prob = 0.0
        for customer, prob in probabilities:
            cumulative_prob += prob
            if r <= cumulative_prob:
                return customer
        return None

    def update_pheromone(self, solutions):
        self.pheromone *= (1 - self.rho)
        for solution in solutions:
            cost = self.calculate_cost(solution)
            for route in solution:
                for i in range(len(route) - 1):
                    self.pheromone[route[i]][route[i + 1]] += self.Q / cost

    def update_best_solution(self, solutions):
        for solution in solutions:
            cost = self.calculate_cost(solution)
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_solution = solution
                self.history["solution"].append(self.best_solution)

    def calculate_cost(self, solution):
        total_cost = 0
        for route in solution:
            route_cost = 0
            for i in range(len(route) - 1):
                route_cost += self.distance_matrix[route[i]][route[i + 1]]
            total_cost += route_cost
        return total_cost

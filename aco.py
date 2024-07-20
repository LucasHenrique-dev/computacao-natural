import numpy as np


class ACO_VRP:
    def __init__(self, routes, vehicle_capacity, num_ants, num_iterations, alpha=1.0, beta=2.0, rho=0.5, Q=10,
                 max_stagnation=5):
        routes.create_routes()
        self.vehicle_capacity = vehicle_capacity
        self.demand = routes.get_demand()
        self.distance_matrix = routes.get_distance_matrix()
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.num_customers = len(self.demand)
        self.pheromone = np.ones((self.num_customers, self.num_customers))
        self.best_solution = None
        self.best_cost = float('inf')
        self.max_stagnation = max_stagnation
        self.history = {"cost": [], "solution": []}

    def run(self):
        num_vehicles = int(np.ceil(sum(self.demand)/self.vehicle_capacity))
        stagnation = True

        while stagnation:
            print(f'{"-="*15} Trying with {num_vehicles} vehicles {"=-"*15}')
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


class MO_ACO_VRP(ACO_VRP):
    def __init__(self, routes, vehicle_capacity, num_ants, num_iterations, alpha=1.0, beta=2.0, rho=0.5, Q=10,
                 max_stagnation=5, veichle_reset=5):
        super().__init__(routes, vehicle_capacity, num_ants, num_iterations, alpha, beta, rho, Q, max_stagnation)
        routes.create_routes()
        self.vehicle_capacity = vehicle_capacity
        self.demand = routes.get_demand()
        self.distance_matrix = routes.get_distance_matrix()
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.num_customers = len(self.demand)
        self.pheromone = np.ones((self.num_customers, self.num_customers))
        self.best_solution = None
        self.best_cost = float('inf')
        self.num_vehicles = int(np.ceil(sum(self.demand)/self.vehicle_capacity))
        self.max_stagnation = max_stagnation
        self.veichle_reset = veichle_reset
        self.history = {"cost": [], "solution": []}

    def run(self):
        reset = 0
        stagnation_counter = 0

        while reset < self.veichle_reset:
            print(f'{"-="*15} Trying with {self.num_vehicles} vehicles {"=-"*15}')
            try:
                for iteration in range(self.num_iterations):
                    solutions = self.construct_solutions(self.num_vehicles)
                    self.update_pheromone(solutions)
                    best_cost_before = self.best_cost
                    self.update_best_solution(solutions)
                    if self.best_cost == best_cost_before:
                        stagnation_counter += 1
                    else:
                        stagnation_counter = 0
                    self.history["cost"].append((self.num_vehicles, iteration, self.best_cost))
                    print(f'Iteration {iteration + 1}: Best cost = {self.best_cost}')
                    if stagnation_counter > self.max_stagnation:
                        stagnation_counter = 0
                        reset += 1
                        break
            except ValueError:
                pass
            self.num_vehicles += 1
            self.pheromone = np.ones((self.num_customers, self.num_customers))

    def update_best_solution(self, solutions):
        for solution in solutions:
            cost = self.calculate_cost(solution)
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_solution = (self.num_vehicles, solution)
                self.history["solution"].append(self.best_solution)


class MO_ACO_VRPT(ACO_VRP):
    def __init__(self, routes, vehicle_capacity, num_ants, num_iterations, alpha=1.0, beta=2.0, rho=0.5, Q=10,
                 max_stagnation=5, num_veichle=5):
        super().__init__(routes, vehicle_capacity, num_ants, num_iterations, alpha, beta, rho, Q, max_stagnation)
        routes.create_routes()
        self.vehicle_capacity = vehicle_capacity
        self.demand = routes.get_demand()
        self.distance_matrix = routes.get_distance_matrix()
        self.time_matrix = routes.get_time_matrix()
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.num_customers = len(self.demand)
        self.pheromone = np.ones((self.num_customers, self.num_customers))
        self.best_solution = None
        self.best_cost = float('inf')
        self.num_vehicles = int(np.ceil(sum(self.demand)/self.vehicle_capacity))
        self.max_stagnation = max_stagnation
        self.num_veichle = num_veichle
        self.best_pareto_front = []

    def run(self):
        all_solutions = []
        stagnation = True

        while stagnation:
            print(f'{"-="*15} Trying with {self.num_vehicles} vehicles {"=-"*15}')
            try:
                for iteration in range(self.num_iterations):
                    solutions = self._construct_solutions()
                    self._update_pheromone(solutions)
                    all_solutions.extend(solutions)
                    print(f'Iteration {iteration + 1}')
                stagnation = False
            except ValueError:
                stagnation = True
                pass
            self.num_vehicles += 1
            self.pheromone = np.ones((self.num_customers, self.num_customers))

        self.best_pareto_front = self._get_pareto_front(all_solutions)

        # all_solutions = []
        # for iteration in range(self.num_iterations):
        #     solutions = self._construct_solutions()
        #     self._update_pheromone(solutions)
        #     all_solutions.extend(solutions)
        #
        # self.best_pareto_front = self._get_pareto_front(all_solutions)

        return self.best_pareto_front

    def _construct_solutions(self):
        solutions = []
        for _ in range(self.num_ants):
            solution = self._construct_solution()
            solutions.append(solution)
        return solutions

    def _construct_solution(self):
        # stagnation_counter = 0
        # remaining_customers = set(range(1, self.num_customers))
        # vehicle_loads = [0] * num_vehicles
        # vehicle_routes = [[0] for _ in range(num_vehicles)]
        #
        # while stagnation_counter < self.max_stagnation:
        #     if not remaining_customers:
        #         break
        #     while remaining_customers:
        #         progress_made = False
        #         for vehicle in range(num_vehicles):
        #             if not remaining_customers:
        #                 break
        #             current_location = vehicle_routes[vehicle][-1]
        #             next_customer = self.select_next_customer(current_location, remaining_customers,
        #                                                       vehicle_loads[vehicle])
        #             if next_customer is not None:
        #                 vehicle_routes[vehicle].append(next_customer)
        #                 vehicle_loads[vehicle] += self.demand[next_customer]
        #                 remaining_customers.remove(next_customer)
        #                 progress_made = True
        #             else:
        #                 vehicle_routes[vehicle].append(0)
        #
        #         if not progress_made:
        #             stagnation_counter += 1
        #
        #             if stagnation_counter >= self.max_stagnation:
        #                 raise ValueError("Não é possível construir uma solução com o número atual de veículos.")
        #
        #             remaining_customers = set(range(1, self.num_customers))
        #             vehicle_loads = [0] * num_vehicles
        #             vehicle_routes = [[0] for _ in range(num_vehicles)]
        #
        # for route in vehicle_routes:
        #     if route[-1] != 0:
        #         route.append(0)

        # Similar ao ACO_VRP mas ajustado para multiobjetivo
        stagnation_counter = 0
        solution = [[] for _ in range(self.num_vehicles)]
        remaining_customers = set(range(1, self.num_customers))

        while stagnation_counter < self.max_stagnation:
            for vehicle_index in range(self.num_vehicles):
                current_load = 0
                current_position = 0
                while remaining_customers and current_load < self.vehicle_capacity:
                    next_customer = self._select_next_customer(current_position, remaining_customers)
                    if current_load + self.demand[next_customer] <= self.vehicle_capacity:
                        solution[vehicle_index].append(next_customer)
                        current_load += self.demand[next_customer]
                        remaining_customers.remove(next_customer)
                        current_position = next_customer
                    else:
                        break
                solution[vehicle_index].append(0)

            if remaining_customers:
                remaining_customers = set(range(1, self.num_customers))
                stagnation_counter += 1

                if stagnation_counter >= self.max_stagnation:
                    raise ValueError("Não é possível construir uma solução com o número atual de veículos.")
            else:
                break

        return solution

    def _select_next_customer(self, current_position, remaining_customers):
        probabilities = []
        for customer in remaining_customers:
            pheromone = self.pheromone[current_position][customer]
            distance = self.distance_matrix[current_position][customer]
            time = self.time_matrix[current_position][customer]
            prob = (pheromone ** self.alpha) * ((1.0 / distance) ** self.beta) * ((1.0 / time) ** self.beta)
            probabilities.append(prob)
        probabilities = np.array(probabilities) / np.sum(probabilities)
        return np.random.choice(list(remaining_customers), p=probabilities)

    def _evaluate_solution(self, solution):
        total_distance = 0
        total_time = 0
        for route in solution:
            for i in range(len(route) - 1):
                total_distance += self.distance_matrix[route[i]][route[i + 1]]
                total_time += self.time_matrix[route[i]][route[i + 1]]
        return total_distance, total_time

    def _update_pheromone(self, solutions):
        self.pheromone *= (1 - self.rho)
        for solution in solutions:
            total_distance, total_time = self._evaluate_solution(solution)
            for route in solution:
                for i in range(len(route) - 1):
                    self.pheromone[route[i]][route[i + 1]] += self.Q / (total_distance + total_time)

    def _get_pareto_front(self, solutions):
        pareto_front = []
        for solution in solutions:
            total_distance, total_time = self._evaluate_solution(solution)
            dominated = False
            for pareto_solution in pareto_front:
                if (pareto_solution[0] <= total_distance and pareto_solution[1] < total_time) or \
                        (pareto_solution[0] < total_distance and pareto_solution[1] <= total_time):
                    dominated = True
                    break
            if not dominated:
                pareto_front = [sol for sol in pareto_front if not ((sol[0] >= total_distance and sol[1] > total_time) or
                                                                    (sol[0] > total_distance and sol[1] >= total_time))]
                pareto_front.append((total_distance, total_time))
        return pareto_front

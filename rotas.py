import numpy as np


class Route:
    def __init__(self, num_cities, capacity, min_capacity_factor=0.2, max_capacity_factor=0.6,
                 min_deposit_coord=10, max_deposit_coord=50, min_coord_factor=-5, max_coord_factor=5):
        self.num_cities = num_cities
        self.capacity = capacity
        self.coordinates = []
        self.demand = []
        self.distance_matrix = []
        self.min_deposit_coord = min_deposit_coord
        self.max_deposit_coord = max_deposit_coord
        self.min_coord_factor = min_coord_factor
        self.max_coord_factor = max_coord_factor
        self.min_capacity_factor = min_capacity_factor
        self.max_capacity_factor = max_capacity_factor
        self.min_demand = capacity * min_capacity_factor
        self.max_demand = capacity * max_capacity_factor

    def create_routes(self):
        self.add_city()
        self.add_demand()
        self.add_distance_manhattan()  # Euclidean OR Manhattan

    def add_city(self):
        # Coordenadas do Depósito
        self.coordinates.append(tuple(np.random.randint(self.min_deposit_coord, self.max_deposit_coord, 2)))
        deposito_x = self.coordinates[0][0]
        deposito_y = self.coordinates[0][1]

        # Coordenadas cidades entorno do depósito
        while len(self.coordinates) < self.num_cities:
            factor_x = np.random.uniform(self.min_coord_factor, self.max_coord_factor)
            factor_y = np.random.uniform(self.min_coord_factor, self.max_coord_factor)

            coordinates = tuple((np.int32(deposito_x*factor_x)+deposito_x, np.int32((deposito_y*factor_y)))+deposito_y)

            if tuple(coordinates) not in set(self.coordinates):
                self.coordinates.append(coordinates)

    def add_demand(self):
        # Demanda do Depósito
        self.demand.append(0)

        # Demanda das Cidades
        self.demand[1:] = np.random.randint(self.min_demand, self.max_demand, size=self.num_cities - 1)

    def add_distance_euclidean(self):
        for i in range(self.num_cities):
            distances = []
            for j in range(self.num_cities):
                diff_x = self.coordinates[i][0] - self.coordinates[j][0]
                diff_y = self.coordinates[i][1] - self.coordinates[j][1]
                distances.append(np.sqrt(diff_x ** 2 + diff_y ** 2))

            self.distance_matrix.append(distances)

    def add_distance_manhattan(self):
        for i in range(self.num_cities):
            pos_x1, pos_y1 = self.coordinates[i][0], self.coordinates[i][1]
            distances = []
            for j in range(self.num_cities):
                pos_x2, pos_y2 = self.coordinates[j][0], self.coordinates[j][1]
                distances.append(abs(pos_x1 - pos_x2) + abs(pos_y1 - pos_y2))

            self.distance_matrix.append(distances)

    def get_demand(self):
        return self.demand

    def get_distance_matrix(self):
        return self.distance_matrix

    def get_coordinates(self):
        return self.coordinates


class Route_Time(Route):
    def __init__(self, num_cities, capacity, min_capacity_factor=0.2, max_capacity_factor=0.6, min_deposit_coord=10,
                 max_deposit_coord=50, min_coord_factor=-5, max_coord_factor=5, min_time=1, max_time=5):
        super().__init__(num_cities, capacity, min_capacity_factor, max_capacity_factor, min_deposit_coord,
                         max_deposit_coord, min_coord_factor, max_coord_factor)
        self.time_matrix = np.zeros((self.num_cities, self.num_cities), dtype=int)
        self.min_time = min_time
        self.max_time = max_time

    def create_routes(self):
        self.add_city()
        self.add_demand()
        self.add_distance_manhattan()  # Euclidean OR Manhattan
        self.add_time()

    def add_time(self):
        # Preencher apenas a metade superior da matriz (excluindo a diagonal)
        for i in range(self.num_cities):
            for j in range(i + 1, self.num_cities):
                time_value = np.random.randint(self.min_time, self.max_time)
                self.time_matrix[i][j] = time_value
                self.time_matrix[j][i] = time_value

        # A diagonal deve ser zero
        np.fill_diagonal(self.time_matrix, 0)

    def get_time_matrix(self):
        return self.time_matrix


if __name__ == '__main__':
    # DISTÂNCIAS
    print("APENAS DISTÂNCIAS")
    route = Route(10, 100)
    route.create_routes()
    print(route.get_coordinates())
    print(route.get_demand())
    print(route.get_distance_matrix())

    print(f"\n{'-='*100}\n")

    # DISTÂNCIAS E TEMPO
    print("DISTÂNCIAS E TEMPO")
    route = Route_Time(10, 100)
    route.create_routes()
    print(route.get_coordinates())
    print(route.get_demand())
    print(route.get_distance_matrix())
    print(route.get_time_matrix())

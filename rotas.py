import numpy as np


class Route:
    def __init__(self, num_cities, capacity, min_capacity_factor=0.2, max_capacity_factor=0.6,
                 min_coord=0, max_coord=50):
        self.num_cities = num_cities
        self.capacity = capacity
        self.coordinates = []
        self.demand = []
        self.distance_matrix = []
        self.min_coord = min_coord
        self.max_coord = max_coord
        self.min_capacity_factor = min_capacity_factor
        self.max_capacity_factor = max_capacity_factor
        self.min_demand = capacity * min_capacity_factor
        self.max_demand = capacity * max_capacity_factor

    def create_routes(self):
        self.add_city()
        self.add_demand()
        self.add_distance()

        return self.coordinates, self.demand, self.distance_matrix

    def add_city(self):
        self.coordinates = np.random.randint(self.min_coord, self.max_coord, size=(self.num_cities, 2))

    def add_demand(self):
        self.demand = np.random.randint(self.min_demand, self.max_demand, size=self.num_cities)

    def add_distance(self):
        for i in range(self.num_cities):
            distances = []
            for j in range(self.num_cities):
                diff_x = self.coordinates[i][0] - self.coordinates[j][0]
                diff_y = self.coordinates[i][1] - self.coordinates[j][1]
                distances.append(np.sqrt(diff_x ** 2 + diff_y ** 2))

            self.distance_matrix.append(distances)


if __name__ == '__main__':
    route = Route(10, 100)
    coord, demand, matrix_distances = route.create_routes()
    print(coord)
    print(demand)
    print(matrix_distances)

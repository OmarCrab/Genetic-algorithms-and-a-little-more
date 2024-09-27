import random

import numpy as np
import matplotlib.pyplot as plt

import tsp


class VehicleRoutingProblem:

    def __init__(self, tspName, numOfVehicles, depotIndex):

        self.tsp = tsp.TravelingSalesmanProblem(tspName)
        self.numOfVehicles = numOfVehicles
        self.depotIndex = depotIndex

    def __len__(self):

        return len(self.tsp) + self.numOfVehicles - 1

    def getRoutes(self, indices):

        # initialize lists:
        routes = []
        route = []

        # loop over all indices in the list:
        for i in indices:

            # skip depot index:
            if i == self.depotIndex:
                continue

            # index is part of the current route:
            if not self.isSeparatorIndex(i):
                route.append(i)

            # separator index - route is complete:
            else:
                routes.append(route)
                route = []  # reset route

        # append the last route:
        if route or self.isSeparatorIndex(i):
            routes.append(route)

        return routes

    def isSeparatorIndex(self, index):

        # check if the index is larger than the number of the participating locations:
        return index >= len(self) - (self.numOfVehicles - 1)

    def getRouteDistance(self, indices):

        if not indices:
            return 0

        # find the distance between the depo location and the city:
        distance = self.tsp.distances[self.depotIndex][indices[0]]

        # add the distance between the last city and the depot location:
        distance += self.tsp.distances[indices[-1]][self.depotIndex]

        # add the distances between the cities along the route:
        for i in range(len(indices) - 1):
            distance += self.tsp.distances[indices[i]][indices[i + 1]]
        return distance

    def getTotalDistance(self, indices):

        totalDistance = 0
        for route in self.getRoutes(indices):
            routeDistance = self.getRouteDistance(route)
            #print("- route distance = ", routeDistance)
            totalDistance += routeDistance
        return totalDistance

    def getMaxDistance(self, indices):

        maxDistance = 0
        for route in self.getRoutes(indices):
            routeDistance = self.getRouteDistance(route)
            #print("- route distance = ", routeDistance)
            maxDistance = max(routeDistance, maxDistance)
        return maxDistance

    def getAvgDistance(self, indices):

        routes = self.getRoutes(indices)
        totalDistance = 0
        counter = 0
        for route in routes:
            if route:  # consider only routes that are not empty
                routeDistance = self.getRouteDistance(route)
                # print("- route distance = ", routeDistance)
                totalDistance += routeDistance
                counter += 1
        return totalDistance/counter

    def plotData(self, indices):

        # plot th ecities of the underlying TSP:
        plt.scatter(*zip(*self.tsp.locations), marker='.', color='red')

        # mark the depot location with a large 'X':
        d = self.tsp.locations[self.depotIndex]
        plt.plot(d[0], d[1], marker='x', markersize=10, color='green')

        # break the indices to separate routes and plot each route in a different color:
        routes = self.getRoutes(indices)
        color = iter(plt.cm.rainbow(np.linspace(0, 1, self.numOfVehicles)))
        for route in routes:
            route = [self.depotIndex] + route + [self.depotIndex]
            stops = [self.tsp.locations[i] for i in route]
            plt.plot(*zip(*stops), linestyle='-', color=next(color))

        return plt


def main():
    # create a problem instance:
    vrp = VehicleRoutingProblem("bayg29", 3, 12)

    # generate random solution and evaluate it:
    randomSolution = random.sample(range(len(vrp)), len(vrp))
    print("random solution = ", randomSolution)
    print("route breakdown = ", vrp.getRoutes(randomSolution))
    print("max distance = ", vrp.getMaxDistance(randomSolution))

    # plot the solution:
    plot = vrp.plotData(randomSolution)
    plot.show()


if __name__ == "__main__":
    main()

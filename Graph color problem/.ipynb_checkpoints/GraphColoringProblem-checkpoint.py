import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

import scipy

class GraphColoringProblem:
    def __init__ (self, graph, hardConstrainPenalty):
        self.graph = graph
        self.hardConstrainPenalty = hardConstrainPenalty

        self.nodeList = list(self.graph.nodes)
        self.adjMatrix = nx.adjacency_matrix(graph).todense()

    def __len__(self):
        return nx.number_of_nodes(self.graph)

    def getCost(self, colorArrangement):
        return self.hardConstrainPenalty * self.getViolationsCount(colorArrangement) + self.getNumberOfColors(colorArrangement)
    
    def getNumberOfColors(self, colorArrangement):
        return len(set(colorArrangement))
        
    def getViolationsCount(self, colorArrangement):

        if len(colorArrangement) != self.__len__():
            raise ValueError("Количество цветов должно быть эквивалентно ", self.__len__())

        violations = 0

        for i in range(len(colorArrangement)):
            for j in range(i + 1, len(colorArrangement)):

                if self.adjMatrix[i, j]:    
                    if colorArrangement[i] == colorArrangement[j]:
                        violations += 1

        return violations

    def plotGraph(self, colorArrangement):
        if len(colorArrangement) != self.__len__():
            raise ValueError("size of color list should be equal to ", self.__len__())

        # create a list of the unique colors in the arrangement:
        colorList = list(set(colorArrangement))

        # create the actual colors for the integers in the color list:
        colors = plt.cm.rainbow(np.linspace(0, 1, len(colorList)))

        # iterate over the nodes, and give each one of them its corresponding color:
        colorMap = []
        for i in range(self.__len__()):
            color = colors[colorList.index(colorArrangement[i])]
            colorMap.append(color)

        # plot the nodes with their labels and matching colors:
        nx.draw_kamada_kawai(self.graph, node_color=colorMap, with_labels=True)
        #nx.draw_circular(self.graph, node_color=color_map, with_labels=True)

        return plt


def main():
    # create a problem instance with petersen graph:
    gcp = GraphColoringProblem(nx.petersen_graph(), 10)

    # generate a random solution with up to 5 different colors:
    solution = np.random.randint(5, size=len(gcp))

    print("solution = ", solution)
    print("number of colors = ", gcp.getNumberOfColors(solution))
    print("Number of violations = ", gcp.getViolationsCount(solution))
    print("Cost = ", gcp.getCost(solution))

    plot = gcp.plotGraph(solution)
    plot.show()


if __name__ == "__main__":
    main()
        
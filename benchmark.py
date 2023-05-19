import timeit
import networkx as nx
import igraph as ig
import numpy as np
# import graph_tool.all as gt
#from snap import GenRndGnm


def benchmark_erdos_renyi(n, p, num_graphs):
    # NetworkX benchmark
    def networkx_benchmark():
        for _ in range(num_graphs):
            G = nx.erdos_renyi_graph(n, p)
        return G

    networkx_time = timeit.timeit(networkx_benchmark, number=1)

    # igraph benchmark
    def igraph_benchmark():
        for _ in range(num_graphs):
            G = ig.Graph.Erdos_Renyi(n, p)
            G.random_walk()
        return G

    igraph_time = timeit.timeit(igraph_benchmark, number=1)

    # numpy benchmark
    def numpy_benchmark():
        for _ in range(num_graphs):
            adjacency_matrix = np.random.choice([0, 1], size=(n, n), p=[1 - p, p])
            G = nx.from_numpy_array(adjacency_matrix)
        return G

    numpy_time = timeit.timeit(numpy_benchmark, number=1)

    # graph-tool benchmark
    # def graph_tool_benchmark():
    #     for _ in range(num_graphs):
    #         G = gt.random_graph(n, lambda: np.random.random() < p)
    #     return G
    #
    # graph_tool_time = timeit.timeit(graph_tool_benchmark, number=1)

    # SNAP benchmark
    # def snap_benchmark():
    #     for _ in range(num_graphs):
    #         G = GenRndGnm(snap.PUNGraph, n, int(n * (n - 1) * p / 2))
    #     return G
    #
    # snap_time = timeit.timeit(snap_benchmark, number=1)

    print(f"NetworkX time: {networkx_time} seconds")
    print(f"igraph time: {igraph_time} seconds")
    print(f"numpy time: {numpy_time} seconds")
    # print(f"graph-tool time: {graph_tool_time} seconds")
    # print(f"SNAP time: {snap_time} seconds")


# Example usage
n_nodes = 1000
p_value = 2/n_nodes
num_graphs = 10000
benchmark_erdos_renyi(n_nodes, p_value, num_graphs)

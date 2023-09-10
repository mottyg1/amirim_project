import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
from utils import random_walk_until_return, walk_stats
from tqdm import tqdm


def plot_graph_with_2core(g, fig_size=(20, 20), label_size=20):
    # Compute the 2-core of the graph
    core = g.shell_index(mode='OUT')

    # Create a color map for the vertices based on core
    colors = ['red' if c >= 2 else 'blue' for v, c in enumerate(core)]

    layout = g.layout_fruchterman_reingold()

    _, ax = plt.subplots(figsize=fig_size)
    # Plot the graph
    ig.plot(g, target=ax, vertex_color=colors, layout=layout, vertex_label=[str(v.index) for v in g.vs],
            vertex_label_size=label_size)
    plt.axis("off")
    plt.show()


def get_transition_matrix(g):
    vertex_degree = np.array(g.outdegree())
    a = np.array(g.get_adjacency().data, dtype=float)
    b = np.array(vertex_degree[:, np.newaxis], dtype=float)
    return np.divide(a, b, out=np.zeros_like(a), where=b != 0)


def get_punctured_transition_matrix(g, start_index):
    initial_state = get_initial_state(len(g.vs), start_index)
    T = get_transition_matrix(g)
    T[start_index] = initial_state
    return T


def get_initial_state(length, start_index):
    # Create a vector of zeros with the desired length
    vector = np.zeros(length)

    # Set the desired index to one
    vector[start_index] = 1

    return vector


def get_probabilities(g, start_index, max_steps):
    initial_state = get_initial_state(len(g.vs), start_index)
    T = get_transition_matrix(g)
    step_one_state = initial_state @ T
    T[start_index] = initial_state
    steps = range(2, max_steps)
    probabilities = []
    current_state = step_one_state
    for _ in steps:
        current_state = current_state @ T
        step_probability = current_state[start_index] - sum(probabilities)
        probabilities.append(step_probability)

    # probabilities.append(1 - sum(probabilities))

    return probabilities

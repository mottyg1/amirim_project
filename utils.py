import random
from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx


def plot_random_graph(g, node_size=70, cmap='Set1_r', algorithm='neato', highlight=[]):
    # Compute the k-core decomposition of the graph
    core_numbers = nx.core_number(g)

    # Use the neato layout algorithm from Graphviz to calculate node positions
    pos = nx.nx_agraph.graphviz_layout(g, prog=algorithm)

    # Define the colormap and labels for the legend
    cmap = plt.cm.get_cmap(cmap, max(core_numbers.values()) + 1)
    labels = [f'K-core {i}' for i in range(max(core_numbers.values()) + 1)]

    # Assign a color to each node based on its k-core
    node_colors = [cmap(core_numbers[node]) for node in g.nodes()]
    edge_colors = [cmap(core_numbers[node]) if node not in highlight else 'green' for node in g.nodes()]

    # Draw the nodes and edges of the graph with the constant node size and colors
    nx.draw_networkx_nodes(g, pos, node_size=node_size, node_color=node_colors, edgecolors=edge_colors, alpha=0.8)
    nx.draw_networkx_edges(g, pos, edge_color='black')
    nx.draw_networkx_labels(g, pos, font_size=7)

    # Create the legend with discrete colors and labels
    legend_elements = [(plt.Circle((0, 0), 0, color=cmap(i)), label) for i, label in enumerate(labels)]
    plt.legend(*zip(*legend_elements), title='K-core number')

    # Set the figure size
    plt.gcf().set_size_inches(8, 8)

    # Show the plot
    plt.show()


def is_retroceding(walk):
    length = len(walk)

    if length % 2 == 1:  # should be an even number of steps
        return False

    return walk[1:] == walk[length:0:-1]


def started_in_2core(g, walk):
    start_node = walk[0]
    return nx.core_number(g)[start_node] >= 2


def in_giant_component(g, walk):
    return walk[0] in max(nx.connected_components(g), key=len)


def random_walk(g):
    start_node = random.choice(list(g.nodes()))

    walk = [start_node]

    current_node = start_node
    while True:
        neighbors = list(g.neighbors(current_node))
        if len(neighbors) == 0:
            break
        next_node = random.choice(neighbors)
        if next_node == start_node:
            break
        walk.append(next_node)
        current_node = next_node

    return walk


def walk_stats(g, walk):
    return {
        'walk_length': len(walk),
        'in_giant_component': in_giant_component(g, walk),
        'started_in_2core': started_in_2core(g, walk),
        'distinct_sites': len(set(walk)),
        'is_retroceding': is_retroceding(walk)
    }

# def random_walk_old(g):
#     # Pick a random starting node
#     start_node = random.choice(list(g.nodes()))
#
#     # Initialize the visited nodes list
#     visited_nodes = [start_node]
#
#     # Initialize the component size, k-core number, and giant component indicator
#     component_size = len(nx.node_connected_component(g, start_node))
#     kcore_2 = nx.core_number(g)[start_node] >= 2
#     giant_component = start_node in max(nx.connected_components(g), key=len)
#
#     # Perform the random walk until the initial node is revisited
#     current_node = start_node
#     while True:
#         neighbors = list(g.neighbors(current_node))
#         if len(neighbors) == 0:
#             break
#         next_node = random.choice(neighbors)
#         if next_node == start_node:
#             break
#         visited_nodes.append(next_node)
#         current_node = next_node
#
#     # Calculate the walk length as the length of the visited nodes list
#     walk_length = len(visited_nodes)
#
#     # Calculate the number of distinct vertices visited
#     distinct_vertices_visited = len(set(visited_nodes))
#
#     # Return a dictionary of the desired outputs
#     return {
#         #    'visited_nodes': visited_nodes,
#         'walk_length': walk_length,
#         'in_giant_component': giant_component,
#         'component_size': component_size,
#         'kcore_2': kcore_2,
#         'distinct_vertices_visited': distinct_vertices_visited
#     }


# data = []
# samples = 2000
# N = range(100, 300, 10)
# connectivity = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Define the number of nodes
# for n in tqdm(N):
#     for c in tqdm(connectivity):
#         print(f'{n}-{c}')
#         for _ in range(samples):
#             # Generate a random graph with N nodes and probability 1/N for edge generation
#             # g = nx.erdos_renyi_graph(n, c / n)
#             g = nx.random_regular_graph(c, n)
#             r = random_walk(g)
#             r['N'] = n
#             r['c'] = c
#             data.append(r)
#
# pd.DataFrame(data).to_csv('rrg.csv', index=False)

# plot_random_graph(g, highlight=r['visited_nodes'])

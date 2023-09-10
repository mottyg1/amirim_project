import math
import random
from collections import Counter, defaultdict
import igraph as ig


# def plot_random_graph(g, node_size=70, cmap='Set1_r', algorithm='neato', highlight=[]):
#     # Compute the k-core decomposition of the graph
#     core_numbers = nx.core_number(g)
#
#     # Use the neato layout algorithm from Graphviz to calculate node positions
#     pos = nx.nx_agraph.graphviz_layout(g, prog=algorithm)
#
#     # Define the colormap and labels for the legend
#     cmap = plt.cm.get_cmap(cmap, max(core_numbers.values()) + 1)
#     labels = [f'K-core {i}' for i in range(max(core_numbers.values()) + 1)]
#
#     # Assign a color to each node based on its k-core
#     node_colors = [cmap(core_numbers[node]) for node in g.nodes()]
#     edge_colors = [cmap(core_numbers[node]) if node not in highlight else 'green' for node in g.nodes()]
#
#     # Draw the nodes and edges of the graph with the constant node size and colors
#     nx.draw_networkx_nodes(g, pos, node_size=node_size, node_color=node_colors, edgecolors=edge_colors, alpha=0.8)
#     nx.draw_networkx_edges(g, pos, edge_color='black')
#     nx.draw_networkx_labels(g, pos, font_size=7)
#
#     # Create the legend with discrete colors and labels
#     legend_elements = [(plt.Circle((0, 0), 0, color=cmap(i)), label) for i, label in enumerate(labels)]
#     plt.legend(*zip(*legend_elements), title='K-core number')
#
#     # Set the figure size
#     plt.gcf().set_size_inches(8, 8)
#
#     # Show the plot
#     plt.show()


def is_roundtrip(walk):  # the walk does not include the last vertex

    length = len(walk) - 1

    if length % 2 == 1:  # should be an even number of steps
        return False

    if walk.count(walk[0]) != 2:  # should not visit the start node until the end
        return False

    if len(set(walk)) < length/2:
        return False

    return walk == walk[::-1]


def is_retroceding(walk):
    if not walk:
        return False

    if walk.count(walk[0]) != 2:  # should not visit the start node until the end
        return False

    edge_counts = defaultdict(int)
    for i in range(len(walk) - 1):
        start_node, end_node = walk[i], walk[i + 1]
        edge = (start_node, end_node)
        reverse_edge = (end_node, start_node)
        edge_counts[edge] += 1
        edge_counts[reverse_edge] -= 1

    for count in edge_counts.values():
        if count != 0:
            if len(walk) == 3:
                print(walk, '\n')
            return False

    return True


def select_random_node_from_giant_component(graph):
    # Find the giant component
    components = graph.components(mode=ig.WEAK)
    giant_component = max(components, key=len)

    # Select a random node from the giant component
    random_node_index = random.randint(0, len(giant_component) - 1)
    random_node = giant_component[random_node_index]

    return random_node


def linearize_graph(g):
    component_sizes = [len(c) for c in g.components(mode="WEAK")]
    new_graph = ig.Graph(directed=False)

    # Compute the total number of vertices needed
    total_vertices = sum(component_sizes)

    # Add the vertices to the new graph
    new_graph.add_vertices(total_vertices)

    # Initialize the starting vertex index
    start_vertex = 0

    # Create disjoint linear chains based on component sizes
    for size in component_sizes:
        # Compute the ending vertex index for the current chain
        end_vertex = start_vertex + size - 1

        # Add edges between vertices to form a linear chain
        edges = [(i, i + 1) for i in range(start_vertex, end_vertex)]
        new_graph.add_edges(edges)

        # Update the start vertex for the next chain
        start_vertex = end_vertex +1
    return new_graph


def component_size_of_random_node(graph):
    node = random.randint(0, graph.vcount() - 1)
    component_size = len(graph.components(mode=ig.WEAK)[node])
    return component_size


def full_histogram(data):
    count = len(data)
    k = Counter()
    k.update(sorted(data))

    return k.keys(), [x / count for x in k.values()]


def catalan_number(n):
    return 1 / (n + 1) * math.comb(2 * n, n)


def in_2core(g, start_node):
    return g.coreness()[start_node] >= 2


def in_giant_component(g, node_index):
    # Get the connected components
    components = g.clusters()

    # Find the size of the largest component
    largest_component_size = max(components.sizes())

    # Get the component ID of the chosen node
    node_component_id = components.membership[node_index]

    # Check if the node is in the giant component
    is_in_giant_component = (components.sizes()[node_component_id] == largest_component_size)
    return is_in_giant_component


def random_walk(g, length, start_node=None):
    if start_node is None:
        start_node = random.randint(0, g.vcount() - 1)
        while not g.neighbors(start_node):
            start_node = random.randint(0, g.vcount() - 1)
    else:
        if not g.neighbors(start_node):
            raise ValueError('The start node has no neighbors')

    visited_nodes = [start_node]

    current_node = start_node

    for i in range(length):
        neighbors = g.neighbors(current_node)
        next_node = random.choice(neighbors)

        visited_nodes.append(next_node)
        current_node = next_node

    return visited_nodes


def random_walk_until_return(g, start_node=None, max_length=100000, exclude_isolated_nodes=False):
    if start_node is None:
        start_node = random.randint(0, g.vcount() - 1)

    if not g.neighbors(start_node):
        if exclude_isolated_nodes:
            while not g.neighbors(start_node):
                start_node = random.randint(0, g.vcount() - 1)
        else:
            return [start_node]

    visited_nodes = [start_node]

    current_node = start_node

    while True:
        neighbors = g.neighbors(current_node)
        next_node = random.choice(neighbors)

        visited_nodes.append(next_node)
        current_node = next_node

        if next_node == start_node:
            break
        if len(visited_nodes) > max_length:
            break

    return visited_nodes


def get_analytic_histogram(c, times, func):
    y = []
    for t in times:
        v = func(c, t)
        y.append(v)
    return y


def poisson_expectation(f, c, N=100):
    return sum([f(n) * (math.exp(-c) * c ** n / math.factorial(n)) for n in range(N)])


def walk_stats(g, walk, stats=['all']):
    if 'all' in stats:
        stats = ['walk_length', 'in_giant_component', 'started_in_2core', 'distinct_sites', 'is_roundtrip',
                 'is_retroceding', 'walk', 'start_node_degree', 'component_size', 'max_visits_for_node']

    d = {}
    if 'walk_length' in stats:
        d['walk_length'] = len(walk) - 1
    if 'in_giant_component' in stats:
        d['in_giant_component'] = in_giant_component(g, walk[0])
    if 'started_in_2core' in stats:
        d['started_in_2core'] = in_2core(g, walk[0])
    if 'distinct_sites' in stats:
        d['distinct_sites'] = len(set(walk))
    if 'is_roundtrip' in stats:
        d['is_roundtrip'] = is_roundtrip(walk)
    if 'is_retroceding' in stats:
        d['is_retroceding'] = is_retroceding(walk)
    if 'walk' in stats:
        d['walk'] = ','.join([str(x) for x in walk])
    if 'start_node_degree' in stats:
        d['start_node_degree'] = g.degree(walk[0])
    if 'component_size' in stats:
        d['component_size'] = g.clusters().sizes()[g.clusters().membership[walk[0]]]
    if 'max_visits_for_node' in stats:
        d['max_visits_for_node'] = max(Counter(walk).values())
    return d

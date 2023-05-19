from math import factorial
from collections import Counter
import networkx as nx
import numpy as np
from tqdm import tqdm

from utils import random_walk


def partition_number(n):
    def generate_partitions(current_partition, remaining):
        if remaining == 0:
            yield current_partition
            return

        start = 2 if not current_partition else current_partition[-1]
        for i in range(start, remaining + 1):
            if i > remaining - i:
                break
            yield from generate_partitions(current_partition + [i], remaining - i)

        yield current_partition + [remaining]

    # Generate partitions using the generator
    yield from generate_partitions([], n)


def count_permutations(numbers):
    counter = Counter(numbers)
    num_permutations = factorial(len(numbers))

    for count in counter.values():
        num_permutations //= factorial(count)

    return num_permutations


g = nx.erdos_renyi_graph(30, 2 / 30)
start_node = 0

sim_counter = Counter()

for _ in tqdm(range(10000)):
    sim_counter.update([len(random_walk(g, start_node))])

adjacency_matrix = nx.to_numpy_matrix(g)
m = adjacency_matrix / adjacency_matrix.sum(axis=1)
s = np.zeros(30)
s[start_node] = 1

p = {0: 0,
     1: 0}

for i in tqdm(range(2, 60)):
    bad = 0
    for partition in partition_number(i):
        if len(partition) == 1:
            continue
        num_permutations = count_permutations(partition)
        prod = 1
        for posi in partition:
            prod *= p[posi]
        bad += num_permutations * prod
    p[i] = (m**i)*s[start_node] - bad

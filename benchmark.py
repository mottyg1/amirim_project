import timeit
from itertools import zip_longest
import random

import numpy as np


def cumulative_distinct(walk):
    distinct_counts = []
    distinct_set = set()

    for item in walk:
        distinct_set.add(item)
        distinct_counts.append(len(distinct_set))

    return distinct_counts


def cumulative_distinct2(walk):
    distinct_counts = []
    distinct_set = set()
    add_to_set = distinct_set.add
    distinct_counts_append = distinct_counts.append

    for item in walk:
        add_to_set(item)
        distinct_counts_append(len(distinct_set))
    return distinct_counts


for i in range(10000):
    ls = np.random.randint(1, 1000, 5000)
    cumulative_distinct2(ls)
    cumulative_distinct(ls)

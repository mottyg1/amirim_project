from collections import Counter


def cumulative_distinct(walk):
    distinct_counts = []
    distinct_set = set()

    for item in walk:
        distinct_set.add(item)
        distinct_counts.append(len(distinct_set))

    return distinct_counts


def avg(ls):
    return sum(ls) / len(ls)


def transpose_lists(lists):
    transpose = []
    i = 0
    while True:
        col = []
        for row in lists:
            if i < len(row):
                col.append(row[i])
        if not col:
            return transpose
        else:
            transpose.append(col)
            i += 1


def get_neighboring_pairs(lst):
    return [(lst[i], lst[i + 1]) for i in range(len(lst) - 1)]


def list_diff(ls):
    ls = [0] + ls
    return [ls[i] - ls[i - 1] for i in range(1, len(ls))]


class RandomWalksTracker:
    def __init__(self, base_dict={}):
        self.base_dict = base_dict
        self.walks = []
        self.cum_distinct = []

    def update(self, walk):
        self.walks.append(walk)
        self.cum_distinct.append(cumulative_distinct(walk))

    def stats_by_time(self):

        mean_distinct_nodes = [avg(t) for t in transpose_lists(self.cum_distinct)]
        prob_new_node = [avg(t) for t in transpose_lists([list_diff(x) for x in self.cum_distinct])]

        return [{'time': i + 1, 'mean_distinct_nodes': v[0], 'new_node_probability': v[1]} | self.base_dict for
                i, v in
                enumerate(zip(mean_distinct_nodes, prob_new_node))]

    def stats_by_distinct_nodes(self):
        c = Counter()
        for walk in self.cum_distinct:
            c.update(get_neighboring_pairs(walk))

        max_sites = max(max(key) for key in c.keys())

        probs = []

        for i in range(1, max_sites):
            probs.append({
                             "new_node_probability": c[(i, i + 1)] / (c[(i, i)] + c[(i, i + 1)]),
                             "distinct_visited": i
                         } | self.base_dict)
        return probs

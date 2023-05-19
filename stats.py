import networkx as nx
import numpy as np
from tqdm import trange, tqdm

from RandomWalksTracker import RandomWalksTracker
from utils import random_walk, walk_stats
import pandas as pd
from datetime import datetime


def run_simulation(samples=5000, n=1000, connectivity=range(1, 21), graph_type="er"):
    walk_data = []
    time_stats = []
    distinct_sites_stats = []

    for c in tqdm(connectivity, ncols=100):
        tracker = RandomWalksTracker({'c': c})

        for _ in trange(samples, ncols=100):
            if graph_type == "er":
                g = nx.erdos_renyi_graph(n, c / n)
            else:  # rrg
                g = nx.random_regular_graph(c, n)

            walk = random_walk(g)

            stats = walk_stats(g, walk) | {'c': c}
            walk_data.append(stats)
            tracker.update(walk)

        time_stats += tracker.stats_by_time()
        distinct_sites_stats += tracker.stats_by_distinct_nodes()

    pd.DataFrame(walk_data).to_csv(
        f'./data/{datetime.now().strftime("%Y-%m-%d-%H")}_{graph_type}_walkData_n{n}_s{samples}.csv', index=True)
    pd.DataFrame(time_stats).to_csv(
        f'./data/{datetime.now().strftime("%Y-%m-%d-%H")}_{graph_type}_timeStats_n{n}_s{samples}.csv', index=True)
    pd.DataFrame(distinct_sites_stats).to_csv(
        f'./data/{datetime.now().strftime("%Y-%m-%d-%H")}_{graph_type}_distinctSitesStats_n{n}_s{samples}.csv',
        index=True)


run_simulation(samples=500, n=200, connectivity=np.linspace(0.95, 2, 50), graph_type="er")

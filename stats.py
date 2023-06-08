import igraph as ig
import numpy as np
from tqdm import trange, tqdm

from RandomWalksTracker import RandomWalksTracker
from utils import random_walk_until_return, walk_stats
import pandas as pd
from datetime import datetime


def run_simulation(samples=5000, n=1000, connectivity=range(1, 21), graph_type="er", stats_to_calculate=['all'],
                   max_length=100000, file_name='simulation_data.h5'):
    time_stats = []
    distinct_sites_stats = []

    for c in tqdm(connectivity, ncols=100):
        # tracker = RandomWalksTracker({'c': c})
        walk_data = []

        for _ in trange(samples, ncols=100):
            if graph_type == "er":
                g = ig.Graph.Erdos_Renyi(n, c / n)
            else:  # rrg
                g = ig.Graph.K_Regular(n, c)

            walk = random_walk_until_return(g, max_length=max_length, exclude_isolated_nodes=True)

            stats = walk_stats(g, walk, stats_to_calculate) | {'c': c}
            walk_data.append(stats)
            # tracker.update(walk)

        pd.DataFrame(walk_data).to_hdf('./data/' + file_name, "table", append=True)
        # time_stats += tracker.stats_by_time()
        # distinct_sites_stats += tracker.stats_by_distinct_nodes()

    # pd.DataFrame(walk_data).to_csv(
    #     f'./data/{datetime.now().strftime("%Y-%m-%d-%H")}_{graph_type}_walkData_n{n}_s{samples}.csv', index=False)
    # pd.DataFrame(time_stats).to_csv(
    #     f'./data/{datetime.now().strftime("%Y-%m-%d-%H")}_{graph_type}_timeStats_n{n}_s{samples}.csv', index=False)
    # pd.DataFrame(distinct_sites_stats).to_csv(
    #     f'./data/{datetime.now().strftime("%Y-%m-%d-%H")}_{graph_type}_distinctSitesStats_n{n}_s{samples}.csv',
    #     index=False)


run_simulation(samples=200000, n=1000, connectivity=np.arange(0.1, 4, 0.1), graph_type="er",
               stats_to_calculate=['is_retroceding', 'walk_length', 'distinct_sites', 'start_node_degree',
                                   'component_size'],
               file_name='walks_0-4_s200000.h5')

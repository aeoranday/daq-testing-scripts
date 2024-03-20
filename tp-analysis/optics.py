"""
Generate the OPTICS
reachability plot.
"""


from trgtools import TPReader

import click
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import OPTICS


@click.command()
@click.argument("file")
def main(file):
    data = TPReader(file)
    data.read_fragment(data.get_fragment_paths()[0])
    channels = data.tp_data['channel'].astype(int)
    times = data.tp_data['time_start'].astype(int)
    times = (times - np.min(times)) // 32

    positions = np.array([channels, times]).T
    positions = positions[:10000]

    optics = OPTICS(min_samples=10, xi=0.05, metric='manhattan', cluster_method='xi', min_cluster_size=5)

    optics.fit(positions)

    ordering = optics.ordering_
    labels = optics.labels_[ordering]
    print("Number of labels:", np.max(labels))
    reachability = optics.reachability_[ordering]
    core_distances = optics.core_distances_[ordering]
    space = np.arange(len(positions))

    plt.figure(figsize=(8, 6), dpi=200)
    for label in np.arange(0, np.max(labels)+1):
        xk = space[labels == label]
        rk = reachability[labels == label]
        plt.plot(xk, rk, ".", alpha=0.2)

    plt.plot(space[labels == -1], reachability[labels == -1], 'k.', alpha=0.3)

    plt.title("Reachability Plot: k=5 & eps=200")
    plt.xlabel("TP Ordering")
    plt.ylabel("Distance")
    plt.savefig("optics-reachability.png")
    plt.close()

    plt.figure(figsize=(8, 6), dpi=200)
    for label in np.arange(0, np.max(labels)+1):
        xk = positions[labels == label]
        plt.plot(xk[:,1], xk[:,0], '.', alpha=0.3)

    plt.title("Clustering")
    plt.xlabel("Time")
    plt.ylabel("Channel")
    plt.savefig("optics-clusters.png")
    plt.close()


if __name__ == "__main__":
    main()

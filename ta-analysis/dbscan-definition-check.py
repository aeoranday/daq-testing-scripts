"""
Check that the TAs produced for a given
run fit the definition of DBSCAN.

Requires knowledge of eps and min_pts for
that run.
"""


from trgtools import TAReader

import click
import numpy as np


def dist(hit0, hit1):
    return np.sum(np.power(hit0 - hit1, 2))


def check_dbscan(tps: np.ndarray, eps: int, min_pts: int) -> bool:
    """
    Check that the set of TPs is DBSCAN compliant.
    """
    tp_label = np.zeros(len(tps))
    cluster_label = np.zeros(len(tps))
    neighbor_count = np.zeros(len(tps))

    time = (tps['time_start'].astype(int) - np.min(tps['time_start'])) / 100
    channel = tps['channel']
    hits = np.array([time, channel]).T
    sq_eps = eps**2

    for idx, hit0 in enumerate(hits):
        for jdx, hit1 in enumerate(hits[idx:]):
            if dist(hit0, hit1) <= sq_eps:
                neighbor_count[idx] += 1
                neighbor_count[jdx+idx] += 1
    #print(neighbor_count)

    for idx, count in enumerate(neighbor_count):
        if count >= min_pts:
            tp_label[idx] = 1

    for idx, label0 in enumerate(tp_label):
        if label0 == 1:  # Skip core points
            continue
        hit0 = hits[idx]
        compliant = False  # Assume that it is not compliant
        for label1, hit1 in zip(tp_label, hits):
            if np.all(hit0 == hit1):
                continue
            if dist(hit0, hit1) <= sq_eps and label1 == 1:
                compliant = True  # Found that it is in the neighborhood of a core point
                break
        if not compliant:  # TP was not in the neighborhood of a core point
            print(neighbor_count)
            return False

    return True


@click.command()
@click.argument("file")
@click.option("--eps", type=click.INT)
@click.option("--min-pts", type=click.INT)
@click.option("--num-fragments", type=click.INT, default=1)
@click.option("--num-tas", type=click.INT, default=10)
def main(file, eps, min_pts, num_fragments, num_tas):
    data = TAReader(file)
    data._fragment_paths = data.get_fragment_paths()[:num_fragments]
    data.read_all_fragments()

    bad_count = 0
    for idx, tps in enumerate(data.tp_data):
        #print("="*60)
        if not check_dbscan(tps, eps, min_pts):
            print("Not DBSCAN compliant.")
            print(f"Found at {idx}.")
            bad_count += 1

    print("Total # of Noncompliant TAs:", bad_count)
    return


if __name__ == "__main__":
    main()

"""
Compare the contents of readout
and trigger in TP fragments per
TriggerRecord.

Ideally, both are the same, I think.
"""

from trgtools import TPReader

import click
import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict
import re


def get_unique_tps(links: dict[list[np.ndarray]]) -> list[np.ndarray]:
    """
    Get the unique TPs per TriggerRecord.

    Parameter:
        links (dict[list[np.ndarray]]):
            Dictionary with keys of the link and values
            of a list per fragment and its contents.

    Returns a list of the unique TPs for each fragment.
    """
    unique_tps = []

    num_records = len(list(links.values())[0])
    # All links _should_ have the same number of TriggerRecords.
    for idx in range(num_records):
        tps = [link[idx] for link in links.values()]
        unique_tps.append(np.unique(tps))
    return unique_tps


def plot_png_total_link_counts(links: dict[list[np.ndarray]], file_id: str) -> None:
    """
    Plot the total TP count in each of the TP links.
    Each link is likely to have some duplication of TPs.

    Parameters:
        links (dict[list[np.ndarray]]):
            Dictionary with keys of the link and values
            of a list per fragment and its contents.
        file_id (str):
            String of the file that produced `links`.

    Returns nothing. Saves a PNG of the associated plot.
    """
    plt.figure(figsize=(6, 4), dpi=200)

    unique_tps = get_unique_tps(links)
    unique_count = [len(tps) for tps in unique_tps]
    plt.plot(unique_count, '-ok', ms=3, alpha=0.4, label=f"Unique TPs: {np.sum(unique_count)} TPs")

    for link_id, fragments in links.items():
        tp_count = [len(fragment) for fragment in fragments]
        plt.plot(tp_count, '-o', ms=3, alpha=0.4, label=f"Link {link_id}: {np.sum(tp_count)} TPs")

    num_links = len(links.keys())
    plt.title("TriggerPrimitive Links:\nTP Count per Link")
    plt.xlabel(f"TriggerRecord ({num_links} Links per TR)")
    plt.ylabel("TP Count")
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"link_total_tp_count-{file_id}.png")
    plt.close()
    return


@click.command()
@click.argument("file")
def main(file):
    tp_data = TPReader(file)
    file_id = f"{tp_data.run_id}.{tp_data.file_index:04}"

    links = defaultdict(list)
    link_regex = re.compile('(\dx\d+)')
    for path in tp_data.get_fragment_paths():
        if "Trigger_Primitive" in path:
            _ = tp_data.read_fragment(path)
            link_idx = int(link_regex.search(path).group(), 0)
            links[link_idx].append(tp_data.tp_data)
            tp_data.clear_data()

    plot_png_total_link_counts(links, file_id)
    return


if __name__ == "__main__":
    main()

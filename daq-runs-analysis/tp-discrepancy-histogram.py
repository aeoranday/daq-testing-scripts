"""
Find the TPs that are discrepant then
make a count for which data member is
discrepant.
"""

import trgtools

import click
import matplotlib.pyplot as plt
import numpy as np

from collections import defaultdict


DATA_MEMBERS = [
                #"algorithm",
                "adc_integral",
                "adc_peak",
                "channel",
                #"detid",
                "time_over_threshold",
                "time_peak",
                #"type",
                #"version"
                #"time_start",  # EXPLICIT: Not including as this will be our static dof
               ]

def plot_png_histogram(data: list[int], data_id: tuple[str, str]) -> None:
    """
    Write a PNG histogram of the given data.

    Parameters:
        data (list[int]): Array of the data to plot.
        data_id (tuple[str, str]): Identifier for title and save name.

    Returns nothing. Write a PNG to the CWD.
    """
    plt.figure(figsize=(6, 4), dpi=200)

    plt.hist(data, bins=10, color='k')

    plt.title(f"Discrepancy Histogram {data_id[0]}")
    plt.xlabel("# of Discrepants / # of TAPs")
    plt.ylabel("Count")

    plt.xlim((-0.1, 1.1))

    plt.tight_layout()
    plt.savefig(f"{data_id[1]}_discrepants_hist.png")
    plt.close()
    return


def plot_png_overlap_histogram(data: dict[list[int]], file_id: str, readout=False) -> None:
    """
    Write a PNG histogram of the given data.

    Parameters:
        data (dict[list[int]]): Dictionary of the data to plot.
        file_id (str): File identifier.
        readout (bool): Is the plot from readout?

    Returns nothing. Write a PNG to the CWD.
    """
    plt.figure(figsize=(6, 4), dpi=200)

    for data_member in DATA_MEMBERS:
        plt.hist(data[data_member], bins=10, alpha=0.2, label=data_member)

    prefix = "Trigger"
    if readout:
        prefix = "Readout"
    plt.title(f"{prefix} Discrepancy Histogram\n{file_id}")
    plt.xlabel("# of Discrepants / # of TAPs")
    plt.ylabel("Count")
    plt.legend()

    plt.xlim((-0.1, 1.1))

    plt.tight_layout()
    plt.savefig(f"{prefix}_overlap_discrepants_hist_{file_id}.png")
    plt.close()
    return


def get_discrepant_count(tps: np.ndarray, taps: np.ndarray, data_members: list[str]) -> int:
    """
    Get the number of discrepant TPs using the given data member.

    Parameters:
        tps (np.ndarray): TPs from a TP fragment.
        taps (np.ndarray): TPs from a TA fragment.
        data_member (list[str]): Data members to use for discrepancy finding.

    Returns the count of TAPs not found in TPs.
    """
    return len(np.setdiff1d(taps[data_members], tps[data_members]))


@click.command()
@click.argument("file")
@click.option("--num", '-n', type=click.INT, default=1)
@click.option("--all-frags", '-a', default=False, is_flag=True)
@click.option("--readout", '-r', default=False, is_flag=True)
def main(file, num, all_frags, readout):
    tp_data = trgtools.TPReader(file)
    ta_data = trgtools.TAReader(file)

    file_id = f"{tp_data.run_id}.{tp_data.file_index:04}"

    # ASSUMPTION: There is only 1 readout unit, so only need to offset the
    # trigger and readout fragments by 1.
    tp_idx = 1
    ta_idx = 0
    if readout:
        tp_idx = 0

    tp_paths = tp_data.get_fragment_paths()
    ta_paths = ta_data.get_fragment_paths()
    if all_frags:
        num = len(ta_paths)

    discrepants = defaultdict(list)
    for _ in range(num):
        tps = tp_data.read_fragment(tp_paths[tp_idx])
        _ = ta_data.read_fragment(ta_paths[ta_idx])

        tp_idx += 2
        ta_idx += 1

        for taps in ta_data.tp_data:
            num_taps = len(taps)
            for data_member in DATA_MEMBERS:
                count = get_discrepant_count(tps, taps, ['time_start', data_member])
                discrepants[data_member].append(count / num_taps)
        tp_data.clear_data()
        ta_data.clear_data()

    for data_member in DATA_MEMBERS:
        data_id = (f"{data_member}\n{file_id}", f"{data_member}_{file_id}")
        plot_png_histogram(discrepants[data_member], data_id)

    plot_png_overlap_histogram(discrepants, file_id, readout)

    return


if __name__ == "__main__":
    main()

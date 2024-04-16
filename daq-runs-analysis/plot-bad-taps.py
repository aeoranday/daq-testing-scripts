"""
Find the bad TAPs and highlight them
in an event display plot.
"""

import trgtools

import click
import matplotlib.pyplot as plt
import numpy as np

import re


def plot_taps(good_taps: np.ndarray, bad_taps: np.ndarray, file_id, record_id) -> None:
    """
    Plot the TAPs event display with bad TAPs highlighted.

    Parameters:
        good_taps (np.ndarray): Good TAPs in the event.
        bad_taps (np.ndarray) : Bad TAPs in the event.
        file_id (str)   : File identifier.
        record_id (str) : Record identifier.

    Returns nothing. Saves to a PNG.
    """

    if len(good_taps) == 0:
        min_time = np.min(bad_taps['time_start'])
    elif len(bad_taps) == 0:
        min_time = np.min(good_taps['time_start'])
    else:
        min_time = np.min((np.min(bad_taps['time_start']), np.min(good_taps['time_start'])))
    plt.figure(figsize=(6, 4), dpi=200)

    plt.plot(good_taps['time_start'] - min_time, good_taps['channel'], 'sk', ms=3, label="Good TAPs")
    plt.plot(bad_taps['time_start'] - min_time, bad_taps['channel'], 'xr', ms=3, label="Bad TAPs")

    plt.title(f"TAPs Display\n{file_id} : TriggerRecord {record_id}")
    plt.xlabel("Time (16 ns / Tick)")
    plt.ylabel("Channel")
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"taps_display_{file_id}-{record_id}.png")
    plt.close()

    return


@click.command()
@click.argument("file")
@click.option("--frag", '-f', type=click.INT, default=0)
def main(file, frag):
    ta_data = trgtools.TAReader(file)
    tp_data = trgtools.TPReader(file)

    file_id = f"{ta_data.run_id}.{ta_data.file_index}"

    path = ta_data.get_fragment_paths()[frag]
    _ = ta_data.read_fragment(path)
    tps = tp_data.read_fragment(tp_data.get_fragment_paths()[frag//2 + 1])

    record_regex = re.compile('(\d+\.)')
    record_id = record_regex.search(path).group()
    for idx, taps in enumerate(ta_data.tp_data):
        bad_taps = np.setdiff1d(taps, tps)
        good_taps = np.setdiff1d(taps, bad_taps)
        plot_taps(good_taps, bad_taps, file_id, record_id+f"{idx}")

    return


if __name__ == "__main__":
    main()

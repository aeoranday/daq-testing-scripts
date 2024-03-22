"""
Check that the time windows created
by the TP and TA fragments are consistent.

I'll check by doing the Delta t for each,
comparing the size, and comparing if they
have the same start TP.

I'll also count the number of TPs that are
contained in these windows.
"""

import trgtools

import click
import matplotlib.pyplot as plt
import numpy as np


def plot_png_time_windows(tp_window: np.ndarray, ta_window: np.ndarray) -> None:
    """
    Plot the width of the time windows and their differences.
    """
    # Individual window widths
    plt.figure(figsize=(6, 4), dpi=200)

    plt.plot(tp_window, '-o', ms=3, color="#63ACBE", label="TP Fragments", alpha=0.4)
    plt.plot(ta_window, '-o', ms=3, color="#EE442F", label="TA Fragments", alpha=0.4)

    plt.title("TP & TA Fragment:\nTime Window Widths")
    plt.xlabel("TriggerRecord (1 TP & TA Fragment per TR)")
    plt.ylabel("Time Window Width (16 ns / Tick)")
    plt.legend()

    plt.tight_layout()
    plt.savefig("time_windows.png")
    plt.close()

    # Difference in widths
    plt.figure(figsize=(6, 4), dpi=200)

    plt.plot(ta_window - tp_window, 'ok', ms=2, label="Difference: TA - TP", alpha=0.4)

    plt.title("TP & TA Fragment Difference:\nTime Window Widths")
    plt.xlabel("TriggerRecord (1 TP & TA Fragment per TR)")
    plt.ylabel("Time Window Width Difference (16 ns / Tick)")
    plt.legend()

    plt.tight_layout()
    plt.savefig("time_window_differences.png")
    plt.close()
    return None


@click.command()
@click.argument("file")
def main(file):
    tp_data = trgtools.TPReader(file)
    ta_data = trgtools.TAReader(file)

    tp_window_width = []            # Time window width for TP fragments.
    ta_window_width = []            # Time window width for TA fragments.
    ta_tp_start_difference = []     # Difference in TA-TP first TP start_time.
    tp_window_tp_count = []         # Number of TPs in TP window.
    ta_window_tp_count = []         # Number of TPs in TA window.
    for tp_path, ta_path in zip(tp_data.get_fragment_paths(), ta_data.get_fragment_paths()):
        tps = tp_data.read_fragment(tp_path)
        _ = ta_data.read_fragment(ta_path)

        tp_window_tp_count.append(len(tps))
        ta_window_tp_count.append(np.sum(ta_data.ta_data['num_tps']))

        tp_window_width.append(tps['time_start'][-1] - tps['time_start'][0])
        # There may be more than one TA in the fragment.
        # Assume that the first TA is earliest in time and the last TA is latest in time.
        ta_window_width.append(ta_data.tp_data[-1]['time_start'][-1].astype(int) - ta_data.tp_data[0]['time_start'][0].astype(int))

        ta_tp_start_difference.append(ta_data.tp_data[0]['time_start'][0].astype(int) - tps['time_start'][0].astype(int))

        # Prepare for the next fragment.
        tp_data.clear_data()
        ta_data.clear_data()

    print("Min Time Start Difference:", np.min(ta_tp_start_difference))
    print("Max Time Start Difference:", np.max(ta_tp_start_difference))

    plot_png_time_windows(np.array(tp_window_width), np.array(ta_window_width))
    return


if __name__ == "__main__":
    main()

"""
Check that the TP Fragments and TA Fragments
both contain the same number of TPs.

Maybe check later that they are actually
the same TPs.
"""

import trgtools

import click
import matplotlib.pyplot as plt
import numpy as np


def plot_tp_fragment_counts(tp_fragment_counts: np.ndarray, ta_fragment_counts: np.ndarray):
    """
    Plot the count of TPs in each fragment.
    """
    print("Max TP Difference:", np.max(ta_fragment_counts - tp_fragment_counts))
    print("Min TP Difference:", np.min(ta_fragment_counts - tp_fragment_counts))
    plt.figure(figsize=(6, 4), dpi=200)

    plt.plot(ta_fragment_counts - tp_fragment_counts, 'o', markersize=2, color="k", label="Difference: TA - TP")

    plt.title("Replay TP & TA Fragments Difference\n Number of TPs Per Fragments")
    plt.xlabel("TriggerRecord (1 TP & 1 TA Fragment per TR)")
    plt.ylabel("Number of TPs")

    plt.legend()

    plt.tight_layout()
    plt.savefig("fragment_counts_diff.png")
    plt.close()

    plt.figure(figsize=(6, 4), dpi=200)

    plt.plot(tp_fragment_counts, '-o', color="#63ACBE", label="TP Fragments")
    plt.plot(ta_fragment_counts, '-o', color="#EE442F", label="TA Fragments")

    plt.title("Replay TP & TA Fragments\n Number of TPs Per Fragments")
    plt.xlabel("TriggerRecord (1 TP & 1 TA Fragment per TR)")
    plt.ylabel("Number of TPs")

    plt.legend()

    plt.tight_layout()
    plt.savefig("fragment_tp_counts.png")
    plt.close()
    return


def plot_ta_fragment_counts(ta_fragment_counts: np.ndarray, tc_fragment_counts: np.ndarray):
    """
    Plot the count of TAs in each fragment.
    """
    plt.figure(figsize=(6, 4), dpi=200)

    plt.plot(ta_fragment_counts, '-o', color="#EE442F", label="TA Fragments")
    plt.plot(tc_fragment_counts, '-o', color="#3BB27A", label="TC Fragments")

    plt.title("Replay TA & TC Fragments\n Number of TAs Per Fragment")
    plt.xlabel("TriggerRecord (1 TA & 1 TC Fragment per TR)")
    plt.ylabel("Number of TAs")

    plt.legend()

    plt.tight_layout()
    plt.savefig("fragment_ta_counts.png")
    plt.close()
    return


@click.command()
@click.argument("file")
def main(file):
    tp_data = trgtools.TPReader(file)
    ta_data = trgtools.TAReader(file)
    tc_data = trgtools.TCReader(file)

    tp_paths = tp_data.get_fragment_paths()
    ta_paths = ta_data.get_fragment_paths()
    tc_paths = tc_data.get_fragment_paths()

    tp_fragment_counts = []  # Number of TPs in TP fragments
    ta_fragment_counts = []  # Number of TPs in TA fragments
    ta_ta_counts = []        # Number of TAs in TA fragments (lazy naming)
    tc_fragment_counts = []  # Number of TAs in TC fragments
    for tp_path, ta_path, tc_path in zip(tp_paths, ta_paths, tc_paths):
        # Collect fragment contents
        tp_datum = tp_data.read_fragment(tp_path)
        _ = ta_data.read_fragment(ta_path)
        _ = tc_data.read_fragment(tc_path)

        # Calculate counts
        tp_fragment_counts.append(len(tp_datum))
        ta_fragment_counts.append(np.sum(ta_data.ta_data['num_tps']))
        ta_ta_counts.append(len(ta_data.ta_data))
        tc_fragment_counts.append(np.sum(tc_data.tc_data['num_tas']))

        # Reset for next fragment
        tp_data.clear_data()
        ta_data.clear_data()
        tc_data.clear_data()

    # Plot the TP-TA relations
    plot_tp_fragment_counts(np.array(tp_fragment_counts), np.array(ta_fragment_counts))

    # Plot the TA-TC relations
    plot_ta_fragment_counts(np.array(ta_ta_counts), np.array(tc_fragment_counts))
    return


if __name__ == "__main__":
    main()

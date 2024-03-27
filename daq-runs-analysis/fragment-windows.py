"""
Check that the fragment windows for TPs and TAs
are consistent. Both should have the same
start and end point.
"""


import trgtools

import daqdataformats

import click
import matplotlib.pyplot as plt
import numpy as np


def plot_png_fragment_window_difference(tp_windows: np.ndarray, ta_windows: np.ndarray) -> None:
    plt.figure(figsize=(6, 4), dpi=200)
    plt.plot(ta_windows[:, 0] - tp_windows[:, 0], 'ok', ms=3, label="TA - TP Window Begin")

    plt.title("Fragment Window Begin Difference\nTA - TP")
    plt.xlabel("TriggerRecord (1 TP & 1 TA Fragment per TR)")
    plt.ylabel("Window Begin Difference (16 ns / Tick)")
    plt.legend()

    plt.tight_layout()
    plt.savefig("fragment_window_begin_difference.png")
    plt.close()

    plt.figure(figsize=(6, 4), dpi=200)
    plt.plot(ta_windows[:, 1] - tp_windows[:, 1], 'ok', ms=3, label="TA - TP Window End")

    plt.title("Fragment Window End Difference\nTA - TP")
    plt.xlabel("TriggerRecord (1 TP & 1 TA Fragment per TR)")
    plt.ylabel("Window End Difference (16 ns / Tick)")
    plt.legend()

    plt.tight_layout()
    plt.savefig("fragment_window_end_difference.png")
    plt.close()
    return


def plot_png_fragment_window_width(tp_windows: np.ndarray, ta_windows: np.ndarray) -> None:
    plt.figure(figsize=(6, 4), dpi=200)
    plt.plot(tp_windows[:, 1] - tp_windows[:, 0], '-o', color="#63ACBE", ms=3, label="TP Fragments", alpha=0.5)
    plt.plot(ta_windows[:, 1] - ta_windows[:, 0], '-o', color="#EE442F", ms=3, label="TA Fragments", alpha=0.5)

    plt.title("Fragment Window Widths")
    plt.xlabel("TriggerRecord (1 TP & 1 TA Fragment per TR)")
    plt.ylabel("Window Width (16 ns / Tick)")
    plt.legend()

    plt.tight_layout()
    plt.savefig("fragment_window_widths.png")
    plt.close()
    return


@click.command()
@click.argument("file")
def main(file):
    tp_data = trgtools.TPReader(file)
    ta_data = trgtools.TAReader(file)

    tp_windows = []
    for path in tp_data.get_fragment_paths():
        tp_frag = tp_data._h5_file.get_frag(path)
        window_begin = tp_frag.get_window_begin()
        window_end = tp_frag.get_window_end()
        tp_windows.append((window_begin, window_end))

    ta_windows = []
    for path in ta_data.get_fragment_paths():
        ta_frag = ta_data._h5_file.get_frag(path)
        window_begin = ta_frag.get_window_begin()
        window_end = ta_frag.get_window_end()
        ta_windows.append((window_begin, window_end))

    tp_windows = np.array(tp_windows)
    ta_windows = np.array(ta_windows)
    plot_png_fragment_window_difference(tp_windows, ta_windows)
    plot_png_fragment_window_width(tp_windows, ta_windows)
    return


if __name__ == "__main__":
    main()

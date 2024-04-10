"""
Calculate the average TP rate for a few fragments.
"""

from trgtools import TPReader

import click
import numpy as np
import matplotlib.pyplot as plt


def plot_png_tp_rates(num_tps: list[int]) -> None:
    """
    Plot the number of TPs per TimeSlice.
    By definition, this is the TP rate in Hz.

    Argument:
        num_tps (list[int]): A list per TimeSlice of the number of TPs.

    Returns nothing.
    """
    plt.figure(figsize=(6, 4), dpi=200)
    plt.plot(num_tps, '-ok', ms=3, label=f"Average Rate: {np.mean(num_tps):.3f} Hz")

    plt.title("TriggerPrimitive Rate")
    plt.xlabel("TimeSlice (1s)")
    plt.ylabel("TP Rate (Hz)")
    plt.legend()

    plt.savefig("tp_rate.png")
    plt.close()


@click.command()
@click.argument("file")
@click.option("--offset", '-o', default=10, type=click.INT)
@click.option("--num", '-n', default=10, type=click.INT)
def main(file, offset, num):
    data = TPReader(file)
    num_tps = []
    for path in data.get_fragment_paths()[offset:offset+num]:
        tps = data.read_fragment(path)
        num_tps.append(len(tps))

    plot_png_tp_rates(num_tps)
    return


if __name__ == "__main__":
    main()

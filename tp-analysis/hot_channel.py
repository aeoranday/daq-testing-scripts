"""
Find the channels that are above a certain limit.
"""

from trgtools import TPReader
from trgtools.plot import PDFPlotter

import click
import numpy as np
import matplotlib.pyplot as plt


@click.command()
@click.argument("file")
@click.option("--limit", type=click.INT, default=10000)
@click.option("--fragment", '-f', type=click.INT, default=10)
def main(file, limit, fragment):
    data = TPReader(file)
    tps = data.read_fragment(data.get_fragment_paths()[fragment])
    plotter = PDFPlotter(f"hot_channels_{data.run_id}.{data.file_index}.pdf")
    hist_style = dict(
            title="Noisy Channels",
            xlabel="Channel",
            ylabel="TP Count",
            linear=True,
            linear_style=dict(color='#63ACBE', alpha=0.6, label='Linear'),
            log=True,
            log_style=dict(color='#EE442F', alpha=0.6, label='Log'),
            bins=np.arange(0, 3072)
    )

    plotter.plot_histogram(tps['channel'], hist_style)
    hist, _ = np.histogram(tps['channel'], bins=np.arange(0, 3072))
    print(f"Total Number of TPs: {len(tps)}.")
    print(f"Above Limit = {limit} Channels:", np.where(hist > limit)[0])
    return


if __name__ == "__main__":
    main()

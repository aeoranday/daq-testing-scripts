"""
Plot the positions of TP-TPs and TA-TPs
according to their time and channel.
"""

import trgtools

import click
import numpy as np
import matplotlib.pyplot as plt


def plot_channel_time(taps: np.ndarray, tps: np.ndarray, file_id: str) -> None:
    """
    Plot the location of TPs in the TA fragment and
    TP fragment.

    Arguments:
        taps (np.ndarray): TPs in the TA fragment.
        tps (np.ndarray): TPs in the TP fragment.

    Returns nothing. Plots the channel-time location of TPs.
    """
    min_time_start = np.min([np.min(taps['time_start']), np.min(tps['time_start'])])
    taps_times = taps['time_start'] - min_time_start
    tps_times = tps['time_start'] - min_time_start

    taps_channels = taps['channel']
    tps_channels = tps['channel']

    plt.figure(figsize=(6, 4), dpi=200)

    plt.plot(taps_times, taps_channels, 's', ms=3, color="#EE442F", label="TAP")
    plt.plot(tps_times, tps_channels, 'x', ms=3, color="#63ACBE", label="TP")

    plt.title("TA vs TP Fragment TPs")
    plt.xlabel("Relative Time Start (16 ns / Tick)")
    plt.ylabel("Channel")
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"tps-taps_channel-time_{file_id}.png")
    plt.close()
    return


def plot_adc_peak_time(taps: np.ndarray, tps: np.ndarray, file_id: str) -> None:
    """
    Plot the location of TPs in the TA fragment and
    TP fragment.

    Arguments:
        taps (np.ndarray): TPs in the TA fragment.
        tps (np.ndarray): TPs in the TP fragment.

    Returns nothing. Plots the peak-time location of TPs.
    """
    min_time_start = np.min([np.min(taps['time_start']), np.min(tps['time_start'])])
    taps_times = taps['time_start'] - min_time_start
    tps_times = tps['time_start'] - min_time_start

    taps_channels = taps['adc_peak']
    tps_channels = tps['adc_peak']

    plt.figure(figsize=(6, 4), dpi=200)

    plt.plot(taps_times, taps_channels, 's', ms=3, color="#EE442F", label="TAP")
    plt.plot(tps_times, tps_channels, 'x', ms=3, color="#63ACBE", label="TP")

    plt.title("TA vs TP Fragment TPs")
    plt.xlabel("Relative Time Start (16 ns / Tick)")
    plt.ylabel("ADC Peak")
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"tps-taps_peak-time_{file_id}.png")
    plt.close()
    return


@click.command()
@click.argument("file")
def main(file):
    tp_data = trgtools.TPReader(file)
    ta_data = trgtools.TAReader(file)
    file_id = f"{tp_data.run_id}.{tp_data.file_index}"

    ta_index = -1
    tp_index = -1
    while True:
        ta_index += 1
        tp_index += 2
        tp_data.clear_data()
        ta_data.clear_data()

        _ = ta_data.read_fragment(ta_data.get_fragment_paths()[ta_index])
        if len(ta_data.ta_data) == 0:
            print("Empty fragment. Skipping.")
            continue
        tps = tp_data.read_fragment(tp_data.get_fragment_paths()[tp_index])
        taps = ta_data.tp_data[0]

        print(f"TP Fragment has {len(tps)} TPs.")
        print(f"TA Fragment has {len(taps)} TPs.")
        print(f"TA Fragment has {len(ta_data.tp_data)} TAs.")
        prompt = input("Plot? [y/n/q]: ")
        if prompt.lower() == 'y':
            plot_channel_time(taps, tps, file_id)
            plot_adc_peak_time(taps, tps, file_id)
            return
        if prompt.lower() == 'q':
            return

    return


if __name__ == "__main__":
    main()

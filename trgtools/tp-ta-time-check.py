"""
Check that the times set for the TA
truly represent the times of the TPs
it contains.

This test was motivated by the problems later
identified by duplication.py. This one didn't
have any problems and is kept historically.
"""

import trgtools

import click
import numpy as np
from tqdm import tqdm


def start_time_check(ta: np.ndarray, tps: np.ndarray) -> bool:
    """
    Check the start time of TA.

    Parameter:
        ta (np.ndarray) : TA to quality check.
        tps (np.ndarray) : TPs associated to TA.

    Returns:
        (bool) : True if the times match, otherwise false.
    """
    return ta['time_start'] == tps[0]['time_start']


def end_time_check(ta: np.ndarray, tps: np.ndarray) -> bool:
    """
    Check the end time of TA.

    Parameter:
        ta (np.ndarray) : TA to quality check.
        tps (np.ndarray) : TPs associated to TA.

    Returns:
        (bool) : True if the times match, otherwise false.
    """
    return ta['time_end'] == tps[-1]['time_start']


def peak_time_check(ta: np.ndarray, tps: np.ndarray) -> bool:
    """
    Check the peak time of TA.

    Parameter:
        ta (np.ndarray) : TA to quality check.
        tps (np.ndarray) : TPs associated to TA.

    Returns:
        (bool) : True if the times match, otherwise false.
    """
    peak = 0
    time_peak = 0
    for tp in tps:
        if tp['adc_peak'] > peak:
            peak = tp['adc_peak']
            time_peak = tp['time_peak']
    return ta['time_peak'] == time_peak


@click.command()
@click.argument("file", type=click.Path(exists=True, readable=True))
def main(file):
    data = trgtools.TAReader(file)
    # Reading all fragments for now.
    data.read_all_fragments()

    start_time_count = 0
    end_time_count = 0
    peak_time_count = 0
    for ta, tps in tqdm(zip(data.ta_data, data.tp_data), total=len(data.ta_data)):
        if not start_time_check(ta, tps):
            start_time_count += 1
        if not end_time_check(ta, tps):
            end_time_count += 1
        if not peak_time_check(ta, tps):
            peak_time_count += 1

    print("Number of incorrect TA time starts:", start_time_count)
    print("Number of incorrect TA time ends:", end_time_count)
    print("Number of incorrect TA time peaks:", peak_time_count)
    return


if __name__ == "__main__":
    main()

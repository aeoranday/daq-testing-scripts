"""
Testing to compare two data sources that __should__ be the same.
"""

import trgtools

import click
import numpy as np


def fourth_tp_check(tps0: np.ndarray, tps1: np.ndarray) -> bool:
    """
    Check that the fourth TP in one source is the first in the other.

    Parameters:
        tps0 (np.ndarray) : One TP source.
        tps1 (np.ndarray) : One TP source.

    Returns:
        True if the fourth of one is the same as the first othe other.
    """
    return tps0[3] == tps1[0]


def check_fourth_subset(tps0: np.ndarray, tps1: np.ndarray) -> bool:
    """
    Check that the subset of fourth TP is the same.

    Parameters:
        tps0 (np.ndarray) : One TP source.
        tps1 (np.ndarray) : One TP source.

    Returns:
        True if the subsets are the same.
    """
    return np.all(tps0[3:] == tps1[:-3])


def check_fourth_bleed(tps0: np.ndarray, tps1: np.ndarray) -> bool:
    """
    Check that the subset of fourth TP is bleeding.

    Parameters:
        tps0 (np.ndarray) : One TP source. Origin TA.
        tps1 (np.ndarray) : One TP source. One TA early.

    Returns:
        True if there is blood.
    """
    return np.all(tps0[:3] == tps1[-3:])


@click.command()
@click.argument('file0')
@click.argument('file1')
def main(file0, file1):
    print("Reading data0 from", file0)  # During test, this was always a process_tpstream.cxx file.
    print("Reading data1 from", file1)  # This was always a replay application file.

    data0 = trgtools.TAReader(file0)
    data1 = trgtools.TAReader(file1)

    data0.read_all_fragments()
    data1.read_all_fragments()
    print("Number of TAs in data0:", len(data0.ta_data))
    print("Number of TAs in data1:", len(data1.ta_data))

    ta_offset = len(data1.ta_data) - len(data0.ta_data)

    # Test found that they both did not have the same start time.
#    time_same = data0.ta_data[:ta_offset]['time_start'] == data1.ta_data['time_start']
#    print("Both use the same start times?", np.all(time_same))
#    if not np.all(time_same):
#        print("Number of matching start times:", np.sum(time_same))

    # Found that the 4th TP in replay was the same as 1st TP in process_tpstream
    total_tas = len(data1.tp_data)
    matching_fourth = 0
    for tps0, tps1 in zip(data0.tp_data[:ta_offset], data1.tp_data):
        if check_fourth_subset(tps0, tps1):  # Was only checking the 4th; now checks an offset subset.
            matching_fourth += 1

    # Check if the last 3 in the "slow" file appear as the first 3 in the "fast" file.
    matching_blood = 0
    for idx in range(1, len(data0.tp_data[:ta_offset+1])):
        if check_fourth_bleed(data0.tp_data[idx], data1.tp_data[idx-1]):
            matching_blood += 1

    print(f"Number of matching fourth subsets: {matching_fourth} out of {total_tas} TAs")
    print(f"Number of matching fourth blood: {matching_blood} out of {total_tas-1} TAs")
    return

if __name__ == "__main__":
    main()

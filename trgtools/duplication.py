"""
Found that data members were being shared.
Tests if the data members are simply "duplicates".
"""

import numpy as np
import trgtools

import click

def build_simultaneous(file0, file1):
    """
    Instance both files and then read one after the other.
    """
    data0 = trgtools.TAReader(file0)
    data1 = trgtools.TAReader(file1)

    data0.read_fragment(data0.get_fragment_paths()[0])
    data1.read_fragment(data1.get_fragment_paths()[0])

    print("data0: Number of TAs read:", len(data0.ta_data))
    print("data0: Number of TPs read:", len(data0.tp_data))

    print("data1: Number of TAs read:", len(data1.ta_data))
    print("data1: Number of TPs read:", len(data1.tp_data))

    del data0
    del data1
    return

def build_consecutively(file0, file1):
    """
    Instance and read one file. Then instance and read the next file.
    """
    data0 = trgtools.TAReader(file0)
    data0.read_fragment(data0.get_fragment_paths()[0])

    print("data0: Number of TAs read:", len(data0.ta_data))
    print("data0: Number of TPs read:", len(data0.tp_data))

    data1 = trgtools.TAReader(file1)
    data1.read_fragment(data1.get_fragment_paths()[0])

    print("data1: Number of TAs read:", len(data1.ta_data))
    print("data1: Number of TPs read:", len(data1.tp_data))

    del data0
    del data1
    return

def build_data0(file0):
    """
    Only instance and read this file.
    """
    data0 = trgtools.TAReader(file0)
    data0.read_fragment(data0.get_fragment_paths()[0])

    print("data0: Number of TAs read:", len(data0.ta_data))
    print("data0: Number of TPs read:", len(data0.tp_data))

    del data0  # Got added later after seeing function scope didn't matter
    return

def build_data1(file1):
    """
    Only instance and read this file.
    (I know this is the same as the previous function.
    It was just nicer to read in main() this way.)
    """
    data1 = trgtools.TAReader(file1)
    data1.read_fragment(data1.get_fragment_paths()[0])

    print("data1: Number of TAs read:", len(data1.ta_data))
    print("data1: Number of TPs read:", len(data1.tp_data))

    del data1  # Got added later after seeing function scope didn't matter
    return

@click.command()
@click.argument("file0")
@click.argument("file1")
def main(file0, file1):
    print("Reading data0 from", file0)
    print("Reading data1 from", file1)

    print("Building Simultaneously")
    build_simultaneous(file0, file1)
    print("="*60)
    print("Building Consecutively")
    build_consecutively(file0, file1)
    print("="*60)
    print("Building data0")
    build_data0(file0)
    print("="*60)
    print("Building data1")
    build_data1(file1)
    return

if __name__ == "__main__":
    main()

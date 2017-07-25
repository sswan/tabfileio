# -*- coding: utf-8 -*-
"""
This is the basic test suite where, for each file type,
the file is written then read. The output of the process
is compared with the original data.
"""

import sys
import os
import pytest
import numpy as np

# Ensure that 'tabfileio' is imported from parent directory.
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(base))

try:
    import tabfileio as tfio
except ImportError:
    tfio = None

all_exts = ["txt", "txt.gz", "pkl", "xls", "xlsx", "json",
            "hdf5", "csv"]

@pytest.mark.parametrize('ext', all_exts)
def test_basic_read_write(ext):
    """
    Ensure that test data can be written and read successfully
    without using the column functionality.
    """

    filename = "output." + ext
    test_head = ["TIME", "INTEGER", "FLOAT"]
    test_data = np.array([[_ / 10.0, _, _ / 9.0] for _ in range(0, 10)])

    print("Writing {0}".format(filename))
    tfio.write_file(filename, test_head, test_data)

    print("Reading {0}".format(filename))
    head, data = tfio.read_file(filename)

    assert test_head == head
    assert np.allclose(test_data, data, atol=1.0e-12, rtol=1.0e-12)

    os.remove(filename)


@pytest.mark.parametrize('ext', all_exts)
def test_column_name_read_write(ext):
    """
    Ensure that test data can be written and read successfully
    with using the column name functionality.
    """

    filename = "output." + ext
    test_head = ["TIME", "INTEGER", "FLOAT"]
    test_data = np.array([[_ / 10.0, _, _ / 9.0] for _ in range(0, 10)])

    print("Writing {0}".format(filename))
    tfio.write_file(filename, test_head, test_data,
                    columns=["FLOAT", "TIME", "INTEGER"])

    print("Reading {0}".format(filename))
    head, data = tfio.read_file(filename, columns=test_head)

    assert test_head == head
    assert np.allclose(test_data, data, atol=1.0e-12, rtol=1.0e-12)

    os.remove(filename)


@pytest.mark.parametrize('ext', all_exts)
def test_column_index_read_write(ext):
    """
    Ensure that test data can be written and read successfully
    with using the column index functionality.
    """

    filename = "output." + ext
    test_head = ["TIME", "INTEGER", "FLOAT"]
    test_data = np.array([[_ / 10.0, _, _ / 9.0] for _ in range(0, 10)])

    print("Writing {0}".format(filename))
    tfio.write_file(filename, test_head, test_data,
                    columns=[2, 0, 1])

    print("Reading {0}".format(filename))
    head, data = tfio.read_file(filename, columns=[1, 2, 0])

    assert test_head == head
    assert np.allclose(test_data, data, atol=1.0e-12, rtol=1.0e-12)

    os.remove(filename)


@pytest.mark.parametrize('ext', all_exts)
def test_column_mixed_read_write(ext):
    """
    Ensure that test data can be written and read successfully
    with using the column index and name functionality.
    """

    filename = "output." + ext
    test_head = ["TIME", "INTEGER", "FLOAT"]
    test_data = np.array([[_ / 10.0, _, _ / 9.0] for _ in range(0, 10)])

    print("Writing {0}".format(filename))
    tfio.write_file(filename, test_head, test_data,
                    columns=["FLOAT", 0, 1])

    print("Reading {0}".format(filename))
    head, data = tfio.read_file(filename, columns=["TIME", "INTEGER", 0])

    assert test_head == head
    assert np.allclose(test_data, data, atol=1.0e-12, rtol=1.0e-12)

    os.remove(filename)

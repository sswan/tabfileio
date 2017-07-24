#!/usr/bin/env python
import numpy as np
import h5py


def read_hdf5(filename):

    F = h5py.File(filename, 'r')

    head = sorted(F.keys())
    data = np.array([F[_] for _ in head]).T

    F.close()

    return head, data


def write_hdf5(filename, head, data):

    F = h5py.File(filename, 'w')
    for idx, key in enumerate(head):
        F.create_dataset(key, data=data[:, idx])
    F.close()

#!/usr/bin/env python
import numpy as np
import h5py

tfio_key = "tabfileio order ID"

def write_hdf5(filename, head, data):

    hf = h5py.File(filename, 'w')
    for idx, key in enumerate(head):
        dset = hf.create_dataset(key, data=data[:, idx])
        # Save the order of columns as metadata
        dset.attrs.create(tfio_key, idx)
    hf.close()


def read_hdf5(filename):

    hf = h5py.File(filename, 'r')

    # Try to find column order metadata
    order = []
    for key in hf.keys():
        if tfio_key in hf[key].attrs:
            order.append([key, hf[key].attrs[tfio_key]])
        else:
            order.append([key, None])

    order = sorted(order, key=lambda x: x[1])
    head = [_[0] for _ in order]

    data = np.array([hf[_] for _ in head]).T

    hf.close()

    return head, data

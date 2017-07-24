#!/usr/bin/env python
import numpy as np
import pickle


def read_pickle(filename):

    with open(filename, 'rb') as F:
        head, data = pickle.load(F)

    data = np.array(data)

    return head, data


def write_pickle(filename, head, data):

    with open(filename, 'wb') as F:
        pickle.dump([head, data], F)

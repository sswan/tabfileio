#!/usr/bin/env python
import numpy as np
import json


def read_json(filename):

    # Cannot read as bytes, must be string
    with open(filename, 'r') as F:
        head, data = json.load(F)

    data = np.array(data)

    return head, data


def write_json(filename, head, data):

    if type(head) == np.ndarray:
        head = head.tolist()
    if type(data) == np.ndarray:
        data = data.tolist()

    # Cannot write as bytes, must be string
    with open(filename, 'w') as F:
        json.dump([head, data], F)

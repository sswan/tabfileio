import numpy as np
import tabfileio as tfio


def test_interpolate():

    test_list = [[1,
                  np.array([[ 0.0, 1.0],
                            [ 1.0, 0.0]]),
                  np.array([[ 0.0, 1.0],
                            [ 0.5, 0.5],
                            [ 1.0, 0.0]])
                 ],
                 [1,
                  np.array([[ 0.0,-1.0],
                            [-1.0, 0.0]]),
                  np.array([[ 0.0,-1.0],
                            [-0.5,-0.5],
                            [-1.0, 0.0]])
                 ],
                 [3,
                  np.array([[-1.0, 2.0],
                            [ 1.0,-2.0]]),
                  np.array([[-1.0, 2.0],
                            [-0.5, 1.0],
                            [ 0.0, 0.0],
                            [ 0.5,-1.0],
                            [ 1.0,-2.0]])
                 ],
                ]

    for N, data_in, data_out in test_list:
        data = tfio.utils.interpolate(data=data_in, N=N)
        assert np.max(np.abs(data - data_out)) < 1.0e-12




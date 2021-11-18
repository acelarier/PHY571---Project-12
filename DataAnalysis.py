"""
calculate using data, metadata
"""

import numpy as np
import matplotlib.pyplot as plt

def AverageVelocity(data, metadata):
    """return the average velocity  (between 0 and 1) from the numpy vector data
    with the formula from the ref (2)"""

    N = metadata[0]
    n_step = metadata[4]

    Cos = np.cos(data[:, :, 2])
    Sin = np.sin(data[:, :, 2])
    SumCos = np.sum(Cos, axis=1)
    SumSin = np.sum(Sin, axis=1)

    V_A = 1/N*(SumCos**2 + SumSin**2)**0.5
    v_a = np.mean(V_A)

    return v_a



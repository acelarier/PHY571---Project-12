"""
calculate using data, metadata
"""


# to do : a function tht takes a basePath and return a list of EXACT (dataPath, metadataPath) tabs / return a iterable /
# change UI.py (see headers in UI.py)



## toolkit

import numpy as np
import matplotlib.pyplot as plt
import os

def AverageVelocity(data, metadata):
    """return the average velocity  (between 0 and 1) from the numpy vector data
    with the formula from the ref (2)
    velocity averaged on particules AND time"""

    N = metadata[0]
    n_step = metadata[4]

    Cos = np.cos(data[:, :, 2])
    Sin = np.sin(data[:, :, 2])
    SumCos = np.sum(Cos, axis=1)
    SumSin = np.sum(Sin, axis=1)

    V_A = 1/N*(SumCos**2 + SumSin**2)**0.5
    v_a = np.mean(V_A)

    return v_a



## executable code



def basicTesting() :
    basePath = '/Users/antoine/Documents/X/3A/PHY571/project/PHY571---Project-12/experimental results/sim [01] fig2/testNoise'

    noises = [i/10 for i in range(10)]

    vas = []
    for i in range(10) :
        path = basePath + '_run' + str(i)
        data, meta = importData(path)
        va = AverageVelocity(data, meta)
        vas.append(va)

    plt.close('all')
    plt.figure()
    plt.plot(noises, vas, label = 'N = 40, L = 3.1')
    plt.xlabel('noise')
    plt.ylabel('average velocity')
    plt.title('Calculating v_a as in Viscek 1995, fig2')
    plt.legend()
    plt.show()



def upgradedTesting() :
    basePath = '/Users/antoine/Documents/X/3A/PHY571/project/PHY571---Project-12/experimental results/sim [01] fig2/upgradedTesting/testNoise'

    noises = []
    vas = []

    exit = False
    i = 0
    while not exit :
        testPath = basePath + '_run' + str(i)
        try :
            data, meta = importData(testPath)
        except :
            exit = True
        else :
            # each simulation is processed inloop to keep the cached memory light
            va = AverageVelocity(data, meta)
            noises.append(meta[2])
            vas.append(va)
        i += 1

    plt.close('all')
    plt.figure()
    thisLabel = 'N = %d, L = %f'%(meta[0], meta[1]) # crapy assignment...
    plt.plot(noises, vas, label = thisLabel)
    plt.xlabel('noise')
    plt.ylabel('average velocity')
    plt.title('Calculating v_a as in Viscek 1995, fig2')
    plt.legend()
    plt.show()


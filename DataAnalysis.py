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
    var = np.var(V_A)
    v_a_END = np.mean(V_A[300:])
    var_END = np.var(V_A[300:])

    return v_a_END, var_END



## executable code



def basicTesting() :
    basePath = '/Users/antoine/Documents/X/3A/PHY571/project/PHY571---Project-12/experimental results/sim [01] fig2/testNoise'

    noises = [i/10 for i in range(10)]

    vas = []
    vars = []
    for i in range(10) :
        path = basePath + '_run' + str(i)
        data, meta = importData(path)
        va, var = AverageVelocity(data, meta)
        vas.append(va)
        vars.append(var)

    plt.close('all')
    plt.figure()
    plt.plot(noises, vas, label = 'N = 40, L = 3.1')
    plt.xlabel('noise')
    plt.ylabel('average velocity')
    plt.title('Calculating v_a as in Viscek 1995, fig2')
    plt.legend()
    plt.show()



def upgradedTesting() :
    basePath = '/Users/antoine/Documents/X/3A/PHY571/project/PHY571---Project-12/experimental results/sim [01] fig2/40 particles/atan av/atan av'

    noises = []
    vas = []
    vars = []

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
            va, var = AverageVelocity(data, meta)
            noises.append(meta[2])
            vas.append(va)
            vars.append(var)
        i += 1

    noises = np.array(noises)
    vas = np.array(vas)
    vars = np.array(vars)
    N = str(int(meta[0]))
    L = "{:.2f}".format(meta[1])


    plt.close('all')
    plt.figure(figsize=(8,8))


    thisLabel = 'N = '+N+', L = '+L # crapy assignment...
    plt.plot(noises, vas, label = thisLabel)
    plt.fill_between(noises, vas-vars, vas+vars, edgecolor='#3F7F4C', facecolor='#3F7F4C', interpolate = True, alpha=0.1, linewidth=0)

    plt.xlabel('noise')
    plt.ylabel('average velocity')
    plt.title('Calculating v_a as in Viscek 1995, fig2')
    plt.legend()
    plt.show()


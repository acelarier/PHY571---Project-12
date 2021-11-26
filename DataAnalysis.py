"""
calculate using data, metadata
"""


# to do : a function tht takes a basePath and return a list of EXACT (dataPath, metadataPath) tabs / return a iterable /
# change UI.py (see headers in UI.py)


# activity : investigation of AverageVelocity on wednesday, 24 nov.


## toolkit

import numpy as np
import matplotlib.pyplot as plt
import os

def AverageVelocity(data, metadata, cut=0):
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
    v_a = np.mean(V_A[cut:])
    var = np.var(V_A[cut:])

    return v_a, var

def timeSeries(data, meta) :
    N = int(meta[0])
    n_step = int(meta[-1])

    Cos = np.cos(data[:, :, 2])
    Sin = np.sin(data[:, :, 2])
    SumCos = np.sum(Cos, axis=1)
    SumSin = np.sum(Sin, axis=1)

    V_A = 1/N*(SumCos**2 + SumSin**2)**0.5
    slidingV_A = np.zeros(n_step)

    # building a sliding average
    for step in range(n_step) :
        av = 0
        for i in range(100) :
            added_step = max(0, step-i)
            av += V_A[added_step]/100
        slidingV_A[step] += av
    return V_A, slidingV_A



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
    #basePath = '/Users/antoine/Documents/X/3A/PHY571/tmp/100p_long_run'
    basePath = '/Users/antoine/Documents/X/3A/PHY571/project/PHY571---Project-12/experimental results/sim [01] fig2/100 particles/long_run/100p_long_run'

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
    plt.figure(figsize=(5,5))


    thisLabel = 'N = '+N+', L = '+L # crapy assignment...
    plt.plot(noises, vas, label = thisLabel)
    plt.fill_between(noises, vas-vars, vas+vars, edgecolor='#3F7F4C', facecolor='#3F7F4C', interpolate = True, alpha=0.1, linewidth=0)

    plt.xlabel('noise')
    plt.ylabel('average velocity')
    plt.title('Calculating v_a as in Viscek 1995, fig2')
    plt.legend()
    plt.show()



def testingRelaxation() :
    basePath = '/Users/antoine/Documents/X/3A/PHY571/tmp/100p_long_run'

    noises = []
    vas = []
    vars = []
    vasCut = []
    varsCut = []

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
            va, var = AverageVelocity(data, meta, cut=0)
            noises.append(meta[2])
            vas.append(va)
            vars.append(var)

            n_step = int(meta[-1])
            vaCut, varCut = AverageVelocity(data, meta, cut=int(n_step*0.9))
            vasCut.append(vaCut)
            varsCut.append(varCut)

        i += 1

    noises = np.array(noises)
    vas = np.array(vas)
    vars = np.array(vars)
    vasCut = np.array(vasCut)
    varsCut = np.array(varsCut)
    N = str(int(meta[0]))
    L = "{:.2f}".format(meta[1])


    plt.close('all')
    plt.figure(figsize=(5,5))


    thisLabel = 'N = '+N+', L = '+L # crapy assignment...
    plt.plot(noises, vas, label = thisLabel + 'unrelaxed')
    plt.plot(noises, vasCut, label = thisLabel + 'relaxed (cut)')
    plt.fill_between(noises, vasCut-varsCut, vasCut+varsCut, edgecolor='#3F7F4C', facecolor='#3F7F4C', interpolate = True, alpha=0.1, linewidth=0)

    plt.xlabel('noise')
    plt.ylabel('average velocity')
    plt.title('Showing the difference with a relaxed situation')
    plt.legend()
    plt.show()



def showingRelaxation() :
    """show the time evolution of v_a for a series of run
indicate a directory containing the result of a testBench run in the variable 'basePath'"""
    basePath = '/Users/antoine/Documents/X/3A/PHY571/tmp/100p_long_run'

    noises = []
    vaSeries = []

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
            va = timeSeries(data, meta)[1]
            noises.append(meta[2])
            vaSeries.append(va)
        i += 1

    N = str(int(meta[0]))
    L = "{:.2f}".format(meta[1])


    plt.close('all')
    plt.figure(figsize=(5,5))

    for i in range(len(noises)) :
        thisLabel = 'N = '+N+', L = '+L+', noise = '+"{:.2f}".format(noises[i]) # crapy assignment...
        plt.plot(np.arange(len(vaSeries[i])), vaSeries[i], label = thisLabel)

    plt.xlabel('step')
    plt.ylabel('average velocity')
    plt.ylim(0,1)
    #plt.grid()
    plt.title('Time evolution of v_a')
    plt.legend()
    plt.show()

"""
shows the animation corresponding to a sim data set
formating :
    'data' --> np.array containing the data, shaped as (n_step, n_part, 3) for [time, particule ID, coordinates]
    'meta' --> np.array containing metadata, shaped as (5,)                for [N, L, noise, speed, n_step]
"""


# to do : modify UI.py so that filename and directory name are always distinguished ----> exportData only show filename (and not the path)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import matplotlib.patches as patches
from matplotlib.widgets import Button
import os



## toolkit


def genData() :
    """generates a random sample formated as a ParticleSystem.simulation() result
formating :
    'data' --> np.array containing the data, shaped as (n_step, n_part, 3) for [time, particule ID, coordinates]
    'meta' --> np.array containing metadata, shaped as (5,)                for [N, L, noise, speed, n_step]"""
    n_step = 100
    n_part = 20
    data = np.zeros((n_step, n_part, 3))
    for i in range(n_part) :
        part0 = np.random.rand(3)
        for j in range(n_step) :
            data[j,i,:] = np.random.rand(3)*0.1 + part0
    return data


def exportData(data, meta, path = None) :
    """saves the results of a trial as .npy files :
    data --> path + '_data'
    meta --> path + '_meta'"""
    if path == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        path = str(input('\nEnter path+filename : '))

    np.save(path + '_data', data)
    np.save(path + '_meta', meta)

    print('\nSimulation results saved as :\n    ' + path.rsplit(sep='/')[-1] + '_data.npy\n    ' + path.rsplit(sep='/')[-1] + '_meta.npy' )
    return



def importData(path = None) :
    """loads the results of a trial as numpy arrays
    ex :
    for two files named "monday_sim_1_data.npy" and "monday_sim_1_meta.npy" simulation : importData('/Users/antoine/Documents/...directories.../monday_sim_1')
    """

    if path == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        path = str(input('\nEnter path+filename : '))

    data = np.load(path + '_data.npy')
    meta = np.load(path + '_meta.npy')
    print('\nLoaded from :\n    ' + path.rsplit(sep='/')[-1] + '_data.npy\n    ' + path.rsplit(sep='/')[-1] + '_meta.npy' )
    return data, meta

def stop(event):
    global anim
    '''what to do here'''
    anim.event_source.stop()
    return



def displayLines(data, meta) :
    """displays a simulation with the twenty last positions as lines, for each particle"""
    n_step, n_part = np.shape(data)[0:2]
    speed = meta[3]

    layers = 3
    trace = 20
    thickness = [1.,0.5,0.3]
    colors = ['r', 'b', 'g']

    plt.close('all')
    plt.figure(figsize = (5,5))
    fig, ax = plt.subplots()
    plt.grid(ls='--', lw=0.5)
    lines = [ax.plot(data[0,pp//layers,0], data[0,pp//layers,1], linewidth = 0.5, color='b')[0] for pp in range(layers*n_part)] #here we plot x2 each line (one 'on top' of the other). If a line crosses a barrier, we use one for each side
    L = meta[1]
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)

    def frame(t):
        start=max((t-trace,0))
        for p in range(n_part) :
            cut_steps = [start]
            for i in range(start+1, t) :
                if np.abs(data[i-1,p,0]-data[i,p,0]) > speed+0.1 or np.abs(data[i-1,p,1]-data[i,p,1]) > speed+0.1 :
                    cut_steps.append(i)
            for i in range(layers+1-len(cut_steps)) :
                cut_steps.append(t)
            for k in range(len(cut_steps)-1) :
                lines[layers*p+k].set_data(data[cut_steps[k]:cut_steps[k+1],p,0], data[cut_steps[k]:cut_steps[k+1],p,1])
        return lines

    ani = animation.FuncAnimation(fig, frame, np.arange(1, n_step), interval=20)
    plt.show()

    return


def displayPoints(data, meta) :
    """displays a simulation with the twenty last positions as dots, for each particle"""
    n_step, n_part = np.shape(data)[0:2]

    plt.close('all')
    fig, ax = plt.subplots()
    plt.grid(ls='--', lw=0.5)
    L = meta[1]
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)

    trace = 20
    dotsize = L/300

    for t in range(trace) :
        for p in range(n_part) :
            dot = patches.Circle(data[t,p,0:2], dotsize)
            ax.add_patch(dot)

    def frame(t):
        start=max(t-trace,0)
        for p in range(n_part) :
            ax.patches.pop(0)
            dot = patches.Circle(data[t,p,0:2], dotsize)
            ax.add_patch(dot)
        return ax

    anim = animation.FuncAnimation(fig, frame, np.arange(1, n_step), interval=20)

    plt.show()
    return





def printState(syst) :
    """for handyness purpose only, useless otherwise"""
    print('FastParticuleSystem state :')
    print('N = %d, L = %d, farRange = %f'%(syst.N, syst.L, syst.farRange))
    try :
        for i in range(3) :
            x = syst.particles[i].pos[0]
            y = syst.particles[i].pos[1]
            theta = syst.particles[i].theta
            n = len(syst.particles[i].closeNeighbors[syst.heads])
            print('particle %d : pos = [%f,%f], theta = %f, number of neighbors = %d'%(i,x,y,theta,n))
    except :
        print('Value not yet defined')
    print('')
    return




## shortcuts

tmpPath = '/Users/antoine/Documents/X/3A/PHY571/tmp/'
fig2Path = '/Users/antoine/Documents/X/3A/PHY571/project/PHY571---Project-12/experimental results/sim [01] fig2/'
longBase = '/Users/antoine/Documents/X/3A/PHY571/project/PHY571---Project-12/experimental results/sim [01] fig2/100 particles/long_run/100p_long_run'


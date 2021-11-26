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

    print('\nSimulation results saved as :\n' + path + '_data.npy\n' + path + '_meta.npy' )
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
    print('\nLoaded from :\n' + path + '_data.npy\n' + path + '_meta.npy' )
    return data, meta

def stop(event):
    global anim
    '''what to do here'''
    anim.event_source.stop()
    return


def displayLines(data, meta) :
    """displays a simulation with the twenty last positions as lines, for each particle"""
    n_step, n_part = np.shape(data)[0:2]

    trace = 20
    thickness = 0.5

    plt.close('all')
    plt.figure(figsize = (5,5))
    fig, ax = plt.subplots()
    plt.grid()
    lines = [ax.plot(data[0,p,0], data[0,p,1], linewidth = thickness, color='r')[0] for p in range(n_part)]
    L = meta[1]
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)

    def frame(t):
        start=max((t-trace,0))
        for p in range(n_part) :
            lines[p].set_data(data[start:t,p,0],data[start:t,p,1])
        return lines

    ani = animation.FuncAnimation(fig, frame, np.arange(1, n_step), interval=200)
    plt.show()


def displayPoints(data, meta) :
    """displays a simulation with the twenty last positions as dots, for each particle"""
    n_step, n_part = np.shape(data)[0:2]

    plt.close('all')
    fig, ax = plt.subplots()
    plt.grid()
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




""" usefull for later


    def frame(i):
        start=max((i-5,0))
        for p in range(n_part) :
            lines[p].set_data(data[start:i,p,0],data[start:i,p,1])
        return lines


    button = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), 'Stop', color='g', hovercolor='0.975')
    button.on_clicked(stop)


button.on_clicked(reset)
"""
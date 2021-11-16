"""
shows the animation corresponding to a sim data set
formating :
    np.array, shape = (n_step, n_part, 3) --> [time, particule ID, coordinates]
    coordinates --> [x, y, theta]
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
import matplotlib.patches as patches
from matplotlib.widgets import Button
import os




def genData() :
    """generates a random sample formated as a simulation result (see headline)"""
    n_step = 100
    n_part = 20
    data = np.zeros((n_step, n_part, 3))
    for i in range(n_part) :
        part0 = np.random.rand(3)
        for j in range(n_step) :
            data[j,i,:] = np.random.rand(3)*0.1 + part0
    return data


def toFile(data, metadata) :
    """saves the results of a trial as .npy files :
    data     --> path + '_data'
    metadata --> path + '_metadata'"""

    current = os.getcwd()
    print('Current directory : ' + current)
    path = str(input('\nEnter path+filename : '))

    np.save(path + '_data', data)
    np.save(path + '_metadata', metadata)

    print('\nSimulation results saved as :\n' + path + '_data.npy\n' + path + '_metadata.npy' )
    return

def fromFile() :
    """loads the results of a trial as numpy arrays
ex : for two files named
    monday_sim_1_data.npy
    monday_sim_1_metadata.npy
then only write path + 'monday_sim_1' as an input
!!! don't write '.npy' !!!"""
    current = os.getcwd()
    print('Current directory : ' + current)
    path = str(input('\nEnter path+filename : '))

    data = np.load(path + '_data.npy')
    metadata = np.load(path + '_metadata.npy')

    print('\nLoaded from :\n' + path + '_data.npy\n' + path + '_metadata.npy' )
    return data, metadata

def stop(event):
    global anim
    '''what to do here'''
    anim.event_source.stop()
    return


def displayLines(data, metadata) :
    n_step, n_part = np.shape(data)[0:2]

    trace = 20

    plt.close('all')
    fig, ax = plt.subplots()
    lines = [ax.plot(data[0,p,0], data[0,p,1], linewidth = 0.5, color='r')[0] for p in range(n_part)]
    L = metadata[1]
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)

    def frame(t):
        start=max((t-trace,0))
        for p in range(n_part) :
            lines[p].set_data(data[start:t,p,0],data[start:t,p,1])
        return lines

    ani = animation.FuncAnimation(fig, frame, np.arange(1, n_step), interval=200)
    plt.show()


def displayPoints(data, metadata) :
    """displays a run with the five last positions as dots, for each particle"""
    n_step, n_part = np.shape(data)[0:2]

    plt.close('all')
    fig, ax = plt.subplots()
    L = metadata[1]
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)

    trace = 20

    for p in range(n_part) :
        dot = patches.Circle(data[0,p,0:2], L/100.)
        ax.add_patch(dot)

    def frame(t):
        start=max((t-trace,0))
        for p in range(n_part) :
            ax.patches.pop(0)
            dot = patches.Circle(data[t,p,0:2], L/400.)
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
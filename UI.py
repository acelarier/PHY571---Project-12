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


def toFile(data) :
    path = str(input(prompt = 'Enter the directory where you want to save the data'))
    np.save(path, data)
    print('Simulation results saved to ' + path)
    return

def fromFile() :
    path = str(input(prompt = 'Enter the complete filename you want to import'))
    data = np.load(path)
    return data

def stop(event):
    global anim
    '''what to do here'''
    anim.event_source.stop()
    return


def displayLines(data, metadata) :
    """displays a run with the five last positions with a line, for each particle (problems with periodic boundary)"""
    n_step, n_part = np.shape(data)[0:2]

    plt.close('all')
    fig, ax = plt.subplots()
    lines = [ax.plot(data[0,i,0], data[0,i,1], linewidth = 0.3, color='r')[0] for i in range(n_part)]

    L = metadata[0]
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)

    anim = animation.FuncAnimation(fig, frame, np.arange(1, n_step), interval=20)
    plt.show()


def displayPoints(data, metadata) :
    """displays a run with the five last positions as dots, for each particle"""
    n_step, n_part = np.shape(data)[0:2]

    plt.close('all')
    fig, ax = plt.subplots()
    L = metadata[0]
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)

    trace = 20

    for t in range(trace) :
        for p in range(n_part) :
            dot = patches.Circle(data[t,p,0:2], L/400.)
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
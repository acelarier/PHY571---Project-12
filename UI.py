"""
shows the animation corresponding to a sim data set
formating : 
    np.array, shape = (n_step, n_part, 3) --> [time, particule ID, coordinates]
    coordinates --> [x, y, theta]
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc




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





def display(file) :
    if isinstance(file, str) :
        data = np.load(file)
    else : data = file
    
    n_step, n_part = np.shape(data)[0:2]
    
    plt.close('all')
    fig, ax = plt.subplots()
    lines = [ax.plot(data[0,i,0], data[0,i,1], linewidth = 0.3, color='r')[0] for i in range(n_part)]
    ax.set_xlim(-.1,1.1)
    ax.set_ylim(-.1,1.1)
    
    def frame(i):
        start=max((i-5,0))
        for p in range(n_part) :
            lines[p].set_data(data[start:i,p,0],data[start:i,p,1])
        return lines
    
    ani = animation.FuncAnimation(fig, frame, np.arange(1, n_step), interval=200)
    plt.show()

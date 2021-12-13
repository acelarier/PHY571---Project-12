"""
calculate using data, meta
"""


# to do : a function tht takes a basePath and return a list of EXACT (dataPath, metadataPath) tabs / return a iterable /
# change UI.py (see headers in UI.py)


# activity : investigation of averageVelocity on wednesday, 24 nov.


## toolkit

import numpy as np
import matplotlib.pyplot as plt
import os







def histoTheta(data, meta, n_bins, accu) :
    """returns the histograms (for each timestep) of thetas"""

    N = int(meta[0])
    n_step = int(meta[4])

    counters = np.zeros((n_step, n_bins))
    dtheta = 2*np.pi/n_bins

    if not accu :
        for t in range(n_step) :
            avTheta = np.mean(data[t,:,2])
            for p in range(N) :
                delta = (data[t,p,2]-avTheta+np.pi)%(2*np.pi)
                ind = int(delta/dtheta)
                counters[t,ind] += 1/(N*dtheta)
    else :
        for t in range(n_step) :
            if t>0 :
                counters[t,:] += counters[t-1,:]
            avTheta = np.mean(data[t,:,2])
            for p in range(N) :
                delta = (data[t,p,2]-avTheta+np.pi)%(2*np.pi)
                ind = int(delta/dtheta)
                counters[t,ind] += 1
        for t in range(n_step) :
            counters[t,:] = counters[t,:]/((t+1)*N*dtheta)
            if t==100 :
                print(np.sum(counters[t,:])*dtheta)

    return counters





def histoDist(data, meta, n_bins, accu, verbose) :
    """returns the histograms (for each timestep) of thetas"""

    N = int(meta[0])
    n_step = int(meta[4])
    L = meta[1]

    counters = np.zeros((n_step, n_bins))
    dr = L/(np.sqrt(2)*n_bins)

    if not accu :
        for t in range(n_step) :
            if verbose : print('Step : %d/%d'%(t,n_step))
            for p in range(N) :
                for q in range(p+1,N) :
                    delta = np.abs(data[t,p,0:2]-data[t,q,0:2])
                    delta[0] = min(delta[0], L-delta[0]) # taking into account the peridodic boundary condition...
                    delta[1] = min(delta[1], L-delta[1]) # ...using the minimum
                    dist = np.linalg.norm(delta)
                    if dist > L :
                        print('ERROR dist>L')
                        print(L)
                        print(t,data[t,p,0:2],data[t,q,0:2], dist, dist/dr, n_bins)
                    ind = int(dist/dr)
                    counters[t,ind] += 2/(N*(N-1)*dr)
    else :
        for t in range(n_step) :
            if verbose : print('Step : %d/%d'%(t,n_step))
            if t>0 :
                counters[t,:] += counters[t-1,:]
            for p in range(N) :
                for q in range(p+1,N) :
                    delta = np.abs(data[t,p,0:2]-data[t,q,0:2])
                    delta[0] = min(delta[0], L-delta[0]) # taking into account the peridodic boundary condition...
                    delta[1] = min(delta[1], L-delta[1]) # ...using the minimum
                    dist = np.linalg.norm(delta)
                    ind = int(dist/dr)
                    counters[t,ind] += 1
        for t in range(n_step) :
            counters[t,:] = 2*counters[t,:]/((t+1)*N*(N-1)*dr)
            if t==100 :
                print(np.sum(counters[t,:])*dr)

    return counters


def averageVelocity(data, meta, cut=0):
    """return the average velocity  (between 0 and 1) from the numpy vector data with the formula from ref [02]
velocity is averaged on particules AND timesteps

optionnal parameter 'cut' (integer) allows to ignore the first <cut> timesteps"""

    N = meta[0]
    n_step = meta[4]

    if cut >= n_step :
        print('ERROR in averageVelocity : too many timesteps were ignored\n')
        return 0., 0.
    print('Velocity averaged on %d out of %d timesteps'%(n_step-cut, n_step))

    Cos = np.cos(data[:, :, 2])
    Sin = np.sin(data[:, :, 2])
    SumCos = np.sum(Cos, axis=1)
    SumSin = np.sum(Sin, axis=1)

    V_A = 1/N*(SumCos**2 + SumSin**2)**0.5
    v_a = np.mean(V_A[cut:])
    var = np.var(V_A[cut:])

    return v_a, var

def timeSeries(data, meta, smooth=0.1) :
    """builds the the time sequence of the average speed for a given simulation output
also builds a sliding average for readability with optionnal parameter smooth
    smooth = 0 --> no averaging
    smooth = 1 --> averaging on all time length"""

    N = int(meta[0])
    n_step = int(meta[-1])
    smoothingLenght = int(smooth*n_step)

    Cos = np.cos(data[:, :, 2])
    Sin = np.sin(data[:, :, 2])
    SumCos = np.sum(Cos, axis=1)
    SumSin = np.sum(Sin, axis=1)

    V_A = 1/N*(SumCos**2 + SumSin**2)**0.5
    slidingV_A = np.zeros(n_step)

    # building a sliding average
    for step in range(n_step) :
        av = 0
        for i in range(smoothingLenght) :
            added_step = max(0, step-i)
            av += V_A[added_step]/smoothingLenght
        slidingV_A[step] += av
    return V_A, slidingV_A



def correlate(V_A) :
    """builds the correlation function of the global speed"""
    n_step = len(V_A)
    avV_A = np.mean(V_A)

    corr = []
    vars = []

    for tau in range(n_step-100) :
        prod = V_A[:n_step-tau]*V_A[tau:] - avV_A**2 # version 1
        #prod = (V_A[:n_step-tau]-avV_A)*(V_A[tau:]-avV_A) # version 2
        corr.append(np.mean(prod))
        vars.append(np.var(prod))

    corr = np.array(corr)
    vars = np.array(vars)

    return corr, vars


## executable code



def velocityVsNoise(basePath=None) :
    """reads a set of files to plot the average speed as a function of the noise
the files must have the format defined in testBench.run"""
    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        basePath = str(input('\nEnter path + base pathname : '))

    #basePath = '/Users/antoine/Documents/X/3A/PHY571/tmp/100p_long_run'
    #basePath = '/Users/antoine/Documents/X/3A/PHY571/project/PHY571---Project-12/experimental results/sim [01] fig2/100 particles/long_run/100p_long_run'

    noises = []
    vas = []
    vars = []

    exit = False
    i = 0
    while not exit :
        testPath = basePath + '_sim' + str(i)
        try :
            data, meta = importData(testPath)
        except :
            exit = True
        else :
            # each ParticleSystem is processed inloop to keep the cached memory light
            va, var = averageVelocity(data, meta)
            noises.append(meta[2])
            vas.append(va)
            vars.append(var)
            i += 1
    if i==0 :
        print('[ERROR] Failed to load files')
        return

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

    plt.savefig(basePath)

    plt.show()

    return




def velocityVsNoiseVsRelaxation(basePath=None) :
    """reads a set of files to plot the average speed AND the average speed cutted as a function of the noise
the files must have the format defined in testBench.run"""

    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        basePath = str(input('\nEnter path + base pathname : '))
    #basePath = '/Users/antoine/Documents/X/3A/PHY571/tmp/100p_long_run'

    noises = []
    vas = []
    vars = []
    vasCut = []
    varsCut = []

    exit = False
    i = 0
    while not exit :
        testPath = basePath + '_sim' + str(i)
        try :
            data, meta = importData(testPath)
        except :
            exit = True
        else :
            # each ParticleSystem is processed inloop to keep the cached memory light
            va, var = averageVelocity(data, meta, cut=0)
            noises.append(meta[2])
            vas.append(va)
            vars.append(var)

            n_step = int(meta[-1])
            vaCut, varCut = averageVelocity(data, meta, cut=100)
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
    plt.plot(noises, vas, label = 'full timeframe')
    plt.plot(noises, vasCut, label = 'truncated timeframe')
    #plt.fill_between(noises, vasCut-varsCut, vasCut+varsCut, edgecolor='#3F7F4C', facecolor='#3F7F4C', interpolate = True, alpha=0.1, linewidth=0)

    plt.xlabel('noise')
    plt.ylabel('average velocity')
    plt.title('Showing the difference with a relaxed situation')
    plt.legend(title=thisLabel)

    plt.savefig(basePath)

    plt.show()
    return





def velocityVsTime(basePath=None) :
    """show the smoothed time evolution of v_a for a series of run
indicate a directory containing the result of a testBench run in the variable 'basePath'"""

    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        basePath = str(input('\nEnter path + base pathname : '))
    #basePath = '/Users/antoine/Documents/X/3A/PHY571/tmp/100p_long_run'

    noises = []
    vaSeries = []

    exit = False
    i = 0
    while not exit :
        testPath = basePath + '_sim' + str(i)
        try :
            data, meta = importData(testPath)
        except :
            exit = True
        else :
            # each ParticleSystem is processed inloop to keep the cached memory light
            va = timeSeries(data, meta)[1] #(...)[1] for smoothing !
            noises.append(meta[2])
            vaSeries.append(va)
        i += 1

    N = str(int(meta[0]))
    L = "{:.2f}".format(meta[1])


    plt.close('all')
    plt.figure(figsize=(5,5))

    for i in range(len(noises)) :
        #thisLabel = 'N = '+N+', L = '+L+', noise = '+"{:.2f}".format(noises[i]) # crapy assignment...
        thisLabel = 'noise = '+"{:.2f}".format(noises[i]) # crapy assignment...
        plt.plot(np.arange(len(vaSeries[i])), vaSeries[i], label = thisLabel)

    plt.xlabel('step')
    plt.ylabel('average velocity')
    plt.ylim(0,1)
    plt.grid(ls='--', lw=0.5)
    plt.title('Time evolution of v_a')
    plt.legend()


    plt.savefig(basePath)

    plt.show()
    return


def velocityVsAny(basePath=None) :
    """reads a set of files to plot the average speed as a function of the noise
the files must have the format defined in testBench.run"""
    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        basePath = str(input('\nEnter path + base pathname : '))

    #basePath = '/Users/antoine/Documents/X/3A/PHY571/tmp/100p_long_run'
    #basePath = '/Users/antoine/Documents/X/3A/PHY571/project/PHY571---Project-12/experimental results/sim [01] fig2/100 particles/long_run/100p_long_run'

    noises = []
    vas = []
    vars = []

    exit = False
    i = 0
    while not exit :
        testPath = basePath + '_sim' + str(i)
        try :
            data, meta = importData(testPath)
        except :
            exit = True
        else :
            # each ParticleSystem is processed inloop to keep the cached memory light
            va, var = averageVelocity(data, meta)
            noises.append(meta[2])
            vas.append(va)
            vars.append(var)
            i += 1
    if i==0 :
        print('[ERROR] Failed to load files')
        return

    index = np.array([j+1 for j in range(i)])
    vas = np.array(vas)
    vars = np.array(vars)
    N = str(int(meta[0]))
    L = "{:.2f}".format(meta[1])

    Mean = np.mean(vas)
    Var = np.var(vas)
    print('mean = %f\nvar = %f'%(Mean,Var))
    Means = np.array([Mean for j in range(i)])
    Vars = np.array([Var for j in range(i)])

    plt.close('all')
    plt.figure(figsize=(5,5))


    thisLabel = 'N = '+N+', L = '+L # crapy assignment...
    plt.plot(index, vas, label = thisLabel)
    plt.plot(index, Means, label = 'mean', ls='--')

    plt.xlabel('trial #')
    plt.ylabel('average velocity')
    plt.title('Calculating v_a as in Viscek 1995, fig2')
    plt.legend()


    plt.savefig(basePath)

    plt.show()

    return




def runtimeVSsyst(basePath=None) :
    """reads and displays a runtime trial"""

    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        basePath = str(input('\nEnter path + base pathname : '))

    runtimes = np.load(basePath + '_runtimes.npy')
    Ns = np.load(basePath + '_Ns.npy')
    syst = ['naïve', 'close neighbourhood', 'Particle In Cell']

    print('\nLoaded from :\n    ' + basePath.rsplit(sep='/')[-1] + '_runtimes.npy\n    ' + basePath.rsplit(sep='/')[-1] + '_Ns.npy' )

    plt.close('all')
    plt.figure(figsize=(5,5))

    plt.plot(Ns, runtimes[0], label = syst[0])
    plt.plot(Ns, runtimes[1], label = syst[1])
    plt.plot(Ns, runtimes[2], label = syst[2])

    plt.xlabel('population')
    plt.ylabel('runtime (s)')
    plt.grid(ls='--', lw=0.5)
    plt.title('Runtime')
    plt.legend()

    plt.savefig(basePath)

    plt.show()

    return





def timeCorrelation(basePath=None) :
    """show the smoothed time evolution of v_a for a series of run
indicate a directory containing the result of a testBench run in the variable 'basePath'"""

    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        basePath = str(input('\nEnter path + base pathname : '))
    #basePath = '/Users/antoine/Documents/X/3A/PHY571/tmp/100p_long_run'

    noises = []
    corrSeries = []

    exit = False
    i = 0
    while not exit :
        testPath = basePath + '_sim' + str(i)
        try :
            data, meta = importData(testPath)
        except :
            exit = True
        else :
            # each ParticleSystem is processed inloop to keep the cached memory light
            va = timeSeries(data, meta)[0]
            corr, vars = correlate(va) #(...)[1] for smoothing !
            noises.append(meta[2])
            corrSeries.append(corr)
        i += 1

    N = str(int(meta[0]))
    L = "{:.2f}".format(meta[1])


    plt.close('all')
    plt.figure(figsize=(5,5))

    for i in range(len(corrSeries)) :
        #thisLabel = 'N = '+N+', L = '+L+', noise = '+"{:.2f}".format(noises[i]) # crapy assignment...
        thisLabel = 'noise = '+"{:.2f}".format(noises[i]) # crapy assignment...
        plt.plot(np.arange(len(corrSeries[i])), corrSeries[i], label = thisLabel)

    plt.xlabel('step')
    plt.ylabel('correlation (unitless)')
    #plt.ylim(-0.005,0.02)
    plt.grid(ls='--', lw=0.5)
    plt.title('Correlation functions')
    plt.legend()


    #plt.savefig(basePath)

    plt.show()
    return





def distLiveHisto(basePath=None, n_bins=20, accu=False, verbose=False) :


    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        path = str(input('\nEnter path + base pathname + _sim# : '))

    data, meta = importData(path)

    n_step, n_part = np.shape(data)[0:2]
    speed = meta[3]
    noise = meta[2]
    layers = 3
    trace = 20
    L = meta[1]

    counters = histoDist(data, meta, n_bins, accu, verbose)
    dists = np.linspace(0, L/np.sqrt(2), n_bins)


    thickness = [1.,0.5,0.3]
    colors = ['r', 'b', 'g']

    plt.close('all')
    fig = plt.figure(figsize=(14,5))
    ax = fig.add_subplot(121, aspect='equal')
    #plt.grid(ls='--', lw=0.5)
    lines = [ax.plot(data[0,pp//layers,0], data[0,pp//layers,1], linewidth = 0.5, color='b')[0] for pp in range(layers*n_part)] #here we plot x3 each line (one 'on top' of the other). If a line crosses a barrier, we use one for each side
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)

    ax = fig.add_subplot(122, aspect='auto')

    thisLabel = 'noise = '+"{:.2f}".format(noise) +', N = %d'%(n_part)
    histo = ax.plot(dists, counters[0,:], label = thisLabel)[0]
    ax.set_xlim(0,L/(np.sqrt(2)))
    ax.set_xlabel('distance')
    ax.set_ylabel('density')
    ax.set_ylim(0,1.3*np.max(counters))
    ax.legend()


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

        histo.set_data(dists,counters[t,:])
        return lines, histo

    ani = animation.FuncAnimation(fig, frame, np.arange(1, n_step), interval=10)
    plt.show()

    return


def thetaLiveHisto(basePath=None, n_bins=20, accu=False) :

    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        path = str(input('\nEnter path + base pathname + _sim# : '))

    data, meta = importData(path)

    counters = histoTheta(data, meta, n_bins, accu)
    thetas = np.linspace(-np.pi, np.pi, n_bins)


    n_step, n_part = np.shape(data)[0:2]
    speed = meta[3]
    noise = meta[2]

    layers = 3
    trace = 20
    thickness = [1.,0.5,0.3]
    colors = ['r', 'b', 'g']

    plt.close('all')
    fig = plt.figure(figsize=(14,5))
    ax = fig.add_subplot(121, aspect='equal')
    #plt.grid(ls='--', lw=0.5)
    lines = [ax.plot(data[0,pp//layers,0], data[0,pp//layers,1], linewidth = 0.5, color='b')[0] for pp in range(layers*n_part)] #here we plot x3 each line (one 'on top' of the other). If a line crosses a barrier, we use one for each side
    L = meta[1]
    ax.set_xlim(0,L)
    ax.set_ylim(0,L)

    ax = fig.add_subplot(122, aspect='auto')

    thisLabel = 'noise = '+"{:.2f}".format(noise) +', N = %d'%(n_part)
    histo = ax.plot(thetas, counters[0,:], label=thisLabel)[0]
    ax.set_xlim(-np.pi, np.pi)
    ax.set_xlabel('\u03B8 - \u27E8\u03B8\u27e9 (rad)')
    ax.set_ylim(0,1.3*np.max(counters))
    ax.set_ylabel('density (/rad)')
    ax.legend()


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

        histo.set_data(thetas,counters[t,:])
        return lines, histo

    ani = animation.FuncAnimation(fig, frame, np.arange(1, n_step), interval=10)
    plt.show()

    return



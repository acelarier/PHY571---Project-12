"""
file used to run functions

!!! needs to execute modelling.py and UI.py before !!!
"""


import time


## toolkit



class TestBench:
    """class able to run multiple simulations successively"""

    def __init__(self, metadatas , basePath, fast=False, farRange=30, field=False) :
        self.mds = metadatas
        self.basePath = basePath
        self.fast = fast
        self.field = field
        self.farRange = farRange

        self.total_runs = len(metadatas)
        self.current_run = -1

        self.timelimit = -1
        self.start_time = 0
        self.stop_time = -1
        self.runtimes = np.array([-1 for i in range(self.total_runs)])
        return

        #self.syst = ParticleSystem()

    def setPath(self, newBasePath) :
        self.basePath = newBasePath
        return

    def setmetadatas(self, mds) :
        self.metadatas = mds
        return

    def showProgress(self) :
        print('\nTest bench progress : %d/%d\n'%(self.current_run,self.total_runs))
        return

    def run(self, verbSim=False) :
        """execute the simulations for the ParticleSystem described in metadatas
no initCondition are indicated for the moment
Runs as followed :
    1 : reads a line from 'metadatas' and builds the corresponding ParticleSystem object ('.syst')
    2 : initialises the ParticleSystem
    3 : executes the simulation on it
    4 : saves the results with a specified data format : [basePath + '_sim' + run number]_data.npy and [basePath + '_sim' + run number]_meta.npy"""
        self.current_run = 0
        for i in range(self.total_runs) :
            N = int(self.mds[i,0])
            L = self.mds[i,1]
            noise = self.mds[i,2]
            speed = self.mds[i,3]
            n_step = int(self.mds[i,4])

            if self.field :
                self.syst = ParticleSystemWithField(N, L, noise, speed)
            elif self.fast :
                self.syst = FastParticleSystem(N, L, noise, speed, farRange=self.farRange)
            else : self.syst = ParticleSystem(N, L, noise, speed)
            self.syst.initialise() # eventually add an input possibility for this function to always start with the same distribution...

            self.start_time = time.time()
            data, meta = self.syst.simulate(n_step, verbose=verbSim)
            self.stop_time = time.time()
            self.runtimes[i] = self.stop_time - self.start_time
            self.current_run += 1
            self.showProgress()

            exportData(data, meta, self.basePath + '_sim' + str(i))
        return





tmp = [[400, 10, 4, 0.03, 1000] for i in range(1)] + [[400, 10, 5*(i+1)/30, 0.03, 1000] for i in range(0)]

## executable code

def noiseTestBench(basePath=None, fast=False, farRange=25, field=False) :
    """execute the simulations specified in the built-in variable 'testNoise'
save the results in the specified path"""
    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        basePath = str(input('\nEnter path + base filename : '))

    global tmp

    #metas = np.array(tmp)
    metas = np.array([[100, 5, (i+1), 0.03, 10000] for i in range(5)])
    #metas = np.array([[40, 3.1, (i+1), 0.03, 10000] for i in range(5)])
    #metas = np.array([[300, 25, 0.1, 0.03, 1000],
    #                  [300, 7,  2,   0.03, 1000],
    #                  [300, 5,  0.1, 0.03, 1000]])
    bench = TestBench(metas, basePath, fast, farRange, field)

    bench.run(verbSim=True)
    return


def densityTestBench(basePath=None, fast=False, farRange=20) :
    """execute the simulations specified in the built-in variable 'testNoise'
save the results in the specified path"""
    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        basePath = str(input('\nEnter path + base filename : '))

    metas = np.array([[rho*400, 20, 3, 0.03, 1000] for rho in range(4)])
    bench = TestBench(metas, basePath, fast, farRange)

    bench.run(verbSim=True)




def oneShotTestBench(N, L, noise, speed, n_step, fast=False, field=False, res=False, _farRange=30, noShow=False) :
    """execute a single simulation specified by N, L, noise, speed, n_step"""
    farRange = _farRange

    if field :
        syst = ParticleSystemWithField(N, L, noise, speed)
    elif fast :
        syst = FastParticleSystem(N, L, noise, speed, farRange)
    else :
        syst = ParticleSystem(N, L, noise, speed)
    syst.initialise() # initialize a random configuration
    data, meta, runtime = syst.simulate(n_step, verbose=True)
    va = averageVelocity(data, meta, cut = 100)[0]
    print('Average velocity : %f'%(va))
    if not noShow : displayLines(data, meta)
    if res : return data, meta
    return va, runtime





def runtimeTestBench(basePath=None) :
    """exucute a series of runs for different values of N and different calculus methods (PIC, fast or naive)"""

    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        basePath = str(input('\nEnter path + base pathname : '))

    runtimes = [[],[],[]]

    Ns = [int(40*((100/40)**(1/2))**(i-3)) for i in range(8)]

    # naïve
    for N in Ns :
        rt = oneShotTestBench(N, 5, 2, 0.03, 100, noShow=True)[1]
        runtimes[0].append(rt)
    # close neighbourhood
    for N in Ns :
        rt = oneShotTestBench(N, 5, 2, 0.03, 100, fast=True, noShow=True)[1]
        runtimes[1].append(rt)
    # PIC
    for N in Ns :
        rt = oneShotTestBench(N, 5, 2, 0.03, 100, field=True, noShow=True)[1]
        runtimes[2].append(rt)


    runtimes=np.array(runtimes)
    Ns = np.array(Ns)

    np.save(basePath + '_runtimes', runtimes)
    np.save(basePath + '_Ns', Ns)

    print('\nSimulation results saved as :\n    ' + basePath.rsplit(sep='/')[-1] + '_runtimes.npy\n    ' + basePath.rsplit(sep='/')[-1] + '_Ns.npy' )

    return



def thetaLiveHisto(basePath=None, n_bins=20, accu=False) :

    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        path = str(input('\nEnter path + base pathname + _sim# : '))

    data, meta = importData(path)

    counters = histoTheta(data, meta, n_bins, accu)
    if not accu :
        thetas = np.linspace(0, 2*np.pi, n_bins)
    else :
        thetas = np.linspace(-np.pi, np.pi, n_bins)


    n_step, n_part = np.shape(data)[0:2]
    speed = meta[3]

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

    histo = ax.plot(thetas, counters[0,:])[0]
    if not accu :
        ax.set_xlim(0, 2*np.pi)
        ax.set_xlabel('theta')
    else :
        ax.set_xlim(-np.pi, np.pi)
        ax.set_xlabel('angular deviation')
    ax.set_ylim(0,1)


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

    ani = animation.FuncAnimation(fig, frame, np.arange(1, n_step), interval=100)
    plt.show()

    return


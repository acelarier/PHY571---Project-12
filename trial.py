"""
file used to run functions

!!! needs to execute modelling.py and UI.py before !!!
"""


import time


## toolkit



class TestBench:
    """class able to run multiple simulations successively"""

    def __init__(self, metadatas , basePath, fast=False) :
        self.mds = metadatas
        self.basePath = basePath
        self.fast = fast

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

            if self.fast : self.syst = FastParticleSystem(N, L, noise, speed)
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








## executable code

def noiseTestBench(basePath=None, fast=False) :
    """execute the simulations specified in the built-in variable 'testNoise'
save the results in the specified path"""
    if basePath == None :
        current = os.getcwd()
        print('Current directory : ' + current)
        basePath = str(input('\nEnter path + base filename : '))

    metas = np.array([[40, 5, 5*(5+i+1)/30, 0.03, 1000] for i in range(3)])
    bench = TestBench(metas, basePath, fast)

    bench.run(verbSim=True)
    return


def oneShotTestBench(res=False) :
    """execute a single simulation specified by the built-in variables 'N', 'L', 'noise', 'speed', 'n_step'
default values :
    N = 300
    L = 25
    noise = 0.1
    speed = 0.03
    n_step = 30"""
    N = 100
    L = 25
    noise = 0.1
    speed = 0.03

    n_step = 90

    syst = ParticleSystem(N, L, noise, speed) # reminder : numberParticles, boxSize, noise, speed
    syst.initialise() # initialize a random configuration
    data, meta = syst.simulate(n_step, verbose=True)
    displayLines(data, meta)
    if res : return data, meta
    return



def oneShotTestBenchFastParticle(res=False, _farRange=10, noShow=False) :
    """execute a single simulation specified by the built-in variables 'N', 'L', 'noise', 'speed', 'n_step'
default values :
    N = 300
    L = 25
    noise = 0.1
    speed = 0.03
    n_step = 30"""
    N = 100
    L = 25
    noise = 0.1
    speed = 0.03
    farRange = _farRange

    n_step = 90

    syst = FastParticleSystem(N, L, noise, speed, farRange) # reminder : numberParticles, boxSize, noise, speed
    syst.initialise() # initialize a random configuration
    data, meta = syst.simulate(n_step, verbose=True)
    if not noShow : displayLines(data, meta)
    if res : return data, meta
    return





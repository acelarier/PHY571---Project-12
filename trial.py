"""
file used to run functions

!!! needs to execute modelling.py and UI.py before !!!
"""


import time


## toolkit



class testBench:

    def __init__(self, metadatas , basePath) :
        self.mds = metadatas
        self.basePath = basePath

        self.total_runs = len(metadatas)
        self.current_run = -1

        self.timelimit = -1
        self.start_time = 0
        self.stop_time = -1
        self.runtimes = np.array([-1 for i in range(self.total_runs)])

        #self.sim = Simulation()

    def setPath(self, newBasePath) :
        self.basePath = newBasePath

    def setmetadatas(self, mds) :
        self.metadatas = mds

    def showProgress(self) :
        print('\nProgress : %d/%d\n'%(self.current_run,self.total_runs))

    def run(self) :

        self.current_run = 0
        for i in range(self.total_runs) :
            N = int(self.mds[i,0])
            L = self.mds[i,1]
            noise = self.mds[i,2]
            speed = self.mds[i,3]
            n_step = int(self.mds[i,4])

            self.sim = Simulation(N, L, noise, speed)
            self.sim.initialise() # eventually add an input possibility for this function to always start with the same distribution...

            self.start_time = time.time()
            data, meta = self.sim.run(n_step)
            self.stop_time = time.time()
            self.runtimes[i] = self.stop_time - self.start_time
            self.current_run += 1
            self.showProgress()

            exportData(data, meta, self.basePath + '_run' + str(i))









## executable code

def testingTheTestBench() :
    testNoise = np.array([[40, 3.1, 5*i/30, 0.03, 1000] for i in range(30)])
    basePath = '/Users/antoine/Documents/X/3A/PHY571/project/PHY571---Project-12/experimental results/sim [01] fig2/40 particles/atan av'
    bench = testBench(testNoise, basePath)

    bench.run()


def oneTrial() :
    numberParticles = 300
    boxSize = 25
    etaNoise = 0.1
    speed = 0.03

    numberTimeStep = 1000

    sim = Simulation(numberParticles, boxSize, etaNoise, speed) # reminder : numberParticles, boxSize, noise, speed
    print('Simulation créée')

    sim.initialise() # initialize a random configuration
    print('Simulation initialisée. Calcul évolution...')


    data, metadata = sim.run(numberTimeStep)
    print('Calcul terminé. Affichage...')

    displayLines(data, metadata)






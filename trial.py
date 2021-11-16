"""
file used to run functions

!!! needs to execute modelling.py and UI.py before !!!
"""


import time



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




class testbench:

    def __init__(metadatas , wrkdir) :
        self.md = metadatas
        self.wrkdir = wrkdir

        self.total_runs = len(metadatas)
        self.current_run = -1

        self.timelimit = -1
        self.start_time = 0
        self.stop_time = -1
        self.runtimes = np.array([-1 for i in range(total_runs)])

        #self.sim = Simulation()

    def setPath(self, new_wrkdir) :
        self.wrkdir = new_wrkdir

    def setmetadatas(self, md) :
        self.metadatas = md

    def showProgress(self) :
        prg = int(100*self.current_run/self.total_runs)
        print(prg)

    def run(self) :

        for i in range(total_runs) :
            N = self.md[i,0]
            L = self.md[i,1]
            noise = self.md[i,2]
            speed = self.md[i,3]
            n_step = self.md[i,4]

            self.sim = Simulation(N, L, noise, speed)
            self.sim.initialise() # eventually add an input possibility for this function to start with the same distribution always...

            self.start_time = time.time()
            data, meta = self.sim.run(n_step)
            self.stop_time = time.time()
            self.runtimes[i] = self.stop_time - self.start_time
            self.showProgress()

            export(self.wrkdir + )





"""
classes and functions used to model the situation described in [02]
"""

import numpy as np
import random
import math
import time


## toolkit



# to do : traduire la table des matières dans overleaf
#         il faut que update il faut mettre à jour les theta APRÈS avoir calculé les nouveaux theta pour tout le monde



class Particle:
    """A class that define a particule (a bird) by its position and oriented speed."""

    def __init__(self, position, speed, theta, noise, L):
        self.pos = position
        self.speed = speed
        self.theta = theta
        self.avTheta = 0
        self.noise = noise
        self.L = L
        return


    def updateAvTheta(self, neighbors) :
        """calculus of the average direction of the velocities of particles being within a circle of radius r surrounding the given particle (neighbors)
periodic boundary conditions are used"""
        ngb = len(neighbors)>0
        if ngb :
            avCos = 0
            avSin = 0
            for neighbor in neighbors :
                avCos += np.cos(neighbor.theta)
                avSin += np.sin(neighbor.theta)
            # avCos & avSin are not normalised because we use only their ratio
            self.avTheta = math.atan(avSin/avCos)
            if avCos<0 :
                self.avTheta += np.pi
        return ngb

    def updateOrientation(self):
        """the thetas are updated AFTER all particle have calculated the 'avTheta'"""
        self.theta = self.avTheta + random.uniform(-self.noise/2,self.noise/2)
        self.theta = self.theta%(2*math.pi)
        return


    def updatePosition(self):
        """moves particle at constant speed, with peridodic boundary condition
it is assumed that the time unit between two updates is the unit of time"""
        self.pos[0]+=np.cos(self.theta)*self.speed
        self.pos[1]+=np.sin(self.theta)*self.speed
        for i in range(2):
            if self.pos[i]>self.L :
                self.pos[i]-=self.L
            if self.pos[i]<0 :
                self.pos[i]+=self.L
        return






class ParticleSystem:
    """arg : N, L, noise, speed
A class that compute a simulation of particules interacting with their neighboors and moving within a box.
The box has periodic boundary counditions.
        """

    def __init__(self, N = 20, L = 7, noise = 0.1, speed = 0.03):
        self.N = N
        self.R = 1
        self.L = L
        self.noise = noise
        self.speed = speed
        self.particles = list()
        return

    def initialise(self) :
        """generates a random configuration of particles"""
        for i in range(self.N) :
            self.particles.append(Particle(np.array([random.uniform(0,self.L), random.uniform(0,self.L)]), self.speed, random.uniform(0,2*np.pi), self.noise, self.L))
        return




    def getNeighbors(self, particle):
        """generates the list of neighbors at less than 1 unit
enumerates all numbers (complexity = N)
can be massively improved"""
        neighbors = []
        for i in range(self.N) :
            particle_i = self.particles[i]
            delta = particle_i.pos - particle.pos
            delta[0] = min(delta[0], self.L-delta[0]) # taking into account the peridodic boundary condition...
            delta[1] = min(delta[1], self.L-delta[1]) # ...using the minimum
            distance = np.linalg.norm(delta)
            if distance <= self.R :
                neighbors.append(particle_i)
        return neighbors

    def doStep(self):
        """engine executing an elementary step"""
        for i in range(self.N):
            neighbors = self.getNeighbors(self.particles[i])
            self.particles[i].updateAvTheta(neighbors)
        for i in range(self.N):
            self.particles[i].updateOrientation()
            self.particles[i].updatePosition()
        return

    def simulate(self, n_step, verbose=False) :
        """runs a simulation of n_step and return a numpy array formatted as above
return :
    'data' --> np.array containing the data, shaped as (n_step, n_part, 3) for [time, particule ID, coordinates]
    'meta' --> np.array containing metadata, shaped as (5,)                for [N, L, noise, speed, n_step]
example :
                       x0     y0     theta0  x1     y1     theta1
    data = np.array([[[1.393, 0.383, 0.000], [1.393, 0.383, 0.000]],       step 0
                     [[1.393, 0.583, 0.000], [1.393, 0.383, 0.300]],       step 1
                     [[1.393, 0.783, 0.000], [1.393, 0.383, 0.600]],       step 2
                     [[1.393, 0.983, 0.000], [1.393, 0.383, 0.900]],       step 3
                     [[1.393, 1.183, 0.000], [1.393, 0.383, 1.200]]]       step 4"""

        if verbose :
            print('ParticleSystem start running...')
            start_time = time.time()

        data = np.zeros((n_step, self.N, 3))

        for p in range(0,self.N) :
            data[0,p,0:2] = self.particles[p].pos
            data[0,p,2] = self.particles[p].theta
        for t in range(1,n_step) :
            if verbose : print('Step : %d/%d'%(t,n_step))
            self.doStep()
            for p in range(0,self.N) :
                data[t,p,0:2] = self.particles[p].pos
                data[t,p,2] = self.particles[p].theta

        meta = np.array([self.N, self.L, self.noise, self.speed, n_step])


        if verbose :
            stop_time = time.time()
            runtime = stop_time - start_time
            print('Runtime : %f s'%(runtime))
            print('End of simulation')

        return data, meta


class FastParticle(Particle):
    """This classe is based on the 'Particle' class. It adds a two-staged neighbors calculator"""

    def __init__(self, position, speed, theta, noise, L):
        Particle.__init__(self, position, speed, theta, noise, L)
        self.closeNeighbors = []
        return



class FastParticleSystem(ParticleSystem):

    def __init__(self,  N = 60, L = 7, noise = 0.1, speed = 0.03, farRange=None) :
        ParticleSystem.__init__(self, N, L, noise, speed)
        if farRange == None :
            self.farRange = int(speed**-1) # number of timesteps neccessary to cross a full radius
        else :
            self.farRange = farRange
        self.countdown = 0
        return

    def initialise(self) :
        """generates a random configuration of particles"""
        for i in range(self.N) :
            self.particles.append(FastParticle(np.array([random.uniform(0,self.L), random.uniform(0,self.L)]), self.speed, random.uniform(0,2*np.pi), self.noise, self.L))
        return


    def getNeighbors(self, particle) :
        """return the exact neighbors of a given particle
AT EACH STEP : look for neighbors in 'particle.closeNeihbors'
WHEN 'countdown' goes to 0 : updates 'particle.closeNeihbors'
this method can make the function up to x10 faster"""
        # updating pools
        if self.countdown == 0 :
            particle.closeNeighbors.clear()
            for part in self.particles :
                delta = part.pos - particle.pos
                delta[0] = min(delta[0], self.L-delta[0]) # taking into account the peridodic boundary condition...
                delta[1] = min(delta[1], self.L-delta[1]) # using the minimum
                distance = np.linalg.norm(delta)
                lowerBound = np.floor((distance-1)/(2*self.speed)) # 1 stands as the radius here
                if lowerBound < self.farRange :
                    particle.closeNeighbors.append(part)
        # calculating the neighbors
        neighbors = []
        for close_one in particle.closeNeighbors :
            distance = np.linalg.norm(close_one.pos - particle.pos)
            if distance < self.R :
                neighbors.append(close_one)
        return neighbors



    def doStep(self):
        """engine executing an elementary step"""
        problem=False
        for i in range(self.N):
            neighbors = self.getNeighbors(self.particles[i])
            ok = self.particles[i].updateAvTheta(neighbors)
            if not ok : print('no neighbors while countdown = %d'%(self.countdown))
        for i in range(self.N):
            self.particles[i].updateOrientation()
            self.particles[i].updatePosition()
        if self.countdown == 0 :
            self.countdown = self.farRange
        self.countdown -= 1
        return













class node:
    """A class that define the nodes of a field. They are evaluating the average orientation of the particle in the boxes around the node ("Particule In Cell" method).
        """
    def __init__(self, positionx, positiony):
        self.i = positionx
        self.j = positiony
        self.SumCos = 0
        self.SumSin = 0
        self.SumPonderation = 0




class ParticleInField:
    """A class that define a particule (a bird) by his position and oriented speed.
        """

    def __init__(self, position, speed, orientation, noise, boxSize):
        """It is assumed that the box has a size that is an integer.
            """
        self.pos = position
        self.v = speed
        self.theta = orientation
        self.costheta = math.cos(orientation)
        self.sintheta = math.sin(orientation)
        self.noise = noise
        self.L = int(boxSize)


    def updateOrientation(self, nodes):
    #calculus of the average direction of the velocities of particles being within a circle of radius r surrounding the given particle (neighbors).
        sommeAires = 0
        sumPonderationNodes = 0
        self.costheta = 0
        self.sintheta = 0
        #where is the particle ?
        i = int(self.pos[0])
        j = int(self.pos[1])
        if i==self.L :
            i=0
        if j==self.L :
            j=0
        #noeud i,j
        aire = (self.pos[0] - i)*(self.pos[1] - j)
        sommeAires += aire
        if nodes[i*self.L + j].SumPonderation != 0 :
            self.costheta += nodes[i*self.L + j].SumCos * (1 - aire)
        if nodes[i*self.L + j].SumPonderation != 0 :
            self.sintheta += nodes[i*self.L + j].SumSin * (1 - aire)
        sumPonderationNodes += nodes[i*self.L + j].SumPonderation
        #noeud i+1,j
        if int(self.pos[0])+1==self.L :
            i = 0
        else :
            i = int(self.pos[0]) + 1
        j = int(self.pos[1])
        aire = (i - self.pos[0])*(self.pos[1] - j)
        sommeAires += aire
        if nodes[i*self.L + j].SumPonderation !=0 :
            self.costheta += nodes[i*self.L + j].SumCos * (1 - aire)
        if nodes[i*self.L + j].SumPonderation !=0 :
            self.sintheta += nodes[i*self.L + j].SumSin * (1 - aire)
        sumPonderationNodes += nodes[i*self.L + j].SumPonderation
        #noeud i,j+1
        i = int(self.pos[0])
        if int(self.pos[1])+1==self.L :
            j = 0
        else :
            j = int(self.pos[1]) + 1
        aire = (self.pos[0] - i)*(j - self.pos[1])
        sommeAires += aire
        if nodes[i*self.L + j].SumPonderation !=0 :
            self.costheta += nodes[i*self.L + j].SumCos * (1 - aire)
        if nodes[i*self.L + j].SumPonderation !=0:
            self.sintheta += nodes[i*self.L + j].SumSin * (1 - aire)
        sumPonderationNodes += nodes[i*self.L + j].SumPonderation
        #noeud i+1,j+1
        if int(self.pos[0])+1==self.L :
            i = 0
        else :
            i = int(self.pos[0]) + 1
        if int(self.pos[1])+1==self.L :
            j = 0
        else :
            j = int(self.pos[1]) + 1
        aire = (i - self.pos[0])*(j - self.pos[1])
        sommeAires += aire
        if nodes[i*self.L + j].SumPonderation !=0 :
            self.costheta += nodes[i*self.L + j].SumCos * (1 - aire)
        if nodes[i*self.L + j].SumPonderation !=0 :
            self.sintheta += nodes[i*self.L + j].SumSin * (1 - aire)
        sumPonderationNodes += nodes[i*self.L + j].SumPonderation
        #renormalization
        #unuseful to normalize costheta and sintheta as we use the ratio to calculate theta and we then (after adding the random part of theta) update costheta and sintheta
        if sommeAires != 0 :
            self.costheta = self.costheta / sommeAires
            self.sintheta = self.sintheta / sommeAires
        if sumPonderationNodes != 0 :
            self.costheta = self.costheta / sumPonderationNodes
            self.sintheta = self.sintheta / sumPonderationNodes
        if self.costheta == 0 :
            self.theta = np.pi/2
        elif self.costheta<0 :
            self.theta = math.atan(self.sintheta / self.costheta) + np.pi
        else :
            self.theta = math.atan(self.sintheta / self.costheta)
        #ad of the noise on theta
        self.theta += random.uniform(-self.noise/2,self.noise/2)
        self.theta = self.theta%(2*math.pi)
        self.costheta = math.cos(self.theta)
        self.sintheta = math.sin(self.theta)




    def updatePosition(self):
    #it is assumed that the time unit between two updates is the unit of time.
        self.pos[0]+=self.costheta*self.v
        self.pos[1]+=self.sintheta*self.v
        for i in range(2):
            if self.pos[i]>self.L :
                self.pos[i]-=self.L
            if self.pos[i]<0 :
                self.pos[i]+=self.L





class ParticleSystemWithField:
    """arg : numberParticles, boxSize, etaNoise, speed
A class that compute a simulation of particules interacting with their neighboors and moving within a box.
    The box has periodic boundary counditions.
        """

    def __init__(self, N = 20, L = 7, noise = 0.1, speed = 0.03):
        self.N = N
        self.R = 1
        self.L = int(L)
        self.noise = noise
        self.speed = speed
        self.particles = list()
        self.nodes = list()


    def initialise(self) :
        #initialize the particles
        for i in range(self.N) :
            self.particles.append(ParticleInField(np.array([random.uniform(0,self.L), random.uniform(0,self.L)]), self.speed, random.uniform(0,2*np.pi), self.noise, self.L))
        #initialize the field
        for i in range(self.L):
            for j in range(self.L):
                self.nodes.append(node(i,j))


    def updatefield(self):
        #re-initialize the field
        for i in range(self.L):
            for j in range(self.L):
                self.nodes[i*self.L + j].SumCos = 0
                self.nodes[i*self.L + j].SumSin = 0
                self.nodes[i*self.L + j].SumPonderate = 0
        #calculate the nodes
        for k in range(self.N) :
            particle = self.particles[k]
            #where is the particle ? at the frontier between two cases, the particle is in the right/upper box. Attention to the limit periodic conditions
            i = int(particle.pos[0])
            j = int(particle.pos[1])
            if i>=self.L :
                i=0
            if j>=self.L :
                j=0
            #node i,j
            aire = (particle.pos[0] - i)*(particle.pos[1] - j)
            self.nodes[i*self.L + j].SumCos += particle.costheta * (1 - aire)
            self.nodes[i*self.L + j].SumSin += particle.sintheta * (1 - aire)
            self.nodes[i*self.L + j].SumPonderation += (1 - aire)
            #node i+1,j
            if int(particle.pos[0])+1==self.L :
                i = 0
            else :
                i = int(particle.pos[0]) + 1
            j = int(particle.pos[1])
            aire = (i - particle.pos[0])*(particle.pos[1] - j)
            self.nodes[i*self.L + j].SumCos += particle.costheta * (1 - aire)
            self.nodes[i*self.L + j].SumSin += particle.sintheta * (1 - aire)
            self.nodes[i*self.L + j].SumPonderation += (1 - aire)
            #node i,j+1
            i = int(particle.pos[0])
            if int(particle.pos[1])+1==self.L :
                j = 0
            else :
                j = int(particle.pos[1]) + 1
            aire = (particle.pos[0] - i)*(j - particle.pos[1])
            self.nodes[i*self.L + j].SumCos += particle.costheta * (1 - aire)
            self.nodes[i*self.L + j].SumSin += particle.sintheta * (1 - aire)
            self.nodes[i*self.L + j].SumPonderation += (1 - aire)
            #node i+1,j+1
            if int(particle.pos[0])+1==self.L :
                i = 0
            else :
                i = int(particle.pos[0]) + 1
            if int(particle.pos[1])+1==self.L :
                j = 0
            else :
                j = int(particle.pos[1]) + 1
            aire = (i - particle.pos[0])*(j - particle.pos[1])
            self.nodes[i*self.L + j].SumCos += particle.costheta * (1 - aire)
            self.nodes[i*self.L + j].SumSin += particle.sintheta * (1 - aire)
            self.nodes[i*self.L + j].SumPonderation += (1 - aire)



    def doStep(self):
        self.updatefield()
        for i in range(self.N):
            self.particles[i].updateOrientation(self.nodes)
        for i in range(self.N):
            self.particles[i].updatePosition()



    def simulate(self, n_step, verbose=False) :
        """data format : np.array, shape = (n_step, n_part, 3) --> [time, particule ID, coordinates]
                         + an array containing meta data : [N, L, noise, speed, n_step]
           runs a simulation of n_step and return a numpy array formatted as above"""
        data = np.zeros((n_step, self.N, 3))

        for p in range(0,self.N) :
            data[0,p,0:2] = self.particles[p].pos
            data[0,p,2] = self.particles[p].theta
        for t in range(1,n_step) :
            self.doStep()
            for p in range(1,self.N) :
                data[t,p,0:2] = self.particles[p].pos
                data[t,p,2] = self.particles[p].theta

        meta = np.array([self.N, self.L, self.noise, self.speed, n_step])

        return data, meta








## executable code





def investigate() :
    """for testing purpose only"""
    r=10

    syst = FastParticleSystem(farRange=r)
    syst.initialise()


    printState(syst)
    syst.doStep()
    printState(syst)
    for i in range(r) :
        syst.doStep()
    printState(syst)
    for i in range(r) :
        syst.doStep()
    printState(syst)


    print('total step done = %d'%(2*r+2))
    return

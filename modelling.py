"""
classes and functions used to model the situation described in [02]
all code is taken from the jupyter notebook written by Armelle
"""

import numpy as np
import random
import math
import time

class particle:
    """A class that define a particule (a bird) by its position and oriented speed.
        """

    def __init__(self, position, speed, theta, noise, L):
        self.pos = position
        self.speed = speed
        self.theta = theta
        self.noise = noise
        self.L = L

    def updateOrientation(self, neighbors):
        """calculus of the average direction of the velocities of particles being within a circle of radius r surrounding the given particle (neighbors)
periodic boundary conditions are used"""
        avTheta = 0
        n_neighbors = len(neighbors)

        """averarge of theta"""
        for neighbor in neighbors :
            avTheta += neighbor.theta
        avTheta = avTheta / n_neighbors

        """cotan (average sin / average cos )"""
        avCos = 0
        avSin = 0
        for neighbor in neighbors :
            avCos += np.cos(neighbor.theta)
            avSin += np.sin(neighbor.theta)
        # avCos & avSin are not normalised because we use only their ratio
        altAvTheta = math.atan(avSin/avCos)

        self.theta = altAvTheta + random.uniform(-self.noise/2,self.noise/2)
        self.theta = self.theta%(2*math.pi)


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

    def initialise(self) :
        """generates a random configuration of particles"""
        for i in range(self.N) :
            self.particles.append(particle(np.array([random.uniform(0,self.L), random.uniform(0,self.L)]), self.speed, random.uniform(0,2*np.pi), self.noise, self.L))

    def getNeighbors(self, particle):
        """generates the list of neighbors at less than 1 unit
enumerates all numbers (complexity = N)
can be massively improved"""
        neighbors = []
        for i in range(self.N) :
            particle_i = self.particles[i]
            distance = np.linalg.norm(particle_i.pos - particle.pos)
            if distance <= self.R :
                neighbors.append(particle_i)
        return neighbors

    def doStep(self):
        """engine executing an elementary step"""
        for i in range(self.N):
            neighbors = self.getNeighbors(self.particles[i])
            self.particles[i].updateOrientation(neighbors)
        for i in range(self.N):
            self.particles[i].updatePosition()

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

        for p in range(1,self.N) :
            data[0,0,0:2] = self.particles[p].pos
            data[0,0,2] = self.particles[p].theta
        for t in range(1,n_step) :
            if verbose : print('Step : %d/%d'%(t,n_step))
            self.doStep()
            for p in range(1,self.N) :
                data[t,p,0:2] = self.particles[p].pos
                data[t,p,2] = self.particles[p].theta

        meta = np.array([self.N, self.L, self.noise, self.speed, n_step])


        if verbose :
            stop_time = time.time()
            runtime = stop_time - start_time
            print('Runtime : %f s'%(runtime))
            print('End of simulation')

        return data, meta




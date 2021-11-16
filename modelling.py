"""
classes and functions used to model the situation described in [02]
all code is taken from the jupyter notebook written by Armelle
"""

import numpy as np
import random
import math


class particle:
    """A class that define a particule (a bird) by his position and oriented speed.
        """

    def __init__(self, position, speed, orientation, noise, boxSize):
        self.pos = position
        self.v = speed
        self.theta = orientation
        self.eta = noise
        self.L = boxSize

    def updateOrientation(self, neighbors):
    #calculus of the average direction of the velocities of particles being within a circle of radius r surrounding the given particle (neighbors).
        averageNeighborsOrientation = 0
        neighborsNumber = len(neighbors)
        for neighbor in neighbors :
            averageNeighborsOrientation += neighbor.theta
        averageNeighborsOrientation = averageNeighborsOrientation / neighborsNumber
        self.theta = averageNeighborsOrientation + random.uniform(-self.eta/2,self.eta/2)
        self.theta = self.theta%(2*math.pi)


    def updatePosition(self):
    #it is assumed that the time unit between two updates is the unit of time.
        self.pos[0]+=np.cos(self.theta)*self.v
        self.pos[1]+=np.sin(self.theta)*self.v
        for i in range(2):
            if self.pos[i]>self.L :
                self.pos[i]-=self.L
            if self.pos[i]<0 :
                self.pos[i]+=self.L


class Simulation:
    """A class that compute a simulation of particules interacting with their neighboors and moving within a box.
    The box has periodic boundary counditions.
        """

    def __init__(self, numberParticles, interactionRadius, boxSize, noise, speed):
        self.N = numberParticles
        self.R = 1 #self.R = interactionRadius
        self.L = boxSize
        self.eta = noise
        self.speed = speed
        self.particles = list()

    def initialise(self) :
        for i in range(self.N) :
            self.particles.append(particle(np.array([random.uniform(0,self.L), random.uniform(0,self.L)]), self.speed, random.uniform(0,2*np.pi), self.eta, self.L))

    def getNeighbors(self, particle):
        neighbors = []
        for i in range(self.N) :
            particle_i = self.particles[i]
            distance = np.linalg.norm(particle_i.pos - particle.pos)
            if distance <= self.R :
                neighbors.append(particle_i)
        return neighbors

    def doStep(self):
        for i in range(self.N):
            neighbors = self.getNeighbors(self.particles[i])
            self.particles[i].updateOrientation(neighbors)
        for i in range(self.N):
            self.particles[i].updatePosition()

    def run(self, n_step) :
        """data format : np.array, shape = (n_step, n_part, 3) --> [time, particule ID, coordinates]
                         + an array containing meta data : [L]
           runs a simulation of n_step and return a numpy array formatted as above"""
        data = np.zeros((n_step, self.N, 3))

        for p in range(1,self.N) :
            data[0,0,0:2] = self.particles[p].pos
            data[0,0,2] = self.particles[p].theta
        for t in range(1,n_step) :
            self.doStep()
            for p in range(1,self.N) :
                data[t,p,0:2] = self.particles[p].pos
                data[t,p,2] = self.particles[p].theta

        metadata = np.array([self.L])

        return data, metadata







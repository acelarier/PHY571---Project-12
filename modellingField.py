"""
classes and functions used to model the situation described in [02]
all code is taken from the jupyter notebook written by Armelle
"""

import numpy as np
import random
import math
from array import array


class node:
    """A class that define the nodes of a field. They are evaluating the average orientation of the particle in the boxes around the node ("Particule In Cell" method).
        """
    def __init__(self, positionx, positiony):
        self.i = positionx
        self.j = positiony
        self.SumCos = 0
        self.SumSin = 0
        self.SumPonderation = 0




class particle:
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
        self.eta = noise
        self.L = int(boxSize)


    def updateOrientation(self, nodes):
    #calculus of the average direction of the velocities of particles being within a circle of radius r surrounding the given particle (neighbors).
        sommeAires = 0
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
        if nodes[i*self.L + j].SumPonderation == 0 :
            self.costheta= 0
        else :
            self.costheta = nodes[i*self.L + j].SumCos / nodes[i*self.L + j].SumPonderation * (1 - aire)
        if nodes[i*self.L + j].SumPonderation == 0 :
            self.sintheta = 0
        else :
            self.sintheta = nodes[i*self.L + j].SumSin / nodes[i*self.L + j].SumPonderation * (1 - aire)
        #noeud i+1,j
        if int(self.pos[0])+1==self.L :
            i = 0
        else :
            i = int(self.pos[0]) + 1
        j = int(self.pos[1])
        aire = (i - self.pos[0])*(self.pos[1] - j)
        sommeAires += aire
        if nodes[i*self.L + j].SumPonderation==0 :
            self.costheta = 0
        else :
            self.costheta = nodes[i*self.L + j].SumCos / nodes[i*self.L + j].SumPonderation * (1 - aire)
        if nodes[i*self.L + j].SumPonderation==0 :
            self.sintheta = 0
        else :
            self.sintheta = nodes[i*self.L + j].SumSin / nodes[i*self.L + j].SumPonderation * (1 - aire)
        #noeud i,j+1
        i = int(self.pos[0])
        if int(self.pos[1])+1==self.L :
            j = 0
        else :
            j = int(self.pos[1]) + 1
        aire = (self.pos[0] - i)*(j - self.pos[1])
        sommeAires += aire
        if nodes[i*self.L + j].SumPonderation==0:
            self.costheta = 0
        else :
            self.costheta = nodes[i*self.L + j].SumCos / nodes[i*self.L + j].SumPonderation * (1 - aire)
        if nodes[i*self.L + j].SumPonderation==0:
            self.sintheta = 0
        else :
            self.sintheta = nodes[i*self.L + j].SumSin / nodes[i*self.L + j].SumPonderation * (1 - aire)
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
        if nodes[i*self.L + j].SumPonderation==0 :
            self.costheta = 0
        else :
            self.costheta = nodes[i*self.L + j].SumCos / nodes[i*self.L + j].SumPonderation * (1 - aire)
        if nodes[i*self.L + j].SumPonderation==0 :
            self.sintheta = 0
        else :
            self.sintheta = nodes[i*self.L + j].SumSin / nodes[i*self.L + j].SumPonderation * (1 - aire)
        #renormalization
        #unuseful to normalize costheta and sintheta as we use the ratio to calculate theta and we then (after adding the random part of theta) update costheta and sintheta
        if sommeAires != 0 :
            self.costheta = self.costheta / sommeAires
            self.sintheta = self.sintheta / sommeAires
        if self.costheta == 0 :
            self.theta = np.pi/2
        else :
            self.theta = math.atan(self.sintheta / self.costheta)
        #ad of the noise on theta
        self.theta += random.uniform(-self.eta/2,self.eta/2)
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





class Simulation:
    """arg : numberParticles, boxSize, etaNoise, speed
A class that compute a simulation of particules interacting with their neighboors and moving within a box.
    The box has periodic boundary counditions.
        """

    def __init__(self, numberParticles = 20, boxSize = 7, etaNoise = 0.1, speed = 0.03):
        self.N = numberParticles
        self.R = 1
        self.L = int(boxSize)
        self.eta = etaNoise
        self.speed = speed
        self.particles = list()
        self.nodes = list()


    def initialise(self) :
        #initialize the particles
        for i in range(self.N) :
            self.particles.append(particle(np.array([random.uniform(0,self.L), random.uniform(0,self.L)]), self.speed, random.uniform(0,2*np.pi), self.eta, self.L))
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
        for i in range(self.N) :
            particle = self.particles[i]
            #where is the particle ? at the frontier between two cases, the particle is in the right/upper box. Attention to the limit periodic conditions
            i = int(particle.pos[0])
            j = int(particle.pos[1])
            if i>=self.L :
                i=0
            if j>=self.L :
                j=0
            #node i,j
            aire = (particle.pos[0] - i)*(particle.pos[1] - j)
            self.nodes[i*self.L + j].SumCos = particle.costheta * (1 - aire)
            self.nodes[i*self.L + j].SumSin = particle.sintheta * (1 - aire)
            self.nodes[i*self.L + j].SumPonderation = (1 - aire)
            #node i+1,j
            if int(particle.pos[0])+1==self.L :
                i = 0
            else :
                i = int(particle.pos[0]) + 1
            j = int(particle.pos[1])
            aire = (i - particle.pos[0])*(particle.pos[1] - j)
            self.nodes[i*self.L + j].SumCos = particle.costheta * (1 - aire)
            self.nodes[i*self.L + j].SumSin = particle.sintheta * (1 - aire)
            self.nodes[i*self.L + j].SumPonderation = (1 - aire)
            #node i,j+1
            i = int(particle.pos[0])
            if int(particle.pos[1])+1==self.L :
                j = 0
            else :
                j = int(particle.pos[1]) + 1
            aire = (particle.pos[0] - i)*(j - particle.pos[1])
            self.nodes[i*self.L + j].SumCos = particle.costheta * (1 - aire)
            self.nodes[i*self.L + j].SumSin = particle.sintheta * (1 - aire)
            self.nodes[i*self.L + j].SumPonderation = (1 - aire)
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
            self.nodes[i*self.L + j].SumCos = particle.costheta * (1 - aire)
            self.nodes[i*self.L + j].SumSin = particle.sintheta * (1 - aire)
            self.nodes[i*self.L + j].SumPonderation = (1 - aire)



    def doStep(self):
        self.updatefield()
        for i in range(self.N):
            self.particles[i].updateOrientation(self.nodes)
        for i in range(self.N):
            self.particles[i].updatePosition()



    def run(self, n_step) :
        """data format : np.array, shape = (n_step, n_part, 3) --> [time, particule ID, coordinates]
                         + an array containing meta data : [N, L, eta, speed, n_step]
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

        metadata = np.array([self.N, self.L, self.eta, self.speed, n_step])

        return data, metadata
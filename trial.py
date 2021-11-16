"""
file used to run functions

!!! needs to execute modelling.py and UI.py before !!!
"""

sim = Simulation(100, 0.1, 1, 0.1, 0.01) # reminder : numberParticles, interactionRadius, boxSize, noise, speed

sim.initRandom() # initialize a random configuration

data = sim.run(10)

display(data)


"""
file used to run functions

!!! needs to execute modelling.py and UI.py before !!!
"""

numberParticles = 300
boxSize = 7
etaNoise = 2
speed = 0.03

numberTimeStep = 100





sim = Simulation(numberParticles, boxSize, etaNoise, speed) # reminder : numberParticles, boxSize, noise, speed
print('Simulation créée')

sim.initialise() # initialize a random configuration
print('Simulation initialisée. Calcul évolution...')

data, metadata = sim.run(numberTimeStep)
print('Calcul terminé. Affchage...')

displayPoints(data, metadata)


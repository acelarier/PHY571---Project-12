"""
file used to run functions

!!! needs to execute modelling.py and UI.py before !!!
"""

sim = Simulation(10, 0.1, 7, 0.1, 0.01) # reminder : numberParticles, interactionRadius, boxSize, noise, speed
print('Simulation créée')

sim.initialise() # initialize a random configuration
print('Simulation initialisée. Calcul évolution...')

data, metadata = sim.run(100)
print('Calcul terminé. Affchage...')

displayPoints(data, metadata)


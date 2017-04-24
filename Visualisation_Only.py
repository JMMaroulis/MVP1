import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as numpy
import Methods as Methods
import sys
import random

# WARNING
# DO NOT TRY TO MAKE n ANYTHING ABOVE APPROX 1000
# DRAW METHOD CANNOT KEEP UP

# command line input:
# width, height, temperature, boltzmann, J, n, dynamics(1/0), starting_spins
# n = number of attempted updates per sweep
# dynamics: 1 = glauber; dynamics = 0 = kawasaki
# starting_spins: 1 = all +1, 2 = half and half, 3 = randomised

# defining various constants
# mostly defined via console argument input,
height = int(sys.argv[1])
width = int(sys.argv[2])
temperature = float(sys.argv[3])
boltzmann = float(sys.argv[4])
J = -int(sys.argv[5])
n = int(sys.argv[6])
dynamics = int(sys.argv[7])
starting_spins = int(sys.argv[8])

# variable importing for Methods class
Methods.import_variables(boltzmann, J)

# initialise various spin arrays for use later
# all ones
ones_spins = numpy.ones((width, height))

# random
numbers = [-1, 1]
random_spins = [[random.choice(numbers) for a in range(height)] for b in range(width)]
random_spins = numpy.array(random_spins)

# half and half
half_spins = numpy.ones((width, height))

for i in range(0, height):
    for j in range(0, (width/2)):
        half_spins[i][j] = -1

# various yield methods to get animation working happily
# for some reason, it really doesn't like being in loops
def generate_data_glauber():
    Methods.update_glauber_n(spins, n, temperature)

    return spins

def generate_data_kawasaki():
    Methods.update_kawasaki_n(spins, n, temperature)

    return spins

def update(state):
    mat.set_data(state)
    return mat

def data_gen_glauber():
    while True:
        yield generate_data_glauber()

def data_gen_kawasaki():
    while True:
        yield generate_data_kawasaki()


# starting spin state choice
if starting_spins == 1:
    spins = ones_spins
elif starting_spins == 2:
    spins = half_spins
elif starting_spins == 3:
    spins = random_spins
else:
    print("Choose a starting spin state setup!")

# glauber/kawasaki user choice
if dynamics == 1:
    fig, ax = plt.subplots()
    mat = ax.matshow(generate_data_glauber())
    plt.colorbar(mat)
    ani = animation.FuncAnimation(fig, update, data_gen_glauber, interval=50)
elif dynamics == 0:
    fig, ax = plt.subplots()
    mat = ax.matshow(generate_data_kawasaki())
    plt.colorbar(mat)
    ani = animation.FuncAnimation(fig, update, data_gen_kawasaki, interval=50)
else:
    print("Choose a dynamic!")

plt.show()

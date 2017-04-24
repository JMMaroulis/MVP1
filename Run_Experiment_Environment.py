import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as numpy
import Methods as Methods
import Measurements
import sys
import random
import gc

# command line input:
# width, height, temperature, boltzmann, J, n, dynamics(1/0), visualisation, num_sweeps_in_run
# n = number of updates per sweep
# dynamics = 1 = glauber; dynamics = 0 = kawasaki
# visualisation = 1 = show, 0 = don't show
# num_sweeps_in_run = how many measurements per temperature block

# defining various constants
# mostly defined via console argument input,
height = int(sys.argv[1])
width = int(sys.argv[2])
temperature = float(sys.argv[3])
boltzmann = float(sys.argv[4])
J = -int(sys.argv[5])
n = int(sys.argv[6])
dynamics = int(sys.argv[7])
visualisation = int(sys.argv[8])
num_sweeps_in_run = int(sys.argv[9])

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


# define running methods, using temp increase and measurement taking
sweep_count = 0

def generate_data_glauber():
    Methods.update_glauber_n(spins, n, temperature)

    global sweep_count
    sweep_count += 1

    if sweep_count > 500:

        # measurements
        mag_array.append(abs(Measurements.magnetisation(spins)))
        energy_array.append(Measurements.energy(spins))
        temp_array.append(temperature)

        # correlation buffer
        for p in range(0, 10):
            Methods.update_glauber_n(spins, n, temperature)

    if sweep_count == (500 + num_sweeps_in_run):
        sweep_count = 0

        # temp increase
        global temperature
        temperature += 0.1
        print("temperature =", temperature)
        gc.collect()

    return spins

def generate_data_kawasaki():
    Methods.update_kawasaki_n(spins, n, temperature)

    global sweep_count
    sweep_count += 1

    # sweep until temperatures uncorrelated
    if sweep_count > 500:

        # measurements
        mag_array.append(abs(Measurements.magnetisation(spins)))
        energy_array.append(Measurements.energy(spins))
        temp_array.append(temperature)

        # correlation buffer
        for p in range(0, 10):
            Methods.update_kawasaki_n(spins, n, temperature)

    if sweep_count == (500 + num_sweeps_in_run):
        sweep_count = 0

        # temp increase
        global temperature
        temperature += 0.1
        print("temperature =", temperature)
        gc.collect()

    return spins

# yield statements
def update(state):
    mat.set_data(state)
    return mat

def data_gen_glauber():
    while True:
        yield generate_data_glauber()

def data_gen_kawasaki():
    while True:
        yield generate_data_kawasaki()

# generate measurement lists
mag_array = list()
energy_array = list()
susc_array = list()
temp_array = list()
cap_array = list()
energy_array_running = list()
mag_array_running = list()
susc_error_array = list()
cap_error_array = list()


gc.disable()
# visualisation user choice
# glauber/kawasaki user choice
# NOTE: IF VISUALISING, CORRELATION BUFFER BETWEEN MEASUREMENTS WILL NOT BE SHOWN
# SOME STUTTERING IS, THEREFORE, TO BE EXPECTED
if visualisation == 1:
    if dynamics == 1:
        spins = ones_spins
        fig, ax = plt.subplots()
        mat = ax.matshow(generate_data_glauber())
        plt.colorbar(mat)
        ani = animation.FuncAnimation(fig, update, data_gen_glauber, interval=50)
    elif dynamics == 0:
        spins = half_spins
        fig, ax = plt.subplots()
        mat = ax.matshow(generate_data_kawasaki())
        plt.colorbar(mat)
        ani = animation.FuncAnimation(fig, update, data_gen_kawasaki, interval=50)

    plt.show()

elif visualisation == 0:
    if dynamics == 1:
        spins = ones_spins
        while temperature <= 3:
            generate_data_glauber()
    elif dynamics == 0:
        spins = numpy.array(random_spins)
        while temperature <= 3:
            generate_data_kawasaki()

else:
    print("choose whether or not to visualise!")

    gc.enable()
# generate susceptibility
Measurements.susceptibility_bootstrap(mag_array, susc_array, susc_error_array, temp_array, spins, num_sweeps_in_run)
# generate specific heat capacity
Measurements.heat_capacity_bootstrap(energy_array, cap_array, cap_error_array, temp_array, spins, num_sweeps_in_run)
# generate .txt files, fill with data
Measurements.write_all_to_file(susc_array, susc_error_array, temp_array, energy_array, mag_array, cap_array, cap_error_array, dynamics, num_sweeps_in_run)
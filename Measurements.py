import Methods
import math
import random

boltzmann = 1.0
J = -1.0

# scan over all elements; record sum of all spins
def magnetisation(state):

    mag = 0
    width = len(state)
    height = len(state[0])

    # sum spin state for magnetisation
    # iterate over all state elements
    for x_pos in range(0, width):
        for y_pos in range(0, height):
            mag += Methods.get_element(state, x_pos, y_pos)

    return float(mag)

# total energy of spin state
def energy(state):

    return Methods.state_energy(state)

# chi = (<m^2> - <m>^2) / (n*KbT)
# (replaced with bootstrap method; left here just in case)
def susceptibility(mag_array, susc_array, susc_error_array, temp_array, state, num_sweeps_in_run):

    num_sweeps = len(mag_array)
    width = len(state)
    height = len(state[0])
    n = float(width*height)

    m2_array = list()
    m_2_array = list()

    num_loops = num_sweeps / num_sweeps_in_run
    counter = 0
    for loop in range(0, num_loops):

        mag_array1 = list()
        mag_array2 = list()

        for z in range(0, num_sweeps_in_run):
            mag_array1.append(mag_array[counter])
            mag_array2.append(math.pow(mag_array[counter], 2))

            counter += 1

        # <M>^2
        M2 = sum(mag_array1) / num_sweeps_in_run
        M2 = M2 * M2
        m2_array.append(M2)

        # <M^2>
        M_2 = sum(mag_array2) / num_sweeps_in_run
        m_2_array.append(M_2)

        for z in range(0, num_sweeps_in_run):
            del mag_array1[0]
            del mag_array2[0]

    counter = 0

    for z in m2_array:

        item = (m_2_array[counter] - m2_array[counter]) / (n * boltzmann * temp_array[counter*num_sweeps_in_run])
        susc_array.append(item)

        counter += 1

def susceptibility_bootstrap(mag_array, susc_array, susc_error_array, temp_array, state, num_sweeps_in_run):

    num_sweeps = len(mag_array)
    width = len(state)
    height = len(state[0])
    n = float(width*height)

    bs_m2_array = list()
    bs_m_2_array = list()
    bs_array_1 = list()
    bs_array_2 = list()
    bs_susc_array = list()
    bs_susc2_array = list()

    num_loops = num_sweeps / num_sweeps_in_run
    counter = 0

    # loop over all temperatures
    for loop in range(0, num_loops):

        mag_array1 = list()
        mag_array2 = list()
        temperature = temp_array[counter]

        # loop over all measurements of one temperature,
        # create arrays of relevant measurements and of
        # relevant measurements squared
        for z in range(0, num_sweeps_in_run):
            mag_array1.append(mag_array[counter])
            mag_array2.append(math.pow(mag_array[counter], 2))

            counter += 1

        # bootstrap incoming
        # loop over all procured measurements
        for z in range(0, num_sweeps_in_run):
            # do a random selection for each measurement, from all measurements
            for x in range(0, num_sweeps_in_run):
                bs_array_1.append(random.choice(mag_array1))
                bs_array_2.append(random.choice(mag_array2))

            # Cv calculations as normal
            # <M>^2 _ bootstrap
            M2 = sum(bs_array_1) / num_sweeps_in_run
            M2 = M2 * M2
            bs_m2_array.append(M2)

            # <M^2> _ bootstrap
            M_2 = sum(bs_array_2) / num_sweeps_in_run
            bs_m_2_array.append(M_2)

            # calculate susceptibility for random sample
            bs_susc = (M_2 - M2) / (n * boltzmann * temperature)
            bs_susc_array.append(bs_susc)

            del bs_array_1[:]
            del bs_array_2[:]

        # <susc> from bs_susc_array
        susc = sum(bs_susc_array) / len(bs_susc_array)
        susc_array.append(susc)

        # <susc^2>
        for susc in bs_susc_array:
            bs_susc2_array.append(math.pow(susc, 2))
        susc2 = sum(bs_susc2_array) / len(bs_susc2_array)

        # error on susc = [<susc^2> - (<susc>^2)] ^ 0.5
        error = math.pow(abs((susc2 - math.pow(susc, 2))), 0.5)
        susc_error_array.append(error)

        # clean out all arrays
        del mag_array1[:]
        del mag_array2[:]
        del bs_array_1[:]
        del bs_array_2[:]
        del bs_susc_array[:]
        del bs_susc2_array[:]
        del bs_m2_array[:]
        del bs_m_2_array[:]

def heat_capacity_bootstrap(energy_array, cap_array, cap_error_array, temp_array, state, num_sweeps_in_run):

    num_sweeps = len(energy_array)
    width = len(state)
    height = len(state[0])
    n = float(width*height)

    bs_e2_array = list()
    bs_e_2_array = list()
    bs_array_1 = list()
    bs_array_2 = list()
    bs_cap_array = list()
    bs_cap2_array = list()

    num_loops = num_sweeps / num_sweeps_in_run
    counter = 0

    # loop over all temperatures
    for loop in range(0, num_loops):

        e_array1 = list()
        e_array2 = list()
        temperature = temp_array[counter]

        # loop over all measurements of one temperature,
        # create arrays of relevant measurements and of
        # relevant measurements squared
        for z in range(0, num_sweeps_in_run):
            e_array1.append(energy_array[counter])
            e_array2.append(math.pow(energy_array[counter], 2))

            counter += 1

        # bootstrap incoming
        # loop over all procured measurements
        for z in range(0, num_sweeps_in_run):
            # do a random selection for each measurement, from all measurements
            for x in range(0, num_sweeps_in_run):
                bs_array_1.append(random.choice(e_array1))
                bs_array_2.append(random.choice(e_array2))

            # Cv calculations as normal
            # <Cv>^2 _ bootstrap
            e2 = sum(bs_array_1) / num_sweeps_in_run
            e2 = e2 * e2
            bs_e2_array.append(e2)

            # <Cv^2> _ bootstrap
            e_2 = sum(bs_array_2) / num_sweeps_in_run
            bs_e_2_array.append(e_2)

            # calculate heat capacity for random sample
            bs_cap = (e_2 - e2) / (boltzmann * math.pow(temperature, 2))
            bs_cap_array.append(bs_cap)

            del bs_array_1[:]
            del bs_array_2[:]

        # <Cv> from bs_cap_array
        cap = sum(bs_cap_array) / len(bs_cap_array)
        cap_array.append(cap)

        # <Cv^2>
        for cap in bs_cap_array:
            bs_cap2_array.append(math.pow(cap, 2))
        cap2 = sum(bs_cap2_array) / len(bs_cap2_array)

        # error on susc = [<susc^2> - (<susc>^2)] ^ 0.5
        error = math.pow(abs((cap2 - math.pow(cap, 2))), 0.5)
        cap_error_array.append(error)

        # clean out all arrays
        del e_array1[:]
        del e_array2[:]
        del bs_array_1[:]
        del bs_array_2[:]
        del bs_cap_array[:]
        del bs_cap2_array[:]
        del bs_e2_array[:]
        del bs_e_2_array[:]


# Cv = (1/Kb T^2) * (<E^2> - <E>^2)
# (replaced with bootstrap method; left here just in case)
def heat_capacity(energy_array, cap_array, temp_array, state, num_sweeps_in_run):

    num_sweeps = len(energy_array)
    width = len(state)
    height = len(state[0])
    n = float(width * height)

    e2_array = list()
    e_2_array = list()

    num_loops = num_sweeps / num_sweeps_in_run
    counter = 0
    for loop in range(0, num_loops):

        energy_array2 = list()
        energy_array1 = list()

        for z in range(0, num_sweeps_in_run):
            energy_array1.append(energy_array[counter])
            energy_array2.append(math.pow(energy_array[counter], 2))

            counter += 1

        # <e>^2
        e2 = sum(energy_array1) / num_sweeps_in_run
        e2 = e2 * e2
        e2_array.append(e2)

        # <e^2>
        e_2 = sum(energy_array2) / num_sweeps_in_run
        e_2_array.append(e_2)

        for z in range(0, len(energy_array1)):
            del energy_array1[0]
            del energy_array2[0]

    counter = 0

    for z in e2_array:
        item = (e_2_array[counter] - e2_array[counter]) / (boltzmann * math.pow(temp_array[counter * num_sweeps_in_run], 2))
        cap_array.append(item)

        counter += 1

def write_all_to_file(susc_array, susc_error_array, temp_array, energy_array, mag_array, cap_array, cap_error_array, dynamics, num_sweeps_in_run):

    if dynamics == 1:

        # declare files
        temp_susc = open("temp_susceptibility_glauber.txt", "w")
        temp_mag = open("temp_magnetisation_glauber.txt", "w")
        temp_energy = open("temp_energy_glauber.txt", "w")
        temp_cap = open("temp_capacity_glauber.txt", "w")

    elif dynamics == 0:

        # declare files
        temp_susc = open("temp_susceptibility_kawasaki.txt", "w")
        temp_mag = open("temp_magnetisation_kawasaki.txt", "w")
        temp_energy = open("temp_energy_kawasaki.txt", "w")
        temp_cap = open("temp_capacity_kawasaki.txt", "w")

    # temp_susc
    count = 0
    for x in susc_array:
        y = temp_array[(count*num_sweeps_in_run)]
        z = susc_error_array[count]
        temp_susc.write('%s' % x)
        temp_susc.write(' ')
        temp_susc.write('%s' % y)
        temp_susc.write(' ')
        temp_susc.write('%s \n' % z)

        count += 1

    # temp_mag
    # NB: PRINTING ABSOLUTE VALUE OF MAGNETISATION
    count = 0
    for x in mag_array:
        y = temp_array[count]
        temp_mag.write('%s' % abs(x))
        temp_mag.write(' ')
        temp_mag.write('%s\n' % y)
        count += 1

    # temp_energy
    count = 0
    for x in energy_array:
        y = temp_array[count]
        temp_energy.write('%s' % x)
        temp_energy.write(' ')
        temp_energy.write('%s\n' % y)
        count += 1

    # temp_cap
    count = 0
    for x in cap_array:
        y = temp_array[(count*num_sweeps_in_run)]
        z = cap_error_array[count]
        temp_cap.write('%s' % x)
        temp_cap.write(' ')
        temp_cap.write('%s' % y)
        temp_cap.write(' ')
        temp_cap.write('%s\n' % z)
        count += 1

    temp_cap.close()
    temp_susc.close()
    temp_mag.close()
    temp_energy.close()

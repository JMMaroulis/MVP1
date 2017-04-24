import numpy as numpy
import random as random

# defined to stop compiler complaining; not the actual values that get used
boltzmann = 0
J = 0

def import_variables(boltzmann2, J2):
    global boltzmann, J
    boltzmann, J = boltzmann2, J2

# return energy of pair of spin elements
def spin_pair_energy(a, b):
    return a * b * -1


# state element getter to deal with looping edges
def get_element(state, element_x_pos, element_y_pos):
    width = len(state)
    height = len(state[0])
    return state[element_x_pos % width, element_y_pos % height]


# state element setter
# NOTE!!!!!
# SET_ELEMENT, AND ALL THINGS DEPENDANT ON IT (FLIP, ATTEMPT_FLIP, ETC) DON'T RETURN ANYTHING
# DUE TO ARRAY COPYING POINTER WEIRDNESS, IT WORKS
# ESSENTIALLY ACTING AS VOID METHODS
# ALL IS FINE
# NOTHING TO SEE HERE
# WE HAVE ALWAYS BEEN AT WAR WITH EURASIA, CITIZEN
def set_element(state, element_x_pos, element_y_pos, new_value):
    width = len(state)
    height = len(state[0])
    state[element_x_pos % width, element_y_pos % height] = new_value


# flips given element
# can deal with looping edges, but please don't. Be nice to the poor thing.
def flip(state, element_x_pos, element_y_pos):

    set_element(state, element_x_pos, element_y_pos, (get_element(state, element_x_pos, element_y_pos) * -1))


# calculates total energy of state
# NOTE: DOES NOT WORK WITH IRREGULAR SHAPES,
# ALL COLUMNS AND ROWS MUST BE SAME LENGTH
# (can't imagine why we'd every try something where that isn't true, but worth pointing out)
def state_energy(state):
    # Iterate over all elements,
    # determine spin pair energy of each element and the elements
    # above it and to the right of it
    energy = 0
    width = len(state)
    height = len(state[0])

    # work along x axis, do pairs with element below
    element_x_pos = 0
    element_y_pos = 0
    while element_y_pos != height:

        while element_x_pos != width:

            # add energy from spin pair
            energy += spin_pair_energy(get_element(state, element_x_pos, element_y_pos),
                                       get_element(state, element_x_pos, element_y_pos + 1))

            # increment position
            element_x_pos += 1

        element_y_pos += 1
        element_x_pos = 0

    # work along y axis, do pair with element to right
    element_x_pos = 0
    element_y_pos = 0
    while element_x_pos != width:

        while element_y_pos != height:

            # add energy from spin pair
            energy += spin_pair_energy(get_element(state, element_x_pos, element_y_pos),
                                       get_element(state, element_x_pos + 1, element_y_pos))

            # increment position
            element_y_pos += 1

        element_y_pos = 0
        element_x_pos += 1

    return energy


# energy from single spin element
def state_element_energy(state, element_x_pos, element_y_pos):
    energy = 0
    # this feels like bad coding practice, but it works and it was quick to write
    energy += spin_pair_energy(get_element(state, element_x_pos, element_y_pos), get_element(state, element_x_pos+1, element_y_pos))
    energy += spin_pair_energy(get_element(state, element_x_pos, element_y_pos), get_element(state, element_x_pos-1, element_y_pos))
    energy += spin_pair_energy(get_element(state, element_x_pos, element_y_pos), get_element(state, element_x_pos, element_y_pos+1))
    energy += spin_pair_energy(get_element(state, element_x_pos, element_y_pos), get_element(state, element_x_pos, element_y_pos-1))

    return energy


# flip attempt
# flips based on energy change requirements;
# flips if energy change negative,
# else flips with probability p = e^(-delta_E / Kb*T)
def attempt_flip(state, element_x_pos, element_y_pos, temperature):

    # determine hypothetical energy change
    energy_change = J * (2 * state_element_energy(state, element_x_pos, element_y_pos))

    # branch dependant on energy_change pos/neg
    if energy_change < 0:
        flip(state, element_x_pos, element_y_pos)

    else:
        # flip with probability
        probability_thresh = numpy.exp((-1) * energy_change/(boltzmann * temperature))
        number = random.random()
        if number <= probability_thresh:
            flip(state, element_x_pos, element_y_pos)


# update step - glauber dynamics
# 1 - random element
# 2 - attempt to flip
def update_glauber(state, temperature):

    width = len(state)
    height = len(state[0])

    # 1 - select random element
    element_x_pos = numpy.random.randint(0, width, 1, int)
    element_y_pos = numpy.random.randint(0, height, 1, int)

    # 2 - attempt to flip
    attempt_flip(state, element_x_pos, element_y_pos, temperature)


# exists as shell for iterating update_glauber n times
def update_glauber_n(state, n, temperature):
    for x in range(0, n):
        update_glauber(state, temperature)


# update step - kawasaki dynamics
# Adjacency check in attempt_exchange_kawasaki
def update_kawasaki(state, temperature):

    width = len(state)
    height = len(state[0])

    # randomly select 2 elements, ensure not the same
    element_x1_pos, element_x2_pos, element_y1_pos, element_y2_pos = 0, 0, 0, 0
    while (element_x1_pos == element_x2_pos) & (element_y1_pos == element_y2_pos):
        element_x1_pos = numpy.random.randint(0, width, 1, int)
        element_y1_pos = numpy.random.randint(0, height, 1, int)
        element_x2_pos = numpy.random.randint(0, width, 1, int)
        element_y2_pos = numpy.random.randint(0, height, 1, int)

    # exchange attempt for non adjacent elements
    # adjacency check occurs in attempt_exchange_kawasaki
    else:
        attempt_exchange_kawasaki(state, temperature, element_x1_pos, element_y1_pos, element_x2_pos, element_y2_pos)


def update_kawasaki_n(state, n, temperature):
    for x in range(0, n):
        update_kawasaki(state, temperature)


# does adjacency check is in here
# adjacency energy compensation also in here
def attempt_exchange_kawasaki(state, temperature, element_x1_pos, element_y1_pos, element_x2_pos, element_y2_pos):
    # check for element1 spin = element2 spin
    if get_element(state, element_x1_pos, element_y1_pos) == get_element(state, element_x2_pos, element_y2_pos):
        # if spins same, method does nothing
        pass

    else:

        energy_change = 0
        # check for adjacency
        if (element_x1_pos == element_x2_pos + 1) or (element_x1_pos == element_x2_pos - 1):
            if (element_y1_pos == element_y2_pos + 1) or (element_y1_pos == element_y2_pos - 1):
                # adjacent!
                # compensate for adjacency in energy_change
                energy_change -= 4 * J

        # determine hypothetical energy change
        energy_change += J * (2 * state_element_energy(state, element_x1_pos, element_y1_pos))
        energy_change += J * (2 * state_element_energy(state, element_x2_pos, element_y2_pos))

        # branch dependant on energy_change pos/neg
        if energy_change < 0:
            flip(state, element_x1_pos, element_y1_pos)
            flip(state, element_x2_pos, element_y2_pos)

        else:
            # flip with probability
            probability_thresh = numpy.exp((-1) * energy_change / (boltzmann * temperature))
            number = random.random()
            if number <= probability_thresh:
                flip(state, element_x1_pos, element_y1_pos)
                flip(state, element_x2_pos, element_y2_pos)

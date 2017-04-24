#http://stackoverflow.com/questions/7229971/2d-grid-data-visualization-in-python
#Grid Example

#Import everything of import

import matplotlib.mpl as mpl
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import numpy as numpy

# make values from -5 to 5, for this example
#100 by 100 array of numbers
zvals = numpy.random.rand(100,100)*10-5

#make a color map of fixed colors
cmap = mpl.colors.ListedColormap(['blue','black','red'])
bounds=[-6,-2,2,6]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# tell imshow about color map so that only set colors are used
img = pyplot.imshow(zvals,interpolation='nearest',
                    cmap = cmap,norm=norm)


# make a color bar
pyplot.colorbar(img,cmap=cmap,
                norm=norm,boundaries=bounds,ticks=[-5,0,5])

pyplot.show()

///////////////

#IMPLEMENT USER INPUT, determine various variables

#Defining things manually for the time being
width = 10
height = 9
temperature = 300
Kb = 1.38064852 * (10**-23)

print(Kb)

//////////////

#Random State Initialisation;
#According to temparature and such

#100 x 100 array of 0's or 1's
spins = numpy.random.randint(0, 2, (height, width), int)

print(state_energy(spins,height,width))

spins

///////////////

# Various required methods

# return energy of pair of spin elements
def spin_pair_energy(a, b):
    if a == b:
        return -1
    else:
        return 1


# CURRENTLY DOESN'T WORK FOR HEIGHT != WIDTH
# TERMINATING EACH STEP EARLY???
# energy of current state

# ABORT, TRY AGAIN WITH MODULAR ARITHMETIC

def state_energy(state, height, width):
    # Iterate over all elements,
    # determine spin pair energy of each element and the elements
    # above it and to the right of it
    energy = 0
    element_x_pos = 0
    element_y_pos = 0

    # work along x axis, do pairs with element below
    # print(element_x_pos,element_y_pos)
    while element_y_pos != height:

        while element_x_pos != width:
            print(element_x_pos, element_y_pos)

            # exception to avoid out-of-bounds errors, due to periodic boundary
            if element_y_pos == (height - 1):
                energy += spin_pair_energy(state[element_x_pos, element_y_pos], state[element_x_pos, 0])
            else:
                energy += spin_pair_energy(state[element_x_pos, element_y_pos], state[element_x_pos, element_y_pos + 1])

            # debug
            print("step1")

            # increment position
            element_x_pos += 1
        element_x_pos = 0
        element_y_pos += 1

    print("heightdone")

    # reset coordinates
    element_x_pos = 0
    element_y_pos = 0

    # work along y axis, do pairs with element to right
    while element_x_pos != width:
        while element_y_pos != height:
            print(element_x_pos, element_y_pos)

            # exception to avoid out-of-bounds errors, due to periodic boundary
            if element_x_pos == (width - 1):
                energy += spin_pair_energy(state[element_x_pos, element_y_pos], state[0, element_y_pos])
            else:
                energy += spin_pair_energy(state[element_x_pos, element_y_pos], state[element_x_pos + 1, element_y_pos])

            # debug
            print("step2")

            # increment position
            element_y_pos += 1
        element_y_pos = 0
        element_x_pos += 1

    print("widthdone")

    return energy

# energy change induced by flip
# def state_energy_change(state):

# flip attempt
# def attempt_flip(element_spin,temperature):

# update step - glauber dynamics
# def update_glauber(state,temparature):

# choose random spin element
# element = numpy.random.randint(0,99,1,int)

# attempt to flip


# update step - kawasaki dynamics
# BEWARE ACCIDENTALLY DOUBLE COUNTING IF ELEMENTS ARE ADJACENT
# def update_kawasaki(state,temperature):

///////////

#Animation

#colourmap
#colours representing spins,
#red = up, blue = down
cmap = mpl.colors.ListedColormap(['blue','red'])

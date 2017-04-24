#http://stackoverflow.com/questions/7229971/2d-grid-data-visualization-in-python
#Grid Example

#Import everything of import

import matplotlib.mpl as mpl
import matplotlib.pyplot as pyplot
import matplotlib.animation as animation
import numpy as numpy

# make values from -5 to 5, for this example
# 100 by 100 array of numbers
zvals = numpy.random.rand(100,100)*10-5

# make a color map of fixed colors
cmap = mpl.colors.ListedColormap(['blue', 'black', 'red'])
bounds=[-6,-2,2,6]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# tell imshow about color map so that only set colors are used
img = pyplot.imshow(zvals, interpolation='nearest',
                    cmap = cmap, norm=norm)


# make a color bar
pyplot.colorbar(img, cmap=cmap,
                norm=norm, boundaries=bounds, ticks=[-5, 0, 5])

pyplot.show()

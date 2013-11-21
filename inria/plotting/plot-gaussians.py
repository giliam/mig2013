#!/usr/bin/env python
# from http://matplotlib.org/mpl_examples/mplot3d/surface3d_demo.py

from math import pi, sqrt

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

####################
# xxx should use covariance matrix instead
# this code is for building illustrations only
# assuming no correlation between x and y
# i.e. sigma = ( sx**2, 0, 0, xy**2)
#    ___
# 1/V2pi
twopi_inv = 1./(2.*pi)

# X and Y are numpy arrays
def gaussian2d (X,Y,mu_x, mu_y, sigma_x, sigma_y):
    R2 = np.add(((X-mu_x)/sigma_x)**2,((Y-mu_y)/sigma_y)**2)
    return twopi_inv * (1./sigma_x*sigma_y) * np.exp(-R2/2.)


# config
# [ mu, sigma ]

# 3 outputs
gaussian_specs = [ (4.,   8., 1., 0.25),
                   (-4., -8., 1., 4.),
                   (-6.,  6., 2., 2),
                   ]
# 2 states
emission_ratios_s = [ (.1, .1, .8), 
                      (.7, .15, .15),
                    ]
# x1, x2, y1, y2, step, max_proba
grid = (-15.,15.,-15.,15.,.2, .12)

def draw_combination (gaussian_specs, weighs, grid):

    (x1,x2,y1,y2,step,max_proba) = grid

    figure3d=plt.figure()
    ax = figure3d.gca(projection='3d')
    X = np.arange(x1,x2,step)
    Y = np.arange(y1,y2,step)
    X, Y = np.meshgrid(X, Y)

    gaussians = np.array ( \
        [ gaussian2d (X,Y, mu_x, mu_y, sigma_x, sigma_y) for \
              (mu_x, mu_y, sigma_x, sigma_y) in gaussian_specs ])
    ratios = np.array(weighs)
    # at this point we have gaussians shape is O * steps * steps
    # and we cannot call dot that apparently expects dim-2 matrices
    weighed_gaussian = \
        reduce (np.add, [ grid * ratio for (ratio,grid) in \
                              zip (weighs, gaussians) ] )
                               
    surf = ax.plot_surface(X, Y, weighed_gaussian, 
                           rstride=1, cstride=1, cmap=cm.coolwarm,
                           #left=0., right=1., bottom=0., top=1.
                           linewidth=0, antialiased=False)

    ax.set_zlim(0., max_proba)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    figure3d.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def main ():
    for emission_ratios in emission_ratios_s:
        draw_combination (gaussian_specs, emission_ratios, grid)

if __name__ == '__main__':
    main()

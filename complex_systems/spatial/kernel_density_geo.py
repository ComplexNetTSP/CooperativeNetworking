#!/usr/bin/python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Copyright (c) 2012 Vincent Gauthier.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# -------------------------------------------------------------------------------

__author__ = """\n""".join(['Vincent Gauthier'])


def kernel_density_geo(X_data, Y_data, bin_size_x=10, bin_size_y=10):
    '''
    more information about the `Kernel density estimation <http://en.wikipedia.org/wiki/Kernel_density_estimation>`_
    '''
    import scipy.stats as stats
    import numpy as N
    
    #Format teh entry to make sure it is a colum vector 
    X_data = N.transpose([X_data.ravel()])
    Y_data = N.transpose([Y_data.ravel()])
    pos = N.append(X_data,Y_data,axis=1)

    kde = stats.kde.gaussian_kde(pos.T)

    X_flat = N.linspace(pos[:,0].min(),pos[:,0].max(),bin_size_x)
    Y_flat = N.linspace(pos[:,1].min(),pos[:,1].max(),bin_size_y)

    X,Y = N.meshgrid(X_flat,Y_flat)
    
    grid_coords =N.append(X.reshape(-1,1),Y.reshape(-1,1),axis=1)
    Z = kde(grid_coords.T)
    Z = Z.reshape(bin_size_x,bin_size_y)

    return grid_coords,Z
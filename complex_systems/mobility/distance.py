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
#-------------------------------------------------------------------------------

__author__ = """\n""".join(['Vincent Gauthier <vgauthier@luxbulb.org>'])

__all__ = ['distance']


def distance(X,Y):
    '''
    Calculate the Euclidian distance between coordinates at differents step in time
    
    .. math::
        dist_{i+1} = Distance( (x_i,y_i), (x_{i+1},y_{i+1}) ) \\ \\forall i
        
    :Example:
    >>> from complex_systems.mobility.levy_flight import *
    >>> X = [0,0,0]
    >>> Y = [1,2,3]
    >>> distance(X,Y)
    [1.0,1.0]

    :Parameters:
    - `X`: list(float)
        X coordinates     
    - `Y`: list(float)
        Y coordinates
    
    :Returns:
    - `dist` : list
            Euclidian distance
    '''
    import numpy as N
    dist = [N.sqrt(float((X[t+1] - X[t]) ** 2 + (Y[t+1] - Y[t]) ** 2)) for t in range(len(X)-1)]
    return dist
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

__author__ = """\n""".join(['Vincent Gauthier <vgauthier@luxbulb.org>'])

__all__ = ['levy_walk']


def levy_walk(
    alpha,
    beta,
    sample_length,
    size_max,
    velocity,
    f_min,
    f_max,
    s_min,
    s_max,
    duration=90000,
    b_c=1,
    ):
    '''
    This code is based on the following paper:
    
    .. [Rhee08] Injong Rhee, Minsu Shin, Seongik Hong, Kyunghan Lee and Song Chong, "On the Levy-walk Nature of Human Mobility", INFOCOM, Arizona, USA, 2008
    
    .. note::
    
        :Levy Flight or Levy Walk model:
          
          The Levy Walk generalize the concept of random walker with jump length distribution :math:`p(\\Delta x)` and 
          and waitting time distribution :math:`p(\\Delta t)` for waitting ting time :math:`\\Delta t_i` and jump length :math:`\\Delta x_i` 
          at evry steps :math:`i = 1, 2, ..., n` of the walk.
          
          .. math::
              p(\\Delta x) \\sim \\frac{1}{(\\Delta x)^{1+\\alpha} },\\ \\ \\ p(\\Delta t) \\sim \\frac{1}{(\\Delta t)^{1+\\beta} }, \\ \\alpha , \\beta > 0
    
    
    :Example:
    >>> from complex_systems.mobility.levy_walk import *
    >>> levy_walk(alpha=0.66, beta=0.99, sample_length=1, size_max=83000, velocity=1.0, f_min=8, f_max=83000, s_min=0.8, s_max=430, duration=500, b_c=2)
    
    :Parameters:
    - `alpha` : float 
        Levy exponent for flight length distribution, 0 < alpha <= 2
    - `beta`  : float 
        Levy exponent for pause time distribution, 0 < beta <= 2
    - `sample_length` : int
        Sample time in mins
    - `size_max` : int 
        size of simulation area
    - `velocity` : float
        speed in m/s
    - `f_min` : int
        min flight length
    - `f_max` : int
        max flight length
    - `s_min` : int 
        min pause time (second)
    - `s_max` : int  
        max pause time (second)
    - `duration` : int 
        simulation duration (minutes)
    - `b_c` : int 
        boundary condition: 
            - wrap-around if b_c=1
            - reflection boundary if b_c=2
    
    :Returns: 
    - `un_sampled` :  list(tulpe(X, Y, T))
        - `X` : list(int) 
            list of X location 
        - `Y` : list(int) 
            list of Y location
        - `T` : list(float) 
            time in seconds
    - `A` : list(int)
        list of jump length
    - `B` : list(int)
        list of pause time length
    - `sampled` :  list(tulpe(X_sampled, Y_sampled, T_sampled))
        - `X_sampled`
            list of X location at sampled intervals
        - `Y_sampled` 
            list of Y location at sampled intervals
        - `T_sampled`
            list of sampled intervals
    '''

    import stabrnd as R
    import numpy as N

    # Pause Time scale parameter

    pt_scale = 1.0

    # Flight Length scale parameter

    fl_scale = 10.0

    # DEBUG

    DEBUG = False

    delta = 0.0

    # Velocity in meter per mins

    velocity = velocity
    if DEBUG:
        print 'velocity (m/mins): ', velocity

    num_step = int(N.ceil(float(duration) / sample_length))
    num_step_gen = 10*int(N.ceil(float(duration) / s_min))

    if DEBUG:
        print 'num steps: ', num_step

    # Constant speed

    mu = 0.0

    # Bounds of the simulation area

    max_x = size_max
    max_y = size_max

    A = []
    B = []
    x = [0] * (num_step_gen + 1)
    y = [0] * (num_step_gen + 1)
    t = [0] * (num_step_gen + 1)
    x_sampled = [0] * (num_step_gen)
    y_sampled = [0] * (num_step_gen)
    t_sampled = [0] * (num_step_gen)
    dist = [0] * num_step_gen

    if alpha < .1 or alpha > 2:
        raise ValueError('Alpha must be in [.1,2] for function stabrnd.'
                         )

    if beta < .1 or beta > 2:
        raise ValueError('Beta must be in [.1,2] for function stabrnd.')

    # Generate flight length

    while len(A) < num_step_gen:
        A_temp = N.abs(R.stabrnd(
            alpha,
            0,
            fl_scale,
            delta,
            num_step,
            1,
            ))
        A_temp = A_temp[A_temp > f_min]
        A_temp = A_temp[A_temp < f_max]
        A = N.append(A, A_temp)

    A = N.round(A[0:num_step_gen])

    # Generate pause time

    while len(B) < num_step_gen:
        B_temp = N.abs(R.stabrnd(
            beta,
            0,
            pt_scale,
            0,
            num_step,
            1,
            ))
        B_temp = B_temp[B_temp > s_min]
        B_temp = B_temp[B_temp < s_max]
        B = N.append(B, B_temp)

    B = N.round(B[0:num_step_gen])

    # Initial Step

    x[0] = max_x * N.random.rand()
    y[0] = max_y * N.random.rand()
    if DEBUG:
        print x[0], y[0]
    t[0] = 0
    x_sampled[0] = x[0]
    y_sampled[0] = y[0]
    j = 1

    for i in N.arange(1, num_step_gen, 2):
        theta = 2 * N.pi * N.random.rand()
        next_x = N.round(x[i - 1] + A[i] * N.cos(theta))
        next_y = N.round(y[i - 1] + A[i] * N.sin(theta))
        if b_c == 1:
            # Boundary of the simulation Area
            # Wrap around
            if next_x < 0:
                x[i] = max_x + next_x
            elif next_x > max_x:
                x[i] = next_x - max_x
            else:
                x[i] = next_x

            if next_y < 0:
                y[i] = max_y + next_y
            elif next_y > max_y:
                y[i] = next_y - max_y
            else:
                y[i] = next_y
        elif b_c == 2:
            # Boundary of the simulation Area
            # Reflection
            if next_x < 0:
                x[i] = -next_x
            elif next_x > max_x:
                x[i] = max_x - (next_x - max_x)
            else:
                x[i] = next_x

            if next_y < 0:
                y[i] = -next_y
            elif next_y > max_y:
                y[i] = max_y - (next_y - max_y)
            else:
                y[i] = next_y
            # end of boundary

        dist[i] = N.sqrt(float((next_x - x[i - 1]) ** 2 + (next_y - y[i
                         - 1]) ** 2))
        t[i] = t[i - 1] + N.power(float(dist[i]) / velocity, 1 - mu)
        t[i + 1] = t[i] + N.abs(B[i])
        x[i + 1] = x[i]
        y[i + 1] = y[i]

        while (j * sample_length) < t[i + 1]:

            if j * sample_length < t[i]:
                p_ratio = ((j * sample_length)- t[i-1]) / (t[i] - t[i - 1])
                x_sampled[j] = next_x * p_ratio + x[i - 1] * (1 - p_ratio)
                y_sampled[j] = next_y * p_ratio + y[i - 1] * (1 - p_ratio)
                t_sampled[j] = j * sample_length
                if b_c == 1:
                    # Boundary wrap around
                    if x_sampled[j] < 0:    
                        x_sampled[j] = max_x + x_sampled[j]
                    elif x_sampled[j] > max_x:
                        x_sampled[j] = next_x - max_x
                    if y_sampled[j] < 0:
                        y_sampled[j] = max_y + y_sampled[j]
                    elif y_sampled[j] > max_y:
                        y_sampled[j] = next_y - max_y
                elif b_c == 2:
                    # Boundary Reflection
                    if x_sampled[j] < 0:
                        x_sampled[j] = -x_sampled[j]
                    elif x_sampled[j] > max_x:
                        x_sampled[j] = max_x - (x_sampled[j] - max_x)
                    if y_sampled[j] < 0:
                        y_sampled[j] = -y_sampled[j]
                    elif y_sampled[j] > max_y:
                        y_sampled[j] = max_y - (y_sampled[j] - max_y)
            else:
                x_sampled[j] = x[i]
                y_sampled[j] = y[i]
                t_sampled[j] = j * sample_length
            
            j += 1

        if t[i+1] > duration:
            break

    if DEBUG:
        print 'Simulation length : ', len(x)

    X = N.round(x[0:i])
    Y = N.round(y[0:i])
    T = t[0:i]
    X_sampled = N.round(x_sampled[0:num_step])
    Y_sampled = N.round(y_sampled[0:num_step])
    T_sampled = t_sampled[0:num_step]
    un_sampled = zip(X,Y,T)
    sampled = zip(X_sampled, Y_sampled, T_sampled)
    return (un_sampled, A, B, sampled)

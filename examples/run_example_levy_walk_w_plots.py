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

__all__ = ['test_levy_walk_w_plots']


def run_example_levy_walk_w_plots():
    import numpy as N
    import pylab as plt
    from scikits.statsmodels.tools.tools import ECDF

    from complex_systems.mobility.levy_walk import levy_walk
    from complex_systems.mobility.distance import distance

    alpha = 0.9
    beta = 0.9
    f_min = 1.0
    f_max = 100.0
    s_min = 1.0
    s_max = 100.0
    velocity = 5.0

    (un_sampled, A, B, sampled) = levy_walk(
        alpha=alpha,
        beta=beta,
        sample_length=10.0,
        size_max=10000,
        velocity=velocity,
        f_min=f_min,
        f_max=f_max,
        s_min=s_min,
        s_max=s_max,
        duration=1000,
        b_c=2,
        )

    (X, Y, T) = zip(*un_sampled)
    (X_sampled, Y_sampled, T_sampled) = zip(*sampled)
    print T_sampled, X_sampled, Y_sampled

    plt.figure()
    plt.plot(X_sampled, Y_sampled, 'ro-')
    plt.plot(X, Y, 'o-')

    ecdf = ECDF(A)
    x = N.linspace(min(A), max(A))
    y = 1 - ecdf(x)

    ax1 = plt.subplot(121)
    plt.loglog(x, y, 'r', linewidth=2.0)
    plt.xlim(1, max(A))
    plt.ylim(min(y), max(y))
    plt.grid(True, which='both')
    plt.xlabel('Distance [m]')
    plt.ylabel('P(X > x)')

    ecdf = ECDF(B)
    x = N.linspace(min(B), max(B))
    y = 1 - ecdf(x)
    ax2 = plt.subplot(122, sharey=ax1)
    plt.setp( ax2.get_yticklabels(), visible=False)
    plt.loglog(x, y, 'r', linewidth=2.0)
    plt.xlim(1, max(B))
    plt.ylim(min(y), max(y))
    plt.grid(True, which='both')
    plt.xlabel('Pause Time [mins]')
    plt.savefig('levywalk.pdf')
    plt.savefig('levywalk.eps')
    #plt.ylabel('P(X > x)')

    D = distance(X, Y)
    D_sampled = distance(X_sampled, Y_sampled)
    Dcumsum = N.cumsum(D)
    Dcumsum_sampled = N.cumsum(D_sampled)

    plt.figure()
    plt.plot(T[0:len(D)], Dcumsum, 'o-r', linewidth=2.0)
    plt.plot(T_sampled[0:len(Dcumsum_sampled)], Dcumsum_sampled, 'o-',
             linewidth=2.0)
    plt.ylabel('Cumulative distance traveled by the random walker (meters)'
               )
    plt.xlabel('Time (mins)')
    plt.show()


if __name__ == '__main__':
    run_example_levy_walk_w_plots()

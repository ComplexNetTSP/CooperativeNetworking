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

__all__ = ['test_levy_walk']

from complex_systems.mobility.levy_walk import levy_walk
import unittest
import logging
import sys


class test_levy_walk(unittest.TestCase):

    def setUp(self):
        pass

    def test_levy_walk(self):
        (un_sample, A, B, sample) = levy_walk(
            alpha=0.66,
            beta=0.99,
            sample_length=10,
            size_max=83000,
            velocity=1.0,
            f_min=8,
            f_max=83000,
            s_min=0.8,
            s_max=430,
            duration=1000,
            b_c=2,
            )
        
        (un_sample, A, B, sample) = levy_walk(
            alpha=0.66,
            beta=0.99,
            sample_length=10,
            size_max=83000,
            velocity=1.0,
            f_min=8,
            f_max=83000,
            s_min=0.8,
            s_max=430,
            duration=1000,
            b_c=1,
            )

    def test_levy_walk_bad_parameter_alpha(self):
        self.assertRaises(
            ValueError,
            levy_walk,
            alpha=-1,
            beta=0.99,
            sample_length=1,
            size_max=83000,
            velocity=1.0,
            f_min=8,
            f_max=83000,
            s_min=0.8,
            s_max=430,
            duration=500,
            b_c=2,
            )

        self.assertRaises(
            ValueError,
            levy_walk,
            alpha=3,
            beta=0.99,
            sample_length=1,
            size_max=83000,
            velocity=1.0,
            f_min=8,
            f_max=83000,
            s_min=0.8,
            s_max=430,
            duration=500,
            b_c=2,
            )

    def test_levy_walk_bad_parameter_beta(self):
        self.assertRaises(
            ValueError,
            levy_walk,
            alpha=1,
            beta=-1,
            sample_length=1,
            size_max=83000,
            velocity=1.0,
            f_min=8,
            f_max=83000,
            s_min=0.8,
            s_max=430,
            duration=500,
            b_c=2,
            )

        self.assertRaises(
            ValueError,
            levy_walk,
            alpha=1,
            beta=3,
            sample_length=1,
            size_max=83000,
            velocity=1.0,
            f_min=8,
            f_max=83000,
            s_min=0.8,
            s_max=430,
            duration=500,
            b_c=2,
            )

    def test_levy_walk_return_sample_length(self):
        import numpy as N
        duration = 1000.0
        sample_length = 10.0
        test_len = 10
        for i in range(test_len):
            (un_sample, A, B, sample) = levy_walk(
                alpha=0.66,
                beta=0.99,
                sample_length=sample_length,
                size_max=83000,
                velocity=1.0,
                f_min=8,
                f_max=83000,
                s_min=0.8,
                s_max=430,
                duration=duration,
                b_c=2,
                )
            (X,Y,T) = zip(*sample)
            print 'NB SAMPLE', int(N.ceil(duration/sample_length)), len(set(T))
            self.assertEqual(N.ceil(duration/sample_length), len(list(set(T))))



if __name__ == '__main__':
    unittest.main()

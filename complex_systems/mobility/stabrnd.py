#-------------------------------------------------------------------------------
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

__all__ = ['stabrnd']


def stabrnd(alpha, beta, c, delta, m, n):
    '''
    Stable Random Number Generator (McCulloch 12/18/96) based on the paper [Cha71]_
    
    Returns m x n matrix of iid stable random numbers with characteristic
    exponent alpha in [.1,2], skewness parameter beta in [-1,1], scale c > 0,
    and location parameter delta. Based on the method of [Cha71]_ .

     .. [Cha71] J.M. Chambers, C. L. Mallows and B. W.Stuck, "A Method for Simulating Stable Random Variables," JASA 71 (1976): 340-4.
 
    :History of this Code:
    - Encoded in MATLAB by J. Huston McCulloch, Ohio State University Econ. Dept. (mcculloch.2@osu.edu).
    - Encoded in Python by V. Gauthier, Telecom SudParis, CNRS Lab (vgauthier@luxbulb.org)
    
    :Parameters:
    - `alpha` : float
        Characteristic exponent in [.1,2]
    - `beta` : float
        Skewness in [-1,1]
    - `c` : float
        Scale c > 0
    - `delta` : float
        Location parameter
    - `m, n` : int 
        Dimension of the matrix resultat
    
    :Returns:
    - `x` : matrix
    
    
    .. note:: The CMS method is applied in such a way that x will have the log characteristic function
    
        .. math::
            \\log E \\cdot e^{(ixt)} = i \\Delta t + \\psi( c \\cdot t ),
    
        where
        
        .. math::
            \\psi(t) = -|t|^{\\alpha} \\cdot [ 1 - i\\beta \\cdot sign(t) \\cdot \\tan(\\pi \\alpha/2) ],\\ for\\ \\alpha \\neq 1
        
        .. math::        
            \\psi(t) = -|t| \\cdot [1 + i \\beta (2 \\pi) \\cdot sign(t) \\cdot \\log |t| ],\\ for\\ \\alpha = 1.
    
        With this parameterization, the stable cdf, see [Mcc96]_ for details.
        
        .. math::
            S(x; \\alpha, \\beta,c, \\delta) = S((x-\\delta)/c; \\alpha, \\beta, 1, 0).  
     
        When :math:`\\alpha = 2`:, the distribution is Gaussian with mean delta and variance :math:`2 c^2`, and beta has no effect.
     
        When :math:`\\alpha > 1`, the mean is delta for all :math:`\\beta`.  
        
        When :math:`\\alpha <= 1`, the mean is undefined.
     
        When :math:`\\beta = 0`, the distribution is symmetrical and delta is the median for all :math:`\\alpha`.  
        
        When :math:`\\alpha = 1` and :math:`\\beta = 0`, the distribution is Cauchy (arctangent) with median :math:`\\delta`.
        
        When the submitted :math:`\\alpha` is > 2 or < .1, or :math:`\\beta` is outside [-1,1], an
        error message is generated and x is returned as a matrix of NaNs.
         
        :math:`\\alpha < 0.1` is not allowed here because of the non-negligible probability of overflows.
    
        If you're only interested in the symmetric cases, you may just set :math:`\\beta = 0`
        and skip the following considerations:
     
        When :math:`\\beta > 0, (< 0)`, the distribution is skewed to the right (left).
    
        When :math:`\\alpha < 1, \\delta`, as defined above, is the unique fractile that is
        invariant under averaging of iid contributions. I call such a fractile a
        "focus of stability."  This, like the mean, is a natural location parameter.
     
        When :math:`\\alpha = 1`, either every fractile is a focus of stability, as in the
        :math:`\\beta = 0` Cauchy case, or else there is no focus of stability at all, as is
        the case for :math:`\\beta ~= 0`.  In the latter cases, which I call "afocal," delta is
        just an arbitrary fractile that has a simple relation to the c.f.
    
        When :math:`\\alpha > 1 and \\beta > 0`, med(x) must lie very far below the mean as
        alpha approaches 1 from above. Furthermore, asalpha approaches 1 from below,
        med(x) must lie very far above the focus of stability when :math:`\\beta > 0`. If :math:`\\beta
        ~= 0`, there is therefore a discontinuity in the distribution as a function
        of alpha as alpha passes 1, when delta is held constant. CMS, following an
        insight of Vladimir Zolotarev, remove this discontinuity by subtracting:
        
        .. math::      
            \\beta \\cdot c \\cdot \\tan(\\pi \\cdot \\alpha/2)
              
       
        in their program RSTAB, a.k.a. RNSTA in IMSL (formerly GGSTA). The result is
        a random number whose distribution is a continuous function of alpha, but
        whose location parameter (which I call zeta) is a shifted version of delta
        that has no known interpretation other than computational convenience.
       
        The present program restores the more meaningful :math:`\\delta` parameterization by
        using the CMS (4.1), but with :math:`\\beta \\cdot c \\cdot tan(\\pi \\alpha/2)` added back in (ie with
        their initial :math:`tan(\\alpha \\phi_0)` deleted). RNSTA therefore gives different
        results than the present program when :math:`\\beta ~= 0`.  However, the present beta
        is equivalent to the CMS beta' (BPRIME).
     
        Rather than using the CMS D2 and exp2 functions to compensate for the ill-
        condition of the CMS (4.1) when :math:`\\alpha` is very near 1, the present program
        merely fudges these cases by computing :math:`x` from their (2.4) and adjusting for
        :math:`\\beta \\cdot c \\cdot tan(\\pi \\alpha/2)` when alpha is within 1.e-8 of 1. This should make no
        difference for simulation results with samples of size less than
        approximately 10^8, and then only when the desired alpha is within 1.e-8 of
        1, but not equal to 1.
    
        The frequently used Gaussian and symmetric cases are coded
        separately so as to speed up execution.
        
        **References**
            .. [Mcc96] J.H. McCulloch, "On the parametrization of the afocal stable distributions," Bull. London Math. Soc. 28 (1996): 651-55, 
            .. [Zov86] V.M. Zolotarev, "One Dimensional Stable Laws," Amer. Math. Soc., 1986.
            .. [Sam94] G. Samorodnitsky and M.S. Taqqu, "Stable Non-Gaussian Random Processes," Chapman & Hill, 1994.
            .. [Jan94] A. Janicki and A. Weron, "Simulaton and Chaotic Behavior of Alpha-Stable Stochastic Processes," Dekker, 1994.
            .. [Mcc97] J.H. McCulloch, "Financial Applications of Stable Distributons," Handbook of Statistics, Vol. 14, 1997.
    '''
    
    import numpy as N
    import numpy.random as R

    # Error traps
    if alpha < .1 or alpha > 2 :
        print 'Alpha must be in [.1,2] for function stabrnd.'
        x = N.nan * N.zeros((n,m))
        return x

    if N.abs(beta) > 1 :
        print 'Beta must be in [-1,1] for function stabrnd.'
        x = N.nan * N.zeros((n,m))
        return x

    # Generate exponential w and uniform phi:
    w = -N.log(R.rand(m,n))
    phi = (R.rand(m,n) - 0.5) * N.pi

    # Gaussian case (Box-Muller):
    if alpha == 2:
        x = (2*N.sqrt(w) * N.sin(phi))
        x = delta + c*x
        return x

    # Symmetrical cases:
    if beta == 0:
        if alpha == 1:   # Cauchy case
            x = N.tan(phi)
        else:
            x = ((N.cos((1-alpha)*phi) / w) ** (1/alpha - 1) * N.sin(alpha * phi) / N.cos(phi) ** (1/alpha))
    # General cases:
    else:
        cosphi = N.cos(phi)
        if N.abs(alpha-1) > 1.e-8:
            zeta = beta * N.tan(N.pi*alpha/2)
            aphi = alpha * phi
            a1phi = (1 - alpha) * phi
            x = ((N.sin(aphi) + zeta * N.cos(aphi)) / cosphi)  * ((N.cos(a1phi) + zeta * N.sin(a1phi)) / (w * cosphi)) ** ((1-alpha)/alpha)
        else:
            bphi = (N.pi/2) + beta * phi
            x = (2/N.pi) * (bphi * N.tan(phi) - beta * N.log((N.pi/2) * w * cosphi / bphi))
            if alpha != 1:
                x = x + beta * N.tan(N.pi * alpha/2)

    # Finale
    x = delta + c * x
    return x

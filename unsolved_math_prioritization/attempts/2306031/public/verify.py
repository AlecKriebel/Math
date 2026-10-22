#!/usr/bin/env python3
"""Finite controls for Function Theory 6.31 partial results; no asymptotic proof.
Python 3.10+, standard library only. No network, randomness, or source files.
Hard limits: n<=256, 256 angular samples, degree<=36 rational polynomials.
"""
import cmath
import json
import math
from fractions import Fraction as Q
from pathlib import Path


def kernel_sum(n, theta):
    q = cmath.exp(-1j*theta)
    return 1/n + 2/n**2*sum((n-j)*q**j for j in range(1,n))


def kernel_closed(n, theta):
    q = cmath.exp(-1j*theta)
    return (1+q)/(n*(1-q))-2*q*(1-q**n)/(n*n*(1-q)**2)


def conv(x,y):
    out=[Q(0)]*(len(x)+len(y)-1)
    for i,a in enumerate(x):
        for j,b in enumerate(y): out[i+j]+=a*b
    return out


def run():
    exact_checks=0
    # Rational coefficient convolution, all coefficients and tested moments exact.
    b=[Q(1),Q(1,3),Q(-1,7),Q(2,11),Q(-1,13)]
    lam=sum(b)
    M1=sum(j*abs(t) for j,t in enumerate(b))
    M=sum(j*t for j,t in enumerate(b))
    coeff=conv([Q(0)]+[Q(j) for j in range(1,33)],b)
    for n in range(1,33):
        lhs=coeff[n]/n
        rhs=sum((1-Q(j,n))*b[j] for j in range(min(n,len(b))))
        assert lhs==rhs
        assert abs(lhs-lam)<=M1/n
        exact_checks+=2
        if n>=len(b):
            assert lhs==lam-M/n
            exact_checks+=1
    # Exact rational family and cancellation at c=1/2, delta=2.
    for c in (Q(1,5),Q(1,2),Q(4,5),Q(1)):
        for n in range(1,65):
            assert (c*n+1-c)/n-c==(1-c)/n
            exact_checks+=1
        for s in (Q(1,2),Q(1,10),Q(1,100)):
            r=1-s
            f=c*r/s**2+(1-c)*r/s
            assert s*s*f==c+(1-2*c)*s-(1-c)*s*s
            exact_checks+=1
            if c==Q(1,2):
                assert s*s*f-Q(1,2)==-s*s/2
                exact_checks+=1
    # Polynomial identity for derivative of the deliberately NONunivalent control.
    for u in (Q(1,100),Q(1,2),Q(2)):
        numerator=lambda x:(1+x)**4+2*u*x*(1-x)**3
        assert numerator(Q(-1))==-16*u and numerator(Q(0))==1
        exact_checks+=2
    # Numerical controls for identities and pointwise kernel inequalities.
    ns=(1,2,3,5,16,64,256)
    thetas=[-math.pi+2*math.pi*(j+0.5)/256 for j in range(256)]
    max_identity_error=0.0
    max_fejer_error=0.0
    kernel_checks=0
    for n in ns:
        assert abs(kernel_sum(n,0)-1)<1e-13
        for theta in thetas:
            K=kernel_sum(n,theta)
            C=kernel_closed(n,theta)
            max_identity_error=max(max_identity_error,abs(K-C))
            q=cmath.exp(1j*theta)
            fejer=abs(sum(q**j for j in range(n)))**2/n**2
            max_fejer_error=max(max_fejer_error,abs(K.real-fejer))
            assert abs(K-C)<1e-10
            assert abs(K.real-fejer)<1e-10
            assert abs(K)<=1+1e-10
            assert abs(K)<=min(1,3*math.pi/(n*abs(theta)))+1e-10
            assert K.real>=-1e-10
            assert K.real<=min(1,math.pi**2/(n*n*theta**2))+1e-10
            kernel_checks+=6
    # Check the exact shell-sum inequality used in the moment criterion.
    for s in (0.25,0.5,0.75,1.0):
        for n in range(1,257):
            for j in (1,max(1,n//2),n,n+1,2*n):
                assert min(1,j/n)<=(j/n)**s+1e-14
    # Finite positive measures: p=(1-z)^2f' has positive real part.
    measures=[[(0.,.4),(.7,.6)],[(0.,.4),(.7,.3),(-.7,.3)],[(0.,1.)]]
    positive_checks=0
    minimum_positive_real=1.0
    for mu in measures:
        for radius in (.0,.25,.75,.95):
            for j in range(64):
                z=radius*cmath.exp(2j*math.pi*j/64)
                p=sum(w*(1+cmath.exp(-1j*theta)*z)/(1-cmath.exp(-1j*theta)*z) for theta,w in mu)
                assert p.real>0
                minimum_positive_real=min(minimum_positive_real,p.real)
                positive_checks+=1
    return {
        'status':'passed',
        'exact_rational_checks':exact_checks,
        'kernel_inequality_checks':kernel_checks,
        'positive_real_part_samples':positive_checks,
        'max_kernel_identity_error':max_identity_error,
        'max_fejer_identity_error':max_fejer_error,
        'minimum_sampled_positive_real_part':minimum_positive_real,
        'limits':{'maximum_n':256,'angular_grid_size':256,'floating_tolerance':1e-10,'network_access':False,'random_sampling':False},
        'scope':'Finite identities and sampled inequalities only; not a proof of univalence, asymptotic rates, novelty, or the full problem.'
    }

if __name__=='__main__':
    result=run()
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    Path(__file__).with_name('CONTROL_RESULTS.json').write_text(text)
    print(text,end='')

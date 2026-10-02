#!/usr/bin/env python3
"""Exact controls for Turn 3; no numerical Helmholtz or Gaussian-integration claim."""
from fractions import Fraction as Q
from math import comb
import json

count=0
def check(v):
    global count
    assert v
    count+=1

# For a centered law, direct averaging of monomials equals their even Taylor sum.
# This finite two-point family is an algebraic moment control, not the Gaussian law.
for den in range(2,23):
    for num in range(1,den):
        theta=Q(num,den); delta=1-theta
        for x in (Q(-2,7),Q(0),Q(3,11)):
            t=delta/4
            for n in range(13):
                avg=((theta*x+t)**n+(theta*x-t)**n)/2
                tay=sum(Q(comb(n,j))*(theta*x)**(n-j)*t**j for j in range(0,n+1,2))
                check(avg==tay)
        # Explicit perturbation constants used in the reused Schur estimate.
        for l in (16,32,64,128):
            eps=delta/l; q=eps/(delta-3*eps)
            check(q<=Q(1,13))
            beta=theta+2*eps
            check(beta/(1-2*eps)<=1-3*delta/4)
            check(delta-3*eps>=13*delta/16)
        # First derivatives of g and its exact cocycle through degree four.
        for c,d in ((Q(1,3),Q(-1,5)),(Q(-2,7),Q(3,11))):
            def expo(C,D):
                return [Q(1),C,D+C*C/2,C*D+C**3/6,D*D/2+C*C*D/2+C**4/24]
            gc=c/delta; gd=d/(1-theta*theta)
            g=expo(gc,gd); a=expo(c,d)
            for n in range(5):
                check(g[n]==sum(a[j]*g[n-j]*theta**(n-j) for j in range(n+1)))
            check(2*g[2]==c*c/delta**2+2*d/(1-theta*theta))

# Moment recurrences from exact integration by parts, represented algebraically.
# Let b=2rh exp(-r^2/(2h))/Z; then m2=h-b and m4=3h*m2-r^2*b.
# Only pairs giving a nonnegative m4 are tested, as is true for the integral.
for rden in range(2,25):
    r=Q(1,rden)
    for hden in range(2,30):
        h=r*r/hden
        for bden in range(2,19):
            b=h*3*h/(r*r+3*h)/bden
            m2=h-b; m4=3*h*m2-r*r*b
            check(0<=m2<=h)
            check(0<=m4<=3*h*h)

print(json.dumps({'status':'PASS','assertions':count,'coverage':['centered even-moment Taylor identities','Schur spectral-gap constants','analytic exponential-weight cocycle and first correction','integration-by-parts moment inequalities'],'scope':'Finite exact controls only; analytic estimates are proved in TURN_3.md; no physical PDE identification.'},sort_keys=True,indent=2))

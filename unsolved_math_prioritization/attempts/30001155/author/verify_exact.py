#!/usr/bin/env python3
"""Exact rational controls for the authored special-case proofs. No external data."""
from fractions import Fraction as F
from math import factorial, comb
import json
from pathlib import Path
NASSERT=0
def check(x):
 global NASSERT
 NASSERT+=1
 assert x

def bessel_sum(n,x,m):
 t=x*x/4
 return (x/2)**n*sum(F((-1)**k)*t**k/F(factorial(k)*factorial(k+n)) for k in range(m+1))
def bounds(n,x):
 # After k=1 terms decrease at all x used; odd/even truncations enclose.
 check(x*x/4 < F(2*(n+2)))
 return bessel_sum(n,x,15),bessel_sum(n,x,16)

# J1>0 on 0<x<=2.41 follows from (x/2)(1-x^2/8)>0.
check(F(241,100)**2<8)
for n,x,sgn in [(0,F(12,5),1),(0,F(241,100),-1),(1,F(383,100),1),(1,F(96,25),-1)]:
 lo,hi=bounds(n,x);check(lo<=hi);check(lo>0 if sgn>0 else hi<0)
# J0 upper alternating truncation P8 negative on [2.41,3.84].
p=[F((-1)**k,factorial(k)**2) for k in range(9)]
a=F(241,100)**2/4;b=F(96,25)**2/4;n=8
c=[sum(p[k]*comb(k,j)*a**(k-j)*(b-a)**j for k in range(j,n+1)) for j in range(n+1)]
beta=[sum(c[j]*F(comb(i,j),comb(n,j)) for j in range(i+1)) for i in range(n+1)]
for z in beta:check(z<0)
# Thus j01 in (2.4,2.41), j11 in (3.83,3.84); ODE zero-crossing argument in proof.
xlo=F(12,5)**2;xhi=F(241,100)**2;ylo=F(383,100)**2;yhi=F(96,25)**2
Dlo=ylo-xhi;Dhi=yhi-xlo
pilo=F(157,50);pihi=F(22,7)
check(Dlo>3*pihi*pihi/4)
check(Dhi<3*pilo*pilo/2)
# 0<theta<1/2, pi^2>8 suffice for all rectangles and triangle comparison.
check(pilo*pilo>8)
# Rigorous ellipse certificate for u=sqrt(1-(b/a)^2)<=1/4.
thhi=1-3*pilo*pilo/(4*Dhi)
ellipse_margin=Dlo-3*pihi*pihi/4-3*pihi*pihi*xhi/(16*Dlo)-thhi*yhi/16
check(ellipse_margin>0)
check(ellipse_margin==F(273124119,3618160000))
# Exact Bernstein enclosure sanity: endpoints of transformed polynomial.
check(beta[0]==sum(p[k]*a**k for k in range(9)))
check(beta[-1]==sum(p[k]*b**k for k in range(9)))
# Rectangular sufficient coefficient, uniformly r in (0,1].
check(8/(pilo*pilo)<1)
for k in range(1,1001):
 r=F(k,1000);q2=16*r*r/(pilo*pilo*(1+r*r)**2)
 check(q2<1)
 check(q2/2<r*r/(1+r*r))
# Triangle theorem threshold: F(q)<=4 Delta<6 pi^2<64 pi^2/9.
check(F(6)<F(64,9))
result={'status':'PASS','assertions':NASSERT,'arithmetic':'fractions.Fraction (exact)','bessel_root_brackets':{'j01':['12/5','241/100'],'j11':['383/100','96/25']},'ellipse_u_max':'1/4','ellipse_axis_ratio_min':'sqrt(15)/4','ellipse_margin_lower_bound':str(ellipse_margin),'bernstein_coefficients':[str(x) for x in beta], 'scope':'Controls support analytic special-case proofs; no unrestricted conjecture proof.'}
print(json.dumps(result,indent=2))

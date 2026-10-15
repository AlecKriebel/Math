#!/usr/bin/env python3
"""Independent exact checks of scope-sensitive algebra. Prints only; no writes."""
from fractions import Fraction as F
from math import isqrt
import json

def phi_poly(p):
    # integral x * p(x) on [-1/2,1/2]
    return sum((c * F(1,2**(k+1)*(k+2)) for k,c in enumerate(p) if k%2),F(0))

f=[F(0),F(-3,20),F(0),F(1)]
p0f=[F(0),F(3,160),F(0),F(1,8)]
assert phi_poly(f)==0
assert phi_poly(p0f)==F(1,320)
assert phi_poly([F(0),F(1)])==F(1,12)

# Rebuild the reported 40 interval inequalities without the submitted checker.
bounds=[]
for j in range(40):
    l,h=F(j,100),F(j+1,100)
    beta=(16-100*l*l)/(4-l*l)
    z=beta*10**6
    k=isqrt(z.numerator//z.denominator)
    if F(k*k)<z:k+=1
    assert F(k*k)>=z and (k==0 or F((k-1)**2)<z)
    upper=(2+h)**2/(4*(2-h)**2)*(1+F(k,3000)+beta/4)
    assert upper<=F(91,100)
    bounds.append(upper)
assert F(91,100)<F(24,25)**2

# Exact nonlinear-factorization checks, including feedback endpoint rectangle.
for r in [F(-2,5),F(-1,5),F(0),F(1,5),F(2,5)]:
    for x in [F(-1,2),F(-1,4),F(0),F(1,4),F(1,2)]:
        fr=((r+4)*x+r+1)/(2*r*x+2)
        h=(x+r/4)/(1+r*x)
        assert h==(fr-F(1,2))/2
        assert (h-r/4)/(1-r*h)==x

print(json.dumps({'status':'PASS','polynomial_counterexample':'phi(f)=0; phi(P0 f)=1/320','inverse_factorization':'normalized lifted map agrees exactly with h_r','rational_intervals':40,'max_squared_upper_bound':str(max(bounds)),'meaning':'Finite exact algebra corroboration; not an all-density theorem, literature-completeness claim, or human peer review.'},indent=2))

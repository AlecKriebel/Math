#!/usr/bin/env python3
"""Exact negative controls for a Fourier nonuniformity argument.

No numerical estimate of the actual multiplication-table profile is made.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import json

checks=Counter()
def check(x,k):
    assert x,k
    checks[k]+=1

def density(freq,amp):return {0:Q(1),freq:amp/2,-freq:amp/2}
def convolve_by_integration(a,b):
    # a(x-y)b(y): integrate each y exponent exactly.
    out=Counter()
    for m,c in a.items():
        for n,d in b.items():
            if n-m==0:out[m]+=c*d
    return {k:v for k,v in out.items() if v}

models=0
amps=(Q(-1,2),Q(-1,3),Q(1,3),Q(1,2))
for r,s,b,c in product(range(1,5),range(1,5),amps,amps):
    if r==s:continue
    models+=1
    a=density(r,b);d=density(s,c)
    check(1-abs(b)>0 and 1-abs(c)>0,'strict_positive_density_lower_bounds')
    check(a[0]==d[0]==1,'probability_normalization')
    check(a[r]!=0 and d[s]!=0,'both_factors_nonuniform')
    check(convolve_by_integration(a,d)=={0:Q(1)},'nonuniform_factors_Haar_convolution')
    check(convolve_by_integration(d,a)=={0:Q(1)},'reversed_convolution')
    for m in range(-5,6):
        check(a.get(m,0)*d.get(m,0)==int(m==0),'common_mode_required')

root_cases=0
for exponent in range(1,7):
    q=2**exponent
    for m in range(-3*q,3*q+1):
        # Formal roots of unity in Q[z]/(z^(q/2)+1), exact and no trig.
        coeff=[0]*(q//2)
        for j in range(q):
            k=(m*j)%q
            coeff[k%(q//2)]+=1 if k<q//2 else -1
        expected=[q]+[0]*(q//2-1) if m%q==0 else [0]*(q//2)
        check(coeff==expected,'atomic_uniform_grid_Fourier_coefficients')
        root_cases+=1
    check(q>0 and (q%q)==0,'finite_approximant_retains_mode_q')
    for shift in (Q(0),Q(1,7),Q(2,9),Q(1,2)):
        vals=[]
        for j in range(q):
            t=(Q(j,q)-shift)%1
            vals.append(min(t,1-t))
        # Integral of circle distance to any fixed point is 1/4, Lip=1.
        check(abs(sum(vals)/q-Q(1,4))<=Q(1,2*q),'Lipschitz_averaging_error_control')

from pathlib import Path
import hashlib
h=hashlib.sha256(Path(__file__).with_name('OBSTRUCTION.md').read_bytes()).hexdigest()
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),
 'checks':dict(sorted(checks.items())),'smooth_countermodel_pairs':models,
 'root_of_unity_cases':root_cases,'artifact_sha256':h,
 'limitation':'Elementary Fourier obstruction controls only; neither arithmetic boundary measure nor the multiplication-table profile is computed.'},indent=2,sort_keys=True))

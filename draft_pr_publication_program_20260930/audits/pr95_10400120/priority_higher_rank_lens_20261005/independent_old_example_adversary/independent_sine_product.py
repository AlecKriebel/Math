#!/usr/bin/env python3
"""Exact HT Theorem 5.1 SECOND formula, using 64 signed sine-product terms.

Uses coroot representatives (x,y,z,-x-y-z), x,y,z in 0,...,63, rather than
simple-root coordinates. All histogram arithmetic and quotient reductions are
integer arithmetic. NumPy only vectorizes integer bincount operations.
z=zeta768; each sine factor is (z^d-z^-d)/(2i), d=(rho+6nu,alpha).
Since (2i)^6=-64, the second formula becomes
tau= -z^-630 * P/(2*384^(3/2)) where P is the printed histogram polynomial.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
import hashlib,json,os
import numpy as np

def strip(a):
    while len(a)>1 and not a[-1]:a.pop()
    return a
def divide(a,b):
    a=strip(list(a));quot=[0]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b):
        k=len(a)-len(b);t=a[-1]//b[-1];assert t*b[-1]==a[-1]
        quot[k]=t
        for j,v in enumerate(b):a[k+j]-=t*v
        strip(a)
        if a==[0]:break
    return strip(quot),a
@lru_cache(None)
def cyclotomic(n):
    a=[-1]+[0]*(n-1)+[1]
    for d in range(1,n):
        if n%d==0:
            a,r=divide(a,cyclotomic(d));assert r==[0]
    return tuple(a)
MOD=cyclotomic(768);D=len(MOD)-1
def reduce(a):
    _,a=divide(a,MOD)
    return tuple(a+[0]*(D-len(a)))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scl(a,t):return tuple(t*x for x in a)
def mul(a,b):
    c=[0]*(2*D-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:c[i+j]+=x*y
    return reduce(c)
def root(k):
    k%=768
    return reduce([0]*k+[1])
def conjugate(a):
    c=[0]*768
    for i,x in enumerate(a):c[-i%768]+=x
    return reduce(c)
def nz(a):return [[i,int(x)] for i,x in enumerate(a) if x]

nu=list(np.indices((64,64,64),dtype=np.int64).reshape(3,-1))
nu.append(-nu[0]-nu[1]-nu[2])
norm=sum(x*x for x in nu)
rho_pair=3*nu[0]+2*nu[1]+nu[2]
differences=[j-i+6*(nu[i]-nu[j]) for i in range(4) for j in range(i+1,4)]
assert len(differences)==6
one=root(0)
sqrt6=mul(add(root(96),root(-96)),add(root(64),root(-64)))
assert mul(sqrt6,sqrt6)==scl(one,6)
results={}
for q in (9,25):
    phase=36*q*norm+12*q*rho_pair
    h=np.zeros(768,dtype=np.int64)
    for mask in range(64):
        signs=[1 if mask&(1<<i) else -1 for i in range(6)]
        sign=int(np.prod(signs))
        exponents=(phase+sum(s*d for s,d in zip(signs,differences)))%768
        h+=sign*np.bincount(exponents,minlength=768)
    assert not np.any(h[1::2]),'all exponents lie in Q(zeta384)'
    filename=Path('sine_product_q'+str(q)+'_histogram.json')
    filename.write_text(json.dumps([int(x) for x in h])+'\n')
    p=reduce([int(x) for x in h])
    sq=mul(p,conjugate(p))
    assert sq==scl(one,75497472)
    # tau=-(phase*P)*sqrt6/36864, since 2*384^(3/2)=6144*sqrt6.
    numerator=scl(mul(mul(p,root(-630)),sqrt6),-1)
    target=scl(add(scl(root(-32),-1),scl(root(-160),2)),12288)
    assert numerator==target
    results[str(q)]={'coroot_representatives':64**3,'signed_product_terms':64**4,
      'raw_histogram_file':str(filename),'raw_histogram_sha256':hashlib.sha256(filename.read_bytes()).hexdigest(),
      'P_reduced':nz(p),'P_times_conjugate_P':nz(sq),
      'magnitude_square':str(Fraction(sq[0],4*384**3)),
      'tau_numerator':nz(numerator),'tau_denominator':36864,
      'tau_simplified':'-(zeta768^96+zeta768^224)/3','S3_normalized_square':'8'}
assert results['9']['P_reduced']==results['25']['P_reduced']
print(json.dumps({'PID':os.getpid(),'method':'exact six-sine-product histogram Q(zeta768)',
 'numpy_version':np.__version__,'modulus':nz(MOD),'results':results,
 'complex_equality_exact':True},indent=2))

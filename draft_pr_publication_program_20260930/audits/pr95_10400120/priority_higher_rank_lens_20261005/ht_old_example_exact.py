#!/usr/bin/env python3
"""Independent integer-cyclotomic evaluation of HT Theorem 5.1 for A3,r=6,p=64.
Phi_384(x)=x^128-x^64+1. No floating arithmetic in the certificate.
Root-lattice representatives a alpha1+b alpha2+c alpha3, a,b,c=0,...,63.
"""
import itertools, json, math, cmath, os
from fractions import Fraction
from pathlib import Path
N=384; DEG=128; P=64; KAPPA=6
rho2=(3,1,-1,-3)
weyl=[]
for perm in itertools.permutations(range(4)):
 sign=(-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
 wrho2=tuple(rho2[j] for j in perm)
 dot4=sum(a*b for a,b in zip(rho2,wrho2))
 if dot4%4:raise RuntimeError('rho dot not integral')
 weyl.append((sign,wrho2,dot4//4))
def reduce_hist(hist):
 c=list(hist)
 for e in range(len(c)-1,127,-1):
  t=c[e];c[e]=0;c[e-64]+=t;c[e-128]-=t
 return c[:128]
def conjugate(v):
 h=[0]*384
 for i,c in enumerate(v):h[-i%384]+=c
 return reduce_hist(h)
def multiply(a,b):
 c=[0]*255
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return reduce_hist(c)
def nonzero(c):return [[i,a] for i,a in enumerate(c) if a]
def ds(q,p):
 return sum((Fraction(j,p)-Fraction(1,2))*(Fraction(q*j%p,p)-Fraction(1,2)) for j in range(1,p))
results={}
for q in (9,25):
 S=12*ds(q,P)
 if S!=Fraction(-63,32):raise RuntimeError('Dedekind symbol mismatch')
 h=[0]*384
 params=[]
 for sign,wrho2,dot in weyl:
  v2=tuple(q*r-w for r,w in zip(rho2,wrho2))
  if any(v%2 for v in v2):raise RuntimeError('odd q rho difference')
  params.append((sign,tuple(v//2 for v in v2),dot))
 for a in range(P):
  for b in range(P):
   for c in range(P):
    nu=(a,-a+b,-b+c,-c)
    norm2=sum(x*x for x in nu)
    phase=18*q*norm2
    for sign,v,dot in params:
     e=(phase+6*sum(x*y for x,y in zip(nu,v))-dot)%384
     h[e]+=sign
 v=reduce_hist(h)
 sq=multiply(v,conjugate(v))
 # Dedekind phase has modulus 1, prefactor squared is 1/(4*(p*kappa)^3).
 den=4*(P*KAPPA)**3
 numeric=sum(c*cmath.exp(2j*math.pi*i/384) for i,c in enumerate(v))
 tau=-cmath.exp(-2j*math.pi*315/384)*numeric/(2*384**1.5)
 result={'q':q,'dedekind_symbol':str(S),'histogram_terms':P**3*24,'sum_polynomial':nonzero(v),'square_polynomial':nonzero(sq),'square_denominator':den,'tau_approx':[tau.real,tau.imag],'magnitude_approx':abs(tau),'magnitude_square_approx':abs(tau)**2,'S3_normalized_square_if_S00_square_1_over_24':nonzero([24*x for x in sq]),'S3_normalized_square_denominator':den}
 results[str(q)]=result
 Path(f'ht_q{q}_histogram.json').write_text(json.dumps(h)+'\n')
print(json.dumps({'PID':os.getpid(),'method':'HT5.1 full A3,r=6 exact cyclotomic','results':results,'exact_squared_magnitude_equality':results['9']['square_polynomial']==results['25']['square_polynomial']},indent=2))

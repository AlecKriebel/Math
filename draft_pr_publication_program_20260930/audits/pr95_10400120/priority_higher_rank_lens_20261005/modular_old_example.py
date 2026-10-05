#!/usr/bin/env python3
"""Separate full SU4 level2 category, all10 dominant weights. Numerical diagnostic."""
from fractions import Fraction as F
from itertools import permutations
import cmath, math, json, os
N=4;r=6;rho=(F(3,2),F(1,2),F(-1,2),F(-3,2))
labels=[(a,b,c) for a in range(3) for b in range(3-a) for c in range(3-a-b)]
vectors=[]
for a,b,c in labels:
 rows=(a+b+c,b+c,c,0);mean=F(sum(rows),4)
 vectors.append(tuple(F(x)-mean+y for x,y in zip(rows,rho)))
perms=[(w,(-1)**sum(w[i]>w[j] for i in range(4) for j in range(i+1,4))) for w in permutations(range(4))]
S=[]
for x in vectors:
 row=[]
 for y in vectors:
  row.append(-sum(sign*cmath.exp(-2j*math.pi*float(sum(x[i]*y[w[i]] for i in range(4)))/r) for w,sign in perms)/(2*r**1.5))
 S.append(row)
T=[cmath.exp(1j*math.pi*float(sum(z*z for z in x)-5)/r) for x in vectors]
unitarity=max(abs(sum(S[i][j]*S[k][j].conjugate() for j in range(10))-(i==k)) for i in range(10) for k in range(10))
def cf(p,q):
 a=[]
 while q:
  c=-(-p//q);a.append(c);p,q=q,c*q-p
 return a
def chain(q):
 a=cf(64,q);v=[complex(i==0) for i in range(10)]
 for c in [None]+list(reversed(a)):
  if c is not None:v=[z*t**c for z,t in zip(v,T)]
  v=[sum(S[i][j]*v[j] for j in range(10)) for i in range(10)]
 return a,v[0]
results={str(q):{'continued_fraction':chain(q)[0],'uncorrected_chain_real':chain(q)[1].real,'uncorrected_chain_imag':chain(q)[1].imag,'magnitude':abs(chain(q)[1]),'squared_magnitude':abs(chain(q)[1])**2} for q in [9,25]}
if unitarity>1e-12:raise RuntimeError('S unitarity failed')
print(json.dumps({'PID':os.getpid(),'all_labels':labels,'S00':[S[0][0].real,S[0][0].imag],'S00_squared':abs(S[0][0])**2,'S_unitarity_error':unitarity,'results':results},indent=2))

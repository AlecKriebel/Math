#!/usr/bin/env python3
"""Independent exact full SU4_k2 S/T surgery in Q(zeta48). Phi48=x16-x8+1."""
from itertools import permutations
from fractions import Fraction as F
import json, os
DEG=16
def red(a):
 a=list(a)
 for e in range(len(a)-1,15,-1):
  t=a[e];a[e]=0;a[e-8]+=t;a[e-16]-=t
 return tuple(a[:16])
def root(e):
 a=[0]*48;a[e%48]=1;return red(a)
def mul(a,b):
 c=[0]*31
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:c[i+j]+=x*y
 return red(c)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,t):return tuple(x*t for x in a)
def conj(a):
 b=[0]*48
 for i,c in enumerate(a):b[-i%48]+=c
 return red(b)
def shift(a,e):return mul(a,root(e))
def nz(a):return [[i,c] for i,c in enumerate(a) if c]
def identity_scalar(a):
 if any(a[1:]):raise RuntimeError('not rational scalar')
 return a[0]
sqrt6=mul(add(root(6),root(-6)),add(root(4),root(-4)))
if identity_scalar(mul(sqrt6,sqrt6))!=6:raise RuntimeError('sqrt6 identity')
rho=(F(3,2),F(1,2),F(-1,2),F(-3,2))
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
  wsum=(0,)*16
  for w,sign in perms:
   d4=4*sum(x[i]*y[w[i]] for i in range(4))
   if d4.denominator!=1:raise RuntimeError('S exponent not integer')
   wsum=add(wsum,scale(root(-2*int(d4)),sign))
  row.append(scale(mul(sqrt6,wsum),-1)) # S=Snum/72
 S.append(row)
Texponents=[]
for x in vectors:
 a=4*(sum(y*y for y in x)-5)
 if a.denominator!=1:raise RuntimeError('T exponent not integer')
 Texponents.append(int(a))
unitarity_exact=True
for i in range(10):
 for k in range(10):
  a=(0,)*16
  for j in range(10):a=add(a,mul(S[i][j],conj(S[k][j])))
  if a!=scale(root(0),72**2*int(i==k)):raise RuntimeError('S unitarity exact failed')
def cf(p,q):
 a=[]
 while q:
  c=-(-p//q);a.append(c);p,q=q,c*q-p
 return a
def chain(q):
 a=cf(64,q);v=[root(0)]+[(0,)*16]*9;den=1
 for c in [None]+list(reversed(a)):
  if c is not None:v=[shift(x,c*t) for x,t in zip(v,Texponents)]
  new=[]
  for i in range(10):
   y=(0,)*16
   for j in range(10):y=add(y,mul(S[i][j],v[j]))
   new.append(y)
  v=new;den*=72
 # positive chain gives orientation reverse of HT. U has Phi=-3;
 # T=omega*Theta, omega=zeta48^10.
 corrected=shift(v[0],10*(-3-sum(a)))
 sq=mul(corrected,conj(corrected))
 scalar=F(identity_scalar(sq),den**2)
 if scalar!=F(1,3):raise RuntimeError('exact square is not 1/3')
 return {'continued_fraction':a,'S_factors':len(a)+1,'chain_denominator':den,'corrected_polynomial':nz(corrected),'squared_magnitude':str(scalar),'S3_normalized_squared_magnitude':str(24*scalar)}
results={str(q):chain(q) for q in [9,25]}
# Compare complex values after putting both polynomials over common denominators.
a=results['9'];b=results['25'];ap=[0]*16;bp=[0]*16
for e,c in a['corrected_polynomial']:ap[e]=c
for e,c in b['corrected_polynomial']:bp[e]=c
same=scale(ap,b['chain_denominator'])==scale(bp,a['chain_denominator'])
print(json.dumps({'PID':os.getpid(),'method':'separate 10-object modular surgery exact Q(zeta48)','all_labels':labels,'S_exact_unitarity_pass':unitarity_exact,'S00_squared':str(F(identity_scalar(mul(S[0][0],conj(S[0][0]))),72**2)),'results':results,'equal_corrected_complex_values':same},indent=2))

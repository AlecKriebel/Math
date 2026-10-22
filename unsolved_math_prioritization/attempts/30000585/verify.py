#!/usr/bin/env python3
"""Exact finite model/normalization controls; not a computation of critical exponents."""
from pathlib import Path
from collections import Counter
from itertools import product
from fractions import Fraction as F
from functools import lru_cache
import hashlib,json
counts=Counter()
def ck(v,label):
 assert v,label
 counts[label]+=1
steps={'E':(1,0),'N':(0,1),'S':(0,-1)}
def vertices(word):
 p=[(0,0)]
 for s in word:
  a,b=p[-1];c,d=steps[s];p.append((a+c,b+d))
 return p
def contacts(p):
 return sum(abs(p[i][0]-p[j][0])+abs(p[i][1]-p[j][1])==1 for i in range(len(p)) for j in range(i+2,len(p)))
def valid(word):return all(a+b not in ('NS','SN') for a,b in zip(word,word[1:]))
def signed_parts(total,k):
 if k==0:
  if total==0:yield()
  return
 for a in range(total+1):
  for rest in signed_parts(total-a,k-1):
   if a==0:yield(0,)+rest
   else:
    yield(a,)+rest;yield(-a,)+rest
all_counts={};walks=0
for n in range(1,10):
 direct=Counter()
 for suffix in product('ENS',repeat=n-1):
  w='E'+''.join(suffix)
  if not valid(w):continue
  walks+=1;p=vertices(w);k=contacts(p);N=w.count('E')
  ck(len(set(p))==n+1,'self_avoidance_from_directed_rule')
  ck(p[-1][0]==N,'span_is_east_count')
  eta=[(p[-1][0]-p[n-i][0],p[-1][1]-p[n-i][1]) for i in range(n+1)]
  ck(eta==vertices(w[::-1]),'endpoint_reversal_isometry')
  ck(contacts(eta)==k and w[::-1][-1]=='E','endpoint_weights_preserved')
  direct[k,N]+=1
 segment=Counter()
 for N in range(1,n+1):
  for r in signed_parts(n-N,N):
   k=sum(min(abs(a),abs(b)) for a,b in zip(r,r[1:]) if a*b<0)
   w=''.join(('N'*a if a>=0 else 'S'*(-a))+'E' for a in r)
   ck(contacts(vertices(w))==k,'segment_contact_formula')
   segment[k,N]+=1
 ck(direct==segment,'2007_2009_contact_span_coefficients')
 all_counts[n]=direct
# Independent no-interaction rational generating-function recurrence.
for h in (F(1,2),F(1),F(3,2),F(2)):
 a=[F(1),h]
 for n in range(2,10):a.append((1+h)*a[-1]+h*a[-2])
 for n,C in all_counts.items():ck(sum(v*h**N for (k,N),v in C.items())==a[n],'no_contact_generating_function')
# Critical line and physical branch, entirely rational in a=sqrt(omega).
for q in range(1,16):
 for p in range(q+1,2*q+12):
  a=F(p,q);omega=a*a;h=omega*(a-1)/(a+1)
  ck(0<h<omega,'critical_physical_branch')
  ck(omega*(omega-h)**2==(omega+h)**2,'critical_curve_identity')
  ck(h-1==(a**3-a*a-a-1)/(a+1),'zero_force_cubic')
  ck(3*a*a-2*a-1==(3*a+1)*(a-1)>0,'unique_zero_force_root_monotonicity')
ck(F(1839,1000)**3-F(1839,1000)**2-F(1839,1000)-1<0,'root_lower_rational_bound')
ck(F(184,100)**3-F(184,100)**2-F(184,100)-1>0,'root_upper_rational_bound')
ck(F(4)*(F(2)-1)/(F(2)+1)==F(4,3),'omega4_critical_force_fugacity')
# Exact finite partition-function covariance, in log omega/log h variables.
for C in all_counts.values():
 for omega,h in ((F(1),F(1)),(F(2),F(3,2)),(F(4),F(4,3))):
  terms=[(F(v)*omega**k*h**N,k,N) for (k,N),v in C.items()];Z=sum(w for w,k,N in terms)
  K=sum(w*k for w,k,N in terms)/Z;H=sum(w*N for w,k,N in terms)/Z
  VK=sum(w*k*k for w,k,N in terms)/Z-K*K;VH=sum(w*N*N for w,k,N in terms)/Z-H*H
  cov=sum(w*k*N for w,k,N in terms)/Z-K*H
  ck(VK>=0 and VH>=0 and VK*VH>=cov*cov,'joint_log_parameter_convexity')
# Secant bounds for a convex3/2 singularity, with square-rational scales.
for j in range(1,20):
 for q in range(2,15):
  delta=F(j,7)**2;root=F(j,7);r=F(q-1,q);b=F(q+1,q)
  lower=root*(1-r**3)/(1-r*r);upper=root*(b**3-1)/(b*b-1)
  ck(lower<=F(3,2)*root<=upper,'convex_secant_derivative_control')
base=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(counts.values()),'categories':dict(counts),'enumerated_first_E_walks':walks,'maximum_length':9,'artifact_sha256':hashlib.sha256((base/'SOURCE_STATUS.md').read_bytes()).hexdigest(),'limits':'Exact finite model matching, rational critical-curve identities and convexity controls only. No numerical proof of an infinite-volume phase transition or the3/2 exponent; the uniform Airy asymptotic is credited to the published sources.'}
(base/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

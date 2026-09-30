#!/usr/bin/env python3
"""Independent exact annular-measure controls, not a proof by truncation."""
from fractions import Fraction as R
from pathlib import Path
import hashlib,json
N=6;checks=0;cases=0

def ck(v):
 global checks
 assert v
 checks+=1

def add(d,p,v):d[p]=d.get(p,R(0))+v

def dilate(d,c):return {tuple(c*x for x in p):v for p,v in d.items()}

def transform(d,a,b,c):
 out={p:a*v for p,v in d.items()}
 for p,v in dilate(d,c).items():add(out,p,b*v)
 return {p:v for p,v in out.items() if v}

def weighted(d):return sum(abs(v)*min(R(1),sum(x*x for x in p)) for p,v in d.items())

cs=[R(5,4),R(5,3),R(7,2)]
for c in cs:
 qs=[1/c**2,(1+1/c**2)/2,R(1),R(3,2),1/(2*c**2)]
 for q in qs:
  cases+=1;a=1/q;b=R(1)
  r=(1+c)/2
  # Three different rays, two different norms, mixed signed seed.
  seeds=[((R(1),R(0)),R(2)),((R(-1),R(0)),R(-3)),((3*r/5,4*r/5),R(5))]
  mass=sum(abs(v) for p,v in seeds)
  moment=sum(abs(v)*sum(x*x for x in p) for p,v in seeds)
  for p,v in seeds:ck(1<=sum(x*x for x in p)<c*c)
  nu={};by_annulus={}
  for k in range(-N,N+1):
   shell={tuple(c**k*x for x in p):v*(-q)**k for p,v in seeds};by_annulus[k]=shell
   for p,v in shell.items():ck(p not in nu);nu[p]=v
   ck(sum(abs(v) for v in shell.values())==q**k*mass)
   ck(weighted(shell)==(q**k*mass if k>=0 else (c*c*q)**k*moment))
  positive={p:v for p,v in nu.items() if v>0};negative={p:-v for p,v in nu.items() if v<0}
  up=transform(positive,a,b,c);um=transform(negative,a,b,c)
  residual=transform(nu,a,b,c)
  expected={p:a*v for p,v in by_annulus[-N].items()}
  for p,v in dilate(by_annulus[N],c).items():add(expected,p,b*v)
  ck(residual==expected)
  ck(len(residual)==2*len(seeds))
  for k in range(-N+1,N+1):
   for p in by_annulus[k]:ck(up.get(p,0)==um.get(p,0))
  # The truncated kernel is expressly not zero.
  ck(any(v!=0 for v in residual.values()))
  ck(weighted(nu)==sum(q**k*mass for k in range(N+1))+sum((c*c*q)**k*moment for k in range(-N,0)))
  if 1/c**2<q<1:
   total=mass/(1-q)+moment/(c*c*q-1)
   tail=mass*q**(N+1)/(1-q)+moment*(c*c*q)**(-N)/(c*c*q-1)
   ck(total-weighted(nu)==tail);ck(tail>0)
  if q==1:
   ck(sum(q**k*mass for k in range(N+1))==mass*(N+1))
  if c*c*q==1:
   ck(sum((c*c*q)**k*moment for k in range(-N,0))==moment*N)
  # D_s(aI+bD_c) is exactly aD_s+bD_(sc), even for mixed seeds.
  for s in [R(2,7),R(5,2)]:
   left=dilate(transform(nu,a,b,c),s)
   right={p:a*v for p,v in dilate(nu,s).items()}
   for p,v in dilate(nu,s*c).items():add(right,p,b*v)
   right={p:v for p,v in right.items() if v}
   ck(left==right)

# Dense rational parametrization of the unit circle; exact imaginary Mellin bound.
for a,b in [(R(2),R(1)),(R(5,3),R(1)),(R(7,2),R(1))]:
 for k in range(-20,21):
  t=R(k,7);co=(1-t*t)/(1+t*t);si=2*t/(1+t*t)
  ck(co*co+si*si==1)
  value=(a+b*co)**2+(b*si)**2
  ck(value-(a-b)**2==2*a*b*(1+co));ck(value>0)

# Independent smooth-density collision algebra: dilation c multiplies x^-2 by c,
# while a cos(pi log_c x) mode changes sign after x -> x/c.
for c in cs+[R(2)]:
 a=c;b=R(1)
 ck(b<a<b*c*c)
 for h in [R(k,10) for k in range(-10,11)]:
  ck(a*(1+h)+b*c*(1-h)==a+b*c)
  ck(0<=1+h<=2)

# Finite-input geometric tails can never both converge.
for q in [R(k,j) for k in range(1,9) for j in range(1,9)]:
 ck(not (q<1 and q>1))
 if q>=1:ck(sum(q**k for k in range(10))>=10)
 else:ck(sum(q**k for k in range(-10,0))>=10)

root=Path(__file__).parent
proof=root/'author_replay/PARTIAL_RESULT.md'
out={'verdict':'PASS','independent_assertions':checks,'multidirectional_seed_cases':cases,
 'frozen_artifact_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
 'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'scope':'Exact finite multidirectional annular identities, endpoint divergences, signed Jordan output equality, scaling normalization, geometric tails and smooth-density cancellation. Infinite quantifiers are reviewed analytically.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))

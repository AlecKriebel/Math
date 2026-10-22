#!/usr/bin/env python3
"""Exact replay of Escobar--Harada Example 4.5 and authored boundary checks.
Standard library only. This verifies a finite certificate and bounded controls,
not the general wall-crossing theorem or a classification of all prime cones.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb, gcd
from functools import reduce
import json

M1=((1,1,1,1),(0,1,2,3),(0,0,-1,4))
M2=((1,1,1,1),(0,1,2,3),(0,0,3,-1))
A=(0,11,0,0); B=(6,0,4,1); C=(7,0,1,3)

def mv(M,a):return tuple(sum(x*y for x,y in zip(r,a)) for r in M)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def det3(m):
 a,b,c=m
 return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])
def minors(M):return [det3(tuple(tuple(r[j] for j in js) for r in M)) for js in combinations(range(4),3)]
def compositions(n):
 for a in range(n+1):
  for b in range(n-a+1):
   for c in range(n-a-b+1):yield (a,b,c,n-a-b-c)
def standard(a,which):
 k,b=divmod(a[1],11); v=B if which==1 else C
 return (a[0]+k*v[0],b,a[2]+k*v[2],a[3]+k*v[3])
def endpoints1(x):return (max(-x/2,5*x-11),4*x/3)
def endpoints2(x):return (-x/3,min(3*x/2,11-4*x))
def shift(x,z):return z-endpoints1(x)[0]+endpoints2(x)[0]
def flip(x,z):return -z+endpoints1(x)[0]+endpoints2(x)[1]

assert mv(M1,A)==mv(M1,B)==(11,11,0)
assert mv(M2,A)==mv(M2,C)==(11,11,0)
assert reduce(gcd,map(abs,minors(M1)))==1
assert reduce(gcd,map(abs,minors(M2)))==1
assert mv(M1,tuple(x-y for x,y in zip(A,B)))==(0,0,0)
assert mv(M2,tuple(x-y for x,y in zip(A,C)))==(0,0,0)
weights={}
for label,w,expected in [('prime_1',(0,0,-1,4),(0,0,11)),('prime_2',(0,0,3,-1),(0,11,0)),('nonprime',(0,0,-2,-3),(0,-11,-11))]:
 weights[label]=tuple(dot(w,t) for t in (A,B,C));assert weights[label]==expected
assert shift(Q(1),Q(0))==Q(1,6)
assert flip(Q(1),Q(0))==1
# On each common affine interval, two endpoint tests prove the affine identities.
for lo,hi in ((Q(0),Q(2)),(Q(2),Q(3))):
 for x in (lo,hi):
  l1,u1=endpoints1(x);l2,u2=endpoints2(x)
  assert u1-l1==u2-l2
  assert shift(x,l1)==l2 and shift(x,u1)==u2
  assert flip(x,l1)==u2 and flip(x,u1)==l2
  assert l1+u2==x
# Primitive relation + b in [0,10] gives unique representatives in every degree.
checks=[];total=0
for n in range(23):
 exps=list(compositions(n));std=[a for a in exps if a[1]<11]
 s1={mv(M1,a) for a in exps};s2={mv(M2,a) for a in exps}
 d1={mv(M1,a):a for a in std};d2={mv(M2,a):a for a in std}
 expected=comb(n+3,3)-(comb(n-8,3) if n>=11 else 0)
 assert len(d1)==len(d2)==len(std)==expected
 assert set(d1)==s1 and set(d2)==s2
 for a in exps:
  assert mv(M1,standard(a,1))==mv(M1,a)
  assert mv(M2,standard(a,2))==mv(M2,a)
 for v,a in d1.items():
  target=mv(M2,a);assert d2[target]==a
  assert v[:2]==target[:2]
 checks.append({'degree':n,'values':expected});total+=len(exps)
v=(1,1,0)
assert mv(M2,standard(A,1))==(11,11,11)!=tuple(11*x for x in v)
h=(1,1,1)
assert h not in {tuple(r[j] for r in M1) for j in range(4)}
assert h not in {tuple(r[j] for r in M2) for j in range(4)}
assert mv(M1,(7,0,1,3))==tuple(11*x for x in h)
assert mv(M2,(6,0,4,1))==tuple(11*x for x in h)
result={
 'result':'PASS','arithmetic':'exact integers and rational fractions',
 'attribution':'Escobar--Harada, arXiv:1912.04809v2, Example 4.5; additional elementary controls are explanatory, with no novelty claim',
 'matrix_minors':{'M1':minors(M1),'M2':minors(M2)},'weight_checks':weights,
 'theta_v':[1,1,0],'theta_11v':[11,11,11],
 'shift_v':['1','1','1/6'],'flip_v':[1,1,1],
 'saturation_hole':[1,1,1],'hole_multiple':11,
 'all_degree_certificate':'Primitive kernel relation and unique standard representative; mathematical proof is in EXACT_CONTROLS.md',
 'bounded_replay':{'degrees':'0 through 22','exponent_vectors':total,'per_degree':checks},
 'limitations':['No numerical sampling used for the piecewise affine identities.','General theorem relies on published proofs.','This program does not test every tropical cone or independently prove the imported Khovanskii-basis theorem.']}
print(json.dumps(result,indent=2))

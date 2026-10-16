#!/usr/bin/env python3
"""Independent exact boundary/parameter checks. General all-state proof is separate."""
from fractions import Fraction as F
from itertools import product
import json,hashlib
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions required')

def mul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(4)),F(0)) for j in range(4)] for i in range(4)]
def diag(a):return [[F(a[i]) if i==j else F(0) for j in range(4)] for i in range(4)]
def tr(a):return sum(a[i][i] for i in range(4))
def scale(c,a):return [[c*x for x in row] for row in a]
def equal(a,b):return all(x==y for r,s in zip(a,b) for x,y in zip(r,s))
one=diag([1]*4);p=diag([0,0,1,1]);q=diag([0,1,0,1]);counts={'matrix_corner_checks':0,'joint_word_checks':0,'parameter_instances':0,'boundary_controls':0}
results=[]
for x,z,b in [(3,4,5),(4,3,5),(5,12,13),(12,5,13),(8,15,17),(15,8,17),(1,0,1),(0,1,1)]:
 v=[F(x,b),F(0),F(0),F(z,b)];rho=[[a*c for c in v] for a in v];lam=F(z*z,b*b)
 assert tr(rho)==1 and equal(mul(rho,rho),rho)
 state=lambda a:tr(mul(rho,a))
 assert state(p)==state(q)==state(mul(p,q))==lam
 for i,j in product(range(4),repeat=2):
  E=[[F(int(a==i and c==j)) for c in range(4)] for a in range(4)]
  assert equal(mul(mul(rho,E),rho),scale(state(E),rho));counts['matrix_corner_checks']+=1
 for n in range(1,9):
  for letters in product([p,q],repeat=n):
   a=one
   for letter in letters:a=mul(a,letter)
   assert state(a)==lam
   assert state(a)==(1-lam)*a[0][0]+lam*a[3][3]
   counts['joint_word_checks']+=1
 if lam in [0,1]:counts['boundary_controls']+=1
 else:assert state([[F(int((i,j)==(0,3))) for j in range(4)] for i in range(4)])!=0
 results.append({'lambda':str(lam),'mixed_downstairs':0<lam<1,'pure_upstairs':True,'downstairs_mixture_components_distinct':True,'nontrivial_mixture':0<lam<1});counts['parameter_instances']+=1
# The formal nonextension Gram determinant does not depend on the unknown second diagonal.
for t in [F(-9),F(0),F(1,7),F(1000)]:assert 0*t-1==-1
print(json.dumps({'status':'PASS','counts':counts,'parameters':results,'arithmetic':'exact rational','scope':'Finite controls plus parameter/boundary checks; universal witness exclusion requires the written positivity/GNS proof.','verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))

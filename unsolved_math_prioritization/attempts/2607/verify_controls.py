#!/usr/bin/env python3
"""Exact finite controls for proof mechanisms; not a search for a counterexample."""
from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path

def eye(n): return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def sub(a,b): return tuple(tuple(x-y for x,y in zip(ar,br)) for ar,br in zip(a,b))
def mul(a,b): return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))) for i in range(len(a)))
def rank(a):
 a=[list(map(Fraction,r)) for r in a]; nr=len(a); nc=len(a[0]); p=0
 for j in range(nc):
  z=next((i for i in range(p,nr) if a[i][j]),None)
  if z is None: continue
  a[p],a[z]=a[z],a[p];t=a[p][j];a[p]=[v/t for v in a[p]]
  for i in range(nr):
   if i!=p:
    t=a[i][j];a[i]=[v-t*u for v,u in zip(a[i],a[p])]
  p+=1
  if p==nr:break
 return p

def determinant(a):
 n=len(a);return sum((-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))*prod(a[i][p[i]] for i in range(n)) for p in permutations(range(n)))
def prod(xs):
 r=1
 for x in xs:r*=x
 return r

def main():
 checks=0;rigidity=0
 for n in range(1,5):
  I=eye(n)
  for p in permutations(range(n)):
   for s in product((-1,1),repeat=n):
    M=tuple(tuple(s[j] if i==p[j] else 0 for j in range(n)) for i in range(n)); D=sub(M,I);P=I;r=rank(D)
    for k in range(1,6):
     P=mul(P,D);assert rank(P)==r;checks+=1
     if determinant(M)==1 and rank(P)<=1:
      assert M==I;rigidity+=1
 U=((1,1),(0,1));assert determinant(U)==1 and rank(sub(U,eye(2)))==1 and U!=eye(2)
 R=((0,-1),(1,-1));assert mul(mul(R,R),R)==eye(2) and determinant(R)==1
 D=sub(R,eye(2));assert rank(mul(D,D))==2
 # Distinct rational slopes on affine lines, including negative parameters.
 pts=[(1,n) for n in range(-100,101)]
 assert all(a*d-b*c!=0 for i,(a,b) in enumerate(pts) for c,d in pts[i+1:])
 # The axes are a countermodel only to normal-set/PCG-style inferences.
 axes=[(n,0) for n in range(-10,11)]+[(0,n) for n in range(-10,11)]
 assert rank(axes)==2 and all(x==0 or y==0 for x,y in axes)
 # Explicit H(Z) x H(Z) controls for the auxiliary induction countermodel.
 def hm(x,y):
  return tuple(x[i]+y[i] for i in range(4))+(x[4]+y[4]+x[0]*y[1],x[5]+y[5]+x[2]*y[3])
 def hi(x):return tuple(-x[i] for i in range(4))+(-x[4]+x[0]*x[1],-x[5]+x[2]*x[3])
 def hc(x,y):return hm(hm(hm(hi(x),hi(y)),x),y)
 X=set()
 for i in range(4):
  for n,c,d in product(range(-2,3),range(-1,2),range(-1,2)):
   x=[0]*4;x[i]=n;X.add(tuple(x)+(c,d))
 pair_checks=0
 for x in X:
  for y in X:
   z=hc(x,y);assert z[:4]==(0,0,0,0)
   assert z[4:]==(x[0]*y[1]-y[0]*x[1],x[2]*y[3]-y[2]*x[3])
   assert z[4]==0 or z[5]==0;pair_checks+=1
 e=[tuple(int(i==j) for i in range(6)) for j in range(6)]
 assert hc(e[0],e[1])==e[4] and hc(e[2],e[3])==e[5]
 out={'heisenberg_X_samples':len(X),'heisenberg_commutator_pair_checks':pair_checks,'heisenberg_derived_rank':2,'signed_permutation_power_rank_checks':checks,'determinant_one_rank_at_most_one_checks':rigidity,'order_three_matrix':R,'rank_of_repeated_commutator':rank(mul(D,D)),'unipotent_hypothesis_countercontrol':True,'distinct_affine_directions':len(pts),'axis_countermodel_rank':2,'scope':'Finite exact controls only; general statements are justified by written proofs.'}
 path=Path(__file__).with_name('control_results.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()

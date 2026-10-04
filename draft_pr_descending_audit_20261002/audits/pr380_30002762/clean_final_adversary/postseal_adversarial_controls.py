#!/usr/bin/env python3
"""Post-seal controls with finite quotient falsifiers and analytic negative boundaries."""
from collections import deque
from fractions import Fraction as F
from itertools import permutations,product
import json
C=0
def ck(x):
 global C
 C+=1
 assert x
# Independent permutation quotient for finite braid maps and invalid wrap/adjacency mutants.
def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inverse(a):return tuple(a.index(i) for i in range(len(a)))
def trans(n,i):
 p=list(range(n));p[i-1],p[i]=p[i],p[i-1];return tuple(p)
def power(a,k):
 if k<0:return power(inverse(a),-k)
 v=tuple(range(len(a)))
 for _ in range(k):v=compose(v,a)
 return v
btargets=[]
for K in range(2,101):
 N=K+2;I=tuple(range(N));s=[trans(N,i) for i in range(1,N)]
 delta=I
 for a in s:delta=compose(delta,a)
 a=s[0];di=inverse(delta);a1=compose(compose(delta,a),di)
 ck(compose(compose(a,a1),a)==compose(compose(a1,a),a1))
 for j in range(1,K+1):
  aj=compose(compose(power(delta,j),a),power(delta,-j));ck(aj==s[j])
  if j>=2:ck(compose(a,aj)==compose(aj,a))
 omitted=compose(compose(power(delta,K+1),a),power(delta,-K-1))
 ck(compose(a,omitted)!=compose(omitted,a))
 ck(compose(compose(delta,s[-1]),di)!=s[0])
 ck(compose(a,a1)!=compose(a1,a))
 btargets.append(N)
# Splitting is essential to quotient identification: Heisenberg noncommutative, product abelian.
def hm(x,y):return(x[0]+y[0],x[1]+y[1],x[2]+y[2]+x[0]*y[1])
ck(hm((1,0,0),(0,1,0))!=hm((0,1,0),(1,0,0)))
# Norm-LP promise cannot be dropped. Reduced free word phi=ab-count minus B A-count.
def red(w):
 out=[]
 for x in w:
  if out and out[-1]==-x:out.pop()
  else:out.append(x)
 return tuple(out)
def phi(w):return sum((a,b)==(1,2) for a,b in zip(w,w[1:]))-sum((a,b)==(-2,-1) for a,b in zip(w,w[1:]))
W={red(w) for n in range(6) for w in product((1,-1,2,-2),repeat=n)}
D=0
for u in W:
 for v in W:
  z=abs(phi(red(u+v))-phi(u)-phi(v));ck(z<=3);D=max(D,z)
for n in range(1,501):ck(phi((1,2,-1,-2)*n)==n)
# Exact denominator/torsion traps that real LP alone cannot turn into one-step lattice claims.
ck(F(2,3)*3==2)
# Z²/<(2,4)>: (1,2) has real cost0 but nonzero quotient class of order2.
v=(1,2);r=(2,4);ck(tuple(2*a for a in v)==r);ck(not any(tuple(k*a for a in r)==v for k in range(-100,101)))
# Z/<2>: v=1 lies in real row span, yet not integer row lattice until multiplier2.
ck(F(-1,2)*2+1==0);ck(all(1+2*k!=0 for k in range(-100,101)))
# Index separation is universal min gap3(j-i)-1; stride2 intentionally fails.
for i in range(-50,51):
 for j in range(i+1,52):ck(3*(j-i)-1>=2)
ck(min(abs(a-b) for a in (0,1) for b in (2,3))==1)
print(json.dumps({'status':'PASS','assertions':C,'finite_braid_permutation_targets':len(btargets),'K_range':[2,100],'negative_mutants_rejected':['first omitted distance','wraparound conjugation','adjacent commutation','nonsplit direct product','unpromised abelianization norm','real-lattice one-step equality','stride2 displacement'],'free_control_words':len(W),'free_control_max_observed_defect':D,'scope':'Exact finite quotient falsifiers and bounded signed controls; universal conclusions are written proofs and primary inputs.'},indent=2,sort_keys=True))

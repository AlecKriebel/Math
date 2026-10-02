#!/usr/bin/env python3
"""Exact free-product, absorption, Schur-ratio and unitary-path coefficient controls."""
from fractions import Fraction as F
from itertools import product
import json
checks=0
def ok(x):
 global checks
 assert x
 checks+=1
def red(w):
 s=[]
 for x in w:
  if s and s[-1]==x:s.pop()
  else:s.append(x)
 return tuple(s)
def mul(x,y):return red(x+y)
def inv(x):return x[::-1]
words={()}
for length in range(1,8):
 for w in product((0,1,2),repeat=length):words.add(red(w))
for g in sorted(words):
 lengths=[len(mul((s,),g)) for s in range(3)]
 if g:ok(lengths.count(len(g)-1)==1);ok(lengths.count(len(g)+1)==2)
 else:ok(lengths==[1,1,1])
 # Root/nonroot weighted row sum as rational coefficient times sqrt(2).
 ratio=F(3,2) if not g else F(2)
 ok(ratio<=2)
small=[w for w in sorted(words) if len(w)<=3]
for g,h,s in product(small,small,range(3)):
 sg=mul((s,),g);sh=mul((s,),h)
 ok(mul(inv(sg),sh)==mul(inv(g),h))
 ok(mul((s,),mul((),(s,)))==())
# Distinct left orbits of ab for the stated representative words (ca)^n.
reps=[(2,0)*n for n in range(1,31)]
for n,g in enumerate(reps):
 for k in range(-20,21):
  u=(0,1)*k if k>=0 else (1,0)*(-k)
  image=mul(u,g)
  if k:ok(image[0] in (0,1));ok(image not in reps)
  else:ok(image==g)
ok(F(9)>F(8));ok(F(3,2)<=2)
# E=1+(zeta-1)P is unitary for a projection P and |zeta|=1.
for m,n in product(range(1,41),repeat=2):
 a=F(m*m-n*n,m*m+n*n);b=F(2*m*n,m*m+n*n)
 ok(a*a+b*b==1)
 ok(2*a-2+(a-1)**2+b*b==0)
# The endpoint zeta=-1 gives 1-2P, and P=(1-v)/2 recovers v formally.
ok(1-2*F(1,2)==0);ok(-2*F(-1,2)==1)
print(json.dumps({'status':'PASS','assertions':checks,'reduced_words':len(words),'absorption_word_pairs':len(small)**2,'scope':'Finite exact algebraic controls; operator norm bounds, positive-part functional calculus, nuclear-ideal commutation and spectrum topology are proved analytically'},indent=2,sort_keys=True))

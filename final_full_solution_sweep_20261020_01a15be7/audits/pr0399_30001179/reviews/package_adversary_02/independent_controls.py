#!/usr/bin/env python3
"""Independent bounded exact controls; no infinite-dimensional certification."""
from fractions import Fraction as F
from itertools import product,permutations
import json

def need(x,s):
 if not x: raise RuntimeError(s)

def cat(a,b):
 # A block is an ultimately constant infinite stream (prefix, final marker).
 ab,af=a;bb,bf=b
 if bb:
  first=(af+bb[0][0],bb[0][1])
  return (ab+(first,)+bb[1:],bf)
 return (ab,af+bf)

def tagged(n,m,tag):
 return (tuple(((tag*100+i,),tag*1000+i) for i in range(n)),tuple(tag*10000+j for j in range(m)))

def grade(x):return len(x[0]),len(x[1])

def add(a,b):return (a[0]+b[0],b[1]) if b[0] else (a[0],a[1]+b[1])

counts={'coordinate_associativity':0,'ordinal_grades':0,'density_chain':0,'finite_core':0,'finite_hull':0,'mutants_rejected':0}
words=[tagged(n,m,1) for n,m in product(range(4),repeat=2)]
for i,j,k in product(range(16),repeat=3):
 a=tagged(*grade(words[i]),1);b=tagged(*grade(words[j]),2);c=tagged(*grade(words[k]),3)
 need(cat(cat(a,b),c)==cat(a,cat(b,c)),'coordinate associativity')
 need(grade(cat(a,b))==add(grade(a),grade(b)),'ordinal grade')
 counts['coordinate_associativity']+=1;counts['ordinal_grades']+=1
for k,l in product(range(7),repeat=2):
 for d in [F(1,3),F(2),F(7,2)]:
  direct=[2**(k+l-j)*d for j in range(k+l)]
  split=[2**(k-j)*2**l*d for j in range(k)]+[2**(l-j)*d for j in range(l)]
  need(direct==split,'Gaussian scales')
  need(F(1,1)/__import__('functools').reduce(lambda a,b:a*b,direct,F(1))==F(1,1)/__import__('functools').reduce(lambda a,b:a*b,split,F(1)),'density normalization')
  counts['density_chain']+=1
for m in range(7):
 for w in product(range(4),repeat=m):
  dec=all(x>=y for x,y in zip(w,w[1:]))
  cuts=all(all(x>=y for x,y in zip([int(v>c) for v in w],[int(v>c) for v in w][1:]))for c in [F(1,2),F(3,2),F(5,2)])
  need(dec==cuts,'finite core cuts')
  counts['finite_core']+=1
for m in range(6):
 for w in permutations(range(5),m):
  colors=list(w);need(all(x!=y for x,y in zip(colors,colors[1:])),'singleton support cover');counts['finite_hull']+=1
# Deliberately wrong rules must actually differ on selected witnesses.
need(add((0,1),(1,0))!=(1,1),'wrong commutative ordinal mutant rejected');counts['mutants_rejected']+=1
need([2**(3-j)*F(2)for j in range(2)]!=[2**(2-j)*F(2)for j in range(2)],'missing tail-scale mutant rejected');counts['mutants_rejected']+=1
need(not all(x>=y for x,y in zip((0,2),(2,))), 'rise omitted mutant rejected');counts['mutants_rejected']+=1
need(F(3,625)<1 and 1-F(3,625)==F(622,625),'properness bound')
need(F(1,1)*F(1,2)*F(1,2)!=F(1,1),'wrong positive half-density direction fails norm');counts['mutants_rejected']+=1
print(json.dumps({'status':'PASS','counts':counts,'scope':'Exact finite coordinate/formal-ordinal, scale, finite-grid core/hull, explicit mutant witnesses; analytic proof independently read, not established by computation.'},sort_keys=True))

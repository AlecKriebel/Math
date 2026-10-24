#!/usr/bin/env python3
from itertools import permutations,product
from collections import defaultdict
from pathlib import Path
import json
PAIRS=((3,2),(20,14),(119,84))
def add(a,b):
 c=dict(a)
 for x,v in b.items():c[x]=c.get(x,0)+v
 return {x:v for x,v in c.items() if v}
def mul(a,b):
 c=defaultdict(int)
 for x,v in a.items():
  for y,w in b.items():c[tuple(i+j for i,j in zip(x,y))]+=v*w
 return {x:v for x,v in c.items() if v}
def det(a):
 out={};n=len(a)
 for p in permutations(range(n)):
  inv=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n));v={(0,0):(-1)**inv}
  for i,j in enumerate(p):
   v=mul(v,a[i][j])
   if not v:break
  out=add(out,v)
 return out

def matrix(types):
 # Normalize the first reflection's phase to 1; remaining two are x,y.
 j0=types.index(1);others=[i for i in range(3) if i!=j0]
 phases=[(0,0)]*3
 for j,k in enumerate(others):phases[k]=tuple(int(i==j) for i in range(2))
 a=[[{} for j in range(6)] for i in range(6)]
 def ins(r,c,e,v):a[r][c]=add(a[r][c],{e:v})
 for i,((p,q),refl,phase) in enumerate(zip(PAIRS,types,phases)):
  neg=tuple(-x for x in phase)
  if refl:
   ins(2*i,1,phase,p);ins(2*i,2,(0,0),-q);ins(2*i,5,phase,1);ins(2*i,4,(0,0),-1)
   ins(2*i+1,0,neg,p);ins(2*i+1,3,(0,0),-q);ins(2*i+1,4,neg,1);ins(2*i+1,5,(0,0),-1)
  else:
   ins(2*i,0,phase,p);ins(2*i,2,(0,0),-q);ins(2*i,4,phase,1);ins(2*i,4,(0,0),-1)
   ins(2*i+1,1,neg,p);ins(2*i+1,3,(0,0),-q);ins(2*i+1,5,neg,1);ins(2*i+1,5,(0,0),-1)
 return a
if __name__=='__main__':
 out=[]
 for ts in product((0,1),repeat=3):
  if not any(ts):continue
  d=det(matrix(ts));row={'types':ts,'terms':[{'exponent':e,'coefficient':v} for e,v in sorted(d.items())]};out.append(row)
  print(ts,len(d),sorted(d.items()))
 Path(__file__).with_name('dihedral_determinants.json').write_text(json.dumps(out,indent=2)+'\n')

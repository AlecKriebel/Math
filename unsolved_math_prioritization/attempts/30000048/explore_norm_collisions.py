"""Exploration: integral averages of irreducible squares modulo small primes."""
from collections import defaultdict
import json,time

def add(a,b,c=1,p=2):
 d=dict(a)
 for k,v in b.items():d[k]=(d.get(k,0)+c*v)%p
 return {k:v for k,v in d.items() if v}
def shift(a,i,j):return {(k+i,l+j):v for (k,l),v in a.items()}
def swap(a):return {(j,i):v for (i,j),v in a.items()}
def mul(a,b,p=2):
 d={}
 for (i,j),v in a.items():
  for (k,l),w in b.items():d[i+k,j+l]=(d.get((i+k,j+l),0)+v*w)%p
 return {k:v for k,v in d.items() if v}
def table(n,p=2):
 cs={(0,0):{(0,0):1}}
 for total in range(1,n+1):
  for a in range(total,0,-1):
   b=total-a
   cs[a,b]=add(add(shift(cs[a-1,b],1,0),cs.get((a-2,b+1),{}),-1,p),cs.get((a-1,b-1),{}),-1,p)
  cs[0,total]=swap(cs[total,0])
 return cs
if __name__=='__main__':
 t=time.time();cs=table(50);by=defaultdict(list)
 for (a,b),p in cs.items():
  if a<b:continue
  norm=mul(p,swap(p));by[tuple(sorted(norm.items()))].append((a,b))
 print(json.dumps({'bound':50,'distinct_up_to_conjugation':sum(a>=b for a,b in cs),'collisions':[vs for vs in by.values() if len(vs)>1],'seconds':time.time()-t},indent=2))

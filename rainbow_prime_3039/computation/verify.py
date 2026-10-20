"""Independent brute-force validator; exhaustive restricted-growth enumeration at primes 5,7,11,13,17.
Unlike C++ search, use no affine reduction or domain propagation.
"""
import json,sys,itertools,time
from pathlib import Path

def violations(c):
 p=len(c)
 return [(a,d) for a in range(p) for d in range(1,p) if len({c[(a+j*d)%p] for j in range(4)})==4]

def brute(p):
 lo,hi=p//4,(p+3)//4
 edges={tuple(sorted((a+j*d)%p for j in range(4))) for a in range(p) for d in range(1,p)}
 ending=[[] for _ in range(p)]
 for e in edges:ending[max(e)].append(e)
 c=[0]*p;counts=[1,0,0,0];nodes=0;sol=None
 def rec(i,m):
  nonlocal nodes,sol
  nodes+=1
  if i==p:
   if min(counts)>=lo:sol=c.copy();return True
   return False
  for b in range(min(m+1,3)+1):
   if counts[b]>=hi:continue
   c[i]=b;counts[b]+=1
   if sum(max(0,lo-n) for n in counts)<=p-i-1 and all(len({c[j] for j in e})<4 for e in ending[i]):
    if rec(i+1,max(m,b)):return True
   counts[b]-=1
  return False
 start=time.monotonic();sat=rec(1,0)
 return dict(p=p,status='SAT' if sat else 'UNSAT_EXHAUSTIVE',nodes=nodes,seconds=time.monotonic()-start,coloring=sol)
if __name__=='__main__':
 if '--brute' in sys.argv:
  for p in [5,7,11,13,17]:print(json.dumps(brute(p)),flush=True)
 else:
  for line in Path(sys.argv[1]).read_text().splitlines():
   r=json.loads(line)
   if r['status']=='SAT':
    c=r['coloring'];p=len(c);assert len(c)==r['p'];assert set(c)==set(range(4));assert all(r.get("min_size",p//4)<=c.count(b)<=r.get("max_size",(p+3)//4) for b in range(4));assert not violations(c)
  print('All supplied SAT witnesses verified against every ordered (a,d), d nonzero.')

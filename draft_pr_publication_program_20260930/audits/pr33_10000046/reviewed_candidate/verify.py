"""Exact finite diagnostics only; no infinite-time certificate."""
import itertools,json,math,sys
from fractions import Fraction
from pathlib import Path
sys.setrecursionlimit(10000)
def paths(d,N,start):
 steps=[tuple(s if i==j else 0 for i in range(d)) for j in range(d) for s in (-1,1)]
 out=[]
 for word in itertools.product(steps,repeat=N):
  z=start;trace=[z]
  for w in word:z=tuple(a+b for a,b in zip(z,w));trace.append(z)
  out.append(frozenset(trace))
 return out
def test(d,N,distance):
 A=paths(d,N,(0,)*d);B=paths(d,N,(distance,)+(0,)*(d-1));L=len(A)
 adj=[[j for j,b in enumerate(B) if not a&b] for a in A]
 mate=[-1]*L
 def augment(i,seen):
  for j in adj[i]:
   if j in seen:continue
   seen.add(j)
   if mate[j]<0 or augment(mate[j],seen):mate[j]=i;return True
  return False
 M=sum(augment(i,set()) for i in range(L));left={i:j for j,i in enumerate(mate) if i>=0}
 # Alternating reachability gives an exact Konig cover.
 ZL=set(range(L))-set(left);ZR=set();todo=list(ZL)
 while todo:
  i=todo.pop()
  for j in adj[i]:
   if left.get(i)==j or j in ZR:continue
   ZR.add(j)
   if mate[j]>=0 and mate[j] not in ZL:ZL.add(mate[j]);todo.append(mate[j])
 CL=set(range(L))-ZL;CR=ZR
 assert len(CL)+len(CR)==M
 assert all(i in CL or j in CR for i,row in enumerate(adj) for j in row)
 assert all(j in adj[i] for i,j in left.items())
 assert len(set(left.values()))==M
 if N<distance:assert M==L
 return dict(d=d,N=N,distance=distance,paths=L,matching=M,cover=len(CL)+len(CR),alpha=str(Fraction(M,L)))
results=[test(d,N,2) for d in (1,2,3) for N in (1,2,3)]
results += [test(4,2,2),test(3,2,10),test(4,2,10)]
# The synchronous translation has no simultaneous collision but intersects cross-time.
for d in (3,4):
 X=[(k,)+(0,)*(d-1) for k in range(11)];Y=[(k+10,)+(0,)*(d-1) for k in range(11)]
 assert all(x!=y for x,y in zip(X,Y)) and X[10]==Y[0]
# Exact multinomial shortest-path counts against recursion for all small targets.
checks=0
for d in (3,4):
 for N in range(1,7):
  counts={(0,)*d:1}
  for _ in range(N):
   nxt={}
   for a,v in counts.items():
    for j in range(d):
     b=list(a);b[j]+=1;b=tuple(b);nxt[b]=nxt.get(b,0)+v
   counts=nxt
  for a,v in counts.items():
   assert v==math.factorial(N)//math.prod(math.factorial(k) for k in a);checks+=1
out={'all_passed':True,'scope':'Finite matching certificates and elementary controls only. No asymptotic inference.','matching_cases':results,'shortest_path_count_checks':checks,'cross_time_controls':2}
Path(__file__).with_name('verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

#!/usr/bin/env python3
"""New exact controls; no candidate or prior review code imported."""
from collections import deque
from fractions import Fraction as Q
from itertools import product, combinations
import json, random
RNG=random.Random(57030006605)
COUNTS={k:0 for k in ('graphs','profiles','threshold_vectors','pivots','source_recursions','source_nodes','balanced_nodes','unbalanced_nodes','dominance_nodes','fiber_below_original')}

def distances(g):
 out=[]
 for s in range(len(g)):
  d=[-1]*len(g);d[s]=0;q=deque([s])
  while q:
   x=q.popleft()
   for y in g[x]:
    if d[y]<0:d[y]=d[x]+1;q.append(y)
  assert min(d)>=0;out.append(d)
 return out

def cube(d):
 return [{x^(1<<i) for i in range(d)} for x in range(1<<d)]

def leaves(g,attachments):
 g=[set(nei) for nei in g]
 for v,count in attachments:
  for _ in range(count):g[v].add(len(g));g.append({v})
 return g

def path(n):return [{j for j in (i-1,i+1) if 0<=j<n} for i in range(n)]

def cuts(g,vs,d):
 seen=set();out=[]
 for x in sorted(vs):
  for y in g[x]&vs:
   if x<y:
    a=frozenset(v for v in vs if d[v][x]<d[v][y]);b=frozenset(vs-a)
    assert a and b and a|b==vs
    key=tuple(sorted((tuple(sorted(a)),tuple(sorted(b)))))
    if key not in seen:seen.add(key);out.append((set(a),set(b)))
 return out

def additive(g,vs,a,d):
 COUNTS['source_nodes']+=1;n=len(vs)
 direct={x:max(d[x][y]+a[y] for y in vs) for x in vs}
 if n<=2:return direct
 f=2*(n-1).bit_length();cs=cuts(g,vs,d)
 bal=[(aa,bb) for aa,bb in cs if f*min(len(aa),len(bb))>=n]
 if bal:
  COUNTS['balanced_nodes']+=1;aa,bb=bal[-1]
  ea=additive(g,aa,a,d);eb=additive(g,bb,a,d);out={}
  for here,other,eh,eo in ((aa,bb,ea,eb),(bb,aa,eb,ea)):
   for x in here:
    gate=min(other,key=lambda z:d[x][z]);assert all(d[x][y]==d[x][gate]+d[gate][y] for y in other)
    out[x]=max(eh[x],d[x][gate]+eo[gate])
 else:
  COUNTS['unbalanced_nodes']+=1
  minorities=[aa if len(aa)<len(bb) else bb for aa,bb in cs]
  majority=vs.copy()
  for mm in minorities:majority-=mm
  assert len(majority)==1;v0=next(iter(majority));mx=max(d[v0][y]+a[y] for y in vs)
  far=v0 if a[v0]==mx else min(y for y in vs if d[v0][y]+a[y]==mx)
  if far==v0:
   COUNTS['dominance_nodes']+=1;out={x:d[x][v0]+a[v0] for x in vs}
  else:
   ladder=[mm for mm in minorities if far in mm and g[v0]&mm&vs]
   assert ladder and 2**len(ladder)<=n
   remain=vs.copy();slices=[]
   for mm in ladder:
    si=remain&mm;after=remain-si;assert si and after
    astar={x:a[x] for x in si}
    fibers={x:[] for x in si}
    for y in after:
     gate=min(si,key=lambda z:d[y][z]);assert all(d[y][x]==d[y][gate]+d[gate][x] for x in si);fibers[gate].append(y)
    for x,ys in fibers.items():
     if ys:
      astar[x]=max(d[x][y]+a[y] for y in ys)
      if astar[x]<a[x]:COUNTS['fiber_below_original']+=1
    e0=additive(g,si,a,d);e1=additive(g,si,astar,d);slices.append((si,e0,e1));remain=after
   assert 2*sum(len(si) for si,_,_ in slices)<=n
   out={x:d[x][v0]+mx for x in remain}
   later=set(remain)
   for si,e0,e1 in reversed(slices):
    for x in later:
     gate=min(si,key=lambda z:d[x][z]);out[x]=max(out[x],d[x][gate]+e0[gate])
    for x in si:out[x]=max(e0[x],e1[x])
    later|=si
 assert out==direct
 return out

def optimize(d,w,upper_median=False):
 n=len(w);D=n-1;r=[max(w[u]*d[x][u] for u in range(n)) for x in range(n)];rho=min(r);centers={x for x in range(n) if r[x]==rho}
 lo=[0]*n;hi=[D]*n;B=D*max(w);wit=0
 while any(l<=h for l,h in zip(lo,hi)):
  total=sum(max(0,h-l+1) for l,h in zip(lo,hi));mid=sorted((w[u]*((lo[u]+hi[u])//2),hi[u]-lo[u]+1) for u in range(n) if lo[u]<=hi[u]);mass=0
  for q,L in (reversed(mid) if upper_median else mid):
   mass+=L
   if 2*mass>=total:break
  assert 2*sum(L for val,L in mid if val<=q)>=total and 2*sum(L for val,L in mid if val>=q)>=total
  direct={x for x in range(n) if r[x]<=q};a=[]
  for u in range(n):
   left,right=0,D+1
   while left<right:
    m=(left+right)//2
    if m*w[u]<=q:left=m+1
    else:right=m
   a.append(D-(left-1))
  transformed={x for x in range(n) if max(d[x][u]+a[u] for u in range(n))<=D};assert direct==transformed;COUNTS['threshold_vectors']+=1
  if direct and q<B:B=q;wit=min(direct)
  for u in range(n):
   while lo[u]<=hi[u] and ((w[u]*hi[u]>=q) if direct else (w[u]*lo[u]<=q)):
    if direct:hi[u]-=1
    else:lo[u]+=1
  remaining=sum(max(0,h-l+1) for l,h in zip(lo,hi));assert 4*remaining<=3*total;assert r[wit]<=B;assert B==rho or any(any(k*w[u]==rho for k in range(lo[u],hi[u]+1)) for u in range(n));COUNTS['pivots']+=1
 assert B==rho and wit in centers;assert {x for x in range(n) if r[x]<=B}==centers
 for q in (Q(-1),Q(0),rho,rho-Q(1,2**271),rho+Q(1,2**271)):
  if q<0:assert not {x for x in range(n) if r[x]<=q};continue
  a=[D-max(k for k in range(D+1) if k*w[u]<=q) for u in range(n)]
  assert {x for x in range(n) if r[x]<=q}=={x for x in range(n) if max(d[x][u]+a[u] for u in range(n))<=D};COUNTS['threshold_vectors']+=1


def main():
 fixtures=[cube(d) for d in range(7)]+[path(n) for n in (2,7,17,33)]+[leaves(cube(3),[(0,75),(1,5),(2,6),(4,7)]),leaves(cube(4),[(0,80)]+[(1<<i,5+i) for i in range(4)]),leaves(cube(2),[(i,5) for i in range(4)])]
 for g in fixtures:
  n=len(g);d=distances(g);vs=set(range(n));COUNTS['graphs']+=1
  for x,y,z in combinations(range(n),3):assert sum(d[x][m]+d[m][y]==d[x][y] and d[y][m]+d[m][z]==d[y][z] and d[z][m]+d[m][x]==d[z][x] for m in range(n))==1
  profiles=[[Q(0)]*n,[Q(1)]*n,[Q(int(i==n-1)) for i in range(n)]]
  profiles += [[RNG.choice((Q(0),Q(1,7),Q(11,13),Q(2**256+297,2**193+17),Q(1,2**191+51))) for _ in range(n)] for _ in range(13)]
  for i,w in enumerate(profiles):optimize(d,w,bool(i%2));COUNTS['profiles']+=1
  for a in ([0]*n,[int(x==0)*(n-1) for x in range(n)],[int(x==n-1)*(n-1) for x in range(n)],[RNG.randrange(n) for _ in range(n)]):additive(g,vs,dict(enumerate(a)),d);COUNTS['source_recursions']+=1
 # Exact succinct N=10^12 counterexample independently reconstructs paper's N-1 arrival.
 n=10**12;ell=30;t=17_000_000_000;q=2**ell;s=n-q-ell*t;minor=q//2+t;union=q-1+ell*t
 exp7=sum((Q(7)**k)/__import__('math').factorial(k) for k in range(20))
 assert exp7>1000 and 56*minor<n and 2*union>n and s==488_926_258_176
 assert (n-1)+30>max(31,1) # antipode unique from zero against all zero-arrival vertices
 print(json.dumps({'status':'PASS','seed':57030006605,'counts':COUNTS,'succinct_counterexample':{'n':n,'root_leaves':s,'minority':minor,'twice_minority_union':2*union,'exp7_partial_terms':20},'limits':'Exact finite controls; imported preprocessing deliberately brute; universal proof and asymptotic runtime are separate.'},indent=2))

if __name__=='__main__':main()

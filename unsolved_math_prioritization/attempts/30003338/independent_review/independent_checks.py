#!/usr/bin/env python3
"""Independent audit controls. No author module imports; integer arithmetic."""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
import json,hashlib,sys
AUTHOR=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
counts=Counter()
def ck(v,k):
 assert v,k;counts[k]+=1

def direct(n,edges,q):
 adj=[[] for _ in range(n)]
 for a,b in edges:adj[a].append(b);adj[b].append(a)
 out=[];c=[-1]*n
 def rec(i):
  if i==n:out.append(tuple(c));return
  used={c[j] for j in adj[i] if j<i}
  for x in range(q):
   if x not in used:c[i]=x;rec(i+1)
  c[i]=-1
 rec(0);return out

def zero_mask(c,n):return sum((c[i]==0)<<i for i in range(n))
def all_upsets(n):
 N=1<<n;out=[]
 for e in range(1<<N):
  if all(not(e>>s&1) or all(e>>(s|(1<<j))&1 for j in range(n) if not(s>>j&1)) for s in range(N)):
   out.append(tuple(s for s in range(N) if e>>s&1))
 return out

# Independent full-coloring reconstruction of the side-four family.
u=[52,12,20,4,12,8,12,8,12,8,12,8,8,16,0,0]
v=[80,16,0,0,0,0,0,0,0,0,0,0,0,0,16,32]
for m in range(1,6):
 masks=[9,12,10,5,6]+[14]*m
 edges=[(a,4+b) for b,N in enumerate(masks) for a in range(4) if N>>a&1]
 c=direct(4+len(masks),edges,3);w=Counter(zero_mask(f,4) for f in c)
 ck([w[s] for s in range(16)]==[u[s]+2**m*v[s] for s in range(16)],'side4_full_colorings')
 ck(len(c)==192+144*2**m,'side4_totals')
U4=all_upsets(4);ck(len(U4)==168,'upset_count')
# Reconstruct coefficient triples from three values rather than the author's
# symbolic-expansion formula. Direct truth-table enumeration yields U4.
hist=Counter()
for i,E in enumerate(U4):
 for F in U4[i:]:
  EF=set(E)&set(F);vals=[]
  for t in [2,3,4]:
   w=[a+t*b for a,b in zip(u,v)];z=sum(w)
   vals.append(z*sum(w[s] for s in EF)-sum(w[s] for s in E)*sum(w[s] for s in F))
  second=vals[2]-2*vals[1]+vals[0];ck(second%2==0,'coefficient_integrality')
  a=second//2;b=vals[1]-vals[0]-a;c=vals[0]
  ck(min(a,b,c)>=0,'coefficient_nonnegativity');hist[(a,b,c)]+=1
saved=json.loads((AUTHOR/'TURN_4_COEFFICIENT_CERTIFICATE.json').read_text())
ck(Counter({tuple(r[:3]):r[3] for r in saved})==hist,'coefficient_histogram')

# Universal Kempe claim and three-coordinate association: all labeled
# bipartite graphs with 3+3 vertices, q=3. Enumerate full proper colorings.
U3=all_upsets(3)
for graph in range(512):
 edges=[(a,3+b) for a in range(3) for b in range(3) if graph>>(3*a+b)&1]
 colorings=direct(6,edges,3);Z=len(colorings);weights=Counter(zero_mask(f,3) for f in colorings)
 for i in range(3):
  target={c for c in colorings if c[i]==0}
  for label in [1,2]:
   image=[]
   for f in colorings:
    if f[i]!=label:continue
    component={i};change=True
    while change:
     change=False
     for a,b in edges:
      if f[a] not in [0,label] or f[b] not in [0,label]:continue
      if (a in component)!=(b in component):component|={a,b};change=True
    g=tuple(label-f[j] if j in component else f[j] for j in range(6))
    ck(zero_mask(f,3)&~zero_mask(g,3)==0,'kempe_monotonicity')
    ck(all(g[a]!=g[b] for a,b in edges),'kempe_properness');image.append(g)
   ck(len(image)==len(set(image)) and set(image)==target,'kempe_bijection')
 for i,E in enumerate(U3):
  for F in U3[i:]:
   mE=sum(weights[s] for s in E);mF=sum(weights[s] for s in F);mEF=sum(weights[s] for s in set(E)&set(F))
   ck(mEF*Z>=mE*mF,'three_coordinate_event_pairs')

# Conditional subdivision representation on a latent multigraph, including
# parallel edges and an isolated original vertex, absent from author K4 controls.
H=[(0,1),(0,1),(1,2),(2,0)];n=4;m=len(H)
edges=[(i,n+e) for e,(a,b) in enumerate(H) for i in (a,b)]
def components(mask):
 parent=list(range(n))
 def root(i):
  while parent[i]!=i:i=parent[i]
  return i
 for e,(a,b) in enumerate(H):
  if mask>>e&1:parent[root(a)]=root(b)
 return [set(i for i in range(n) if root(i)==r) for r in set(root(i) for i in range(n))]
for q in [3,4]:
 colorings=direct(n+m,edges,q);a=q-2;r=q-1
 for W in range(1<<n):
  J=[e for e,(x,y) in enumerate(H) if W>>x&1 and W>>y&1]
  direct_dist=Counter(sum((f[n+e]==0)<<e for e in J) for f in colorings if all(f[i]!=0 for i in range(n) if W>>i&1))
  bonds=Counter();bondweights=[]
  for eta in range(1<<m):
   k1=sum(any(W>>i&1 for i in C) for C in components(eta));k0=len(components(eta))-k1
   cluster=r**k1*q**k0;closedJ=[e for e in J if not eta>>e&1]
   outside=sum(not(eta>>e&1) for e in range(m) if e not in J)
   bondweights.append(cluster*a**(m-eta.bit_count()))
   for bits in range(1<<len(closedJ)):
    retained=sum(1<<e for j,e in enumerate(closedJ) if bits>>j&1)
    bonds[retained]+=cluster*a**outside*(a-1)**(len(closedJ)-bits.bit_count())
  ck(all(direct_dist[s]==bonds[s] for s in range(1<<m)),'subdivision_polynomial')
  for S in range(1<<m):
   for T in range(1<<m):
    ck(bondweights[S&T]*bondweights[S|T]>=bondweights[S]*bondweights[T],'marked_bond_lattice')

print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'breakdown':dict(counts),'scope':'Independent controls only; universal claims are audited by their written arguments. 512 graphs on fixed 3+3 vertices, five members of the side-four family, all 14,196 coefficient pairs, and one multigraph subdivision with an isolated vertex.'},indent=2,sort_keys=True))

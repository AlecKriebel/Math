from random import Random
from collections import deque
import json
r=Random(3000058);checks=0

def ck(x):
 global checks;checks+=1;assert x

def instance(n,cyclic):
 edges=[(i,r.randrange(i)) for i in range(1,n)]
 if cyclic:
  if n==2:edges.append((0,1))
  else:
   existing={tuple(sorted(e)) for e in edges};pairs=[(i,j) for i in range(n) for j in range(i) if (j,i) not in existing];edges.append(r.choice(pairs))
 H=[[] for _ in range(n)];adj=[[] for _ in range(n)];a=[1]*len(edges)
 for k,(i,j) in enumerate(edges):H[i].append(k);H[j].append(k);adj[i].append((j,k));adj[j].append((i,k))
 required=None;root=r.randrange(n)
 if not cyclic:
  required=len(a);a.append(1);H[root].append(required)
 for i in range(n):
  for _ in range(max(0,2-len(H[i]))+r.randrange(3)):
   H[i].append(len(a));a.append(0)
 ck(all(len(h)>=2 for h in H))
 if cyclic:
  deg=[len(x) for x in adj];q=deque(i for i in range(n) if deg[i]==1);live=set(range(n))
  while q:
   i=q.popleft();live.remove(i)
   for j,k in adj[i]:
    if j in live:
     deg[j]-=1
     if deg[j]==1:q.append(j)
  ce=[k for k,(i,j) in enumerate(edges) if i in live and j in live];roots=list(live)
 else:ce=[];roots=[root]
 depth={i:0 for i in roots};q=deque(roots)
 while q:
  i=q.popleft()
  for j,k in adj[i]:
   if j not in depth:depth[j]=depth[i]+1;q.append(j)
 weights=[[-n-100]*len(a) for _ in range(2)]
 for k,(i,j) in enumerate(edges):
  if k not in ce:
   for w in weights:w[k]=-max(depth[i],depth[j])
 for j,k in enumerate(ce):weights[0][k]=j+1;weights[1][k]=len(ce)-j
 if required is not None:
  for w in weights:w[required]=0
 out=[]
 for w in weights:
  counts=[0]*len(a)
  for h in H:
   top=max(w[k] for k in h);winners=[k for k in h if w[k]==top];ck(len(winners)==1);counts[winners[0]]+=1
  v=[x-y for x,y in zip(counts,a)];ck(sum(v)==0);out.append(v)
 ck(all(x+y==0 for x,y in zip(*out)))
 for k in range(len(a)):
  d=sum(k in h for h in H);ck(d<=2);ck(-1<=-a[k] and d-a[k]<=1)
 return len(a)
cases=0;mx=0
for n in range(1,31):
 for cyc in [False,True]:
  if cyc and n<2:continue
  for _ in range(20):mx=max(mx,instance(n,cyc));cases+=1
print(json.dumps({'assertions':checks,'instances':cases,'max_coordinates':mx,'scope':'Exact exposing-weight and opposite-vertex controls; general proof in TURN_4.md.'},indent=2))

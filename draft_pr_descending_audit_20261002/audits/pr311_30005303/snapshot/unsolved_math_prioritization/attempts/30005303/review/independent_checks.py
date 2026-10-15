import itertools,json,random
from collections import deque
count=0
# Exhaust every nonempty Boolean 4-cube sublattice and every graph.
n=4; X=list(range(1<<n)); edges=list(itertools.combinations(range(n),2))
def bit(x,i):return (x>>i)&1
sublattices=0; factorizable=0
for mask in range(1,1<<len(X)):
 S=[x for x in X if mask>>x&1]; SS=set(S)
 if any(x&y not in SS or x|y not in SS for x in S for y in S):continue
 sublattices+=1
 unary=[{bit(x,i) for x in S} for i in range(n)]
 for gm in range(1<<len(edges)):
  E=[e for k,e in enumerate(edges) if gm>>k&1]
  proj={e:{(bit(x,e[0]),bit(x,e[1])) for x in S} for e in E}
  T={x for x in X if all(bit(x,i) in unary[i] for i in range(n)) and all((bit(x,i),bit(x,j)) in proj[i,j] for i,j in E)}
  if T!=SS:continue
  factorizable+=1; implications=[]
  for i,j in E:
   if len(unary[i])==len(unary[j])==2:
    if (1,0) not in proj[i,j]:implications.append((i,j))
    if (0,1) not in proj[i,j]:implications.append((j,i))
  R={x for x in X if all(bit(x,i) in unary[i] for i in range(n)) and all(bit(x,i)<=bit(x,j) for i,j in implications)}
  assert R==SS;count+=1
# Independent max-flow residual test for random integer attractive energies.
rng=random.Random(5303)
for trial in range(1000):
 n=rng.randrange(1,8);h=[rng.randrange(-9,10) for _ in range(n)]
 J={(i,j):rng.randrange(10) for i in range(n) for j in range(i+1,n) if rng.randrange(2)}
 N=n+2;s=n;t=n+1; cap=[[0]*N for _ in range(N)];b=[-a for a in h]
 for (i,j),w in J.items():cap[i][j]=w;b[i]-=w
 for i,v in enumerate(b):
  if v>=0:cap[i][t]=v
  else:cap[s][i]=-v
 res=[r[:] for r in cap];flow=0
 while True:
  prev=[None]*N;prev[s]=s;q=deque([s])
  while q and prev[t] is None:
   u=q.popleft()
   for v in range(N):
    if res[u][v]>0 and prev[v] is None:prev[v]=u;q.append(v)
  if prev[t] is None:break
  v=t;d=10**9
  while v!=s:u=prev[v];d=min(d,res[u][v]);v=u
  v=t
  while v!=s:u=prev[v];res[u][v]-=d;res[v][u]+=d;v=u
  flow+=d
 energies={x:-sum(h[i]*bit(x,i) for i in range(n))-sum(w*bit(x,i)*bit(x,j) for (i,j),w in J.items()) for x in range(1<<n)}
 emin=min(energies.values())
 for x,E in energies.items():
  S={s}|{i for i in range(n) if bit(x,i)}
  rc=sum(res[u][v] for u in S for v in range(N) if v not in S)
  assert rc==E-emin;count+=1
  assert all(res[i][j]==0 for i in range(n) for j in range(n) if i!=j and (min(i,j),max(i,j)) not in J);count+=1
print(json.dumps({'assertions':count,'sublattices_n4':sublattices,'factorizable_support_graph_pairs':factorizable,'residual_networks':1000},sort_keys=True))

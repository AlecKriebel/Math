N=20
E={tuple(sorted(e)) for i in range(10) for e in [(i,(i+1)%10),(i,10+i),(10+i,10+(i+2)%10)]}
adj=[set() for _ in range(N)]
for u,v in E:adj[u].add(v);adj[v].add(u)
def matchings(rem,M):
 if not rem:yield M;return
 u=min(rem)
 for v in adj[u]&rem:yield from matchings(rem-{u,v},M+[(u,v)])
res=[]
for M in matchings(set(range(N)),[]):
 S=E-{tuple(sorted(e)) for e in M}; sa=[set() for _ in range(N)]
 for u,v in S:sa[u].add(v);sa[v].add(u)
 b={};cy=[];ok=True
 for u in range(N):
  if u in b:continue
  vs=[u];b[u]=0
  for v in vs:
   for w in sa[v]:
    if w in b:
     if b[w]==b[v]:ok=False
    else:b[w]=1-b[v];vs.append(w)
  cy.append(vs)
 if not ok:continue
 for mask in range(1<<(len(cy)-1)):
  bb=b.copy()
  for j,vs in enumerate(cy[1:]):
   if mask>>j&1:
    for v in vs:bb[v]^=1
  L=[(u,v) for u,v in M if bb[u]==bb[v]]
  short=E-{tuple(sorted(e)) for e in L};h=[set() for _ in range(N)]
  for u,v in short:h[u].add(v);h[v].add(u)
  endpoints={v for e in L for v in e}; parent=list(range(N))
  def find(x):
   while parent[x]!=x:x=parent[x]
   return x
  for u in endpoints:
   near=h[u]|{w for v in h[u] for w in h[v]}
   for v in near&endpoints:parent[find(v)]=find(u)
  impossible=any(find(u)==find(v) for u,v in L)
  res.append((M,cy,bb,L,impossible))
print('even matching / b configs',len(res),'DSU contradictions',sum(r[-1] for r in res))
for r in res[:1]:print(r)
M,cy,b,L,_=res[0]
short=E-{tuple(sorted(e)) for e in L};h=[set() for _ in range(N)]
for u,v in short:h[u].add(v);h[v].add(u)
eps={v for e in L for v in e}; q=[L[0][0]];pred={q[0]:None};wits={}
for u in q:
 for v in eps:
  w=next(iter(h[u]&h[v]),None)
  if v not in pred and (v in h[u] or w is not None):
   pred[v]=u;q.append(v);wits[u,v]=[u,v] if v in h[u] else [u,w,v]
v=L[0][1];chain=[]
while pred[v] is not None:
 u=pred[v];chain.append(wits[u,v]);v=u
print('certificate',chain[::-1])
# follow actual cycle
S=E-{tuple(sorted(e)) for e in M}; path=[0];prev=-1
while len(path)<N:
 u=path[-1];v=next(v for v in adj[u] if tuple(sorted((u,v))) in S and v!=prev and v not in path)
 prev=u;path.append(v)
print('Hamilton cycle',path)

def bounded_phase_possible(M, b, W):
 L=[(u,v) for u,v in M if b[u]==b[v]]
 for signs in range(1<<len(L)):
  # Arc (u,v,w) means phi[v] <= phi[u]+w.
  arcs=[]
  for u,v in E:
   if (u,v) not in L and (v,u) not in L:arcs.extend([(u,v,3),(v,u,3)])
  for j,(u,v) in enumerate(L):
   if signs>>j&1:u,v=v,u
   arcs.append((v,u,-7))
  for v in range(N):arcs.extend([(N,v,W),(v,N,0)])
  d=[0]*(N+1)
  for iteration in range(N+1):
   changed=False
   for u,v,w in arcs:
    if d[v]>d[u]+w:d[v]=d[u]+w;changed=True
   if not changed:return True
 return False

assert len(res)==30
assert all(r[-1] for r in res)
assert all(not bounded_phase_possible(M,b,8) for M,cy,b,L,_ in res)
phi=[7,0,1,8,9,2,5,8,1,4,7,3,4,5,6,2,3,9,0,6]
M,cy,b,L,_=res[0]
colors=[(10*b[v]+phi[v])%20 for v in range(N)]
assert all(7 <= (colors[u]-colors[v])%20 <= 13 for u,v in E)
print('Exact difference-constraint check: all 30 choices infeasible at width 8.')
print('Verified width-9 phases:',phi)
print('Verified (20,7) colors:',colors)

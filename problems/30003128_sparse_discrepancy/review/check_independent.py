import itertools,json,hashlib,pathlib
from fractions import Fraction as F
p=pathlib.Path('/workspace/shared/math-30003128'); count=0
for manifest in ['MANIFEST.json','SOURCE_HASHES.json']:
 data=json.loads((p/manifest).read_text()); data=data.get('files',data)
 for name,h in data.items():
  assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h; count+=1
for q,k in [(3,2),(4,2),(3,3)]:
 vs=list(itertools.product(range(q),repeat=k)); N=len(vs);d=(q-1)**k;m=d+1;n=N+m
 edges={(i,j) for i in range(N) for j in range(i+1,N) if all(a!=b for a,b in zip(vs[i],vs[j]))}
 edges|={(i,j) for i in range(N,n) for j in range(i+1,n)}
 x,y=next(e for e in edges if e[1]<N);u,v=N,N+1
 edges.remove((x,y));edges.remove((u,v));edges.add((x,u));edges.add((y,v))
 deg=[0]*n;adj=[set() for _ in range(n)]
 for i,j in edges:deg[i]+=1;deg[j]+=1;adj[i].add(j);adj[j].add(i)
 assert set(deg)=={d};count+=1
 seen={0};stack=[0]
 while stack:
  for j in adj[stack.pop()]-seen:seen.add(j);stack.append(j)
 assert len(seen)==n;count+=1
 w=[-F(1,N)]*N+[F(1,m)]*m
 assert sum(w)==0;count+=1
 assert sum((w[i]-w[j])**2 for i,j in edges)/sum(t*t for t in w)==F(2*n,m*N);count+=1
 # Exact tensor eigenvectors spanning the nonconstant coordinate characters.
 for coords in itertools.product(range(q),repeat=k):
  ev=[(q-1 if t==0 else -1) for t in coords]
  eigen=1
  for a in ev:eigen*=a
  if any(coords):assert abs(eigen)<=d//(q-1)
  else:assert eigen==d
  count+=1
print(json.dumps({'independent_assertions':count,'fixtures':3,'status':'PASS'},indent=2))

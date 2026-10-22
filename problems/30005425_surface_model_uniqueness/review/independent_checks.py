import itertools,json
count=0;models=0
for k in range(1,11):
 for eps in itertools.product(range(2),repeat=k):
  edges=[];forbid=set()
  for j in range(k):
   z=4*j;o=len(edges)
   edges.extend([(z,z+1),(z,z+2),(z+1,z+2),(z+1,z+3),(z+2,z+3)])
   forbid.add((o,o+2));forbid.add((o+1 if eps[j]==0 else o+2,o+4))
  for j in range(k-1):
   q=len(edges);edges.append((4*j+3,4*j+4));forbid.update([(5*j+4,q),(q,5*(j+1)+1)])
  succ={};pred={};m=len(edges)
  for a,(u,v) in enumerate(edges):
   for b,(w,t) in enumerate(edges):
    if v==w and (a,b) not in forbid:
     assert a not in succ and b not in pred;count+=1;succ[a]=b;pred[b]=a
  paths=[]
  for a in range(m):
   if a in pred:continue
   path=[edges[a][0],edges[a][1]];b=a;seen={a}
   while b in succ:
    b=succ[b];assert b not in seen;count+=1;seen.add(b);path.append(edges[b][1])
   paths.append(path)
  assert sum(len(p)-1 for p in paths)==m;count+=1
  dim=4*k+sum((len(p)-1)*len(p)//2 for p in paths)
  assert dim==(9*k*k+13*k)//2;count+=1
  sigma={};occ={};d=0
  for p in paths:
   ids=list(range(d,d+len(p)));d+=len(p)
   for i,v in enumerate(p):sigma[ids[i]]=ids[(i+1)%len(p)];occ.setdefault(v,[]).append(ids[i])
  assert len(occ)==4*k and all(len(v)==2 for v in occ.values());count+=1
  alpha={}
  for a,b in occ.values():alpha[a]=b;alpha[b]=a
  perm={a:sigma[alpha[a]] for a in alpha};remaining=set(perm);bdy=0
  while remaining:
   bdy+=1;a=next(iter(remaining))
   while a in remaining:remaining.remove(a);a=perm[a]
  chi=len(paths)-4*k
  assert bdy==2*k+1-2*sum(eps);count+=1
  assert 2-2*sum(eps)-bdy==chi;count+=1;models+=1
# Local completion enumeration, independently compare all tables and 2x2 permutations.
local=0
for p,q in itertools.product(range(3),repeat=2):
 cells=list(itertools.product(range(p),range(q)))
 for bits in itertools.product(range(2),repeat=len(cells)):
  T=dict(zip(cells,bits))
  good=all(sum(T[i,j]==s for j in range(q))<=1 for i in range(p) for s in (0,1)) and all(sum(T[i,j]==s for i in range(p))<=1 for j in range(q) for s in (0,1))
  extension=any(all(T[i,j]==int((i==j)==bool(diag)) for i,j in cells) for diag in (0,1))
  assert good==extension;count+=1;local+=1
print(json.dumps({'status':'PASS','assertions':count,'family_models':models,'local_tables':local},sort_keys=True))

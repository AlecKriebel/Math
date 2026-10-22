import itertools,json
checks=0
def ck(x):
 global checks
 checks+=1;assert x
valid=0;prefix_counts=[0]*4
for labeling in itertools.product((-1,0,1),repeat=8):
 support=[x for x in range(8) if labeling[x]>=0]
 good=all(labeling[x]<=labeling[y] for x in support for y in support if x&y==x)
 P=[x for x in support if labeling[x]==1]
 H=lambda y:any(x&y==x for x in P)
 ck(good==all(H(x)==bool(labeling[x]) for x in support))
 if not good:continue
 valid+=1
 for N in range(4):
  mask=(1<<N)-1
  if all((x&mask)&(y&mask)!=(x&mask) for x in P for y in support if labeling[y]==0):break
 else:raise AssertionError
 prefix_counts[N]+=1
 HH=lambda y:any((x&mask)&y==(x&mask) for x in P)
 for x in support:ck(HH(x&mask)==bool(labeling[x]))
 for x,y in itertools.product(range(1<<N),repeat=2):
  if x&y==x:ck(HH(x)<=HH(y))
noninjective=0
for g in itertools.product(range(4),repeat=4):
 for f in itertools.product(range(2),repeat=4):
  good=all(f[a]<=f[b] for a,b in itertools.product(range(4),repeat=2) if g[a]&g[b]==g[a])
  h=lambda y:any(f[a] and g[a]&y==g[a] for a in range(4))
  ck(good==all(h(g[a])==bool(f[a]) for a in range(4)))
  if good and len(set(g))<4:noninjective+=1
print(json.dumps({'assertions':checks,'cube_partial_labelings':3**8,'extendible_labelings':valid,'least_prefix_counts':prefix_counts,'general_map_pairs':4**4*2**4,'compatible_noninjective_pairs':noninjective},indent=2))

import itertools,json
checks=0
def ck(x):
 global checks
 checks+=1;assert x

def posets(n):
 pairs=list(itertools.combinations(range(n),2));out=[]
 for v in itertools.product(range(3),repeat=len(pairs)):
  r={(i,i) for i in range(n)}
  for (i,j),x in zip(pairs,v):
   if x:r.add((i,j) if x==1 else (j,i))
  if all((a,c) in r for a,b in r for b1,c in r if b==b1):out.append(frozenset(r))
 return out
counts=[]
for n in range(1,5):
 ps=posets(n);counts.append(len(ps))
 for r in ps:
  code=[sum(1<<i for i in range(n) if (i,a) in r) for a in range(n)]
  ck(len(set(code))==n)
  for a,b in itertools.product(range(n),repeat=2):ck(((code[a]&code[b])==code[a])==((a,b) in r))
  for a,b in itertools.product(range(n),repeat=2):ck((((15^code[a])&(15^code[b]))==(15^code[a]))==((b,a) in r))
ps=posets(4);lookup=set(ps); comparable=0
for r,s in itertools.product(ps,repeat=2):
 f=[sum(1<<i for i in range(4) if (i,a) in r) for a in range(4)]
 g=[sum(1<<i for i in range(4) if (i,a) in s) for a in range(4)]
 ck(r&s in lookup)
 if s<=r:
  comparable+=1
  for b,j in itertools.product(range(4),repeat=2):
   val=any((f[a]>>j)&1 and g[a]&g[b]==g[a] for a in range(4));ck(val==bool((f[b]>>j)&1))
 else:
  a,b=next(iter(s-r));ck(g[a]&g[b]==g[a]);ck(bool(f[a]&(1<<a)) and not bool(f[b]&(1<<a)))
 for a,b in itertools.product(range(4),repeat=2):ck(((f[a]|(g[a]<<4))&(f[b]|(g[b]<<4))==(f[a]|(g[a]<<4)))==((a,b) in r&s))
ck(counts==[1,3,19,219])
print(json.dumps({'assertions':checks,'labelled_poset_counts':counts,'four_symbol_pairs':len(ps)**2,'compatible_order_pairs':comparable,'scope':'finite code algebra; no claim of complete fiber size'},indent=2))

import itertools,json
checks=0
def ck(x):
 global checks
 checks+=1;assert x
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def even(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2==0
def order(p):
 q=tuple(range(len(p)));r=q
 for k in range(1,100):
  r=comp(p,r)
  if r==q:return k
 raise AssertionError
for n in range(5,8):
 cycles=[]
 for a,b,c in itertools.combinations(range(n),3):
  q=list(range(n));q[a]=b;q[b]=c;q[c]=a;cycles.append(tuple(q))
 for p in itertools.permutations(range(n)):
  if even(p) and p!=tuple(range(n)):ck(any(comp(p,q)!=comp(q,p) for q in cycles))
for p in [3,5,7,11,13,17,19,23,29,31,37,41,43,47]:
 q=tuple(list(range(1,p))+[0]);ck(even(q));ck(order(q)==p)
graph_cases=0
for n in range(1,6):
 edges=list(itertools.combinations(range(n),2));perms=[p for p in itertools.permutations(range(n)) if order(p) in (2,3,5)]
 for mask in range(1<<len(edges)):
  E={e for i,e in enumerate(edges) if mask>>i&1};adj=[{j for j in range(n) if tuple(sorted((i,j))) in E} for i in range(n)];d=max(map(len,adj),default=0)
  for p in perms:
   if order(p)<=d or not any(p[i]==i for i in range(n)):continue
   if {tuple(sorted((p[i],p[j]))) for i,j in E}!=E:continue
   for v in range(n):
    if p[v]!=v:continue
    seen={v};todo=[v]
    while todo:
     for w in adj[todo.pop()]:
      if w not in seen:seen.add(w);todo.append(w)
    ck(all(p[w]==w for w in seen));graph_cases+=1
print(json.dumps({'assertions':checks,'alternating_sizes':[5,6,7],'graph_vertex_cases':graph_cases,'graph_sizes':list(range(1,6)),'scope':'finite controls of credited prior argument'},indent=2))

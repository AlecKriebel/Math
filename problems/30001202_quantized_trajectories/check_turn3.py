import itertools,json
checks=0;cases=0
def check(c):
 global checks
 assert c;checks+=1
# Finite closed-relation models: verify viable infinite pair orbits by exact graph pruning.
for n in range(1,5):
 pairs=list(itertools.product(range(n),repeat=2));diag={(i,i) for i in range(n)};off=[p for p in pairs if p not in diag]
 # all diagonal-plus-symmetric relations, not necessarily equivalence relations.
 unordered=list(itertools.combinations(range(n),2))
 for f in itertools.product(range(n),repeat=n):
  for mask in range(1<<len(unordered)):
   R=set(diag)
   for k,(a,b) in enumerate(unordered):
    if mask>>k&1:R|={(a,b),(b,a)}
   succ=lambda p:(f[p[0]],f[p[1]])
   future=set(R)
   for k in range(n*n+1):future={p for p in future if succ(p) in future}
   # Independent explicit forward orbit detects survival until first repeat.
   brute=set()
   for p in R:
    seen=set();x=p
    while x in R and x not in seen:seen.add(x);x=succ(x)
    if x in seen:brute.add(p)
   check(future==brute)
   both=set(future)
   for k in range(n*n+1):both={p for p in both if any(succ(q)==p for q in both)}
   # In a finite deterministic graph, bi-infinite states are exactly cycle vertices.
   cycles=set()
   for p in R:
    seen=[];x=p
    while x in R and x not in seen:seen.append(x);x=succ(x)
    if x in seen:cycles.update(seen[seen.index(x):])
   check(both==cycles);cases+=1
print(json.dumps({'assertions':checks,'finite_relation_models':cases,'scope':'exact pair-graph forward and bilateral viability controls; compact infinite-space proof is separate'},indent=2))

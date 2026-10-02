import itertools,json
A=[p for p in itertools.permutations(range(5)) if sum(p[i]>p[j] for i in range(5) for j in range(i+1,5))%2==0];I=tuple(range(5));N=0
def ck(x):
 global N
 assert x;N+=1
def mul(p,q):return tuple(p[q[i]] for i in range(5))
def inv(p):return tuple(p.index(i) for i in range(5))
ck(len(A)==60)
for s in A:
 if s==I:continue
 comm=[mul(mul(mul(s,a),inv(s)),inv(a)) for a in A]
 ck(any(c!=I for c in comm));c=next(c for c in comm if c!=I)
 gens={mul(mul(a,c),inv(a)) for a in A};seen={I};todo=[I]
 while todo:
  x=todo.pop()
  for g in gens:
   y=mul(x,g)
   if y not in seen:seen.add(y);todo.append(y)
 ck(len(seen)==60)
print(json.dumps({'status':'PASS','independent_assertions':N,'nonidentity_A5_elements':59,'scope':'finite commutator/normal-closure controls; infinite topological proof separately reviewed'},indent=2))

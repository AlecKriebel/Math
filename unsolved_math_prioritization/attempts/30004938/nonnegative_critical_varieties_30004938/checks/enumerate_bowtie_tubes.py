from pathlib import Path
BASE = Path(__file__).resolve().parent
import itertools,json,collections
n=5; crossings=[(1,2),(1,3),(2,3),(2,4),(2,5),(4,5)]
lo,hi=-30,40
succ={i:set() for i in range(lo,hi+1)}
for p,q in crossings:
 for t in range(-10,11):
  for x,y in [(p+t*n,q+t*n),(q+t*n,p+(t+1)*n)]:
   if x in succ and y in succ:succ[x].add(y)
for x in range(hi,lo-1,-1):
 for y in list(succ[x]):succ[x].update(succ[y])
def related(x,y):return y in succ[x]
def tube(S):
 S=set(S)
 if len({x%n for x in S})<len(S):return False
 for a,b in itertools.combinations(sorted(S),2):
  if related(a,b):
   for c in range(a+1,b):
    if related(a,c) and related(c,b) and c not in S:return False
 seen={min(S)}
 while True:
  nxt=seen|{x for x in S if any(related(x,y) or related(y,x) for y in seen)}
  if nxt==seen:break
  seen=nxt
 return seen==S
out=[]
for m in range(1,6):
 for size in range(2,6):
  for rest in itertools.combinations(range(m+1,m+17),size-1):
   S=(m,)+rest
   if tube(S):out.append(S)
counts=collections.Counter(map(len,out));print('counts',dict(counts),'total',len(out))
for s in out:print(s)
open(BASE / 'bowtie_tubes.json','w').write(json.dumps({'counts':dict(counts),'tubes':out},indent=2))

import itertools,json,math
from fractions import Fraction as F
N=0
def ck(v):
 global N
 assert v;N+=1
def comp(p,X):
 X=set(X);out={}
 for x in X:
  y=p[x]
  while y not in X:y=p[y]
  out[x]=y
 return out
for m in range(2,6):
 P=list(itertools.permutations(range(m)))
 for p in P:
  for n in range(1,m):
   subsets=list(itertools.combinations(range(m),n))
   for X in subsets:
    cx=comp(p,X)
    for Z in subsets:
     I=set(X)&set(Z);th={x:x for x in I};th.update(zip(sorted(set(X)-I),sorted(set(Z)-I)));inv={v:k for k,v in th.items()};cz=comp(p,Z)
     ck(sum(cx[x]!=inv[cz[th[x]]] for x in X)<=3*(n-len(I)))
# Diagonal orbit occupancy and exact indicator energy for free two-generator actions.
for m in range(2,6):
 n=m-1;cyc=tuple((i+1)%m for i in range(m));Q=list(itertools.permutations(range(m)))
 small=list(itertools.permutations(range(n)))
 for q in Q[:min(8,len(Q))]:
  for a,b in itertools.product(small[:min(6,len(small))],repeat=2):
   gens=[(cyc,a),(q,b)];pairs=set(itertools.product(range(m),range(n)));orbits=[]
   while pairs:
    root=min(pairs);O={root};todo=[root];pairs.remove(root)
    while todo:
     y,x=todo.pop()
     for g,h in gens:
      z=(g[y],h[x])
      if z not in O:O.add(z);todo.append(z);pairs.discard(z)
    orbits.append(O)
   A={(x,x) for x in range(n)};dist=sum(F(len(O&A))-F(len(O&A)**2,len(O)) for O in orbits)
   ck(dist>=F(n,2))
   for g,h in gens:
    sA={(g[y],h[x]) for y,x in A};err=sum(g[x]!=h[x] for x in range(n));ck(len(sA^A)==2*err)
x=F(5,4);s=sum(x**j/F(math.factorial(j)) for j in range(21));tail=x**21/F(math.factorial(21))/(1-x/22)
ck(s+tail<F(7,2));ck(2**17>7**6)
print(json.dumps({'status':'PASS','independent_exact_assertions':N,'scope':'subset transport, diagonal orbit/energy identities, rational spectral constants'},indent=2))

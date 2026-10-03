#!/usr/bin/env python3
import itertools,json
checks=0
def ck(x):
 global checks
 assert x;checks+=1

def analyze(name,elts,op):
 ix={x:i for i,x in enumerate(elts)};M=[[ix[op(a,b)] for b in elts] for a in elts];e=0;G=frozenset(range(len(elts)))
 def closure(gs):
  S={e};todo=[e]
  while todo:
   a=todo.pop()
   for b in gs:
    c=M[a][b]
    if c not in S:S.add(c);todo.append(c)
  return frozenset(S)
 subs={frozenset({e})};todo=list(subs)
 while todo:
  S=todo.pop()
  for g in G-S:
   T=closure(tuple(S)+(g,))
   if T not in subs:subs.add(T);todo.append(T)
 cache={}
 def autos(S):
  if S in cache:return cache[S]
  gs=[];T=closure(gs)
  for g in sorted(S):
   if g not in T:gs.append(g);T=closure(gs)
  ans=[]
  for ys in itertools.product(S,repeat=len(gs)):
   phi={e:e};todo=[e];ok=True
   while todo and ok:
    a=todo.pop()
    for x,y in zip(gs,ys):
     b=M[a][x];z=M[phi[a]][y]
     if b in phi:
      if phi[b]!=z:ok=False;break
     else:phi[b]=z;todo.append(b)
   if ok and set(phi.values())==set(S):
    ck(all(phi[M[a][b]]==M[phi[a]][phi[b]] for a in S for b in S));ans.append(phi)
  cache[S]=ans;return ans
 def char(S,T):return all({a[x] for x in T}==set(T) for a in autos(S))
 def core(S,T):
  R=set(T)
  for a in autos(S):R &= {a[x] for x in T}
  return frozenset(R)
 for U in subs:
  if U==G:continue
  V=U
  while True:
   W=core(U,core(G,V));ck(W<=V)
   if W==V:break
   V=W
  candidates=[K for K in subs if K<=U and char(G,K) and char(U,K)]
  ck(all(K<=V for K in candidates));ck(V in candidates)
 return {'group':name,'order':len(G),'subgroups':len(subs),'automorphisms':len(autos(G))}
out=[]
out.append(analyze('C4',list(range(4)),lambda a,b:(a+b)%4))
out.append(analyze('C2xC2',list(itertools.product(range(2),repeat=2)),lambda a,b:tuple((x+y)%2 for x,y in zip(a,b))))
out.append(analyze('D8',list(itertools.product(range(4),range(2))),lambda x,y:((x[0]+(-1)**x[1]*y[0])%4,(x[1]+y[1])%2)))
out.append(analyze('Heisenberg_3',list(itertools.product(range(3),repeat=3)),lambda x,y:((x[0]+y[0])%3,(x[1]+y[1])%3,(x[2]+y[2]+x[0]*y[1])%3)))
for p,d in [(2,2),(2,3),(3,2),(3,3),(5,2)]:
 D=1+p*(d-1)
 # Explicit rank is d-1 because each nonzero row has its own disjoint p-column block.
 rows=[]
 for i in range(d-1):rows.append([0]+[int(i==j) for j in range(d-1) for _ in range(p)])
 ck(len(rows)==d-1 and all(len(r)==D for r in rows))
 ck(all(sum(r)==p for r in rows));ck(D-(d-1)==1+(p-1)*(d-1));ck(0<D-(d-1)<D)
print(json.dumps({'turn':2,'assertions':checks,'finite_groups':out,'scope':'exact finite core-iteration controls, not a convergence proof in free pro-p groups'},sort_keys=True,indent=2))

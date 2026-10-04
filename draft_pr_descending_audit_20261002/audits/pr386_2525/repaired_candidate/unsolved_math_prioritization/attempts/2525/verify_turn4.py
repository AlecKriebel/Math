from finite_groups import *
from itertools import permutations
import json
checks=0;cats={};rows=[]
def ck(x,k):
 global checks
 assert x,k;checks+=1;cats[k]=cats.get(k,0)+1
def permgroup(n,even):
 ps=[p for p in permutations(range(n)) if not even or sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2==0];ix={p:i for i,p in enumerate(ps)}
 return ps,[[ix[tuple(p[q[i]] for i in range(n))] for q in ps] for p in ps]
for n,even in [(3,False),(4,False),(4,True),(5,True)]:
 ps,M=permgroup(n,even);N=len(M);iv=inverses(M)
 classes={frozenset(M[M[h][g]][iv[h]] for h in range(N)) for g in range(1,N)};classes=sorted(classes,key=min);pairs=0;ngen=0
 for mask in range(1,1<<len(classes)):
  S=set().union(*(classes[i] for i in range(len(classes)) if mask>>i&1));l=lengths(M,S)
  if len(l)!=N:continue
  ngen+=1
  for g in range(N):
   for h in range(N):ck(l[M[M[h][g]][iv[h]]]==l[g],'invariant_length')
  for fm in range(1,1<<len(classes)):
   F=[min(classes[i]) for i in range(len(classes)) if fm>>i&1]
   U={M[M[h][f]][iv[h]] for h in range(N) for f0 in F for f in [f0,iv[f0]]};ul=lengths(M,U)
   if len(ul)!=N:continue
   b=max(ul.values());C=max(l[f] for f0 in F for f in [f0,iv[f0]])
   ck(max(l.values())<=b*C,'finite_normal_generation_bound');pairs+=1
 rows.append({'group':('A' if even else 'S')+str(n),'order':N,'normal_positive_generating_sets':ngen,'normal_generator_pairs':pairs})
_,M=dihedral(4);N=len(M);iv=inverses(M);F=[1,4];U={M[M[h][f]][iv[h]] for h in range(N) for f0 in F for f in [f0,iv[f0]]};b=max(lengths(M,U).values())
for S in subsets(N):
 l=lengths(M,S)
 if len(l)!=N:continue
 K=max(l[M[M[h][s]][iv[h]]] for h in range(N) for s in S);C=max(l[f] for f0 in F for f in [f0,iv[f0]])
 ck(max(l.values())<=b*K*C,'conjugacy_cost_bound')
for n in range(10,41):
 _,M=dihedral(n);S=[1,2,3,n-1,n];d=lengths(M,S)
 ck(d[n-3]==3,'local_finite_dihedral_three_letters')
print(json.dumps({'assertions':checks,'categories':cats,'groups':rows,'scope':'Finite normal-generation and conjugacy controls; all-group hypotheses remain explicit.'},sort_keys=True,indent=2))

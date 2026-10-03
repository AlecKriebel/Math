from finite_groups import *
import json
checks=0;cats={};rows=[]
def ck(x,k):
 global checks
 assert x,k;checks+=1;cats[k]=cats.get(k,0)+1
for name,M in [cyclic(n) for n in range(2,9)]+[dihedral(3),dihedral(4)]:
 N=len(M);iv=inverses(M);subs={frozenset([0]),frozenset(range(N))}
 for A in subsets(N):subs.add(frozenset(lengths(M,A)))
 normal={H for H in subs if all(M[M[g][h]][iv[g]] in H for g in range(N) for h in H)}
 count=0
 for S in subsets(N):
  l=lengths(M,S)
  if len(l)!=N:continue
  for H in subs:
   cosets={frozenset(M[h][g] for h in H) for g in range(N)}
   C={g:next(c for c in cosets if g in c) for g in range(N)}
   reps={c:min(c,key=lambda g:(l[g],g)) for c in cosets};q=max(l[r] for r in reps.values());c=max(l[iv[r]] for r in reps.values())
   ck(q<=len(cosets)-1,'shortest_coset_bound')
   T={M[M[r][s]][iv[reps[C[M[r][s]]]]] for r in reps.values() for s in S}
   ck(T<=H,'schreier_membership');ck(all(l[t]<=q+1+c for t in T),'schreier_cost')
   tlen=lengths(M,T);ck(set(tlen)==set(H),'positive_schreier_generation');k=max(tlen.values())
   ck(max(l.values())<=k*(q+1+c)+q,'overgroup_diameter')
   if H in normal:
    CN=max(l[h] for h in H)
    for g in range(N):
     lq=min(l[x] for x in C[g]);ck(lq<=l[g]<=lq+CN,'quotient_metric_comparison')
   count+=1
 rows.append({'group':name,'subgroups':len(subs),'normal_subgroups':len(normal),'generating_set_subgroup_pairs':count})
print(json.dumps({'assertions':checks,'categories':cats,'groups':rows,'scope':'Finite directed Schreier and quotient controls; infinite extension results proved in TURN_2.md.'},sort_keys=True,indent=2))

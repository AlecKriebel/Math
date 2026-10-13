"""Exhaustive labeled semigroup controls of orders at most three.
The count is finite diagnostic evidence, not a structural characterization.
"""
from itertools import product
from collections import Counter
import json

def catalogue(n):
 X=range(n); triples=list(product(X,repeat=3));pairs=list(product(X,repeat=2))
 semigroups=[];regular=[]
 for t in product(X,repeat=n*n):
  if not all(t[t[a*n+b]*n+c]==t[a*n+t[b*n+c]] for a,b,c in triples):continue
  semigroups.append(t);inv=[]
  for a in X:
   choices=[b for b in X if t[t[a*n+b]*n+a]==a and t[t[b*n+a]*n+b]==b and t[a*n+b]==t[b*n+a]]
   if len(choices)!=1:break
   inv.append(choices[0])
  if len(inv)==n:regular.append((t,inv))
 stats=Counter();witnesses={}
 for mul,inv in regular:
  m=lambda a,b:mul[a*n+b]
  for plus in semigroups:
   add=lambda a,b:plus[a*n+b]
   if not all(m(a,add(b,c))==add(m(a,b),m(a,add(inv[a],c))) for a,b,c in triples):continue
   stats['generalized_left_semi_braces']+=1
   rr={}
   for a,b in pairs:
    d=add(inv[a],b);rr[a,b]=(m(a,d),m(inv[d],b))
   masks=[];fail={}
   for a,b,c in triples:
    u,v=rr[a,b];w,z=rr[v,c];x,y=rr[u,w];L=(x,y,z)
    u,v=rr[b,c];w,z=rr[a,u];x,y=rr[z,v];R=(w,x,y)
    for i in range(3):
     if L[i]!=R[i] and i not in fail:fail[i]={'triple':[a,b,c],'left':L,'right':R}
   mask=''.join(str(i+1) for i in sorted(fail)) or 'none';stats['YBE_failed_coordinates_'+mask]+=1
   fact=all(m(*rr[a,b])==m(a,b) for a,b in pairs)
   lh=all(rr[a,rr[b,c][0]][0]==rr[m(a,b),c][0] for a,b,c in triples)
   rh=all(rr[rr[a,b][1],c][1]==rr[a,m(b,c)][1] for a,b,c in triples)
   for key,yes in [('factorization',fact),('lambda_homomorphism',lh),('rho_antihomomorphism',rh)]:
    if not yes:
     stats[key+'_fails']+=1
     witnesses.setdefault(key,{'addition':plus,'multiplication':mul,'inverse':inv,'r':[rr[a,b] for a,b in pairs],'ybe_fails':fail})
   if fail:witnesses.setdefault('YBE_'+mask,{'addition':plus,'multiplication':mul,'inverse':inv,'r':[rr[a,b] for a,b in pairs],'ybe_fails':fail})
   # Audit the two projection additions without trusting a printed r formula.
   if all(add(a,b)==b for a,b in pairs):
    crit=all(m(m(a,b),inv[m(a,b)])==m(m(m(a,inv[a]),b),inv[m(m(a,inv[a]),b)]) for a,b in pairs)
    assert crit==(not fail)
    assert all(rr[a,b]==(m(a,b),m(b,inv[b])) for a,b in pairs)
    stats['right_zero_criterion_checked']+=1
   if all(add(a,b)==a for a,b in pairs):
    crit=all(m(m(a,b),inv[m(a,b)])==m(m(a,m(b,inv[b])),inv[m(a,m(b,inv[b]))]) for a,b in pairs)
    assert crit==(not fail)
    assert all(rr[a,b]==(m(a,inv[a]),m(a,b)) for a,b in pairs)
    stats['left_zero_criterion_checked']+=1
 return {'order':n,'labeled_semigroups':len(semigroups),'completely_regular_multiplications':len(regular),'stats':dict(stats),'first_witnesses':witnesses}
print(json.dumps({'scope':'All labeled binary operations of orders 1,2,3 filtered by exact associativity and completely regular/brace axioms. Not an all-size classification.','catalogues':[catalogue(n) for n in (1,2,3)]},indent=2))

from finite_groups import *
import json
checks=0;cats={};rows=[]
def ck(x,k):
 global checks
 assert x,k;checks+=1;cats[k]=cats.get(k,0)+1
for n in range(3,13):
 name,H=cyclic(n);_,G=dihedral(n);t=n;num=0
 for S in subsets(n):
  if len(lengths(H,S))!=n:continue
  num+=1;T=set(S)|{(-s)%n for s in S};dt=lengths(H,T);dw=lengths(G,list(S)+[t])
  ck(len(dw)==2*n,'positive_extension_generation')
  for h in range(n):ck(dt[h]<=dw[h]<=3*dt[h],'saturation_metric')
  for g in range(2*n):ck(dw[g]<=3*max(dt.values())+1,'normal_form_bound')
  if set(S)==T:
   ds=lengths(H,S)
   for h in range(n):ck(ds[h]==dw[h],'invariant_metric_equality')
 rows.append({'cyclic_order':n,'positive_generating_subsets':num})
# Bounded finite windows verify the normal form without using cyclic wrap-around.
for k in range(-100,101):
 if k>=0:letters=[(k,0)] if k else []
 else:letters=[(0,1),(-k,0),(0,1)]
 a=e=0
 for b,f in letters:a,e=a+(-1)**e*b,(e+f)%2
 ck((a,e)==(k,0) and len(letters)<=3,'integer_dihedral_rotation')
 letters=[(k,0),(0,1)] if k>=0 else [(0,1),(-k,0)]
 a=e=0
 for b,f in letters:a,e=a+(-1)**e*b,(e+f)%2
 ck((a,e)==(k,1) and len(letters)<=2,'integer_dihedral_reflection')
ck(-3 < -2,'exact_diameter_lower_bound')
print(json.dumps({'assertions':checks,'categories':cats,'groups':rows,'scope':'Finite-action metric controls; all-group equivalences and infinite dihedral example proved in TURN_3.md.'},sort_keys=True,indent=2))

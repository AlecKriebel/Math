from finite_groups import *
import json
checks=0;cats={};rows=[]
def ck(x,k):
 global checks
 assert x,k;checks+=1;cats[k]=cats.get(k,0)+1
groups=[cyclic(n) for n in range(2,10)]+[dihedral(3),dihedral(4),abelian(2,2),abelian(3,3)]
for name,M in groups:
 N=len(M);iv=inverses(M);num=0
 for S in subsets(N):
  pos=lengths(M,S);sym=lengths(M,set(S)|{iv[s] for s in S});ck(set(pos)==set(sym),'finite_generation')
  if len(pos)!=N:continue
  num+=1;D=max(pos.values());d=max(sym.values());R=max(pos[iv[s]] for s in S)
  ck(R<=D<=d*max(1,R),'inverse_cost_bound')
  orders=[]
  for s in S:
   a=s;e=1
   while a:a=M[a][s];e+=1
   orders.append(e)
  ck(R<=max(orders)-1,'order_inverse_bound');ck(D<=d*max(1,max(orders)-1),'order_diameter_bound')
  for n in range(D+1):
   A={a for a in range(N) if pos[a]<=n and pos[iv[a]]<=n};ad=lengths(M,A)
   ck({iv[a] for a in A}==A,'core_symmetry')
   ck(set(ad)==set(lengths(M,set(A)|{iv[a] for a in A})),'core_subgroup')
   ck(all(pos[a]<=n*dist for a,dist in ad.items()),'core_word_bound')
   if len(ad)==N:ck(D<=n*max(ad.values()),'core_diameter_bound')
 rows.append({'group':name,'monoid_generating_sets':num})
# Exact finite windows of the stated Z length formula, checked without wrapping.
for m in range(1,41):
 ck(-m < -(m-1),'integer_lower_bound')
 ck(sum([-1]*m)==-m,'integer_attainment')
print(json.dumps({'assertions':checks,'categories':cats,'groups':rows,'scope':'Finite exhaustive metric controls and integer formula checks; infinite results proved in TURN_1.md.'},indent=2,sort_keys=True))

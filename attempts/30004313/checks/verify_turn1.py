"""Exact controls for the retracted-right-zero addition subclass."""
from itertools import product
from collections import Counter
import json
C=Counter();models=[]
def ck(x,k):assert x,k;C[k]+=1
for name,n,top,meet in [('chain2',2,1,min),('chain3',3,2,min),('chain4',4,3,min),('boolean_square',4,3,lambda x,y:x&y),('two_atoms_no_top',3,None,lambda x,y:x if x==y else 0)]:
 X=range(n);triples=list(product(X,repeat=3));brace_count=sol_count=0
 for f in product(X,repeat=n):
  plus=lambda a,b:f[b]
  additive=all(plus(plus(a,b),c)==plus(a,plus(b,c)) for a,b,c in triples)
  ck(additive==all(f[f[x]]==f[x] for x in X),'additive_associativity_iff_idempotent_map')
  if not additive:continue
  brace=all(meet(a,plus(b,c))==plus(meet(a,b),meet(a,plus(a,c))) for a,b,c in triples)
  ideal=all(f[meet(a,f[c])]==meet(a,f[c]) for a,c in product(X,repeat=2))
  ck(brace==ideal,'brace_law_iff_downward_fixed_image')
  if not brace:continue
  brace_count+=1
  r=lambda a,b:(meet(a,f[b]),meet(f[b],b))
  def sides(a,b,c):
   u,v=r(a,b);w,z=r(v,c);x,y=r(u,w);L=(x,y,z)
   u,v=r(b,c);w,z=r(a,u);x,y=r(z,v);R=(w,x,y)
   return L,R
  valid=True
  for a,b,c in triples:
   L,R=sides(a,b,c)
   derivedL=(meet(meet(meet(a,b),f[b]),f[c]),meet(meet(b,f[b]),f[c]),meet(c,f[c]))
   derivedR=(meet(meet(a,b),f[c]),meet(meet(b,c),f[c]),meet(c,f[c]))
   ck(L==derivedL and R==derivedR,'explicit_braid_side_formulas')
   valid=valid and L==R
  monotone=all(meet(f[x],f[y])==f[x] for x,y in product(X,repeat=2) if meet(x,y)==x)
  deflationary=all(meet(x,f[x])==f[x] for x in X)
  ck(valid==(monotone and deflationary),'semilattice_full_subclass_criterion')
  if top is not None:
   principal=all(f[x]==meet(x,f[top]) for x in X)
   ck(valid==principal,'bounded_semilattice_full_subclass_criterion')
  if valid:sol_count+=1
 models.append({'model':name,'generalized_brace_maps':brace_count,'YBE_maps':sol_count})
# Exact smallest middle-coordinate-only failure with no top: zero and two atoms.
meet=lambda a,b:a if a==b else 0
f=[0,1,1];r=lambda a,b:(meet(a,f[b]),meet(f[b],b))
for a,b,c in product(range(3),repeat=3):
 ck(meet(a,f[c])==f[meet(a,f[c])],'fork_example_brace_identity')
 u,v=r(a,b);w,z=r(v,c);x,y=r(u,w);L=(x,y,z)
 u,v=r(b,c);w,z=r(a,u);x,y=r(z,v);R=(w,x,y)
 ck(L[0]==R[0] and L[2]==R[2],'fork_outer_YBE_coordinates_hold')
 if (a,b,c)==(0,1,2):ck(L==(0,1,0) and R==(0,0,0),'fork_exact_middle_failure')
# The two-element zero-addition example is a genuine solution whose factors
# do not multiply to the original product.
rr=lambda a,b:(0,0)
ck(rr(1,1)[0]*rr(1,1)[1]!=1,'factorization_not_necessary_for_YBE')
print(json.dumps({'status':'PASS','models':models,'exact_assertions':sum(C.values()),'counts':dict(C),'scope':'Finite controls for written all-size subclass proofs and explicit obstructions; not a full generalized-semi-brace classification.'},indent=2,sort_keys=True))

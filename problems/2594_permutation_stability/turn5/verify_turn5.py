#!/usr/bin/env python3
from itertools import permutations,combinations
from collections import Counter
from fractions import Fraction as F
import json
C=Counter()
def ck(v,k):
 C[k]+=1
 if not v:raise AssertionError(k)
def comp_labels(p,X):
 X=tuple(X);S=set(X);out={}
 for x in X:
  y=p[x]
  while y not in S:y=p[y]
  out[x]=y
 return out
def mismatch_dict(p,q):return sum(p[x]!=q[x] for x in p)
def power(p,k):
 ans=tuple(range(len(p)))
 for _ in range(k):ans=tuple(p[x] for x in ans)
 return ans
# Every permutation, equal-size subset pair, and intersection-fixing transport.
for M in range(1,6):
 for p in permutations(range(M)):
  for n in range(1,M+1):
   subsets=list(combinations(range(M),n));cs={X:comp_labels(p,X) for X in subsets}
   for X in subsets:
    for Z in subsets:
     I=set(X)&set(Z);left=sorted(set(X)-I);right=sorted(set(Z)-I);d=len(left)
     for image in permutations(right):
      th={x:x for x in I};th.update(zip(left,image));back={v:k for k,v in th.items()}
      transported={x:back[cs[Z][th[x]]] for x in X}
      ck(mismatch_dict(cs[X],transported)<=3*d,'three_exchange_bound_complete')
# Exact sharpness witness for the comparison, not for minimized repair costs.
p=(3,4,0,1,2);X=(0,1,2,3);Z=(0,1,2,4);th={0:0,1:1,2:2,3:4};back={v:k for k,v in th.items()}
a=comp_labels(p,X);b=comp_labels(p,Z);bt={x:back[b[th[x]]] for x in X}
ck(mismatch_dict(a,bt)==3,'sharp_three_exchange')
# Every injection and pair of generator permutations in dimensions up to four.
injection_models=0
for M in range(1,5):
 for n in range(1,M+1):
  X=tuple(range(n));k=M-n
  for rho in permutations(range(M)):
   c=comp_labels(rho,X)
   for tau in permutations(range(n)):
    # Inclusion bound for arbitrary candidate action.
    r=sum(c[x]!=tau[x] for x in X);e_inc=sum(rho[x]!=tau[x] for x in X)
    ck(e_inc<=r+k,'inclusion_matching_bound')
    # Constant fractional matrix always feasible and equivariant.
    B=[[F(1,M) for x in X] for y in range(M)]
    ck(all(sum(B[y][x] for y in range(M))==1 for x in X),'fractional_columns')
    ck(all(sum(row)<=1 for row in B),'fractional_rows')
    # Left action permutes rows; right action permutes columns.
    ir=[0]*M
    for x,y in enumerate(rho):ir[y]=x
    ck(all(B[ir[y]][x]==B[y][tau[x]] for y in range(M) for x in X),'fractional_zero_intertwining')
    for inj in permutations(range(M),n):
     injection_models+=1;Z=set(inj);jb={y:x for x,y in enumerate(inj)}
     E=sum(rho[inj[x]]!=inj[tau[x]] for x in X)
     # Build the actual two M by n zero-one matrices and Frobenius residual.
     sq=sum((int(y==rho[inj[x]])-int(y==inj[tau[x]]))**2 for y in range(M) for x in X)
     ck(sq==2*E,'injection_frobenius_identity')
     I=set(X)&Z;th={x:x for x in I};th.update(zip(sorted(set(X)-I),sorted(Z-I)));back={y:x for x,y in th.items()}
     transported={x:back[inj[tau[jb[th[x]]]]] for x in X}
     ck(sorted(transported.values())==list(X),'matching_transport_permutation')
     d=len(set(X)-Z)
     ck(mismatch_dict(c,transported)<=E+2*d,'matching_transport_bound')
# Exact cyclic-presentation search in the finite varying-domain example.
prime_results=[]
for p in [3,5,7]:
 n=p-1;rho=tuple(list(range(1,p))+[0]);X=tuple(range(n));valid=[]
 for beta in permutations(X):
  if power(beta,p)==X:valid.append(beta)
 ck(valid==[X],'prime_cyclic_only_trivial_smaller_action')
 c=comp_labels(rho,X)
 ck(sum(c[x]!=x for x in X)==n,'prime_cyclic_compression_error_one')
 vals=[]
 for inj in permutations(range(p),n):
  E=sum(rho[inj[x]]!=inj[x] for x in X);ck(E==n,'prime_cyclic_matching_error_one');vals.append(E)
 prime_results.append({'varying_group_order':p,'target_size':n,'exact_matching_optimum':str(F(min(vals),n)),'fractional_optimum':'0'})
print(json.dumps({'scope':'Exact finite controls; prime-cyclic groups vary and are not a source counterexample','checks_by_kind':dict(sorted(C.items())),'total_assertions':sum(C.values()),'injection_models':injection_models,'varying_group_diagnostics':prime_results},indent=2,sort_keys=True))

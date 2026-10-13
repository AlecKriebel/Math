"""Exact diagnostics for non-Clifford projection and Rees-matrix branches."""
from itertools import product,permutations
from collections import Counter
import json
C=Counter();summary=[]
def ck(x,k):assert x,k;C[k]+=1
def braid_sides(r,a,b,c):
 u,v=r(a,b);w,z=r(v,c);x,y=r(u,w);L=(x,y,z)
 u,v=r(b,c);w,z=r(a,u);x,y=r(z,v);R=(w,x,y)
 return L,R
for n in (1,2,3):
 X=range(n);triples=list(product(X,repeat=3));bands=rect=0
 for t in product(X,repeat=n*n):
  plus=lambda a,b:t[a*n+b]
  if not all(plus(plus(a,b),c)==plus(a,plus(b,c)) for a,b,c in triples):continue
  band=all(plus(a,a)==a for a in X)
  left_brace=all(a==plus(a,a) for a,b,c in triples)
  ck(left_brace==band,'left_zero_multiplication_compatibility')
  if band:
   bands+=1;r=lambda a,b:(a,plus(a,b))
   for a,b,c in triples:
    L,R=braid_sides(r,a,b,c)
    ck(L==R==(a,plus(a,b),plus(plus(a,b),c)),'left_zero_multiplication_all_braid_coordinates')
  rectangular=all(plus(b,c)==plus(b,plus(a,c)) for a,b,c in triples)
  if rectangular:
   rect+=1;r=lambda a,b:(plus(a,b),b)
   for a,b,c in triples:
    L,R=braid_sides(r,a,b,c)
    ck(L==R==(plus(a,c),plus(b,c),c),'right_zero_multiplication_all_braid_coordinates')
 summary.append({'order':n,'additive_bands':bands,'right_zero_multiplication_compatible_additions':rect})
# The explicit size-four counterexample, including all axioms.
X=range(4);mul=lambda a,b:2*(a//2)+b%2;plus=lambda a,b:2 if a and b else 0
r=lambda a,b:(mul(a,plus(a,b)),mul(plus(a,b),b))
for a,b,c in product(X,repeat=3):
 ck(plus(plus(a,b),c)==plus(a,plus(b,c)),'four_element_additive_associativity')
 ck(mul(mul(a,b),c)==mul(a,mul(b,c)),'four_element_multiplicative_associativity')
 ck(mul(a,plus(b,c))==plus(mul(a,b),mul(a,plus(a,c))),'four_element_full_brace_identity')
for a in X:ck(mul(a,a)==a,'four_element_group_inverse')
ck(braid_sides(r,0,1,1)==((0,0,3),(0,0,1)),'four_element_exact_YBE_failure')
# Concrete group operations, with a noncommutative group included.
groups=[]
groups.append(('C2',range(2),lambda a,b:(a+b)%2,lambda a:a,0))
P=list(permutations(range(3)));ids={p:i for i,p in enumerate(P)}
gmul=lambda a,b:ids[tuple(P[a][P[b][i]] for i in range(3))]
ginv=lambda a:ids[tuple(P[a].index(i) for i in range(3))]
groups.append(('S3',range(6),gmul,ginv,ids[(0,1,2)]))
rees=[]
for name,G,gm,gi,one in groups:
 matrices=list(product(G,repeat=4)) if name=='C2' else []
 if name=='S3':
  for u,v in [([0,1],[2,3]),([3,4],[1,5]),([4,2],[5,1])]:matrices.append(tuple(gm(u[l],v[i]) for l,i in product(range(2),repeat=2)))
  matrices += [(0,0,0,k) for k in (1,2,3)]
 for p in matrices:
  X=list(product(range(2),G,range(2)))
  def m(a,b):return (a[0],gm(gm(a[1],p[2*a[2]+b[0]]),b[1]),b[2])
  def inv(a):
   q=gi(p[2*a[2]+a[0]])
   return(a[0],gm(gm(q,gi(a[1])),q),a[2])
  for a in X:
   aa=inv(a)
   ck(m(m(a,aa),a)==a and m(m(aa,a),aa)==aa and m(a,aa)==m(aa,a),'Rees_commuting_group_inverse_formula')
  compatible=all(m(a,m(b,c))==m(m(a,b),m(a,m(inv(a),c))) for a,b,c in product(X,repeat=3))
  criterion=all(p[2*mu+k]==gm(gm(p[2*mu+i],gi(p[2*lam+i])),p[2*lam+k]) for mu,k,i,lam in product(range(2),repeat=4))
  ck(compatible==criterion,'Rees_compatibility_iff_sandwich_factorization')
  if not compatible:
   rees.append({'group':name,'matrix':p,'brace_compatible':False});continue
  u=[p[0],p[2]];v=[gm(gi(p[0]),p[i]) for i in range(2)]
  N=lambda a:(a[0],gm(gm(v[a[0]],a[1]),u[a[2]]),a[2])
  normmul=lambda a,b:(a[0],gm(a[1],b[1]),b[2])
  def r(a,b):
   d=m(inv(a),b)
   return m(a,d),m(inv(d),b)
  for a,b in product(X,repeat=2):
   ck(N(m(a,b))==normmul(N(a),N(b)),'Rees_actual_normalization_isomorphism')
   A,B=N(a),N(b);g,h=A[1],B[1]
   expected=((A[0],h,B[2]),(A[0],gm(gm(gi(h),g),h),B[2]))
   ck(tuple(N(z) for z in r(a,b))==expected,'Rees_source_r_formula_after_normalization')
  for a,b,c in product(X,repeat=3):
   L,R=braid_sides(r,a,b,c)
   ck(L==R,'Rees_all_three_braid_coordinates')
  rees.append({'group':name,'matrix':p,'brace_compatible':True,'YBE_verified':True})
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(C),'projection_models':summary,'Rees_models':rees,'scope':'Exact finite diagnostics for all-size proofs in TURN_2. The unrestricted source target remains unresolved.'},indent=2,sort_keys=True))

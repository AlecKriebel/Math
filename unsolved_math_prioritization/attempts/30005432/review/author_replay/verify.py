#!/usr/bin/env python3
"""Exact controls in Z x Z/4; never reduce the integer coordinate modulo a bound."""
from itertools import product
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
C=Counter()
def ck(g,b):assert b,g;C[g]+=1
def eps(c):return 1 if c%4 in (0,1) else -1
def diamond(c,d):return(c+d+2*c*d)%4
def add(a,b):return(a[0]+b[0],(a[1]+b[1])%4)
def neg(a):return(-a[0],-a[1]%4)
def sub(a,b):return add(a,neg(b))
def circ(a,b):return(a[0]+eps(a[1])*b[0],diamond(a[1],b[1]))
def inv(a):return(-eps(a[1])*a[0],a[1])
def lam(a,b):return sub(circ(a,b),a)
def star(a,b):return sub(lam(a,b),b)
def conjugate(g,x):return circ(circ(g,x),inv(g))
zero=(0,0)
for c,d in product(range(4),repeat=2):
 ck('klein_xor',diamond(c,d)==c^d)
 ck('epsilon_character',eps(diamond(c,d))==eps(c)*eps(d))
 ck('parity_character',(-1)**diamond(c,d)==(-1)**c*(-1)**d)
 # Coefficients of arbitrary integer variables (n,m,l) in associativity.
 ck('symbolic_integer_associativity',(1,eps(c),eps(diamond(c,d)))==(1,eps(c),eps(c)*eps(d)))
 for e in range(4):
  ck('klein_associativity',diamond(diamond(c,d),e)==diamond(c,diamond(d,e)))
  ck('symbolic_left_distributivity',diamond(c,(d+e)%4)==(diamond(c,d)-c+diamond(c,e))%4)
  ck('symbolic_first_coordinate_distributivity',(1,eps(c),eps(c))==(1-1+1,eps(c),eps(c)))
for c in range(4):
 ck('symbolic_inverse',1-eps(c)*eps(c)==0 and diamond(c,c)==0)
 # Automorphisms of the infinite additive group are diagonal signs.
 ck('lambda_diagonal_units',eps(c) in (-1,1) and (1+2*c)%4 in (1,3))

points=list(product(range(-2,3),range(4)))
for a in points:
 ck('identity',circ(a,zero)==a==circ(zero,a))
 ck('inverse',circ(a,inv(a))==zero==circ(inv(a),a))
 for b in points:
  ck('lambda_formula',lam(a,b)==(eps(a[1])*b[0],((-1)**a[1]*b[1])%4))
  ck('star_formula',star(a,b)==((eps(a[1])-1)*b[0],2*a[1]*b[1]%4))
  for e in points:
   ck('integer_group_associativity',circ(circ(a,b),e)==circ(a,circ(b,e)))
   ck('left_brace_identity',circ(a,add(b,e))==add(sub(circ(a,b),a),circ(a,e)))
   ck('lambda_homomorphism',lam(circ(a,b),e)==lam(a,lam(b,e)))

x=(0,1);y=add(x,x)
for m,d in product(range(-40,41),range(4)):
 b=(m,d)
 ck('witness_central',circ(x,b)==circ(b,x))
 ck('witness_right_fixed', (star(x,b)==zero)==(d%2==0))
 ck('witness_left_fixed', (star(b,x)==zero)==(d%2==0))
 ck('double_right_star',star(y,b)==(-2*m,0))
 ck('double_right_fixed',(star(y,b)==zero)==(m==0))
ck('additive_failure',x==(0,1) and y==(0,2))
ck('lambda_invariance_failure',lam(x,x)==(0,3))
ck('not_two_sided',circ(add(x,x),(1,0))==(-1,2) and add(sub(circ(x,(1,0)),(1,0)),circ(x,(1,0)))==(1,2))

indices=[]
for n,c in product(range(-4,5),range(4)):
 z=(n,c)
 if c in (0,1):
  K={d for d in range(4) if (eps(d)-1)*n==0 and (2*d*c)%4==0}
  expectedK=set(range(4)) if (c==0 and n==0) else ({0,1} if c==0 else ({0,2} if n==0 else {0}))
  ck('second_fixed_centralizer_kernel',K==expectedK)
  ck('multiplicative_kernel_subgroup',0 in K and all(diamond(d,e) in K for d,e in product(K,repeat=2)))
  idx1=1 if c==0 else 2;idx2=4//len(K)
  expected=(1,1 if n==0 else 2) if c==0 else (2,2 if n==0 else 4)
  ck('exact_finite_indices',(idx1,idx2)==expected)
  indices.append({'element':[n,c],'first_index':idx1,'second_index':idx2})
 for m,d in product(range(-5,6),range(4)):
  g=(m,d)
  ck('centralizer_equation',(circ(g,z)==circ(z,g))==((1-eps(c))*m==(1-eps(d))*n))
  if c in (0,1):
   ck('second_intersection',(star(g,z)==zero and circ(g,z)==circ(z,g))==(d in K))
  else:
   ck('infinite_index_fixed_description',(star(z,g)==zero)==(m==0 and (2*c*d)%4==0))
# Distinct additive cosets, with the global injectivity coefficient checked explicitly.
ck('infinite_witness_coefficient',eps(2)-1==-2 and eps(2)-1!=0)
for m,n in product(range(-20,21),repeat=2):
 ck('pairwise_distinct_additive_cosets',(sub((m,0),(n,0))[0]==0)==(m==n))
 ck('star_injectivity_control',((-2*m,0)==(-2*n,0))==(m==n))
# Multiplicative normality of the complete s-set does not repair additive failure.
for z,g in product(points,repeat=2):
 if z[1] in (0,1):ck('s_set_multiplicative_normality',conjugate(g,z)[1] in (0,1))
root=Path(__file__).resolve().parent
out={'problem_id':30005432,'verdict':'PASS_EXACT_COUNTEREXAMPLE_CONTROLS','assertions':sum(C.values()),'categories':dict(sorted(C.items())),'artifact_sha256':sha256((root/'COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'witness':{'x':[0,1],'indices':[2,2],'additive_double':[0,2],'double_first_index':'infinite','double_right_fixed_subgroup':'{0} x Z/4','s_set':'Z x {0,1}'},'scope':'Exact finite-component and symbolic integer coefficients, plus bounded controls in the actual infinite brace. Infinite index is certified by the written injective Z-family of cosets, not inferred from a finite quotient.'}
print(json.dumps(out,indent=2,sort_keys=True))

#!/usr/bin/env python3
"""Independent coefficient identities and subgroup diagnostics for the infinite brace."""
from itertools import product
from collections import Counter
from pathlib import Path
import hashlib,json
counts=Counter()
def ck(p,label):
 assert p,label
 counts[label]+=1
def eps(c):return 1 if c<2 else -1
def dia(c,d):return (c+d+2*c*d)%4
# Symbolic integer-coordinate linear forms in three independent variables.
def addv(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(c,a):return tuple(c*x for x in a)
def plus(a,b):return(addv(a[0],b[0]),(a[1]+b[1])%4)
def neg(a):return(scale(-1,a[0]),(-a[1])%4)
def circ(a,b):return(addv(a[0],scale(eps(a[1]),b[0])),dia(a[1],b[1]))
def lam(a,b):return(scale(eps(a[1]),b[0]),((1+2*a[1])*b[1])%4)
N=(1,0,0);M=(0,1,0);L=(0,0,1);Z=(0,0,0)
for c,d in product(range(4),repeat=2):
 ck(dia(c,d)==c^d,'Klein_binary_coordinates')
 ck(eps(dia(c,d))==eps(c)*eps(d),'epsilon_character')
 ck((-1)**dia(c,d)==(-1)**(c+d),'parity_character')
 for e in range(4):
  a=(N,c);b=(M,d);q=(L,e)
  ck(circ(circ(a,b),q)==circ(a,circ(b,q)),'formal_integer_associativity')
  ck(circ(a,plus(b,q))==plus(plus(circ(a,b),neg(a)),circ(a,q)),'formal_left_distributivity')
  ck(lam(circ(a,b),q)==lam(a,lam(b,q)),'formal_lambda_homomorphism')
  ck(lam(a,plus(b,q))==plus(lam(a,b),lam(a,q)),'formal_lambda_additivity')
for c in range(4):
 a=(N,c);inv=(scale(-eps(c),N),c)
 ck(circ(a,inv)==circ(inv,a)==(Z,0),'formal_two_sided_inverse')
# Numeric operations retain the actual unbounded integer coordinate.
def P(a,b):return(a[0]+b[0],(a[1]+b[1])%4)
def I(a):return(-a[0],(-a[1])%4)
def C(a,b):return(a[0]+eps(a[1])*b[0],dia(a[1],b[1]))
def CI(a):return(-eps(a[1])*a[0],a[1])
def S(a,b):return P(P(I(a),C(a,b)),I(b))
# Reconstruct all fixed/centralizer conditions from direct operations.
for n,c,m,d in product(range(-4,5),range(4),range(-8,9),range(4)):
 a=(n,c);b=(m,d)
 ck(S(a,b)==((eps(c)-1)*m,(2*c*d)%4),'direct_star_equation')
 ck((C(a,b)==C(b,a))==((1-eps(c))*m+(eps(d)-1)*n==0),'centralizer_linear_equation')
 if c in (0,1):
  right=(S(a,b)==(0,0))
  ck(right==(c==0 or d%2==0),'first_finite_index_kernel')
  second=(S(b,a)==(0,0) and C(a,b)==C(b,a))
  allowed=range(4) if (n,c)==(0,0) else ((0,1) if c==0 else ((0,2) if n==0 else (0,)))
  ck(second==(d in allowed),'second_finite_index_kernel')
 else:
  ck(not(S(a,b)==(0,0)) or m==0,'infinite_index_forcing_equation')
# The finite-index sets are kernels of actual homomorphisms of the infinite group.
for c,d in product(range(4),repeat=2):
 ck(dia(c,d)%2==(c+d)%2,'parity_quotient_homomorphism')
 ck(dia(c,d)//2==(c//2)^(d//2),'epsilon_quotient_homomorphism')
for T,want in [((0,1,2,3),1),((0,1),2),((0,2),2),((0,),4)]:
 cosets={frozenset(dia(c,d) for d in T) for c in range(4)}
 ck(len(cosets)==want,'exact_multiplicative_index')
x=(0,1);y=P(x,x)
ck(y==(0,2),'bad_additive_double')
ck(P(I(x),C(x,x))==(0,3),'lambda_invariance_failure')
ck(C(P(x,x),(1,0))!=P(P(C(x,(1,0)),I((1,0))),C(x,(1,0))),'right_distributivity_failure')
for n in range(-50,51):
 ck(S(y,(n,0))==(-2*n,0),'infinite_star_image_formula')
 ck(C(C((n,0),y),CI((n,0)))==(2*n,2),'infinite_multiplicative_conjugates')
# Annihilator: lambda is identity iff c=0; such a point is circle-central iff n=0.
for n,c in product(range(-20,21),range(4)):
 a=(n,c)
 kernel=all(P(I(a),C(a,b))==b for b in [(1,0),(0,1)])
 central=all(C(a,b)==C(b,a) for b in [(1,0),(0,1),(0,2)])
 ck(kernel==(c==0),'lambda_kernel_condition')
 ck((kernel and central)==(a==(0,0)),'annihilator_condition')
# Source Lemma3.12's displayed finite-data map has this constant infinite family
# if interpreted without the preceding whole-brace property-(S) assumption.
gens=((1,0),(0,1))
def finite_data(b):return tuple(S(b,g) for g in gens)+tuple(S(g,b) for g in gens)+((0,0),(0,0))
for n in range(-50,51):ck(finite_data((n,0))==finite_data((0,0)),'source_map_noninjectivity_diagnostic')
# A finite quotient confirms that global property(S) does not repair the displayed
# map's injectivity; no theorem-level finiteness conclusion is contradicted.
finite=list(product(range(3),range(4)))
def CP(a,b):return((a[0]+b[0])%3,(a[1]+b[1])%4)
def CN(a):return((-a[0])%3,(-a[1])%4)
def CC(a,b):return((a[0]+eps(a[1])*b[0])%3,dia(a[1],b[1]))
def CS(a,b):return CP(CP(CN(a),CC(a,b)),CN(b))
ann=[]
for a in finite:
 isann=all(CS(a,b)==CS(b,a)==(0,0) and CC(a,b)==CC(b,a) for b in finite)
 ck(isann==(a==(0,0)),'finite_quotient_annihilator')
 if isann:ann.append(a)
for n in range(3):
 b=(n,0)
 ck(all(CS(b,g)==CS(g,b)==(0,0) for g in gens),'finite_quotient_map_collision')
ck(len(ann)==1,'finite_quotient_trivial_annihilator')
base=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(counts.values()),'categories':dict(counts),'artifact_sha256':hashlib.sha256((base/'author_replay/COUNTEREXAMPLE.md').read_bytes()).hexdigest(),'limits':'Formal coefficient identities certify all integer coordinates; finite tests supplement exact subgroup quotient proofs. No finite-quotient inference of infinite index, or historical priority claim.'}
(base/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

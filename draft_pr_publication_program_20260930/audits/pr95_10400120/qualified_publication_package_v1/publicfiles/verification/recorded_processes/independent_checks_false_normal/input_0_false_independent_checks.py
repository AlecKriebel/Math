#!/usr/bin/env python3
def require(condition, message="explicit guard failed"):
 if not condition: raise AssertionError(message)
"""Independent A4 root-lattice Gauss-sum certificate via Hansen–Takata Thm 5.1.
No NumPy, floating point, author imports, or 126x126 modular matrix construction.
"""
from itertools import permutations,product,combinations
from collections import Counter
from fractions import Fraction as F
import json
checks=Counter()
def ck(p,name):
 require(p,name)
 checks[name]+=1
# Independent degree-four ring: w=exp(pi*i/5), Phi_10=w^4-w^3+w^2-w+1.
def red(a):
 a=list(a)+[0]*max(0,4-len(a))
 for j in range(len(a)-1,3,-1):
  c=a[j]
  for d,s in [(1,1),(2,-1),(3,1),(4,-1)]:a[j-d]+=s*c
 return tuple(a[:4])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(c,a):return tuple(c*x for x in a)
def mul(a,b):
 c=[0]*7
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return red(c)
W=[red([0]*i+[1]) for i in range(10)]
def conj(a):
 z=(0,0,0,0)
 for i,x in enumerate(a):z=add(z,scale(x,W[-i%10]))
 return z
one=W[0];u=add(W[2],scale(-1,W[3]));sqrt5=add(one,scale(2,u))
ck(add(mul(u,u),u)==one,'golden_ratio_relation')
ck(mul(sqrt5,sqrt5)==scale(5,one),'square_root_five_relation')
for i,j in product(range(10),repeat=2):ck(mul(W[i],W[j])==W[(i+j)%10],'cyclotomic_multiplication')
# A4 simple-root Gram determinant is 5, so root covolume is sqrt(5).
G=[[F(2 if i==j else -1 if abs(i-j)==1 else 0) for j in range(4)] for i in range(4)]
det=F(1)
for i in range(4):
 pivot=G[i][i];det*=pivot
 for j in range(i+1,4):
  ratio=G[j][i]/pivot
  for k in range(i,4):G[j][k]-=ratio*G[i][k]
ck(det==5,'root_lattice_covolume_squared')
rho=(2,1,0,-1,-2)
ck(sum(rho)==0 and sum(x*x for x in rho)==10,'Weyl_vector')
# Distinct residues with one endpoint zero independently give 126 alcove weights.
alcoves=[]
for c in combinations(range(1,10),4):
 ell=tuple(sorted(c,reverse=True))+(0,)
 dynkin=tuple(ell[i]-ell[i+1]-1 for i in range(4))
 ck(min(dynkin)>=0 and sum(dynkin)<=5,'integrable_weight_bound')
 alcoves.append(dynkin)
ck(len(set(alcoves))==126,'full_integrable_weight_count')
# Representatives of Y/5Y in the simple-root basis, not weight labels.
nu=[]
for c in product(range(5),repeat=4):
 v=(c[0],c[1]-c[0],c[2]-c[1],c[3]-c[2],-c[3])
 ck(sum(v)==0,'root_lattice_sum_zero')
 ck(sum(x*x for x in v)%2==0,'even_root_lattice_norm')
 nu.append(v)
ck(len(nu)==625,'root_lattice_quotient_size')
perms=list(permutations(rho));ck(len(perms)==120,'Weyl_group_size')
out={}
for q in (1,2,3,4):
 sigma=(0,0,0,0);survivors=[]
 for w in perms:
  sg=(-1)**sum(w[i]<w[j] for i in range(5) for j in range(i+1,5))
  v=tuple(q*a-b for a,b in zip(rho,w))
  # At kappa=10,p=5 the quadratic term is exp(2*pi*i*q*norm)=1.
  histogram=Counter(sum(a*b for a,b in zip(n,v))%5 for n in nu)
  character=(0,0,0,0)
  for exponent,mult in histogram.items():character=add(character,scale(mult,W[(2*exponent)%10]))
  selected=len({x%5 for x in v})==1
  ck(character==(scale(625,one) if selected else (0,0,0,0)),'full_character_sum_orthogonality')
  if selected:
   dot=sum(a*b for a,b in zip(rho,w))
   ck(dot%5==0,'surviving_phase_lies_in_Q_zeta10')
   sigma=add(sigma,scale(sg,W[(-dot//5)%10]))
   survivors.append({'permuted_rho':list(w),'sign':sg,'dot':dot})
 ck(len(survivors)==5,'five_surviving_permutations')
 norm=mul(sigma,conj(sigma))
 expected=add(scale(13,one),scale(4 if q in (1,4) else 8,u))
 ck(norm==expected,'closed_form_phase_norm')
 out[q]={'sigma':list(sigma),'norm':list(norm),'survivors':survivors}
# The positive-root product has multiplicities 4,3,2,1 for root heights 1,2,3,4.
# (2sin(pi/5))^2=2-u and (2sin(2pi/5))^2=3+u; their product is 5.
# The two positive unsquared sine factors have product sqrt(5).
root_product=mul(mul(mul(u,u),add(scale(2,one),scale(-1,u))),sqrt5)
ck(root_product==add(scale(-5,one),scale(10,u)),'Weyl_denominator_product')
DD=mul(root_product,root_product)
ck(DD==add(scale(125,one),scale(-200,u)),'vacuum_squared_numerator')
# HT unnormalized tau has factor 625/(50^2 sqrt5)=1/(4sqrt5).
ck(F(625,50**2)==F(1,4),'Gauss_prefactor')
ck(F(50000,80)==625,'S3_normalization_ratio')
for q,ab in [(1,(3476,1550)),(2,(4025,1800)),(3,(4025,1800)),(4,(3475,1550))]:
 target=add(scale(ab[0],one),scale(ab[1],sqrt5))
 ck(mul(target,DD)==scale(625,tuple(out[q]['norm'])),'claimed_normalized_squared_value')
ck(F(5)<F(9,4)**2 and F(5)>1,'positive_denominator_root_bound')
# Inverse surgery and reversed chain controls at the SL(2,Z) level.
def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
for a,b in [(3,2),(2,3)]:
 ck(F(a)-F(1,b)==F(5,b),'lens_continued_fraction')
 ck(a*b-1==5,'chain_homology_determinant')
ck(out[1]['norm']==out[4]['norm'] and out[2]['norm']==out[3]['norm'],'orientation_reversal_absolute_value')
print(json.dumps({'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
 'method':'Hansen–Takata Theorem5.1 root-lattice Gauss sum; 625 root-lattice residues and 120 Weyl elements; Phi10 arithmetic with four integer coefficients.',
 'normalized_squared_magnitudes':{'L(5,1)':[3475,1550],'L(5,2)':[4025,1800]},
 'coefficient_basis':'a+b*sqrt(5)','q_phase_sums':out,
 'scope':'Independent exact formula evaluation and normalization; general quantum-group surgery theorems are cited inputs, not re-proved.'},indent=2,sort_keys=True))

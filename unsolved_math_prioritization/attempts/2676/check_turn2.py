"""Exact finite algebra controls for Turn 2, not link-geometry certification."""
from itertools import product,permutations
from collections import Counter
from math import gcd
import sympy as sp
import json
C=Counter()
def ck(x,label):
 assert x,label
 C[label]+=1
# Even words in meridian involutions: Reidemeister-Schreier abelian coordinates.
# Index 0 denotes the distinguished involution t; a_i=m_i*t, a_0=1.
def coordinates(word,r):
 assert len(word)%2==0
 out=[0]*r
 for j,x in enumerate(word):
  if x:out[x-1]+=1 if j%2==0 else -1
 return tuple(out)
def reduce_word(w):
 out=[]
 for x in w:
  if out and out[-1]==x:out.pop()
  else:out.append(x)
 return tuple(out)
for r,maxlength in [(1,12),(2,10),(3,8)]:
 for length in range(0,maxlength+1,2):
  for word in product(range(r+1),repeat=length):
   v=coordinates(word,r)
   ck(coordinates((0,)+word+(0,),r)==tuple(-x for x in v),'deck_conjugation_negative_on_kernel_abelianization')
   ck(coordinates(reduce_word(word),r)==v,'involution_relations_preserve_rewriting')
# Standard Poincare presentation: perfect abelianization and explicit A5 quotient.
R=sp.Matrix([[2,-3,0],[0,3,-5],[-1,-1,4]])
ck(R.det()==-1,'poincare_relation_matrix_unimodular')
e=tuple(range(5))
def mul(p,q):return tuple(p[q[i]] for i in range(5))
def power(p,n):
 out=e
 for _ in range(n):out=mul(out,p)
 return out
x=(1,0,3,2,4)
y=next(p for p in permutations(range(5)) if p!=e and power(p,3)==e and power(mul(x,p),5)==e and mul(x,p)!=e)
xy=mul(x,y);z=power(xy,4)
ck(power(x,2)==power(y,3)==power(z,5)==mul(mul(x,y),z)==e,'poincare_nontrivial_permutation_quotient_relations')
generated={e};todo=[e]
while todo:
 g=todo.pop()
 for h in [x,y]:
  k=mul(g,h)
  if k not in generated:generated.add(k);todo.append(k)
ck(len(generated)==60,'poincare_quotient_has_order_60')
# The exact torus polynomial and determinant-one family.
t=sp.symbols('t')
poly=sp.cancel((t**15-1)*(t-1)/((t**3-1)*(t**5-1)))
ck(sp.Poly(poly,t).degree()==8,'torus35_alexander_degree')
ck(poly.subs(t,-1)==1,'torus35_determinant_one')
ck(sp.cancel(poly*poly.subs(t,1/t)).subs(t,-1)==1,'torus35_mirror_sum_determinant_one')
for p in range(3,26,2):
 for q in range(p+2,28,2):
  if gcd(p,q)==1:
   numerator = ((-1)**(p*q)-1)*(-2)
   denominator = ((-1)**p-1)*((-1)**q-1)
   ck(numerator==denominator,'odd_torus_determinant_formula')
# Minus identity always preserves a nonsingular integral symmetric lattice.
for n in range(1,10):
 for diag in [2,3,5]:
  A=sp.diag(*([diag]*n))
  for j in range(n-1):A[j,j+1]=A[j+1,j]=-1
  T=-sp.eye(n)
  ck(T.T*A*T==A,'minus_identity_lattice_isometry')
  ck(T*A.inv()==-A.inv(),'minus_identity_dual_action')
  ck(A.det()!=0,'tested_lattice_nonsingular')
# Exact characteristic-vector values and stabilization inertia bookkeeping.
for r in range(1,8):
 for bits in product([-1,1],repeat=r):
  ck(-sum(x*x for x in bits)+r==0,'diagonal_filling_correction_equality')
 for v in product([-3,-1,1,3],repeat=min(r,5)):
  ck(-sum(x*x for x in v)+len(v)<=0,'diagonal_filling_correction_inequality')
for pos in range(9):
 for neg in range(9):
  rank=pos+neg;sig=pos-neg
  ck((rank+2+sig)//2==pos+1 and (rank+2-sig)//2==neg+1,'tube_adds_one_index_of_each_sign')
  if rank and min(pos,neg)==0:ck((pos+1)*(neg+1)>0,'tube_destroys_definiteness')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'A5_quotient_generators':{'x':x,'y':y,'z':z},'scope':'Exact finite group-word, polynomial, lattice and signature controls. The topological and Floer statements require the written proof and primary inputs; original KP-1.17 unresolved.'},indent=2,sort_keys=True))

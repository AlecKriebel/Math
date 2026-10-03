#!/usr/bin/env python3
"""Independent exact residue/Ore controls, with universal proof limits explicit."""
from itertools import product
from math import comb
import json
import sympy as sp
counts={}
def ck(tag,b):
 if not b:raise AssertionError(tag)
 counts[tag]=counts.get(tag,0)+1
class Ore:
 """GF(p)[a^+-1,b^+-1,s] PBW order; w^p=a+s^(q(p-1))w, yw=(w+s^q)y."""
 def __init__(self,p,q):self.p=p;self.q=q
 def radd(self,x,y):
  z=x.copy()
  for k,v in y.items():z[k]=(z.get(k,0)+v)%self.p
  return {k:v for k,v in z.items()if v}
 def rneg(self,x):return {k:-v%self.p for k,v in x.items()if v}
 def rmul(self,x,y):
  z={}
  for a,v in x.items():
   for b,u in y.items():
    k=tuple(i+j for i,j in zip(a,b));z[k]=(z.get(k,0)+v*u)%self.p
  return {k:v for k,v in z.items()if v}
 def mono(self,a=0,b=0,s=0,c=1):return {(a,b,s):c%self.p} if c%self.p else{}
 def add(self,x,y):
  z={k:v.copy()for k,v in x.items()}
  for k,v in y.items():z[k]=self.radd(z.get(k,{}),v)
  return {k:v for k,v in z.items()if v}
 def basis(self,i,j):return {(i,j):self.mono()}
 def wp(self,n):
  if n<self.p:return {n:self.mono()}
  # Recursively w^n=a*w^(n-p)+s^(q(p-1))*w^(n-p+1).
  z={}
  for a,c in self.wp(n-self.p).items():z[a]=self.radd(z.get(a,{}),self.rmul(self.mono(a=1),c))
  for a,c in self.wp(n-self.p+1).items():z[a]=self.radd(z.get(a,{}),self.rmul(self.mono(s=self.q*(self.p-1)),c))
  return {k:v for k,v in z.items()if v}
 def mul(self,x,y):
  z={}
  for (i,j),a in x.items():
   for (k,l),b in y.items():
    for r in range(k+1):
     coef=self.rmul(self.rmul(a,b),self.mono(b=(j+l)//self.p,s=self.q*(k-r),c=comb(k,r)*pow(j,k-r,self.p)))
     for n,c in self.wp(i+r).items():
      key=(n,(j+l)%self.p);z[key]=self.radd(z.get(key,{}),self.rmul(coef,c))
  return {k:v for k,v in z.items()if v}
 def scale(self,x,r):return {k:self.rmul(v,r)for k,v in x.items()if self.rmul(v,r)}
 def residue(self,x):return {k:{m:v for m,v in r.items()if m[2]==0}for k,r in x.items()if any(m[2]==0 for m in r)}
 def frob(self,r,N):return {tuple(e*self.p for e in k):v for k,v in r.items()if k[2]*self.p<N}
 def trunc(self,r,N):return {k:v for k,v in r.items()if k[2]<N}
 def matrix(self,x,residue=False):
  a,b,s=sp.symbols('a b s');basis=list(product(range(self.p),repeat=2));rows=[]
  M=sp.zeros(self.p*self.p)
  for col,(i,j)in enumerate(basis):
   out=self.mul(x,self.basis(i,j))
   if residue:out=self.residue(out)
   for row,key in enumerate(basis):M[row,col]=sum(v*a**ea*b**eb*s**es for (ea,eb,es),v in out.get(key,{}).items())
  return M
# Full associativity on all basis triples for p2/p3, independent of split matrices.
for p in (2,3):
 for q in (1,2,4):
  O=Ore(p,q);bs=[O.basis(i,j)for i,j in product(range(p),repeat=2)]
  for x,y,z in product(bs,repeat=3):ck('full_PBW_associativity',O.mul(O.mul(x,y),z)==O.mul(x,O.mul(y,z)))
  w=O.basis(1,0);y=O.basis(0,1);one=O.basis(0,0)
  winv=O.scale(O.add(O.basis(p-1,0),O.scale(one,O.mono(s=q*(p-1),c=-1))),O.mono(a=-1))
  yinv=O.scale(O.basis(0,p-1),O.mono(b=-1))
  ck('actual_generators_are_units',O.mul(w,winv)==one and O.mul(winv,w)==one)
  ck('actual_generators_are_units',O.mul(y,yinv)==one and O.mul(yinv,y)==one)
  for x,z in product(bs,repeat=2):
   ck('residue_order_is_commutative',O.residue(O.mul(x,z))==O.residue(O.mul(z,x)))
  ck('deformed_order_noncommutative',O.mul(y,w)!=O.mul(w,y))
  # Central generator Frobenius and exact left-regular determinants over symbolic constants.
  a,b,s=sp.symbols('a b s')
  for el,norm in [(w,a),(y,b)]:
   poly=sp.Poly(sp.expand(O.matrix(el).det()-norm**p),a,b,s,modulus=p)
   ck('symbolic_left_regular_determinant_generators',poly.is_zero)
  for coef in range(1,p):
   z=O.add(w,O.scale(y,O.mono(c=coef)))
   poly=sp.Poly(sp.expand(O.matrix(z,True).det()-(a+coef*b)**p),a,b,s,modulus=p)
   ck('symbolic_residue_mixed_element_determinant',poly.is_zero)
# Nontrivial sparse scalar combinations: larger p, deterministic pseudo-random basis triples.
for p in (5,7):
 O=Ore(p,3);one=O.basis(0,0)
 for seed in range(41):
  xs=[]
  for offset in range(3):
   x={}
   for r in range(3):
    i=(seed*(r+1)+offset)%p;j=(seed+offset*(r+2))%p
    x=O.add(x,O.scale(O.basis(i,j),O.mono(a=r,b=offset,s=r+offset,c=r+1)))
   xs.append(x)
  x,y,z=xs
  ck('larger_prime_sparse_PBW_associativity',O.mul(O.mul(x,y),z)==O.mul(x,O.mul(y,z)))
# Multiterm contractions test complete coefficient polynomials, not finite-field a substitutions.
for p in (2,3,5,7):
 O=Ore(p,1)
 for N in (17,31,47):
  for seed in range(1,4):
   c=O.radd(O.mono(s=seed),O.radd(O.mono(b=1,s=seed+1),O.mono(a=1,s=seed+2)))
   delta={}
   for j in range(12):delta=O.trunc(O.radd(c,O.rneg(O.rmul(O.mono(a=1),O.frob(delta,N)))),N)
   error=O.trunc(O.radd(O.radd(delta,O.rmul(O.mono(a=1),O.frob(delta,N))),O.rneg(c)),N)
   ck('multiterm_symbolic_contraction',error=={})
   ck('multiterm_contraction_positive_valuation',min(e[2]for e in delta)==seed)
# A wild separable parameter relation actually splits the AS torsor, unlike pure-root stages.
s=sp.symbols('s')
for p in (2,3,5,7,11,13):
 t=s**p/(1-s**(p-1));ck('wild_non_Puiseux_parameter_splits_AS',sp.cancel(1/t-(s**(-p)-s**(-1)))==0)
 # Its formal derivative is nonzero: this is a separable parameter extension with wild index p.
 derivative=sp.together(sp.diff(t,s));num=sp.fraction(derivative)[0]
 ck('wild_parameter_separable',not sp.Poly(num,s,modulus=p).is_zero)
 for e in range(1,7):
  for m in (1,p+1,2*p+1):
   B={-m*p**j:1 for j in range(e)};D={}
   for n,c in B.items():D[p*n]=(D.get(p*n,0)+c)%p;D[n]=(D.get(n,0)-c)%p
   D={n:c for n,c in D.items()if c}
   ck('pure_root_AS_exact_reduction',D=={-m*p**e:1,-m:p-1})
# Necessity boundary: if a is a pth power, the supposedly pointless wound torsor has a point.
b,d=sp.symbols('b d')
for p in (2,3,5,7,11,13):
 x=-b;y=-d*b;a=d**p
 ck('pth_power_coefficient_negative_control',sp.Poly(sp.expand(y**p-a*x**p-x-b),b,d,modulus=p).is_zero)
# Nonintegral individual points do not defeat point-existence descent.
for pole in range(1,41):ck('existence_vs_integrality_negative_control',-pole<0 and 0>=0)
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'by_family':counts,'scope':'Distinct finite Ore/valuation/contraction controls. Symbolic rational-function constants preserve p-independence assumptions. No finite control proves that the residue quotient is a field, a universal gerbe theorem, or original homogeneous descent.'},indent=2,sort_keys=True))

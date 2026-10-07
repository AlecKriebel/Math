#!/usr/bin/env python3
"""Exact audit of the Turn 3 odd-order spectral-factor filters at orders 13 and 15."""
from itertools import product
from pathlib import Path
import sympy as sp
import json
z,t=sp.symbols('z t')

class Cyclo:
 def __init__(self,k):
  self.k=k;self.poly=sp.Poly(sp.cyclotomic_poly(2*k,z),z);self.d=self.poly.degree();self.mod=list(reversed([int(c) for c in self.poly.all_coeffs()]));self.zero=(0,)*self.d;self.one=(1,)+(0,)*(self.d-1)
  self.pows=[self.one]
  zz=(0,1)+(0,)*(self.d-2)
  for i in range(1,2*k):self.pows.append(self.mul(self.pows[-1],zz))
 def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
 def scale(self,a,s):return tuple(s*x for x in a)
 def mul(self,a,b):
  v=[0]*(2*self.d-1)
  for i,x in enumerate(a):
   if x:
    for j,y in enumerate(b):
     if y:v[i+j]+=x*y
  for i in range(len(v)-1,self.d-1,-1):
   if v[i]:
    q=v[i]
    for j in range(self.d):v[i-self.d+j]-=q*self.mod[j]
  return tuple(v[:self.d])
 def expr(self,a):return sum(c*z**i for i,c in enumerate(a))
 def from_expr(self,e):
  p=sp.Poly(e,z);return tuple(p.nth(i) for i in range(self.d))
 def inverse(self,a):return self.from_expr(sp.invert(self.expr(a),self.poly.as_expr(),z))
 def charpoly(self,a):
  cols=[self.mul(a,tuple(int(i==j) for i in range(self.d))) for j in range(self.d)]
  return sp.Poly(sp.Matrix(self.d,self.d,lambda i,j:cols[j][i]).charpoly(t).as_expr(),t)
 def integral(self,a):return all(c.q==1 for c in self.charpoly(a).all_coeffs())
 def factor_A(self,signs):
  A=[self.one,self.one]
  for j,sg in enumerate(signs,1):
   c=self.scale(self.add(self.pows[j],self.pows[2*self.k-j]),sg)
   out=[self.zero]*(len(A)+2)
   for i,x in enumerate(A):
    out[i]=self.add(out[i],x);out[i+1]=self.add(out[i+1],self.mul(x,c));out[i+2]=self.add(out[i+2],x)
   A=out
  return A

results=[]
# These two explicit orders are verification examples, not an exhaustive test of all orders.
for k in [13,15]:
 C=Cyclo(k);stats={'k':k,'field_degree':C.d,'patterns':2**((k-1)//2),'zero_interior_sum':0,'failed_total_realness':0,'failed_integrality':0,'survivors':[]};rejects=[]
 for signs in product([-1,1],repeat=(k-1)//2):
  A=C.factor_A(signs);L=C.zero
  for a in A[1:-1]:L=C.add(L,a)
  if L==C.zero:
   stats['zero_interior_sum']+=1;continue
  V=C.add(L,C.scale(C.one,2));cp=C.charpoly(V)
  assert cp.count_roots(-sp.oo,0)==0
  if cp.count_roots(0,2)>0:
   stats['failed_total_realness']+=1;rejects.append({'signs':signs,'reason':'A(1) has a conjugate in (0,2)','polynomial':str(cp.sqf_part().as_expr())});continue
  invL=C.inverse(L)
  bad=None
  for j,a in enumerate(A[1:-1],1):
   quot=C.mul(C.mul(a,a),invL)
   cpq=C.charpoly(quot)
   if any(c.q!=1 for c in cpq.all_coeffs()):
    bad={'index':j,'polynomial':str(cpq.sqf_part().as_expr())};break
  if bad:
   stats['failed_integrality']+=1;rejects.append({'signs':signs,'reason':'coefficient-square quotient not algebraic integer',**bad});continue
  stats['survivors'].append({'signs':signs,'A_coefficients':[str(C.expr(a)) for a in A]})

 retained=[]; negative=[]
 for candidate in stats['survivors']:
  exprs=[sp.sympify(a) for a in candidate['A_coefficients']]
  assert all(not a.has(z) for a in exprs), 'Surviving coefficients must be explicitly resolved before acceptance.'
  if any(a<0 for a in exprs): negative.append(candidate)
  else: retained.append(candidate)
 stats['negative_coefficient_rejections']=len(negative)
 stats['nonnegative_survivors']=retained
 if k==13:
  assert (stats['zero_interior_sum'],stats['failed_total_realness'],stats['failed_integrality'],len(retained))==(1,62,1,0)
 elif k==15:
  assert (stats['zero_interior_sum'],stats['failed_total_realness'],stats['failed_integrality'],len(negative),len(retained))==(2,114,10,1,1)
  assert retained[0]['A_coefficients']==[str(1 if j in [0,15] else 2 if j in [5,10] else 0) for j in range(16)]
 print(stats,flush=True);results.append({'summary':stats,'rejections':rejects,'negative_coefficient_candidates':negative})
Path(__file__).with_name('turn03_verification.json').write_text(json.dumps({'all_passed':True,'sympy_version':sp.__version__,'arithmetic':'Exact rational cyclotomic-field arithmetic and exact real-root counts; no floating point.','orders':results},indent=2)+'\n')

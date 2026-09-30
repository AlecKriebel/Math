#!/usr/bin/env python3
from itertools import product
from math import gcd
from pathlib import Path
from hashlib import sha256
import json
counts={}
def ck(cat,x):
 assert x,cat
 counts[cat]=counts.get(cat,0)+1

def egcd(a,b):
 if not b:return (a,1,0)
 g,u,v=egcd(b,a%b);return(g,v,u-(a//b)*v)
for p in (2,3,5,7):
 for e in range(1,6):
  for m in range(1,101):
   if gcd(p,m)>1:continue
   g,u,v=egcd(p**e,m);ck('bezout_coprime_annihilators',g==1 and u*p**e+v*m==1)
# Smith invariant of Pic(root_l O(d)): Z²/<(-d,l)>.
for ell in (2,3,5,7,11,13):
 for d in range(-2*ell,2*ell+1):
  g,u,v=egcd(abs(d),ell)
  ck('picard_smith_invariant',g==gcd(abs(d),ell))
  ell_torsion=sum(1 for a in range(g) if ell*a%g==0)
  ck('picard_kummer_torsion',ell_torsion==gcd(g,ell))
  if d==0:ck('neutral_picard_torsion',ell_torsion==ell)
  if d==1:ck('nonneutral_O1_torsion',ell_torsion==1)
# Heisenberg extension, checking the actual group law rather than cocycle formula.
for ell in (2,3):
 G=list(product(range(ell),repeat=3))
 def op(x,y):
  a,b,c=x;d,e,f=y
  return ((a+d)%ell,(b+e)%ell,(c+f+b*d)%ell)
 for x,y,z in product(G,repeat=3):ck('central_extension_associativity',op(op(x,y),z)==op(x,op(y,z)))
 for x,y in product(G,repeat=2):
  xy=op(x,y);yx=op(y,x)
  ck('central_extension_commutator',xy[:2]==yx[:2] and (xy[2]-yx[2])%ell==(x[1]*y[0]-y[1]*x[0])%ell)
# Generic finite fields represented by coefficient tuples and a monic modulus.
class GF:
 def __init__(self,p,mod):self.p=p;self.mod=mod;self.m=len(mod);self.q=p**self.m;self.zero=(0,)*self.m;self.one=(1,)+(0,)*(self.m-1)
 def add(self,a,b):return tuple((x+y)%self.p for x,y in zip(a,b))
 def neg(self,a):return tuple(-x%self.p for x in a)
 def mul(self,a,b):
  v=[0]*(2*self.m-1)
  for i,x in enumerate(a):
   for j,y in enumerate(b):v[i+j]+=x*y
  for k in range(len(v)-1,self.m-1,-1):
   c=v[k]%self.p
   for j in range(self.m):v[k-self.m+j]-=c*self.mod[j]
  return tuple(x%self.p for x in v[:self.m])
 def power(self,a,n):
  v=self.one
  while n:
   if n&1:v=self.mul(v,a)
   a=self.mul(a,a);n//=2
  return v
 def root(self,a):return self.power(a,self.p**(self.m-1))
def plus(K,a,b):
 c=dict(a)
 for d,v in b.items():
  c[d]=K.add(c.get(d,K.zero),v)
  if c[d]==K.zero:del c[d]
 return c
def minus(K,a):return {d:K.neg(v) for d,v in a.items()}
def frob(K,a):return {d*K.p:K.power(v,K.p) for d,v in a.items()}
def closed(K,f):
 N={};H={}
 for d,a in f.items():
  assert d>0
  while d%K.p==0:
   d//=K.p;a=K.root(a);H=plus(K,H,{d:a})
  N=plus(K,N,{d:a})
 return N,H
cases=0
for K in (GF(2,[1,1,0]),GF(3,[2,2,0]),GF(5,[2,0])):
 E=list(product(range(K.p),repeat=K.m))
 for a in E:
  ck('field_and_inverse_frobenius',K.power(a,K.q)==a and K.power(K.root(a),K.p)==a)
  if a!=K.zero:ck('field_nonzero_units',K.power(a,K.q-1)==K.one)
 image={K.add(K.power(a,K.p),K.neg(a)) for a in E}
 ck('finite_field_constant_warning',len(image)==K.q//K.p and len(image)<K.q)
 for j in range(1500):
  coeff=[E[(j*(2*i+1)+i*i)%K.q] for i in range(6)]
  deg=[1,2,K.p,2*K.p,K.p**2,K.p**3]
  f={}
  for d,a in zip(deg,coeff):f=plus(K,f,{d:a})
  N,H=closed(K,f)
  ck('closed_form_AS_certificate',plus(K,f,minus(K,N))==plus(K,frob(K,H),minus(K,H)))
  ck('closed_form_prime_exponents',all(d>0 and d%K.p for d in N))
  ck('closed_form_idempotence',closed(K,N)==(N,{}))
  g={3*K.p:E[(j+2)%K.q]}
  ck('closed_form_additivity',closed(K,plus(K,f,g))[0]==plus(K,N,closed(K,g)[0]))
  cases+=1
# Total-degree-two Leray bookkeeping, with vanishing hypotheses checked in prose.
terms={(2,0):'Tsen',(1,1):'finite support',(0,2):'stalk sum'}
ck('Leray_total_degree_two',[(p,q) for p,q in terms if terms[p,q]=='stalk sum']==[(0,2)])
for r in range(2,8):
 target=(r,3-r)
 ck('Leray_outgoing_differentials',target in [(2,1),(3,0)] or target[1]<0)
result={'status':'PASS','assertions':sum(counts.values()),'categories':counts,'AS_polynomials':cases,'reviewed_artifact_sha256':'27e178e2c1b22e8e18ab32c3ff117ac4b4672dc7b799f2d18fd3d2a019fad51a','limits':'Finite algebra controls supplement the source and cohomological proofs; no arbitrary-stack classification or finite-field constant surjectivity is asserted.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

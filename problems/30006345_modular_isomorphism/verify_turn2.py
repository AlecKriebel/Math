#!/usr/bin/env python3
"""Exact author controls: actual finite groups, class sums, and center radical layers;
then independent finite implementation of the parameter recovery in TURN_2.md.
Standard library only. No general theorem is inferred from the finite sample.
"""
from itertools import product
from collections import Counter,deque
from functools import lru_cache
from math import prod
import json
checks=Counter()
def ck(x,label):
 assert x,label
 checks[label]+=1

def group_case(p,e,d=0):
 q=p**e
 if e==1:
  add=lambda x,y:(x+y)%p
  mul=lambda x,y:x*y%p
  neg=lambda x:-x%p
 else:
  assert e==2
  add=lambda x,y:((x%p+y%p)%p)+p*((x//p+y//p)%p)
  mul=lambda x,y:((x%p*(y%p)+d*(x//p)*(y//p))%p)+p*((x%p*(y//p)+x//p*(y%p))%p)
  neg=lambda x:(-(x%p)%p)+p*((-(x//p))%p)
 def gp(g,h):return (add(g[0],h[0]),add(g[1],h[1]),add(add(g[2],h[2]),mul(g[0],h[1])))
 def gi(g):return (neg(g[0]),neg(g[1]),add(neg(g[2]),mul(g[0],g[1])))
 gens=[(p**i,0,0) for i in range(e)]+[(0,p**i,0) for i in range(e)]
 conj=[(h,gi(h)) for h in gens]
 universe=set(product(range(q),repeat=3));remaining=set(universe);classes=[]
 while remaining:
  first=min(remaining);C={first};todo=deque([first])
  while todo:
   g=todo.popleft()
   for h,hi in conj:
    v=gp(gp(h,g),hi)
    if v not in C:C.add(v);todo.append(v)
  ck(C<=remaining,'disjoint_conjugacy_orbits')
  remaining-=C;classes.append(tuple(sorted(C)))
 N=len(classes);which={g:i for i,C in enumerate(classes) for g in C}
 ck(sum(map(len,classes))==q**3,'conjugacy_partition_size')
 ck(N==q*q+q-1,'class_count_formula')
 ck(Counter(map(len,classes))==Counter({1:q,q:q*q-1}),'class_size_distribution')
 table={}
 for i,C in enumerate(classes):
  for j in range(i,N):
   D=classes[j];coeff=Counter(gp(g,h) for g in C for h in D)
   coeff={g:v%p for g,v in coeff.items() if v%p}
   out={}
   for g,v in coeff.items():
    z=which[g]
    if z not in out:out[z]=v
    else:ck(out[z]==v,'class_sum_product_centrality')
   ck(sum(len(classes[z]) for z in out)==len(coeff),'class_sum_product_full_support')
   if len(C)==len(D)==1:expected={which[gp(C[0],D[0])]:1}
   elif len(C)==1:expected={j:1}
   elif len(D)==1:expected={i:1}
   else:expected={}
   ck(out==expected,'center_square_zero_extension_product')
   table[i,j]=table[j,i]=out
 def vmul(v,w):
  ans=[0]*N
  for i,a in enumerate(v):
   if not a:continue
   for j,b in enumerate(w):
    if b:
     for z,c in table[i,j].items():ans[z]=(ans[z]+a*b*c)%p
  return ans
 def span(vecs):
  piv={}
  for v in vecs:
   v=[a%p for a in v]
   for j,u in sorted(piv.items()):
    c=v[j]
    if c:v=[(a-c*b)%p for a,b in zip(v,u)]
   j=next((j for j,a in enumerate(v) if a),None)
   if j is not None:
    inv=pow(v[j],-1,p);piv[j]=[(a*inv)%p for a in v]
  return list(piv.values())
 unit=which[(0,0,0)];rad=[]
 for i,C in enumerate(classes):
  if i==unit:continue
  v=[0]*N;v[i]=1;v[unit]=(-len(C))%p;rad.append(v)
 current=span(rad);dims=[N,len(current)]
 for _ in range(1,30):
  current=span(vmul(v,w) for v in current for w in rad)
  dims.append(len(current))
  if not current:break
 else:raise AssertionError('nilpotence bound exceeded')
 hilbert=[a-b for a,b in zip(dims,dims[1:])]
 expected=poly_pow([1]*p,e);expected[1]+=q*q-1
 ck(hilbert==expected,'center_radical_hilbert_formula')
 ck(dims[-1]==0 and len(hilbert)-1==e*(p-1),'center_radical_top_degree')
 return {'p':p,'e':e,'group_order':q**3,'class_count':N,'center_radical_power_dimensions':dims,'hilbert_polynomial_coefficients':hilbert}

def trim(a):
 a=list(a)
 while len(a)>1 and a[-1]==0:a.pop()
 return a
def poly_mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def poly_pow(a,n):
 out=[1]
 for _ in range(n):out=poly_mul(out,a)
 return out
def poly_div_exact(a,b):
 a=list(a);b=trim(b);assert b[-1]==1
 if len(a)<len(b):raise AssertionError('nondivisible degree')
 out=[0]*(len(a)-len(b)+1)
 for j in range(len(out)-1,-1,-1):
  z=a[j+len(b)-1];out[j]=z
  for i,c in enumerate(b):a[j+i]-=z*c
 assert not any(a),'nonzero remainder'
 return trim(out)
def quotient_coefficient(num,den,d):
 assert den[0]==1
 out=[]
 for i in range(d+1):out.append((num[i] if i<len(num) else 0)-sum(den[j]*out[i-j] for j in range(1,min(i,len(den)-1)+1)))
 return out[-1]
@lru_cache(None)
def Apow(p,e):return poly_pow([1]*p,e)
def he(p,e):
 h=list(Apow(p,e));h[1]+=p**(2*e)-1;return h

def recover(p,n,L):
 D=len(L)-1
 assert L[-1]==1 and D%(p-1)==0
 s=D//(p-1);assert (n-s)%2==0 and (3*s-n)%2==0
 R=(n-s)//2;a=(3*s-n)//2;assert R>=0 and a>=0
 initialR=R;P=list(reversed(L));es=[]
 for e in range(1,initialR+1):
  if not R:break
  c=p**(2*e)-1;d=e*(p-1)-1
  coefficient=quotient_coefficient(P,Apow(p,a+R),d)
  assert coefficient>=0 and coefficient%c==0
  multiplicity=coefficient//c
  for _ in range(multiplicity):P=poly_div_exact(P,list(reversed(he(p,e))));es.append(e);R-=e
  assert R>=0
 assert R==0 and P==Apow(p,a)
 return a,tuple(es)
def parts(n,lo=1):
 if n==0:yield ();return
 for i in range(lo,n+1):
  for tail in parts(n-i,i):yield (i,)+tail

cases=[group_case(3,1),group_case(3,2,2),group_case(5,1)]
recovery_cases=0;by_prime={}
for p in (3,5,7):
 seen={};count=0
 for r in range(13):
  for es in parts(r):
   for a in range(5):
    L=list(Apow(p,a))
    for e in es:L=poly_mul(L,he(p,e))
    n=a+3*r
    ck(recover(p,n,L)==(a,es),'parameter_recovery')
    sig=n,tuple(L)
    ck(sig not in seen,'distinct_parameter_signature')
    seen[sig]=a,es
    ck(sum(L)==p**a*prod(p**(2*e)+p**e-1 for e in es),'center_dimension_product')
    count+=1;recovery_cases+=1
 by_prime[str(p)]=count
print(json.dumps({'status':'PASS','arithmetic':'exact finite-field and integer','assertions':sum(checks.values()),'assertions_by_scope':dict(checks),'actual_group_cases':cases,'parameter_recovery_cases':recovery_cases,'recovery_cases_by_prime':by_prime,'scope':'Both input groups are required to be elementary-abelian times finite-field Heisenberg products. These finite controls do not establish family membership for an arbitrary group or solve the original all-field problem.'},indent=2,sort_keys=True))

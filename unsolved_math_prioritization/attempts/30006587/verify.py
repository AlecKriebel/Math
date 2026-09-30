#!/usr/bin/env python3
"""Exact formal-word diagnostics, not an analytic proof of the preprint's realization theorem."""
from collections import Counter,defaultdict
from functools import lru_cache
from fractions import Fraction as Q
from itertools import product
from math import factorial
from pathlib import Path
from hashlib import sha256
import json
C=Counter()
def ck(name,v):
 assert v,name;C[name]+=1
def clean(x):return {w:c for w,c in x.items() if c}
def add(*xs):
 out=defaultdict(Q)
 for x in xs:
  for w,c in x.items():out[w]+=c
 return clean(out)
def scale(x,c):return clean({w:v*c for w,v in x.items()})
def unit(w):return {w:Q(1)}
def extend(fn,x):return add(*(scale(fn(w),c) for w,c in x.items()))
def prefix(a,x):return {(a,)+w:c for w,c in x.items()}
@lru_cache(None)
def stuff(a,b):
 if not a:return unit(b)
 if not b:return unit(a)
 merged=tuple(x+y for x,y in zip(a[0],b[0])) if isinstance(a[0],tuple) else a[0]+b[0]
 return add(prefix(a[0],stuff(a[1:],b)),prefix(b[0],stuff(a,b[1:])),prefix(merged,stuff(a[1:],b[1:])))
def times(x,y):return add(*(scale(stuff(a,b),c*d) for a,c in x.items() for b,d in y.items()))
@lru_cache(None)
def shufxy(a,b):
 if not a:return unit(b)
 if not b:return unit(a)
 return add(prefix(a[0],shufxy(a[1:],b)),prefix(b[0],shufxy(a,b[1:])))
def xy(w):return tuple(a for k in w for a in (0,)*(k-1)+(1,))
def ind(w):
 out=[];k=1
 for a in w:
  if a:k0=k;out.append(k0);k=1
  else:k+=1
 assert k==1
 return tuple(out)
@lru_cache(None)
def shuffle(a,b):return {ind(w):c for w,c in shufxy(xy(a),xy(b)).items()}
@lru_cache(None)
def antipode(w):
 if not w:return unit(())
 return scale(add(*(times(antipode(w[:j]),unit(w[j:])) for j in range(len(w)))),-1)
@lru_cache(None)
def drop_one(w):
 if 1 not in w:return unit(w)
 assert w[0]>=2 and w.count(1)==1
 i=w.index(1);k,l=w[:i],w[i+1:]
 return add(unit(w),*(times(unit(k[:j]),extend(lambda v:shuffle(v,(1,)),times(antipode(k[j:]),unit(l)))) for j in range(len(k)+1)))
def theta(w):return add(extend(drop_one,shuffle(w,(2,))),scale(stuff(w,(2,)),-1))
def embed(w):return tuple((k,0) for k in w)
def rho(w,i):
 if not 0<=i<len(w):return {}
 v=list(w);k,d=v[i];v[i]=(k,d+1);return unit(tuple(v))
def deriv(w):return add(*(scale(unit(w[:j]+((k+1,d+1),)+w[j+1:]),k) for j,(k,d) in enumerate(w)))
def words(maxwt,minpart=2):
 yield ()
 def rec(pref,total):
  for k in range(minpart,maxwt-total+1):
   w=pref+(k,);yield w;yield from rec(w,total+k)
 yield from rec((),0)
# The literal x-y shuffle verifies the exceptional one-1 term independently.
ws=list(words(11))
for w in ws:
 sh=shuffle(w,(2,));actual={v:c for v,c in sh.items() if 1 in v};expected={}
 for j,k in enumerate(w):
  v=list(w);v[j]+=1;v=tuple(v)
  for i in range(j+1,len(w)+1):expected=add(expected,scale(unit(v[:i]+(1,)+v[i:]),2*k))
 ck('one_1_shuffle_component',actual==expected)
 th=theta(w)
 ck('theta_admissible_output',all(all(k>=2 for k in v) for v in th))
 ck('theta_weight_shift',all(sum(v)==sum(w)+2 for v in th))
 # The two boundary rho terms telescope at every fixed differentiated index.
 total={}
 for j,k in enumerate(w):
  v=list(embed(w));v[j]=(k+1,0);v=tuple(v)
  for i in range(j+1,len(w)+1):total=add(total,scale(add(rho(v,i-1),scale(rho(v,i),-1)),2*k))
 ck('formal_telescoping',total==scale(deriv(embed(w)),2))
ck('unit_case',theta(())=={})
for k in range(2,12):
 expected=add(unit((k+2,)) and scale(unit((k+2,)),2*k-1),scale(unit((2,k)),-1),*(scale(unit((k-j+2,j)),-(k+j-1)) for j in range(2,k+1)))
 ck('credited_depth_one_theta',theta((k,))==expected)
for r in range(1,6):
 ck('credited_all_twos_theta',theta((2,)*r)==add(scale(stuff((2,)*r,(2,)),3),scale(unit((2,)*(r+1)),-(r+1)*(2*r+3))))
ck('source_theta_2',theta((2,))=={(4,):3,(2,2):-4})
ck('source_theta_3',theta((3,))=={(5,):5,(3,2):-4,(2,3):-6})
ck('source_theta_22',theta((2,2))=={(4,2):3,(2,4):3,(2,2,2):-12})
# Appendix A.3 on genuine bi-letter words, including nonzero lower indices.
alphabet=((1,0),(2,0),(2,1),(3,2))
for r in range(1,4):
 for k in product(alphabet,repeat=r):
  for l in ((),((1,1),),((2,0),(1,2))):
   lhs=add(*(times(unit(k[:j]),extend(lambda w:rho(w,0),times(antipode(k[j:]),unit(l)))) for j in range(r+1)))
   rhs=add(rho(k+l,r),scale(rho(k+l,r-1),-1))
   ck('antipode_rho_identity_A3',lhs==rhs)
# Swap is transposed coefficient substitution in the divided-power convention.
@lru_cache(None)
def comps(n,r):
 if r==0:return ((),) if n==0 else ()
 return tuple((a,)+b for a in range(n+1) for b in comps(n-a,r-1))
def linear_poly_product(forms,powers,r):
 out={(0,)*r:1}
 for form,n in zip(forms,powers):
  for _ in range(n):
   new=defaultdict(int)
   for e,c in out.items():
    for j,v in form:
     f=list(e);f[j]+=1;new[tuple(f)]+=c*v
   out=clean(new)
 return out
@lru_cache(None)
def sigma(w):
 r=len(w)
 if r==0:return unit(())
 k=tuple(a-1 for a,b in w);d=tuple(b for a,b in w)
 vforms=tuple(((r-i-1,1),) if i==0 else ((r-i-1,1),(r-i,-1)) for i in range(r))
 uforms=tuple(tuple((j,1) for j in range(r-i)) for i in range(r))
 out={}
 for dp in comps(sum(k),r):
  c=linear_poly_product(vforms,dp,r).get(k,0)
  if not c:continue
  pref=Q(c)
  for a in d:pref*=factorial(a)
  for a in dp:pref/=factorial(a)
  for ep in comps(sum(d),r):
   e=linear_poly_product(uforms,ep,r).get(d,0)
   if e:out[tuple((a+1,b) for a,b in zip(ep,dp))]=pref*e
 return out
for w in words(7,1):
 if len(w)>3:continue
 e=embed(w)
 ck('swap_involution',extend(sigma,sigma(e))==unit(e))
 for a in (1,2):
  lhs=extend(sigma,times(sigma(e),sigma(((a,0),))))
  expected={embed(v):c for v,c in shuffle(w,(a,)).items()}
  expected=add(expected,rho(e,0) if a==1 else deriv(e))
  ck('swap_shuffle_derivative_identity',lhs==expected)
# For a fixed finite harmonic sum, verify the one-1 Drop1 expression directly.
@lru_cache(None)
def hn(w,N):
 if not w:return Q(1)
 return sum((Q(1,m**w[0])*hn(w[1:],m) for m in range(1,N)),Q())
def diamond_one(w,N):
 if 1 not in w:return hn(w,N)
 j=w.index(1);r=len(w);out=Q()
 for ns in product(range(1,N),repeat=r):
  if all(ns[i-1]>ns[i] for i in range(1,r)):out+=Q(1,prod(ns[i]**w[i] for i in range(r)))
  if all(ns[i-1]>ns[i] if i!=j else ns[i-1]>=ns[i] for i in range(1,r)):
   out+=Q(1,(N-ns[j])*prod(ns[i]**w[i] for i in range(r) if i!=j))
 return out
def prod(xs):
 v=1
 for x in xs:v*=x
 return v
for k in (2,3,4):
 for suffix in ((),(2,),(3,),(2,2)):
  w=(k,1)+suffix
  for N in range(2,8):
   ck('finite_diamond_drop1',diamond_one(w,N)==sum(c*hn(v,N) for v,c in drop_one(w).items()))
root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),'admissible_words_through_weight_11':len(ws),'scope':'Exact formal-word and finite-harmonic controls only. These do not prove the analytic bi-MES realization, all analytic derivative identities or the completeness conjecture.','source_status_sha256':sha256((root/'SOURCE_STATUS.md').read_bytes()).hexdigest() if (root/'SOURCE_STATUS.md').exists() else None}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

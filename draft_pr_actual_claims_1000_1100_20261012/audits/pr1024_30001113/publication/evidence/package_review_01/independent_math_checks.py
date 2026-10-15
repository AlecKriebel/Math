"""Independent finite boundary checks, never used as proof of full formal series."""
from pathlib import Path
from itertools import product
import json,sys
from datetime import datetime,timezone
R=Path(__file__).resolve().parent
G=[[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]]
def mul(a,b):return G[a][b]
def add(a,b):return [x^y for x,y in zip(a,b)]
def prod(a,b):
 n=len(a);c=[0]*n
 for i,x in enumerate(a):
  for j,y in enumerate(b[:n-i]):c[i+j]^=mul(x,y)
 return c
def powr(a,n):
 c=[1]+[0]*(len(a)-1)
 for _ in range(n):c=prod(c,a)
 return c
def mm(a,b):return [[add(prod(a[i][0],b[0][j]),prod(a[i][1],b[1][j])) for j in range(2)] for i in range(2)]
def sm(s,a):return [[prod(s,x) for x in row] for row in a]
def equal(a,b,label):
 if a!=b:raise RuntimeError(label)
rows=[]
for length in (3,4):
 o=[1]+[0]*(length-1);e=[0,1]+[0]*(length-2);zero=[0]*length;ee=prod(e,e)
 for a in (1,2,3):
  ae=[mul(a,x) for x in e];target=add(e,[mul(mul(a,a),x) for x in ee]);c=[[add(o,ae),ae],[zero,o]];m=[[o,e],[o,o]];mp=[[o,target],[o,o]]
  identity=mm(mp,c)==sm(add(o,ae),mm(c,m));equal(identity,length==3,'cubic-only conjugacy a='+str(a))
  rows.append({'nilpotency':length,'parameter_a':a,'matrix_identity':identity,'expected':length==3})
# Reconstruct the Proposition 6.1 injection equality with its square-root translation.
o=[1,0,0];w=[0,1,0];w2=[0,0,1];zero=[0,0,0];c=[[add(o,w),w],[zero,o]]
equal(mm([[o,w2],[o,o]],c),sm(add(o,w),mm(c,[[o,zero],[o,o]])),'injected tangent/basepoint actual conjugacy')
def operator(f):
 n=len(f);s=[0]+[1]*(n-1);v=[0]*n;power=[1]+[0]*(n-1)
 for a in f:v=add(v,[mul(a,x) for x in power]);power=prod(power,s)
 weight=[1,0,1]+[0]*(n-3)
 return prod(weight,v)
def rank(mat):
 a=[row[:] for row in mat];k=0
 for col in range(len(a[0])):
  pivot=next((r for r in range(k,len(a)) if a[r][col]),None)
  if pivot is None:continue
  a[k],a[pivot]=a[pivot],a[k];p=a[k][col];inv=next(x for x in (1,2,3) if mul(p,x)==1);a[k]=[mul(inv,x) for x in a[k]]
  for r in range(len(a)):
   if r!=k and a[r][col]:q=a[r][col];a[r]=[x^mul(q,y) for x,y in zip(a[r],a[k])]
  k+=1
 return k
trunc=[]
for n in (5,6,9,10,17,18,33,34,41,42):
 for start in (0,1,2):
  cols=[]
  for i in range(start,n):
   e=[0]*n;e[i]=1;equal(operator(operator(e)),e,'T squared');cols.append(add(operator(e),e)[start:])
  mat=[list(x) for x in zip(*cols)];r=rank(mat);h=(n-start)-2*r
  trunc.append({'precision':n,'lattice_start':start,'dimension':n-start,'rank_T_minus_1':r,'finite_H1_dimension':h})
  if start==1:equal(h,0 if n%2 else 1,'finite M H1 parity artifact')
  if start==0:equal(h,1 if n%2 else 2,'finite sharp H1 parity artifact')
# All 1024 arbitrary degree-four conjugators, including constants, have zero
# constant coboundary. The nontrivial tangent normalized cocycle is 1+y.
conjugators=0
for coefficients in product(range(4),repeat=5):
 f=list(coefficients)+[0]*4;equal(add(operator(f),f)[0],0,'conjugator constant cancellation');conjugators+=1
# Selected complete-formula prefixes at several nonzero coefficient patterns.
series=[]
for n in (17,33,41):
 y=[0,1]+[0]*(n-2);z=[0,0]+[1]*(n-2);y2=prod(y,y)
 for pattern in (1,2,3):
  h=[0]*n;zp=[1]+[0]*(n-1)
  for j in range(n//2):h=add(h,[mul((j*pattern+pattern)%4,x) for x in zp]);zp=prod(zp,z)
  equal(add(operator(prod(y,h)),prod(y,h)),prod(y2,h),'series coboundary');equal(operator(prod(y2,h)),prod(y2,h),'series invariant');series.append({'precision':n,'pattern':pattern})
result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','cubic_vs_quartic_boundaries':rows,'prior_injection_explicit_conjugacy':True,'conjugators_with_nilpotent_constants_tested':conjugators,'series_prefix_checks':series,'finite_cohomology_artifact_demonstration':trunc,'limits':'Finite checks only. Even precision creates spurious highest-order cocycles; changing the integral lattice also changes H1. Full proofs remain necessary.'}
(R/'receipts/INDEPENDENT_MATH_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('finite_cohomology_artifact_demonstration','cubic_vs_quartic_boundaries')},indent=2))

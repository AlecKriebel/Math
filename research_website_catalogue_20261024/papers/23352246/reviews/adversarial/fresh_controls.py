"""Fresh exact falsification controls for 23352246; no published checker imports.
Uses dual-certified arbitrary LP optima, bulk signed-layer removal, an analytic
K2,2 completion oracle, and constructive finite convex mixtures of recession
steps. Finite diagnostics, not a polynomial LP/SFM/GLS implementation.
"""
from fractions import Fraction as Q
from itertools import product
from math import ceil, floor, lcm, factorial
from pathlib import Path
import random, json, hashlib
R=random.Random(23352246)
counts={}
def need(c,m):
 if not c: raise RuntimeError(m)
def tick(k,n=1): counts[k]=counts.get(k,0)+n
def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q(0))
def decompose(d):
 ans=[]
 for sign in (-1,1):
  levels=sorted({sign*x for x in d if sign*x>0})
  prev=Q(0)
  for level in levels:
   ans.append((level-prev,tuple(sign*int(sign*x>=level) for x in d)))
   prev=level
 return ans
# Dual certificates deliberately supply nonvertex/unanchored relaxation optima.
for trial in range(650):
 n=R.randint(1,10);split=R.randrange(n+1);U=set(range(split));I={i for i in range(n) if R.randrange(2)}
 scale=(1<<157) if trial%13==0 else 1
 star=tuple(Q(R.randint(-12,12)*scale,R.choice([1,2,5,17,97])) for _ in range(n))
 edges=[];a=[Q(0)]*n
 for u in U:
  for v in range(split,n):
   if R.randrange(3)==0:continue
   slack=Q(0) if R.randrange(2) else Q(R.randint(1,8),R.choice([2,7,19]))
   b=star[u]-star[v]-slack
   w=Q(R.randint(0,7),R.choice([1,3,11])) if slack==0 else Q(0)
   edges.append((u,v,b,w));a[u]+=w;a[v]-=w
 need(dot(a,star)==sum((w*b for u,v,b,w in edges),Q(0)),'invalid dual certificate')
 big=max([0]+[ceil(b) for u,v,b,w in edges])+R.randrange(5)
 orig=[Q(big+R.randrange(10))+(Q(0) if i in I else Q(R.randrange(4),7)) for i in range(n)]
 z=tuple(orig[i] if i in U else -orig[i] for i in range(n))
 need(all(z[u]-z[v]>=b for u,v,b,w in edges),'constructed mixed point infeasible')
 d=tuple(z[i]-star[i] for i in range(n));layers=decompose(d)
 need(len(layers)<=n,'too many layers')
 need(tuple(sum((lam*r[i] for lam,r in layers),Q(0)) for i in range(n))==d,'layer reconstruction')
 for lam,r in layers:
  need(dot(a,r)>=0,'dual-certified layer has negative cost')
  for i,j in product(range(n),repeat=2):
   gap=d[i]-d[j];step=lam*(r[i]-r[j])
   need(min(0,gap)<=step<=max(0,gap),'difference conformity');tick('signed_difference_controls')
  need(all(star[u]-star[v]+lam*(r[u]-r[v])>=b for u,v,b,w in edges),'forward layer fails')
  tick('dual_certified_layers')
 near=tuple(z[i]-sum(floor(lam)*r[i] for lam,r in layers) for i in range(n))
 need(all(near[u]-near[v]>=b for u,v,b,w in edges),'bulk integral removal infeasible')
 need(all(near[i].denominator==1 for i in I),'bulk removal lost selected integrality')
 need(dot(a,near)<=dot(a,z),'bulk removal increased objective')
 need(max(abs(near[i]-star[i]) for i in range(n))<n,'strict arbitrary-optimum proximity fails')
 tick('arbitrary_lp_optimum_models')
 if scale>1:tick('huge_bit_optimum_models')
# Closed-form partial minimization on K2,2: y_v = min_i(p_i-b_iv).
# This independent route avoids vertex enumeration and checks the oracle on a
# wide exact grid against submodularity and continuous/integer breakpoints.
for trial in range(80):
 den=(1<<127)-1 if trial%10==0 else R.choice([2,3,5,11])
 b=[[Q(R.randint(-15,15),den) for j in range(2)] for i in range(2)]
 w=[[Q(R.randrange(6),R.choice([1,3,7])) for j in range(2)] for i in range(2)]
 alpha=[sum(w[i]) for i in range(2)];beta=[w[0][j]+w[1][j] for j in range(2)]
 def value(p):return dot(alpha,p)-sum(beta[j]*min(p[0]-b[0][j],p[1]-b[1][j]) for j in range(2))
 def completion(p):return tuple(p)+(min(p[0]-b[0][0],p[1]-b[1][0]),min(p[0]-b[0][1],p[1]-b[1][1]))
 breaks=[b[0][j]-b[1][j] for j in range(2)]
 t=min(breaks,key=lambda t:value((t,Q(0))))
 star=completion((t,Q(0)));a=alpha+[-q for q in beta]
 lo=[ceil(star[i]-4) for i in range(2)];hi=[floor(star[i]+4) for i in range(2)]
 grid=list(product(*(range(lo[i],hi[i]+1) for i in range(2))))
 vals={p:value(tuple(map(Q,p))) for p in grid}
 k=lcm(*(x.denominator for row in b for x in row));q=lcm(*(x.denominator for x in a))
 B=max([1]+[ceil(abs(x)) for row in b for x in row]);A=max([1]+[ceil(abs(x)) for x in a]);Hs=ceil(max(map(abs,star)))+4
 for p,v in vals.items():
  need((v*k*q).denominator==1,'oracle denominator bound fails')
  need(abs(v)<=4*A*(Hs+4*B),'oracle magnitude bound fails');tick('analytic_oracle_values')
 for p,z in product(grid,repeat=2):
  meet=tuple(min(x,y) for x,y in zip(p,z));join=tuple(max(x,y) for x,y in zip(p,z))
  need(vals[p]+vals[z]>=vals[meet]+vals[join],'analytic partial oracle is not submodular');tick('analytic_submodular_pairs')
 # With integer left labels, translate p1 to zero; only integer break neighbors
 # can be minimal for this univariate convex piecewise-linear expression.
 candidate={floor(s) for s in breaks}|{ceil(s) for s in breaks}
 exact=min(value((Q(s),Q(0))) for s in candidate)
 need(min(vals.values())==exact,'short-label box misses exact mixed optimum')
 tick('analytic_exact_mixed_optima')
# Integral cone threshold rays and actual finite convex hull interpolation.
for trial in range(160):
 n=R.randint(1,6);split=R.randrange(n+1)
 raw=tuple(Q(R.randint(-5,5),R.choice([1,2,3])) for i in range(n))
 edges=[(u,v) for u in range(split) for v in range(split,n) if raw[u]>=raw[v]]
 layers=decompose(raw)
 need(all(all(ray[u]>=ray[v] for u,v in edges) for lam,ray in layers),'cone layer outside cone')
 # Each fractional layer combines its two neighboring integer multiples.
 mixture={tuple([0]*n):Q(1)}
 for lam,ray in layers:
  m=floor(lam);frac=lam-m;nextmix={}
  for z,weight in mixture.items():
   for step,mass in [(m,1-frac),(m+1,frac)]:
    if not mass:continue
    v=tuple(z[i]+step*ray[i] for i in range(n));nextmix[v]=nextmix.get(v,Q(0))+weight*mass
  mixture=nextmix
 need(sum(mixture.values())==1,'mixture weights')
 need(tuple(sum((weight*z[i] for z,weight in mixture.items()),Q(0)) for i in range(n))==raw,'finite convex interpolation')
 need(all(all(z[u]>=z[v] for u,v in edges) for z in mixture),'integer mixture ray invalid')
 tick('actual_hull_convex_mixtures');tick('integer_mixture_support_points',len(mixture))
# Targeted falsification controls for invalid substitute claims.
need(Q(1,2)<ceil(Q(1,2)),'rounding control')
need(Q(1,3)<1,'continuous endpoint cannot be rounded')
need(min(0,1)+min(1,0)<1,'cover coordinates are not meet closed')
need(not (0-0>=1),'baseline implication indispensable')
need(Q(1,2)-0<1 and Q(1,2)-0>=Q(1,2),'relaxation differs from all-integer hull')
need(Q(3,2)-Q(1,2)==1,'fractional hull boundary')
counts['unsupported_substitution_controls']=6
# The facet-length expression remains a binary-size bound, not magnitude bound.
for n in [1,2,10,100]:
 for kb,hb in [(1,1),(127,511),(1000,2000)]:
  k=(1<<kb)-1;H=(1<<hb)-1;M=factorial(n)*(k*(H+1))**n
  # Conservative signed integer vector encoding: n+1 signs + bit lengths.
  length=(n+1)*(M.bit_length()+2)
  phi=10*(n+1)**2*(1+n.bit_length()+k.bit_length()+(H+1).bit_length())
  need(length<=phi,'facet encoding formula insufficient');tick('facet_binary_bounds')
result={'status':'PASS','seed':23352246,'counts':counts,'scope':'Fresh independent exact Fraction controls; no supplied checker imported. Analytic K2,2 elimination, dual-certified arbitrary/nonvertex LP optima, signed bulk removal, constructive finite recession mixtures and binary length boundaries.','limits':'Bounded corroboration; does not implement general polynomial LP, SFM or GLS and does not establish a universal theorem by enumeration.'}
print(json.dumps(result,indent=2))

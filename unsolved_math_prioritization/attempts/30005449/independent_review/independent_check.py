#!/usr/bin/env python3
"""Independent exact finite checks via discrete-time first-step equations.
No author checker or symbolic algebra is imported. Numerical ODE runs are not used.
"""
from fractions import Fraction as Q
from pathlib import Path
import random,json
rng=random.Random(30005449);counts={}
def ck(name,yes):
 assert yes,name;counts[name]=counts.get(name,0)+1
def solve(A,b):
 A=[[Q(x) for x in r]+[Q(v)] for r,v in zip(A,b)];n=len(A)
 for j in range(n):
  p=next(i for i in range(j,n) if A[i][j]);A[j],A[p]=A[p],A[j];v=A[j][j];A[j]=[x/v for x in A[j]]
  for i in range(n):
   if i!=j:
    v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[j])]
 return [r[-1] for r in A]
def trace(edges,w,N,F,chosen):
 # Independently normalized discrete-time transition equations: success on chosen
 # edge traversal; failure on another transition into F. Edge identities retained.
 verts=sorted(set(sum(([a,b] for a,b in edges),[]))-{F});idx={v:i for i,v in enumerate(verts)};A=[[Q(i==j) for j in range(len(verts))] for i in range(len(verts))];rhs=[Q(0) for _ in verts]
 for u in verts:
  tot=sum(w[j] for j,e in enumerate(edges) if u in e)
  for j,(a,b) in enumerate(edges):
   if u not in (a,b):continue
   v=b if u==a else a;p=w[j]/tot
   if j==chosen:rhs[idx[u]]+=p
   elif v!=F:A[idx[u]][idx[v]]-=p
 return solve(A,rhs)[idx[N]]
def lap(edges,w,F):
 vs=sorted(set(sum(([a,b] for a,b in edges),[]))-{F});ix={a:i for i,a in enumerate(vs)};n=len(vs);L=[[Q(0) for _ in vs] for _ in vs]
 for (a,b),v in zip(edges,w):
  if a!=F:L[ix[a]][ix[a]]+=v
  if b!=F:L[ix[b]][ix[b]]+=v
  if a!=F and b!=F:L[ix[a]][ix[b]]-=v;L[ix[b]][ix[a]]-=v
 G=[[Q(0) for _ in vs] for _ in vs]
 for j in range(n):
  z=solve(L,[Q(i==j) for i in range(n)])
  for i in range(n):G[i][j]=z[i]
 return vs,ix,L,G
def effective_core(edges,w,N,e):
 # Voltage at N fixed to one and at success fixed to zero. Solve interior
 # Kirchhoff equations then measure outgoing root flux, including success legs.
 vs=sorted(set(sum(([a,b] for a,b in edges),[])));others=[x for x in vs if x!=N];ix={x:i for i,x in enumerate(others)};A=[[Q(0) for _ in others] for _ in others];rhs=[Q(0) for _ in others]
 for j,((a,b),v) in enumerate(zip(edges,w)):
  if j==e:
   for u in [a,b]:
    if u!=N:A[ix[u]][ix[u]]+=v
  else:
   for u,z in [(a,b),(b,a)]:
    if u!=N:
     A[ix[u]][ix[u]]+=v
     if z==N:rhs[ix[u]]+=v
     else:A[ix[u]][ix[z]]-=v
 values={N:Q(1)};values.update(zip(others,solve(A,rhs)))
 C=Q(0)
 for j,((a,b),v) in enumerate(zip(edges,w)):
  if j==e:
   if N in (a,b):C+=v
  elif N in (a,b):C+=v*(1-values[b if a==N else a])
 return C
examples=[([(0,1),(1,2)],0,2),([(0,1),(1,2),(1,3)],0,2),([(0,1),(1,2),(2,3)],0,2),([(0,1),(0,1),(1,2),(0,2)],0,2),([(0,1),(1,2),(2,3),(3,0),(0,2),(3,4)],0,4)]
for edges,N,F in examples:
 for rep in range(12):
  w=[Q(rng.randrange(1,8),rng.randrange(1,6)) for _ in edges];vs,ix,L,G=lap(edges,w,F)
  ps=[trace(edges,w,N,F,j) for j in range(len(edges))]
  ck('terminal_partition',sum(p for e,p in zip(edges,ps) if F in e)==1)
  for j,((u,v),weight) in enumerate(zip(edges,w)):
   ck('probability_range',0<=ps[j]<=1)
   ck('homogeneous_trace',trace(edges,[Q(7,3)*z for z in w],N,F,j)==ps[j])
   K=[r[:] for r in L];b=[Q(0) for _ in vs]
   if F in (u,v):b[ix[v if u==F else u]]=weight
   else:K[ix[u]][ix[v]]+=weight;K[ix[v]][ix[u]]+=weight;b[ix[u]]=b[ix[v]]=weight
   ck('killed_edge_formula',solve(K,b)[ix[N]]==ps[j])
   if F not in (u,v):
    a=G[ix[u]][ix[u]];b0=G[ix[v]][ix[v]];c=G[ix[u]][ix[v]];r=G[ix[N]][ix[u]];t=G[ix[N]][ix[v]];den=(1+weight*c)**2-weight**2*a*b0
    ck('Woodbury_positive_denominator',den>0)
    ck('Woodbury_trace',weight*(r*(1+weight*(c-b0))+t*(1+weight*(c-a)))/den==ps[j])
   # Exact rational own-weight concavity and decreasing per-capita controls.
   lo=w[:];hi=w[:];lo[j]/=2;hi[j]*=2
   pl=trace(edges,lo,N,F,j);ph=trace(edges,hi,N,F,j)
   ck('own_weight_monotone',pl<=ps[j]<=ph)
   ck('own_weight_per_capita',pl/lo[j]>=ps[j]/weight>=ph/hi[j])
   mid=w[:];mid[j]=(lo[j]+hi[j])/2
   ck('own_weight_concave',trace(edges,mid,N,F,j)>=(pl+ph)/2)
# Exact tree resistance probabilities at arbitrary branch weights and depths.
for d in range(1,6):
 for depth in range(1,6):
  path=[(i,i+1) for i in range(d)];N=0;F=d
  branch=[(0,d+1)]+[(d+i,d+i+1) for i in range(1,depth)]
  for rep in range(4):
   wbranch=[Q(rng.randrange(1,6),rng.randrange(1,6)) for _ in branch];edges=path+branch;w=[Q(1)]*d+wbranch
   ck('tree_resistance_trace',trace(edges,w,N,F,len(edges)-1)==Q(d)/(Q(d)+sum(1/z for z in wbranch)))
  if d>=2:
   b=Q(d-1,d);vals=[b**k for k in range(1,depth+1)];ck('tree_equilibrium',trace(path+branch,[Q(1)]*d+vals,N,F,len(path+branch)-1)==vals[-1])
# General cyclic cores, including parallel edges; compare actual walk to root capacity.
cores=[[(0,1)],[(0,1),(1,2),(2,0)],[(0,1),(0,1),(1,2),(2,0)],[(0,1),(1,2),(2,3),(3,0),(1,3)],[(0,1),(1,2),(2,0),(2,3)]]
for core in cores:
 V=max(max(e) for e in core)+1
 for d in [2,3,6]:
  path=[(0,V)]+[(V+i,V+i+1) for i in range(d-1)];F=V+d-1
  for rep in range(8):
   w=[Q(rng.randrange(1,7),rng.randrange(1,6)) for _ in core]
   for e in range(len(core)):
    C=effective_core(core,w,0,e);p=trace(core+path,w+[Q(1)]*d,0,F,e)
    ck('core_capacity_positive',C>0)
    ck('core_trace_fraction',p==d*C/(1+d*C))
    ck('core_capacity_homogeneity',effective_core(core,[2*z for z in w],0,e)==2*C)
    increase=w[:];increase[(e+1)%len(core)]+=Q(1,3)
    ck('core_capacity_monotone',effective_core(core,increase,0,e)>=C)
    ck('core_strict_subhomogeneity',d*(2*C)/(1+2*d*C)<2*p)
# Scalar drift, logarithmic contradiction and comparison identities are universal
# algebra; these exact controls calibrate signs and constants at rational inputs.
for d in range(2,12):
 for a in range(d,2*d+4):
  beta=Q(d-1,a)
  ck('scalar_positive_fixed_point',d*beta/(1+a*beta)==beta)
  for x in [beta/2,beta,(beta+1)/2]:
   drift=d*x/(1+a*x)-x
   ck('scalar_drift_sign',(drift>0)==(x<beta) and (drift==0)==(x==beta))
for chi in [Q(1,5),Q(1,2),Q(4,5)]:
 for c in [Q(1,5),Q(1,2),Q(1),Q(2),Q(5)]:
  ck('radial_comparison_identity',(c*chi/(1+(c-1)*chi)-c*chi)/chi==c*(1-c)*chi/(1+(c-1)*chi))
ck('triangle_curl',-Q(1,9)+Q(1,4)==Q(5,36))
# The pendant-at-food-neighbor boundary calibration in the literal positivity clause.
for x in [Q(1,10),Q(1,2),Q(1),Q(3)]:
 ck('accessible_pendant_zero_drift',trace([(0,1),(1,2),(1,3)],[Q(1),Q(1),x],0,2,2)==x/(1+x))
out={'status':'PASS','exact_assertions':sum(counts.values()),'categories':counts,'method':'Independent Fraction Gaussian elimination on normalized discrete-time first-step equations, Kirchhoff root flux, and rational identities','limitations':'Finite exact controls support the separately reviewed analytic and stochastic proofs; no numerical ODE evidence is used as a theorem.'}
Path(__file__).with_name('INDEPENDENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

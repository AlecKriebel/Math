#!/usr/bin/env python3
"""Bounded exact controls for the unresolved AND-layer sensitivity problem.

Truth tables are checked only on small cubes. Larger Hamming examples use the
explicit syndrome quotient proved in OBSTRUCTION.md; no search certifies the
original asymptotic conjecture.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json
checks=Counter()
def req(b,label):
 assert b,label
 checks[label]+=1

def sens(f,n):return [sum(f[x]!=f[x^(1<<k)] for k in range(n)) for x in range(1<<n)]
def ams(fs,n):
 ss=[sens(f,n) for f in fs]
 return F(sum(max(s[x] for s in ss) for x in range(1<<n)),1<<n)
def conjunction(fs,inds):return [int(all(fs[j][x] for j in inds)) for x in range(len(fs[0]))]

# All pairs of Boolean functions on the 2-cube, every conjunction, and each
# pair of outputs: this checks the elementary inequalities, not the conjecture.
n=2;tables=[[(bits>>x)&1 for x in range(4)] for bits in range(16)]
for f,g in product(tables,repeat=2):
 fs=[f,g];ss=[sens(v,n) for v in fs];M=[max(ss[0][x],ss[1][x]) for x in range(4)]
 for subset in ((),(0,),(1,),(0,1)):
  h=conjunction(fs,subset);s=sens(h,n)
  req(sum(s[x] for x in range(4) if h[x]==0)==sum(s[x] for x in range(4) if h[x]==1),'single_cut_edge_balance')
  req(all(h[x] or s[x]<=M[x] for x in range(4)),'zero_side_domination')
  req(all(s[x]<=len(subset)*M[x] for x in range(4)),'fanin_pointwise_bound')
  req(sum(s)<=2*sum(M),'single_output_factor_two')
 req(ams([f,f,g,g],n)==ams(fs,n),'repetitions_preserve_maximum')

# Disjoint k-fold conjunctions. Exact small-cube enumeration checks the formula.
block_cases=[]
for k in range(1,4):
 for m in range(1,5):
  n=k*m;fs=[[(x>>j)&1 for x in range(1<<n)] for j in range(n)]
  gs=[conjunction(fs,tuple(range(i*k,(i+1)*k))) for i in range(m)]
  a=F(1)-F(1,2**k);b=F(1)-F(k+1,2**k)
  predicted=F(k)-F(k-1)*a**m-b**m
  req(ams(fs,n)==1,'coordinate_family_ams')
  req(ams(gs,n)==predicted,'disjoint_block_formula')
  req(ams(gs+[gs[0]]*(n-m),n)==predicted,'output_padding')
  block_cases.append(dict(k=k,m=m,dimension=n,ams=str(predicted)))
# Infinite-family parameters n=k*2^k, with a simple exact lower constant 1/2.
for k in range(1,11):
 m=2**k;a=1-F(1,m)
 req(a**m<=F(1,2),'block_event_probability_lower_half')
 value=F(k)-F(k-1)*a**m-(1-F(k+1,m))**m
 req(F(k,2)<=value<=k,'logarithmic_amplification_bounds')
 req(k<= (k+1)*2**k,'parameter_control')

# Syndrome coloring of the cube: columns are every nonzero vector in F_2^r.
hamming=[]
for r in range(2,8):
 n=2**r-1;colors=range(1,n+1)
 local_total=0;zero_total=0
 for sigma in range(n+1):
  ss=[];zero=[]
  for a in colors:
   v=int(sigma==a);s=sum(v!=int((sigma^col)==a) for col in colors)
   req(s==(n if sigma==a else 1),'syndrome_sensitivity')
   ss.append(s);zero.append(s if not v else 0)
  req(max(zero)==1,'syndrome_zero_side_maximum')
  req(max(ss)==(1 if sigma==0 else n),'syndrome_full_maximum')
  local_total+=max(ss);zero_total+=max(zero)
 A=F(local_total,n+1)
 req(A==F(n*n+1,n+1),'syndrome_ams_formula')
 req(F(zero_total,n+1)==1,'syndrome_zero_side_expectation')
 if r>=3:
  req(2*r<=n,'parity_input_padding_available')
  for b in range(r):
   req(sum((col>>b)&1 for col in colors)==2**(r-1),'parity_factor_sensitivity')
  for sigma,a in product(range(n+1),colors):
   req(all(((sigma>>b)&1)==((a>>b)&1) for b in range(r))==(sigma==a),'parity_factor_conjunction')
  req(A<=2*F(n+1,2),'not_a_low_input_counterexample')
 hamming.append(dict(r=r,dimension=n,outputs=n,ams=str(A),zero_side_ams='1',parity_factor_ams=str(F(n+1,2))))
# Full truth tables for r=2,3: the syndrome quotient agrees with actual flips.
for r in (2,3):
 n=2**r-1
 def sy(x):
  a=0
  for j in range(n):
   if x>>j&1:a^=j+1
  return a
 counts=Counter(sy(x) for x in range(1<<n))
 req(set(counts.values())=={2**(n-r)},'syndrome_uniform_fibers')
 gs=[[int(sy(x)==a) for x in range(1<<n)] for a in range(1,n+1)]
 req(ams(gs,n)==F(n*n+1,n+1),'full_cube_Hamming_ams')
 if r==3:
  fs=[[int(((sy(x)>>b)&1)==e) for x in range(1<<n)] for b in range(r) for e in (0,1)]
  fs+= [fs[0]]*(n-len(fs))
  req(ams(fs,n)==F(n+1,2),'full_cube_parity_input_ams')
  for a in range(1,n+1):req(conjunction(fs,tuple(2*b+((a>>b)&1) for b in range(r)))==gs[a-1],'full_cube_conjunction_realization')

p=Path(__file__).resolve().parent
out=dict(status='PASS',exact_assertions=sum(checks.values()),checks=dict(sorted(checks.items())),
 block_cases=block_cases,hamming_controls=hamming,
 artifact_sha256=hashlib.sha256((p/'OBSTRUCTION.md').read_bytes()).hexdigest(),
 scope='Elementary inequalities, exact small truth tables, and standard syndrome controls. Neither the original AND-layer implication nor its negation is certified.')
print(json.dumps(out,indent=2,sort_keys=True))

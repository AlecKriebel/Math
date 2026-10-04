#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from math import factorial,comb
import json
counts={}
def ck(v,k):
 assert v,k
 counts[k]=counts.get(k,0)+1
def mv(P,v):return tuple(sum((x*y for x,y in zip(row,v)),F(0)) for row in P)
def rank(vectors):
 a=[list(v) for v in vectors];m=len(a)
 if not m:return 0
 r=0
 for col in range(len(a[0])):
  p=next((j for j in range(r,m) if a[j][col]),None)
  if p is None:continue
  a[r],a[p]=a[p],a[r];z=a[r][col];a[r]=[x/z for x in a[r]]
  for j in range(m):
   if j!=r:
    z=a[j][col];a[j]=[x-z*y for x,y in zip(a[j],a[r])]
  r+=1
  if r==m:break
 return r
# Period-two genuinely stochastic hidden chains, not just deterministic cycles.
for a,b in product([F(1,4),F(1,2),F(3,4)],repeat=2):
 P=[(0,0,a,1-a),(0,0,1-a,a),(b,1-b,0,0),(1-b,b,0,0)]
 ck(all(sum(row)==1 for row in P),'stochastic')
 ck(all(sum(row[j] for row in P)==1 for j in range(4)),'stationary_uniform')
 for labels in product(range(2),repeat=4):
  matrices={c:[tuple(x if labels[i]==c else 0 for x in row) for i,row in enumerate(P)] for c in (0,1)}
  cols={():tuple([F(1)]*4)}
  for n in range(1,7):
   for w in product(range(2),repeat=n):cols[w]=mv(matrices[w[0]],cols[w[1:]])
  short=[v for w,v in cols.items() if len(w)<=3];R=rank(short)
  ck(rank(list(cols.values()))==R,'word_span_stabilization')
  for M in matrices.values():ck(rank(short+[mv(M,v) for v in short])==R,'word_span_invariance')
  delta=(F(1,2),F(1,2),F(-1,2),F(-1,2))
  eq=lambda v:sum(x*y for x,y in zip(delta,v))==0
  ck(all(map(eq,short))==all(map(eq,cols.values())),'phase_observability_quotient')
  for w in product(range(2),repeat=3):
   direct=[F(0)]*4
   for path in product(range(4),repeat=3):
    if tuple(labels[i] for i in path)==w:direct[path[0]]+=P[path[0]][path[1]]*P[path[1]][path[2]]
   ck(tuple(direct)==cols[w],'direct_hidden_path_sum')
# General beta prior controls include the author's uniform case.
B=lambda a,b:F(factorial(a-1)*factorial(b-1),factorial(a+b-1))
for a,b in product(range(1,5),repeat=2):
 for N in range(1,19):
  total=F(0);mean=F(0);var=F(0)
  for k in range(N+1):
   pk=comb(N,k)*B(k+a,N-k+b)/B(a,b);total+=pk;mean+=pk*F(k+a,N+a+b)
   ck(B(k+a+1,N-k+b)/B(k+a,N-k+b)==F(k+a,N+a+b),'beta_posterior')
  ck(total==1 and mean==F(a,a+b),'beta_mixture_moments')
  # Conditional independence yields difference variance2N E[p(1-p)].
  defect=F(2*N,(N+a+b)**2)*B(a+1,b+1)/B(a,b)
  ck(defect==F(2*N*a*b,(a+b)*(a+b+1)*(N+a+b)**2),'beta_two_block_defect')
  if a==b==1:ck(defect==F(N,3*(N+2)**2),'uniform_beta_specialization')
# Exhaust finite forcing-uniform patterns against disjoint-block run bound.
for eps in [F(1,3),F(2,3)]:
 for n in range(1,11):
  for ell in range(1,n+1):
   miss=F(0)
   for w in product(range(2),repeat=n):
    if not any(all(w[j:j+ell]) for j in range(n-ell+1)):
     miss+=eps**sum(w)*(1-eps)**(n-sum(w))
   ck(miss<=(1-eps**ell)**(n//ell),'forced_run_probability')
# Decisiveness checked by grouping all completions of observed prefixes.
words=list(product(range(2),repeat=9))
def output(w):
 L=next((i for i in range(3) if w[i]),3)
 return w[2**L],2**L
tables={}
for radius in range(9):
 for w in words:tables.setdefault((radius,w[:radius+1]),set()).add(output(w)[0])
for w in words:
 y,R=output(w)
 least=next(r for r in range(9) if len(tables[r,w[:r+1]])==1)
 ck(least==R,'decisive_radius_exact')
 for r in range(R,9):ck(tables[r,w[:r+1]]=={y},'decisive_block_consistency')
for cutoff in range(1,21):
 law={2**j:F(1,2**(j+1)) for j in range(cutoff)};law[2**cutoff]=F(1,2**cutoff)
 ck(sum(x*p for x,p in law.items())==F(cutoff,2)+1,'infinite_mean_truncations')
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'by_family':counts,'scope':'Independent exact hidden-path/word-space, beta-mixture, forcing-block and decisive-code controls. Infinite tail arguments were audited separately.'},indent=2,sort_keys=True))

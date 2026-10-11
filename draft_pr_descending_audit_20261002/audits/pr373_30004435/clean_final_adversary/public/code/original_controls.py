#!/usr/bin/env python3
"""Independent exact controls written before reading candidate mathematics."""
from fractions import Fraction as F
from itertools import product
import json

def matmul(a,b):
 return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def wordlaw(P,pi,emit,w):
 v=list(pi)
 for idx,a in enumerate(w):
  v=[x*F(emit[i]==a) for i,x in enumerate(v)]
  if idx+1<len(w): v=matmul([v],P)[0]
 return sum(v)
def cycle(n): return [[F(j==(i+1)%n) for j in range(n)] for i in range(n)]
def phase_signatures(P,emit,maxlen):
 n=len(P);words=[w for k in range(1,maxlen+1) for w in product(sorted(set(emit)),repeat=k)]
 return [[str(wordlaw(P,[F(i==j) for j in range(n)],emit,w)) for w in words] for i in range(n)]
def quotient(sig):
 return [[j for j,s in enumerate(sig) if s==sig[i]] for i in range(len(sig)) if not any(sig[i]==s for s in sig[:i])]

r={}
r['hidden_period_two_constant_observation']=quotient(phase_signatures(cycle(2),[0,0],3));assert r['hidden_period_two_constant_observation']==[[0,1]]
r['four_cycle_0011_wordlength_one']=quotient(phase_signatures(cycle(4),[0,0,1,1],1));assert r['four_cycle_0011_wordlength_one']==[[0,1],[2,3]]
r['four_cycle_0011_wordlength_two']=quotient(phase_signatures(cycle(4),[0,0,1,1],2));assert r['four_cycle_0011_wordlength_two']==[[0],[1],[2],[3]]
r['alternation_tail_phase']=quotient(phase_signatures(cycle(2),[0,1],2));assert r['alternation_tail_phase']==[[0],[1]]
r['symmetric_markov_weak_limit']=[{'epsilon':str(e),'fixed_10_block_no_flip_probability':str((1-e)**9),'tail_for_each_positive_epsilon':'trivial','tail_at_zero':'constant_bit'} for e in [F(1,2),F(1,10),F(1,100),F(1,1000)]]
# Independent reset chain from zero: q(k)=1/(4*2**k).
dist={0:F(1)};stream=[]
for t in range(21):
 stream.append({'time':t,'reset_mass':str(dist.get(0,F(0)))})
 new={}
 for k,p in dist.items():
  q=F(1,4*2**k);new[0]=new.get(0,F(0))+p*q;new[k+1]=new.get(k+1,F(0))+p*(1-q)
 dist=new
r['reset_chain_exact_stream']=stream
r['summable_influence_union_bound']=[{'n':n,'bound_for_geometric_radius_P_R_ge_k_2_minus_k':str(F(2,2**n))} for n in [1,2,4,8,16]]
r['status']='PASS; finite exact controls only; no general tail theorem asserted'
print(json.dumps(r,indent=2,sort_keys=True))

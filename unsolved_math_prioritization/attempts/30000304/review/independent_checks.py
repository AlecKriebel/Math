#!/usr/bin/env python3
"""Independent active/frozen-size CTMC and symbolic controls. No author-code import."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from collections import defaultdict,Counter
from math import comb,factorial,prod
from pathlib import Path
import json,sympy as sp
N=0;families={}
def ck(v,f):
 global N
 assert v,f
 N+=1;families[f]=families.get(f,0)+1

def mult(shape):
 return factorial(sum(shape))//(prod(factorial(i) for i in shape)*prod(factorial(i) for i in Counter(shape).values()))

class FreezeCTMC:
 def __init__(self,atoms,r,king=0):
  self.atoms=tuple((F(rate),tuple(map(F,x))) for rate,x in atoms);self.r=F(r);self.king=F(king)
 @lru_cache(None)
 def mergers(self,active):
  k=len(active);out=defaultdict(F)
  for rate,x in self.atoms:
   prob=(1-sum(x),)+x
   usable=[i for i,p in enumerate(prob) if p]
   for colors in product(usable,repeat=k):
    groups=defaultdict(int);dust=[]
    for sz,c in zip(active,colors):
     if c:groups[c]+=sz
     else:dust.append(sz)
    new=tuple(sorted(dust+list(groups.values())))
    if len(new)<k:out[new]+=rate*prod(prob[c] for c in colors)
  if self.king:
   for i in range(k):
    for j in range(i):
     new=tuple(sorted([s for h,s in enumerate(active) if h not in (i,j)]+[active[i]+active[j]]))
     out[new]+=self.king
  return dict(out)
 @lru_cache(None)
 def terminal(self,active,frozen=()):
  if not active:return {frozen:F(1)}
  mergers=self.mergers(active);den=len(active)*self.r+sum(mergers.values(),F(0));out=defaultdict(F)
  for i,s in enumerate(active):
   a=active[:i]+active[i+1:];f=tuple(sorted(frozen+(s,)))
   for sh,p in self.terminal(a,f).items():out[sh]+=self.r*p/den
  for a,rate in mergers.items():
   for sh,p in self.terminal(a,frozen).items():out[sh]+=rate*p/den
  return dict(out)
 def law(self,n):return self.terminal((1,)*n)
 def g(self,n):return sum(self.mergers((1,)*n).values(),F(0))
 def phi(self,n):
  out=[F(0),F(1)]
  for k in range(2,n+1):out.append(out[-1]*(self.g(k)+k*self.r)/(self.g(k)+(k-1)*self.r))
  return out
 def q(self,n,m):
  ph=self.phi(n)
  return F(comb(n,m))*sum((F((-1)**(j+1)*comb(m,j))*ph[n-m+j] for j in range(m+1)),F(0))/ph[n]

def compositions(n):
 if n==0:yield ();return
 for j in range(1,n+1):
  for rest in compositions(n-j):yield (j,)+rest

def regen_shapes(M,n):
 out=defaultdict(F)
 for c in compositions(n):
  k=n;p=F(1)
  for j in c:p*=M.q(k,j);k-=j
  out[tuple(sorted(c))]+=p
 return dict(out)

# Independent symbolic derivation without finite paintbox substitution.
a,b,c,d,r=sp.symbols('a b c d r')
g=[0,0,a,3*a-2*b,6*a-8*b+3*c-3*d]
phi=[sp.S(0),sp.S(1)]
for n in range(2,5):phi.append(phi[-1]*(g[n]+n*r)/(g[n]+(n-1)*r))
P2=a/(a+2*r);P3=(3*(a-b)*P2+b)/(g[3]+3*r)
P4=(6*(a-2*b+c-d)*P3+(4*(b-c)+3*d)*P2+c)/(g[4]+4*r)
reg4=(4-6*phi[2]+4*phi[3]-phi[4])/phi[4]
defect=2*r*(3*d*(a+r)-2*b*(a-2*b+c))/((a+2*r)*(3*a-2*b+3*r)*(g[4]+4*r))
ck(sp.factor(P4-reg4-defect)==0,'symbolic_four_sample_identity')
ck(sp.factor((2-phi[2])/phi[2]-P2)==0,'automatic_two_sample_match')
ck(sp.factor((3-3*phi[2]+phi[3])/phi[3]-P3)==0,'automatic_three_sample_match')
for n in range(2,5):ck(sp.factor(n*(phi[n]-phi[n-1])/phi[n]-n*r/(g[n]+n*r))==0,'singleton_decrement_identity')

models=[
 FreezeCTMC([(10,(F(1,2),)),(1,(F(1,2),F(1,2)))],3),
 FreezeCTMC([(2,(F(1,3),))],F(1,2),F(2,5)),
 FreezeCTMC([(3,(F(1,4),F(3,4)))],2),
 FreezeCTMC([(10,(1,)),(1,(F(1,3),)*3)],F(85,27)),
 FreezeCTMC([],F(3,2),1),
 FreezeCTMC([(2,(1,))],F(7,10)),
 FreezeCTMC([],1)]
for M in models:
 for n in range(1,7):
  law=M.law(n);ck(sum(law.values(),F(0))==1,'full_state_normalization')
  ck(all(p>=0 for p in law.values()),'full_state_positivity')
  if n>1:
   ck(law.get((1,)*n,0)/M.law(n-1).get((1,)*(n-1),0)==n*M.r/(M.g(n)+n*M.r),'full_state_singleton_recursion')
  # Direct sampling consistency of shape laws via deletion of a uniform individual.
  if n>1:
   reduced=defaultdict(F)
   for shape,p in law.items():
    for i,s in enumerate(shape):
     shrunk=list(shape);shrunk[i]-=1;sh=tuple(sorted(x for x in shrunk if x))
     reduced[sh]+=p*F(s,n)
   prev=M.law(n-1)
   for sh in reduced.keys()|prev.keys():ck(reduced.get(sh,0)==prev.get(sh,0),'full_state_sampling_consistency')

W=models[0]
for n,p in [(2,F(1,3)),(3,F(1,5)),(4,F(7,53)),(5,F(2857,30687))]:ck(W.law(n).get((n,),0)==p,'five_sample_witness')
ck(W.q(5,5)==F(934,10229),'five_sample_witness')
ck(W.law(5)[(5,)]-W.q(5,5)==F(55,30687),'five_sample_witness')
for n in range(1,5):
 reg=regen_shapes(W,n);law=W.law(n)
 for sh in reg.keys()|law.keys():ck(reg.get(sh,0)==law.get(sh,0),'all_shapes_through_four')

# Explicit Ewens distribution with theta=2r/king and unordered multiplicities.
K=models[4];theta=2*K.r/K.king
for n in range(1,7):
 denom=prod(theta+j for j in range(n))
 for sh,p in K.law(n).items():
  expected=mult(sh)*theta**len(sh)*prod(factorial(s-1) for s in sh)/denom
  ck(p==expected,'independent_ewens_control')
  ck(regen_shapes(K,n).get(sh,0)==p,'kingman_regeneration_control')

# Star formula from V~Beta(K/r,1), with dust; this does not use recursion Phi.
S=models[5];eta=F(2)/S.r
def beta_moment(m,s):return eta*factorial(s)/prod(eta+m+j for j in range(s+1))
for n in range(2,7):
 for sh,p in S.law(n).items():
  large=[x for x in sh if x>=2]
  if not large:expected=beta_moment(0,n)+n*beta_moment(1,n-1)
  elif len(large)==1:
   m=large[0];expected=comb(n,m)*beta_moment(m,n-m)
  else:expected=0
  ck(p==expected,'independent_star_paintbox_control')
  ck(regen_shapes(S,n).get(sh,0)==p,'star_regeneration_control')

# Full replacement bounds repeated alleles in all finite laws checked.
for M,bound in [(models[2],2),(models[3],3)]:
 for n in range(2,2*bound+3):
  law=M.law(n)
  ck(all(sum(s>1 for s in sh)<=bound for sh,p in law.items() if p),'bounded_parent_support')
 ck(M.law(4).get((2,2),0)>0,'bounded_parent_two_positive_blocks')
 ck(M.law(2*bound+2).get((2,)*(bound+1),0)==0,'bounded_parent_forbidden_shape')
ck(models[3].law(4)[(4,)]==models[3].q(4,4),'bounded_parent_passing_four_sample')

# Positive internal Levy atoms give every even two-step decrement positive,
# including drift and killing; a direct integral/binomial formula control.
for delta,kill,rate,x in product((F(0),F(2)),(F(0),F(3)),(F(1),F(5)),(F(1,5),F(1,2),F(4,5))):
 product_probability=F(1)
 for j in range(1,9):
  n=2*j;Phi=delta*n+kill+rate*(1-(1-x)**n)
  numerator=comb(n,2)*rate*x*x*(1-x)**(n-2)+(kill if n==2 else 0)
  q=numerator/Phi
  ck(q>0,'internal_levy_even_decrements')
  product_probability*=q
 ck(product_probability>0,'arbitrary_bound_regeneration_control')

result={'problem_id':30000304,'status':'PASS','independent_assertions':N,'families':families,
 'method':'Symbolic identity and independently implemented active/frozen-size CTMC; no author-code import',
 'five_sample_true':str(W.law(5)[(5,)]),'five_sample_regenerative':str(W.q(5,5)),
 'five_sample_difference':str(W.law(5)[(5,)]-W.q(5,5)),
 'scope':'Finite diagnostics support, but do not replace, the written all-sample bounded-parent proof.'}
root=Path(__file__).resolve().parent;(root/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

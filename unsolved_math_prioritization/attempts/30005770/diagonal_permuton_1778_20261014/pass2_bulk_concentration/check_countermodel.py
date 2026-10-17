#!/usr/bin/env python3
"""Finite exact regression tests for the abstract completion-bound countermodel.
The accompanying proof supplies the all-size claims; this script does not.
"""
from math import comb,factorial
from fractions import Fraction
from collections import defaultdict
from pathlib import Path
import hashlib,json,sys
P=Path(__file__).resolve().parent
T=80
LM=64

def require(c,m):
 if not c:raise RuntimeError(m)
def B(L,t):
 if L==0:return int(t==0)
 x=L*comb(L+2*t,t)
 require(x%(L+2*t)==0,'ballot integrality')
 return x//(L+2*t)
def A(L,t):
 return sum(3**s*B(L+s-3,t-s) for s in range(t+1))
def children(kind,L):
 if kind=='P0':return [('P1',2)]
 if kind=='P1':return [('P2',3)]*2
 if kind=='P2':return [('A',4)]*3
 if kind=='A':return [('A',L+1)]*3+[('B',j) for j in range(2,L-1)]
 if kind=='B':return [('B',j) for j in range(2,L+2)]
 raise RuntimeError('bad kind')
def D(kind,L,t):
 if kind=='P0':return a[t]
 if kind=='P1':return [1,2][t] if t<2 else 6*d[t-2]
 if kind=='P2':return 1 if t==0 else 3*d[t-1]
 if kind=='A':return A(L,t)
 if kind=='B':return B(L,t)
 raise RuntimeError('bad kind')
d=[A(4,t) for t in range(T+3)]
a=[1,1,2]+[6*d[t-3] for t in range(3,T+3)]
# A recurrence versus independent spine/forest summation.
recurrence_checks=0
for L in range(4,LM+2):
 for t in range(T):
  require(A(L,t+1)==3*A(L+1,t)+sum(B(j,t) for j in range(2,L-1)),'A recurrence')
  recurrence_checks+=1
# Positive Jacobi return sequence, independently multiplied.
v=[0]*(T+3);v[0]=1
for t in range(T+1):
 require(v[0]==d[t],'Jacobi moments versus tree')
 w=[0]*len(v)
 for i,x in enumerate(v):
  w[i]+=(4 if i==0 else 2)*x
  if i:w[i-1]+=x
  if i+1<len(v):w[i+1]+=x
 v=w
for t in range(1,T+1):
 require(d[t]**2<=d[t-1]*d[t+1],'d log convexity')
 require(a[t]**2<=a[t-1]*a[t+1],'a log convexity')
for n in range(T+1):
 require(a[n]<=factorial(n),'factorial degree upper')
 require(a[n]>=B(1,n),'Catalan lower')
 for k in range(n+1):require(a[k]*a[n-k]<=a[n],'supermultiplicativity')
# All node types, labels, bounded descendant depths.
upper_checks=0
for kind,labels in [('P0',[1]),('P1',[2]),('P2',[3]),('A',range(4,LM+1)),('B',range(2,LM+1))]:
 for L in labels:
  ch=children(kind,L)
  require(len(ch)==L,'degree')
  labs=sorted(k for _,k in ch)
  require(max(labs)<=L+1,'child upper')
  require(all(k>=j+1 for j,k in enumerate(labs,1)),'Catalan sorted domination')
  for t in range(T+1):
   count=D(kind,L,t)
   require(B(L,t)<=count,'Catalan descendants')
   require(count<=comb(L+t-1,t)*a[t],'binomial completion upper')
   upper_checks+=1
# Finite level histograms independently propagated through the actual rules.
hists=[{('P0',1):1}]
for n in range(40):
 nxt=defaultdict(int)
 for (kind,L),count in hists[-1].items():
  for child in children(kind,L):nxt[child]+=count
 hists.append(dict(nxt))
for n,h in enumerate(hists):require(sum(h.values())==a[n],'root generating counts')
weighted_checks=0
for n in range(41):
 for j in range(n+1):
  total=sum(count*D(kind,L,n-j) for (kind,L),count in hists[j].items())
  require(total==a[n],'exact descendant-weighted ancestor law')
  weighted_checks+=1
# Marked law: exact first-A-spine distribution versus continuation tails.
spine=[]
for n in [20,50,100,200,400]:
 t=n-3
 weights=[3**s*B(s+1,t-s) for s in range(t+1)]
 den=sum(weights)
 require(den==A(4,t),'marked total')
 mean=sum(Fraction(s*w,den) for s,w in enumerate(weights))
 second=sum(Fraction(s*s*w,den) for s,w in enumerate(weights))
 var=second-mean*mean
 j=n//4;r=j-3
 left=sum(weights[max(0,r):])
 right=3**r*A(j+1,n-j) if r>=0 else den
 require(left==right,'marked tail equals ancestor completions')
 spine.append({'n':n,'mean_over_n':float(mean/n),'variance_over_n':float(var/n),'prob_A_ancestor_at_floor_n_over_4':str(Fraction(left,den))})
# Repair boundary: original model had a3=5 and D3(A3)=51.
require(A(3,3)==51,'old-model witness numerator')
require(comb(5,3)*5==50,'old-model witness bound')
require(a[5]==102 and a[4]==24,'not a principal avoidance count sequence')
report={'status':'PASS','scope':'Finite exact tests only; all-size proofs are in the authored note. This is not a permutation counterexample.','python_optimization_level':sys.flags.optimize,'bounds':{'descendant_depth':T,'labels':LM,'level_histograms':'0 through 40','marked_spine_sizes':[20,50,100,200,400]},'checks':{'A_recurrences':recurrence_checks,'node_completion_bounds':upper_checks,'weighted_ancestor_identities':weighted_checks},'root_counts_n0_to_n10':a[:11],'marked_spine_regression':spine,'proof_sha256':hashlib.sha256((P/'COMPLETION_BOUND_COUNTERMODEL.md').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(report,indent=2,sort_keys=True))

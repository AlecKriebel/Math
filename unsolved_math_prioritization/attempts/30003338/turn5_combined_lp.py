# Numerical LP is a witness-finding device only; any retained witness is verified rationally.
from itertools import product
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
import json
n=4;q=3
partitions=set()
for c in product(range(q),repeat=n):
 blocks=tuple(sorted(sum(1<<i for i in range(n) if c[i]==v) for v in set(c)))
 partitions.add(blocks)
P=sorted(partitions)
def up(n):
 if n==0:return[0,1]
 a=up(n-1);return[x|(y<<(1<<(n-1))) for x in a for y in a if x&y==x]
U=up(4);count=np.zeros((len(P),16),dtype=int)
for j,p in enumerate(P):
 count[j,0]=q-len(p)
 for S in p:count[j,S]+=1
C=[]
for i in range(n):
 for E in U:
  total=np.array([sum(row[S] for S in range(16) if E>>S&1) for row in count])
  both=np.array([sum(row[S] for S in range(16) if E>>S&1 and S>>i&1) for row in count])
  C.append(q*both-total)
# Add the universally necessary Kempe partition-coarsening count inequalities.
from math import factorial
for i,pi in enumerate(P):
 for j,pj in enumerate(P):
  if i==j:continue
  if all(any((block&coarse)==block for coarse in pj) for block in pi):
   row=np.zeros(len(P),dtype=int)
   den_i=factorial(q)//factorial(q-len(pi));den_j=factorial(q)//factorial(q-len(pj))
   row[j]=den_i;row[i]=-den_j;C.append(row)
C=np.array(C)
A=np.array([sum(row[S] for S in range(16) if S&3==3) for row in count]);B=np.array([sum(row[S] for S in range(16) if S&12==12) for row in count]);J=count[:,15]
for r in [F(i,90) for i in range(10,31)]:
 for s in [F(i,90) for i in range(10,31)]:
  result=linprog(J.astype(float),A_ub=-C,b_ub=np.zeros(len(C)),A_eq=np.array([np.ones(len(P)),A,B]),b_eq=[1,float(q*r),float(q*s)],bounds=(0,None),method='highs')
  if result.success and result.fun/q<float(r*s)-1e-10:
   weights=[F(float(x)).limit_denominator(10000000) for x in result.x]
   def dot(v):return sum(w*int(c) for w,c in zip(weights,v))
   ok=sum(weights)==1 and min(weights)>=0 and min(dot(row) for row in C)>=0 and dot(J)/q<(dot(A)/q)*(dot(B)/q)
   print(json.dumps({'status':'ABSTRACT_REGRESSION_AND_COARSENING_COUNTEREXAMPLE_CANDIDATE','exact_verified':ok,'q':q,'partitions':P,'partition_probabilities':[str(w) for w in weights],'P_F':str(dot(A)/q),'P_G':str(dot(B)/q),'P_FG':str(dot(J)/q),'covariance':str(dot(J)/q-(dot(A)/q)*(dot(B)/q)),'minimum_regression_numerator':str(min(dot(row) for row in C)),'scope':'Abstract color-symmetric law satisfying singleton regression and partition-coarsening dominance; graph realizability is not established.'},indent=2));raise SystemExit
print(json.dumps({'status':'NO_COMBINED_ABSTRACT_WITNESS_ON_GRID','q':q,'LP_cases':441}))

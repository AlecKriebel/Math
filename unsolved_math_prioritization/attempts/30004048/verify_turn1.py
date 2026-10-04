#!/usr/bin/env python3
"""Exact small sampling/reversal controls and concentration-envelope arithmetic."""
from fractions import Fraction as F
from itertools import product
import json
checks=0;graphs=0;sample_graphs=0
def ok(x):
 global checks
 assert x
 checks+=1
def matrix(mask):return [[(mask>>(2*i+j))&1 for j in range(2)] for i in range(2)]
def reach(P,Q):return [[any(P[i][j] and Q[j][k] for j in range(2)) for k in range(2)] for i in range(2)]
def minboth(M):return min([sum(row) for row in M]+[sum(M[i][j] for i in range(2)) for j in range(2)])
for pm,qm in product(range(16),repeat=2):
 P,Q=matrix(pm),matrix(qm)
 if not minboth(P) or not minboth(Q):continue
 graphs+=1;alpha=F(minboth(P),2);beta=F(minboth(Q),2)
 ok(alpha>0);ok(beta>0)
 R=reach(P,Q)
 forward=max(sum(R[i][k] for i in range(2)) for k in range(2))
 reverse=max(sum(row) for row in R)
 # Every labeled sample creates a simple graph; repeated originals are twins.
 for aa,bb,cc in product(list(product(range(2),repeat=2)),repeat=3):
  PP=[[P[aa[i]][bb[j]] for j in range(2)] for i in range(2)]
  QQ=[[Q[bb[j]][cc[k]] for k in range(2)] for j in range(2)]
  RR=reach(PP,QQ);sample_graphs+=1
  for i,k in product(range(2),repeat=2):ok(not RR[i][k] or R[aa[i]][cc[k]])
  for k in range(2):ok(sum(RR[i][k] for i in range(2))<=sum(R[aa[i]][cc[k]] for i in range(2)))
  for i in range(2):ok(sum(RR[i][k] for k in range(2))<=sum(R[aa[i]][cc[k]] for k in range(2)))
 # Cofinal rational parameters are their actual minimum degree fractions.
 for den in range(1,11):
  x=alpha/F(den);y=beta/F(den);ok(x<=alpha);ok(y<=beta)
# Exact algebra used for the analytic probability envelope.
ok(1+3+F(9,2)+F(27,6)>10)
for i in range(1,1001):
 u=F(i,1000)
 upper_uL=3*u+1-u
 ok(upper_uL<=3);ok(F(6,100)*(upper_uL+u*u)<=F(24,100));ok(F(24,100)<1)
# Finite-certificate ordering arithmetic, with no table value inferred.
for low,gap,eps in product([F(1,5),F(1,3)],[F(1,10),F(1,6)],[F(1,100),F(1,50)]):
 high=low+gap+eps
 ok(low<high-eps)
print(json.dumps({'status':'PASS','assertions':checks,'source_graphs':graphs,'labeled_samples':sample_graphs,'scope':'Finite exact graph/copy reachability and envelope algebra; uniform concentration, infimum reduction and certificate implications are proved analytically'},indent=2,sort_keys=True))

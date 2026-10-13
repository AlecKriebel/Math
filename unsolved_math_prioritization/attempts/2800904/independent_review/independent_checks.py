#!/usr/bin/env python3
"""Independent exact metric, assignment-spectrum and dual-certificate controls."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations,product
import json
C=Counter()
def check(p,k):
 assert p,k
 C[k]+=1
D=[
[0,1050,1998,1954,1006,1934,1966,1063],
[1050,0,1052,1939,1962,1046,1975,1928],
[1998,1052,0,1065,1918,1937,1018,1997],
[1954,1939,1065,0,1013,1980,1933,1069],
[1006,1962,1918,1013,0,1091,1978,1919],
[1934,1046,1937,1980,1091,0,1040,1913],
[1966,1975,1018,1933,1978,1040,0,1094],
[1063,1928,1997,1069,1919,1913,1094,0]]
for i,j in product(range(8),repeat=2):
 check(D[i][j]==D[j][i],'symmetric_distance')
 check((D[i][j]==0)==(i==j),'metric_separation')
for i,j,k in product(range(8),repeat=3):check(D[i][k]<=D[i][j]+D[j][k],'triangle_inequality')
# Cost-generating polynomials independently count every assignment without importing
# or repeating the submitted assignment enumeration.
spectrum=Counter();centers=[]
for a,b in combinations(range(8),2):
 p=Counter({0:1})
 for j in range(8):
  nxt=Counter()
  for degree,coefficient in p.items():
   nxt[degree+D[a][j]]+=coefficient;nxt[degree+D[b][j]]+=coefficient
  p=nxt
  check(sum(p.values())==2**(j+1),'generating_polynomial_assignment_count')
 check(sum(p.values())==256,'center_pair_assignment_count')
 centers.append((min(p),a,b));spectrum.update(p)
check(sum(spectrum.values())==7168,'all_assignment_count')
keys=sorted(spectrum)
check(keys[0]==7099 and spectrum[7099]==1,'unique_minimum')
check(keys[1]==7110,'distinct_runner_up')
check(min(centers)==(7099,2,4),'optimal_centers')
assign=tuple(min((2,4),key=lambda i:D[i][j]) for j in range(8))
check(assign==(4,2,2,4,4,4,2,4),'optimal_assignment')
alpha=F(1001,1000)
for cost in keys[1:]:check(cost-alpha*7099>0,'universal_perturbation_cost_margin')
check(F(7110)-alpha*7099==F(3901,1000),'strict_resilience_margin')
# Adjacency defined by cyclic separation 1 or 4, independently of edge listing.
x=[[F(int(i==j or (i-j)%8 in (1,4,7)),4) for j in range(8)] for i in range(8)]
for j in range(8):check(sum(x[i][j] for i in range(8))==1,'fractional_column_sum')
for i,j in product(range(8),repeat=2):check(0<=x[i][j]<=F(1,4),'fractional_facility_bound')
cost=sum(x[i][j]*D[i][j] for i,j in product(range(8),repeat=2))
check(cost==F(12607,2),'fractional_objective')
check(F(7099)-cost==F(1591,2),'strict_integrality_gap')
opts={}
for k in (1,2,3):
 opts[k]=min(sum(min(D[c][j] for c in s) for j in range(8)) for s in combinations(range(8),k))
check(opts=={1:10887,2:7099,3:5171},'three_integer_objectives')
# Robust dual certificate on the independently reconstructed line metric.
pos=(0,1,2,100,101,102);base=[[F(abs(a-b)) for b in pos] for a in pos]
S=(1,4);owner=(1,1,1,4,4,4);t=F(3);eps=F(1,100)
def certify(d):
 a=[d[owner[j]][j]+1 for j in range(6)]
 b=[[max(a[j]-d[i][j],0) for j in range(6)] for i in range(6)]
 gamma=min(d[i][j]-a[j] for i in S for j in range(6) if i!=owner[j])
 eta=min(t-sum(b[i]) for i in range(6) if i not in S)
 for i,j in product(range(6),repeat=2):check(a[j]-b[i][j]<=d[i][j],'dual_pointwise_feasibility')
 for i in S:check(sum(b[i])==t,'selected_dual_sum')
 for i in range(6):check(sum(b[i])<=t,'all_dual_sums')
 check(sum(a)-2*t==sum(d[owner[j]][j] for j in range(6)),'dual_attains_integral_cost')
 check(gamma>0 and eta>0,'strict_dual_margins')
 return gamma,eta
check(certify(base)==(F(97),F(1)),'base_certificate_margins')
check(2*eps<97 and 12*eps<1,'uniform_robustness_hypotheses')
# Every single-entry cost direction, including nonmetrics and negative diagonals,
# is permitted by the cost-matrix version of the certificate.
for i,j in product(range(6),repeat=2):
 for sign in (-1,1):
  pert=[row[:] for row in base];pert[i][j]+=sign*eps
  gamma,eta=certify(pert)
  check(gamma>=97-2*eps and eta>=1-12*eps,'predicted_margin_bounds')
# Finite positive control unique among every integer center/assignment solution.
minimum=10**9;mult=0
for s in combinations(range(6),2):
 for labels in product(s,repeat=6):
  v=sum(base[labels[j]][j] for j in range(6))
  if v<minimum:minimum,mult=v,1
  elif v==minimum:mult+=1
check((minimum,mult)==(4,1),'certificate_integral_uniqueness')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'checks':dict(sorted(C.items())),
 'integer_assignment_solutions':7168,'integer_cost':7099,'runner_up':7110,'fractional_feasible_cost':str(cost),
 'uniform_resilience_margin':str(F(7110)-alpha*7099),'source_scope':'Finite metric k-median partial only; no Euclidean realization, strong-threshold theorem or k-means SDP claim.'},indent=2,sort_keys=True))

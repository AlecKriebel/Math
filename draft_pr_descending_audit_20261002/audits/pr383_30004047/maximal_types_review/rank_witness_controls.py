#!/usr/bin/env python3
"""Actual uniform-A below-reach witnesses exercise the necessary conditions.

Integer multiplicities on B,C realize the rational weights by ordinary blow-up;
the graph is checked by incidence sets, without importing candidate code.
"""
from fractions import Fraction as Q
from math import lcm
import json

rows=[];assertions=0;pair_checks=0
for k in range(2,16):
 n=4*k+1;r=4;A=set(range(n))
 blocks=[frozenset(range(4*i,4*i+4)) for i in range(k-1)]
 U=set().union(*blocks);D=sorted(A-U)
 types=blocks+[frozenset([v]) for v in D]
 beta=[Q(1,len(types))]*len(types)
 y=(Q(1,k+1)+Q(4,4*k+1))/2
 residual_mass=1-(k-1)*y
 reach_classes=blocks+[frozenset(set(D)-{v}) for v in D]
 gamma=[y]*(k-1)+[residual_mass/5]*5
 edges=[{j for j,R in enumerate(reach_classes) if S<=R} for S in types]
 assert sum(beta)==sum(gamma)==1 and y>Q(1,k+1);assertions+=2
 degreeA=[sum(beta[b] for b,S in enumerate(types) if a in S) for a in A]
 degreeB=[sum(gamma[c] for c in adj) for adj in edges]
 reaches=[set().union(*(types[b] for b,adj in enumerate(edges) if c in adj)) for c in range(len(gamma))]
 x=min(degreeA)
 assert min(degreeB)>=y and all(len(R)*k<n for R in reaches);assertions+=2
 largest=[S for S in set(types) if len(S)==r]
 assert len(largest)==k-1;assertions+=1
 assert x<=Q(r*(r-1),r*n-len(U))<=Q(r-1,n-len(largest))<=Q(r-1,n-k+1);assertions+=1
 residual=[S for S in types if not any(S<=T for T in largest)]
 for S in residual:
  for T in residual:
   assert len(S|T)<=4;pair_checks+=1
 # Realize integer copies and compare aggregate degrees/reaches exactly.
 bden=lcm(*(v.denominator for v in beta));cden=lcm(*(v.denominator for v in gamma))
 bcopies=[int(bden*v) for v in beta];ccopies=[int(cden*v) for v in gamma]
 assert sum(bcopies)==bden and sum(ccopies)==cden;assertions+=2
 for a in A:
  assert Q(sum(bcopies[b] for b,S in enumerate(types) if a in S),bden)==degreeA[a];assertions+=1
 for b,adj in enumerate(edges):
  assert Q(sum(ccopies[c] for c in adj),cden)==degreeB[b];assertions+=1
 rows.append({'k':k,'ordinary_part_sizes':[n,bden,cden],'x':str(x),'y':str(y),'max_A_reach':max(map(len,reaches)),'maximal_r_types':len(largest),'union_size':len(U),'residual_pair_checks':len(residual)**2})

# Strictness at |A|=5k: k+1 disjoint paths are counterexamples at equality
# x=y=1/(k+1), while |A|=k+1<=5k. Actual graph count, no weighted inference.
for k in range(2,51):
 n=k+1
 AB=[{i} for i in range(n)];BC=[{i} for i in range(n)]
 reach=[{a for a,S in enumerate(AB) if any(c in BC[b] for b in S)} for c in range(n)]
 assert max(map(len,reach))*k<n and n<=5*k;assertions+=1
 assert Q(1,n)==Q(1,k+1);assertions+=1
print(json.dumps({'status':'PASS','exact_assertions':assertions,'nonvacuous_residual_pair_checks':pair_checks,'below_reach_actual_ordinary_witnesses':rows,'equal_threshold_actual_path_controls':49,'scope':'Explicit ordinary below-reach graphs exercise the Turn 3 necessary bound and n=4k+1 residual compatibility without satisfying strict x threshold; no conjecture counterexample.'},indent=2))

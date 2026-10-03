#!/usr/bin/env python3
"""Post-inspection targeted falsification, separate from the source-first seal.
New implementation, no author or reviewer imports. Exact integers/Fractions.
"""
from itertools import combinations
from fractions import Fraction as F
import json,datetime
rows=[]
def actual(p,q,r,S,T):
 assert sum(p)==sum(q)==sum(r)==1 and all(v>0 for v in p+q+r)
 Adeg=[sum(q[b] for b,s in enumerate(S) if a in s) for a in range(len(p))]
 Bdeg=[sum(r[c] for c in t) for t in T]
 reach=[set().union(*(s for s,t in zip(S,T) if c in t)) for c in range(len(r))]
 masses=[sum(p[a] for a in v) for v in reach]
 return min(Adeg),min(Bdeg),max(masses)
# Three exact nonuniform, below-half witnesses. All actual edges are listed.
for nums,S,q in [([17,19,23,18,23],[{0,1},{1,2},{2,0},{3,4}],[F(1,5)]*3+[F(2,5)]),([2,2,500000000000000000-3,500000000000000000-1],[{0,1},{1,2},{2,0},{3}],[F(1,5)]*3+[F(2,5)]),([17,19,21,22,21],[{0,1},{1,2},{2,3},{3,4},{4,0}],[F(1,5)]*5)]:
 p=[F(v,sum(nums)) for v in nums];m=len(S);r=[F(1,m)]*m;T=[{c} for c in range(m)];x,y,z=actual(p,q,r,S,T)
 assert x==F(2,5) and z<F(1,2) and y<=F(1,4)
 rows.append({'A_weights':list(map(str,p)),'B_weights':list(map(str,q)),'C_weights':list(map(str,r)),'B_A_sets':list(map(sorted,S)),'B_C_sets':list(map(sorted,T)),'x':str(x),'y':str(y),'max_reach':str(z),'at_most_two_positive_A_types':True})
# Candidate's middle deletion, checked by cross multiplication and real edges.
params=[(k,x,y) for k in [2,3,19,1000003] for x,y in [(F(1,k+1)+F(1,10**18),F(1,k+1)+F(1,10**18)),(F(1,2*k),F(1,2)),(F(1,1000000000000),1-F(k,1000000000000)),(F(1),F(1,1000000))]]
checks=0;weakzero=0;denominators=[]
for k,x,y in params:
 d1=k*y;d2=k+y-1;assert d1>0 and d2>0
 first=(x+k*y-1)/d1;second=(k*x+y-1)/d2
 for epsilon in {F(0),x/2,x-F(1,10**30),first,second,first-F(1,10**30),first+F(1,10**30),second-F(1,10**30),second+F(1,10**30)}:
  if not 0<=epsilon<x:continue
  xp=(x-epsilon)/(1-epsilon)
  assert 0<xp<=1 and ((xp+k*y>1)==(x+k*y-1-epsilon*d1>0)) and ((k*xp+y>=1)==(k*x+y-1-epsilon*d2>=0));checks+=1
 if k*x+y==1:assert second==0;weakzero+=1
 denominators.append({'k':k,'x':str(x),'y':str(y),'ky':str(d1),'k+y-1':str(d2),'strict_bound':str(first),'weak_bound':str(second)})
p=[F(1,4)]*4;q=[F(9,20),F(9,20),F(1,10)];r=[F(3,5),F(2,5)];S=[{0,1},{2,3},{1,2}];T=[{0},{0,1},{0}]
x,y,z_deletion=actual(p,q,r,S,T);eps=q[-1];xp=(x-eps)/(1-eps);xnew,ynew,znew=actual(p,[v/(1-eps) for v in q[:-1]],r,S[:-1],T[:-1]);assert xnew>=xp and ynew>=y and znew<=z_deletion and eps<(x+2*y-1)/(2*y) and eps<=(2*x+y-1)/(1+y)
# Full exact local reassignment, explicitly reconstruct unchanged graph.
A=[frozenset(c) for c in combinations(range(11),9)];B=[frozenset(c) for c in combinations(range(11),4)];P=frozenset({0,1,2,3});Q=frozenset({4,5,6,7});S1={i for i,a in enumerate(A) if P<=a};S2={i for i,a in enumerate(A) if Q<=a};U=S1|S2;I=S1&S2
unchanged=[{i for i,a in enumerate(A) if any(c in b and b<=a for b in B if b!=P and b!=Q)} for c in range(11)]
assert all(len(v)==45 for v in unchanged)
rU=[len(v|U) for v in unchanged];rI=[len(v|I) for v in unchanged];rBoth=[len(v|U|I) for v in unchanged]
choices=[set(c) for c in combinations(range(11),4)];best=56;witness=None;count=0;hist={}
for uc in choices:
 for ic in choices:
  z=max(rBoth[c] if c in uc and c in ic else rU[c] if c in uc else rI[c] if c in ic else 45 for c in range(11));count+=1;hist[z]=hist.get(z,0)+1
  if z<best:best=z;witness=[sorted(uc),sorted(ic)]
assert best==51 and count==108900
print(json.dumps({'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'separate_from_source_first_seal':True,'nonvacuous_rank_two_actual_graphs':rows,'middle_deletion_boundary_checks':checks,'weak_boundary_zero_deletion_cases':weakzero,'middle_deletion_parameter_receipts':denominators,'actual_middle_deletion':{'x':str(x),'y':str(y),'epsilon':str(eps),'lower_x_prime':str(xp),'actual_x_prime':str(xnew),'actual_remaining_y':str(ynew),'reach_before':str(z_deletion),'reach_after':str(znew)},'uncrossing':{'ordinary_part_sizes':[55,330,11],'old_max':45,'all_reassignments':count,'maximum_reach_histogram':hist,'minimum_legal_max':best,'minimizer':witness,'union_per_C':rU,'intersection_per_C':rI}},indent=2))

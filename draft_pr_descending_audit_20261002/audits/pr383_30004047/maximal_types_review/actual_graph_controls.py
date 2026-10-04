#!/usr/bin/env python3
"""Independent exhaustive adjacency-matrix controls. No author imports.

All labelled A--B and B--C graphs in listed finite boxes are enumerated;
positive minimum forward degrees are required but no reverse degree is imposed.
For each graph its maximal admissible x,y are exact minimum-degree fractions.
Testing at these maxima covers all real smaller x,y for monotone conclusions.
Finite checks certify only these boxes, not the original universal conjecture.
"""
from itertools import product
from fractions import Fraction as Q
import json,time

started=time.time()
counts={'actual_graphs':0,'threshold_trigger_graph_k_pairs':0,'turn3_below_reach_cases':0,'equal_threshold_failure_graphs':0,'pairwise_residual_checks':0}
box_results=[]
first_boundary=None

def analyze(n,b,c):
 global first_boundary
 actual=0;trigger=0;necessary=0
 # B--C has no zero row (y>0); A--B has no zero row (x>0).
 for bc in product(range(1,1<<c),repeat=b):
  dC=min(v.bit_count() for v in bc)
  bsets=[sum(1<<i for i,v in enumerate(bc) if v&(1<<j)) for j in range(c)]
  # Precompute A forward C-reach for every possible A--B row.
  second=[0]*(1<<b)
  for s in range(1,1<<b):
   second[s]=0
   for i in range(b):
    if s&(1<<i):second[s]|=bc[i]
  for ab in product(range(1,1<<b),repeat=n):
   actual+=1;counts['actual_graphs']+=1
   dB=min(v.bit_count() for v in ab)
   AatB=[sum(1<<i for i,v in enumerate(ab) if v&(1<<j)) for j in range(b)]
   AatC=[sum(1<<i for i,s in enumerate(ab) if second[s]&(1<<j)) for j in range(c)]
   R=max(v.bit_count() for v in AatC)
   # k>=n is automatic since some positive two-reach exists.
   for k in range(2,max(3,n)):
    if n<=5*k and dB*(k+1)>b and dC*(k+1)>c:
     trigger+=1;counts['threshold_trigger_graph_k_pairs']+=1
     assert R*k>=n,(n,b,c,ab,bc,k)
    if R*k<n and dC*(k+1)>c:
     r=(n-1)//k
     assert r>=2,(n,b,c,ab,bc,k)
     maximal=sorted({s for s in AatB if s.bit_count()==r})
     t=len(maximal);U=0
     for s in maximal:U|=s
     assert t<=k-1
     u=U.bit_count()
     assert Q(dB,b)<=Q(r*(r-1),r*n-u)<=Q(r-1,n-t)<=Q(r-1,n-k+1)
     necessary+=1;counts['turn3_below_reach_cases']+=1
     if n==4*k+1:
      residual=[s for s in AatB if not any(s&~v==0 for v in maximal)]
      for s in residual:
       for t2 in residual:
        assert (s|t2).bit_count()<=4
        counts['pairwise_residual_checks']+=1
    # Preserve strictness: report actual failures on the equality threshold.
    if dB*(k+1)==b and dC*(k+1)==c and R*k<n:
     counts['equal_threshold_failure_graphs']+=1
     if first_boundary is None:first_boundary={'parts':[n,b,c],'A_to_B_rows':ab,'B_to_C_rows':bc,'k':k,'x':str(Q(dB,b)),'y':str(Q(dC,c)),'max_A_reach':R}
 return {'parts':[n,b,c],'actual_graphs':actual,'strict_threshold_graph_k_pairs':trigger,'turn3_below_reach_cases':necessary}

# Materially distinct from canonical charge generation: actual two-layer graphs.
boxes=[(n,b,c) for n in range(1,6) for b in range(1,4) for c in range(1,4)]
boxes += [(6,3,2),(7,2,3),(8,2,3),(4,4,2)]
for box in boxes:box_results.append(analyze(*box))
result={'status':'PASS','mechanism':'exhaustive_actual_labelled_graphs','uniform_A':True,'no_reverse_degree_assumptions':True,'counts':counts,'first_equality_failure':first_boundary,'boxes':box_results,'elapsed_seconds':round(time.time()-started,3),'scope':'Only listed actual finite graph boxes; no arbitrary-graph or weighted-support extrapolation.'}
print(json.dumps(result,indent=2))

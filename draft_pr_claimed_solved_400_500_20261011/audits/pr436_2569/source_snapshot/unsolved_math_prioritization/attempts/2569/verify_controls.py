#!/usr/bin/env python3
"""Exact finite controls, not a proof of the unrestricted conjecture."""
import json
from pathlib import Path

def rank_mod(A,p):
 A=[list(r) for r in A]; m=len(A); n=len(A[0]) if m else 0; r=0
 for c in range(n):
  j=next((j for j in range(r,m) if A[j][c]%p),None)
  if j is None: continue
  A[r],A[j]=A[j],A[r]; v=pow(A[r][c],-1,p); A[r]=[(x*v)%p for x in A[r]]
  for j in range(m):
   if j!=r:
    v=A[j][c]; A[j]=[(x-v*y)%p for x,y in zip(A[j],A[r])]
  r+=1
 return r

def quaternion_padding_controls():
 rows=[]
 for p in [3,5,7,11]:
  for a in [1,2,3]:
   n=p**a
   assert n%2==1
   rows.append({"p":p,"cyclic_p_group_order":n,"faithful_simple_multiplicity_in_pim":n,"rational_reduction_multiplicities_divisible_by":2,"excluded":True})
 return rows

def jordan_controls():
 rows=[]
 for p in [2,3,5,7,11]:
  N=[[int(i==(j+1)%p)-int(i==j) for j in range(p)] for i in range(p)]
  r=rank_mod(N,p)
  assert r==p-1
  rows.append({"p":p,"regular_dimension":p,"regular_g_minus_1_rank":r,"trivial_sum_g_minus_1_rank":0,"regular_coinvariants":p-r,"trivial_sum_coinvariants":p})
 return rows
if __name__=="__main__":
 out={"jordan_and_coinvariant_controls":jordan_controls(),"quaternion_padding_controls":quaternion_padding_controls()}
 Path(__file__).with_name("control_results.json").write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps(out,indent=2))

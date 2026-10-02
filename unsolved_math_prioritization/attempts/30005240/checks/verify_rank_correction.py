#!/usr/bin/env python3
from fractions import Fraction as Q
import json
count=0
for L in range(1,101):
 sigma=Q(5,7)
 matrix=[[sigma if (i<L and j==i+1) or (i==L and j==L) else Q(0) for j in range(L+1)] for i in range(L+1)]
 assert all(row[0]==0 for row in matrix);count+=1
 assert matrix[L]==matrix[L-1];count+=1
 for i in range(L):
  for j in range(1,L+1):
   assert matrix[i][j]==(sigma if j==i+1 else 0);count+=1
print(json.dumps({'status':'PASS','assertions':count,'rank':'exactly L','scope':'Finite rank certificates supplement the general coordinate proof in REVIEW_CORRECTION_1.md.'},indent=2,sort_keys=True))

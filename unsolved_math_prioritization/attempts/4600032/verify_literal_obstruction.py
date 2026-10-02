#!/usr/bin/env python3
from itertools import product
import json
checks=0

def ck(x):
 global checks
 assert x
 checks+=1

# Verify every finite permitted word in the constant-sequence SFT.
for N in range(2,7):
 for k in range(1,6):
  words=[w for w in product(range(N+1),repeat=k) if all(w[i]==w[i+1] for i in range(k-1))]
  ck(len(words)==N+1);ck(set(words)=={(a,)*k for a in range(N+1)})
 for a in range(N+1):
  predecessors=[b for b in range(N+1) if b==a]
  ck(predecessors==[a]);ck(len(predecessors)<=N)
 # Every image of a source fixed point must be one of the N target constants.
 if N<=4:
  for image in product(range(N),repeat=N+1):ck(len(set(image))<N+1)
 # Adjacency identity matrix has one incoming edge at every vertex.
 A=[[int(i==j) for j in range(N+1)] for i in range(N+1)]
 ck(all(sum(A[i][j] for i in range(N+1))==1 for j in range(N+1)))
 ck(sum(A[i][i] for i in range(N+1))==N+1)
print(json.dumps({'status':'PASS','exact_assertions':checks,'tested_N_values':list(range(2,7)),'scope':'Finite controls for the classical fixed-point obstruction only; no repaired one-sided embedding sufficiency claim.'},indent=2))

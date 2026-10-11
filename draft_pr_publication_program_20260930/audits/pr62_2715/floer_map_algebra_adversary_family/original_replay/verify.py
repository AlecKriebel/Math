#!/usr/bin/env python3
"""Bounded exact algebra diagnostics; no Floer computation or knot search."""
from itertools import product
from collections import Counter
from pathlib import Path
import json,hashlib
checks=0

def ck(v):
    global checks
    assert v
    checks+=1

# Coordinatewise injection plus equality of total dimension forces equality.
graded=tuple(product(range(3),repeat=3))
pairs=0
for A in graded:
 for B in graded:
    if all(a<=b for a,b in zip(A,B)) and sum(A)==sum(B):
        ck(A==B);pairs+=1
# Actual invertible F2 matrices, not numerical rank tests.
def inverse(A):
 n=len(A);W=[list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(A)]
 for k in range(n):
    p=next((i for i in range(k,n) if W[i][k]),None)
    if p is None:return None
    W[k],W[p]=W[p],W[k]
    for i in range(n):
        if i!=k and W[i][k]: W[i]=[x^y for x,y in zip(W[i],W[k])]
 return [row[n:] for row in W]
def mul(A,B):return [[sum(a*b for a,b in zip(row,col))%2 for col in zip(*B)] for row in A]
invertible={}
for n in (1,2,3):
 count=0;I=[[int(i==j) for j in range(n)] for i in range(n)]
 for raw in product((0,1),repeat=n*n):
    A=[list(raw[i*n:(i+1)*n]) for i in range(n)];B=inverse(A)
    if B is not None:
        ck(mul(B,A)==I);ck(mul(A,B)==I);count+=1
 invertible[n]=count
ck(invertible=={1:1,2:6,3:168})
# Formal partial-order functor: its noninvertible arrow maps to a linear iso.
order={(0,0),(0,1),(1,1)}
ck((0,1) in order and (1,0) not in order)
ck([[1]]==inverse([[1]]))
# Finite grading-shift model of Wang's formula; this is not an actual knot table.
base=Counter({(0,0):2,(1,2):1})
H=Counter({(-1,1):1,(2,3):2})
def family(n):return base+Counter({(h+2*n,q+4*n):c for (h,q),c in H.items()})
models=[family(n) for n in range(-3,4)]
for i,A in enumerate(models):
 ck(sum(A.values())==sum(base.values())+sum(H.values()))
 for j,B in enumerate(models):
    if i!=j:
        ck(A!=B)
        ck(not all(A[k]<=B[k] for k in A))
# Oddness and a conditional strict-drop bound are elementary arithmetic.
for ranks in product(range(4),repeat=4):
 euler=ranks[0]-ranks[1]+ranks[2]-ranks[3]
 if euler==1:ck(sum(ranks)%2==1)
for R in range(1,52,2):
 chain=list(range(R,0,-2));ck(len(chain)-1==(R-1)//2)
 ck(chain[-1]==1)
# Births and maxima exchange under reversal of an annular Morse function.
ck([2-i for i in (0,1)]==[2,1])
result={'status':'PASS','assertions':checks,'equal_rank_graded_pairs':pairs,'invertible_F2_matrices':invertible,'artifact_sha256':hashlib.sha256(Path(__file__).with_name('OBSTRUCTION.md').read_bytes()).hexdigest(),'scope':'Finite linear-algebra, grading and conditional arithmetic controls only. No knot Floer calculations, knot search, or proof of KP-1.56.'}
print(json.dumps(result,indent=2,sort_keys=True))

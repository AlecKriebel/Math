#!/usr/bin/env python3
"""Independent exact examples for the transition model, not asymptotic proofs."""
import json
from math import comb
from pathlib import Path

def cumulative(A,b,c,n):
    v=b[:]
    total=0
    for k in range(n+1):
        total += sum(x*y for x,y in zip(v,c))
        v=[sum(v[i]*A[i][j] for i in range(len(A))) for j in range(len(A))]
    return total

cases=[]
for n in range(101):
    assert cumulative([[0,1],[0,0]],[1,0],[0,1],n) == int(n>=1)
    assert cumulative([[0,1],[1,0]],[1,0],[1,0],n) == n//2+1
    assert cumulative([[1,1],[0,1]],[1,0],[0,1],n) == n*(n+1)//2
    assert cumulative([[1,1,0],[0,1,1],[0,0,1]],[1,0,0],[0,0,1],n) == comb(n+1,3)
    assert cumulative([[2]],[1],[1],n) == 2**(n+1)-1
    cases.append(n)
for k in range(1,101):
    assert 2**(k*(k+1)//2) == 2**k * 2**((k-1)*k//2)
result={
    "status":"pass",
    "counts_tested":"101 lengths for each of five exact symbolic-formula examples",
    "models":["acyclic (eventual constant)","one cycle (linear cumulative)","two cyclic SCCs (quadratic cumulative)","three cyclic SCCs (cubic cumulative)","parallel loops (exponential)"],
    "recurrence_indices": [1,100],
    "scope":"Examples and finite arithmetic only; asymptotic conclusions require the independent mathematical audit."
}
Path(__file__).with_name('transition_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

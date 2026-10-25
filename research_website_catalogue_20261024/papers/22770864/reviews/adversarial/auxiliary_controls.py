#!/usr/bin/env python3
"""Supplementary exact tau and H1 checks; imports only this review's code."""
import json
from fresh_exact_checks import original, bracket, add, rank, OUT

c=original()

def tau(v):
    z={}
    for k,a in v.items():
        target=k+15 if 10<=k<15 else k-15 if 25<=k<30 else k
        z[target]=-a if k==30 else a
    return z

n=0
for i in range(31):
    for j in range(31):
        assert tau(bracket(c,{i:1},{j:1}))==bracket(c,tau({i:1}),tau({j:1}))
        n+=1

coho=[]
for highest,start in [(0,30),(2,22),(4,10),(6,3)]:
    size=highest+1; rows=[]
    for a,b,d,scalar in [(0,1,1,2),(0,2,2,-2),(1,2,0,1)]:
        for k in range(size):
            row={d*size+k:scalar}
            for t in range(size):
                add(row,b*size+t,-c.get((a,start+t),{}).get(start+k,0))
                add(row,a*size+t,c.get((b,start+t),{}).get(start+k,0))
            rows.append(row)
    cob=[{t:c.get((a,start+t),{}).get(start+k,0) for t in range(size)}
         for a in range(3) for k in range(size)]
    kernel=3*size-rank(rows); image=rank(cob)
    assert kernel==image
    coho.append([highest,kernel,image])

result={'tau_bracket_checks':n,'H1_checks':coho}
(OUT/'auxiliary_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

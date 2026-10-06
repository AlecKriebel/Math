#!/usr/bin/env python3
"""Independent exact matrix and Segre-fiber controls."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import Counter
import hashlib
import json

C=Counter()
def ck(name,b):
    if not b:raise ValueError(name)
    C[name]+=1
def mono(i,j):
    ans=[0]*6
    ans[i]+=1;ans[3+j]+=1
    return tuple(ans)
pairs=[(0,1),(1,2),(2,0)]
positive=[mono(i,j) for i,j in pairs]
negative=[mono(j,i) for i,j in pairs]
columns=positive+negative
E=[[col[j] for col in columns] for j in range(6)]
A=E+[[int(j==i or j==i+3) for j in range(6)] for i in range(3)]
def mv(M,v):
    return [sum(F(a)*b for a,b in zip(row,v)) for row in M]
def rank(M):
    m=[[F(a) for a in row] for row in M];r=0
    for j in range(len(m[0])):
        pivot=next((i for i in range(r,len(m)) if m[i][j]),None)
        if pivot is None:continue
        m[r],m[pivot]=m[pivot],m[r]
        v=m[r][j];m[r]=[a/v for a in m[r]]
        for i in range(len(m)):
            if i!=r and m[i][j]:
                v=m[i][j];m[i]=[a-v*b for a,b in zip(m[i],m[r])]
        r+=1
        if r==len(m):break
    return r
ck('matrix_rank',rank(E)==5 and rank(A)==5)
ck('kernel',mv(A,[1,1,1,-1,-1,-1])==[0]*9)
ck('dual_pair_caps',mv(list(map(list,zip(*A))),[0]*6+[1]*3)==[1]*6)
ck('dual_variable_loads',mv(list(map(list,zip(*A))),[F(1,2)]*6+[0]*3)==[1]*6)
ck('endpoint_plus',mv(A,[1,1,1,0,0,0])==[1]*9)
ck('endpoint_minus',mv(A,[0,0,0,1,1,1])==[1]*9)
for den in range(1,31):
    for num in range(den+1):
        t=F(num,den);v=[t]*3+[1-t]*3
        ck('segment_image',mv(A,v)==[1]*9)
        ck('segment_objective',sum(v)==3)
        other=[1]*3+[0]*3 if t!=1 else [0]*3+[1]*3
        ck('rational_fiber_not_singleton',other!=v and mv(A,other)==mv(A,v))

# Exhaust the three last-row saturation parameters on a rational grid.
# Feasibility then forces equality of all three mu coordinates.
for a,b,c in product(range(7),repeat=3):
    v=[F(a,6),F(b,6),F(c,6),1-F(a,6),1-F(b,6),1-F(c,6)]
    feasible=all(x<=1 for x in mv(A,v))
    ck('saturated_slice',feasible==(a==b==c))

# Segre monomial parameterization: xi -> s ui, yi -> t ui.
def image(e):
    return (sum(e[:3]),sum(e[3:]),e[0]+e[3],e[1]+e[4],e[2]+e[5])
for a,b in zip(positive,negative):
    ck('binomials_in_kernel',image(a)==image(b))
ck('minimal_quadratic_support',len(set(columns))==6)
ck('quadratic_independence',rank([[int(m==a)-int(m==b) for m in columns] for a,b in zip(positive,negative)])==3)
ck('Segre_rank',rank([[image(tuple(int(i==j) for i in range(6)))[k] for j in range(6)] for k in range(5)])==4)

# General straightening move tested on all monomial pairs with column totals
# up to five. Each step exchanges xi*yj and xj*yi, and strictly decreases
# the distance from the target row allocation.
for totals in product(range(6),repeat=3):
    if sum(totals)>5:continue
    states=list(product(*(range(c+1) for c in totals)))
    for alpha in states:
        e=alpha+tuple(totals[i]-alpha[i] for i in range(3))
        ck('nonzero_monomial_image',sum(image(e))==2*sum(totals))
        for beta in states:
            if sum(alpha)!=sum(beta):continue
            current=list(alpha)
            start_distance=sum(abs(alpha[i]-beta[i]) for i in range(3))
            steps=0
            while tuple(current)!=beta:
                i=next(i for i in range(3) if current[i]>beta[i])
                j=next(j for j in range(3) if current[j]<beta[j])
                ck('straightening_divisibility',current[i]>0 and totals[j]-current[j]>0)
                before=tuple(current)+tuple(totals[k]-current[k] for k in range(3))
                current[i]-=1;current[j]+=1;steps+=1
                after=tuple(current)+tuple(totals[k]-current[k] for k in range(3))
                ck('straightening_image',image(before)==image(after))
                diff=tuple(before[k]-after[k] for k in range(6))
                gens=[tuple(a[k]-b[k] for k in range(6)) for a,b in zip(positive,negative)]
                ck('straightening_generator',diff in gens or tuple(-x for x in diff) in gens)
            ck('straightening_termination',2*steps==start_distance)

root=Path(__file__).resolve().parent
snapshot=root/'author_replay/CANDIDATE.md'
out={'status':'PASS','assertions':sum(C.values()),'checks':dict(C),
     'augmented_matrix':A,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'artifact_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest() if snapshot.exists() else None,
     'limitations':'Finite monomial fibers and rational grids supplement the complete straightening and optimal-face proofs; no novelty or log-canonical-threshold computation is inferred.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

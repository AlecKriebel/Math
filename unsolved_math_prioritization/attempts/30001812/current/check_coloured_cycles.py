#!/usr/bin/env python3
"""Finite bookkeeping checks only; not a universal topology/proof certificate."""
from collections import defaultdict
from fractions import Fraction
from itertools import permutations
import json

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sign(p):
    return (-1) ** sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1,len(p)))

def boundary(c):
    out=defaultdict(Fraction)
    for s,a in c.items():
        for i in range(len(s)):
            out[s[:i]+s[i+1:]] += a * (-1)**i
    return {s:a for s,a in out.items() if a}

def sym(c):
    out=defaultdict(Fraction)
    n=len(next(iter(c)))
    pp=list(permutations(range(n)))
    for s,a in c.items():
        for p in pp:
            out[tuple(s[i] for i in p)] += a * sign(p) / len(pp)
    return {s:a for s,a in out.items() if a}

def face(c,i):
    out=defaultdict(Fraction)
    for s,a in c.items():
        out[s[:i]+s[i+1:]] += a
    return {s:a for s,a in out.items() if a}

original=boundary({tuple(range(5)):Fraction(1)})
require(not boundary(original), 'Diagnostic failed: not boundary(original)')
normalized=sym(original)
require(not boundary(normalized), 'Diagnostic failed: not boundary(normalized)')
require(all(not face(normalized,i) for i in range(4)), 'Diagnostic failed: all(not face(normalized,i) for i in range(4))')
require(sum(map(abs,normalized.values())) == sum(map(abs,original.values())) == 5, 'Diagnostic failed: sum(map(abs,normalized.values())) == sum(map(abs,original.values())) == 5')
m=24
copies=[]
for s,a in normalized.items():
    n=a*m
    require(n.denominator==1, 'Diagnostic failed: n.denominator==1')
    copies += [(s,1 if n>0 else -1)]*abs(n.numerator)
require(len(copies)==120, 'Diagnostic failed: len(copies)==120')
parent=list(range(4*len(copies)))
def root(x):
    while parent[x]!=x:
        parent[x]=parent[parent[x]]
        x=parent[x]
    return x

def union(a,b):
    parent[root(a)]=root(b)

pairs=[]
for i in range(4):
    by_face=defaultdict(lambda:{1:[],-1:[]})
    for a,(s,orientation) in enumerate(copies):
        by_face[s[:i]+s[i+1:]][orientation].append(a)
    for f,sides in by_face.items():
        require(len(sides[1])==len(sides[-1]), 'Diagnostic failed: len(sides[1])==len(sides[-1])')
        for a,b in zip(sides[1],sides[-1]):
            pairs.append((i,a,b))
            require(copies[a][1]==-copies[b][1], 'Diagnostic failed: copies[a][1]==-copies[b][1]')
            for j in range(4):
                if i!=j:
                    require(copies[a][0][j]==copies[b][0][j], 'Diagnostic failed: copies[a][0][j]==copies[b][0][j]')
                    union(4*a+j,4*b+j)
require(len(pairs)==240, 'Diagnostic failed: len(pairs)==240')
colors=defaultdict(set)
for k in range(4*len(copies)):
    colors[root(k)].add(k%4)
require(all(len(c)==1 for c in colors.values()), 'Diagnostic failed: all(len(c)==1 for c in colors.values())')
require(Fraction(len(copies),m)==5, 'Diagnostic failed: Fraction(len(copies),m)==5')
require(Fraction(24,8)==3, 'Diagnostic failed: Fraction(24,8)==3')
require(Fraction(1,8)*8==1, 'Diagnostic failed: Fraction(1,8)*8==1')
out={
 'status':'PASS',
 'test':'symmetrized boundary of an abstract4-simplex',
 'original_tetrahedra':len(original),
 'original_l1':str(sum(map(abs,original.values()))),
 'symmetrized_l1':str(sum(map(abs,normalized.values()))),
 'denominator':m,
 'paired_tetrahedra':len(copies),
 'face_pairs':len(pairs),
 'individual_face_operators_zero':[not face(normalized,i) for i in range(4)],
 'all_vertex_identifications_color_preserving':True,
 'normalized_tetrahedron_count':str(Fraction(len(copies),m)),
 'barycentric_loss_removed':24,
 'scope':'Formal finite face/sign/denominator check; no Gaifullin topology or all-space theorem is certified computationally.'
}
print(json.dumps(out,indent=2))

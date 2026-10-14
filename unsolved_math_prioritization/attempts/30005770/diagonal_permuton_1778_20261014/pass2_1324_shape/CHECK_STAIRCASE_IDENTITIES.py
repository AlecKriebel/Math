"""Finite identity checks only; not a proof of the asymptotic theorem."""
from itertools import permutations, combinations
from collections import Counter
from pathlib import Path
import json


def standardize(p):
    d={v:i+1 for i,v in enumerate(sorted(p))}
    return tuple(d[v] for v in p)

def avoids(p,pat):
    return not any(standardize(tuple(p[i] for i in I))==pat
                   for I in combinations(range(len(p)),len(pat)))

def prefix(p,pat):
    for k in range(1,len(p)+1):
        if not avoids(p[:k],pat):return k-1
    return len(p)

def top(p,pat):
    for k in range(1,len(p)+1):
        q=tuple(v for v in p if v>len(p)-k)
        if not avoids(q,pat):return k-1
    return len(p)

def inverse(p):
    q=[0]*len(p)
    for i,v in enumerate(p,1):q[v-1]=i
    return tuple(q)

def greedy_cells(p):
    remaining=list(enumerate(p,1));cells=[]
    while remaining:
        q=standardize(tuple(v for _,v in remaining))
        if len(cells)%2==0:
            m=top(q,(2,1,3));cut=sorted(v for _,v in remaining)[-m]
            cell=[point for point in remaining if point[1]>=cut]
        else:
            m=prefix(q,(1,3,2));cell=remaining[:m]
        assert m>0
        cells.append(cell);chosen=set(cell)
        remaining=[point for point in remaining if point not in chosen]
    return cells

def skew(a,b):
    return tuple(v+len(b) for v in a)+tuple(b)

counts=Counter();av=[]
for n in range(1,9):
    current=0
    for p in permutations(range(1,n+1)):
        if not avoids(p,(1,3,2,4)):continue
        current+=1;cells=greedy_cells(p);sizes=[len(c) for c in cells]
        assert sum(sizes)==n
        assert top(p,(2,1,3))==prefix(tuple(reversed(inverse(p))),(3,1,2))
        assert prefix(p,(1,3,2))==prefix(tuple(n+1-v for v in p),(3,1,2))
        counts['frontier_symmetry_pairs']+=1
        for j,C in enumerate(cells):
            Q=sum(sizes[max(0,j-1):j+2])
            for i,v in C:
                assert abs(i+v-n-1)<=Q-1
                counts['local_geometry_points']+=1
            for D in cells[j+2:]:
                assert all(i<k and v>w for i,v in C for k,w in D)
                counts['nonadjacent_cell_pairs']+=1
        counts['canonical_griddings']+=1
    av.append(current)
examples=[]
for r in range(1,8):
    for N in range(1,10):
        p=tuple(range(1,N+1))
        for _ in range(r):p=skew((2,4,1,3),p)
        for _ in range(r):p=skew(p,(2,4,1,3))
        expected=[3]+[4]*(r-1)+[N+4]+[4]*(r-1)+[1]
        actual=[len(c) for c in greedy_cells(p)]
        assert actual==expected,(r,N,actual,expected)
        counts['escape_example_cell_sequences']+=1
        if r<=2:examples.append({'r':r,'N':N,'cell_sizes':actual})
result={'status':'passed','scope':'Finite identity sanity checks only; no asymptotic inference',
        'counts':dict(counts),'avoidance_counts_n_1_through_8':av,
        'small_escape_examples':examples}
Path(__file__).with_name('FINITE_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='small_escape_examples'},indent=2))

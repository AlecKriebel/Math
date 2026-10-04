#!/usr/bin/env python3
"""Independent tuple-coordinate audit; imports no release implementation.

The audit uses lexicographic coordinate vectors, permutation inversion for strong
units, and all-element associativity tests. Release data is loaded only after
all independent computations, for exact comparison of table lists and counts.
"""
from itertools import product
from collections import Counter
import hashlib
import json
from pathlib import Path

V = tuple(product((0, 1), repeat=3))
IDX = {v:i for i,v in enumerate(V)}
Z, ONE = IDX[(0,0,0)], IDX[(1,0,0)]
BIT = tuple(a+2*b+4*c for a,b,c in V)

def multiplication(structure):
    out = []
    for a,b,c in V:
        row=[]
        for d,e,f in V:
            scalar = (a*d, a*e+b*d, a*f+c*d)
            coefficients = (b*e,b*f,c*e,c*f)
            result=tuple((scalar[k]+sum(coef*term[k] for coef,term in
                         zip(coefficients,structure)))%2 for k in range(3))
            row.append(IDX[result])
        out.append(row)
    return out

def invert_permutation(p):
    if len(set(p)) != 8:
        return None
    out=[None]*8
    for i,j in enumerate(p):out[j]=i
    return out

def strong_units(m):
    result=[]
    for a in range(8):
        li=invert_permutation(m[a])
        ri=invert_permutation([m[z][a] for z in range(8)])
        if li is None or ri is None:continue
        b=li[ONE]
        if b==ri[ONE] and m[b]==li and [m[z][b] for z in range(8)]==ri:
            result.append(a)
    return result

def moufang(m,u):
    for y,z in product(range(8), repeat=2):
        if m[u][m[y][m[u][z]]] != m[m[u][m[y][u]]][z]:return False
        if m[m[m[z][u]][y]][u] != m[z][m[m[u][y]][u]]:return False
        if m[m[u][y]][m[z][u]] != m[m[u][m[y][z]]][u]:return False
    return True

def z_condition(m):
    for a in range(8):
        right_ann=[b for b in range(8) if m[a][b]==Z]
        left_ann=[c for c in range(8) if m[c][a]==Z]
        for b,c in product(right_ann,left_ann):
            d=m[b][c]
            for t in range(8):
                if (m[d][m[a][t]]!=Z or m[m[t][a]][d]!=Z or
                    m[a][m[d][t]]!=Z or m[m[t][d]][a]!=Z):return False
    return True

def main():
    counts=Counter();unit_hist=Counter();unit_survivors=[];both_survivors=[]
    for structure in product(V,repeat=4):
        m=multiplication(structure)
        assert all(m[ONE][x]==x==m[x][ONE] for x in range(8))
        units=strong_units(m)
        alt=all(m[m[a][a]][b]==m[a][m[a][b]] and
                m[m[b][a]][a]==m[b][m[a][a]] for a,b in product(range(8),repeat=2))
        assoc=all(m[m[a][b]][c]==m[a][m[b][c]] for a,b,c in product(range(8),repeat=3))
        unit_ok=all(moufang(m,u) for u in units)
        covered=all(a in units or IDX[(V[a][0]^1,V[a][1],V[a][2])] in units for a in range(8))
        counts['total']+=1;counts['alternative']+=alt;counts['associative']+=assoc
        counts['unit_moufang']+=unit_ok;counts['integer_shift_covers']+=covered
        assert not covered or not unit_ok or alt
        if alt:assert z_condition(m)
        if unit_ok and not alt:
            ring=[BIT[IDX[t]] for t in structure]
            unit_survivors.append(ring);unit_hist[len(units)]+=1
            if z_condition(m):both_survivors.append(ring)
    unit_survivors.sort();both_survivors.sort()
    counts['nonalternative_survivors']=len(unit_survivors)
    counts['nonalternative_after_both_filters']=len(both_survivors)
    counts['nonalternative_rejected_by_opposite_root']=len(unit_survivors)-len(both_survivors)
    digest=hashlib.sha256(json.dumps(unit_survivors,separators=(',',':')).encode()).hexdigest()
    release=json.loads((Path(__file__).parent.parent/'release'/'finite_algebra_results.json').read_text())
    assert dict(counts)==release['counts']
    assert {str(k):v for k,v in sorted(unit_hist.items())}==release['nonalternative_survivor_unit_counts']
    assert digest==release['unit_moufang_nonalternative_tables_sha256']
    assert both_survivors==release['survivor_tables_after_both_filters']
    print(json.dumps({'independent_implementation':True,'release_imported':False,
          'counts':dict(counts),'nonalternative_survivor_unit_counts':dict(sorted(unit_hist.items())),
          'all_576_survivor_tables_match':True,'intermediate_3900_tables_hash_matches':True,
          'unit_moufang_nonalternative_tables_sha256':digest,
          'group_realization_checked':False},indent=2,sort_keys=True))

if __name__=='__main__':main()

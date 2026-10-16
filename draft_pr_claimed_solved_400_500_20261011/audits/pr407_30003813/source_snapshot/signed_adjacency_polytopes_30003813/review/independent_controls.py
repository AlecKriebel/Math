#!/usr/bin/env python3
"""Independent audit controls. Does not import or reuse the authored verifier."""
from itertools import permutations, product, combinations_with_replacement, groupby
from collections import defaultdict, Counter
from math import comb
import hashlib, json
from pathlib import Path

OUT = Path(__file__).parent
stats = Counter()

def des(p):
    return tuple(i for i in range(len(p)-1) if p[i] > p[i+1])

def inv(p):
    q = [0]*len(p)
    for i, a in enumerate(p): q[a] = i
    return tuple(q)

def ok(x, signs, m, strict=False):
    return all((x[i]+x[i+1] < m if strict else x[i]+x[i+1] <= m)
               if s == '-' else
               (x[i]+x[i+1] > m if strict else x[i]+x[i+1] >= m)
               for i,s in enumerate(signs))

def transfer(signs,m):
    # Explicit dense transition matrices, in original coordinates.
    v = [1]*(m+1)
    for s in signs:
        v = [sum(v[a] for a in range(m+1)
                 if (a+b<=m if s=='-' else a+b>=m))
             for b in range(m+1)]
    return sum(v)

def canon(D,n):
    # Reverse each maximal descending block in the identity permutation.
    p=list(range(n)); start=0
    for end in range(n):
        if end not in D:
            p[start:end+1] = reversed(p[start:end+1]); start=end+1
    assert des(p)==D
    return tuple(p)

examples={}
for n in range(1,8):
    classes=defaultdict(list)
    for p in permutations(range(n)): classes[des(p)].append(p)
    for signs in product('-+',repeat=n-1):
        # The theorem's sign/descent conversion, without poset construction.
        D=tuple(i for i,s in enumerate(signs)
                if (i%2==0 and s=='+') or (i%2==1 and s=='-'))
        alpha=canon(D,n)
        inverses=[inv(sigma) for sigma in classes[D]]
        h=Counter(len(des(tuple(alpha[j] for j in q))) for q in inverses)
        for beta in classes[D]:
            hb=Counter(len(des(tuple(beta[j] for j in q))) for q in inverses)
            assert hb==h, ('label invariance',n,signs,beta,h,hb)
            stats['natural_labelings_checked']+=1
            stats['relative_descent_pairs_checked']+=len(inverses)
        for m in range(n+4):
            raw=transfer(signs,m)
            predicted=sum(c*comb(m+n-k,n) for k,c in h.items() if m>=k)
            assert raw==predicted,('original transfer mismatch',n,signs,m)
            stats['dense_original_coordinate_counts']+=1
            if n<=5:
                direct=sum(ok(x,signs,m) for x in product(range(m+1),repeat=n))
                assert direct==raw,('direct grid mismatch',n,signs,m)
                stats['direct_grid_lattice_counts']+=1
                stats['direct_grid_points_examined']+=(m+1)**n
        # Independent degree control via codegree / longest directed chain.
        dirs=[i in D for i in range(n-1)]
        chain=1+max((len(list(g)) for _,g in groupby(dirs)),default=0)
        assert max(h)==n-chain,('degree mismatch',n,signs,h,chain)
        stats['degree_codegree_controls']+=1
        if n<=5:
            for m in range(1,8):
                interior=sum(ok(x,signs,m,True)
                             for x in product(range(1,m),repeat=n))
                predicted=sum(c*comb(m+k-1,n) for k,c in h.items() if m+k-1>=n)
                assert interior==predicted,('reciprocity mismatch',n,signs,m)
                stats['strict_interior_reciprocity_counts']+=1
            # Reverse construction: every half-open simplex contributes once.
            labels_to_test=classes[D] if n<=4 else [alpha]
            for beta in labels_to_test:
                for m in range(5):
                    assigned=Counter()
                    for w in inverses:
                        labels=tuple(beta[j] for j in w)
                        strict_at=des(labels)
                        for a in combinations_with_replacement(range(m+1),n):
                            if any(a[j]==a[j+1] for j in strict_at): continue
                            y=[0]*n
                            for j,vertex in enumerate(w): y[vertex]=a[j]
                            x=tuple(y[j] if j%2==0 else m-y[j] for j in range(n))
                            assert ok(x,signs,m)
                            assigned[x]+=1
                    target={x for x in product(range(m+1),repeat=n) if ok(x,signs,m)}
                    assert set(assigned)==target
                    assert all(c==1 for c in assigned.values())
                    stats['exhaustive_boundary_partition_cases']+=1
                    stats['boundary_points_reconstructed']+=len(assigned)
        stats['sign_patterns_checked']+=1
        if n<=4: examples[''.join(signs) or '(empty)']=dict(sorted(h.items()))

# Deliberately wrong conventions must be distinguishable.
alpha=(0,2,1); sigmas=[p for p in permutations(range(3)) if des(p)==(1,)]
raw=Counter(len(des(inv(p))) for p in sigmas)
assert raw==Counter({1:2})
assert transfer(('-', '-'),1)==5
# Incorrect use of T_1 on a 2-dilate sends an admitted x=(0,2) to (0,-1).
assert ok((0,2),('-',),2) and not (0 <= 1-2 <= 2)
# Labeling outside the required descent class invalidates h_0=1.
wrong=Counter(len(des(tuple(tuple(range(3))[j] for j in inv(p)))) for p in sigmas)
assert wrong[0]==0
stats['negative_controls']=3
result={'verdict':'PASS','independence':'Standalone code, no imports from or modifications to the frozen candidate',
        'coverage':dict(stats),'small_examples':examples,
        'scope':'Exact finite controls supplement the separately audited all-n proof.'}
path=OUT/'independent_results.json'
path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))

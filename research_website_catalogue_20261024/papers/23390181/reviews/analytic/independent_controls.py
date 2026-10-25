#!/usr/bin/env python3
"""Fresh direct-word, cyclic-factor and matrix controls; no published checker imports.

Exact integer checks are separated from floating spectral diagnostics. These tests
cannot prove the asymptotic theorem or property (T).
"""
from collections import Counter
from functools import lru_cache
from itertools import product
from pathlib import Path
import datetime
import hashlib
import json
import math
import random
import numpy as np

checks = Counter()
samples = []

def require(condition, family):
    checks[family] += 1
    if not condition:
        raise ValueError(family)

def alphabet(sizes):
    return tuple((i, a) for i, n in enumerate(sizes) for a in range(1, n+1))

def inverse(w, sizes):
    return tuple((i, (-a) % (sizes[i]+1)) for i, a in reversed(w))

def words(sizes, length):
    abc = alphabet(sizes)
    def extend(w):
        if len(w) == length:
            yield w
        else:
            for a in abc:
                if not w or w[-1][0] != a[0]:
                    yield from extend(w+(a,))
    return extend(())

@lru_cache(None)
def visible(sizes, length):
    return tuple(w for w in words(sizes, length) if w != inverse(w, sizes))

def cuts(ell):
    q, e = divmod(ell, 3)
    return (q, q+(e == 2), q+(e > 0))

def blocks(w):
    a, b, c = cuts(len(w))
    return (w[:a], w[a:a+b], w[a+b:])

def direct_link(sizes, ell):
    lengths = sorted(set(cuts(ell)))
    vertices = sum((visible(sizes, t) for t in lengths), ())
    actual = Counter()
    total = retained = rejected = 0
    repeats = 0
    for w in words(sizes, ell):
        if w[0][0] == w[-1][0]:
            continue
        total += 1
        bs = blocks(w)
        if any(b == inverse(b, sizes) for b in bs):
            rejected += 1
            continue
        retained += 1
        incidence = Counter()
        edges = []
        for i in range(3):
            x, y = inverse(bs[i], sizes), bs[(i+1) % 3]
            require(x != y, 'exact_no_link_loops')
            actual[x, y] += 1
            actual[y, x] += 1
            incidence[x] += 1
            incidence[y] += 1
            edges.append(frozenset((x, y)))
        require(max(incidence.values()) <= 3, 'exact_whole_relator_degree_bound')
        if len(set(edges)) < 3:
            repeats += 1
    c = Counter()
    for i in range(3):
        t, u = cuts(ell)[i], cuts(ell)[(i+1) % 3]
        c[t, u] += 1
        c[u, t] += 1
    explicit = ([[6]], [[2, 2], [2, 0]], [[0, 2], [2, 2]])[ell % 3]
    require([[c[t,u] for u in lengths] for t in lengths] == explicit,
            'exact_type_matrix')
    completion = {}
    for t in lengths:
        for u in lengths:
            if c[t,u]:
                h = ell-t-u
                for p in range(len(sizes)):
                    for q in range(len(sizes)):
                        completion[t,u,p,q] = sum(w[0][0] != p and w[-1][0] != q
                                                  for w in visible(sizes,h))
    for x in vertices:
        for y in vertices:
            t, u = len(x), len(y)
            expected = 0
            if c[t,u] and x[0][0] != y[0][0]:
                expected = c[t,u]*completion[t,u,x[-1][0],y[-1][0]]
            require(actual[x,y] == expected, 'exact_rooted_word_kernel')
    require(sum(actual.values()) == 6*retained, 'exact_total_corner_mass')
    samples.append({'sizes': sizes, 'ell': ell, 'cyclic_words': total,
                    'retained': retained, 'rejected': rejected,
                    'signed_vertices': len(vertices), 'repeated_edge_samples': repeats})
    return vertices, actual, total

def multiply_free_product(left, right, sizes):
    stack = list(left)
    for i, a in right:
        if stack and stack[-1][0] == i:
            value = (stack.pop()[1]+a) % (sizes[i]+1)
            if value:
                stack.append((i,value))
        else:
            stack.append((i,a))
    return tuple(stack)

def suffix_checks(sizes):
    abc = alphabet(sizes)
    for length in range(4,18):
        for a,b in product(abc, repeat=2):
            C = next(i for i in range(len(sizes)) if i not in (a[0],b[0]))
            others = [i for i in range(len(sizes)) if i != C]
            if length % 2 == 0:
                sequence = ([C,others[0]]*((length+1)//2))[:length-1]
            else:
                sequence = [C,others[0],others[1],C]+[others[0],C]*((length-5)//2)
            suffix = tuple((i,1) for i in sequence)
            x = (a,)+suffix
            y = inverse((b,),sizes)+suffix
            require(len(x) == length and len(y) == length, 'exact_suffix_length')
            require(all(w[j][0] != w[j+1][0] for w in (x,y)
                        for j in range(length-1)), 'exact_suffix_reduced')
            require(x != inverse(x,sizes) and y != inverse(y,sizes),
                    'exact_suffix_not_inverse_fixed')
            lhs = multiply_free_product(x,inverse(y,sizes),sizes)
            rhs = multiply_free_product((a,),(b,),sizes)
            require(lhs == rhs, 'exact_suffix_two_letter_identity')

def matmul(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def matpow(a,n):
    out = [[int(i==j) for j in range(len(a))] for i in range(len(a))]
    while n:
        if n & 1: out = matmul(out,a)
        a = matmul(a,a)
        n //= 2
    return out

def factor_visible(sizes,t):
    n = len(sizes)
    a = [[0 if i == j else sizes[j] for j in range(n)] for i in range(n)]
    power = matpow(a,t-1)
    v = [[sizes[i]*power[i][j] for j in range(n)] for i in range(n)]
    # All nonidentity elements of C_(size+1): one involution iff size is odd.
    fixed = [int(s % 2 == 1) for s in sizes]
    if t == 1:
        for i in range(n): v[i][i] -= fixed[i]
    elif t % 2:
        prefix = matpow(a,(t-3)//2)
        for i in range(n):
            removed = sum(sizes[i]*prefix[i][j]*(sum(fixed)-fixed[j]) for j in range(n))
            v[i][i] -= removed
    return v

def exact_factor_compression(sizes,ell):
    n = len(sizes)
    lengths = sorted(set(cuts(ell)))
    c = Counter()
    for i in range(3):
        t,u = cuts(ell)[i],cuts(ell)[(i+1)%3]
        c[t,u] += 1; c[u,t] += 1
    v = {t:factor_visible(sizes,t) for t in lengths}
    labels = [(t,a,b) for t in lengths for a in range(n) for b in range(n) if v[t][a][b]]
    completions = {}
    for t,u in c:
        h = ell-t-u
        vh = factor_visible(sizes,h)
        completions[t,u] = [[sum(vh[i][j] for i in range(n) for j in range(n)
                                      if i != p and j != q) for q in range(n)] for p in range(n)]
    kernel = [[c[t,u]*int(a!=cc)*completions[t,u][b][f] if c[t,u] else 0
                for u,cc,f in labels] for t,a,b in labels]
    counts = [v[t][a][b] for t,a,b in labels]
    degrees = [sum(k*x for k,x in zip(row,counts)) for row in kernel]
    require(all(degrees), 'exact_compressed_positive_degrees')
    sym = np.array([[kernel[i][j]*math.sqrt(counts[i]/degrees[i])*math.sqrt(counts[j]/degrees[j])
                     for j in range(len(labels))] for i in range(len(labels))])
    require(np.max(np.abs(sym-sym.T)) < 1e-12, 'numeric_compressed_reversibility')
    eig = np.linalg.eigvalsh(sym)
    require(abs(eig[-1]-1) < 1e-10, 'numeric_compressed_principal_eigenvalue')
    return 1-max(0,float(eig[-2]))

def probability_and_minmax_control(sizes,ell):
    vertices,adj,total = direct_link(sizes,ell)
    index = {v:i for i,v in enumerate(vertices)}
    M = len(vertices)
    mean_adj = np.zeros((M,M))
    for (x,y),v in adj.items(): mean_adj[index[x],index[y]] = v/total
    pool = [w for w in words(sizes,ell) if w[0][0] != w[-1][0]]
    rng = random.Random(23390181+ell)
    N = 5000
    actual = np.zeros((M,M))
    for _ in range(N):
        bs = blocks(rng.choice(pool))
        if any(w == inverse(w,sizes) for w in bs): continue
        for i in range(3):
            a,b = index[inverse(bs[i],sizes)],index[bs[(i+1)%3]]
            actual[a,b] += 1; actual[b,a] += 1
    barD = N*mean_adj.sum(axis=1)
    D = actual.sum(axis=1)
    require(bool(np.min(D)>0), 'numeric_sample_positive_degree')
    lap = np.diag(D)-actual
    norm_mean = lap/np.sqrt(np.outer(barD,barD))
    norm_actual = lap/np.sqrt(np.outer(D,D))
    alpha = float(np.linalg.eigvalsh(norm_mean)[1])
    gap = float(np.linalg.eigvalsh(norm_actual)[1])
    beta = float(max(D/barD))
    require(gap+1e-10 >= alpha/beta, 'numeric_wrong_center_minmax_control')
    z = np.sqrt(barD)
    require(np.max(np.abs(norm_mean@z)) < 1e-9, 'numeric_common_deterministic_kernel')
    samples.append({'minmax_ell':ell,'draws':N,'mean_center_minimum':alpha,
                    'degree_ratio':beta,'actual_gap':gap,'certified_comparison':alpha/beta})

def main():
    cases = [((1,1,1),range(6,12)),((2,1,1),range(6,10)),
             ((2,2,2),range(6,9)),((1,2,3),range(6,9)),((1,1,1,1),range(6,10))]
    for sizes,lengths in cases:
        for ell in lengths: direct_link(sizes,ell)
        suffix_checks(sizes)
        for t in range(1,8):
            observed = Counter((w[0][0],w[-1][0]) for w in visible(sizes,t))
            v = factor_visible(sizes,t)
            for i,j in product(range(len(sizes)),repeat=2):
                require(v[i][j] == observed[i,j], 'exact_inverse_fixed_deletion_formula')
    for sizes in [(1,1,1),(1,2,5),(1,1,15),(1,1,40)]:
        part = np.array([[0 if i==j else math.sqrt(a*b) for j,b in enumerate(sizes)]
                         for i,a in enumerate(sizes)])
        ev = np.linalg.eigvalsh(part)
        rho = float(-ev[0]/ev[-1])
        gamma = (3-rho)/4
        for e in range(3):
            results = []
            for L in [4,8,16,32,64,128]:
                gap = exact_factor_compression(sizes,3*L+e)
                results.append({'L':L,'gap':gap})
            target = 1 if e==0 else 1-rho/2
            require(results[-1]['gap'] > gamma, 'numeric_eventual_mean_gap_margin')
            require(abs(results[-1]['gap']-target) < 1e-4, 'numeric_tensor_limit')
            samples.append({'spectral_sizes':sizes,'residue':e,'rho':rho,
                            'eventual_gamma':gamma,'target_gap':target,'finite_gaps':results})
    for ell in (12,13,14): probability_and_minmax_control((1,1,1),ell)
    # Explicit boundaries: the excluded two-factor tensor has eigenvalue 1/2;
    # inverse-fixed blocks exist with torsion; density equality has no growth.
    P = np.array([[0.,1.],[1.,0.]])
    Q = np.array([[.5,.5],[1.,0.]])
    eigen = np.sort(np.linalg.eigvals(np.kron(Q,P)).real)
    require(abs(eigen[-2]-.5) < 1e-12, 'negative_control_two_factor_strict_gap')
    w = ((0,1),(1,1),(0,1))
    require(w == inverse(w,(1,1,1)), 'negative_control_inverse_fixed_block')
    require(all(ell/3-math.ceil(ell/3)<=0 for ell in range(3,301)),
            'negative_control_critical_density_growth')
    require(any(s.get('rejected',0)>0 for s in samples), 'rejection_cases_exercised')
    require(any(s.get('repeated_edge_samples',0)>0 for s in samples), 'multiplicity_cases_exercised')
    result = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
              'assertions':sum(checks.values()),'families':dict(checks),'samples':samples,
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'numpy_version':np.__version__,
              'scope':'Exact independent finite enumeration and cyclic-factor normal forms; floating spectral/min-max diagnostics explicitly labelled numeric. No supplied checker imports, no asymptotic, property (T), priority or formal proof certification.'}
    Path(__file__).with_name('independent_controls_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'assertions':result['assertions'],'families':len(checks)}))

if __name__ == '__main__': main()

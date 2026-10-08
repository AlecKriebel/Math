#!/usr/bin/env python3
"""Independent exact controls, written without importing the author's algorithms.
The optional candidate file is loaded only to cross-check its public functions.
No filesystem writes, dependencies, or network calls.
"""
import argparse
from collections import Counter
from fractions import Fraction
from functools import reduce
from itertools import combinations, combinations_with_replacement, permutations, product
from math import gcd
import json
import runpy

class AuditFailure(Exception):
    pass

def need(test, label):
    if not test:
        raise AuditFailure(label)

LABELS = tuple(combinations(range(1, 7), 3))
PAIRS = tuple(product(range(1, 4), repeat=2))
HEX = ((0, 0, 0, 0, 0, 0), (18, 3, 15, 6, 9, 12), (42, 35, 28, 21, 14, 7))

def exp(order):
    a = [0] * 18
    for row, col in enumerate(order):
        a[row * 6 + col - 1] = 1
    return tuple(a)

def order(label, ell):
    low, high = [x for x in label if x <= ell], [x for x in label if x > ell]
    return (high[0], low[0], high[1]) if len(low) == 1 else label

def sumvec(*vectors):
    return tuple(map(sum, zip(*vectors)))

def packed_hilbert(vectors):
    # Every exponent is <= 4; base 8 prevents carries between variable slots.
    packed = [sum(x << (3*i) for i, x in enumerate(v)) for v in vectors]
    return [len({sum(choice) for choice in combinations_with_replacement(packed, d)}) for d in range(5)]

def exact_rank(rows):
    # Fraction-free row echelon, with primitive integer rows, no rational RREF.
    basis = {}
    for row in rows:
        v = list(row)
        for p, b in sorted(basis.items()):
            if v[p]:
                lead = v[p]
                v = [b[p]*x - lead*y for x, y in zip(v, b)]
                g = reduce(gcd, map(abs, v), 0)
                if g: v = [x//g for x in v]
        nz = next((i for i, x in enumerate(v) if x), None)
        if nz is not None:
            g = reduce(gcd, map(abs, v), 0)
            v = [x//g for x in v]
            if v[nz] < 0: v = [-x for x in v]
            basis[nz] = v
    return len(basis)

def transpose(columns):
    return list(zip(*columns))

def leading(label, weights):
    winners = Counter()
    for rows in permutations(label):
        winners[rows] = sum(weights[i][j-1] for i, j in enumerate(rows))
    m = min(winners.values())
    smallest = [k for k, v in winners.items() if v == m]
    need(len(smallest) == 1, 'coherence nonunique')
    return smallest[0], sorted(winners.values())[1] - m

def rect(label):
    widths = tuple(4+i-j for i, j in enumerate(label))
    result = []
    for r, c in PAIRS:
        counts = Counter()
        for i in range(r):
            for j in range(c):
                if j >= widths[i]: counts[j-i] += 1
        result.append(max(counts.values(), default=0))
    return tuple(result)

def tropical(v, use_max):
    out = list(v)
    options = (v[1] + v[3], v[4])
    out[0] = (max(options) if use_max else min(options)) - v[0]
    return tuple(out)

def polynomial_minor(cols, first_row=0):
    # Laplace expansion, sorted tuples of variable indices encode monomials.
    if not cols: return {(): 1}
    result = Counter()
    for i, col in enumerate(cols):
        for mon, coeff in polynomial_minor(cols[:i]+cols[i+1:], first_row+1).items():
            result[tuple(sorted((6*first_row+col-1,)+mon))] += (-1)**i*coeff
    return {m:c for m,c in result.items() if c}

def polymul(a,b):
    out = Counter()
    for am, ac in a.items():
        for bm, bc in b.items(): out[tuple(sorted(am+bm))] += ac*bc
    return {m:c for m,c in out.items() if c}

def algebra_branches():
    t, A, B = (1,0,0), (0,1,0), (0,0,1)
    neg = lambda x: tuple(-q for q in x)
    sub = lambda x,y: sumvec(x,neg(y))
    epsilon = neg(t)
    checks = 0
    for small, large in ((A,B),(B,A)):
        psi_min, psi_max = sumvec(epsilon, small), sumvec(epsilon, large)
        # Coefficients in t,A,B prove each identity on the entire closed chamber.
        need(sumvec(epsilon, small) == psi_min, 'min coefficients')
        need(sub(epsilon, neg(large)) == psi_max, 'max coefficients')
        need(sumvec(psi_max, sub(small, large)) == psi_min, 'difference coefficients')
        need(sumvec(sub(epsilon, small), A, B) == psi_max, 'correcting shear coefficients')
        need(sumvec(psi_max, small) == sumvec(epsilon, A, B), 'composed shear coefficients')
        need(sumvec(psi_max, neg(A), neg(B), small, small) == psi_min, 'squared shear coefficients')
        checks += 6
    return checks

def check(candidate=None):
    all_blocks = [[exp(order(I, ell)) for I in LABELS] for ell in range(7)]
    hilberts = [packed_hilbert(block) for block in all_blocks]
    need(all(h == [1,20,175,980,4116] for h in hilberts), 'block Hilbert counts')
    # Independent dimension control: enumerate semistandard tableaux of shape (d,d,d)
    # as weakly row-increasing sequences of strictly increasing column triples.
    sst_counts = []
    for d in range(5):
        count = 0
        for cols in combinations_with_replacement(LABELS, d):
            if all(all(a <= b for a,b in zip(cols[i], cols[i+1])) for i in range(d-1)):
                count += 1
        sst_counts.append(count)
    need(sst_counts == hilberts[0], 'tableau Hilbert dimensions')
    hex_orders, gaps = zip(*(leading(I,HEX) for I in LABELS))
    hex_counts = packed_hilbert([exp(a) for a in hex_orders])
    need(hex_counts == [1,20,174,968,4040], 'hex Hilbert counts')
    block_gaps = []
    for ell in range(7):
        weights = (tuple([0]*6), tuple(range(ell,0,-1))+tuple(range(6,ell,-1)), tuple(range(12,0,-2)))
        for I in LABELS:
            actual, gap = leading(I, weights)
            need(actual == order(I,ell), 'block coherence')
            block_gaps.append(gap)
    b0, b1 = [{I:e for I,e in zip(LABELS, block)} for block in all_blocks[:2]]
    rel = ((1,3,4),(2,4,5),(1,4,5),(2,3,4))
    delta = lambda b: sumvec(b[rel[0]],b[rel[1]],tuple(-x for x in b[rel[2]]),tuple(-x for x in b[rel[3]]))
    need(delta(b0) == (0,)*18, 'source additive relation')
    expected_delta = [0]*18
    for r,c,s in ((1,3,1),(1,4,-1),(2,4,1),(2,3,-1)): expected_delta[(r-1)*6+c-1]=s
    need(delta(b1) == tuple(expected_delta), 'target additive defect')
    ranks = [exact_rank(transpose(b)) for b in all_blocks]
    stacked = exact_rank(transpose(all_blocks[0])+transpose(all_blocks[1]))
    need(ranks == [10]*7 and stacked == 12, 'rank certificates')
    common = ranks[0]+ranks[1]-stacked
    need(common == 8 and common < 9, 'adjacency dimension')
    vals = {I:rect(I) for I in LABELS}
    need(len(set(vals.values())) == 20, 'distinct rectangle values')
    # Invert the diagonal-sum GT coordinate change. Enumerate all binary order filters.
    binary_patterns = [bits for bits in product((0,1), repeat=9)
        if all(bits[(r-1)*3+c-1] <= bits[(r-1)*3+c] for r in range(1,4) for c in range(1,3))
        and all(bits[(r-1)*3+c-1] <= bits[r*3+c-1] for r in range(1,3) for c in range(1,4))]
    gt_values = set()
    for bits in binary_patterns:
        gt_values.add(tuple(sum(bits[(r-j-1)*3+c-j-1] for j in range(min(r,c))) for r,c in PAIRS))
    need(set(vals.values()) == gt_values, 'rectangle GT coordinate identification')
    u, v = vals[(1,4,5)], vals[(3,5,6)]
    need(u == (0,0,0,0,1,1,0,1,2), 'first valuation')
    need(v == (0,1,1,1,1,2,1,2,2), 'second valuation')
    midpoint = tuple(Fraction(x+y,2) for x,y in zip(tropical(u,True), tropical(v,True)))
    inverse = tropical(midpoint, True)
    need(inverse[0] == Fraction(-1,2), 'nonconvex inverse separator')
    need(tropical(inverse,True)==midpoint and all(x[0]>=0 for x in vals.values()), 'nonconvex involution')
    poly = Counter()
    for factor, left, right in ((1,(3,5,6),(2,4,6)),(-1,(2,5,6),(3,4,6)),(-1,(2,3,6),(4,5,6))):
        for mon, coeff in polymul(polynomial_minor(left),polynomial_minor(right)).items(): poly[mon] += factor*coeff
    need(not any(poly.values()), 'independent Laplace exchange identity')
    branches = algebra_branches()
    compared = 0
    if candidate:
        c = runpy.run_path(str(candidate), run_name='independent_audit_candidate')
        for ell, block in enumerate(all_blocks):
            need([c['exponent'](c['block_order'](I,ell)) for I in LABELS] == block, 'candidate block exponents')
            need(c['hilbert_counts'](block) == hilberts[ell], 'candidate Hilbert')
            need(c['rank'](transpose(block)) == ranks[ell], 'candidate block ranks')
        need(c['rank'](transpose(all_blocks[0])+transpose(all_blocks[1]))==stacked, 'candidate stacked rank')
        need([c['leading_order'](I,HEX) for I in LABELS] == list(hex_orders), 'candidate coherent minima')
        need(c['hilbert_counts']([exp(x) for x in hex_orders])==hex_counts, 'candidate hex Hilbert')
        need({I:c['rectangle_valuation'](I) for I in LABELS}==vals, 'candidate rectangle rule')
        for t,A,B in product((Fraction(-5,3),Fraction(-1,2),Fraction(0),Fraction(2,7),Fraction(4)), repeat=3):
            x = (t,A,0,0,B,0,0,0,0)
            minval,maxval = tropical(x,False),tropical(x,True)
            need(c['mutate'](x,'min')==minval and c['mutate'](x,'max')==maxval,'candidate tropical maps')
            eps = (-x[0],)+x[1:]
            need(c['phi'](eps,-1,1)==minval and c['phi'](eps,1,-1)==maxval, 'candidate factor signs')
            need(c['difference_phi'](maxval)==minval, 'candidate difference factor')
            compared += 1
        c['plucker_identity']()
    return {'status':'PASS','scope':'Independent checks of five existing partial results, not a global solution',
       'ranks':ranks,'stacked_rank':stacked,'intersection_dimension':common,
       'block_hilbert':hilberts[0],'semistandard_tableau_dimensions':sst_counts,'hex_hilbert':hex_counts,
       'hex_minimum_uniqueness_gap':min(gaps),'block_minimum_uniqueness_gap':min(block_gaps),
       'target_relation_difference':list(expected_delta),'rectangle_GT_binary_patterns':len(binary_patterns),
       'max_image_midpoint':[str(x) for x in midpoint],'unique_inverse':[str(x) for x in inverse],
       'exchange_polynomial':'zero by independent recursive Laplace expansion',
       'universal_chamber_coefficient_identities':branches,'candidate_rational_comparisons':compared}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate')
    args = parser.parse_args()
    print(json.dumps(check(args.candidate), indent=2, sort_keys=True))

#!/usr/bin/env python3
"""Finite source-specialization checks; no novelty or universal-proof claim."""
import json
from math import comb

def need(condition, message):
    if not condition:
        raise ValueError(message)

def partitions(n, bound=None):
    if n == 0:
        yield ()
        return
    for a in range(min(n, n if bound is None else bound), 0, -1):
        for tail in partitions(n-a, a):
            yield (a,) + tail

def dominates(mu, lam):
    m = max(len(mu), len(lam))
    return all(sum(mu[:j]) >= sum(lam[:j]) for j in range(1, m+1))

def targets(d, j, p, upper):
    if upper:
        return {k for k in range(j+1) if comb(j, k) % p}
    return {j+k for k in range(d-j+1) if comb(d-j, k) % p}

def run():
    rows = []
    for p in (3, 5, 7, 11):
        r, d = 2*p-1, 2*p-3
        lam = (r-1, 1)
        higher = [x for x in partitions(r) if dominates(x, lam)]
        need(higher == [(r,), lam], 'Unexpected dominating labels')
        need(all(len(x) <= 2 for x in higher), 'Rank-two reduction lacks a highest weight')
        need(r % p != 0, 'Young-side simplicity premise fails')
        need(d == p + (p-3) and 0 <= p-3 <= p-2, 'Classical sequence parameters invalid')
        w = set(range(p-2)) | set(range(p, d+1))
        complement = set(range(d+1)) - w
        need(len(w) == 2*p-4 and len(complement) == 2, 'Incorrect dimensions')
        need(all(targets(d, j, p, upper) <= w for j in w for upper in (True, False)),
             'Proposed Frobenius subspace is not invariant')
        witnesses = [(j, upper, sorted(targets(d,j,p,upper)-complement))
                     for j in sorted(complement) for upper in (True,False)
                     if not targets(d,j,p,upper) <= complement]
        need(bool(witnesses), 'Coordinate weight complement unexpectedly invariant')
        need(all(comb(r,j) % p for j in range(r+1)), 'Simple symmetric-power coefficients vanish')
        rows.append({'p':p,'r':r,'lambda':lam,'dominating_labels':higher,
                     'costandard_dimension':d+1,'socle_dimension':len(w),'head_dimension':2,
                     'subspace_invariant_for_all_formal_unipotent_coefficients':True,
                     'weight_complement_noninvariance_witness':witnesses[0],
                     'all_simple_Sym_r_coefficients_nonzero':True})
    D = [[1,0,0],[0,1,1],[0,0,1]]
    nabla_dim = [6,4,2]
    simple_dim = [6,2,2]
    need([sum(a*b for a,b in zip(row,simple_dim)) for row in D] == nabla_dim,
         'Decomposition labels/dimensions inconsistent')
    projective_dim = [sum(D[j][i]*nabla_dim[j] for j in range(3)) for i in range(3)]
    need(projective_dim == [6,4,6], 'Reciprocity dimensions disagree')
    need(nabla_dim[1] != projective_dim[2], 'Tiny injective/projective-head obstruction lost')
    need((4,1) != (3,2), 'Rational highest weights confused')
    return {'status':'PASS','pr':786,'head':'34f21454986a28ca49f24999be3a0fd1b42755f8',
            'scope':'Finite checks of published-formula specializations and dominance. These computations are not a universal all-prime proof, a literature search, or novelty evidence.',
            'tested_primes':rows,'p3_labels':[[5],[4,1],[3,2]],'p3_costandard_decomposition':D,
            'p3_costandard_dimensions':nabla_dim,'p3_simple_dimensions':simple_dim,
            'p3_projective_dimensions':projective_dim,
            'p3_I_4_1_dimension':4,'p3_I_4_1_head_label':[3,2],
            'p3_P_3_2_dimension':6,
            'all_rank_deduction_dependency':'Analytic labelled truncation and tilting facts, DD2005; not finite-rank extrapolation.'}

if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))

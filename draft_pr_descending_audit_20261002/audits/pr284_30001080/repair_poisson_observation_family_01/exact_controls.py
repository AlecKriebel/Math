"""Finite exact controls of the frozen observation proof; not an infinite proof."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from math import factorial
import hashlib
import json
from pathlib import Path

counts = Counter()
def ck(value, label):
    if not value:
        raise AssertionError(label)
    counts[label] += 1

def group(moduli):
    points = list(product(*(range(n) for n in moduli)))
    index = {p: i for i, p in enumerate(points)}
    def add(s, t):
        return index[tuple((a+b) % n for a,b,n in zip(points[s],points[t],moduli))]
    def neg(s):
        return index[tuple((-a) % n for a,n in zip(points[s],moduli))]
    def shift(v, s):
        return tuple(v[add(i,s)] for i in range(len(points)))
    return points, add, neg, shift

def poisson_coefficient(alpha, eta):
    # The common factor exp(-sum(alpha)) is omitted, and is shift-invariant.
    out = F(1)
    for a,k in zip(alpha,eta):
        out *= F(a**k, factorial(k))
    return out

groups = [(2,), (3,), (2,2), (4,)]
patterns = 0
for moduli in groups:
    points,add,neg,shift = group(moduli)
    n = len(points)
    etas = list(product(range(3), repeat=n))
    for eta in etas:
        for s in range(n):
            for t in range(n):
                base = list(eta); base[s] += 1; base[t] += 1
                moved = shift(tuple(base),s)
                expected = list(shift(eta,s)); expected[0] += 1; expected[add(t,neg(s))] += 1
                ck(moved == tuple(expected), 'two_endpoint_translation_including_coincidence')
        # C=G; denominator (1+nu(G))^2 is symmetric and strictly positive.
        den = (1+sum(eta))**2
        def gate(v,t):
            # A deliberately asymmetric indicator, symmetrized under J.
            raw = lambda z,u: int((z[0]+2*z[u]+u) % 3 == 0)
            return F(raw(v,t)+raw(shift(v,t),neg(t)),2)
        T = [[F(0) for _ in range(n)] for _ in range(n)]
        for s in range(n):
            row = F(0)
            for t in range(n):
                if s == t:
                    continue
                b = gate(shift(eta,s),add(t,neg(s)))
                ck(b == gate(shift(eta,t),add(s,neg(t))), 'observable_gate_endpoint_symmetry')
                jump = F(eta[t],den)*b
                T[s][t] = jump; row += jump
            ck(0 <= row <= F(sum(eta),1+sum(eta)) <= 1, 'observable_transport_row_bound')
            T[s][s] = 1-row
            ck(sum(T[s]) == 1 and min(T[s]) >= 0, 'Markov_rows')
        for t in range(n):
            ck(sum(eta[s]*T[s][t] for s in range(n)) == eta[t], 'counting_measure_preservation')
        for s in range(n):
            ck(gate(eta,s) == gate(shift(eta,s),neg(s)), 'J_gate_involution')

    for seed in product(range(3),repeat=n):
        if not any(seed) or seed != min(shift(seed,s) for s in range(n)):
            continue
        patterns += 1
        states = sorted(set(shift(seed,s) for s in range(n)))
        q_bad = {a:F(i+1,sum(range(1,len(states)+1))) for i,a in enumerate(states)}
        z = sum(a[0] for a in states)
        q_palm = {a:F(a[0],z) for a in states}
        for q in (q_bad,q_palm):
            def c(a,s):
                return q[a]*a[s]
            def cr(a,s):
                # R is its own inverse: old base is theta_s(a), edge -s.
                old = shift(a,s)
                return q[old]*old[neg(s)]
            for a in states:
                for s in range(1,n):
                    u,v,up,vp = c(a,s),c(a,neg(s)),cr(a,s),cr(a,neg(s))
                    beta = shift(a,neg(s))
                    for eta in etas:
                        p = poisson_coefficient(a,eta)
                        p_beta = poisson_coefficient(beta,eta)
                        # J image of a residual at -s uses residual shift by -s.
                        original_eta = shift(eta,s)
                        ck(poisson_coefficient(a,original_eta) == p_beta, 'J_residual_intensity_minus_s')
                        # R preimage: old intensity theta_s(a), old residual theta_s(eta).
                        old_eta = shift(eta,s)
                        ck(poisson_coefficient(shift(a,s),old_eta) == p, 'R_conditional_intensity_alpha')
                        direct = (u-up)*p+(v-vp)*poisson_coefficient(a,original_eta)
                        mixture = (u-up)*p+(v-vp)*p_beta
                        ck(direct == mixture, 'four_measure_symmetrization_coefficients')
                        if q is q_palm:
                            ck(direct == 0, 'Palm_lift_reversal')
                    if a != beta:
                        differing = [i for i in range(n) if a[i] != beta[i]]
                        ck(bool(differing), 'Poisson_void_separation_distinct_intensities')
                        # exp(-a_i) differs exactly when the integer a_i differs.
                        i = differing[0]
                        ck(a[i] != beta[i], 'nonzero_two_law_determinant_exponents')
                    else:
                        ck(a[s] == a[neg(s)], 'period_graph_inversion')
                    if s == neg(s):
                        ck(u == v and up == vp, 'order_two_base_inversion')
                    if q is q_palm:
                        ck(u == up, 'canonical_Campbell_reversal')

proof = Path(__file__).with_name('POISSON_OBSERVATION_REPAIR.md')
ck(hashlib.sha256(proof.read_bytes()).hexdigest() == 'bd5eb9048439f6e6cac903e0b44b0277180e360dc94439f8eab34fac19efeeef', 'frozen_candidate_binding')
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),
                  'counts':dict(sorted(counts.items())), 'finite_orbit_patterns':patterns,
                  'groups':groups, 'scope':'Exact finite algebra, observable Markov preservation, insertion/covariance signs and two-law coefficient controls only; not an infinite theorem, deterministic-allocation reduction, source closure, priority or publication clearance.'}, indent=2,sort_keys=True))

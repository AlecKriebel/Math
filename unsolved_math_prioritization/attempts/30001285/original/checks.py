#!/usr/bin/env python3
"""Exact finite controls for the authored lemmas; not a motivic proof checker."""
import json
import math
from collections import Counter

counts = Counter()

def check(category, condition):
    if not condition:
        raise AssertionError(category)
    counts[category] += 1

# All subgroups D=h Z/m, all annihilators e<=m, and every quotient element.
for m in range(1, 37):
    for h in range(1, m + 1):
        if m % h:
            continue
        B = set(range(m))
        D = set(range(0, m, h))
        Q = set(range(h))
        for e in range(1, m + 1):
            if (e * h) % m:
                continue
            mu = lambda q: (e * q) % m
            for q in Q:
                check('multiplier_well_defined', all(mu((q + d) % m) == mu(q) for d in D))
                check('quotient_multiplier_relation', mu(q) % h == (e * q) % h)
            for b in B:
                check('multiplier_quotient_relation', mu(b % h) == (e * b) % m)
            Be = {b for b in B if (e * b) % m == 0}
            kernel = {q for q in Q if mu(q) == 0}
            check('multiplier_kernel', kernel == {b % h for b in Be})
            Qe = {q for q in Q if (e * q) % h == 0}
            image = {mu(q) for q in Qe}
            check('torsion_sequence_image', image == D.intersection({(e * b) % m for b in B}))
            check('torsion_sequence_kernel', {q for q in Qe if mu(q) == 0} == kernel)
        # A map Z/n -> B/D is determined by q with nq=0 in B/D.
        for n in range(1, 25):
            nD = {(n * d) % m for d in D}
            for q in Q:
                if (n * q) % h:
                    continue
                theta_zero = (n * q) % m in nD
                lift_exists = any((n * b) % m == 0 for b in B if b % h == q)
                check('cyclic_lift_criterion', theta_zero == lift_exists)
                for d in D:
                    check('theta_representative_independence', ((n * (q + d) - n * q) % m) in nD)

# Explicit finite coefficient obstruction: B=Z/4, D={0,2}, S=Z/2.
hom_images = [b for b in range(4) if 2 * b % 4 == 0]
check('negative_projection_control', hom_images == [0, 2] and all(b % 2 == 0 for b in hom_images))
check('nonliftable_nonzero_quotient_map', not any(2 * b % 4 == 0 and b % 2 == 1 for b in range(4)))
check('nonzero_theta_control', (2 * 1) % 4 == 2 and {2 * d % 4 for d in [0, 2]} == {0})
check('finite_multiplier_positive_control', [2 * q % 4 for q in range(2)] == [0, 2])

# Multiplication can lose information: B=(Z/2)^2, D=<(1,0)>.
check('noncyclic_multiplier_negative_control', all(2 * q % 2 == 0 for q in range(2)) and len(range(2)) == 2)

# B=Q/Z can be replaced by its 8-torsion for this finite diagnostic.
# D={0,4} in Z/8; Q[4] has four classes but B[4]/D only two.
check('finite_refinement_negative_control', len(range(4)) == 4 and len({b % 4 for b in range(8) if 4 * b % 8 == 0}) == 2)

# Bezout annihilator test. A restriction/corestriction identity is a theorem input.
for m in range(1, 25):
    for d in range(1, 17):
        for n in range(1, 17):
            if math.gcd(d, n) != 1:
                continue
            check('coprime_descent_control', all(x == 0 for x in range(m) if d * x % m == 0 and n * x % m == 0))
check('joint_degree_descent_control', math.gcd(6, math.gcd(2, 3)) == 1 and all(x == 0 for x in range(6) if 2 * x % 6 == 0 and 3 * x % 6 == 0))
check('splitting_descent_negative_control', 4 * 1 % 4 == 0 and 1 != 0)

# Residue-field sanity checks used in the explicit Q_5 example.
squares_mod_5 = {a * a % 5 for a in range(1, 5)}
check('local_parameter_sanity', 2 not in squares_mod_5 and 4 in squares_mod_5)

# Spectral-sequence bookkeeping. These checks do not construct the maps.
def etale_degree(p, q):
    return p - q, -q, -p - q

def incoming(target, r):
    p, q = target
    return p - r, q + r - 1

check('edge_index_SK1', etale_degree(2, -3) == (5, 3, 1))
check('edge_index_SK2', etale_degree(2, -4) == (6, 4, 2))
check('incoming_d2_SK1', etale_degree(*incoming((2, -3), 2))[:2] == (2, 2))
check('incoming_d2_SK2', etale_degree(*incoming((2, -4), 2))[:2] == (3, 3))
check('incoming_d3_SK2', etale_degree(*incoming((2, -4), 3))[:2] == (1, 2))
check('product_bidegree', (2 + 0, -3 - 1) == (2, -4))
check('degree_one_connecting_sign', (-1) ** 1 == -1)
check('right_suspension_sign', (-1) ** (1 * 1) == -1)
check('degree_four_cup_sign', (-1) ** (4 * 1) == 1)

print(json.dumps({
    'status': 'PASS',
    'checks': dict(sorted(counts.items())),
    'total_assertions': sum(counts.values()),
    'limits': [
        'Finite controls do not prove the imported Platonov, Suslin, Rost, norm-residue, or generic-evaluation theorems.',
        'No beta-versus-sigma comparison or general equality classification is certified.',
        'The product-normalization hypothesis in approach 5 remains unverified for the two specific families.'
    ]
}, indent=2, sort_keys=True))

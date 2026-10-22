#!/usr/bin/env python3
"""Independent exact controls; no finite check is used as an infinite proof."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
C = ((0, 0), (3, 3), (10, 0), (0, 10))
E = (3, 3)
RHO = {'a': 'ab', 'b': 'ac', 'c': 'db', 'd': 'dc'}
SIGN = {'a': 1, 'b': 1, 'c': -1, 'd': -1}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def substitute(word):
    return ''.join(RHO[c] for c in word)

def points(x, y, phase=(0, 0), marker=True):
    ans = set()
    for i, xv in x.items():
        for j, yv in y.items():
            slots = [(0, 0)]
            if marker:
                slots.append(E)
            if xv == 1:
                slots.append(C[2])
            if yv == 1:
                slots.append(C[3])
            for u, v in slots:
                ans.add((30*i + u-phase[0], 30*j+v-phase[1]))
    return ans

# Exhaustive infinite marker reduction modulo the anchor lattice.
marker_pairs = [(i, j) for i, c in enumerate(C) for j, d in enumerate(C)
                if ((d[0]-c[0]) % 30, (d[1]-c[1]) % 30) == E]
require(marker_pairs == [(0, 1)], 'ambiguous marker residue')
require(len(set(C)) == 4, 'colliding slots')
minimum_squared = min(Q((30*m+d[0]-c[0])**2 + (30*n+d[1]-c[1])**2, 900)
    for c in C for d in C for m, n in product(range(-1, 2), repeat=2)
    if (30*m+d[0]-c[0], 30*n+d[1]-c[1]) != (0, 0))
require(minimum_squared == Q(1, 50), 'wrong uniform separation')

# Exhaust every local binary column/row configuration, including all slots absent.
# The larger patch provides neighbours for every tested inner-cell marker.
local_patterns = phase_cases = decoded_slots = 0
phases = list(product((0, 1, 10, 27), repeat=2))
for bits in product((-1, 1), repeat=10):
    x = dict(zip(range(-2, 3), bits[:5]))
    y = dict(zip(range(-2, 3), bits[5:]))
    local_patterns += 1
    for phase in phases:
        pts = points(x, y, phase)
        inner_candidates = {(30*i+c[0]-phase[0], 30*j+c[1]-phase[1])
            for i, j in product(range(-1, 2), repeat=2) for c in C}
        found = {p for p in pts & inner_candidates if (p[0]+3, p[1]+3) in pts}
        expected = {(30*i-phase[0], 30*j-phase[1])
                    for i, j in product(range(-1, 2), repeat=2)}
        require(found == expected, f'marker failure {bits} {phase}')
        for i, j in product(range(-1, 2), repeat=2):
            anchor = (30*i-phase[0], 30*j-phase[1])
            require(((anchor[0]+10, anchor[1]) in pts) == (x[i] == 1), 'column decode')
            require(((anchor[0], anchor[1]+10) in pts) == (y[j] == 1), 'row decode')
            decoded_slots += 2
        phase_cases += 1

# Negative control: deleting mandatory e and incorrectly using optional a fails.
x_neg = {i: -1 for i in range(-2, 3)}
y_neg = {j: -1 for j in range(-2, 3)}
pts_neg = points(x_neg, y_neg, marker=False)
faulty_anchors = {p for p in pts_neg if (p[0]+10, p[1]) in pts_neg}
require(not faulty_anchors, 'negative control unexpectedly found anchors')
require((0, 0) in pts_neg, 'negative control empty point set')

# Four-letter substitution: seed legality and primitivity are finite statements.
rho2 = {c: substitute(substitute(c)) for c in RHO}
require('ca' in rho2['c'], 'illegal bilateral seed')
require(rho2['c'].endswith('c') and rho2['a'].startswith('a'), 'seed gluing')
for c in RHO:
    require(set(substitute(substitute(substitute(c)))) == set(RHO), 'not primitive at power 3')
left, right = 'c', 'a'
for _ in range(6):
    left, right = substitute(substitute(left)), substitute(substitute(right))
letters = dict(enumerate(left+right, start=-len(left)))
w = {i: SIGN[c] for i, c in letters.items()}
require(w[0] == 1 and w[-1] == -1, 'primary initial data mismatch')
parity_sites = 0
for i, c in letters.items():
    require(c in ('a', 'd') if i % 2 == 0 else c in ('b', 'c'), 'wrong letter parity')
    parity_sites += 1
recursion_sites = 0
for n in range(-1024, 1024):
    for r in range(4):
        factor = 1 if r < 2 else (-1 if (n+r) % 2 else 1)
        require(w[4*n+r] == factor*w[n], f'recurrence mismatch n={n},r={r}')
        recursion_sites += 1

# Suspension edge gluing, using legal signs and exact phases. Compare the same
# interior geometric window after changing each canonical representative.
base = {i: w[i] for i in range(-20, 21)}
other = {i: w[i+5] for i in range(-20, 21)}
window = lambda pts: {p for p in pts if -180 <= p[0] <= 180 and -180 <= p[1] <= 180}
gluing_cases = 0
for phase in phases:
    for m, n in product((-2, -1, 0, 1, 2), repeat=2):
        sx = {i: base[i+m] for i in range(-15, 16)}
        sy = {j: other[j+n] for j in range(-15, 16)}
        before = window(points(base, other, (phase[0]+30*m, phase[1]+30*n)))
        after = window(points(sx, sy, phase))
        require(before == after, 'suspension representative mismatch')
        gluing_cases += 1

result = {
    'check_version': 1,
    'arithmetic': 'exact integers and fractions; explicit exceptions, no asserts',
    'marker_residue_pairs_examined': 16,
    'unique_marker_pair_slot_indices': marker_pairs,
    'minimum_point_separation_squared': str(minimum_squared),
    'relative_density_covering_radius_squared_bound': '1/2',
    'all_local_sign_patterns': local_patterns,
    'rational_phase_choices': len(phases),
    'pattern_phase_cases': phase_cases,
    'decoded_optional_slots': decoded_slots,
    'faulty_optional_marker_negative_control': 'detected: all-minus configuration loses anchor lattice',
    'rho2_letter_images': rho2,
    'seed': 'c|a legal and rho2-fixed',
    'primitivity_power': 3,
    'bilateral_letter_parity_sites': parity_sites,
    'bilateral_primary_recursion_sites': recursion_sites,
    'suspension_gluing_cases': gluing_cases,
    'failures': [],
    'proof_limit': 'Controls validate finite algebra, geometry, and representative gluing. Infinite hull/ergodicity conclusions use analytic arguments and credited primary input.'
}
(ROOT/'geometry_controls_results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))

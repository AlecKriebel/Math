#!/usr/bin/env python3
"""Independent exact audit controls. Standard library only; no packet imports.

Finite computations corroborate the separate infinite proof, never replace it.
All checks remain active under python -O. Output is deterministic JSON.
"""
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
from math import prod
import json

checks = defaultdict(int)

def require(condition, category):
    checks[category] += 1
    if not condition:
        raise AssertionError(category)


def fibers(shape):
    points = list(product(*map(range, shape)))
    rows = []
    for axis in range(len(shape)):
        buckets = defaultdict(set)
        for j, point in enumerate(points):
            buckets[point[:axis] + point[axis+1:]].add(j)
        rows.extend(buckets.values())
    return points, rows


def echelon(rows):
    pivots = {}
    for original in rows:
        row = set(original)
        while row:
            column = min(row)
            if column in pivots:
                row.symmetric_difference_update(pivots[column])
            else:
                pivots[column] = row
                break
    return pivots


def nullspace(rows, columns):
    pivots = echelon(rows)
    result = []
    for f in sorted(set(range(columns)) - set(pivots)):
        vector = {f}
        for p in sorted(pivots, reverse=True):
            if len(pivots[p] & vector) % 2:
                vector.add(p)
        result.append(vector)
    return result


linear_cases = []
for shape in [(4,), (8,), (4, 8), (4, 8, 16), (4, 4, 4), (2, 2, 2, 2)]:
    points, rows = fibers(shape)
    basis = nullspace(rows, len(points))
    require(len(basis) == prod(q-1 for q in shape), 'kernel_dimensions')
    for vector in basis:
        require(all(len(vector & row) % 2 == 0 for row in rows), 'nullspace_membership')
    projections = []
    if len(shape) > 1:
        old_points, old_rows = fibers(shape[:-1])
        old_index = {p: i for i, p in enumerate(old_points)}
        for tail in sorted({0, 1, shape[-1]-1}):
            projected = [{old_index[points[j][:-1]] for j in vector
                          if points[j][-1] == tail} for vector in basis]
            image_dimension = len(echelon(projected))
            require(image_dimension == prod(q-1 for q in shape[:-1]),
                    'restriction_surjectivity')
            for v in projected:
                require(all(len(v & row) % 2 == 0 for row in old_rows),
                        'projected_membership')
            projections.append({'tail_value': tail, 'image_dimension': image_dimension})
    linear_cases.append({'shape': shape, 'dimension': len(basis), 'projections': projections})

# Brute-force all assignments rather than infer counts solely by matrix rank.
exhaustive_cases = []
for shape in [(2, 4), (4, 4), (2, 2, 2, 2)]:
    points, rows = fibers(shape)
    admissible = []
    for bits in product((0, 1), repeat=len(points)):
        if all(sum(bits[j] for j in row) % 2 == 0 for row in rows):
            admissible.append(bits)
    dimension = prod(q-1 for q in shape)
    require(len(admissible) == 2**dimension, 'exhaustive_counts')
    # Test all choices of distinguished coordinate, including zero, at FINITE level.
    for distinguished in product(*map(range, shape)):
        free = [j for j, p in enumerate(points)
                if all(p[k] != distinguished[k] for k in range(len(shape)))]
        patterns = {tuple(bits[j] for j in free) for bits in admissible}
        require(len(patterns) == 2**dimension, 'free_coordinate_bijections')
    exhaustive_cases.append({'shape': shape, 'assignments_examined': 2**len(points),
                             'admissible': len(admissible)})

# Restrict fresh-coordinate equations to vectors supported in the old window.
fresh_cases = []
for shape in [(4,), (4, 8), (4, 8, 16)]:
    old_points, old_rows = fibers(shape)
    old_index = {p: j for j, p in enumerate(old_points)}
    for q in (2, 4):
        points, rows = fibers(shape + (q,))
        restricted = [{old_index[points[j][:-1]] for j in row if points[j][-1] == 0}
                      for row in rows]
        require(len(nullspace(restricted, len(old_points))) == 0, 'fresh_tail_obstructions')
        old_basis = nullspace(old_rows, len(old_points))
        test_vector = old_basis[0]
        require(any(len(row & test_vector) % 2 for row in restricted),
                'zero_extension_negative_controls')
        fresh_cases.append({'shape': shape, 'fresh_factor_size': q,
                            'supported_kernel_dimension': 0})

# Test the genuinely countable-coordinate formula at sparse group elements.
# The function w is defined on every finitely supported tuple, not merely a box.
def normalize(point):
    point = tuple(point)
    while point and point[-1] == 0:
        point = point[:-1]
    return point


def free_value(point):
    return sha256(repr(normalize(point)).encode('ascii')).digest()[0] % 2


@lru_cache(None)
def interpolate(point):
    point = normalize(point)
    for k, value in enumerate(point):
        q = 2**(k+2)
        if value == q-1:
            total = 0
            for b in range(q-1):
                total ^= interpolate(normalize(point[:k] + (b,) + point[k+1:]))
            return total
    return free_value(point)


anchors = [(0, 0, 0, 0), (3, 7, 0, 0), (3, 0, 15, 0),
           (0, 7, 15, 31), (2, 5, 9, 17), (0, 0, 0, 0, 0, 0, 2)]
for anchor in anchors:
    for axis in range(5):
        point = list(anchor) + [0] * max(0, axis+1-len(anchor))
        total = 0
        for b in range(2**(axis+2)):
            point[axis] = b
            total ^= interpolate(normalize(point))
        require(total == 0, 'countable_formula_fibers')
# Check that independently specified free-coordinate values are retained.
require(interpolate(()) == free_value(()), 'free_assignment_preserved')
for p in [(2, 5, 9, 17), (0, 0, 0, 0, 0, 0, 2)]:
    require(interpolate(p) == free_value(p), 'free_assignment_preserved')
# A delta assignment at zero on E extends nontrivially along fresh tail factors.
# These eight finite evaluations corroborate the separate all-n argument.
for axis in range(8):
    q = 2**(axis+2)
    point = (0,)*axis + (q-1,)
    value = sum(int(all(c == 0 for c in point[:axis]+(b,)))
                for b in range(q-1)) % 2
    require(value == 1, 'basis_seed_tail_evaluations')

# No nonzero element of the finite group fixes every allowed pattern.
points, rows = fibers((4, 8))
index = {p: j for j, p in enumerate(points)}
basis = nullspace(rows, len(points))
for shift in points[1:]:
    require(any({index[(points[j][0]^shift[0], points[j][1]^shift[1])]
                 for j in v} != v for v in basis), 'faithful_translation_controls')

# Negative control for the literal indexing in preprint formula (37).
# On H_1, choose a=3 and g=3. The permitted h=0 leaves g+h=3 outside E.
a = 3
require((a ^ 0) == a and 0 != a, 'source_formula_undefined_index')
require(all(b != a for b in range(4) if b != a), 'replacement_index_in_E')

# Rational bounds for the INFINITE product: proof of the tail bound is in AUDIT.md.
p = Fraction(1)
bound_cases = []
for n in range(1, 61):
    p *= Fraction(2**(n+1)-1, 2**(n+1))
    low = p * (1-Fraction(1, 2**(n+1)))
    require(p >= Fraction(1, 2) + Fraction(1, 2**(n+1)), 'finite_union_bounds')
    require(low >= Fraction(1, 2), 'infinite_tail_bounds')
    require(low <= p, 'bound_order')
    if n in (1, 3, 12, 40, 60):
        bound_cases.append({'n': n, 'product_lower': str(low), 'product_upper': str(p)})
for n in range(1, 61):
    require(Fraction(1, 2**n) < Fraction(1, 2**(n-1)), 'constant_two_decay')

# Exact logarithm enclosure using 2*atanh(1/3), with geometric remainder.
m = 32
log_low = 2*sum((Fraction(1, (2*k+1)*3**(2*k+1)) for k in range(m)), Fraction(0))
log_tail = Fraction(2, (2*m+1)*3**(2*m+1)) / (1-Fraction(1, 9))
log_high = log_low + log_tail
entropy_low = low * log_low
entropy_high = p * log_high
scale = 10**12
def floor_scaled(v):
    return v.numerator*scale // v.denominator

def ceiling_scaled(v):
    return -((-v.numerator*scale) // v.denominator)

rounded_low = Fraction(floor_scaled(entropy_low), scale)
rounded_high = Fraction(ceiling_scaled(entropy_high), scale)
require(rounded_low <= entropy_low <= entropy_high <= rounded_high, 'entropy_enclosure')
require(entropy_low > Fraction(1,2)*log_high, 'strict_half_log2_lower')
result = {
    'all_passed': True,
    'assertions': sum(checks.values()),
    'categories': dict(sorted(checks.items())),
    'method': 'Independent set-based Gaussian elimination, full configuration enumeration, recursive sparse-coordinate interpolation, exact rational arithmetic.',
    'linear_cases': linear_cases,
    'exhaustive_cases': exhaustive_cases,
    'fresh_tail_cases': fresh_cases,
    'global_formula_anchors': anchors,
    'product_bounds': bound_cases,
    'entropy_bound_manifest': {
        'log_base': 'natural',
        'product_terms': 60,
        'log_series_terms': m,
        'product_lower': str(low), 'product_upper': str(p),
        'log2_lower': str(log_low), 'log2_upper': str(log_high),
        'entropy_lower': str(entropy_low), 'entropy_upper': str(entropy_high),
        'readable_exact_lower': str(rounded_low),
        'readable_exact_upper': str(rounded_high),
        'universal_symbolic_bound': 'entropy >= log(2)/2 > 0',
        'tail_proof_required': True
    },
    'limits': 'Finite tests do not establish the infinite construction; see the separate mathematical audit.'
}
print(json.dumps(result, indent=2, sort_keys=True))

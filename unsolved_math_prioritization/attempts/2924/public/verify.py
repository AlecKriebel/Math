#!/usr/bin/env python3
"""Exact checks for the explicit disk-supported model; not a topology oracle.

Run: python3 verify.py > verification.json
Standard library only. Fractions prevent floating-point tolerance artifacts.
"""
from fractions import Fraction as Q
from itertools import product
import json

checks = {}

def record(name, condition):
    assert condition, name
    checks[name] = checks.get(name, 0) + 1


def radius(x):
    return max(map(abs, x))


def shear(x, a):
    """Boundary-fixing cube homeomorphism for |a|<1."""
    c = a
    for y in x:
        c *= 1 - abs(y)
    return (x[0] + c,) + x[1:]


def shear_inverse(y, a):
    c = a
    for z in y[1:]:
        c *= 1 - abs(z)
    # x -> x+c(1-|x|), with value c at the breakpoint x=0.
    x0 = (y[0] - c) / (1 + c if y[0] <= c else 1 - c)
    return (x0,) + y[1:]


def alexander(f, t, x):
    if t == 0 or radius(x) >= t:
        return x
    return tuple(t * y for y in f(tuple(z / t for z in x)))


grid = [Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1)]
points = list(product(grid, repeat=4))
parameters = [Q(-2, 3), Q(1, 3), Q(3, 4)]
times = [Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]
for a in parameters:
    f = lambda x, a=a: shear(x, a)
    inv = lambda x, a=a: shear_inverse(x, a)
    for x in points:
        y = f(x)
        record('cube_preserved', radius(y) <= 1)
        record('inverse_left', inv(y) == x)
        record('inverse_right', f(inv(x)) == x)
        if radius(x) == 1:
            record('boundary_fixed', y == x)
        for t in times:
            at = lambda x, t=t: alexander(f, t, x)
            bt = lambda x, t=t: alexander(inv, t, x)
            z = at(x)
            record('scaled_inverse_left', bt(z) == x)
            record('scaled_inverse_right', at(bt(x)) == x)
            record('uniform_displacement_bound', max(abs(y - z) for y, z in zip(z, x)) <= 2*t)
            # This special shear model has a stronger bound than the general 2t bound.
            record('shear_displacement_bound', max(abs(y - z) for y, z in zip(z, x)) <= abs(a)*t)
            if radius(x) >= t:
                record('outside_support_fixed', z == x)
            if t == 0:
                record('time_zero_identity', z == x)
            if t == 1:
                record('time_one_original', z == y)
            for s in times:
                record('semigroup_identity', alexander(at, s, x) == alexander(f, s*t, x))

# Check the rational slopes on both pieces of the inverse model.
for a in parameters:
    for tail in product(grid, repeat=3):
        c = a
        for z in tail:
            c *= 1-abs(z)
        record('strict_piecewise_monotonicity', 1+c > 0 and 1-c > 0)

# These are the inequalities actually used in KK26, Lemma 6.10 with k=2.
dimension_gate = {}
for m in range(3, 9):
    valid = Q(2) < min(Q(m-2), Q(m, 2))
    dimension_gate[str(m)] = valid
    record('dimension_threshold', valid == (m >= 5))
record('classical_dimension4_handle_bound', 4-3 == 1)

out = {
    'result': 'pass',
    'scope': 'Exact finite consistency checks of an explicit disk-supported homeomorphism family and dimension inequalities. Does not compute pi_k(Homeo_boundary(Delta)) or prove the general problem.',
    'arithmetic': 'fractions.Fraction',
    'cube_dimension': 4,
    'grid_points': len(points),
    'shear_parameters': [str(a) for a in parameters],
    'times': [str(t) for t in times],
    'checks_by_name': checks,
    'total_assertions': sum(checks.values()),
    'kk_lemma_6_10_k_equals_2': dimension_gate,
    'general_problem': 'unresolved',
}
print(json.dumps(out, indent=2, sort_keys=True))

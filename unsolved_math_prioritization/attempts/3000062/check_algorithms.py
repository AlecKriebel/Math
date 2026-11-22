"""Exact small-instance checks; no numerical optimization or external dependencies."""
from fractions import Fraction as Q
from itertools import product
import json

def F(x, arcs):
    y = [0] * len(x)
    for u, v, w in arcs:
        y[v] = max(y[v], w - x[u])
    return tuple(y)

def good(x, A):
    return F(x, A) == tuple(x)

def R(t):
    return round(t)
checks = {}
A = [(1, 0, 2), (1, 2, 4), (2, 1, 4)]
l = (0, 0, 0)
u = F(l, A)
m = tuple((Q(a + b, 2) for a, b in zip(l, u)))
if not (F(u, A) == l and (not good(m, A))):
    raise AssertionError('verification failed')
checks['midpoint'] = {'arcs': A, 'lower': l, 'upper': u, 'midpoint': list(map(str, m)), 'F_midpoint': list(map(str, F(m, A)))}
A = [(0, 1, 2), (0, 2, 2)]
feas = [x for x in product(range(3), repeat=3) if all((x[a] + x[b] >= w for a, b, w in A))]
opt = min(map(sum, feas))
opts = [x for x in feas if sum(x) == opt]
if not (opts == [(2, 0, 0)] and (not good(opts[0], A))):
    raise AssertionError('verification failed')
checks['minimum_sum'] = {'arcs': A, 'unique_optimum': opts[0], 'valid_cover': (0, 2, 2)}
pairs = [(u, v) for u in range(3) for v in range(3) if u != v]
identity_count = 0
for W in range(0, 13, 2):
    for k in range(-32, 65):
        t = Q(k, 4)
        if not R(W - t) == W - R(t):
            raise AssertionError('verification failed')
        identity_count += 1
fp_count = 0
for ws in product((None, 2, 4), repeat=6):
    A = [(u, v, w) for (u, v), w in zip(pairs, ws) if w is not None]
    for nums in product(range(9), repeat=3):
        x = tuple((Q(k, 2) for k in nums))
        if good(x, A):
            if not good(tuple((R(z) for z in x)), A):
                raise AssertionError('verification failed')
            fp_count += 1
checks['rounding'] = {'scalar_identity_checks': identity_count, 'graphs': 3 ** 6, 'half_grid_fixed_points_checked': fp_count}
print(json.dumps(checks, indent=2))

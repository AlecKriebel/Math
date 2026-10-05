"""Exact finite controls for the independent historical priority comparison."""
from fractions import Fraction
from itertools import product
import json


def mtp2_failures(p):
    result = []
    for x, y in product(p, repeat=2):
        meet = tuple(min(a, b) for a, b in zip(x, y))
        join = tuple(max(a, b) for a, b in zip(x, y))
        if p[x] * p[y] > p[meet] * p[join]:
            result.append([list(x), list(y)])
    return result


cube2 = list(product(range(2), repeat=2))
psi = {(0, 0): 1, (0, 1): 1, (1, 0): 1, (1, 1): 0}
p = {x: Fraction(psi[x] * (1 - x[0]), 2) for x in cube2}
assert not mtp2_failures(p)
assert psi[0, 0] * psi[1, 1] - psi[0, 1] * psi[1, 0] == -1
eps = Fraction(1, 10)
w_smooth = {x: (1 if x[0] == 0 else eps) * (psi[x] or eps) for x in cube2}
smooth_z = sum(w_smooth.values())
smooth = {x: w_smooth[x] / smooth_z for x in cube2}
assert mtp2_failures(smooth)

cube4 = list(product(range(2), repeat=4))
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
energy = {x: sum(abs(x[i] - x[j]) for i, j in edges[:3]) + 1 - abs(x[3] - x[0]) for x in cube4}
emin = min(energy.values())
support = [x for x in cube4 if energy[x] == emin]
q = {x: Fraction(int(x in support), len(support)) for x in cube4}
edge_projections = [set((x[i], x[j]) for x in support) for i, j in edges]
assert len(support) == 8
assert all(len(projection) == 4 for projection in edge_projections)
assert mtp2_failures(q)

tie = {x: Fraction(int(x[0] == x[1]), 2) for x in cube2}
assert not mtp2_failures(tie)
print(json.dumps({
    'pinned_potential': {'mtp2_failures': mtp2_failures(p), 'edge_determinant': -1,
                         'smoothed_mtp2_first_failure': mtp2_failures(smooth)[0]},
    'frustrated_cycle': {'minimum_energy': emin, 'support': support,
                         'all_edge_projections_full': True, 'mtp2_first_failure': mtp2_failures(q)[0]},
    'tie': {'support': [x for x in tie if tie[x]], 'natural_lattice_rank': 1, 'number_of_coordinates': 2}
}, indent=2))

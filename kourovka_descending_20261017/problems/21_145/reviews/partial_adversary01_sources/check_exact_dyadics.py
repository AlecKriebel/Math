"""Exact finite checks supplementing, not replacing, the audit's proofs.

Run with Python 3. Uses only fractions and the standard library.
"""

from collections import deque
from fractions import Fraction as Q
import json


def x0(t):
    if t <= Q(1, 2):
        return t / 2
    if t <= Q(3, 4):
        return t - Q(1, 4)
    return 2 * t - 1


def x0_inverse(t):
    if t <= Q(1, 4):
        return 2 * t
    if t <= Q(1, 2):
        return t + Q(1, 4)
    return (t + 1) / 2


def x1(t):
    if t <= Q(1, 2):
        return t
    return Q(1, 2) + x0(2 * t - 1) / 2


def x1_inverse(t):
    if t <= Q(1, 2):
        return t
    return Q(1, 2) + x0_inverse(2 * t - 1) / 2


generators = (x0, x0_inverse, x1, x1_inverse)


def depth(q):
    assert 0 < q < 1
    denominator = q.denominator
    assert denominator & (denominator - 1) == 0
    return denominator.bit_length() - 1


def iterate(f, n, q):
    for _ in range(n):
        q = f(q)
    return q


def left_clone(f, q):
    return f(2 * q) / 2 if q <= Q(1, 2) else q


depth_checks = 0
inverse_checks = 0
for exponent in range(1, 14):
    for numerator in range(1, 2**exponent, 2):
        q = Q(numerator, 2**exponent)
        for s in generators:
            assert depth(s(q)) <= exponent + 1
            depth_checks += 1
        assert x0_inverse(x0(q)) == q == x0(x0_inverse(q))
        assert x1_inverse(x1(q)) == q == x1(x1_inverse(q))
        inverse_checks += 4

# Minimal word lengths in the orbit of 1/2, up to radius 10.
distances = {Q(1, 2): 0}
queue = deque([Q(1, 2)])
while queue:
    q = queue.popleft()
    radius = distances[q]
    if radius == 10:
        continue
    for s in generators:
        image = s(q)
        if image not in distances:
            distances[image] = radius + 1
            queue.append(image)
orbit_lengths = []
for n in range(11):
    q = Q(1, 2 ** (n + 1))
    assert distances[q] == n
    orbit_lengths.append(distances[q])

for n in range(1, 129):
    # f_n = x1^n x0, where products mean composition.
    assert iterate(x1, n, x0(Q(1, 2))) == Q(1, 4)
    assert iterate(x1, n, Q(1, 2)) == Q(1, 2)
    near_one = 1 - Q(1, 2 ** (n + 4))
    fn_near_one = iterate(x1, n, x0(near_one))
    assert (1 - fn_near_one) / (1 - near_one) == 2 ** (n + 1)
    assert iterate(x0, n, Q(1, 2)) == Q(1, 2 ** (n + 1))
    # Adversarial caveat: denominator depth is not a globally Lipschitz
    # function on the usual left-invariant word metric.
    a_n = lambda q: left_clone(lambda t: iterate(x0, n, t), q)
    assert depth(a_n(Q(1, 2))) == 1
    assert depth(a_n(x0(Q(1, 2)))) == n + 2

print(json.dumps({
    "arithmetic": "exact fractions, no floating point",
    "depth_inequality_checks": depth_checks,
    "inverse_identity_checks": inverse_checks,
    "max_reduced_dyadic_exponent": 13,
    "orbit_bfs_radius": 10,
    "orbit_vertices_found": len(distances),
    "minimal_orbit_lengths_for_2_to_minus_n_minus_1": orbit_lengths,
    "explicit_sequence_checks_n": [1, 128],
    "status": "PASS",
}, indent=2))

#!/usr/bin/env python3
"""Independent finite-interval audit; standard library only.

All computations set lambda=1 and drop the common positive Newton
normalization. Scaling restores arbitrary lambda>0. Numerical results are
diagnostics, not validated interval arithmetic and not the theorem proof.
"""

import json
import math
import random


def gauss_legendre(order):
    nodes = []
    for index in range(1, (order + 1) // 2 + 1):
        root = math.cos(math.pi * (index - 0.25) / (order + 0.5))
        for _ in range(40):
            p0, p1 = 1.0, root
            for degree in range(2, order + 1):
                p0, p1 = p1, ((2 * degree - 1) * root * p1 - (degree - 1) * p0) / degree
            derivative = order * (root * p1 - p0) / (root * root - 1)
            change = p1 / derivative
            root -= change
            if abs(change) < 2e-16:
                break
        weight = 2 / ((1 - root * root) * derivative * derivative)
        nodes.append((-root, weight))
        if root != 0:
            nodes.append((root, weight))
    return sorted(nodes)


NODES = gauss_legendre(48)


def integral(fn, lo, hi, extra=()):
    if hi <= lo:
        return 0.0
    cuts = {lo, hi}
    cuts.update(x for x in extra if lo < x < hi)
    # Dyadic kernel scales prevent narrow central peaks from being missed.
    for sign in (-1, 1):
        value = 0.125
        while value < 2 * max(abs(lo), abs(hi), 1):
            if lo < sign * value < hi:
                cuts.add(sign * value)
            value *= 2
    if lo < 0 < hi:
        cuts.add(0.0)
    cuts = sorted(cuts)
    pieces = []
    for a, b in zip(cuts, cuts[1:]):
        middle, radius = (a + b) / 2, (b - a) / 2
        pieces.append(radius * math.fsum(weight * fn(middle + radius * node) for node, weight in NODES))
    return math.fsum(pieces)


def overlap_formula(h, length_i, length_j, separation):
    return max(0.0, min(length_i, length_j, (length_i + length_j) / 2 - abs(h - separation)))


def finite_terms(n, length_i, length_j, separation):
    a, b = separation - length_i / 2, separation + length_i / 2
    c, d = -length_j / 2, length_j / 2
    radius, plateau = (length_i + length_j) / 2, abs(length_i - length_j) / 2
    lo, hi = separation - radius, separation + radius
    cuts = [separation + sign * size for sign in (-1, 1) for size in (radius, plateau)]
    kernel = lambda h: (1 + h * h) ** (-(n - 2) / 2)
    rho = lambda h: overlap_formula(h, length_i, length_j, separation)
    mass = integral(rho, lo, hi, cuts)
    A = integral(lambda h: rho(h) * kernel(h), lo, hi, cuts)
    D = integral(lambda h: rho(h) * h * h / (1 + h * h) * kernel(h), lo, hi, cuts)
    T = integral(lambda h: rho(h) * h / (1 + h * h) * kernel(h), lo, hi, cuts)
    # Endpoint terms integrate directly along interval endpoints, independently
    # of the overlap density used above.
    EI = length_i / 2 * (integral(kernel, a - d, a - c) + integral(kernel, b - d, b - c))
    EJ = length_j / 2 * (integral(kernel, a - c, b - c) + integral(kernel, a - d, b - d))
    # A second, explicitly paired computation of the midpoint integral.
    positive_d = abs(separation)
    paired_cuts = [sign * positive_d + side * size for sign in (-1, 1) for side in (-1, 1) for size in (radius, plateau)]
    paired_T = integral(
        lambda h: (overlap_formula(h, length_i, length_j, positive_d)
                   - overlap_formula(-h, length_i, length_j, positive_d))
        * h / (1 + h * h) * kernel(h),
        0, positive_d + radius, paired_cuts,
    )
    paired_T *= 1 if separation >= 0 else -1
    return A, D, T, EI, EJ, mass, paired_T


def four_corners(fn, length_i, length_j, separation):
    a, b = separation - length_i / 2, separation + length_i / 2
    c, d = -length_j / 2, length_j / 2
    return math.fsum([fn(b - c), -fn(a - c), -fn(b - d), fn(a - d)])


def n3_exact(length_i, length_j, separation):
    a, b = separation - length_i / 2, separation + length_i / 2
    c, d = -length_j / 2, length_j / 2
    H = lambda h: h * math.asinh(h) - math.hypot(1, h)
    HD = lambda h: h * math.asinh(h) - 2 * math.hypot(1, h)
    HT = lambda h: -math.asinh(h)
    G = math.asinh
    A, D, T = (four_corners(fn, length_i, length_j, separation) for fn in (H, HD, HT))
    EI = length_i / 2 * math.fsum([G(a - c), -G(a - d), G(b - c), -G(b - d)])
    EJ = length_j / 2 * math.fsum([G(b - c), -G(a - c), G(b - d), -G(a - d)])
    return A, D, T, EI, EJ


def run():
    rng = random.Random(37020261007)
    records = []
    max_identity_error = 0.0
    max_slack_error = 0.0
    max_pair_error = 0.0
    max_mass_error = 0.0
    min_slack_scaled = math.inf
    min_midpoint_product = math.inf
    max_overlap_error = 0.0

    cases = [
        (n, L, M, d0, ci, cj)
        for n in (3, 4, 5, 10)
        for L, M, d0 in ((2, 2, 0), (1, 4, 0), (1, 4, .2), (1, 4, -3), (2, .1, 20), (.1, 2, -20))
        for ci, cj in ((1, 1), (2, 7), (0, 3), (0, 0))
    ]
    # These normalized geometries represent fixed physical intervals at very
    # small lambda. In particular d0=4 with L=2, M=.5 is strictly disjoint.
    small_lambda_case_count = 0
    for physical_lambda in (1e-3, 1e-6):
        for n in (3, 4, 10):
            for L, M, d0 in ((2, .5, 0), (2, .5, 4), (.1, 3, -8)):
                cases.append((n, L / physical_lambda, M / physical_lambda,
                              d0 / physical_lambda, 1, 3))
                small_lambda_case_count += 1
    for _ in range(500):
        n = rng.choice((3, 4, 5, 6, 10, 20))
        L, M = (10 ** rng.uniform(-2, 2) for _ in range(2))
        d0 = rng.choice((-1, 0, 1)) * 10 ** rng.uniform(-2, 2)
        ci, cj = (rng.choice((0, 1, 10 ** rng.uniform(-2, 2))) for _ in range(2))
        cases.append((n, L, M, d0, ci, cj))

    for n, L, M, d0, ci, cj in cases:
        A, D, T, EI, EJ, mass, paired_T = finite_terms(n, L, M, d0)
        scale = max(2 * A + EI + EJ + (n - 2) * (D + abs(d0 * T)), 1e-250)
        identity_error = abs(2 * A - EI - EJ - (n - 2) * (D - d0 * T)) / scale
        minimum = min(ci, cj)
        lhs = (ci + cj) * A
        rhs = ci * EI + cj * EJ + (n - 2) * minimum * D + abs(ci - cj) * A
        expected_slack = (n - 2) * minimum * d0 * T + (ci - minimum) * EI + (cj - minimum) * EJ
        weighted_scale = max(lhs + rhs, 1e-250)
        slack_error = abs(rhs - lhs - expected_slack) / weighted_scale
        slack_scaled = (rhs - lhs) / weighted_scale
        max_identity_error = max(max_identity_error, identity_error)
        max_slack_error = max(max_slack_error, slack_error)
        max_pair_error = max(max_pair_error, abs(T - paired_T) / max(A, 1e-250))
        max_mass_error = max(max_mass_error, abs(mass - L * M) / (L * M))
        min_slack_scaled = min(min_slack_scaled, slack_scaled)
        min_midpoint_product = min(min_midpoint_product, d0 * T / max(A, 1e-250))
        for _ in range(4):
            h = d0 + rng.uniform(-1.2, 1.2) * (L + M) / 2
            a, b = d0 - L / 2, d0 + L / 2
            c, d = -M / 2, M / 2
            actual_overlap = max(0, min(b, d + h) - max(a, c + h))
            max_overlap_error = max(max_overlap_error, abs(actual_overlap - overlap_formula(h, L, M, d0)) / min(L, M))
        assert identity_error < 3e-10, (n, L, M, d0, identity_error)
        assert slack_error < 3e-10, (n, L, M, d0, slack_error)
        assert slack_scaled >= -3e-10, (n, L, M, d0, ci, cj, slack_scaled)
        assert d0 * T >= -3e-10 * A, (n, L, M, d0, T)
        assert abs(mass - L * M) < 3e-10 * L * M
        if len(records) < 6:
            records.append(dict(n=n, L=L, M=M, d0=d0, ci=ci, cj=cj, lhs=lhs, rhs=rhs, midpoint_product=d0*T))

    # Closed forms provide an independent check of every n=3 quantity.
    max_n3_error = 0.0
    for L, M, d0 in ((2, 2, 0), (1, 4, 0), (1, 4, .2), (1, 4, -3), (2, .1, 20), (.1, 2, -20)):
        quadrature = finite_terms(3, L, M, d0)[:5]
        exact = n3_exact(L, M, d0)
        scale = max(quadrature[0], 1e-250)
        error = max(abs(x - y) / scale for x, y in zip(quadrature, exact))
        max_n3_error = max(max_n3_error, error)
        assert error < 3e-10, (L, M, d0, error)

    # At n=3 and lambda=1, for fixed bounded I=(-1,1) and J=(-R,R),
    # A(R) has a closed form; its increasing increments approach 4 log(10)
    # when R is multiplied by 10. This confirms the logarithmic tail.
    tail = []
    previous = None
    for R in (10, 100, 1000, 10000):
        A = n3_exact(2, 2 * R, 0)[0]
        tail.append(dict(R=R, A=A, increment=None if previous is None else A-previous))
        previous = A

    print(json.dumps(dict(
        seed=37020261007,
        finite_case_count=len(cases),
        small_transverse_separation_case_count=small_lambda_case_count,
        physical_lambdas_for_small_separation_cases=[1e-3, 1e-6],
        overlap_point_count=4*len(cases),
        max_midpoint_identity_scaled_error=max_identity_error,
        max_weighted_slack_scaled_error=max_slack_error,
        max_direct_vs_paired_T_scaled_error=max_pair_error,
        max_density_mass_relative_error=max_mass_error,
        max_overlap_formula_relative_error=max_overlap_error,
        minimum_scaled_slack=min_slack_scaled,
        minimum_scaled_midpoint_product=min_midpoint_product,
        max_n3_closed_form_scaled_error=max_n3_error,
        n3_unbounded_truncations=tail,
        representative_cases=records,
    ), indent=2))


if __name__ == "__main__":
    run()

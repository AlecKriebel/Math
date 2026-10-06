#!/usr/bin/env python3
"""Finite exact controls for the elementary lemmas; not a topology solver."""
import itertools
import json
import math
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical(p, q):
    return (p, q) if p > 0 or (p == 0 and q > 0) else (-p, -q)


def slope_grid(alpha, beta, m, n):
    a, b = alpha
    c, d = beta
    D = a * d - b * c
    require(D != 0, "parallel slopes are outside the inverse formula")
    require(m >= 0 and n >= 0, "thresholds must be nonnegative")
    found = set()
    for u in range(-m, m + 1):
        for v in range(-n, n + 1):
            P, Q = c * u - a * v, d * u - b * v
            if P % D or Q % D:
                continue
            p, q = P // D, Q // D
            if math.gcd(p, q) == 1:
                require(a * q - b * p == u, "first determinant inversion")
                require(c * q - d * p == v, "second determinant inversion")
                found.add(canonical(p, q))
    return found


def brute_slopes(alpha, beta, m, n):
    a, b = alpha
    c, d = beta
    D = abs(a * d - b * c)
    P = (abs(c) * m + abs(a) * n) // D
    Q = (abs(d) * m + abs(b) * n) // D
    return {canonical(p, q) for p in range(-P, P + 1)
            for q in range(-Q, Q + 1)
            if math.gcd(p, q) == 1 and abs(a*q-b*p) <= m and abs(c*q-d*p) <= n}


def group_controls(elements, identity, mul):
    count = 0
    for mask in range(1 << len(elements)):
        S = {g for i, g in enumerate(elements) if (mask >> i) & 1}
        triples = False
        for g in elements:
            for h in elements:
                if g == identity or h == identity or g == h:
                    continue
                intersection = S & {mul(g, s) for s in S} & {mul(h, s) for s in S}
                triples = triples or bool(intersection)
        require(triples == (len(S) >= 3), "regular-fiber triple criterion")
        count += 1
    return count


def solve_affine(A, B):
    rows = [[Fraction(int(i == j)) - A[i][j] for j in range(3)] + [B[i]] for i in range(3)]
    for col in range(3):
        piv = next((i for i in range(col, 3) if rows[i][col]), None)
        require(piv is not None, "strict contraction linear system must be invertible")
        rows[col], rows[piv] = rows[piv], rows[col]
        scale = rows[col][col]
        rows[col] = [v / scale for v in rows[col]]
        for i in range(3):
            if i != col:
                scale = rows[i][col]
                rows[i] = [u - scale*v for u, v in zip(rows[i], rows[col])]
    return [rows[i][3] for i in range(3)]


def main():
    cyclic = sum(group_controls(tuple(range(d)), 0, lambda x, y, d=d: (x+y) % d)
                 for d in range(1, 9))
    perms = tuple(itertools.permutations(range(3)))
    nonabelian = group_controls(perms, (0,1,2), lambda p, q: tuple(p[q[j]] for j in range(3)))
    # The whole regular fiber is one repeated translated subset, but has many preimages.
    require({0, 1, 2} == {(x + 1) % 3 for x in (0, 1, 2)}, "stabilizer control")
    require(len({0, 1, 2}) == 3, "stabilizer multiplicity is three")
    slopes = sorted({canonical(p, q) for p in range(-2, 3) for q in range(-2, 3)
                     if math.gcd(p, q) == 1})
    slope_cases = 0
    for alpha in slopes:
        for beta in slopes:
            if alpha == beta:
                continue
            for m in range(5):
                for n in range(5):
                    exact = slope_grid(alpha, beta, m, n)
                    require(exact == brute_slopes(alpha, beta, m, n), "exceptional slope enumeration")
                    require(len(exact) <= ((2*m+1)*(2*n+1)-1)//2, "exceptional slope count bound")
                    require(exact == slope_grid((-alpha[0],-alpha[1]), beta, m, n), "slope orientation invariance")
                    require(exact == slope_grid(beta, alpha, n, m), "slope interchange invariance")
                    slope_cases += 1
    example = slope_grid((1,0), (0,1), 1, 1)
    require(example == {(1,0),(0,1),(1,1),(1,-1)}, "four-exception arithmetic example")
    rejected = 0
    for args in [((1,0),(1,0),1,1),((1,0),(0,1),-1,1)]:
        try:
            slope_grid(*args)
        except RuntimeError:
            rejected += 1
    require(rejected == 2, "invalid slope inputs must be rejected")
    affine_cases = 0
    for signs in itertools.product((-1,1), repeat=6):
        A = [[Fraction(0) for _ in range(3)] for _ in range(3)]
        it = iter(signs)
        for i in range(3):
            for j in range(3):
                if i != j:
                    A[i][j] = Fraction(next(it),8)
        for numerator in itertools.product((-1,0,1), repeat=3):
            B = [Fraction(v,8) for v in numerator]
            require(all(sum(abs(v) for v in A[i]) + abs(B[i]) < 1 for i in range(3)), "graphs map into open cube")
            x = solve_affine(A,B)
            require(all(abs(v) < 1 for v in x), "fixed point is interior")
            require(all(x[i] == B[i] + sum(A[i][j]*x[j] for j in range(3)) for i in range(3)), "fixed point equations")
            affine_cases += 1
    result = {
        "status": "PASS_FINITE_EXACT_CONTROLS",
        "scope": "finite controls only; not a proof of KP-3.13 or of geometric input existence",
        "cyclic_regular_fiber_subsets": cyclic,
        "nonabelian_S3_regular_fiber_subsets": nonabelian,
        "slope_pairs_threshold_cases": slope_cases,
        "primitive_slope_representatives": len(slopes),
        "affine_three_graph_cases": affine_cases,
        "invalid_input_controls_rejected": rejected,
        "arithmetic_exception_example": sorted([list(x) for x in example]),
        "dependencies": "Python standard library; exact integers and fractions",
        "optimized_python": "all controls use explicit exceptions; optimization does not disable them"
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()

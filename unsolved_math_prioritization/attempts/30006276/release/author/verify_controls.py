#!/usr/bin/env python3
"""Exact algebraic controls; no moduli-space Chow intersection is inferred.

Run with Python 3.10+; only the standard library is used.
"""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product, combinations
import json

checks = 0


def check(condition):
    global checks
    checks += 1
    assert condition, checks


def add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, Q(0)) + v
    return {k: v for k, v in out.items() if v}


def scale(a, q):
    return {k: q * v for k, v in a.items() if q * v}


def fibre_mul(a, b):
    out = {}
    for (i, j), c in a.items():
        for (k, l), d in b.items():
            if i + k <= 1 and j + l <= 1:
                key = (i + k, j + l)
                out[key] = out.get(key, Q(0)) + c * d
    return {k: v for k, v in out.items() if v}


def fibre_proj(a):
    out = {}
    for mon, c in a.items():
        term = ({(1, 0): c / 2, (0, 1): c / 2}
                if mon in ((1, 0), (0, 1)) else {mon: c})
        out = add(out, term)
    return out


def fibre_control():
    basis = [{m: Q(1)} for m in [(0, 0), (1, 0), (0, 1), (1, 1)]]
    one, a, b, ab = basis
    theta = add(a, b)
    eta = add(a, scale(b, -1))
    rbasis = [one, theta, ab]
    for x, y, z in product(basis, repeat=3):
        check(fibre_mul(fibre_mul(x, y), z) == fibre_mul(x, fibre_mul(y, z)))
    for x in basis:
        check(fibre_proj(fibre_proj(x)) == fibre_proj(x))
        for r in rbasis:
            check(fibre_proj(fibre_mul(x, r)) == fibre_mul(fibre_proj(x), r))
    for x in basis:
        for r in rbasis:
            check(fibre_mul(x, r).get((1, 1), Q(0)) ==
                  fibre_mul(fibre_proj(x), r).get((1, 1), Q(0)))
    check(fibre_proj(eta) == {})
    check(fibre_proj(fibre_mul(eta, eta)) == scale(ab, -2))
    check(fibre_proj(fibre_mul(a, a)) == {})
    check(fibre_mul(fibre_proj(a), fibre_proj(a)) == scale(ab, Q(1, 2)))
    # Restricted trace pairing in basis (1, theta, ab) has determinant -2.
    matrix = [[fibre_mul(x, y).get((1, 1), Q(0)) for y in rbasis] for x in rbasis]
    check(matrix == [[0, 0, 1], [0, 2, 0], [1, 0, 0]])
    return {"ring": "Q[a,b]/(a^2,b^2)", "projection_a": "(a+b)/2",
            "projection_a_squared": "ab/2", "projection_of_a_squared": "0",
            "kernel_element": "a-b", "projection_of_kernel_square": "-2ab",
            "restricted_pairing_determinant": -2,
            "scope": "fixed polarized abelian surface only, not A_g"}


class LambdaRing:
    """R*(A_g) with n=g-1 generators, squarefree additive basis.

    lambda_i^2 = 2 sum_{k=1}^i (-1)^(k+1) lambda_(i-k) lambda_(i+k).
    A rewrite increases the sum of squared indices at fixed weighted degree,
    so the bounded indices imply termination. The basis theorem is a cited
    geometric input, not established by these controls.
    """
    def __init__(self, n):
        self.n = n

    @lru_cache(None)
    def reduce(self, mon):
        if any(i > self.n or i < 1 for i in mon):
            return ()
        for i in mon:
            if mon.count(i) >= 2:
                rest = list(mon)
                rest.remove(i)
                rest.remove(i)
                out = {}
                for k in range(1, i + 1):
                    if i + k > self.n:
                        continue
                    new = rest + [i + k] + ([i - k] if i - k else [])
                    out = add(out, scale(dict(self.reduce(tuple(sorted(new)))),
                                         Q(2 * (-1) ** (k + 1))))
                return tuple(sorted(out.items()))
        return ((mon, Q(1)),)

    def term(self, coeff, *indices):
        return scale(dict(self.reduce(tuple(sorted(indices)))), Q(coeff))

    def mul(self, a, b):
        out = {}
        for u, c in a.items():
            for v, d in b.items():
                out = add(out, scale(dict(self.reduce(tuple(sorted(u + v)))), c * d))
        return out

    def basis(self):
        return [p for r in range(self.n + 1) for p in combinations(range(1, self.n + 1), r)]


def readable(poly):
    return [{"coefficient": str(c), "lambda_indices": list(m)}
            for m, c in sorted(poly.items())]


def lambda_controls():
    rows = []
    for g in range(2, 9):
        n = g - 1
        ring = LambdaRing(n)
        basis = ring.basis()
        last = ring.term(1, n)
        rank = 0
        for mon in basis:
            result = ring.mul(last, ring.term(1, *mon))
            if n in mon:
                check(result == {})
            else:
                rank += 1
                check(result == {tuple(sorted(mon + (n,))): Q(1)})
        check(rank == 2 ** (n - 1))
        check(ring.mul(last, last) == {})
        # Check every coefficient in c(t)c(-t)-1, with lambda_g=0.
        for degree in range(1, 2 * n + 1):
            value = {}
            for i in range(n + 1):
                j = degree - i
                if 0 <= j <= n:
                    value = add(value, ring.term((-1) ** j, *([i] if i else []),
                                                  *([j] if j else [])))
            check(value == {})
        # All basis triples through g=5 independently exercise associativity.
        if g <= 5:
            for x, y, z in product(basis, repeat=3):
                a, b, c = [ring.term(1, *m) for m in (x, y, z)]
                check(ring.mul(ring.mul(a, b), c) == ring.mul(a, ring.mul(b, c)))
        rows.append({"g": g, "dimension": len(basis), "socle_degree": g * (g - 1) // 2,
                     "lambda_last_rank": rank, "lambda_last_kernel_dimension": len(basis) - rank})
    return rows


def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for first in range(minimum, n + 1):
        for rest in partitions(n - first, first):
            yield (first,) + rest


def codimension_controls():
    tested, surviving = 0, []
    # Finite control, not a replacement for the all-g elementary proof.
    for g in range(2, 41):
        expected = {(1, g - 1)}
        if g >= 4:
            expected.add((2, g - 2))
        if g >= 3:
            expected.add((1, 1, g - 2))
        if g == 6:
            expected.add((3, 3))
        actual = set()
        for part in partitions(g):
            if len(part) < 2:
                continue
            tested += 1
            codim = sum(a * b for i, a in enumerate(part) for b in part[i + 1:])
            if codim <= 2 * g - 3:
                actual.add(part)
        check(actual == expected)
        if g <= 12:
            surviving.append({"g": g, "partitions": [list(p) for p in sorted(actual)]})
    self_candidates = []
    for g in range(2, 101):
        c = (g - 2) * (g - 3) // 2
        N = g * (g - 1) // 2
        check((2 * c <= N) == (g <= 7))
        if 5 <= g <= 7:
            self_candidates.append({"g": g, "codimension_J": c,
                                    "codimension_J_squared": 2 * c, "socle_degree": N,
                                    "complementary_test_degree": N - 2 * c})
    return {"partition_range": [2, 40], "partitions_examined": tested,
            "survivors_through_g12": surviving, "Torelli_self_product_candidates": self_candidates}


def torelli_squares():
    outputs = []
    coeffs = {
        5: [(144, (1, 2)), (-96, (3,))],
        6: [(768, (1, 2, 3)), (-2304, (2, 4)), (Q(948096, 691), (1, 5))],
        7: [(1536, (1, 2, 3, 4)), (-13824, (2, 3, 5)),
            (Q(4418304, 691), (1, 4, 5)), (Q(15044352, 691), (1, 3, 6)),
            (-Q(17685504, 691), (4, 6))]
    }
    for g, terms in coeffs.items():
        ring = LambdaRing(g - 1)
        proj = {}
        for c, mon in terms:
            proj = add(proj, ring.term(c, *mon))
        square = ring.mul(proj, proj)
        check(all(sum(mon) == (g - 2) * (g - 3) for mon in square))
        check(bool(square))
        socle = g * (g - 1) // 2
        complement = socle - (g - 2) * (g - 3)
        pairings = []
        for mon in ring.basis():
            if sum(mon) != complement:
                continue
            pairing = ring.mul(square, ring.term(1, *mon))
            check(all(m == tuple(range(1, g)) for m in pairing))
            pairings.append({"test_lambda_indices": list(mon),
                             "normalized_top_pairing": str(pairing.get(tuple(range(1, g)), Q(0)))})
        outputs.append({"g": g, "P_J_squared": readable(square),
                        "required_J_squared_test_values": pairings,
                        "scope": "right-hand side only; P(J^2) not computed"})
    return outputs


def main():
    result = {"status": "passed", "fixed_fibre_control": fibre_control(),
              "lambda_annihilator_controls": lambda_controls(),
              "codimension_controls": codimension_controls(),
              "torelli_square_right_hand_sides": torelli_squares()}
    result["exact_assertions"] = checks
    result["limitations"] = ["No arbitrary Chow group is computed.",
                              "No lambda_g-pairing of unknown non-tautological products is computed.",
                              "These controls do not resolve problem 30006276."]
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

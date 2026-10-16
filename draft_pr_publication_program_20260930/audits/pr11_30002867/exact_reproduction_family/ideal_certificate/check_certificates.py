#!/usr/bin/env python3
"""Dependency-free exact checks for the finite ideal certificates.

The mathematical proof of generator minimality and resolution exactness is in
REPORT.md. This checks its polynomial identities and quotient-algebra models.
"""
from datetime import datetime, timezone
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path


def add(a, b):
    out = dict(a)
    for exp, coefficient in b.items():
        out[exp] = out.get(exp, 0) + coefficient
        if not out[exp]:
            del out[exp]
    return out


def scale(a, scalar):
    return {exp: coefficient * scalar for exp, coefficient in a.items()
            if coefficient * scalar}


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    out = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            exp = tuple(x + y for x, y in zip(ea, eb))
            out[exp] = out.get(exp, 0) + ca * cb
    return {exp: coefficient for exp, coefficient in out.items() if coefficient}


def power(a, n, variables):
    out = {(0,) * variables: 1}
    for _ in range(n):
        out = mul(out, a)
    return out


def variable(i, variables):
    exp = [0] * variables
    exp[i] = 1
    return {tuple(exp): 1}


def determinant2(a, b, c, d):
    return sub(mul(a, d), mul(b, c))


def reduce_quadratic_extension(polynomial):
    """Variables 3,4 are r,i with r^2=2 and i^2=-1."""
    result = {}
    for exp, coefficient in polynomial.items():
        er, ei = exp[3], exp[4]
        target = exp[:3] + (er % 2, ei % 2)
        value = coefficient * (2 ** (er // 2)) * ((-1) ** (ei // 2))
        result = add(result, {target: value})
    return result


class Algebra:
    def __init__(self, names, unit=0):
        self.names = names
        self.n = len(names)
        self.unit = unit
        self.zero = (0,) * self.n
        self.table = [[self.zero for _ in names] for _ in names]
        for i in range(self.n):
            self.table[unit][i] = self.table[i][unit] = self.basis(i)

    def basis(self, i):
        return tuple(int(j == i) for j in range(self.n))

    def set(self, i, j, value):
        self.table[i][j] = self.table[j][i] = value

    def sum(self, *vectors):
        return tuple(sum(items) for items in zip(*vectors))

    def multiply(self, a, b):
        out = [0] * self.n
        for i, ca in enumerate(a):
            if ca:
                for j, cb in enumerate(b):
                    if cb:
                        for k, ck in enumerate(self.table[i][j]):
                            out[k] += ca * cb * ck
        return tuple(out)

    def exp(self, a, n):
        result = self.basis(self.unit)
        for _ in range(n):
            result = self.multiply(result, a)
        return result

    def evaluate(self, polynomial, coordinates):
        out = [0] * self.n
        for exp, coefficient in polynomial.items():
            term = self.basis(self.unit)
            for coordinate, degree in zip(coordinates, exp):
                term = self.multiply(term, self.exp(coordinate, degree))
            for i, value in enumerate(term):
                out[i] += coefficient * value
        return tuple(out)

    def verify(self):
        b = [self.basis(i) for i in range(self.n)]
        for i, j in product(range(self.n), repeat=2):
            assert self.table[i][j] == self.table[j][i]
            assert self.multiply(b[self.unit], b[i]) == b[i]
        for i, j, k in product(range(self.n), repeat=3):
            assert self.multiply(self.table[i][j], b[k]) == self.multiply(b[i], self.table[j][k])
        return {"dimension": self.n, "basis_associativity_checks": self.n ** 3,
                "commutative": True, "unital": True}


def truncated(qs):
    exps = list(product(*(range(q) for q in qs)))
    a = Algebra([str(e) for e in exps])
    index = {e: i for i, e in enumerate(exps)}
    for i, ei in enumerate(exps):
        for j, ej in enumerate(exps):
            e = tuple(x + y for x, y in zip(ei, ej))
            if all(x < q for x, q in zip(e, qs)):
                a.set(i, j, a.basis(index[e]))
    return a, index


def tensor(a, b):
    c = Algebra([f"{x}*{y}" for x in a.names for y in b.names])
    for i, j in product(range(a.n), repeat=2):
        for k, ell in product(range(b.n), repeat=2):
            v = tuple(x * y for x in a.table[i][j] for y in b.table[k][ell])
            c.set(i * b.n + k, j * b.n + ell, v)
    return c


def convolve(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def check_square_colons(d):
    exponents = set()
    for i in range(d):
        for j in range(i, d):
            exp = [0] * d
            exp[i] += 1
            exp[j] += 1
            exponents.add(tuple(exp))
    preceding = []
    for g in sorted(exponents, reverse=True):
        j = max(i for i, x in enumerate(g) if x)
        for h in preceding:
            quotient = [x - min(x, y) for x, y in zip(h, g)]
            assert any(quotient[q] for q in range(j))
        for q in range(j):
            multiple = list(g)
            multiple[q] += 1
            assert any(all(x <= y for x, y in zip(h, multiple)) for h in preceding)
        preceding.append(g)
    return len(exponents)


def main():
    u, v = variable(0, 2), variable(1, 2)
    f1, f2, f3 = sub(power(u, 2, 2), power(v, 3, 2)), mul(u, v), power(v, 4, 2)
    assert sub(mul(v, f1), mul(u, f2)) == scale(f3, -1)

    F = [power(u, 4, 2), sub(mul(u, v), power(u, 3, 2)), power(v, 2, 2)]
    zero = {}
    B = [[sub(v, power(u, 2, 2)), u], [scale(power(u, 3, 2), -1), add(v, power(u, 2, 2))], [zero, scale(u, -1)]]
    for col in range(2):
        value = {}
        for row in range(3):
            value = add(value, mul(F[row], B[row][col]))
        assert value == {}
    minors = [determinant2(*B[1], *B[2]), scale(determinant2(*B[0], *B[2]), -1), determinant2(*B[0], *B[1])]
    assert minors == F
    assert power(sub(v, power(u, 2, 2)), 2, 2) == sub(sub(F[2], scale(mul(u, F[1]), 2)), F[0])

    P = Algebra(["1", "u", "v", "v2", "v3"])
    P.set(1, 1, P.basis(4))
    for i, j in product(range(1, 4), repeat=2):
        if i + j <= 3:
            P.set(i + 1, j + 1, P.basis(i + j + 1))
    assert all(P.evaluate(f, [P.basis(1), P.basis(2)]) == P.zero for f in [f1, f2, f3])

    K = Algebra(["1", "u", "u2", "u3", "v"])
    for i, j in product(range(1, 4), repeat=2):
        if i + j <= 3:
            K.set(i, j, K.basis(i + j))
    K.set(1, 4, K.basis(3))
    assert all(K.evaluate(f, [K.basis(1), K.basis(4)]) == K.zero for f in F)

    J = Algebra(["1", "x", "y", "z", "q"])
    J.set(1, 2, J.basis(4))
    J.set(3, 3, J.basis(4))
    x, y, z = [variable(i, 3) for i in range(3)]
    G = [power(x, 2, 3), power(y, 2, 3), mul(x, z), mul(y, z), sub(power(z, 2, 3), mul(x, y))]
    assert all(J.evaluate(f, [J.basis(i) for i in [1, 2, 3]]) == J.zero for f in G)

    C, idx = truncated((3, 2))
    a, b = C.basis(idx[(1, 0)]), C.basis(idx[(0, 1)])
    original = [a, C.sum(b, C.exp(a, 2)), C.multiply(a, b)]
    uu, vv, ww = [variable(i, 3) for i in range(3)]
    H = [power(uu, 3, 3), power(sub(vv, power(uu, 2, 3)), 2, 3), sub(ww, mul(uu, vv))]
    assert all(C.evaluate(f, original) == C.zero for f in H)
    # Inverse coordinates a=u, b=v-u^2, c=w-uv are also checked universally.
    aa, bb, cc = [variable(i, 3) for i in range(3)]
    inv_v = add(bb, power(aa, 2, 3))
    inv_w = add(add(cc, mul(aa, bb)), power(aa, 3, 3))
    assert sub(inv_v, power(aa, 2, 3)) == bb
    assert sub(inv_w, mul(aa, inv_v)) == cc

    # Equal-squares isomorphism in the exact field Q(i,sqrt(2)).
    qa, qb, qc, qr, qi = [variable(i, 5) for i in range(5)]
    qu = scale(mul(qr, add(qa, qb)), Fraction(1, 2))
    qv = scale(mul(mul(qi, qr), sub(qa, qb)), Fraction(-1, 2))
    qw = qc
    qa2, qb2 = power(qa, 2, 5), power(qb, 2, 5)
    equal_square_identities = [
        sub(sub(power(qu, 2, 5), power(qv, 2, 5)), add(qa2, qb2)),
        sub(sub(power(qu, 2, 5), power(qw, 2, 5)),
            sub(scale(add(qa2, qb2), Fraction(1, 2)), sub(power(qc, 2, 5), mul(qa, qb)))),
        sub(mul(qu, qv), scale(mul(qi, sub(qa2, qb2)), Fraction(-1, 2))),
        sub(mul(qu, qw), scale(mul(qr, add(mul(qa, qc), mul(qb, qc))), Fraction(1, 2))),
        sub(mul(qv, qw), scale(mul(mul(qi, qr), sub(mul(qa, qc), mul(qb, qc))), Fraction(-1, 2))),
        sub(scale(mul(qr, add(qu, mul(qi, qv))), Fraction(1, 2)), qa),
        sub(scale(mul(qr, sub(qu, mul(qi, qv))), Fraction(1, 2)), qb),
    ]
    assert all(reduce_quadratic_extension(identity) == {} for identity in equal_square_identities)

    E, _ = truncated((2, 2))
    K4, J5 = tensor(K, E), tensor(J, E)
    assert convolve([1, 3, 2], [1, 2, 1]) == [1, 5, 9, 7, 2]
    assert convolve([1, 5, 5, 1], [1, 2, 1]) == [1, 7, 16, 16, 7, 1]
    M5 = Algebra(["1", "x1", "x2", "x3", "x4", "x5"])
    colons = {str(d): check_square_colons(d) for d in range(1, 8)}
    assert [1] + [i * comb(6, i + 1) for i in range(1, 6)] == [1, 15, 40, 45, 24, 5]
    models = {"plane_redundancy_CI": P, "plane_nonhomogeneous_nonCI": K,
              "Gorenstein_d3": J, "triangular_CI_d3": C,
              "plane_tensor_d4": K4, "Gorenstein_tensor_d5": J5,
              "maximal_ideal_square_d5": M5}
    results = {name: algebra.verify() for name, algebra in models.items()}
    expected = [("plane_redundancy_CI", 2, [1, 2, 1]),
                ("plane_nonhomogeneous_nonCI", 3, [1, 3, 2]),
                ("Gorenstein_d3", 5, [1, 5, 5, 1]),
                ("triangular_CI_d3", 3, [1, 3, 3, 1]),
                ("plane_tensor_d4", 5, [1, 5, 9, 7, 2]),
                ("Gorenstein_tensor_d5", 7, [1, 7, 16, 16, 7, 1]),
                ("maximal_ideal_square_d5", 15, [1, 15, 40, 45, 24, 5])]
    for name, mu, betti in expected:
        results[name].update({"minimal_generators_proved_in_REPORT": mu,
                              "minimal_Betti_vector_proved_in_reports": betti})
    output = {"timestamp_UTC": datetime.now(timezone.utc).isoformat(),
              "status": "PASS", "coefficient_arithmetic": "exact integers and rationals",
              "polynomial_identities": "PASS", "models": results,
              "equal_squares_complex_coordinate_identities": {
                  "coefficient_ring": "Q[i,r]/(i^2+1,r^2-2)", "identities_checked": 7, "status": "PASS"},
              "m_squared_lex_colon_checks_dimensions_1_through_7": colons,
              "scope": "Finite quotient models and identities; see reports for exactness and minimality proofs."}
    path = Path(__file__).with_name("CHECK_RESULTS.json")
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

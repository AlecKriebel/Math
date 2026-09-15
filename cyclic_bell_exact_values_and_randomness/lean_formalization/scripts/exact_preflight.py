#!/usr/bin/env python3
"""Supplementary exact checks, NOT a Lean proof or a kernel certificate.

Arithmetic: Q[x]/(x^8+1), interpreted as x=exp(pi*i/8). All equality checks
are rational coefficient comparisons. Positivity/order interpretations and
this Python implementation are not substituted for Lean proof evidence.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json


@dataclass(frozen=True)
class Cyclo:
    c: tuple[Q, ...]

    def __post_init__(self):
        if len(self.c) != 8:
            raise ValueError("Cyclotomic representation must have eight coefficients")

    @staticmethod
    def coerce(value):
        if isinstance(value, Cyclo):
            return value
        return Cyclo((Q(value),) + (Q(0),) * 7)

    def __add__(self, other):
        o = Cyclo.coerce(other)
        return Cyclo(tuple(a + b for a, b in zip(self.c, o.c)))

    __radd__ = __add__

    def __neg__(self):
        return Cyclo(tuple(-a for a in self.c))

    def __sub__(self, other):
        return self + (-Cyclo.coerce(other))

    def __rsub__(self, other):
        return Cyclo.coerce(other) - self

    def __mul__(self, other):
        o = Cyclo.coerce(other)
        r = [Q(0)] * 8
        for i, a in enumerate(self.c):
            if not a:
                continue
            for j, b in enumerate(o.c):
                if b:
                    k = i + j
                    r[k % 8] += (a * b if k < 8 else -a * b)
        return Cyclo(tuple(r))

    __rmul__ = __mul__

    def inverse(self):
        if not any(self.c):
            raise ZeroDivisionError("zero cyclotomic element")
        columns = [(self * zeta(k)).c for k in range(8)]
        rows = [[columns[j][i] for j in range(8)] + [Q(i == 0)] for i in range(8)]
        for k in range(8):
            pivot = next((i for i in range(k, 8) if rows[i][k]), None)
            if pivot is None:
                raise ArithmeticError("singular multiplication map")
            rows[k], rows[pivot] = rows[pivot], rows[k]
            d = rows[k][k]
            rows[k] = [a / d for a in rows[k]]
            for i in range(8):
                if i != k:
                    d = rows[i][k]
                    rows[i] = [a - d * b for a, b in zip(rows[i], rows[k])]
        inv = Cyclo(tuple(rows[i][8] for i in range(8)))
        if self * inv != ONE:
            raise ArithmeticError("inverse residual failed")
        return inv

    def __truediv__(self, other):
        if isinstance(other, (int, Q)):
            return Cyclo(tuple(a / other for a in self.c))
        return self * Cyclo.coerce(other).inverse()

    def __rtruediv__(self, other):
        return Cyclo.coerce(other) * self.inverse()

    def __pow__(self, n: int):
        if n < 0:
            return self.inverse() ** (-n)
        r, b = ONE, self
        while n:
            if n & 1:
                r = r * b
            b = b * b
            n >>= 1
        return r

    def conj(self):
        return sum((a * zeta(-k) for k, a in enumerate(self.c)), ZERO)

    def real(self):
        return (self + self.conj()) / 2

    def rational(self) -> Q:
        if any(self.c[1:]):
            raise ValueError(f"not rational: {self.c}")
        return self.c[0]

    def encoded(self):
        return [str(a) for a in self.c]


ZERO = Cyclo.coerce(0)
ONE = Cyclo.coerce(1)


def zeta(k: int) -> Cyclo:
    k %= 16
    r = [Q(0)] * 8
    r[k % 8] = Q(1 if k < 8 else -1)
    return Cyclo(tuple(r))


def ident(n):
    return tuple(tuple(ONE if i == j else ZERO for j in range(n)) for i in range(n))


def zero_mat(n):
    return tuple(tuple(ZERO for _ in range(n)) for _ in range(n))


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(r, s)) for r, s in zip(a, b))


def scale(c, a):
    return tuple(tuple(c * x for x in r) for r in a)


def mul(a, b):
    n, p, m = len(a), len(b), len(b[0])
    r = [[ZERO for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for k in range(p):
            if a[i][k] == ZERO:
                continue
            for j in range(m):
                if b[k][j] != ZERO:
                    r[i][j] = r[i][j] + a[i][k] * b[k][j]
    return tuple(tuple(row) for row in r)


def dagger(a):
    return tuple(tuple(a[j][i].conj() for j in range(len(a))) for i in range(len(a[0])))


def conjugate(a):
    return tuple(tuple(x.conj() for x in r) for r in a)


def kron(a, b):
    return tuple(tuple(a[i][j] * b[k][l] for j in range(len(a)) for l in range(len(b)))
                 for i in range(len(a)) for k in range(len(b)))


def mv(a, v):
    return tuple(sum((x * y for x, y in zip(row, v) if x != ZERO and y != ZERO), ZERO)
                 for row in a)


def inner(u, v):
    return sum((x.conj() * y for x, y in zip(u, v) if x != ZERO and y != ZERO), ZERO)


def outer(v):
    return tuple(tuple(x * y.conj() for y in v) for x in v)


def mpow(a, n):
    r = ident(len(a))
    for _ in range(n):
        r = mul(r, a)
    return r


def weighted(weights):
    return tuple(tuple(weights[j] if i == (j + 1) % 4 else ZERO for j in range(4))
                 for i in range(4))


def projectors(a):
    powers = [mpow(a, k) for k in range(4)]
    return tuple(sum_mats([scale(zeta(-4 * outcome * k) / 4, powers[k]) for k in range(4)])
                 for outcome in range(4))


def sum_mats(ms):
    r = zero_mat(len(ms[0]))
    for m in ms:
        r = add(r, m)
    return r


def hermitian_part(a):
    return scale(Q(1, 2), add(a, dagger(a)))


class Checks:
    def __init__(self):
        self.passed = []

    def eq(self, label, left, right):
        if left != right:
            raise AssertionError(f"FAILED: {label}")
        self.passed.append(label)

    def different(self, label, left, right):
        if left == right:
            raise AssertionError(f"NEGATIVE CONTROL FAILED: {label}")
        self.passed.append(label)


# Universal algebra side check: free unitary generators in two commuting
# parties, NOT commuting generators within a party. This Python equality
# checker has not been formalized, so this is not a Lean universal bound.
def reduced_word(w):
    stack = []
    for t in w:
        if stack and stack[-1] == -t:
            stack.pop()
        else:
            stack.append(t)
    return tuple(stack)


def word_mul(a, b):
    return (reduced_word(a[0] + b[0]), reduced_word(a[1] + b[1]))


EMPTY = ((), ())


def poly_add(*ps):
    out = {}
    for p in ps:
        for w, c in p.items():
            out[w] = out.get(w, ZERO) + c
    return {w: c for w, c in out.items() if c != ZERO}


def poly_scale(c, p):
    return {w: c * a for w, a in p.items() if c * a != ZERO}


def poly_mul(a, b):
    out = {}
    for u, c in a.items():
        for v, d in b.items():
            w = word_mul(u, v)
            out[w] = out.get(w, ZERO) + c * d
    return {w: c for w, c in out.items() if c != ZERO}


def poly_star(p):
    return {(tuple(-t for t in reversed(w[0])), tuple(-t for t in reversed(w[1]))): c.conj()
            for w, c in p.items()}


def symbolic_sos(lambdas, ck):
    one = {EMPTY: ONE}
    a = [{((l + 1,), ()): ONE} for l in range(4)]
    b = [{((), (y + 1,)): ONE} for y in range(5)]
    terms, squares = [], []
    for l in range(4):
        bh = poly_add(*(poly_scale(zeta(4 * l * y), b[y]) for y in range(4)))
        abh = poly_mul(a[l], bh)
        p = poly_add(poly_scale(4 * lambdas[l], one), poly_scale(-1, abh))
        t = poly_scale(lambdas[l].conj(), abh)
        terms.append(poly_scale(Q(1, 2), poly_add(t, poly_star(t))))
        squares.append(poly_mul(poly_star(p), p))
    f = poly_add(*terms)
    lhs = poly_add(poly_scale(4, one), poly_scale(-1, f))
    rhs = poly_scale(Q(1, 8), poly_add(*squares))
    ck.eq("symbolic reduced second SOS in two-party free unitary algebra", lhs, rhs)
    ab = poly_mul(a[0], b[4])
    r = poly_add(one, poly_scale(-1, ab))
    aug_lhs = poly_add(lhs, one, poly_scale(Q(-1, 2), poly_add(ab, poly_star(ab))))
    aug_rhs = poly_add(rhs, poly_scale(Q(1, 2), poly_mul(poly_star(r), r)))
    ck.eq("symbolic augmented second SOS", aug_lhs, aug_rhs)
    ck.different("wrong SOS prefactor 1/4 rejected", lhs,
                 poly_scale(Q(1, 4), poly_add(*squares)))
    # Ensure the algebra has not accidentally imposed same-party commutation.
    ck.different("Alice same-party commutation NOT assumed", poly_mul(a[0], a[1]), poly_mul(a[1], a[0]))
    ck.different("Bob same-party commutation NOT assumed", poly_mul(b[0], b[1]), poly_mul(b[1], b[0]))
    return {"normal_form_terms_reduced_gap": len(lhs), "normal_form_terms_augmented_gap": len(aug_lhs),
            "kernel_checked": False}


def run():
    ck = Checks()
    ck.eq("cyclotomic relation", zeta(1) ** 8, -ONE)
    ck.eq("conjugation root control", zeta(1).conj(), zeta(15))
    i = zeta(4)
    ck.eq("i squared", i * i, -ONE)
    sin8 = (zeta(1) - zeta(-1)) / (2 * i)
    cos8 = (zeta(1) + zeta(-1)) / 2
    lam = [1 / (4 * sin8), 1 / (4 * sin8), -i / (4 * cos8), -i / (4 * cos8)]
    ck.eq("coefficient normalization", sum((x.conj() * x for x in lam), ZERO), ONE)
    kappa = (0, 1, 3, 2)
    x = weighted((ONE,) * 4)
    first_alice = [x, weighted(tuple(zeta(2 * (2 * t + 1)) for t in kappa))]
    exponents = [(1, 3, 15, 13), (3, 13, 1, 15), (13, 15, 3, 1), (15, 1, 13, 3)]
    bob = [conjugate(weighted(tuple(zeta(e) for e in row))) for row in exponents] + [x]
    d = [scale(zeta(-2 * l * l), weighted(tuple(zeta(-4 * l * t) for t in kappa)))
         for l in range(4)]
    alice = [conjugate(m) for m in d]
    ck.eq("second A0 equals first A0", alice[0], first_alice[0])
    ck.eq("second A1 equals first A1", alice[1], first_alice[1])
    pvm = {}
    for name, obs in [(f"A{j}", a) for j, a in enumerate(alice)] + [(f"B{j}", b) for j, b in enumerate(bob)]:
        ck.eq(name + " unitarity", mul(dagger(obs), obs), ident(4))
        ck.eq(name + " fourth power", mpow(obs, 4), ident(4))
        weights = [obs[(j + 1) % 4][j] for j in range(4)]
        q = [ONE]
        for j in range(3):
            q.append(q[-1] * weights[j])
        ck.eq(name + " cycle product", q[-1] * weights[-1], ONE)
        ps = projectors(obs)
        pvm[name] = ps
        ck.eq(name + " PVM completeness", sum_mats(ps), ident(4))
        ck.eq(name + " observable encoding", sum_mats([scale(zeta(4 * a), ps[a]) for a in range(4)]), obs)
        for a in range(4):
            v = tuple(q[j] * zeta(-4 * a * j) / 2 for j in range(4))
            ck.eq(name + f" eigenvector {a}", mv(obs, v), tuple(zeta(4 * a) * t for t in v))
            ck.eq(name + f" unit eigenvector {a}", inner(v, v), ONE)
            ck.eq(name + f" outer factorization {a}", ps[a], outer(v))
            ck.eq(name + f" Hermitian projector {a}", dagger(ps[a]), ps[a])
            for b in range(4):
                ck.eq(name + f" orthogonal/idempotent {a},{b}", mul(ps[a], ps[b]), ps[a] if a == b else zero_mat(4))
    phi = tuple(ONE / 2 if r == s else ZERO for r in range(4) for s in range(4))
    ck.eq("state normalization", inner(phi, phi), ONE)
    ck.eq("density trace", sum((outer(phi)[j][j] for j in range(16)), ZERO), ONE)
    probabilities = []
    for a in range(4):
        row = []
        for b in range(4):
            pr = inner(phi, mv(kron(pvm['A1'][a], pvm['B4'][b]), phi))
            expected = Q(1, 32) if (a + b) % 2 == 0 else Q(3, 32)
            ck.eq(f"Born probability {a},{b}", pr, Cyclo.coerce(expected))
            row.append(pr.rational())
        probabilities.append(row)
    ck.eq("total probability", sum(map(sum, probabilities)), Q(1))
    for a in range(4):
        ck.eq(f"Alice marginal {a}", sum(probabilities[a]), Q(1, 4))
    for b in range(4):
        ck.eq(f"Bob marginal {b}", sum(row[b] for row in probabilities), Q(1, 4))
    ck.eq("largest entry", max(x for row in probabilities for x in row), Q(3, 32))
    ck.eq("trivial-Eve guessing gap", Q(3, 32) > Q(1, 16), True)
    q = [ONE, zeta(2), -ONE, zeta(6)]
    fourier = []
    for m in range(4):
        qhat = sum((q[j] * zeta(4 * m * j) for j in range(4)), ZERO)
        fourier.append((qhat.conj() * qhat).rational())
    ck.eq("independent Fourier magnitudes", fourier, [Q(2), Q(6), Q(2), Q(6)])
    reduced = sum((inner(phi, mv(kron(add(first_alice[0], scale(zeta(4*y), first_alice[1])), bob[y]), phi)).real()
                   for y in range(4)), ZERO)
    augmented_term = inner(phi, mv(kron(first_alice[0], bob[4]), phi)).real()
    ck.eq("first reduced attained value", reduced, 2 / sin8)
    ck.eq("augmented stabilizer", augmented_term, ONE)
    ck.eq("first augmented attained value", reduced + augmented_term, 2 / sin8 + 1)
    bh = [sum_mats([scale(zeta(4*l*y), bob[y]) for y in range(4)]) for l in range(4)]
    for l in range(4):
        ck.eq(f"Fourier compression {l}", bh[l], scale(4 * lam[l], d[l]))
    f = sum_mats([hermitian_part(scale(lam[l].conj(), kron(alice[l], bh[l]))) for l in range(4)])
    ps = [add(scale(4 * lam[l], ident(16)), scale(-1, kron(alice[l], bh[l]))) for l in range(4)]
    for l in range(4):
        ck.eq(f"second SOS annihilation {l}", mv(ps[l], phi), (ZERO,) * 16)
    ck.eq("full 16x16 witness SOS", add(scale(4, ident(16)), scale(-1, f)),
          scale(Q(1, 8), sum_mats([mul(dagger(p), p) for p in ps])))
    ck.eq("second attained value", inner(phi, mv(f, phi)).real() + augmented_term, Cyclo.coerce(5))
    # Negative controls exercise the physical calculation, not just a number literal.
    wrong_phi = tuple(2 * x for x in phi)
    ck.different("wrong state normalization rejected", inner(wrong_phi, wrong_phi), ONE)
    wrong_pr = inner(wrong_phi, mv(kron(pvm['A1'][0], pvm['B4'][1]), wrong_phi))
    ck.different("wrong Born normalization rejected", wrong_pr, Cyclo.coerce(Q(3, 32)))
    canonical_a1 = weighted(tuple(zeta(2 * (2 * t + 1)) for t in range(4)))
    canonical_p = projectors(canonical_a1)
    canonical_pr = inner(phi, mv(kron(canonical_p[0], pvm['B4'][1]), phi))
    ck.eq("unswapped witness is Fourier-flat at control pair", canonical_pr, Cyclo.coerce(Q(1, 16)))
    ck.different("altered witness cannot retain prescribed odd table entry", canonical_pr, Cyclo.coerce(Q(3, 32)))
    malformed_b = conjugate(weighted(tuple(zeta(e + (j == 0)) for j, e in enumerate(exponents[0]))))
    ck.different("altered polar phase breaks fourth-power relation", mpow(malformed_b, 4), ident(4))
    symbolic = symbolic_sos(lam, ck)
    return {
        "status": "exact_python_checks_passed_NOT_LEAN",
        "kernel_checked": False,
        "formal_endpoint_certified": False,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "arithmetic": "Fraction coefficients in Q[x]/(x^8+1), x interpreted as exp(pi*i/8)",
        "checks_passed": len(ck.passed),
        "check_names": ck.passed,
        "target_probabilities": [[str(p) for p in row] for row in probabilities],
        "fourier_squared_moduli": [str(p) for p in fourier],
        "first_augmented_attained_value_coefficient_vector": (reduced + augmented_term).encoded(),
        "first_value_interpretation": "2/sin(pi/8)+1; this checks attainment, NOT a universal first bound",
        "second_augmented_attained_value": "5",
        "symbolic_second_sos": symbolic,
        "limitations": [
            "Python rational arithmetic and its interpretation were not checked in Lean",
            "No first-family universal bound is established here",
            "The symbolic second SOS is supplemental algebra, not a kernel-checked physical upper bound",
            "No worst-case Eve optimization or independent-agent audit was performed"
        ]
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"{result['checks_passed']} exact checks passed; kernel_checked=false")
    print("Target rows:")
    for row in result["target_probabilities"]:
        print("  " + "  ".join(row))
    print("First attained value: 2/sin(pi/8)+1; second attained value: 5")
    print("No Lean certification or universal first-family bound is claimed.")


if __name__ == "__main__":
    main()

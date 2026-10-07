#!/usr/bin/env python3
"""Independent reference reduction using the p-fixed algebra over F_p.

Standard library only.  The field presentation and p primality are promises.
The factor() interface takes a split-prime-polynomial oracle; its shipped
small_prime_oracle is an EXHAUSTIVE TEST FIXTURE, restricted to p <= 257,
and is not a polynomial-time prime-field factorization implementation.

Represent field and polynomial coefficients as tuples of prime residues and
ascending lists respectively.  Nothing enumerates a field in the reduction.
The demo's oracle and checks intentionally enumerate only tiny test fields.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path


class Field:
    def __init__(self, p: int, h: list[int]):
        if p < 2 or len(h) < 2 or h[-1] % p != 1:
            raise ValueError("Require prime p and monic positive-degree h")
        self.p = p
        self.h = tuple(a % p for a in h)
        self.m = len(h) - 1
        self.q = p ** self.m
        self.zero = (0,) * self.m
        self.one = (1,) + (0,) * (self.m - 1)

    def element(self, a):
        if isinstance(a, int):
            return (a % self.p,) + (0,) * (self.m - 1)
        if len(a) != self.m:
            raise ValueError("Wrong field coefficient dimension")
        return tuple(x % self.p for x in a)

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def neg(self, a):
        return tuple(-x % self.p for x in a)

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def mul(self, a, b):
        c = [0] * (2 * self.m - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                c[i + j] = (c[i + j] + x * y) % self.p
        for k in range(len(c) - 1, self.m - 1, -1):
            x = c[k]
            for j in range(self.m):
                c[k - self.m + j] = (c[k - self.m + j] - x * self.h[j]) % self.p
        return tuple(c[:self.m])

    def power(self, a, e):
        if e < 0:
            raise ValueError("Negative exponent")
        r = self.one
        while e:
            if e & 1:
                r = self.mul(r, a)
            e >>= 1
            if e:
                a = self.mul(a, a)
        return r

    def inv(self, a):
        if a == self.zero:
            raise ZeroDivisionError
        # Promise that h is irreducible supplies the finite-field identity.
        r = self.power(a, self.q - 2)
        if self.mul(a, r) != self.one:
            raise ValueError("Field promise failed")
        return r


def trim(F, a):
    a = list(a)
    while a and a[-1] == F.zero:
        a.pop()
    return a


def poly(F, raw):
    return trim(F, [F.element(a) for a in raw])


def add(F, a, b):
    c = [F.zero] * max(len(a), len(b))
    for i in range(len(c)):
        c[i] = F.add(a[i] if i < len(a) else F.zero,
                     b[i] if i < len(b) else F.zero)
    return trim(F, c)


def sub(F, a, b):
    return add(F, a, [F.neg(x) for x in b])


def scale(F, a, c):
    return trim(F, [F.mul(x, c) for x in a])


def mul(F, a, b):
    if not a or not b:
        return []
    c = [F.zero] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] = F.add(c[i + j], F.mul(x, y))
    return trim(F, c)


def divmod_poly(F, a, b):
    if not b:
        raise ZeroDivisionError
    r = trim(F, a)
    q = [F.zero] * max(0, len(a) - len(b) + 1)
    ib = F.inv(b[-1])
    while len(r) >= len(b):
        k = len(r) - len(b)
        c = F.mul(r[-1], ib)
        q[k] = c
        for j, x in enumerate(b):
            r[k + j] = F.sub(r[k + j], F.mul(c, x))
        r = trim(F, r)
    return trim(F, q), r


def quotient(F, a, b):
    q, r = divmod_poly(F, a, b)
    if r:
        raise ArithmeticError("Division was not exact")
    return q


def monic(F, a):
    return scale(F, a, F.inv(a[-1])) if a else []


def gcd(F, a, b):
    while b:
        a, b = b, divmod_poly(F, a, b)[1]
    return monic(F, a)


def power(F, a, e, modulus=None):
    r = [F.one]
    if modulus is not None:
        a = divmod_poly(F, a, modulus)[1]
    while e:
        if e & 1:
            r = mul(F, r, a)
            if modulus is not None:
                r = divmod_poly(F, r, modulus)[1]
        e >>= 1
        if e:
            a = mul(F, a, a)
            if modulus is not None:
                a = divmod_poly(F, a, modulus)[1]
    return r


def derivative(F, a):
    return trim(F, [F.mul(F.element(i), a[i]) for i in range(1, len(a))])


def squarefree(F, f):
    """Return disjoint squarefree supports with exact multiplicities."""
    if len(f) <= 1:
        return []
    C = gcd(F, f, derivative(F, f))
    W = quotient(F, f, C)
    ans = []
    i = 1
    while W != [F.one]:
        Y = gcd(F, W, C)
        Z = quotient(F, W, Y)
        if Z != [F.one]:
            ans.append((Z, i))
        W = Y
        C = quotient(F, C, Y)
        i += 1
    if C != [F.one]:
        if derivative(F, C):
            raise ArithmeticError("Residual polynomial is not a pth power")
        for k, c in enumerate(C):
            if k % F.p and c != F.zero:
                raise ArithmeticError("Non-p-divisible exponent in pth power")
        H = [F.power(C[k], F.p ** (F.m - 1))
             for k in range(0, len(C), F.p)]
        ans.extend((Z, F.p * j) for Z, j in squarefree(F, trim(F, H)))
    return ans


def vector(F, a, d):
    return [a[i][j] if i < len(a) else 0
            for i in range(d) for j in range(F.m)]


def from_vector(F, v):
    if len(v) % F.m:
        raise ValueError("Wrong vector dimension")
    return trim(F, [tuple(v[i:i + F.m]) for i in range(0, len(v), F.m)])


def kernel_prime(p, columns):
    """Deterministic full RREF; columns are prime-field vectors."""
    ncols = len(columns)
    nrows = len(columns[0]) if columns else 0
    M = [[columns[j][i] % p for j in range(ncols)] for i in range(nrows)]
    pivots = []
    row = 0
    for col in range(ncols):
        pivot = next((i for i in range(row, nrows) if M[i][col]), None)
        if pivot is None:
            continue
        M[row], M[pivot] = M[pivot], M[row]
        t = pow(M[row][col], -1, p)
        M[row] = [(x * t) % p for x in M[row]]
        for i in range(nrows):
            if i != row and M[i][col]:
                t = M[i][col]
                M[i] = [(x - t * y) % p for x, y in zip(M[i], M[row])]
        pivots.append(col)
        row += 1
        if row == nrows:
            break
    free = [i for i in range(ncols) if i not in pivots]
    basis = []
    for col in free:
        v = [0] * ncols
        v[col] = 1
        for i, pivot in enumerate(pivots):
            v[pivot] = -M[i][col] % p
        basis.append(v)
    return basis


def p_fixed_basis(F, f):
    d = len(f) - 1
    columns = []
    for i in range(d):
        for j in range(F.m):
            e = tuple(1 if k == j else 0 for k in range(F.m))
            a = [F.zero] * i + [e]
            columns.append(vector(F, sub(F, power(F, a, F.p, f), a), d))
    return [from_vector(F, v) for v in kernel_prime(F.p, columns)]


def minimal_polynomial(F, c, f, fixed_dim):
    """First power relation, incrementally reduced in ambient dimension dm."""
    d = len(f) - 1
    basis = []  # (pivot, normalized vector, normalized power relation)
    a = [F.one]
    for k in range(fixed_dim + 1):
        v = vector(F, a, d)
        relation = [0] * k + [1]
        for pivot, w, wr in basis:
            t = v[pivot]
            if t:
                v = [(x - t * y) % F.p for x, y in zip(v, w)]
                for j, x in enumerate(wr):
                    relation[j] = (relation[j] - t * x) % F.p
        pivot = next((j for j, x in enumerate(v) if x), None)
        if pivot is None:
            if relation[-1] != 1:
                raise ArithmeticError("Power relation unexpectedly nonmonic")
            # Independently evaluate the returned relation in the quotient.
            result = []
            for coefficient in reversed(relation):
                result = divmod_poly(F, add(F, mul(F, result, c),
                                           [F.element(coefficient)]), f)[1]
            if result:
                raise ArithmeticError("Invalid minimal-polynomial relation")
            return relation
        t = pow(v[pivot], -1, F.p)
        basis.append((pivot, [(x * t) % F.p for x in v],
                      [(x * t) % F.p for x in relation]))
        a = divmod_poly(F, mul(F, a, c), f)[1]
    raise ArithmeticError("No relation within fixed algebra dimension")


def small_prime_oracle(p, coefficients):
    """Exhaustive split-polynomial oracle FOR SMALL TEST FIXTURES ONLY."""
    if p > 257:
        raise ValueError("Test oracle refuses p>257; supply a genuine oracle")
    roots = []
    for a in range(p):
        z = 0
        for c in reversed(coefficients):
            z = (a * z + c) % p
        if z == 0:
            roots.append(a)
    if len(roots) != len(coefficients) - 1:
        raise ArithmeticError("Oracle input not split squarefree")
    return roots


def check_roots(p, mu, roots):
    """Check the exact split factorization, not just the number of roots."""
    if len(set(roots)) != len(roots) or any(not 0 <= a < p for a in roots):
        raise ArithmeticError("Invalid or repeated oracle roots")
    product = [1]
    for a in roots:
        nxt = [0] * (len(product) + 1)
        for j, c in enumerate(product):
            nxt[j] = (nxt[j] - a * c) % p
            nxt[j + 1] = (nxt[j + 1] + c) % p
        product = nxt
    if product != mu:
        raise ArithmeticError("Oracle roots do not factor minimal polynomial")


def product_poly(F, polys):
    r = [F.one]
    for a in polys:
        r = mul(F, r, a)
    return r


def factor(F, raw, prime_split_oracle):
    """Conditional full reduction, including multiplicities and zero status."""
    f = poly(F, raw)
    if not f:
        return {"zero": True, "scalar": None, "factors": [], "trace": []}
    scalar = f[-1]
    answer, trace = [], []
    for u, exponent in squarefree(F, monic(F, f)):
        basis = p_fixed_basis(F, u)
        blocks = [u]
        receipt = {"degree": len(u) - 1,
                   "matrix_dimension": (len(u) - 1) * F.m,
                   "fixed_dimension": len(basis), "minimal_degrees": [],
                   "gcd_calls": 0}
        for c in basis:
            if sub(F, power(F, c, F.p, u), c):
                raise ArithmeticError("Kernel basis is not p-fixed")
            mu = minimal_polynomial(F, c, u, len(basis))
            receipt["minimal_degrees"].append(len(mu) - 1)
            roots = prime_split_oracle(F.p, mu)
            check_roots(F.p, mu, roots)
            refined = []
            for g in blocks:
                for a in roots:
                    receipt["gcd_calls"] += 1
                    v = gcd(F, g, sub(F, c, [F.element(a)]))
                    if len(v) > 1:
                        refined.append(v)
            if product_poly(F, refined) != u:
                raise ArithmeticError("Gcd refinement did not partition input")
            blocks = refined
        if product_poly(F, blocks) != u:
            raise ArithmeticError("Factor support reconstruction failed")
        answer.extend((g, exponent) for g in blocks)
        trace.append(receipt)
    reconstructed = scale(F, product_poly(F, [power(F, g, e)
                                               for g, e in answer]), scalar)
    if reconstructed != f:
        raise ArithmeticError("Complete factorization reconstruction failed")
    return {"zero": False, "scalar": scalar, "factors": answer, "trace": trace}


def factor_key(g, exponent):
    return (tuple(g), exponent)


def fixture(F, scalar, factors):
    f = scale(F, product_poly(F, [power(F, g, e) for g, e in factors]), scalar)
    result = factor(F, f, small_prime_oracle)
    expected = sorted(factor_key(g, e) for g, e in factors)
    actual = sorted(factor_key(g, e) for g, e in result["factors"])
    if actual != expected or result["scalar"] != scalar:
        raise AssertionError((actual, expected))
    if sum(len(x["minimal_degrees"]) for x in result["trace"]) > len(f) - 1:
        raise AssertionError("Too many prime calls")
    return {"p": F.p, "h": F.h, "degree": len(f) - 1,
            "input": f, "scalar": scalar, "factors": result["factors"],
            "diagnostics": result["trace"]}


def demo():
    receipts = []
    F = Field(2, [0, 1])
    receipts.append(fixture(F, F.one, [(poly(F, [0, 1]), 4),
                                     (poly(F, [1, 1]), 3)]))
    F = Field(2, [1, 1, 1])
    t, tp1 = F.element((0, 1)), F.element((1, 1))
    # X^2+X+t has no root in F_4 (trace(t)=1), hence is irreducible.
    receipts.append(fixture(F, F.one, [([t, F.one], 4),
                                     ([tp1, F.one], 3),
                                     ([t, F.one, F.one], 2)]))
    # Squarefree case p | m, where Tr(1)=0, with two distinct K-values.
    receipts.append(fixture(F, F.one, [([F.zero, F.one], 1),
                                     ([t, F.one], 1)]))
    F = Field(3, [1, 0, 1])
    t = F.element((0, 1))
    # 1+t is nonsquare in F_9; X^2-(1+t) is irreducible.
    quadratic = [F.element((2, 2)), F.zero, F.one]
    receipts.append(fixture(F, F.element(2), [([F.neg(t), F.one], 2),
                                             ([t, F.one], 5),
                                             (quadratic, 2)]))
    F = Field(5, [0, 1])
    receipts.append(fixture(F, F.element(3), [(poly(F, [2, 0, 1]), 2),
                                             (poly(F, [1, 1]), 3)]))
    for p, h in [(2, [0, 1]), (2, [1, 1, 1]), (3, [1, 0, 1])]:
        F = Field(p, h)
        if not factor(F, [], small_prime_oracle)["zero"]:
            raise AssertionError("Zero convention")
        r = factor(F, [F.one], small_prime_oracle)
        if r["zero"] or r["factors"] or r["scalar"] != F.one:
            raise AssertionError("Constant convention")
        for a in range(F.q):
            digits, z = [], a
            for _ in range(F.m):
                digits.append(z % F.p)
                z //= F.p
            x = tuple(digits)
            if F.power(F.power(x, F.p ** (F.m - 1)), F.p) != x:
                raise AssertionError("Inverse Frobenius fixture failed")
    return {"status": "pass", "implementation": "direct p-fixed algebra",
            "oracle": "exhaustive small-prime TEST FIXTURE, not production factoring",
            "python": platform.python_version(), "examples": receipts,
            "zero_constant_and_inverse_frobenius_checks": "pass"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = demo()
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    data = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(data)
    print(data, end="")

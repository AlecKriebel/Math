#!/usr/bin/env python3
"""Small, independent checks of family 142's auxiliary-table construction.

No claim to implement its astronomical large-characteristic factoring branch.
Uses only Python's standard library. Coefficients have ascending degree order.
"""
import json


def prime(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def kernel(rows, width, p):
    a = [[v % p for v in row] for row in rows]
    pivots = []
    r = 0
    for c in range(width):
        hit = next((i for i in range(r, len(a)) if a[i][c]), None)
        if hit is None:
            continue
        a[r], a[hit] = a[hit], a[r]
        inv = pow(a[r][c], -1, p)
        a[r] = [(v * inv) % p for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                t = a[i][c]
                a[i] = [(v - t * w) % p for v, w in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    out = []
    for c in range(width):
        if c in pivots:
            continue
        v = [0] * width
        v[c] = 1
        for i, pc in enumerate(pivots):
            v[pc] = -a[i][c] % p
        out.append(tuple(v))
    return out


class Cyclotomic:
    def __init__(self, p, ell):
        self.p, self.ell, self.d = p, ell, ell - 1
        self.zero = (0,) * self.d
        self.one = (1,) + (0,) * (self.d - 1)

    def monomial(self, e):
        e %= self.ell
        if e == self.d:
            return ((self.p - 1),) * self.d
        return tuple(int(i == e) for i in range(self.d))

    def scale(self, a, c):
        return tuple(c * x % self.p for x in a)

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def mul(self, a, b):
        # T^ell=1 holds; eliminate T^(ell-1) using Phi_ell.
        z = [0] * self.ell
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                z[(i + j) % self.ell] += x * y
        return tuple((z[i] - z[-1]) % self.p for i in range(self.d))

    def power(self, a, n):
        z = self.one
        while n:
            if n & 1:
                z = self.mul(z, a)
            a = self.mul(a, a)
            n //= 2
        return z

    def subst(self, a, exp):
        z = self.zero
        for i, x in enumerate(a):
            z = self.add(z, self.scale(self.monomial(i * exp), x))
        return z

    def linear_constraints(self, basis, action, scalar=1):
        images = [self.add(action(v), self.scale(v, -scalar)) for v in basis]
        rows = [[col[i] for col in images] for i in range(self.d)]
        coeffs = kernel(rows, len(basis), self.p)
        output = []
        for c in coeffs:
            z = self.zero
            for v, t in zip(basis, c):
                z = self.add(z, self.scale(v, t))
            output.append(z)
        return output


def vq(a, q):
    s = 0
    while a % q == 0:
        a //= q
        s += 1
    return s


def check(p, q):
    assert prime(p) and prime(q) and p > q
    ell = next(ell for ell in range(5, 2000)
               if prime(ell) and ell not in (p, q)
               and ell % (12 * q) == 1
               and pow(p, (ell - 1) // q, ell) != 1)
    r = Cyclotomic(p, ell)
    monomials = [r.monomial(i) for i in range(r.d)]
    subgroup = sorted({pow(a, q, ell) for a in range(1, ell)})
    # One generator gives the same invariant kernel. Small exhaustive order
    # checks here avoid any integer-factorization or primitive-root oracle.
    h = next(a for a in subgroup
             if len({pow(a, j, ell) for j in range(len(subgroup))}) == len(subgroup))
    cols = [r.add(r.subst(v, h), r.scale(v, -1)) for v in monomials]
    rows = [[col[i] for col in cols] for i in range(r.d)]
    basis = kernel(rows, r.d, p)
    assert len(basis) == q
    assert all(r.subst(v, a) == v for a in subgroup for v in basis)
    # Algebraically U_q is reduced; one Frobenius-fixed dimension checks
    # that its q-dimensional reduced algebra has exactly one field factor.
    fixed = r.linear_constraints(basis, lambda v: r.power(v, p))
    assert len(fixed) == 1
    for v in basis:
        assert r.power(v, p ** q) == v
    if q == 2:
        eig = r.linear_constraints(basis, lambda v: r.power(v, p), -1)
        assert len(eig) == 1
        c = r.mul(eig[0], eig[0])
        assert all(x == 0 for x in c[1:]) and c[0]
        assert pow(c[0], (p - 1) // 2, p) == p - 1
        s = vq(p - 1, 2)
        omega = pow(c[0], (p - 1) // 2 ** s, p)
        assert pow(omega, 2 ** s, p) == 1
        assert pow(omega, 2 ** (s - 1), p) != 1
    else:
        # These examples have K_q=F_p, so V_q=U_q.
        assert (p - 1) % q == 0
        zeta = next(x for x in range(2, p) if pow(x, q, p) == 1)
        eig = r.linear_constraints(basis, lambda v: r.power(v, p), zeta)
        assert len(eig) == 1
        s = vq(p - 1, q)
        u = eig[0]
        w = r.power(u, (p ** q - 1) // q ** (s + 1))
        omega_vector = r.power(w, q)
        assert all(x == 0 for x in omega_vector[1:])
        omega = omega_vector[0]
        assert pow(omega, q ** s, p) == 1
        assert pow(omega, q ** (s - 1), p) != 1
    return {"p": p, "q": q, "ell": ell, "ambient_dimension": ell - 1,
            "invariant_dimension": len(basis), "Frobenius_fixed_dimension": len(fixed),
            "primary_generator": omega, "primary_order": q ** vq(p - 1, q)}


if __name__ == "__main__":
    for p, q in [(5, 2), (7, 2), (13, 2), (7, 3), (13, 3), (11, 5), (31, 5)]:
        print(json.dumps(check(p, q), sort_keys=True))

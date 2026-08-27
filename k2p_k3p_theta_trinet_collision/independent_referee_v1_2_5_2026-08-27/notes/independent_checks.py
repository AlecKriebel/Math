#!/usr/bin/env python3
"""Independent arithmetic checks reconstructed from the v1.2.5 manuscript."""

from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import permutations, product


LABELS = range(4)  # A,C,G,T as 0,1,2,3 with group law xor.
CHARS = (
    (1, 1, 1, 1),
    (1, 1, -1, -1),
    (1, -1, 1, -1),
    (1, -1, -1, 1),
)


def invrow(v):
    _, c, g, t = v
    return (
        (1 + c + g + t) / 4,
        (1 + c - g - t) / 4,
        (1 - c + g - t) / 4,
        (1 - c - g + t) / 4,
    )


def theta_q(E1, D2, D3, U, V, A2, A3, B2, B3, d2, d3):
    out = {}
    for x, y, z in product(LABELS, repeat=3):
        if x ^ y ^ z:
            out[x, y, z] = 0
            continue
        core = (
            d2 * d3 * A2[y] * A3[z] * U[y ^ z]
            + d2 * (1 - d3) * A2[y] * B3[z] * U[y] * V[z]
            + (1 - d2) * d3 * B2[y] * A3[z] * V[y] * U[z]
            + (1 - d2) * (1 - d3) * B2[y] * B3[z] * V[y ^ z]
        )
        out[x, y, z] = E1[x] * D2[y] * D3[z] * core
    return out


def invert_q(q):
    out = {}
    for i, j, k in product(LABELS, repeat=3):
        val = 0
        for x, y, z in product(LABELS, repeat=3):
            val += CHARS[x][i] * CHARS[y][j] * CHARS[z][k] * q[x, y, z]
        out[i, j, k] = val / 64
    return out


def transition_matrix(edge):
    increments = invrow(edge)
    return tuple(tuple(increments[i ^ j] for j in LABELS) for i in LABELS)


def star_prune(alpha, beta, gamma):
    mats = tuple(transition_matrix(e) for e in (alpha, beta, gamma))
    out = {}
    for obs in product(LABELS, repeat=3):
        out[obs] = sum(
            mats[0][s][obs[0]] * mats[1][s][obs[1]] * mats[2][s][obs[2]]
            for s in LABELS
        ) / 4
    return out


def theta_prune(root_leaf, root_u, D2, D3, U, V, A2, A3, B2, B3, d2, d3):
    """Literal ordinary-state pruning on each of the four retained rooted graphs."""
    mats = {name: transition_matrix(edge) for name, edge in (
        ("root_leaf", root_leaf), ("root_u", root_u), ("D2", D2), ("D3", D3),
        ("U", U), ("V", V), ("A2", A2), ("A3", A3), ("B2", B2), ("B3", B3),
    )}
    out = {}
    switchings = ((True, True, d2 * d3), (True, False, d2 * (1 - d3)),
                  (False, True, (1 - d2) * d3), (False, False, (1 - d2) * (1 - d3)))
    for obs1, obs2, obs3 in product(LABELS, repeat=3):
        total = 0
        for p2, p3, weight in switchings:
            lr2 = [mats["D2"][s][obs2] for s in LABELS]
            lr3 = [mats["D3"][s][obs3] for s in LABELS]
            lp = []
            lq = []
            for state in LABELS:
                pp = 1
                qq = 1
                if p2:
                    pp *= sum(mats["A2"][state][r] * lr2[r] for r in LABELS)
                else:
                    qq *= sum(mats["B2"][state][r] * lr2[r] for r in LABELS)
                if p3:
                    pp *= sum(mats["A3"][state][r] * lr3[r] for r in LABELS)
                else:
                    qq *= sum(mats["B3"][state][r] * lr3[r] for r in LABELS)
                lp.append(pp)
                lq.append(qq)
            lu = []
            for state in LABELS:
                to_p = sum(mats["U"][state][p] * lp[p] for p in LABELS)
                to_q = sum(mats["V"][state][q] * lq[q] for q in LABELS)
                lu.append(to_p * to_q)
            retained = sum(
                mats["root_leaf"][rho][obs1]
                * sum(mats["root_u"][rho][u] * lu[u] for u in LABELS)
                for rho in LABELS
            ) / 4
            total += weight * retained
        out[obs1, obs2, obs3] = total
    return out


def determinant(a):
    a = [list(row) for row in a]
    n = len(a)
    ans = 1
    sign = 1
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j] != 0), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            sign *= -1
        p = a[j][j]
        ans *= p
        for i in range(j + 1, n):
            r = a[i][j] / p
            for k in range(j + 1, n):
                a[i][k] -= r * a[j][k]
    return sign * ans


def solve_linear(a, b):
    a = [list(row) + [rhs] for row, rhs in zip(a, b)]
    n = len(a)
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j] != 0)
        a[j], a[pivot] = a[pivot], a[j]
        p = a[j][j]
        a[j] = [x / p for x in a[j]]
        for i in range(n):
            if i == j:
                continue
            p = a[i][j]
            a[i] = [x - p * y for x, y in zip(a[i], a[j])]
    return tuple(row[-1] for row in a)


class NumberField:
    """Tiny exact Q[x]/(x^n-sum(red[i]x^i)) implementation."""

    def __init__(self, red, symbol):
        self.red = tuple(F(x) for x in red)
        self.n = len(self.red)
        self.symbol = symbol

    def elt(self, *coeffs):
        coeffs = list(coeffs) + [0] * (self.n - len(coeffs))
        return NFElement(self, tuple(F(x) for x in coeffs[: self.n]))

    @property
    def zero(self):
        return self.elt(0)

    @property
    def one(self):
        return self.elt(1)

    @property
    def gen(self):
        return self.elt(0, 1)


class NFElement:
    def __init__(self, field, coeffs):
        self.field = field
        self.c = coeffs

    def _coerce(self, other):
        if isinstance(other, NFElement):
            assert other.field is self.field
            return other
        return self.field.elt(other)

    def __add__(self, other):
        if "Jet" in globals() and isinstance(other, Jet):
            return other + self
        other = self._coerce(other)
        return NFElement(self.field, tuple(a + b for a, b in zip(self.c, other.c)))

    __radd__ = __add__

    def __neg__(self):
        return NFElement(self.field, tuple(-a for a in self.c))

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __mul__(self, other):
        if "Jet" in globals() and isinstance(other, Jet):
            return other * self
        other = self._coerce(other)
        n = self.field.n
        raw = [F(0) for _ in range(2 * n - 1)]
        for i, a in enumerate(self.c):
            for j, b in enumerate(other.c):
                raw[i + j] += a * b
        for d in range(2 * n - 2, n - 1, -1):
            a = raw[d]
            for i, r in enumerate(self.field.red):
                raw[d - n + i] += a * r
        return NFElement(self.field, tuple(raw[:n]))

    __rmul__ = __mul__

    def inverse(self):
        n = self.field.n
        # Column j is self*x^j in the power basis.
        cols = []
        x = self.field.gen
        for j in range(n):
            cols.append((self * (x ** j)).c)
        aug = [[cols[j][i] for j in range(n)] + [F(i == 0)] for i in range(n)]
        for j in range(n):
            p = next(i for i in range(j, n) if aug[i][j] != 0)
            aug[j], aug[p] = aug[p], aug[j]
            q = aug[j][j]
            aug[j] = [v / q for v in aug[j]]
            for i in range(n):
                if i == j:
                    continue
                q = aug[i][j]
                aug[i] = [u - q * v for u, v in zip(aug[i], aug[j])]
        return NFElement(self.field, tuple(aug[i][-1] for i in range(n)))

    def __truediv__(self, other):
        return self * self._coerce(other).inverse()

    def __rtruediv__(self, other):
        return self._coerce(other) / self

    def __pow__(self, n):
        assert n >= 0
        ans = self.field.one
        a = self
        while n:
            if n & 1:
                ans *= a
            a *= a
            n //= 2
        return ans

    def __eq__(self, other):
        try:
            return self.c == self._coerce(other).c
        except (AssertionError, TypeError):
            return False

    def __float__(self):
        raise TypeError("supply a numerical value for the field generator")

    def evaluate(self, x):
        x = Decimal(x)
        return sum(Decimal(a.numerator) / Decimal(a.denominator) * x**i for i, a in enumerate(self.c))

    def __repr__(self):
        return f"{self.c}"


class Jet:
    def __init__(self, value, derivs):
        self.v = value
        self.d = tuple(derivs)

    def _coerce(self, other):
        if isinstance(other, Jet):
            return other
        return Jet(other, (0,) * len(self.d))

    def __add__(self, other):
        other = self._coerce(other)
        return Jet(self.v + other.v, (a + b for a, b in zip(self.d, other.d)))

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.v, (-a for a in self.d))

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __mul__(self, other):
        other = self._coerce(other)
        return Jet(self.v * other.v, (a * other.v + self.v * b for a, b in zip(self.d, other.d)))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self._coerce(other)
        return Jet(
            self.v / other.v,
            ((a * other.v - self.v * b) / (other.v * other.v) for a, b in zip(self.d, other.d)),
        )

    def __rtruediv__(self, other):
        return self._coerce(other) / self

    def __pow__(self, n):
        ans = self._coerce(1)
        for _ in range(n):
            ans *= self
        return ans

    def __eq__(self, other):
        other = self._coerce(other)
        return self.v == other.v and self.d == other.d


def var(value, j, n):
    d = [0] * n
    d[j] = 1
    return Jet(value, d)


def k2p(s, g):
    return (1, s, g, s)


class SqrtPair:
    """a+b*t with t^2=d over an exact base field."""

    def __init__(self, a, b=0, d=1423):
        self.a, self.b, self.d = a, b, d

    def _coerce(self, other):
        return other if isinstance(other, SqrtPair) else SqrtPair(other, 0, self.d)

    def __add__(self, other):
        other = self._coerce(other)
        return SqrtPair(self.a + other.a, self.b + other.b, self.d)

    __radd__ = __add__

    def __neg__(self):
        return SqrtPair(-self.a, -self.b, self.d)

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __mul__(self, other):
        other = self._coerce(other)
        return SqrtPair(self.a * other.a + self.d * self.b * other.b, self.a * other.b + self.b * other.a, self.d)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, SqrtPair):
            den = other.a * other.a - self.d * other.b * other.b
            return self * SqrtPair(other.a / den, -other.b / den, self.d)
        return SqrtPair(self.a / other, self.b / other, self.d)

    def __rtruediv__(self, other):
        return self._coerce(other) / self

    def __pow__(self, n):
        ans = SqrtPair(1, 0, self.d)
        for _ in range(n):
            ans *= self
        return ans

    def __eq__(self, other):
        other = self._coerce(other)
        return self.a == other.a and self.b == other.b and self.d == other.d

    def evaluate(self, x, t):
        def ev(v):
            return v.evaluate(x) if isinstance(v, NFElement) else Decimal(v.numerator) / Decimal(v.denominator) if isinstance(v, F) else Decimal(v)

        return ev(self.a) + ev(self.b) * Decimal(t)


def rational_poly_bounds(v, lo, hi):
    """Rigorous interval enclosure for a power-basis element on positive [lo,hi]."""
    if not isinstance(v, NFElement):
        v = lo * 0 + v
        return v, v
    lower = F(0)
    upper = F(0)
    for i, c in enumerate(v.c):
        a, b = lo**i, hi**i
        if c >= 0:
            lower += c * a
            upper += c * b
        else:
            lower += c * b
            upper += c * a
    return lower, upper


def compact_k2p_checks():
    K = k2p(F(1, 2), F(1, 2))
    U = k2p(F(4, 5), F(19, 30))
    V = k2p(F(7, 240), F(239, 360))
    S = k2p(F(1, 4), F(1, 2))
    T = k2p(F(1, 3), F(1, 27))
    stated_rows = (
        (F(5, 8), F(1, 8), F(1, 8), F(1, 8)),
        (F(97, 120), F(11, 120), F(1, 120), F(11, 120)),
        (F(31, 72), F(121, 1440), F(289, 720), F(121, 1440)),
        (F(1, 2), F(1, 8), F(1, 4), F(1, 8)),
        (F(23, 54), F(13, 54), F(5, 54), F(13, 54)),
    )
    assert tuple(invrow(v) for v in (K, U, V, S, T)) == stated_rows
    E1 = tuple(a * a for a in K)
    qn = theta_q(E1, K, K, U, V, S, S, T, T, F(1, 2), F(1, 2))
    M = {k: qn[k] / (K[k[0]] ** 2 * K[k[1]] * K[k[2]]) for k in qn if not (k[0] ^ k[1] ^ k[2])}
    displayed = (
        (F(1), F(151, 1440), F(3317, 19440), F(151, 1440)),
        (F(151, 1440), F(71, 1600), F(4681, 172800), F(7597, 259200)),
        (F(3317, 19440), F(4681, 172800), F(961, 14400), F(4681, 172800)),
        (F(151, 1440), F(7597, 259200), F(4681, 172800), F(71, 1600)),
    )
    assert tuple(tuple(M[y ^ z, y, z] for z in LABELS) for y in LABELS) == displayed

    Q71 = NumberField((71, 0), "sqrt71")
    eta = Q71.gen
    P = (1, F(151, 36) / eta, F(107, 162), F(151, 36) / eta)
    R = (1, eta / 40, F(31, 120), eta / 40)
    for y, z in product(LABELS, repeat=2):
        assert M[y ^ z, y, z] == P[y ^ z] * R[y] * R[z]
    alpha = tuple(K[i] ** 2 * P[i] for i in LABELS)
    beta = tuple(K[i] * R[i] for i in LABELS)
    qt = {}
    for x, y, z in product(LABELS, repeat=3):
        qt[x, y, z] = alpha[x] * beta[y] * beta[z] if not (x ^ y ^ z) else 0
        assert qt[x, y, z] == qn[x, y, z]
    qn_nf = {k: Q71.elt(v) for k, v in qn.items()}
    pn = invert_q(qn_nf)
    for v in pn.values():
        assert all(c == 0 for c in v.c[1:])
    minp = min(v.c[0] for v in pn.values())
    assert minp == F(1188799, 79626240)
    literal = theta_prune(K, K, K, K, U, V, S, S, T, T, F(1, 2), F(1, 2))
    tree_literal = star_prune(alpha, beta, beta)
    for pattern in product(LABELS, repeat=3):
        assert Q71.elt(literal[pattern]) == pn[pattern] == tree_literal[pattern]
    eta_decimal = Decimal(71).sqrt()
    for edge in (alpha, beta):
        assert all(v.evaluate(eta_decimal) > 0 for v in invrow(edge))
    return K, U, V, S, T


def compact_k2p_rank_check(K, U, V, S, T):
    n = 9
    ar1_s, ar1_g = var(K[1], 0, n), var(K[2], 1, n)
    us, ug = var(U[1], 2, n), var(U[2], 3, n)
    vs, vg = var(V[1], 4, n), var(V[2], 5, n)
    a2s, a2g = var(S[1], 6, n), var(S[2], 7, n)
    b2s = var(T[1], 8, n)
    ar1 = k2p(ar1_s, ar1_g)
    E1 = tuple(ar1[i] * K[i] for i in LABELS)
    q = theta_q(
        E1,
        K,
        K,
        k2p(us, ug),
        k2p(vs, vg),
        k2p(a2s, a2g),
        S,
        k2p(b2s, T[2]),
        T,
        F(1, 2),
        F(1, 2),
    )
    rows = ((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 1, 0), (1, 2, 3), (1, 3, 2), (2, 0, 2), (2, 1, 3), (2, 2, 0))
    det = determinant([q[r].d for r in rows])
    stated = -F(7**2 * 11**2 * 19 * 107 * 151**2 * 15013, 2**60 * 3**25 * 5**10)
    assert det == stated
    return det


def compact_symmetric_family_check(U, V, S, T):
    # Independent differentiation of the two factorization equations (15) in (v,x).
    v = var(U[2], 0, 2)
    x = var(V[2], 1, 2)
    a, b, c, d, u, w = S[1], S[2], T[1], T[2], U[1], V[1]
    MAC = (a * u + c * w) / 2
    MAG = (b * v + d * x) / 2
    MCC = (a * a + 2 * a * c * u * w + c * c) / 4
    MGG = (b * b + 2 * b * d * v * x + d * d) / 4
    MCG = (a * b * u + a * d * u * x + b * c * v * w + c * d * w) / 4
    MCT = (a * a * v + 2 * a * c * u * w + c * c * x) / 4
    e1 = MCG**2 - MAC**2 * MGG
    e2 = MCT**2 * MGG - MAG**2 * MCC**2
    det = determinant((e1.d, e2.d))
    assert det == F(675554683609333, 194995116803358720000000)
    return det


def fixed_order_point_check():
    E1 = k2p(F(69, 100), F(4, 5))
    U = k2p(F(53, 100), F(23, 100))
    V = k2p(F(23, 50), F(3, 20))
    A2 = k2p(F(9, 25), F(89, 100))
    B2 = k2p(F(19, 50), F(17, 50))
    A3 = k2p(F(9, 20), F(21, 100))
    B3 = k2p(F(3, 25), F(39, 50))
    D2 = k2p(F(17, 100), F(19, 100))
    D3 = k2p(F(49, 100), F(27, 100))
    edges = (E1, U, V, A2, B2, A3, B3, D2, D3)
    assert all(0 < x < 1 for e in edges for x in e[1:])
    assert all(x > 0 for e in edges for x in invrow(e))
    q = theta_q(E1, D2, D3, U, V, A2, A3, B2, B3, F(3, 5), F(11, 50))

    def Q(qp):
        return qp[0, 2, 2] * qp[2, 0, 2] * qp[1, 1, 0] ** 2 - qp[0, 0, 0] * qp[2, 2, 0] * qp[3, 1, 2] ** 2

    vals = []
    for perm in permutations(range(3)):
        qp = {idx: q[tuple(idx[perm[i]] for i in range(3))] for idx in product(LABELS, repeat=3)}
        vals.append(Q(qp))
    expected = {
        -F(1622035263547207769829908849883, 122070312500000000000000000000000000000),
        -F(167331432602036163517296212056077, 19531250000000000000000000000000000000000),
        -F(51058092403609003822417228842579, 381469726562500000000000000000000000000000),
    }
    assert set(vals) == expected and all(vals.count(v) == 2 for v in expected)
    p = invert_q(q)
    assert min(p.values()) == F(2920987217429243, 200000000000000000)
    return vals


def continuous_k2p_setup():
    A = 634127002560
    B = -2160769703472
    C = 1746884136303
    D = -169873318739
    L = NumberField((-F(D, A), -F(C, A), -F(B, A)), "ell")
    ell = L.gen
    lo = F(1073231219980, 10**12)
    hi = F(1073231219981, 10**12)

    def poly(x):
        return A * x**3 + B * x**2 + C * x + D

    def deriv(x):
        return 3 * A * x**2 + 2 * B * x + C

    def second(x):
        return 6 * A * x + 2 * B

    assert poly(lo) * poly(hi) < 0
    # p' has one sign throughout this tiny interval, proving uniqueness there.
    assert deriv(lo) * deriv(hi) > 0 and second(lo) * second(hi) > 0
    assert (deriv(lo) > 0) == (deriv(hi) > 0)

    v = F(73394329, 14503216) * ell**2 - F(1453474193, 248626560) * ell + F(4133719, 3669120)
    x = -F(366971645, 99450624) * ell**2 + F(4259402513, 340973568) * ell - F(42362455, 5031936)
    K = tuple(L.elt(z) for z in k2p(F(1, 2), F(1, 2)))
    U = k2p(L.elt(F(3, 4)), v)
    V = k2p(L.elt(F(1, 16)), x)
    S = tuple(L.elt(z) for z in k2p(F(1, 5), F(1, 2)))
    T = tuple(L.elt(z) for z in k2p(F(7, 30), F(1, 15)))
    return L, ell, lo, hi, K, U, V, S, T


def continuous_k2p_checks():
    L, ell, lo, hi, K, U, V, S, T = continuous_k2p_setup()
    E1 = tuple(a * a for a in K)
    qn = theta_q(E1, K, K, U, V, S, S, T, T, F(1, 2), F(1, 2))
    M = {k: qn[k] / (K[k[0]] ** 2 * K[k[1]] * K[k[2]]) for k in qn if not (k[0] ^ k[1] ^ k[2])}

    t = SqrtPair(L.zero, L.one)
    P = (
        SqrtPair(L.one),
        F(79, 4 * 1423) * t,
        SqrtPair(F(73394329, 4762633008) * ell**2 + F(368713223407, 81645137280) * ell - F(4985775401, 1204882560)),
        F(79, 4 * 1423) * t,
    )
    R = (SqrtPair(L.one), t / 240, SqrtPair(ell / 4), t / 240)
    for y, z in product(LABELS, repeat=2):
        assert SqrtPair(M[y ^ z, y, z]) == P[y ^ z] * R[y] * R[z]
    alpha = tuple(SqrtPair(K[i] ** 2) * P[i] for i in LABELS)
    beta = tuple(SqrtPair(K[i]) * R[i] for i in LABELS)
    for x0, y, z in product(LABELS, repeat=3):
        qt = alpha[x0] * beta[y] * beta[z] if not (x0 ^ y ^ z) else SqrtPair(L.zero)
        assert qt == SqrtPair(qn[x0, y, z])

    pn = invert_q(qn)
    enclosures = {k: rational_poly_bounds(v, lo, hi) for k, v in pn.items()}
    candidate = min(enclosures, key=lambda k: enclosures[k][1])
    cand_lo, cand_hi = enclosures[candidate]
    assert all(
        pn[k] == pn[candidate] or cand_hi < bounds[0]
        for k, bounds in enclosures.items()
        if k != candidate
    )
    manuscript_lo = F(149867914232177, 10**16)
    manuscript_hi = F(149867914232311, 10**16)
    assert manuscript_lo < cand_lo <= cand_hi < manuscript_hi

    # Network, effective, and tree K2P continuous-time margins.
    margins = []
    for edge in (K, U, V, S, T, E1):
        margins.append(edge[2] - edge[1] ** 2)
    for edge in (alpha, beta):
        margins.append(edge[2] - edge[1] ** 2)

    getcontext().prec = 70
    ell_d = (Decimal(lo.numerator) / Decimal(lo.denominator) + Decimal(hi.numerator) / Decimal(hi.denominator)) / 2
    for _ in range(12):
        f = Decimal(634127002560) * ell_d**3 - Decimal(2160769703472) * ell_d**2 + Decimal(1746884136303) * ell_d - Decimal(169873318739)
        fp = Decimal(3 * 634127002560) * ell_d**2 - Decimal(2 * 2160769703472) * ell_d + Decimal(1746884136303)
        ell_d -= f / fp
    t_d = Decimal(1423).sqrt()

    def eval_num(v):
        if isinstance(v, SqrtPair):
            return v.evaluate(ell_d, t_d)
        if isinstance(v, NFElement):
            return v.evaluate(ell_d)
        return Decimal(v.numerator) / Decimal(v.denominator)

    margin_values = [eval_num(m) for m in margins]
    assert min(margin_values) == Decimal(11) / Decimal(900)
    for edge in (K, U, V, S, T, E1, alpha, beta):
        assert all(eval_num(x) > 0 for x in invrow(edge))
    pmin_num = eval_num(pn[candidate])
    assert Decimal("0.0149867914232177") < pmin_num < Decimal("0.0149867914232311")
    literal = theta_prune(K, K, K, K, U, V, S, S, T, T, F(1, 2), F(1, 2))
    tree_literal = star_prune(alpha, beta, beta)
    for pattern in product(LABELS, repeat=3):
        assert literal[pattern] == pn[pattern]
        assert SqrtPair(pn[pattern]) == tree_literal[pattern]
    return (L, ell, lo, hi, K, U, V, S, T, ell_d, pmin_num)


def continuous_k2p_rank_check(setup):
    L, ell, lo, hi, K, U, V, S, T, ell_d, _ = setup
    n = 9
    ar1_s, ar1_g = var(K[1], 0, n), var(K[2], 1, n)
    us, ug = var(U[1], 2, n), var(U[2], 3, n)
    vs, vg = var(V[1], 4, n), var(V[2], 5, n)
    a2s, a2g = var(S[1], 6, n), var(S[2], 7, n)
    b2s = var(T[1], 8, n)
    ar1 = k2p(ar1_s, ar1_g)
    E1 = tuple(ar1[i] * K[i] for i in LABELS)
    q = theta_q(
        E1,
        K,
        K,
        k2p(us, ug),
        k2p(vs, vg),
        k2p(a2s, a2g),
        S,
        k2p(b2s, T[2]),
        T,
        F(1, 2),
        F(1, 2),
    )
    rows = ((0, 1, 1), (0, 2, 2), (1, 0, 1), (1, 1, 0), (1, 2, 3), (1, 3, 2), (2, 0, 2), (2, 1, 3), (2, 2, 0))
    det = determinant([q[r].d for r in rows])
    val = det.evaluate(ell_d)
    assert Decimal("-4.129735e-22") < val < Decimal("-4.129729e-22")
    return det, val


def k3p(v1, v2, v3):
    return (1, v1, v2, v3)


def quartic_k3p_setup():
    H = NumberField((F(1, 5), 0, 0, 0), "h")
    h = H.gen
    K = tuple(H.elt(x) for x in k3p(F(1, 2), F(1, 2), F(1, 2)))
    U = k3p(h / 3, h, H.elt(F(1, 3)))
    V = k3p(h, h / 3, H.elt(F(1, 3)))
    S = k3p(3 * h**2 / 4, H.elt(F(1, 4)), H.elt(F(3, 10)))
    T = k3p(H.elt(F(1, 4)), 3 * h**2 / 4, H.elt(F(3, 10)))
    B = k3p(h**2 / 2, h**2 / 2, h**2 / 2)
    P = k3p((5 * h**3 + h) / 4, (5 * h**3 + h) / 4, h**2)
    return H, h, K, U, V, S, T, B, P


def quartic_k3p_checks():
    H, h, K, U, V, S, T, B, P = quartic_k3p_setup()
    E1 = tuple(a * a for a in K)
    qn = theta_q(E1, K, K, U, V, S, S, T, T, F(1, 2), F(1, 2))
    M = {k: qn[k] / (K[k[0]] ** 2 * K[k[1]] * K[k[2]]) for k in qn if not (k[0] ^ k[1] ^ k[2])}
    for y, z in product(LABELS, repeat=2):
        assert M[y ^ z, y, z] == P[y ^ z] * B[y] * B[z]
    alpha = tuple(K[i] ** 2 * P[i] for i in LABELS)
    beta = tuple(K[i] * B[i] for i in LABELS)
    qt = {}
    for x, y, z in product(LABELS, repeat=3):
        qt[x, y, z] = alpha[x] * beta[y] * beta[z] if not (x ^ y ^ z) else H.zero
        assert qt[x, y, z] == qn[x, y, z]

    getcontext().prec = 70
    h_d = Decimal(5) ** (Decimal(-1) / Decimal(4))
    assert Decimal(2) / 3 < h_d < Decimal(7) / 10
    for edge in (K, U, V, S, T, E1, alpha, beta):
        assert all(x.evaluate(h_d) > 0 for x in invrow(edge))
        assert all(Decimal(0) < x.evaluate(h_d) < Decimal(1) for x in edge[1:])
    p = invert_q(qn)
    assert min(x.evaluate(h_d) for x in p.values()) > 0
    literal = theta_prune(K, K, K, K, U, V, S, S, T, T, F(1, 2), F(1, 2))
    tree_literal = star_prune(alpha, beta, beta)
    for pattern in product(LABELS, repeat=3):
        assert literal[pattern] == p[pattern] == tree_literal[pattern]
    assert U[1] != U[2] and U[1] != U[3] and U[2] != U[3]
    a, t = alpha[1], alpha[3]
    assert a == alpha[2] and beta[1] == beta[2] == beta[3]
    assert (a - t).evaluate(h_d) > 0
    assert qn[1, 1, 0] != qn[3, 3, 0]
    return H, h, K, U, V, S, T, B, P, h_d


K3P_ROWS = (
    (0, 1, 1), (0, 2, 2), (0, 3, 3), (1, 0, 1), (1, 1, 0),
    (1, 2, 3), (1, 3, 2), (2, 0, 2), (2, 1, 3), (2, 2, 0),
    (2, 3, 1), (3, 0, 3), (3, 1, 2), (3, 2, 1), (3, 3, 0),
)


def quartic_rank_jets(setup, include_free=False):
    H, h, K, U, V, S, T, B, P, h_d = setup
    n = 17 if include_free else 15

    def c(v):
        return Jet(v, (0,) * n)

    ar1 = [c(x) for x in K]
    ar1[1], ar1[2], ar1[3] = var(K[1], 0, n), var(K[2], 1, n), var(K[3], 2, n)
    Uj = [c(x) for x in U]
    Uj[2] = var(U[2], 3, n)
    A2 = [c(x) for x in S]
    A2[1], A2[2] = var(S[1], 4, n), var(S[2], 5, n)
    B2 = [c(x) for x in T]
    B2[1], B2[2] = var(T[1], 6, n), var(T[2], 7, n)
    A3 = [c(x) for x in S]
    A3[1], A3[2] = var(S[1], 8, n), var(S[2], 9, n)
    B3 = [c(x) for x in T]
    B3[1], B3[2] = var(T[1], 10, n), var(T[2], 11, n)
    D2 = [c(x) for x in K]
    D3 = [c(x) for x in K]
    D2[3], D3[3] = var(K[3], 12, n), var(K[3], 13, n)
    d3 = var(H.elt(F(1, 2)), 14, n)
    Vj = [c(x) for x in V]
    if include_free:
        Uj[1] = var(U[1], 15, n)
        Vj[2] = var(V[2], 16, n)
    E1 = tuple(ar1[i] * K[i] for i in LABELS)
    q = theta_q(E1, D2, D3, Uj, Vj, A2, A3, B2, B3, H.elt(F(1, 2)), d3)
    return q


def quartic_k3p_rank_and_tangent_check(setup):
    H, h, K, U, V, S, T, B, P, h_d = setup
    q = quartic_rank_jets(setup)
    J = [q[r].d for r in K3P_ROWS]
    det = determinant(J)
    stated = h * (10 * h**2 + 1) / (2**61 * 3**4 * 5**14)
    assert det == stated

    q17 = quartic_rank_jets(setup, include_free=True)
    J17 = [q17[r].d for r in K3P_ROWS]
    tangent = (
        -F(3, 19) * h - F(375, 304) * h**3,
        -F(621, 152) * h + F(1875, 304) * h**3,
        H.zero,
        -F(6, 19) + F(60, 19) * h**2,
        -F(117, 304) * h + F(459, 608) * h**3,
        -F(75, 608) * h - F(195, 304) * h**3,
        -F(255, 608) * h + F(135, 304) * h**3,
        F(9, 304) * h - F(9, 608) * h**3,
        -F(117, 304) * h + F(459, 608) * h**3,
        -F(75, 608) * h - F(195, 304) * h**3,
        -F(255, 608) * h + F(135, 304) * h**3,
        F(9, 304) * h - F(9, 608) * h**3,
        H.zero,
        H.zero,
        H.zero,
    )
    solved_tangent = solve_linear([row[:15] for row in J17], [-(row[15] + row[16]) for row in J17])
    if solved_tangent != tangent:
        for i, (got, shown) in enumerate(zip(solved_tangent, tangent)):
            if got != shown:
                print("K3P tangent mismatch", i, "solved", got, "transcribed", shown)
    for i, row in enumerate(J17):
        residual = sum((row[j] * tangent[j] for j in range(15)), H.zero) + row[15] + row[16]
        if residual != 0:
            print("nonzero K3P tangent residual", i, residual)
        assert residual == 0
    d_margin_u = 1 - tangent[3] * U[3]
    stated_u = (21 - 20 * h**2) / 19
    assert d_margin_u == stated_u == (10 * h**2 - 1) / (1 + 10 * h**2)
    d_margin_v = H.one
    assert d_margin_v == 1

    # Audit all base network continuous-time inequalities and the claimed tree margins.
    def margins(edge):
        return (edge[1] - edge[2] * edge[3], edge[2] - edge[1] * edge[3], edge[3] - edge[1] * edge[2])

    base_margins = {"K": margins(K), "U": margins(U), "V": margins(V), "S": margins(S), "T": margins(T)}
    assert base_margins["U"][0] == 0 and base_margins["V"][1] == 0
    assert all(m.evaluate(h_d) > 0 for key, ms in base_margins.items() for i, m in enumerate(ms) if not (key == "U" and i == 0) and not (key == "V" and i == 1))
    alpha = tuple(K[i] ** 2 * P[i] for i in LABELS)
    beta = tuple(K[i] * B[i] for i in LABELS)
    assert all(m.evaluate(h_d) > 0 for edge in (alpha, beta) for m in margins(edge))
    a, t = alpha[1], alpha[3]
    assert margins(alpha) == (a * (1 - t), a * (1 - t), h**2 * (58 - 10 * h**2) / 256)
    assert margins(beta) == (h**2 / 4 - F(1, 80),) * 3
    return det


def main():
    K, U, V, S, T = compact_k2p_checks()
    d9 = compact_k2p_rank_check(K, U, V, S, T)
    d2 = compact_symmetric_family_check(U, V, S, T)
    qvals = fixed_order_point_check()
    ct_setup = continuous_k2p_checks()
    _, ct_det = continuous_k2p_rank_check(ct_setup)
    k3_setup = quartic_k3p_checks()
    k3_det = quartic_k3p_rank_and_tangent_check(k3_setup)
    print("compact K2P collision: exact factorization, stochasticity, and 64-pattern minimum verified")
    print("K2P rank-9 determinant:", d9)
    print("symmetric-family 2x2 determinant:", d2)
    print("fixed-order rational point: all six Q values negative; distinct values:", sorted(set(qvals)))
    print("continuous-time K2P: exact factorization and rigorous p_min enclosure verified")
    print("continuous-time K2P rank determinant (decimal):", ct_det)
    print("quartic K3P collision, rank-15 determinant, and IFT tangent: exact checks passed")
    print("K3P rank determinant:", k3_det)


if __name__ == "__main__":
    main()

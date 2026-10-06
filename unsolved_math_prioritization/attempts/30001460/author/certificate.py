#!/usr/bin/env python3
"""Exact rank-one identities only; no general quotient theorem is encoded."""
import json

N = 5
ZERO = (0,) * N


class P:
    """Sparse Laurent polynomials over Z in a,b,t,c,z."""
    def __init__(self, terms=None):
        if isinstance(terms, int):
            terms = {ZERO: terms}
        self.terms = {tuple(m): v for m, v in (terms or {}).items() if v}
        if any(len(m) != N or not all(isinstance(i, int) for i in m)
               or not isinstance(v, int) for m, v in self.terms.items()):
            raise ValueError("invalid Laurent polynomial")

    @staticmethod
    def coerce(value):
        return value if isinstance(value, P) else P(value)

    def __eq__(self, other):
        return self.terms == P.coerce(other).terms

    def __add__(self, other):
        out = dict(self.terms)
        for m, v in P.coerce(other).terms.items():
            out[m] = out.get(m, 0) + v
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -v for m, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-P.coerce(other))

    def __mul__(self, other):
        out = {}
        for m, v in self.terms.items():
            for n, w in P.coerce(other).terms.items():
                exponent = tuple(x + y for x, y in zip(m, n))
                out[exponent] = out.get(exponent, 0) + v * w
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, power):
        if not isinstance(power, int):
            raise ValueError("integer power required")
        if power < 0:
            if len(self.terms) != 1:
                raise ValueError("only signed monomial units may be inverted")
            m, v = next(iter(self.terms.items()))
            if v not in (1, -1):
                raise ValueError("not a unit over Z")
            return P({tuple(power * x for x in m): v ** (-power)})
        result = P(1)
        for _ in range(power):
            result = result * self
        return result


def var(i):
    m = [0] * N
    m[i] = 1
    return P({tuple(m): 1})


def mat(a, b, c, d):
    return [[P.coerce(a), P.coerce(b)], [P.coerce(c), P.coerce(d)]]


def mul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(2)), P())
             for j in range(2)] for i in range(2)]


def scale(c, A):
    return [[c * x for x in row] for row in A]


def bracket(A, B):
    C, D = mul(A, B), mul(B, A)
    return [[C[i][j] - D[i][j] for j in range(2)] for i in range(2)]


def calculate():
    a, b, t, c, z = (var(i) for i in range(N))
    checks = []

    def check(name, left, right):
        if left != right:
            raise ValueError("identity failed: " + name)
        checks.append(name)

    E, F, H = mat(0, 1, 0, 0), mat(0, 0, 1, 0), mat(1, 0, 0, -1)
    X = mat(0, a, b, 0)
    J = mat(1, 0, 0, -1)
    check("sl2_EF", bracket(E, F), H)
    check("sl2_HE", bracket(H, E), scale(2, E))
    check("sl2_HF", bracket(H, F), scale(-2, F))
    check("theta_squared", mul(J, J), mat(1, 0, 0, 1))
    check("theta_E", mul(mul(J, E), J), scale(-1, E))
    check("theta_F", mul(mul(J, F), J), scale(-1, F))
    check("theta_H", mul(mul(J, H), J), H)
    check("p_centralizer_f", bracket(X, F), scale(a, H))
    check("p_centralizer_e", bracket(X, E), scale(-b, H))
    check("effective_torus_action", mul(mul(mat(t, 0, 0, 1), X),
          mat(t ** -1, 0, 0, 1)), mat(0, t * a, t ** -1 * b, 0))
    check("invariant_product", (t * a) * (t ** -1 * b), a * b)
    check("plus_chart_product", t * (c * t ** -1), c)
    check("minus_chart_product", (c * t) * (t ** -1), c)
    check("plus_chart_inverse_a", a, a)
    check("plus_chart_inverse_b", (a * b) * a ** -1, b)
    check("minus_chart_inverse_a", (a * b) * b ** -1, a)
    check("minus_chart_inverse_b", (b ** -1) ** -1, b)
    check("plus_section_to_minus_a", c * P(1), c)
    check("plus_section_to_minus_b", c ** -1 * c, P(1))
    check("generic_curve_orbit_a", z * P(1), z)
    check("generic_curve_orbit_b", z ** -1 * z, P(1))
    check("opposite_triple_FE", bracket(F, E), scale(-1, H))
    check("opposite_triple_HF", bracket(scale(-1, H), F), scale(2, F))
    # Mutation-style mathematical negative control: wrong second weight.
    if (t * a) * (t * b) == a * b:
        raise ValueError("wrong-weight negative control was not detected")
    if (P(1), P(0)) == (P(0), P(1)):
        raise ValueError("axis representatives unexpectedly coincide")
    return {"schema": 1, "arithmetic": "exact Laurent polynomials over Z",
            "identities_passed": len(checks), "identity_names": checks,
            "wrong_weight_negative_control": "rejected",
            "axis_representatives": "distinct",
            "scope": "rank-one formulas only; general theorem is a prose proof"}


if __name__ == "__main__":
    print(json.dumps(calculate(), indent=2, sort_keys=True))

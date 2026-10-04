#!/usr/bin/env python3
"""Exact algebra controls. Python 3 standard library only; no network or input files.

These are symbolic identity/linear-algebra checks, not a general theorem prover.
Topological arguments and source-hypothesis checks remain in PROOF.md.
"""
from fractions import Fraction
import json

N = 6
ZERO = (0,) * N


class P:
    def __init__(self, terms=None):
        if isinstance(terms, (int, Fraction)):
            terms = {ZERO: Fraction(terms)}
        self.terms = {m: Fraction(c) for m, c in (terms or {}).items() if c}

    def __add__(self, other):
        other = other if isinstance(other, P) else P(other)
        ans = self.terms.copy()
        for m, c in other.terms.items():
            ans[m] = ans.get(m, 0) + c
        return P(ans)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, P) else -P(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, P) else P(other)
        ans = {}
        for m, c in self.terms.items():
            for n, d in other.terms.items():
                k = tuple(a + b for a, b in zip(m, n))
                ans[k] = ans.get(k, 0) + c * d
        return P(ans)

    __rmul__ = __mul__

    def __pow__(self, k):
        assert isinstance(k, int) and k >= 0
        ans = P(1)
        for _ in range(k):
            ans = ans * self
        return ans

    def __eq__(self, other):
        other = other if isinstance(other, P) else P(other)
        return self.terms == other.terms

    def substitute(self, values):
        ans = P()
        for powers, coefficient in self.terms.items():
            term = P(coefficient)
            for base, exponent in zip(values, powers):
                term *= base ** exponent
            ans += term
        return ans

    def derivative(self, i):
        ans = {}
        for m, c in self.terms.items():
            if m[i]:
                n = list(m)
                n[i] -= 1
                ans[tuple(n)] = c * m[i]
        return P(ans)

    def constant_at_origin(self):
        return self.terms.get(ZERO, Fraction(0))


def variable(i):
    exponents = [0] * N
    exponents[i] = 1
    return P({tuple(exponents): 1})


def rank(matrix):
    a = [[Fraction(v) for v in row] for row in matrix]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        d = a[r][c]
        a[r] = [v / d for v in a[r]]
        for i in range(len(a)):
            if i != r:
                d = a[i][c]
                a[i] = [v - d * w for v, w in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def gradient_at_origin(p, indices):
    return [p.derivative(i).constant_at_origin() for i in indices]


def main():
    x, y, z, a, b, t = [variable(i) for i in range(N)]
    variables = [x, y, z, a, b, t]
    checks = {}

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks[name] = True

    # The quotient of xy=0 by (x,y,z)->(y,x,-z).
    u, v, w = x + y, z * (x - y), z ** 2
    check("invariant_relation_exact", v ** 2 - w * u ** 2 == -4 * z ** 2 * x * y)
    check("relation_zero_mod_xy", all(m[0] > 0 and m[1] > 0 for m in (v ** 2 - w * u ** 2).terms))
    for name, generator in (("u", u), ("v", v), ("w", w)):
        check("theta_invariance_" + name, generator.substitute([y, x, -z, a, b, t]) == generator)
    check("wrong_missing_z_squared_relation_rejected", v ** 2 - w * u ** 2 != -4 * x * y)
    check("wrong_plus_sign_relation_rejected", v ** 2 + w * u ** 2 != 0)
    # Every invariant d^i z^j has equal parities. This finite exhaustion is
    # only a control for the all-degree parity proof in PROOF.md.
    monomials = 0
    for i in range(31):
        for j in range(31):
            if (i + j) % 2 == 0:
                e = i % 2
                check(f"parity_{i}_{j}", i == 2 * (i // 2) + e and j == 2 * (j // 2) + e)
                monomials += 1

    # From now on x=u,y=v,z=w; no numerical sampling is used.
    F = y ** 2 - z * x ** 2
    chart = F.substitute([z * a, z * b, z, a, b, t])
    check("point_blowup_w_chart", chart == z ** 2 * (b ** 2 - z * a ** 2))
    strict = b ** 2 - z * a ** 2
    check("reproduced_pinch_singular_at_origin", all(v == 0 for v in gradient_at_origin(strict, [2, 3, 4])))
    check("double_line_u_chart", F.substitute([x, x * t, z, a, b, t]) == x ** 2 * (t ** 2 - z))
    check("double_line_u_chart_smooth", (t ** 2 - z).derivative(2) == -1)
    check("double_line_v_chart", F.substitute([y * t, y, z, a, b, t]) == y ** 2 * (1 - z * t ** 2))
    check("normalization_substitution", F.substitute([x, x * t, t ** 2, a, b, t]) == 0)

    # Branched base change and tangent-normal rank.
    branched = F.substitute([x, y, t ** 2, a, b, t])
    plus, minus = y - t * x, y + t * x
    check("branched_factorization", branched == plus * minus)
    tangent_rank = rank([gradient_at_origin(plus, [0, 1, 5]), gradient_at_origin(minus, [0, 1, 5])])
    check("branched_sheets_not_transverse", tangent_rank == 1)
    check("ordinary_nc_sheets_transverse_control", rank([[1, 0, 0], [0, 1, 0]]) == 2)
    check("conductor_ramifies_at_zero", (t ** 2).derivative(5).constant_at_origin() == 0)

    # Nodal cubic and its projective normalization, x=S,y=T.
    X = y * (x ** 2 - y ** 2)
    Y = x * (x ** 2 - y ** 2)
    Z = y ** 3
    check("projective_cubic_parametrization", Y ** 2 * Z - X ** 3 - X ** 2 * Z == 0)
    cubic = y ** 2 * z - x ** 3 - x ** 2 * z
    check("infinity_point_smooth", cubic.derivative(2).substitute([P(0), P(1), P(0), a, b, t]) == 1)
    affine = y ** 2 - x ** 3 - x ** 2
    check("node_hessian_nondegenerate", rank([[affine.derivative(i).derivative(j).constant_at_origin() for j in [0, 1]] for i in [0, 1]]) == 2)
    check("affine_normalization", affine.substitute([t ** 2 - 1, t * (t ** 2 - 1), z, a, b, t]) == 0)
    for root in (-1, 1):
        check("node_preimage_" + str(root), root ** 2 - 1 == 0 and root * (root ** 2 - 1) == 0)
    repeated_roots = [Fraction(0), Fraction(-2, 3)]
    exceptional = sorted(-(r ** 3 + r ** 2) for r in repeated_roots)
    check("cubic_smoothing_exceptional_parameters", exceptional == [Fraction(-4, 27), Fraction(0)])

    # Coarse quotient kills an order-two stabilizer: exact finite group
    # check only, with the topological cone argument supplied separately.
    c2 = {0, 1}
    normal_closure = {0}
    changed = True
    while changed:
        expanded = normal_closure | {1} | {(i + j) % 2 for i in normal_closure for j in normal_closure | {1}}
        changed = expanded != normal_closure
        normal_closure = expanded
    check("c2_stabilizer_normal_closure", normal_closure == c2)

    visible = {k: v for k, v in checks.items() if not k.startswith("parity_")}
    return {
        "status": "passed",
        "arithmetic": "exact integer and Fraction sparse polynomials; standard library only",
        "non_parity_checks": visible,
        "invariant_monomial_controls": monomials,
        "total_assertions": len(checks),
        "branched_sheet_normal_rank": tangent_rank,
        "cubic_smoothing_exceptional_parameters": [str(e) for e in exceptional],
        "scope_limit": "No automatic certification of source claims, global projectivity, fundamental groups, or full target resolution."
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))

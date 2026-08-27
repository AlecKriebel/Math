#!/usr/bin/env python3
"""Independent rational-interval replay of the sharpness box.

The network maps are rebuilt directly from the two literal rooted DAGs and
the Fourier switching formula in the article.  Only the numerical box,
parameter scaling, and chosen rank columns are read from the certificate.
Stored interval Jacobians, Krawczyk operators, physical PASS records, and
rank matrices are ignored and then compared with the fresh results.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from pathlib import Path
import sys

sys.set_int_max_str_digits(0)


CERT = Path("../package_copy/proof_package/sharpness/K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json")
ORDER3 = (
    "000", "0CC", "0GG", "0TT", "C0C", "CC0", "CGT", "CTG",
    "G0G", "GCT", "GG0", "GTC", "T0T", "TCG", "TGC", "TT0",
)
CH = {x: i for i, x in enumerate("0CGT")}


def rat(x) -> Q:
    return Q(str(x))


@dataclass(frozen=True)
class I:
    lo: Q
    hi: Q

    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError((self.lo, self.hi))

    @staticmethod
    def point(x):
        x = rat(x)
        return I(x, x)

    def __add__(self, other):
        other = as_interval(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_interval(other))

    def __rsub__(self, other):
        return as_interval(other) - self

    def __mul__(self, other):
        other = as_interval(other)
        vals = (self.lo * other.lo, self.lo * other.hi,
                self.hi * other.lo, self.hi * other.hi)
        return I(min(vals), max(vals))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_interval(other)
        if other.lo <= 0 <= other.hi:
            raise ZeroDivisionError(other)
        return self * I(min(1 / other.lo, 1 / other.hi),
                        max(1 / other.lo, 1 / other.hi))

    def absmax(self):
        return max(abs(self.lo), abs(self.hi))


def as_interval(x):
    return x if isinstance(x, I) else I.point(x)


def zero_like(values):
    return I.point(0) if values and isinstance(values[0], I) else Q(0)


def one_like(values):
    return I.point(1) if values and isinstance(values[0], I) else Q(1)


def multiply(values, one):
    out = one
    for value in values:
        out = out * value
    return out


def interval_pair(pair):
    return I(rat(pair[0]), rat(pair[1]))


def matrix_inverse(a):
    n = len(a)
    m = [[rat(a[i][j]) for j in range(n)] + [Q(i == j) for j in range(n)]
         for i in range(n)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if m[i][col])
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
        p = m[col][col]
        m[col] = [x / p for x in m[col]]
        for i in range(n):
            if i == col or not m[i][col]:
                continue
            f = m[i][col]
            m[i] = [x - f * y for x, y in zip(m[i], m[col])]
    return [row[n:] for row in m]


def determinant(a):
    m = [[rat(x) for x in row] for row in a]
    ans = Q(1)
    for col in range(len(m)):
        pivot = next((i for i in range(col, len(m)) if m[i][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            ans = -ans
        p = m[col][col]
        ans *= p
        for i in range(col + 1, len(m)):
            if m[i][col]:
                f = m[i][col] / p
                for j in range(col + 1, len(m)):
                    m[i][j] -= f * m[col][j]
    return ans


def matmul(a, b):
    n, k, m = len(a), len(b), len(b[0])
    out = []
    for i in range(n):
        row = []
        for j in range(m):
            seed = I.point(0) if any(isinstance(a[i][z], I) or isinstance(b[z][j], I)
                                     for z in range(k)) else Q(0)
            row.append(sum((a[i][z] * b[z][j] for z in range(k)), seed))
        out.append(row)
    return out


def matvec(a, x):
    b = [[v] for v in x]
    return [row[0] for row in matmul(a, b)]


def identity_minus(a):
    return [[Q(i == j) - a[i][j] for j in range(len(a))] for i in range(len(a))]


def inf_norm_interval(a):
    return max(sum(as_interval(x).absmax() for x in row) for row in a)


class LiteralNetwork:
    def __init__(self, record):
        self.arcs = [tuple(x) for x in record["arcs"]]
        self.labels = {node: int(label) for node, label in record["labels"]}
        self.retics = list(record["reticulations"])
        self.parent0 = dict(zip(self.retics, record["parent0"]))
        self.parents = {r: [u for u, v in self.arcs if v == r] for r in self.retics}
        assert all(self.parent0[r] in self.parents[r] and len(self.parents[r]) == 2
                   for r in self.retics)
        self.switchings = []
        for choices in product((0, 1), repeat=len(self.retics)):
            # choice 1 selects parent0 with probability lambda; choice 0
            # selects the other parent with probability 1-lambda.
            selected = {}
            for r, choice in zip(self.retics, choices):
                other = next(p for p in self.parents[r] if p != self.parent0[r])
                selected[r] = self.parent0[r] if choice else other
            kept = [e for e in self.arcs if e[1] not in selected or e[0] == selected[e[1]]]
            masks = self._descendant_masks(kept)
            self.switchings.append((choices, kept, masks))

    def _descendant_masks(self, kept):
        children = {}
        for u, v in kept:
            children.setdefault(u, []).append(v)
            children.setdefault(v, [])
        memo = {}

        def visit(v):
            if v in memo:
                return memo[v]
            mask = (1 << self.labels[v]) if v in self.labels else 0
            for w in children.get(v, []):
                mask |= visit(w)
            memo[v] = mask
            return mask

        for u, v in kept:
            visit(u)
            visit(v)
        return {e: memo[e[1]] for e in kept}

    @staticmethod
    def sector(mask, chars):
        ans = 0
        i = 0
        while mask:
            if mask & 1:
                ans ^= chars[i]
            mask >>= 1
            i += 1
        return ans

    def value_and_jacobian(self, params):
        """Return 15 normalized outputs and their 15-by-32 Jacobian."""
        assert len(params) == 32
        one = one_like(params)
        zero = zero_like(params)
        outputs = []
        jac = []
        for word in ORDER3[1:]:
            chars = tuple(CH[x] for x in word)
            value = zero
            row = [zero for _ in range(32)]
            for choices, kept, masks in self.switchings:
                inheritance_factors = [params[30 + j] if choice else 1 - params[30 + j]
                                       for j, choice in enumerate(choices)]
                edge_factors = []
                edge_columns = []
                for edge_index, edge in enumerate(self.arcs):
                    if edge not in masks:
                        continue
                    s = self.sector(masks[edge], chars)
                    if s:
                        edge_factors.append(params[3 * edge_index + s - 1])
                        edge_columns.append(3 * edge_index + s - 1)
                weight = multiply(inheritance_factors, one)
                edge_product = multiply(edge_factors, one)
                value += weight * edge_product
                for k, col in enumerate(edge_columns):
                    derivative_product = multiply(edge_factors[:k] + edge_factors[k + 1:], one)
                    row[col] += weight * derivative_product
                for j, choice in enumerate(choices):
                    other_weights = multiply(inheritance_factors[:j] + inheritance_factors[j + 1:], one)
                    row[30 + j] += (1 if choice else -1) * other_weights * edge_product
            outputs.append(value)
            jac.append(row)
        return outputs, jac


def exact_equal_matrix(a, stored):
    return all(rat(stored[i][j]) == a[i][j]
               for i in range(len(a)) for j in range(len(a[i])))


def lower_bound(expr):
    return as_interval(expr).lo


def physical_bounds(params):
    categories = {"eigen": [], "transition": [], "ct": [], "inheritance": []}
    for edge in range(10):
        c, g, t = params[3*edge:3*edge+3]
        categories["eigen"].extend((lower_bound(c), lower_bound(g), lower_bound(t),
                                     lower_bound(1-c), lower_bound(1-g), lower_bound(1-t)))
        categories["transition"].extend((
            lower_bound((1+c+g+t) * Q(1, 4)),
            lower_bound((1+c-g-t) * Q(1, 4)),
            lower_bound((1-c+g-t) * Q(1, 4)),
            lower_bound((1-c-g+t) * Q(1, 4)),
        ))
        categories["ct"].extend((lower_bound(c-g*t), lower_bound(g-c*t), lower_bound(t-c*g)))
    for lam in params[30:]:
        categories["inheritance"].extend((lower_bound(lam), lower_bound(1-lam)))
    return {k: min(v) for k, v in categories.items()}


def decimal(x, digits=12):
    x = rat(x)
    with localcontext() as ctx:
        ctx.prec = digits + 8
        value = Decimal(x.numerator) / Decimal(x.denominator)
        return f"{value:.{digits}E}"


def exact_summary(x):
    x = rat(x)
    encoded = str(x).encode()
    return {
        "decimal": decimal(x),
        "exact_fraction_sha256": hashlib.sha256(encoded).hexdigest(),
        "numerator_digits": len(str(abs(x.numerator))),
        "denominator_digits": len(str(x.denominator)),
        "sign": -1 if x < 0 else 1 if x > 0 else 0,
    }


def main():
    data = json.loads(CERT.read_text())
    par = data["parameterization"]
    box = [interval_pair(x) for x in par["direct_parameter_box"]]
    point = [rat(x) for x in par["direct_parameter_point"]]
    y0 = [rat(x) for x in par["scaled_variable_center"]]
    radius = rat(par["box_radius"])
    pivots = list(par["pivot_global_columns"])
    scales = [rat(x) for x in par["multiplicative_scales_for_pivots_and_values_for_frozen_parameters"]]
    row_scales = [rat(x) for x in par["row_scales"]]

    assert len(box) == len(point) == len(scales) == 64
    assert all(point[col] == scales[col] * y0[j] for j, col in enumerate(pivots))
    assert all(box[col] == I(scales[col] * (y0[j] - radius), scales[col] * (y0[j] + radius))
               for j, col in enumerate(pivots))

    W = LiteralNetwork(data["primitive_networks"]["W"])
    Wp = LiteralNetwork(data["primitive_networks"]["Wprime"])
    qW0, jW0 = W.value_and_jacobian(point[:32])
    qP0, jP0 = Wp.value_and_jacobian(point[32:])
    qWX, jWX = W.value_and_jacobian(box[:32])
    qPX, jPX = Wp.value_and_jacobian(box[32:])

    f0 = [row_scales[i] * (qW0[i] - qP0[i]) for i in range(15)]
    stored_f0 = [rat(x) for x in data["equality_system"]["exact_center_residual"]]
    assert f0 == stored_f0, "literal switching map does not reproduce stored residual"

    J0, JX = [], []
    for i in range(15):
        row0, rowx = [], []
        for j, col in enumerate(pivots):
            if col < 32:
                deriv0, derivx, sign = jW0[i][col], jWX[i][col], 1
            else:
                deriv0, derivx, sign = jP0[i][col-32], jPX[i][col-32], -1
            row0.append(row_scales[i] * sign * scales[col] * deriv0)
            rowx.append(row_scales[i] * sign * scales[col] * derivx)
        J0.append(row0)
        JX.append(rowx)
    assert exact_equal_matrix(J0, data["equality_system"]["point_jacobian"])
    detJ = determinant(J0)
    assert detJ == rat(data["equality_system"]["point_jacobian_determinant"])
    Y = matrix_inverse(J0)
    # The stored preconditioner is used only as a post-derivation comparison.
    assert exact_equal_matrix(Y, data["krawczyk"]["preconditioner_exact_inverse_of_point_jacobian"])

    E = identity_minus(matmul(Y, JX))
    contraction = inf_norm_interval(E)
    correction = [y0[i] - z for i, z in enumerate(matvec(Y, f0))]
    delta = [I(-radius, radius) for _ in range(15)]
    edelta = matvec(E, delta)
    K = [I(correction[i] + edelta[i].lo, correction[i] + edelta[i].hi) for i in range(15)]
    normalized = max(max(abs(K[i].lo-y0[i]), abs(K[i].hi-y0[i])) / radius for i in range(15))
    strict = all(y0[i]-radius < K[i].lo <= K[i].hi < y0[i]+radius for i in range(15))
    assert strict and contraction < 1

    rank_results = {}
    for side, jac0, jacx in (("W", jW0, jWX), ("Wprime", jP0, jPX)):
        rec = data["rank_15_minors"][side]
        cols = rec["selected_columns"]
        A0 = [[jac0[i][j] for j in cols] for i in range(15)]
        AX = [[jacx[i][j] for j in cols] for i in range(15)]
        detA = determinant(A0)
        assert detA == rat(rec["point_determinant"])
        invA = matrix_inverse(A0)
        err = identity_minus(matmul(invA, AX))
        neumann = inf_norm_interval(err)
        assert neumann < 1
        rank_results[side] = {
            "determinant": exact_summary(detA),
            "neumann_bound": exact_summary(neumann),
            "rank_15_throughout_box": True,
        }

    physical = {
        "W": {k: exact_summary(v) for k, v in physical_bounds(box[:32]).items()},
        "Wprime": {k: exact_summary(v) for k, v in physical_bounds(box[32:]).items()},
    }
    assert all(v["sign"] > 0 for side in physical.values() for v in side.values())

    result = {
        "literal_map_matches_stored_center_residual": True,
        "literal_map_matches_stored_point_jacobian": True,
        "point_jacobian_determinant": exact_summary(detJ),
        "max_scaled_center_residual": decimal(max(abs(x) for x in f0)),
        "krawczyk_strict_inclusion": strict,
        "krawczyk_max_normalized_distance": exact_summary(normalized),
        "preconditioned_interval_jacobian_inf_norm": exact_summary(contraction),
        "uniqueness_scope": "unique zero in the 15-dimensional scaled pivot slice box only",
        "rank": rank_results,
        "physical_lower_bounds": physical,
        "method_boundary": (
            "Network polynomials and all intervals were freshly rebuilt from the literal DAGs. "
            "The supplied rational center, frozen coordinates, pivot scaling, box radius, and "
            "selected rank columns remain certificate inputs."
        ),
    }
    Path("krawczyk_literal_results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

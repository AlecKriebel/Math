#!/usr/bin/env python3
"""Exact polynomial-vector-field upper certificates for K2P descriptors.

For edge-sector parameters x_i and inheritance parameters l_j, use the ansatz

    V(x_i) = x_i A_i(l),
    V(l_j) = l_j(1-l_j) C_j(l_0,...,hat(l_j),...,l_{r-1}),

where A_i is multilinear in all inheritance variables and C_j is
multilinear in the other inheritance variables.  Expanding J_f V=0 gives an
integer linear system in the coefficients of A_i and C_j.  This module builds
that system exactly from a MapDescriptor's sparse integer pullbacks.

If A is the coefficient system and E is exact evaluation of the vector-field
ansatz at an interior rational point, then

    dim E(ker A) = rank([A; E]) - rank(A).

Thus d independent evaluated polynomial vector fields in ker J_f certify
generic rank(J_f) <= p-d.  No sampled Jacobian is used for the upper bound.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import gcd


def _lcm(a: int, b: int) -> int:
    return abs(a // gcd(a, b) * b) if a and b else 0


def ansatz_layout(desc):
    """Return coefficient labels in a deterministic order.

    Labels are (kind, parameter_index, lambda_mask).  Edge masks range over
    all r variables.  Lambda-j masks never contain bit j.
    """
    evars = 2 * desc.edge_class_count
    r = desc.retic_count
    labels = []
    for i in range(evars):
        for mask in range(1 << r):
            labels.append(("edge", i, mask))
    for j in range(r):
        for mask in range(1 << r):
            if not (mask >> j) & 1:
                labels.append(("lambda", j, mask))
    return tuple(labels)


def coefficient_system(desc, output_sparse_polynomials):
    """Build the exact integer coefficient matrix for J_f V=0.

    Rows are indexed by (output coordinate, exponent tuple).  Zero rows are
    discarded.  The returned row labels make the expansion independently
    auditable.
    """
    labels = ansatz_layout(desc)
    col = {lab: i for i, lab in enumerate(labels)}
    evars = 2 * desc.edge_class_count
    r = desc.retic_count
    p = evars + r
    constraints = defaultdict(lambda: defaultdict(int))

    for oi, poly in enumerate(output_sparse_polynomials(desc)):
        for exponent, coefficient in poly.items():
            exponent = tuple(exponent)
            # x_i d/dx_i preserves the monomial, then A_i adds a lambda mask.
            for i in range(evars):
                power = exponent[i]
                if not power:
                    continue
                for mask in range(1 << r):
                    out_exp = list(exponent)
                    for j in range(r):
                        if (mask >> j) & 1:
                            out_exp[evars + j] += 1
                    constraints[(oi, tuple(out_exp))][col[("edge", i, mask)]] += coefficient * power

            # d/dl_j followed by l_j(1-l_j) C_j.  Input pullbacks are
            # multilinear in each l_j, but this formula is valid for any
            # positive exponent as well.
            for j in range(r):
                pos = evars + j
                power = exponent[pos]
                if not power:
                    continue
                for mask in range(1 << r):
                    if (mask >> j) & 1:
                        continue
                    base = list(exponent)
                    for q in range(r):
                        if (mask >> q) & 1:
                            base[evars + q] += 1
                    # derivative lowers l_j, first factor l_j restores it
                    constraints[(oi, tuple(base))][col[("lambda", j, mask)]] += coefficient * power
                    # the -l_j^2 term raises it once relative to the input
                    raised = list(base)
                    raised[pos] += 1
                    constraints[(oi, tuple(raised))][col[("lambda", j, mask)]] -= coefficient * power

    rows = []
    row_labels = []
    for key in sorted(constraints):
        sparse = constraints[key]
        row = [sparse.get(i, 0) for i in range(len(labels))]
        if any(row):
            row_labels.append(key)
            rows.append(row)
    return tuple(labels), tuple(row_labels), rows


def evaluation_rows(desc, labels, edge_pairs, lambdas):
    """Integer row-scaled matrix evaluating ansatz fields at a rational point."""
    evars = 2 * desc.edge_class_count
    p = evars + desc.retic_count
    xs = tuple(z for pair in edge_pairs for z in pair)
    rows = []
    for parameter in range(p):
        vals = []
        for kind, index, mask in labels:
            value = Fraction(0)
            mon = Fraction(1)
            for j, lam in enumerate(lambdas):
                if (mask >> j) & 1:
                    mon *= lam
            if kind == "edge" and parameter == index:
                value = xs[index] * mon
            elif kind == "lambda" and parameter == evars + index:
                lam = lambdas[index]
                value = lam * (1 - lam) * mon
            vals.append(value)
        den = 1
        for value in vals:
            den = _lcm(den, value.denominator)
        rows.append([int(value * den) for value in vals])
    return rows


def exact_integer_rank(rows):
    """Rank over Q, using SymPy's exact domain-matrix implementation."""
    if not rows:
        return 0
    from sympy import ZZ
    from sympy.polys.matrices import DomainMatrix

    matrix = DomainMatrix.from_list(rows, ZZ)
    return int(matrix.rank())


def upper_certificate(desc, output_sparse_polynomials, default_exact_point):
    labels, row_labels, system = coefficient_system(desc, output_sparse_polynomials)
    edge_pairs, lambdas = default_exact_point(desc)
    evaluation = evaluation_rows(desc, labels, edge_pairs, lambdas)
    rank_system = exact_integer_rank(system)
    rank_stacked = exact_integer_rank(system + evaluation)
    independent_kernel_fields = rank_stacked - rank_system
    parameter_count = 2 * desc.edge_class_count + desc.retic_count
    return {
        "parameter_count": parameter_count,
        "unknown_coefficient_count": len(labels),
        "coefficient_equation_count": len(system),
        "coefficient_system_rank": rank_system,
        "stacked_system_rank": rank_stacked,
        "independent_kernel_fields": independent_kernel_fields,
        "certified_rank_upper": parameter_count - independent_kernel_fields,
        "row_labels": row_labels,
        "coefficient_labels": labels,
    }

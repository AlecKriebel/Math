#!/usr/bin/env python3
"""Deterministic exact searches for small extensions of the base gauge ansatz."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import gcd

from syzygy_upper import exact_integer_rank


def _lcm(a, b):
    return abs(a // gcd(a, b) * b) if a and b else 0


def cross_linear_layout(desc):
    """V(x_i)=sum_k x_k A_ik(lambda), with base lambda fields."""
    evars = 2 * desc.edge_class_count
    r = desc.retic_count
    labels = []
    for i in range(evars):
        for k in range(evars):
            for mask in range(1 << r):
                labels.append(("edge", i, k, mask))
    for j in range(r):
        for mask in range(1 << r):
            if not (mask >> j) & 1:
                labels.append(("lambda", j, -1, mask))
    return tuple(labels)


def cross_linear_system(desc, output_sparse_polynomials):
    labels = cross_linear_layout(desc)
    col = {lab: i for i, lab in enumerate(labels)}
    evars = 2 * desc.edge_class_count
    r = desc.retic_count
    constraints = defaultdict(lambda: defaultdict(int))
    for oi, poly in enumerate(output_sparse_polynomials(desc)):
        for exponent, coefficient in poly.items():
            exponent = tuple(exponent)
            for i in range(evars):
                power = exponent[i]
                if not power:
                    continue
                for k in range(evars):
                    for mask in range(1 << r):
                        out = list(exponent)
                        out[i] -= 1
                        out[k] += 1
                        for j in range(r):
                            if (mask >> j) & 1:
                                out[evars + j] += 1
                        constraints[(oi, tuple(out))][col[("edge", i, k, mask)]] += coefficient * power
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
                    constraints[(oi, tuple(base))][col[("lambda", j, -1, mask)]] += coefficient * power
                    raised = list(base)
                    raised[pos] += 1
                    constraints[(oi, tuple(raised))][col[("lambda", j, -1, mask)]] -= coefficient * power
    rows = []
    for key in sorted(constraints):
        sparse = constraints[key]
        row = [sparse.get(i, 0) for i in range(len(labels))]
        if any(row):
            rows.append(row)
    return labels, rows


def cross_linear_evaluation(desc, labels, edge_pairs, lambdas):
    evars = 2 * desc.edge_class_count
    xs = tuple(z for pair in edge_pairs for z in pair)
    rows = []
    for parameter in range(evars + desc.retic_count):
        vals = []
        for kind, component, factor, mask in labels:
            lm = Fraction(1)
            for j, lam in enumerate(lambdas):
                if (mask >> j) & 1:
                    lm *= lam
            value = Fraction(0)
            if kind == "edge" and component == parameter:
                value = xs[factor] * lm
            elif kind == "lambda" and evars + component == parameter:
                lam = lambdas[component]
                value = lam * (1 - lam) * lm
            vals.append(value)
        den = 1
        for value in vals:
            den = _lcm(den, value.denominator)
        rows.append([int(value * den) for value in vals])
    return rows


def cross_linear_upper(desc, output_sparse_polynomials, default_exact_point):
    labels, system = cross_linear_system(desc, output_sparse_polynomials)
    edge_pairs, lambdas = default_exact_point(desc)
    evaluation = cross_linear_evaluation(desc, labels, edge_pairs, lambdas)
    rs = exact_integer_rank(system)
    rt = exact_integer_rank(system + evaluation)
    fields = rt - rs
    p = 2 * desc.edge_class_count + desc.retic_count
    return {
        "unknowns": len(labels),
        "equations": len(system),
        "system_rank": rs,
        "stacked_rank": rt,
        "fields": fields,
        "upper": p - fields,
    }

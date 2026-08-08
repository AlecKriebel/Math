#!/usr/bin/env python3
"""Exact finite certificate for connected unweighted gadgets through order 6."""

from __future__ import annotations

import hashlib

import networkx as nx
import sympy as sp
from flint import fmpq

from scan_unweighted_gadgets import fixation_vector


Q = fmpq
R = Q(3, 2)


def sympy_q(value: fmpq) -> sp.Rational:
    return sp.Rational(str(value))


def separator_polynomial(graph: nx.Graph) -> tuple[sp.Poly, sp.Expr]:
    graph = nx.convert_node_labels_to_integers(graph, ordering="sorted")
    n = graph.number_of_nodes()
    degrees = [graph.degree(vertex) for vertex in range(n)]
    bd_plus = fixation_vector(graph, R, "Bd")
    bd_minus = fixation_vector(graph, 1 / R, "Bd")
    db_plus = fixation_vector(graph, R, "dB")
    db_minus = fixation_vector(graph, 1 / R, "dB")
    p = (R - 1) / R

    reciprocal_degrees = sum((Q(1, degree) for degree in degrees), Q(0))
    bd_reverse_sum = sum(bd_minus, Q(0))
    db_reverse_weighted = sum(
        (value / degree for value, degree in zip(db_minus, degrees)), Q(0)
    )
    slope_b = (R - 1) * reciprocal_degrees / bd_reverse_sum
    numerator_d = R * (R - 1) * n / db_reverse_weighted
    c_b = (sum(bd_plus, Q(0)) / n) / p
    c_d = (sum(db_plus, Q(0)) / n) / p

    a = sp.symbols("a", positive=True)
    A = sympy_q(slope_b)
    D = sympy_q(numerator_d)
    CB = sympy_q(c_b)
    CD = sympy_q(c_d)
    f_b = n * (CB * A * a / (1 + A * a) - 1)
    f_d = n * (CD * D / (a + D) - 1)
    separator = sp.factor(f_d + sp.Rational(1, 2) * f_b)
    numerator, denominator = sp.together(separator).as_numer_denom()
    assert sp.Poly(denominator, a).eval(sp.Rational(1)) > 0
    return sp.Poly(numerator, a), sp.factor(separator)


def main() -> None:
    graphs = [
        graph
        for graph in nx.graph_atlas_g()
        if 2 <= graph.number_of_nodes() <= 6 and nx.is_connected(graph)
    ]
    feasible: list[tuple[str, sp.Expr]] = []
    records: list[str] = []
    a = sp.symbols("a", positive=True)
    for graph in graphs:
        polynomial, separator = separator_polynomial(graph)
        coefficients = polynomial.all_coeffs()
        if polynomial.degree() < 2:
            coefficients = [sp.Rational(0)] * (3 - len(coefficients)) + coefficients
        leading, linear, constant = coefficients
        assert leading < 0
        assert constant <= 0
        discriminant = sp.discriminant(polynomial.as_expr(), a)
        can_be_positive = linear > 0 and discriminant > 0
        graph6 = nx.to_graph6_bytes(graph, header=False).decode().strip()
        records.append(
            f"{graph.number_of_nodes()}:{graph.number_of_edges()}:{graph6}:"
            f"{leading}:{linear}:{constant}:{discriminant}:"
            f"{int(bool(can_be_positive))}"
        )
        if can_be_positive:
            feasible.append((graph6, separator))

    assert len(graphs) == 142
    assert len(feasible) == 1
    assert feasible[0][0] == nx.to_graph6_bytes(nx.path_graph(2), header=False).decode().strip()
    k2_separator = sp.factor(feasible[0][1])
    expected = -3 * a * (4 * a - 1) / ((2 * a + 3) * (5 * a + 4))
    assert sp.simplify(k2_separator - expected) == 0

    digest = hashlib.sha256("\n".join(records).encode()).hexdigest()
    print(f"connected gadgets certified: {len(graphs)}")
    print(f"unique feasible graph6: {feasible[0][0]}")
    print(f"certificate digest: {digest}")
    print("PASS exact unweighted bounded-gadget certificate through order 6")


if __name__ == "__main__":
    main()

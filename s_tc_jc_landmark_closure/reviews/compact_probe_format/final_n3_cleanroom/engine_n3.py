#!/usr/bin/env python3
"""n=3 extensions to the committed clean-room graph/Fourier engine.

The base engine is the independently implemented n=4 engine from commit
35c0116d.  This module adds ordinary-triangle quotient transports and an
independent exact open-cube sign proof.  No module under ``primary`` is
imported.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import sys

import networkx as nx
import sympy as sp


HERE = Path(__file__).resolve().parent
N4 = HERE.parent / "final_n4_cleanroom"
sys.path.insert(0, str(N4))

from engine import (  # noqa: E402
    MixedEdge,
    MixedGraph,
    RootedGraph,
    canonical_representation,
    exact_poly_hash,
    incidence_graph,
    require,
    sd0,
    triangles,
)


def quotient_triangle(mixed: MixedGraph) -> MixedGraph:
    cycles = triangles(mixed)
    require(len(cycles) <= 1, "multiple_triangles_in_T_quotient",
            triangles=cycles)
    if not cycles:
        return mixed
    triangle = set(cycles[0])
    edges = tuple(sorted(
        MixedEdge.make(edge.u, edge.v)
        if edge.u in triangle and edge.v in triangle else edge
        for edge in mixed.edges
    ))
    return MixedGraph(mixed.labels, edges)


def all_vertex_isomorphisms(source: MixedGraph, target: MixedGraph, limit=2):
    def node_match(left, right):
        return (left.get("kind") == right.get("kind") and
                left.get("label") == right.get("label"))
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        incidence_graph(source), incidence_graph(target), node_match=node_match)
    answer = []
    for full in matcher.isomorphisms_iter():
        mapping = tuple(sorted((node[1], image[1])
                               for node, image in full.items()
                               if node[0] == "v"))
        if mapping not in answer:
            answer.append(mapping)
        if len(answer) >= limit:
            break
    return tuple(answer)


def derive_and_validate_transport(source: RootedGraph, target: RootedGraph,
                                  stored: dict):
    source_mixed = sd0(source); target_mixed = sd0(target)
    direct = all_vertex_isomorphisms(source_mixed, target_mixed)
    require(len(direct) <= 1, "nonrigid_direct_isomorphism", count=len(direct))
    independently_classified = (
        "labelled_isomorphism" if direct else "ordinary_T")
    require(stored["classification"] == independently_classified,
            "transport_classification",
            stored=stored["classification"],
            independent=independently_classified)

    source_q = quotient_triangle(source_mixed)
    target_q = quotient_triangle(target_mixed)
    quotient_maps = all_vertex_isomorphisms(source_q, target_q)
    require(len(quotient_maps) == 1, "T_quotient_not_uniquely_isomorphic",
            count=len(quotient_maps))
    mapping_rows = quotient_maps[0]; mapping = dict(mapping_rows)
    if independently_classified == "ordinary_T":
        require(len(triangles(source_mixed)) == 1 and
                len(triangles(target_mixed)) == 1,
                "T_without_two_triangles")

    canonicalization = stored["canonicalization"]
    source_canonical = tuple(tuple(x) for x in
                             canonicalization["source_raw_to_canonical"])
    target_canonical = tuple(tuple(x) for x in
                             canonicalization["target_raw_to_canonical"])
    require(canonical_representation(source_q, source_canonical) ==
            canonical_representation(target_q, target_canonical),
            "stored_quotient_canonicalization_not_common")
    target_inverse = {int(canonical): int(raw)
                      for raw, canonical in target_canonical}
    induced = tuple(sorted((int(raw), target_inverse[int(canonical)])
                           for raw, canonical in source_canonical))
    require(induced == mapping_rows,
            "quotient_canonicalization_transport_not_unique")

    body = stored["transport"]
    require(tuple(tuple(x) for x in body["vertex_transport"]) == mapping_rows,
            "vertex_transport")
    expected_ports = tuple(sorted(
        (label, target_q.label_map[mapping[vertex]])
        for vertex, label in source_q.labels))
    require(tuple(tuple(x) for x in body["port_transport"]) == expected_ports,
            "port_transport")
    require(all(left == right for left, right in expected_ports),
            "nonidentity_physical_port_transport")

    source_retics = source_mixed.reticulations()
    target_retics = target_mixed.reticulations()
    require(tuple(body["reticulation_vertices_source"]) == source_retics,
            "source_reticulation_list")
    require(tuple(body["reticulation_vertices_target"]) == target_retics,
            "target_reticulation_list")
    stable_retics = tuple(sorted((vertex, mapping[vertex])
                                 for vertex in source_retics
                                 if mapping[vertex] in target_retics))
    require(tuple(tuple(x) for x in
                  body["reticulation_transport_outside_redirected_triangle"]) ==
            stable_retics, "stable_reticulation_transport")

    target_edges = {edge: index for index, edge in enumerate(target_q.edges)}
    expected_permutation = []
    for index, edge in enumerate(source_q.edges):
        moved = MixedEdge.make(mapping[edge.u], mapping[edge.v],
                               (mapping[head] for head in edge.heads()))
        require(moved in target_edges, "transported_quotient_edge_missing")
        expected_permutation.append((index, target_edges[moved]))
    require(tuple(tuple(x) for x in body["t_quotient_edge_permutation"]) ==
            tuple(expected_permutation), "quotient_edge_permutation")
    require(stored["fourier_coordinate_transport"] ==
            "identity_on_fixed_port_labels", "fourier_coordinate_transport")
    return mapping_rows, independently_classified


def _poly_expr(poly):
    variables = len(poly[0][0]) if poly else 0
    symbols = sp.symbols(f"x0:{variables}")
    expression = sp.Integer(0)
    for exponent, coefficient in poly:
        term = sp.Integer(coefficient)
        for symbol, power in zip(symbols, exponent):
            term *= symbol ** int(power)
        expression += term
    return symbols, sp.expand(expression)


def _factor_poly_tuple(factor, symbols):
    terms = sp.Poly(factor, *symbols, domain=sp.QQ).terms()
    rows = []
    for exponent, coefficient in terms:
        require(coefficient.q == 1, "nonintegral_factor_coefficient",
                coefficient=str(coefficient))
        rows.append((tuple(int(x) for x in exponent), int(coefficient)))
    return tuple(sorted(rows))


def prove_strict_open_cube_sign(poly):
    """Factor exactly and prove the sign on the open unit cube.

    Every factor in the final n=3 strict family is independently required to
    be a nonzero univariate affine factor whose endpoint values have one weak
    sign and are not both zero.  Affinity then proves a strict sign throughout
    (0,1).  The exact factor product is also re-expanded and compared.
    """
    require(bool(poly), "zero_strict_polynomial")
    symbols, expression = _poly_expr(poly)
    coefficient, factors = sp.factor_list(expression, *symbols)
    require(sp.expand(coefficient * sp.prod(factor ** multiplicity
                                            for factor, multiplicity in factors)) ==
            expression, "factorization_recomposition")
    coefficient = sp.Rational(coefficient)
    require(coefficient != 0, "zero_factor_coefficient")
    sign = 1 if coefficient > 0 else -1
    factor_proofs = []
    for factor, multiplicity in factors:
        polynomial = sp.Poly(factor, *symbols, domain=sp.QQ)
        require(polynomial.total_degree() == 1, "nonaffine_sign_factor",
                factor=str(factor))
        used = tuple(index for index, symbol in enumerate(symbols)
                     if polynomial.degree(symbol) > 0)
        require(len(used) == 1, "multivariate_sign_factor",
                factor=str(factor), used=used)
        variable = symbols[used[0]]
        at_zero = sp.Rational(factor.subs(variable, 0))
        at_one = sp.Rational(factor.subs(variable, 1))
        if at_zero >= 0 and at_one >= 0 and (at_zero > 0 or at_one > 0):
            factor_sign = 1
        elif at_zero <= 0 and at_one <= 0 and (at_zero < 0 or at_one < 0):
            factor_sign = -1
        else:
            raise AssertionError({
                "category": "factor_not_sign_definite",
                "factor": str(factor), "at_zero": str(at_zero),
                "at_one": str(at_one),
            })
        if int(multiplicity) % 2:
            sign *= factor_sign
        factor_tuple = _factor_poly_tuple(factor, symbols)
        factor_proofs.append({
            "factor_exact_sha256": exact_poly_hash(factor_tuple),
            "multiplicity": int(multiplicity),
            "used_variable": used[0],
            "endpoint_values": [str(at_zero), str(at_one)],
            "strict_open_sign": factor_sign,
        })
    return {
        "method": "exact factorization plus affine endpoint sign",
        "coefficient": str(coefficient),
        "strict_open_sign": sign,
        "factors": factor_proofs,
        "polynomial_exact_sha256": exact_poly_hash(poly),
    }

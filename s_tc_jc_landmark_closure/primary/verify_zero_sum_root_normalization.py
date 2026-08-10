#!/usr/bin/env python3
"""Exact regression for the zero-sum split-complement quotient.

The hard-cover atlas compares standard semi-directed JC port tensors, not a
chosen rooted presentation.  Suppressing a root on an undirected edge replaces
its two physical multipliers by their product.  On a zero-sum Fourier
assignment the two descendant sides have equal XOR, so complementing every
split mask before zipping equal rows is the exact algebraic quotient.

This verifier uses two different admissible root placements of one labelled
quartet tree.  Their raw rooted descriptors differ, while their standard
mixed graphs and complement-normalized JC descriptors agree exactly.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from graph_model import RootedGraph, canonical_mixed, rooted_validation, sd0
from hard_cover_compiler import full_deck
from jc_tensor import canonicalize_rows, coordinate_polynomials, raw_descriptor


HERE = Path(__file__).resolve().parent


def stable_hash(payload) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def normalized_descriptor(graph: RootedGraph):
    retics, signatures = raw_descriptor(graph, ("L_0", "L_1", "L_2", "L_3"))
    rows = []
    for signature in signatures:
        rows.append(tuple(min(mask, 0b1111 ^ mask) for mask in signature))
    return canonicalize_rows(retics, rows)


def graph_payload(graph: RootedGraph):
    return {
        "root": graph.root,
        "labels": graph.labels,
        "arcs": graph.arcs,
    }


def polynomial_payload(polynomials):
    return tuple(
        tuple((tuple(exponent), coefficient) for exponent, coefficient in sorted(poly.items()))
        for poly in polynomials
    )


def main() -> None:
    # The common unrooted quartet has cherries 0,1 and 2,3.  The first root is
    # on its internal edge; the second is on the pendant edge incident to L_0.
    internal_root = RootedGraph(
        root=6,
        labels=((0, "L_0"), (1, "L_1"), (2, "L_2"), (3, "L_3")),
        arcs=((6, 4), (6, 5), (4, 0), (4, 1), (5, 2), (5, 3)),
    )
    pendant_root = RootedGraph(
        root=6,
        labels=((0, "L_0"), (1, "L_1"), (2, "L_2"), (3, "L_3")),
        arcs=((6, 0), (6, 4), (4, 1), (4, 5), (5, 2), (5, 3)),
    )

    for graph in (internal_root, pendant_root):
        valid, problems = rooted_validation(graph)
        if not valid or problems:
            raise AssertionError(("invalid fixture", problems))

    mixed_a = canonical_mixed(sd0(internal_root))[0]
    mixed_b = canonical_mixed(sd0(pendant_root))[0]
    if mixed_a != mixed_b:
        raise AssertionError("fixtures do not reduce to one mixed topology")

    raw_a = raw_descriptor(internal_root, ("L_0", "L_1", "L_2", "L_3"))
    raw_b = raw_descriptor(pendant_root, ("L_0", "L_1", "L_2", "L_3"))
    if raw_a == raw_b:
        raise AssertionError("regression fixture does not expose rooted masks")

    normalized_a = normalized_descriptor(internal_root)
    normalized_b = normalized_descriptor(pendant_root)
    if normalized_a != normalized_b:
        raise AssertionError("split-complement quotient depends on root")
    if full_deck(internal_root, 4) != (normalized_a,):
        raise AssertionError("hard-cover producer omits normalization")
    if full_deck(pendant_root, 4) != (normalized_b,):
        raise AssertionError("hard-cover producer omits normalization")
    if coordinate_polynomials(normalized_a) != coordinate_polynomials(normalized_b):
        raise AssertionError("normalized JC coordinate rings differ")

    graph_ids = tuple(stable_hash(graph_payload(graph)) for graph in (internal_root, pendant_root))
    if graph_ids[0] == graph_ids[1]:
        raise AssertionError("exact rooted graph provenance was collapsed")

    certificate = {
        "schema": "zero-sum-root-normalization-regression-v1",
        "status": "EXACTLY_VERIFIED",
        "rooted_graph_ids": graph_ids,
        "standard_mixed_code_sha256": hashlib.sha256(mixed_a.encode()).hexdigest(),
        "raw_descriptors_are_distinct": True,
        "normalized_descriptor_sha256": stable_hash(normalized_a),
        "coordinate_polynomials_sha256": stable_hash(
            polynomial_payload(coordinate_polynomials(normalized_a))
        ),
        "mathematical_identity": (
            "xor(A)=xor(A_complement) for zero-sum boundary assignments"
        ),
        "effective_root_edge_parameter": "x_root_left*x_root_right",
    }
    output = HERE / "certificates" / "zero_sum_root_normalization.json"
    output.write_text(json.dumps(certificate, sort_keys=True, indent=2) + "\n")
    print(json.dumps(certificate, sort_keys=True))


if __name__ == "__main__":
    main()

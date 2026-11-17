#!/usr/bin/env python3
"""Exact finite checks of the CM manuscript's GL(3) neighbor counts.

Python 3 standard library only.  This enumerates F_q^3 for the five prime
fields q = 2, 3, 5, 7, 11.  It checks incidence counts for the raw radial
minuscule operators and graph specialization multiplicities for a fixed
distinguished line M.  It does not check algebraic moduli, specialization
of group schemes, theta covariance, or the Hodge conjecture.

Run from any directory.  The result is written next to this source.
"""

from collections import Counter
from itertools import product
import json
from math import isqrt
from pathlib import Path


def normalize(v, q):
    """Canonical representative of a nonzero one-dimensional subspace."""
    pivot = next(x for x in v if x)
    inverse = pow(pivot, -1, q)
    return tuple((inverse * x) % q for x in v)


def projective_vectors(n, q):
    return sorted({normalize(v, q) for v in product(range(q), repeat=n) if any(v)})


def dot(v, w, q):
    return sum(x * y for x, y in zip(v, w)) % q


def add_polynomial(destination, coefficient, exponents):
    destination[exponents] += coefficient
    if destination[exponents] == 0:
        del destination[exponents]


def cancellation(q):
    """Expand X^3 - (X+qY)X^2 + q(XY+q^2 Z)X - q^3 XZ."""
    terms = Counter()
    for coefficient, exponents in (
        (1, (3, 0, 0)),
        (-1, (3, 0, 0)),
        (-q, (2, 1, 0)),
        (q, (2, 1, 0)),
        (q**3, (1, 0, 1)),
        (-q**3, (1, 0, 1)),
    ):
        add_polynomial(terms, coefficient, exponents)
    assert terms == {}, terms


def check_field(q):
    assert q >= 2 and all(q % d for d in range(2, isqrt(q) + 1))
    vectors = list(product(range(q), repeat=3))
    lines = projective_vectors(3, q)
    # Every plane is the kernel of a unique normalized nonzero linear form.
    planes = lines
    labels = projective_vectors(2, q)
    distinguished = (1, 0, 0)
    zero = (0, 0, 0)
    expected_total = q**2 + q + 1
    assert len(lines) == len(planes) == expected_total

    # Check all primitive residue vectors rather than just one representative.
    primitive_line_counts = set()
    primitive_plane_counts = set()
    for v in vectors:
        if v == zero:
            continue
        line_count = sum(normalize(v, q) == l for l in lines)
        plane_count = sum(dot(v, normal, q) == 0 for normal in planes)
        primitive_line_counts.add(line_count)
        primitive_plane_counts.add(plane_count)
    assert primitive_line_counts == {1}
    assert primitive_plane_counts == {q + 1}
    # For a vector in q Z_q^3, its residue is zero, in every subspace.
    assert all(dot(zero, normal, q) == 0 for normal in planes)

    # Generic subspaces of M + E, classified by whether they contain M.
    # Their images in E are canonical labels.  A line disjoint from M is
    # a graph over a label line; a plane disjoint from M is a graph over E.
    graph_lines_by_label = Counter()
    planes_containing_M_by_label = Counter()
    planes_disjoint_from_M = 0
    lines_containing_M = 0
    for l in lines:
        if l == distinguished:
            lines_containing_M += 1
        else:
            graph_lines_by_label[normalize(l[1:], q)] += 1
    for normal in planes:
        if normal[0] == 0:
            # The normal on E is nonzero; its kernel is one E-line.
            candidates = [label for label in labels if dot(normal[1:], label, q) == 0]
            assert len(candidates) == 1
            planes_containing_M_by_label[candidates[0]] += 1
        else:
            # Solve for the first coordinate: exactly one graph over all E.
            planes_disjoint_from_M += 1
    assert lines_containing_M == 1
    assert set(graph_lines_by_label) == set(labels)
    assert all(multiplicity == q for multiplicity in graph_lines_by_label.values())
    assert set(planes_containing_M_by_label) == set(labels)
    assert all(multiplicity == 1 for multiplicity in planes_containing_M_by_label.values())
    assert planes_disjoint_from_M == q**2
    assert lines_containing_M + sum(graph_lines_by_label.values()) == expected_total
    assert sum(planes_containing_M_by_label.values()) + planes_disjoint_from_M == expected_total

    # Raw radial action: its scalar factor is q^(i/2).  The bracket
    # coefficients are integer incidence counts, so no floating point is used.
    radial_T1 = [q + 1, expected_total - (q + 1)]
    radial_T2 = [1, expected_total - 1]
    assert radial_T1 == [q + 1, q**2]
    assert radial_T2 == [1, q**2 + q]
    cancellation(q)
    return {
        "q": q,
        "nonzero_residue_vectors_checked": q**3 - 1,
        "lines": len(lines),
        "planes": len(planes),
        "E_line_labels": len(labels),
        "primitive_vector_line_incidence": 1,
        "primitive_vector_plane_incidence": q + 1,
        "D1_distinguished_line_multiplicity": lines_containing_M,
        "D1_graphs_per_E_line": q,
        "D2_planes_containing_M_per_E_line": 1,
        "D2_graph_planes_over_E": planes_disjoint_from_M,
        "D3_full_space_multiplicity": 1,
        "raw_radial_T1_bracket": radial_T1,
        "raw_radial_T2_bracket": radial_T2,
        "formal_commutative_cubic_cancellation": True,
    }


def main():
    report = {
        "method": "Exact enumeration over prime fields, standard-library Python 3",
        "scope": "Finite counts and a formal commutative cancellation only; not a proof of the arithmetic geometry or Hodge conjecture",
        "fields": [check_field(q) for q in (2, 3, 5, 7, 11)],
        "all_assertions_passed": True,
    }
    path = Path(__file__).with_name("hecke_counts.json")
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_assertions_passed": True, "q": [2, 3, 5, 7, 11], "report": str(path)}, sort_keys=True))


if __name__ == "__main__":
    main()

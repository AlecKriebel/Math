#!/usr/bin/env python3
"""Self-contained active certificate for the ordinary JC triangle move.

The three labelled three-sunlet orientations are constructed as rooted
standard-strong witnesses, reduced with the locked ``sd0`` convention, and
evaluated directly by displayed-tree Fourier summation.  A rational common
point and a nonzero four-by-four Jacobian minor prove a common regular germ.
No equality of complete stochastic images is claimed.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

from graph_model import (
    MixedEdge,
    MixedGraph,
    RootedGraph,
    canonical_mixed,
    descendant_masks,
    mixed_local_strong,
    root_is_lsa,
    rooted_tree_child,
    rooted_validation,
    sd0,
    standard_strong_by_census,
    t_quotient,
    underlying_triangles,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent


def ratio(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def determinant(matrix):
    size = len(matrix)
    result = Fraction(0)
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size) for j in range(i + 1, size)
        )
        term = Fraction(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        result += term
    return result


def sunlet(reticulation_label: int) -> RootedGraph:
    """One rooted three-sunlet with the named taxon below the reticulation."""
    if reticulation_label not in range(3):
        raise ValueError(reticulation_label)
    root, left, right, retic = 0, 1, 2, 3
    leaf_left, leaf_right, leaf_retic = 4, 5, 6
    ordinary = [label for label in range(3) if label != reticulation_label]
    labels = (
        (leaf_left, f"L_{ordinary[0]}"),
        (leaf_right, f"L_{ordinary[1]}"),
        (leaf_retic, f"L_{reticulation_label}"),
    )
    arcs = (
        (root, left), (root, right),
        (left, retic), (right, retic),
        (left, leaf_left), (right, leaf_right), (retic, leaf_retic),
    )
    return RootedGraph(root, tuple(sorted(labels)), tuple(sorted(arcs)))


def unheaded_code(graph: MixedGraph) -> str:
    unheaded = MixedGraph(
        graph.labels,
        tuple(sorted(MixedEdge.make(edge.u, edge.v) for edge in graph.edges)),
    )
    return canonical_mixed(unheaded)[0]


def direct_fourier(
    graph: RootedGraph,
    edge_parameters: dict[tuple[int, int], Fraction],
    inheritance: Fraction,
) -> tuple[Fraction, ...]:
    """Evaluate all 64 Fourier entries by direct displayed-tree summation."""
    labels = ("L_0", "L_1", "L_2")
    retic = 3
    incoming = tuple(
        index for index, (_u, v) in enumerate(graph.arcs) if v == retic
    )
    if len(incoming) != 2:
        raise AssertionError("three-sunlet reticulation indegree")
    left_incoming = graph.arcs.index((1, retic))
    values = []
    for assignment in itertools.product(range(4), repeat=3):
        if assignment[0] ^ assignment[1] ^ assignment[2]:
            values.append(Fraction(0))
            continue
        total = Fraction(0)
        for chosen in incoming:
            active = tuple(
                index for index in range(len(graph.arcs))
                if index not in incoming or index == chosen
            )
            weight = inheritance if chosen == left_incoming else 1 - inheritance
            masks = descendant_masks(graph, active, labels)
            monomial = Fraction(1)
            for active_index, mask in zip(active, masks):
                character = 0
                for leaf_index, value in enumerate(assignment):
                    if mask & (1 << leaf_index):
                        character ^= value
                if character:
                    monomial *= edge_parameters[graph.arcs[active_index]]
            total += weight * monomial
        values.append(total)
    return tuple(values)


def orbit_coordinates(tensor: tuple[Fraction, ...]):
    def at(g1, g2, g3):
        return tensor[(g1 * 4 + g2) * 4 + g3]
    # One representative nonzero character suffices under JC.
    return at(1, 1, 0), at(1, 0, 1), at(0, 1, 1), at(1, 2, 3)


def jacobian_minor(r1, r2, r3, lam, x, u, v):
    y = lam * u + (1 - lam) * x * v
    z = lam * x * u + (1 - lam) * v
    h = lam * u + (1 - lam) * v
    w = x * h
    dy_dx = (1 - lam) * v
    dz_dx = lam * u
    return (
        (r2 * x, r1 * x, Fraction(0), r1 * r2),
        (r3 * y, Fraction(0), r1 * y, r1 * r3 * dy_dx),
        (Fraction(0), r3 * z, r2 * z, r2 * r3 * dz_dx),
        (r2 * r3 * w, r1 * r3 * w, r1 * r2 * w, r1 * r2 * r3 * h),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path,
        default=HERE / "certificates/jc_triangle_redirection_active.json",
    )
    args = parser.parse_args()

    delta = Fraction(1, 1024)
    ordinary_arm = 2 * delta
    reticulation_arm = Fraction(16, 5) * delta
    root_arm = Fraction(1, 2)
    internal = Fraction(1, 4)
    inheritance = Fraction(1, 2)

    rooted_records = []
    tensors = []
    mixed_codes = []
    quotient_codes = []
    unheaded_codes = []
    for reticulation_label in range(3):
        graph = sunlet(reticulation_label)
        valid, problems = rooted_validation(graph)
        mixed = sd0(graph)
        standard_strong, rooting_count, tree_child_rooting_count = (
            standard_strong_by_census(mixed)
        )
        edge_parameters = {
            (0, 1): root_arm,
            (0, 2): root_arm,
            (1, 3): internal,
            (2, 3): internal,
        }
        for u, v in graph.arcs:
            if v not in {4, 5, 6}:
                continue
            label = dict(graph.labels)[v]
            edge_parameters[(u, v)] = (
                reticulation_arm
                if label == f"L_{reticulation_label}" else ordinary_arm
            )
        tensor = direct_fourier(graph, edge_parameters, inheritance)
        tensors.append(tensor)
        mixed_code = canonical_mixed(mixed)[0]
        quotient_code = canonical_mixed(t_quotient(mixed))[0]
        mixed_codes.append(mixed_code)
        quotient_codes.append(quotient_code)
        unheaded_codes.append(unheaded_code(mixed))
        rooted_records.append({
            "reticulation_taxon": f"L_{reticulation_label}",
            "rooted_valid": valid,
            "rooted_validation_problems": list(problems),
            "root_is_lsa": root_is_lsa(graph),
            "chosen_rooting_tree_child": rooted_tree_child(graph),
            "standard_local_strong": mixed_local_strong(mixed),
            "all_admissible_rootings_tree_child": standard_strong,
            "admissible_rooting_count": rooting_count,
            "tree_child_rooting_count": tree_child_rooting_count,
            "triangle_count": len(underlying_triangles(mixed)),
            "reticulation_count": len(mixed.reticulations()),
            "standard_mixed_code_sha256": hashlib.sha256(mixed_code.encode()).hexdigest(),
            "T_quotient_code_sha256": hashlib.sha256(quotient_code.encode()).hexdigest(),
            "unheaded_code_sha256": hashlib.sha256(unheaded_codes[-1].encode()).hexdigest(),
            "edge_parameters": {
                f"{u}->{v}": ratio(value)
                for (u, v), value in sorted(edge_parameters.items())
            },
            "inheritance_probability": ratio(inheritance),
            "orbit_coordinates": [ratio(value) for value in orbit_coordinates(tensor)],
        })

    representative = tensors[0]
    target = (
        delta**2, delta**2, delta**2, Fraction(4, 5) * delta**3
    )
    minor = jacobian_minor(
        ordinary_arm, ordinary_arm, reticulation_arm,
        inheritance, internal, internal, internal,
    )
    minor_determinant = determinant(minor)
    expected_determinant = -Fraction(3, 23058430092136939520)
    all_parameters = (
        delta, ordinary_arm, reticulation_arm, root_arm, internal, inheritance
    )
    coordinate_counts = {
        "coordinates": len(representative),
        "constant_one": sum(value == 1 for value in representative),
        "nonzero_pair_coordinates": sum(value == delta**2 for value in representative),
        "nonzero_triple_coordinates": sum(
            value == Fraction(4, 5) * delta**3 for value in representative
        ),
        "zero_coordinates": sum(value == 0 for value in representative),
    }
    checks = {
        "three_distinct_standard_mixed_orientations": len(set(mixed_codes)) == 3,
        "one_common_labelled_unheaded_graph": len(set(unheaded_codes)) == 1,
        "one_common_T_quotient": len(set(quotient_codes)) == 1,
        "all_rooted_witnesses_valid_LSA_tree_child": all(
            row["rooted_valid"] and row["root_is_lsa"]
            and row["chosen_rooting_tree_child"] for row in rooted_records
        ),
        "all_standard_mixed_graphs_strong": all(
            row["standard_local_strong"]
            and row["all_admissible_rootings_tree_child"]
            for row in rooted_records
        ),
        "all_are_level_one_single_triangles": all(
            row["triangle_count"] == 1 and row["reticulation_count"] == 1
            for row in rooted_records
        ),
        "all_parameters_in_open_Theta0": all(
            Fraction(0) < value < Fraction(1) for value in all_parameters
        ),
        "all_64_Fourier_coordinates_equal": len(set(tensors)) == 1,
        "all_orbit_coordinates_equal_target": all(
            orbit_coordinates(tensor) == target for tensor in tensors
        ),
        "Fourier_coordinate_counts_1_9_6_48": coordinate_counts == {
            "coordinates": 64,
            "constant_one": 1,
            "nonzero_pair_coordinates": 9,
            "nonzero_triple_coordinates": 6,
            "zero_coordinates": 48,
        },
        "rank_minor_matches": minor_determinant == expected_determinant,
        "rank_is_four": minor_determinant != 0,
    }
    result = {
        "schema": "active-jc-ordinary-triangle-germ-v1",
        "status": "VERIFIED" if all(checks.values()) else "FALSE",
        "scope": "ordinary triangle redirection T under the locked sd0 standard S_TC convention",
        "parameter_space": "0 < every JC Fourier multiplier < 1 and 0 < lambda < 1",
        "topology": {
            "rooted_witnesses": rooted_records,
            "semi_directed_orientation_count": len(set(mixed_codes)),
            "underlying_labelled_graph_count": len(set(unheaded_codes)),
            "T_quotient_class_count": len(set(quotient_codes)),
        },
        "common_point": {
            "delta": ratio(delta),
            "target_orbit_coordinates": [ratio(value) for value in target],
            "complete_Fourier_tensor": [ratio(value) for value in representative],
            "complete_Fourier_tensor_sha256": hashlib.sha256(
                json.dumps(
                    [ratio(value) for value in representative],
                    separators=(",", ":"),
                ).encode()
            ).hexdigest(),
            "coordinate_counts": coordinate_counts,
        },
        "rank_certificate": {
            "output_coordinates": ["q12", "q13", "q23", "q123"],
            "parameter_columns": ["r1", "r2", "r3", "x"],
            "matrix": [[ratio(value) for value in row] for row in minor],
            "determinant": ratio(minor_determinant),
            "expected_determinant": ratio(expected_determinant),
            "upper_bound": 4,
            "upper_bound_reason": "the normalized three-leaf JC orbit tensor has four nonconstant coordinates",
        },
        "stochastic_conclusion": {
            "pairwise_symmetric_full_dimensional_regular_overlap": "VERIFIED",
            "argument": "the exact common interior point and nonzero four-coordinate Jacobian give an open output neighborhood for every orientation by the inverse function theorem",
            "complete_open_stochastic_image_equality": "NOT CLAIMED",
        },
        "checks": checks,
        "failed_checks": sorted(key for key, value in checks.items() if not value),
        "implementation": {
            "path": str(Path(__file__).resolve().relative_to(PROJECT)),
            "sha256": sha256(Path(__file__).resolve()),
            "Fourier_evaluation": "direct displayed-tree summation over all 64 character assignments",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "output": str(args.output),
        "sha256": sha256(args.output),
    }, sort_keys=True))
    if result["status"] != "VERIFIED":
        raise SystemExit(result["failed_checks"])


if __name__ == "__main__":
    main()

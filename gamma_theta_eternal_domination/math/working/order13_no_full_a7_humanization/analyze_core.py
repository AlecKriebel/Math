#!/usr/bin/env python3
"""Classify clauses retained by a DRAT-extracted core.

The structured formula is deliberately simple enough that its clause blocks
can be reconstructed from the production generator's documented loop order.
This script checks that census, maps every original clause to a semantic
category, and reports how much of each category occurs in ``core.cnf``.
"""

from __future__ import annotations

import argparse
from collections import Counter
import itertools
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "order13_no_full_a7_structured"


def read_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = -1
    clauses: list[tuple[int, ...]] = []
    with path.open(encoding="ascii") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p "):
                _, kind, variables_text, clauses_text = line.split()
                if kind != "cnf":
                    raise ValueError(f"unexpected DIMACS kind {kind}")
                variables = int(variables_text)
                expected = int(clauses_text)
                continue
            literals = tuple(map(int, line.split()))
            if not literals or literals[-1] != 0:
                raise ValueError(f"malformed clause line: {line}")
            clauses.append(literals[:-1])
    if variables < 0:
        raise ValueError("missing DIMACS header")
    if len(clauses) != expected:
        raise ValueError(f"header says {expected} clauses, read {len(clauses)}")
    return variables, clauses


def semantic_labels() -> list[str]:
    labels: list[str] = []

    labels.extend(["alpha_no_H_K4"] * 715)

    # For each of 78 unordered pairs: one common-neighbor choice followed by
    # two witness implications for each of the eleven possible witnesses.
    for _ in range(78):
        labels.append("gamma_pair_common_neighbor_choice")
        for _ in range(11):
            labels.append("gamma_witness_first_H_edge")
            labels.append("gamma_witness_second_H_edge")

    labels.extend(["family_state_dominates_G"] * 2860)
    labels.append("family_nonempty")

    # For each of 286 triples and ten attacks: two implications per candidate
    # guard, then the clause requiring at least one reply.
    for _ in range(286 * 10):
        for _ in range(3):
            labels.append("closure_move_uses_G_edge")
            labels.append("closure_successor_in_family")
        labels.append("closure_reply_exists")

    labels.extend(["anchor_triangle_H_edges"] * 3)
    labels.append("anchor_state_in_family")
    labels.extend(["theta_no_anchored_3_coloring"] * (3**10))
    labels.extend(["anchor_no_full_response"] * 10)
    # Type omitting anchor 0: port 3, mate 4.
    labels.extend(
        [
            "port_signature_required_H_edge",
            "port_signature_G_edge_implied_by_positive_list",
            "port_signature_G_edge_implied_by_positive_list",
            "mate_signature_required_H_edge",
            "mate_signature_required_G_edge",
            "mate_signature_required_G_edge",
            "port_negative_list_membership",
            "port_positive_list_membership",
            "port_positive_list_membership",
            "representative_H_mate_edges",
        ]
    )
    # Type omitting anchor 2: port 5, mate 6.
    labels.extend(
        [
            "port_signature_G_edge_implied_by_positive_list",
            "port_signature_G_edge_implied_by_positive_list",
            "port_signature_required_H_edge",
            "mate_signature_required_G_edge",
            "mate_signature_required_G_edge",
            "mate_signature_required_H_edge",
            "port_positive_list_membership",
            "port_positive_list_membership",
            "port_negative_list_membership",
            "representative_H_mate_edges",
        ]
    )
    labels.extend(["residual_signature_sorting"] * 140)
    labels.append("fourth_residual_nonzero_signature")
    return labels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, default=HERE / "core.cnf")
    args = parser.parse_args()
    variables, original = read_cnf(SOURCE / "instance-proof.cnf")
    core_variables, core = read_cnf(args.core)
    if variables != core_variables:
        raise AssertionError((variables, core_variables))
    labels = semantic_labels()
    if len(labels) != len(original):
        raise AssertionError((len(labels), len(original)))
    canonical_original = [frozenset(clause) for clause in original]
    if len(set(canonical_original)) != len(original):
        raise AssertionError("formula unexpectedly has duplicate clauses")

    label_by_clause = dict(zip(canonical_original, labels, strict=True))
    index_by_clause = {
        clause: index for index, clause in enumerate(canonical_original)
    }
    missing = [
        clause for clause in core if frozenset(clause) not in label_by_clause
    ]
    if missing:
        raise AssertionError(f"{len(missing)} core clauses absent from source")

    total = Counter(labels)
    retained = Counter(label_by_clause[frozenset(clause)] for clause in core)
    print(f"variables={variables}")
    print(f"source_clauses={len(original)} core_clauses={len(core)}")
    print()
    print(f"{'category':42s} {'core':>8s} {'total':>8s} {'percent':>9s}")
    for category in total:
        kept = retained[category]
        count = total[category]
        print(f"{category:42s} {kept:8d} {count:8d} {100*kept/count:8.2f}%")

    print()
    print("retained structural clauses")
    triples = tuple(itertools.combinations(range(13), 3))
    family_start = 78 + 78 * 11 + 1
    family_by_variable = {
        family_start + index: triple for index, triple in enumerate(triples)
    }
    structural = {
        "anchor_no_full_response",
        "port_signature_required_H_edge",
        "port_signature_G_edge_implied_by_positive_list",
        "mate_signature_required_H_edge",
        "mate_signature_required_G_edge",
        "port_positive_list_membership",
        "port_negative_list_membership",
        "representative_H_mate_edges",
        "fourth_residual_nonzero_signature",
    }
    for clause in core:
        canonical = frozenset(clause)
        category = label_by_clause[canonical]
        if category not in structural:
            continue
        decoded = [
            (
                ("+" if literal > 0 else "-")
                + (
                    f"f{family_by_variable[abs(literal)]}"
                    if abs(literal) in family_by_variable
                    else f"v{abs(literal)}"
                )
            )
            for literal in clause
        ]
        print(f"{category:42s} {' '.join(decoded)}")

    theta_start = labels.index("theta_no_anchored_3_coloring")
    theta_patterns: Counter[tuple[int, int, int, int]] = Counter()
    theta_vertex_colors = {
        vertex: Counter() for vertex in range(3, 13)
    }
    retained_theta = [
        frozenset(clause)
        for clause in core
        if label_by_clause[frozenset(clause)]
        == "theta_no_anchored_3_coloring"
    ]
    for clause in retained_theta:
        offset = index_by_clause[clause] - theta_start
        digits = [0] * 10
        for position in range(9, -1, -1):
            digits[position] = offset % 3
            offset //= 3
        if offset:
            raise AssertionError("bad base-three theta offset")
        for vertex, color in zip(range(3, 13), digits, strict=True):
            theta_vertex_colors[vertex][color] += 1
        theta_patterns[(digits[0], digits[1], digits[2], digits[3])] += 1

    print()
    print("retained theta-color clauses by orientations (c3,c4,c5,c6)")
    for pattern, count in sorted(theta_patterns.items()):
        print(f"{pattern}: {count}")
    print()
    print("retained theta-color marginal counts")
    for vertex, counts in theta_vertex_colors.items():
        print(
            f"vertex {vertex}: "
            + " ".join(f"color{color}={counts[color]}" for color in range(3))
        )

    core_set = frozenset(frozenset(clause) for clause in core)
    pairs = tuple(itertools.combinations(range(13), 2))
    gamma_start = 715
    gamma_pairs = []
    for pair_index, pair in enumerate(pairs):
        choice = canonical_original[gamma_start + 23 * pair_index]
        if choice in core_set:
            gamma_pairs.append(pair)
    print()
    print("common-H-neighbor pair-choice clauses")
    print(f"retained ({len(gamma_pairs)}): {gamma_pairs}")
    print(
        f"omitted ({len(pairs) - len(gamma_pairs)}): "
        f"{[pair for pair in pairs if pair not in gamma_pairs]}"
    )

    closure_start = 715 + 1794 + 2860 + 1
    attacks_by_state: Counter[tuple[int, int, int]] = Counter()
    attacks_by_target: Counter[int] = Counter()
    attacks_by_anchor_intersection: Counter[int] = Counter()
    retained_obligations: list[tuple[tuple[int, int, int], int]] = []
    for state_index, state in enumerate(triples):
        attacks = tuple(vertex for vertex in range(13) if vertex not in state)
        for attack_index, attack in enumerate(attacks):
            obligation_index = state_index * 10 + attack_index
            reply_clause_index = closure_start + 7 * obligation_index + 6
            if canonical_original[reply_clause_index] not in core_set:
                continue
            retained_obligations.append((state, attack))
            attacks_by_state[state] += 1
            attacks_by_target[attack] += 1
            attacks_by_anchor_intersection[len(set(state) & {0, 1, 2})] += 1
    print()
    print("retained closure-reply obligations")
    print(
        f"states with at least one={len(attacks_by_state)} of {len(triples)}; "
        f"obligations={len(retained_obligations)} of {len(triples) * 10}"
    )
    state_histogram = Counter(attacks_by_state.values())
    print(
        "obligations per retained state: "
        + ", ".join(
            f"{count}:{states}" for count, states in sorted(state_histogram.items())
        )
    )
    print(
        "by |state intersect S|: "
        + ", ".join(
            f"{size}:{attacks_by_anchor_intersection[size]}"
            for size in range(4)
        )
    )
    print(
        "by attacked vertex: "
        + ", ".join(
            f"{vertex}:{attacks_by_target[vertex]}" for vertex in range(13)
        )
    )


if __name__ == "__main__":
    main()

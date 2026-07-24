#!/usr/bin/env python3
"""Independently rank fixed core pairs occurring in a drat-trim input core.

The script does not import the Ramsey CNF generator.  It reconstructs every
source clause directly from the pinned graph, the metadata free-edge order,
and all 5-subsets.  The clauses retained by drat-trim are then matched as an
ordered subsequence of the original DIMACS input, which recovers the exact
5-subset associated with each retained input-clause occurrence.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


SCRIPT_ID = "ramsey55_drat_core_fixed_pair_rank_v1"
REPORTED_TOP = (
    ((0, 32), 104),
    ((18, 33), 102),
    ((18, 20), 101),
    ((24, 26), 101),
    ((1, 10), 100),
    ((9, 29), 96),
    ((27, 29), 94),
    ((6, 15), 94),
    ((1, 12), 94),
    ((2, 25), 93),
)


@dataclass(frozen=True)
class SourceClause:
    literals: tuple[int, ...]
    vertices: tuple[int, ...]
    family: str


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def first_graph6(path: Path) -> str:
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            if line.startswith(">>graph6<<"):
                line = line[len(">>graph6<<") :]
            return line
    raise ValueError("graph file has no data line")


def decode_short_graph6(line: str) -> list[int]:
    if not line:
        raise ValueError("empty graph6")
    order = ord(line[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("only short graph6 is supported")
    adjacency = [0] * order
    bit_index = 0
    for right in range(1, order):
        for left in range(right):
            payload_index = 1 + bit_index // 6
            if payload_index >= len(line):
                raise ValueError("truncated graph6")
            value = ord(line[payload_index]) - 63
            if not 0 <= value < 64:
                raise ValueError("invalid graph6 payload")
            if (value >> (5 - bit_index % 6)) & 1:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            bit_index += 1
    return adjacency


def read_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variable_count: int | None = None
    declared_count: int | None = None
    clauses: list[tuple[int, ...]] = []
    pending: list[int] = []
    for line_number, raw in enumerate(
        path.read_text(encoding="ascii").splitlines(), 1
    ):
        fields = raw.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "p":
            if (
                variable_count is not None
                or len(fields) != 4
                or fields[1] != "cnf"
            ):
                raise ValueError(f"invalid DIMACS header at line {line_number}")
            variable_count = int(fields[2])
            declared_count = int(fields[3])
            continue
        if variable_count is None:
            raise ValueError("clause precedes DIMACS header")
        for field in fields:
            literal = int(field)
            if literal:
                if not 1 <= abs(literal) <= variable_count:
                    raise ValueError("literal outside DIMACS variable range")
                pending.append(literal)
            else:
                clauses.append(tuple(pending))
                pending = []
    if (
        variable_count is None
        or declared_count is None
        or pending
        or len(clauses) != declared_count
    ):
        raise ValueError("malformed or incomplete DIMACS")
    return variable_count, clauses


def reconstruct_source_clauses(
    adjacency: Sequence[int],
    free_edges: Sequence[tuple[int, int]],
    forbidden_size: int,
) -> list[SourceClause]:
    variable_by_pair = {
        pair: variable for variable, pair in enumerate(free_edges, 1)
    }
    negative: list[SourceClause] = []
    positive: list[SourceClause] = []
    for vertices in itertools.combinations(range(len(adjacency)), forbidden_size):
        variables: list[int] = []
        fixed_values: list[bool] = []
        for left, right in itertools.combinations(vertices, 2):
            variable = variable_by_pair.get((left, right))
            if variable is None:
                fixed_values.append(bool((adjacency[left] >> right) & 1))
            else:
                variables.append(variable)
        if all(fixed_values):
            negative.append(
                SourceClause(
                    tuple(-variable for variable in variables),
                    vertices,
                    "clique_prevention",
                )
            )
        if not any(fixed_values):
            positive.append(
                SourceClause(
                    tuple(variables),
                    vertices,
                    "independent_prevention",
                )
            )
    return negative + positive


def clause_key(clause: Sequence[int]) -> tuple[int, ...]:
    return tuple(sorted(clause))


def earliest_subsequence_positions(
    source: Sequence[SourceClause], retained: Sequence[tuple[int, ...]]
) -> list[int]:
    positions: list[int] = []
    cursor = 0
    for retained_clause in retained:
        key = clause_key(retained_clause)
        while cursor < len(source) and clause_key(source[cursor].literals) != key:
            cursor += 1
        if cursor == len(source):
            raise ValueError("core clauses are not an ordered source subsequence")
        positions.append(cursor)
        cursor += 1
    return positions


def latest_subsequence_positions(
    source: Sequence[SourceClause], retained: Sequence[tuple[int, ...]]
) -> list[int]:
    positions = [0] * len(retained)
    cursor = len(source) - 1
    for retained_index in range(len(retained) - 1, -1, -1):
        key = clause_key(retained[retained_index])
        while cursor >= 0 and clause_key(source[cursor].literals) != key:
            cursor -= 1
        if cursor < 0:
            raise ValueError(
                "core clauses are not a reverse ordered source subsequence"
            )
        positions[retained_index] = cursor
        cursor -= 1
    return positions


def pair_record(pair: tuple[int, int], score: int, rank: int) -> dict[str, object]:
    return {"pair": list(pair), "score": score, "rank": rank}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--core-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    graph6 = first_graph6(args.graph)
    if metadata["base_graph6"] != graph6:
        raise SystemExit("metadata base_graph6 does not match the graph input")
    adjacency = decode_short_graph6(graph6)
    if len(adjacency) != 43:
        raise SystemExit("this audit requires the 43-vertex incident-six formula")
    free_edges = tuple(tuple(pair) for pair in metadata["free_edges"])
    incident_vertices = tuple(metadata["incident_free_vertices"])
    incident_set = set(incident_vertices)
    expected_free = tuple(
        pair
        for pair in itertools.combinations(range(43), 2)
        if pair[0] in incident_set or pair[1] in incident_set
    )
    if free_edges != expected_free or len(free_edges) != 237:
        raise SystemExit("metadata does not encode the exact incident-six boundary")
    if tuple(sorted(incident_vertices)) != (3, 4, 7, 38, 41, 42):
        raise SystemExit("unexpected incident vertex set")

    variables, input_clauses = read_dimacs(args.cnf)
    if variables != len(free_edges):
        raise SystemExit("CNF variable count disagrees with metadata")
    source = reconstruct_source_clauses(
        adjacency, free_edges, metadata["forbidden_size"]
    )
    source_literals = [entry.literals for entry in source]
    if source_literals != input_clauses:
        raise SystemExit("direct 5-subset reconstruction disagrees with input CNF")

    core_variables, core_clauses = read_dimacs(args.core_cnf)
    if core_variables != variables:
        raise SystemExit("core variable count disagrees with source CNF")
    earliest = earliest_subsequence_positions(source, core_clauses)
    latest = latest_subsequence_positions(source, core_clauses)
    ambiguous_indices = [
        index for index, (left, right) in enumerate(zip(earliest, latest, strict=True))
        if left != right
    ]
    if ambiguous_indices:
        raise SystemExit(
            "ordered core-to-input mapping is not unique: "
            f"{len(ambiguous_indices)} ambiguous retained clauses"
        )

    fixed_vertices = tuple(
        vertex for vertex in range(43) if vertex not in incident_set
    )
    fixed_set = set(fixed_vertices)
    scores: Counter[tuple[int, int]] = Counter()
    family_counts: Counter[str] = Counter()
    scored_pair_occurrences = 0
    for source_index in earliest:
        entry = source[source_index]
        family_counts[entry.family] += 1
        subset_fixed = tuple(
            vertex for vertex in entry.vertices if vertex in fixed_set
        )
        for pair in itertools.combinations(subset_fixed, 2):
            scores[pair] += 1
            scored_pair_occurrences += 1

    # Counter.most_common preserves first-scored order for equal counts.  This
    # is the ranking convention used by the reported list.  A canonical
    # lexicographic tie-break is also emitted for consumers that require one.
    occurrence_ranking = scores.most_common()
    canonical_ranking = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    occurrence_rank_by_pair = {
        pair: rank for rank, (pair, _) in enumerate(occurrence_ranking, 1)
    }
    reported_comparison = []
    for pair, reported_score in REPORTED_TOP:
        actual_score = scores[pair]
        reported_comparison.append(
            {
                "pair": list(pair),
                "reported_score": reported_score,
                "actual_score": actual_score,
                "score_match": actual_score == reported_score,
                "occurrence_order_rank": occurrence_rank_by_pair[pair],
            }
        )
    computed_top = tuple(occurrence_ranking[: len(REPORTED_TOP)])
    scores_match = all(
        scores[pair] == expected for pair, expected in REPORTED_TOP
    )
    ordered_list_match = computed_top == REPORTED_TOP

    result = {
        "script": SCRIPT_ID,
        "status": (
            "CONFIRMED"
            if scores_match and ordered_list_match
            else "PARTIAL_CONFIRMATION"
            if scores_match
            else "REFUTED"
        ),
        "method": {
            "source_formula_reconstruction": (
                "direct lexicographic enumeration of all 5-subsets; "
                "clique-prevention family followed by independent-prevention family"
            ),
            "core_mapping": (
                "unique ordered subsequence match after sorting literals within clauses"
            ),
            "score": (
                "one occurrence for every fixed-core pair contained in the exact "
                "5-subset of each retained input clause"
            ),
            "tie_order": "first scored occurrence via Counter.most_common",
        },
        "inputs": {
            "graph": str(args.graph),
            "graph_sha256": sha256(args.graph),
            "metadata": str(args.metadata),
            "metadata_sha256": sha256(args.metadata),
            "cnf": str(args.cnf),
            "cnf_sha256": sha256(args.cnf),
            "core_cnf": str(args.core_cnf),
            "core_cnf_sha256": sha256(args.core_cnf),
            "script_sha256": sha256(Path(__file__)),
        },
        "formula": {
            "variable_count": variables,
            "input_clause_count": len(input_clauses),
            "direct_reconstruction_exact_order_match": True,
            "core_clause_count": len(core_clauses),
            "mapped_core_clause_count": len(earliest),
            "mapping_strictly_increasing": all(
                left < right for left, right in itertools.pairwise(earliest)
            ),
            "unique_ordered_mapping": not ambiguous_indices,
            "ambiguous_mapping_count": len(ambiguous_indices),
            "first_source_clause_index_one_based": earliest[0] + 1,
            "last_source_clause_index_one_based": earliest[-1] + 1,
            "retained_family_counts": dict(sorted(family_counts.items())),
        },
        "fixed_core": {
            "vertices": list(fixed_vertices),
            "vertex_count": len(fixed_vertices),
            "possible_pair_count": len(fixed_vertices)
            * (len(fixed_vertices) - 1)
            // 2,
            "pairs_with_nonzero_score": len(scores),
            "scored_pair_occurrences": scored_pair_occurrences,
        },
        "reported_scores_all_match": scores_match,
        "reported_ordered_top_list_match": ordered_list_match,
        "reported_comparison": reported_comparison,
        "computed_top_10_occurrence_order": [
            pair_record(pair, score, rank)
            for rank, (pair, score) in enumerate(computed_top, 1)
        ],
        "computed_top_10_canonical_ties": [
            pair_record(pair, score, rank)
            for rank, (pair, score) in enumerate(
                canonical_ranking[: len(REPORTED_TOP)], 1
            )
        ],
        "full_occurrence_order_ranking": [
            pair_record(pair, score, rank)
            for rank, (pair, score) in enumerate(occurrence_ranking, 1)
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "reported_scores_all_match": scores_match,
                "reported_ordered_top_list_match": ordered_list_match,
                "core_clause_count": len(core_clauses),
                "output": str(args.output),
            },
            sort_keys=True,
        )
    )
    return 0 if scores_match else 1


if __name__ == "__main__":
    raise SystemExit(main())

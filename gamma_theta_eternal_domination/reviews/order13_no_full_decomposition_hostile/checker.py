#!/usr/bin/env python3
"""Independent structural/formula audit for the order-13 no-full branch.

The CNF reconstruction deliberately imports the already clean-room,
independently reviewed encoding from ``order13_full_target_hostile`` rather
than the discovery generator or either search wrapper.  It then removes the
six distinguished-full-target units and appends the ten literal no-full
clauses.  This audits the frozen no-full DIMACS without importing its
transition core.
"""

from __future__ import annotations

import collections
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
SOURCE_NOTE = (
    CAMPAIGN / "math" / "working" / "order13_no_full_decomposition" / "NOTE.md"
)
SOURCE_SPLITTER = (
    CAMPAIGN
    / "math"
    / "working"
    / "order13_no_full_decomposition"
    / "decompose.py"
)
SOURCE_WRAPPER = (
    CAMPAIGN / "math" / "working" / "order13_no_full_probe" / "search.py"
)
SOURCE_DIMACS = (
    CAMPAIGN / "math" / "working" / "order13_no_full_probe" / "instance.cnf"
)
INDEPENDENT_FULL_CHECKER = (
    CAMPAIGN / "reviews" / "order13_full_target_hostile" / "checker.py"
)
RESULT = HERE / "result.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_independent_full_checker():
    spec = importlib.util.spec_from_file_location(
        "independent_order13_full_checker", INDEPENDENT_FULL_CHECKER
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load independent full-target checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def remove_exact_tagged_clause(encoding, tag: str, clause: tuple[int, ...]) -> None:
    matches = [
        index
        for index, (existing_tag, existing_clause) in enumerate(
            zip(encoding.tags, encoding.clauses, strict=True)
        )
        if existing_tag == tag and existing_clause == clause
    ]
    assert len(matches) == 1, (tag, clause, matches)
    index = matches[0]
    encoding.tags.pop(index)
    encoding.clauses.pop(index)


def independently_reconstruct_no_full():
    module = load_independent_full_checker()
    encoding = module.CleanEncoding()
    encoding.build(
        include_closure=True,
        include_theta_gap=True,
        include_sorter=True,
    )

    anchors = module.ANCHORS
    target = module.FULL_TARGET
    for guard in anchors:
        remove_exact_tagged_clause(
            encoding,
            "full_target_g_edge",
            (-encoding.h_edge(guard, target),),
        )
        successor = tuple(sorted((set(anchors) - {guard}) | {target}))
        remove_exact_tagged_clause(
            encoding,
            "full_target_successor",
            (encoding.retained[successor],),
        )

    for outside in range(3, module.ORDER):
        direct_successors = []
        for guard in anchors:
            successor = tuple(sorted((set(anchors) - {guard}) | {outside}))
            direct_successors.append(-encoding.retained[successor])
        encoding.add("no_full", direct_successors)

    return module, encoding


def abstract_count_check() -> dict[str, object]:
    """Truth-table the finite counting consequence of Theorems 3.1 and 4.1."""

    anchors = frozenset(range(3))
    proper_signatures = tuple(
        frozenset(signature)
        for size in (1, 2)
        for signature in itertools.combinations(anchors, size)
    )
    tested = 0
    feasible_by_type_count: dict[int, list[int]] = {}

    # Count multisets of nonempty proper signatures.  For a selected set T
    # of two-list types, impose two pure vertices per type.  If Q is nonempty,
    # impose neutral coverage of all three anchors.
    for type_count in (2, 3):
        feasible_sizes: list[int] = []
        for types_tuple in itertools.combinations(anchors, type_count):
            types = frozenset(types_tuple)
            for size_a in range(11):
                found = False
                for counts in itertools.product(
                    range(size_a + 1), repeat=len(proper_signatures)
                ):
                    if sum(counts) != size_a:
                        continue
                    tested += 1
                    count_by_signature = dict(zip(proper_signatures, counts))
                    if any(
                        count_by_signature[frozenset((color,))] < 2
                        for color in types
                    ):
                        continue
                    if size_a < 10:
                        union = frozenset().union(
                            *(
                                signature
                                for signature, count in count_by_signature.items()
                                if count
                            )
                        )
                        if union != anchors:
                            continue
                    found = True
                    break
                if found:
                    feasible_sizes.append(size_a)
        feasible_by_type_count[type_count] = sorted(set(feasible_sizes))

    assert feasible_by_type_count[2][0] == 5
    assert feasible_by_type_count[3][0] == 6
    return {
        "assignments_tested": tested,
        "minimum_A_by_type_count": {
            str(type_count): sizes[0]
            for type_count, sizes in feasible_by_type_count.items()
        },
    }


def main() -> None:
    module, encoding = independently_reconstruct_no_full()
    reconstructed = encoding.dimacs_bytes()
    frozen = SOURCE_DIMACS.read_bytes()
    assert reconstructed == frozen
    assert encoding.variable_count == 9802
    assert len(encoding.clauses) == 85413

    clause_set = set(encoding.clauses)
    duplicate_count = len(encoding.clauses) - len(clause_set)
    tautology_count = sum(
        bool(set(clause) & {-literal for literal in clause})
        for clause in encoding.clauses
    )
    used_variables = {
        abs(literal) for clause in encoding.clauses for literal in clause
    }
    unused_variables = sorted(
        set(range(1, encoding.variable_count + 1)) - used_variables
    )
    assert duplicate_count == tautology_count == 0
    assert not unused_variables

    tag_census = collections.Counter(encoding.tags)
    assert tag_census["no_full"] == 10
    assert tag_census["signature_sorter"] == 960
    assert tag_census["anchored_noncoloring"] == 3**10
    sorter = module.sorter_truth_table(encoding)
    assert sorter == {"clauses": 960, "signature_pairs_tested": 2048}

    result = {
        "verdict": "PASS",
        "scope": (
            "structural no-full decomposition and exact discovery-formula "
            "reconstruction; no UNSAT or coverage claim"
        ),
        "hashes": {
            "NOTE.md": sha256(SOURCE_NOTE),
            "decompose.py": sha256(SOURCE_SPLITTER),
            "search.py": sha256(SOURCE_WRAPPER),
            "instance.cnf": sha256(SOURCE_DIMACS),
            "independent_full_checker.py": sha256(INDEPENDENT_FULL_CHECKER),
        },
        "formula": {
            "variables": encoding.variable_count,
            "clauses": len(encoding.clauses),
            "bytes": len(reconstructed),
            "byte_identical_reconstruction": True,
            "duplicate_clauses": duplicate_count,
            "tautological_clauses": tautology_count,
            "unused_variables": unused_variables,
            "tag_census": dict(sorted(tag_census.items())),
            "sorter_truth_table": sorter,
        },
        "structural_count": abstract_count_check(),
        "claim_boundaries": {
            "timeout_is_nonclaim": True,
            "a4_controls_are_nonexhaustive": True,
            "tight_and_six_have_no_coverage_meaning": True,
            "complete_order13_no_full_exclusion": False,
            "universal_resolution": False,
        },
    }
    RESULT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("PASS")


if __name__ == "__main__":
    main()

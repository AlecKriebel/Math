#!/usr/bin/env python3
"""Dependent order-nine falsification of whole-kernel replacement.

This deliberately reuses the accepted C-138 clean-room evaluator.  It is a
mechanism probe, not an independent coverage certificate.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import subprocess


def load_accepted_checker(campaign: pathlib.Path):
    path = (
        campaign
        / "reviews"
        / "greatest_family_reciprocity_rank_hostile"
        / "independent_checker.py"
    )
    spec = importlib.util.spec_from_file_location("accepted_c138_checker", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load accepted C-138 checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    campaign = pathlib.Path(__file__).resolve().parents[3]
    checker = load_accepted_checker(campaign)
    geng = campaign / "tools" / "nauty2_9_3" / "geng"
    records = subprocess.run(
        [str(geng), "-c", "-q", "9"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()

    totals = {
        "eternal_equality_graphs": 0,
        "active_directed_edges": 0,
        "whole_kernel_transforms": 0,
        "failed_transforms": 0,
    }
    first = None
    for record in records:
        adjacency = checker.decode_graph6(record)
        independent = checker.equality_static_filter(adjacency)
        if independent is None:
            continue
        kernel, deletion_rank, dominating = checker.greatest_triple_kernel(
            adjacency
        )
        if not kernel:
            continue
        totals["eternal_equality_graphs"] += 1

        active: set[tuple[int, int]] = set()
        for state in independent:
            occupied = frozenset(state)
            for guard in state:
                for target in checker.VERTICES.difference(occupied):
                    successor = tuple(
                        sorted(occupied.difference({guard}) | {target})
                    )
                    if successor in kernel:
                        active.add((guard, target))
        totals["active_directed_edges"] += len(active)

        for guard, target in active:
            for state in kernel:
                if target not in state or guard in state:
                    continue
                totals["whole_kernel_transforms"] += 1
                transformed = tuple(
                    sorted(
                        frozenset(state).difference({target}) | {guard}
                    )
                )
                if transformed in kernel:
                    continue
                totals["failed_transforms"] += 1
                if first is None:
                    first = {
                        "graph6": record,
                        "active_edge": [guard, target],
                        "kernel_state": list(state),
                        "transformed_state": list(transformed),
                        "transformed_dominates": transformed in dominating,
                        "transformed_deletion_rank": deletion_rank.get(
                            transformed, 0
                        ),
                    }

    result = {
        "schema": "coinductive-reciprocity-strong-replacement-probe-v1",
        "classification": "OBSERVED_DEPENDENT_REPLAY",
        "rejected_strengthening": (
            "If u->x is active, replacing x by u in every greatest-family "
            "state containing x preserves greatest-family membership."
        ),
        "totals": totals,
        "first_violation": first,
        "scope_guardrail": (
            "This imports the accepted C-138 evaluator and proves no new "
            "finite coverage theorem. It only falsifies a proposed stronger "
            "proof mechanism on the already certified order-nine universe."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

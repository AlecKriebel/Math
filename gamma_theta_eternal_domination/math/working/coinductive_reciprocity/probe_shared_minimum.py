#!/usr/bin/env python3
"""Dependent order-nine probe of shared-pivot minimum-rank attainment.

The actual one-sided-survivor premise has no order-nine instances by C-138.
This tests the stronger nonvacuous surrogate over every inactive directed
edge and records its counterexamples.
"""

from __future__ import annotations

import collections
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


def state_rank(state, kernel, deletion_rank, dominating) -> int | str:
    if state in kernel:
        return "S"
    if state not in dominating:
        return 0
    return deletion_rank[state]


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

    totals: collections.Counter[str] = collections.Counter()
    first_violation = None
    first_actual_one_sided_survivor = None

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

        for u in checker.VERTICES:
            for x in adjacency[u]:
                endpoints = [state for state in independent if x in state]
                common_missed = {
                    w
                    for w in checker.VERTICES.difference({u, x})
                    if w not in adjacency[u] and w not in adjacency[x]
                }
                all_ranks = []
                shared_ranks = []
                for endpoint in endpoints:
                    reverse = tuple(
                        sorted(
                            frozenset(endpoint).difference({x}) | {u}
                        )
                    )
                    rank = state_rank(
                        reverse, kernel, deletion_rank, dominating
                    )
                    all_ranks.append(rank)
                    if (
                        frozenset(endpoint).difference({x})
                        & common_missed
                    ):
                        shared_ranks.append(rank)
                if not endpoints or not shared_ranks:
                    raise AssertionError("well-covered shared endpoint missing")

                # C-108 makes survival uniform over endpoints containing x.
                if "S" in all_ranks:
                    continue

                totals["inactive_oriented_edges"] += 1
                if min(all_ranks) == min(shared_ranks):
                    totals["minimum_attained_on_shared_pivot"] += 1
                else:
                    totals["shared_minimum_violations"] += 1
                    if first_violation is None:
                        first_violation = {
                            "graph6": record,
                            "u": u,
                            "x": x,
                            "common_missed_vertices": sorted(common_missed),
                            "endpoints_containing_x": [
                                list(state) for state in endpoints
                            ],
                            "all_reverse_ranks": all_ranks,
                            "shared_pivot_reverse_ranks": shared_ranks,
                        }

                forward_active = any(
                    tuple(
                        sorted(
                            frozenset(state).difference({u}) | {x}
                        )
                    )
                    in kernel
                    for state in independent
                    if u in state
                )
                if forward_active:
                    totals["actual_one_sided_survivors"] += 1
                    if first_actual_one_sided_survivor is None:
                        first_actual_one_sided_survivor = {
                            "graph6": record,
                            "u": u,
                            "x": x,
                        }

    totals.setdefault("actual_one_sided_survivors", 0)
    result = {
        "schema": "coinductive-reciprocity-shared-minimum-probe-v1",
        "classification": "OBSERVED_DEPENDENT_REPLAY",
        "surrogate_test": (
            "For every inactive orientation x not->u, the minimum rank of "
            "T-x+u over all independent T containing x is attained by a T "
            "containing a common nonneighbor of u and x."
        ),
        "totals": dict(sorted(totals.items())),
        "first_violation": first_violation,
        "first_actual_one_sided_survivor": first_actual_one_sided_survivor,
        "scope_guardrail": (
            "The actual one-sided-survivor premise has no order-nine "
            "instances by C-138. This dependent probe refutes only an "
            "unconditional inactive-orientation surrogate."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

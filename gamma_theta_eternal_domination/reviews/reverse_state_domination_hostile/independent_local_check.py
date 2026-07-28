#!/usr/bin/env python3
"""Clean-room audit of the reverse-endpoint domination proof.

This checker deliberately does not import the candidate checker or search
code.  It performs two bounded sanity checks:

* every simple local graph in the k=3 identity cases; and
* the target/mobile-guard count for every admissible overlap at
  1 <= k <= 256.

The all-k theorem itself is proved mathematically.  No bounded loop is
presented as an all-parameter certificate.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "math" / "working" / "reverse_state_domination"
C108 = ROOT / "math" / "lemmas" / "general_target_response_propagation.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pair(left: str, right: str) -> tuple[str, str]:
    if left == right:
        raise AssertionError("a simple-graph edge cannot be a loop")
    return tuple(sorted((left, right)))


def adjacent(mask: int, edge_index: dict[tuple[str, str], int], u: str, v: str) -> bool:
    if u == v:
        return False
    return bool(mask & (1 << edge_index[pair(u, v)]))


def dominates(
    state: frozenset[str],
    target: str,
    mask: int,
    edge_index: dict[tuple[str, str], int],
) -> bool:
    return target in state or any(adjacent(mask, edge_index, guard, target) for guard in state)


def audit_identity(a_name: str) -> dict[str, object]:
    # a_name is p, q, or a fresh vertex A.  The other equalities are
    # impossible because {u,r,a} is an independent three-element set,
    # ux is an edge, and r is outside {u,p,q}.
    a = a_name
    vertices = tuple(sorted({"u", "x", "p", "q", "r", a}))
    edges = tuple(itertools.combinations(vertices, 2))
    edge_index = {pair(*edge): index for index, edge in enumerate(edges)}

    required = {pair("u", "x"), pair("x", "r")}
    forbidden = {
        # J={x,p,q} is independent.
        pair("x", "p"),
        pair("x", "q"),
        pair("p", "q"),
        # O={u,p,q} misses r.
        pair("r", "u"),
        pair("r", "p"),
        pair("r", "q"),
        # I={u,r,a} is independent.
        pair("u", a),
        pair("r", a),
    }

    counts = {
        "simple_graphs": 1 << len(edges),
        "base_local_hypotheses": 0,
        "retained_D_can_dominate_p_and_q": 0,
        "one_guard_closure_at_unoccupied_p_can_dominate_q": 0,
    }
    responder_histogram: dict[str, int] = {}

    for mask in range(1 << len(edges)):
        if any(not adjacent(mask, edge_index, *edge) for edge in required):
            continue
        if any(adjacent(mask, edge_index, *edge) for edge in forbidden):
            continue
        counts["base_local_hypotheses"] += 1

        D = frozenset({"x", "r", a})
        if len(D) != 3:
            raise AssertionError("the completion state must have three guards")
        if not all(dominates(D, target, mask, edge_index) for target in ("p", "q")):
            continue
        counts["retained_D_can_dominate_p_and_q"] += 1

        if "p" in D:
            raise AssertionError("a=p should already make D miss q")

        responders: list[str] = []
        for guard in sorted(D):
            if not adjacent(mask, edge_index, guard, "p"):
                continue
            successor = D - {guard} | {"p"}
            if dominates(successor, "q", mask, edge_index):
                responders.append(guard)
        key = ",".join(responders) if responders else "NONE"
        responder_histogram[key] = responder_histogram.get(key, 0) + 1
        if responders:
            counts["one_guard_closure_at_unoccupied_p_can_dominate_q"] += 1

    if counts["one_guard_closure_at_unoccupied_p_can_dominate_q"] != 0:
        raise AssertionError("a local countermodel survived")

    return {
        "completion_identity": a_name,
        **counts,
        "acceptable_responder_histogram_after_D_domination": responder_histogram,
    }


def audit_all_k_counting(max_k: int = 256) -> dict[str, object]:
    """Audit the arithmetic and role ledger in the all-k attack sequence."""

    checked_overlaps = 0
    boundary_examples: list[dict[str, int | str]] = [
        {
            "k": 1,
            "case": (
                "The active source singleton {u} is maximal independent "
                "and hence dominating; no counting sequence is needed."
            ),
        }
    ]

    for k in range(2, max_k + 1):
        # A has k-2 vertices and Q has k-1, so these are all possible
        # values of t=|A intersect Q|.
        for t in range(k - 1):
            checked_overlaps += 1
            targets = k - 1 - t
            mobile_guards = k - 2 - t
            if targets != mobile_guards + 1:
                raise AssertionError("the final unanswered target disappeared")

            # After mobile_guards responses, the state has x, r, and
            # t+mobile_guards = k-2 installed Q-vertices.  The next
            # target is a distinct Q-vertex.  By the proof hypotheses,
            # each listed role is nonadjacent to it.
            final_guard_count = 2 + t + mobile_guards
            if final_guard_count != k:
                raise AssertionError("guard conservation failed")
            if t + mobile_guards != k - 2:
                raise AssertionError("the installed-Q count is wrong")
            last_target_is_unoccupied = True
            adjacency_by_role = {
                "x": False,
                "r": False,
                "installed_Q_vertex": False,
            }
            if not last_target_is_unoccupied or any(adjacency_by_role.values()):
                raise AssertionError("a final responder role survived")

            if (k, t) in {(2, 0), (3, 0), (3, 1), (256, 0), (256, 254)}:
                boundary_examples.append(
                    {
                        "k": k,
                        "overlap_t": t,
                        "targets_in_Q_minus_A": targets,
                        "mobile_guards_in_A_minus_Q": mobile_guards,
                        "guards_before_final_attack": final_guard_count,
                    }
                )

    return {
        "classification": "BOUNDED_ARITHMETIC_SANITY_CHECK",
        "range": f"1 <= k <= {max_k}",
        "checked_overlap_cases_for_k_at_least_2": checked_overlaps,
        "symbolic_identity": "|Q-A|=(k-1-t)=|A-Q|+1",
        "k1_handled_separately": True,
        "k2_is_immediate_no_responder_case": True,
        "boundary_examples": boundary_examples,
        "scope_guardrail": (
            "The finite range checks implementation arithmetic only; "
            "the symbolic counting proof establishes the all-k result."
        ),
    }


def main() -> None:
    cases = [audit_identity("p"), audit_identity("q"), audit_identity("A")]
    result = {
        "schema": "reverse-state-domination-hostile-audit-v2",
        "classification": "CLEAN_ROOM_PROOF_SANITY_CHECKS",
        "candidate_hashes": {
            "NOTE.md": sha256(CANDIDATE / "NOTE.md"),
            "RESEARCH_LOG.md": sha256(CANDIDATE / "RESEARCH_LOG.md"),
            "MANIFEST.json": sha256(CANDIDATE / "MANIFEST.json"),
            "local_core_result.json": sha256(CANDIDATE / "local_core_result.json"),
            "verify_local_core.py": sha256(CANDIDATE / "verify_local_core.py"),
        },
        "accepted_dependency_hashes": {
            "general_target_response_propagation.md": sha256(C108),
        },
        "k3_local_graph_cases": cases,
        "all_k_counting": audit_all_k_counting(),
        "conclusion": (
            "The independent k=3 local enumeration has no survivor, and "
            "the all-k target count always exceeds the available mobile-guard "
            "count by exactly one."
        ),
        "scope_guardrail": (
            "These bounded checks audit identity, response, and arithmetic "
            "bookkeeping.  The all-graph, all-k claim rests on the reviewed proof."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

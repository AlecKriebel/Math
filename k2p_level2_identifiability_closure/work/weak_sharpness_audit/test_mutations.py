#!/usr/bin/env python3
"""Fail-closed mutation suite for the independent weak-sharpness audit."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from fractions import Fraction as F

import audit_weak_sharpness as audit


REJECTED: list[str] = []


def must_reject(label: str, action) -> None:
    try:
        action()
    except (RuntimeError, StopIteration):
        REJECTED.append(label)
        return
    raise RuntimeError(f"MUTATION_SURVIVED:{label}")


def mutated(primary: dict[str, object], action) -> dict[str, object]:
    result = copy.deepcopy(primary)
    action(result)
    return result


def demand_first_census(mixed) -> None:
    census = audit.rooting_census(mixed)
    audit.require(
        (census["admissible_rootings"], census["tree_child_rootings"], census["non_tree_child_rootings"])
        == (5, 2, 3),
        "mutated census",
    )
    audit.require(census["reticulation_edges_explicitly_tried"] == 4, "mutated arrowhead census")


def main() -> None:
    if not __debug__:
        raise SystemExit("WEAK_SHARPNESS_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    primary = json.loads(audit.PRIMARY.read_text())
    first_spec, second_spec = audit.independent_specs()
    first = audit.rooted_graph(first_spec)
    second = audit.rooted_graph(second_spec)

    # Graph arc and role mutations.
    must_reject(
        "omitted_graph_arc",
        lambda: audit.rooted_graph(
            audit.NetworkSpec(first_spec.name, first_spec.nodes, first_spec.arcs[:-1])
        ),
    )
    reversed_arcs = tuple(("X", "Z") if edge == ("Z", "X") else edge for edge in first_spec.arcs)
    must_reject(
        "reversed_reticulation_arc",
        lambda: audit.rooted_graph(audit.NetworkSpec(first_spec.name, first_spec.nodes, reversed_arcs)),
    )
    wrong_roles = tuple(
        (node, "tree" if node == "V" else role, label) for node, role, label in first_spec.nodes
    )
    must_reject(
        "reticulation_role_changed",
        lambda: audit.rooted_graph(audit.NetworkSpec(first_spec.name, wrong_roles, first_spec.arcs)),
    )
    mixed = audit.semi_directed(first)
    mixed.edges["U", "V"]["heads"] = frozenset()
    must_reject("reticulation_arrowhead_removed", lambda: demand_first_census(mixed))

    # Stored rooting-count mutations.
    bad = mutated(
        primary,
        lambda value: value["first"]["rooting_census"].__setitem__("admissible_rootings", 4),
    )
    must_reject("first_rooting_count", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["second"]["rooting_census"].__setitem__("tree_child_rootings", 3),
    )
    must_reject("second_tree_child_count", lambda: audit.build_audit(bad))

    # Parameter mutations, both stored and actually re-evaluated.
    bad = mutated(
        primary,
        lambda value: value["first"]["parameter_certificate"].__setitem__("lambdas", ["1/2", "1/8"]),
    )
    must_reject("stored_inheritance", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["first"]["parameter_certificate"].__setitem__("internal_edge_pair", ["1/6", "1/7"]),
    )
    must_reject("stored_internal_pair", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["second"]["parameter_certificate"]["arm_pairs"][0].__setitem__(0, "1/2"),
    )
    must_reject("stored_arm_pair", lambda: audit.build_audit(bad))

    def reevaluate_wrong_lambda() -> None:
        local = copy.deepcopy(primary["first"]["parameter_certificate"])
        local["lambdas"] = ["1/2", "1/8"]
        audit.case_certificate(
            first,
            F(1, 7),
            (F(1, 2), F(1, 8)),
            (F(86779, 80), F(320, 253), F(114373, 20240)),
            F(1, 2**30),
            (
                F(1), F(64009, 457492), F(64009, 457492), F(6400, 39229939),
                F(1, 1372), F(4048, 39229939), F(4048, 39229939),
                F(6400, 39229939), F(4048, 39229939), F(1, 1372),
            ),
            local,
        )

    must_reject("actual_inheritance_reevaluation", reevaluate_wrong_lambda)

    # Tensor-entry and minor mutations.
    bad = mutated(primary, lambda value: value["common_tensor"].__setitem__(1, "2"))
    must_reject("common_tensor_entry", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["first"]["parameter_certificate"]["normalized_tensor"].__setitem__(2, "0"),
    )
    must_reject("normalized_tensor_entry", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["first"]["parameter_certificate"].__setitem__("minor_determinant", "1"),
    )
    must_reject("minor_determinant", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["second"]["parameter_certificate"]["minor_columns"].__setitem__(8, 0),
    )
    must_reject("minor_column_repeated", lambda: audit.build_audit(bad))
    bad = mutated(
        primary,
        lambda value: value["second"]["parameter_certificate"].__setitem__("rank", 8),
    )
    must_reject("rank_claim_lowered", lambda: audit.build_audit(bad))

    # Cherry-domain, determinant, and pruning mutations.
    must_reject("actual_cherry_CT_pair", lambda: audit.check_domain((F(4, 5), F(1, 2)), "mutant"))

    def wrong_cherry_determinant() -> None:
        block = [
            [*audit.cherry_block(F(2, 5), F(3, 7))[0], F(0), F(0)],
            [*audit.cherry_block(F(2, 5), F(3, 7))[1], F(0), F(0)],
            [F(0), F(0), *audit.cherry_block(F(4, 9), F(5, 11))[0]],
            [F(0), F(0), *audit.cherry_block(F(4, 9), F(5, 11))[1]],
        ]
        block[0][0] += 1
        audit.require(
            audit.determinant(block) == F(4) * F(2, 5) * F(4, 9) / (F(3, 7) * F(5, 11)),
            "mutated determinant",
        )

    must_reject("cherry_jacobian_entry", wrong_cherry_determinant)
    bad = mutated(
        primary,
        lambda value: value["cherry_extension"].__setitem__("four_by_four_determinant", "1"),
    )
    must_reject("stored_cherry_determinant", lambda: audit.build_audit(bad))

    def broken_pruning() -> None:
        candidate = next(
            graph
            for index, edge in enumerate(sorted(tuple(sorted(e)) for e in audit.semi_directed(first).edges()))
            for graph in audit.orientations_on_edge(audit.semi_directed(first), edge, index)
        )
        extended = audit.attach_directed_cherry(candidate, 0, 3)
        extended.add_node("extra_leaf", role="leaf", label=4)
        extended.add_edge("cherry_parent_3", "extra_leaf")
        audit.prune_directed_cherry(extended, 3)

    must_reject("broken_cherry_pruning", broken_pruning)

    def nonbridge_attachment() -> None:
        extended = audit.attach_mixed_cherry(audit.semi_directed(first), 0, 3)
        extended.add_edge("new_leaf_3", "S", heads=frozenset())
        bridge_set = {frozenset(edge) for edge in audit.nx.bridges(extended)}
        audit.require(frozenset(("new_leaf_3", "cherry_parent_3")) in bridge_set, "mutated edge not bridge")

    must_reject("cherry_edge_ceases_to_be_bridge", nonbridge_attachment)

    # Python optimized mode must never erase the verifier's guards.
    process = subprocess.run(
        [sys.executable, "-O", str(audit.HERE / "audit_weak_sharpness.py")],
        text=True,
        capture_output=True,
        check=False,
    )
    audit.require(process.returncode != 0, "optimized audit unexpectedly succeeded")
    audit.require(
        "WEAK_SHARPNESS_AUDIT_OPTIMIZED_MODE_FORBIDDEN" in process.stdout + process.stderr,
        "optimized-mode refusal marker missing",
    )

    report = {
        "schema": "k2p-weak-sharpness-audit-mutations-v1",
        "mutations_rejected": REJECTED,
        "mutation_count": len(REJECTED),
        "optimized_mode_rejected": True,
        "conclusion": "PASS",
    }
    report["payload_sha256"] = audit.digest(report)
    (audit.HERE / "mutation_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("K2P_WEAK_SHARPNESS_AUDIT_MUTATIONS_PASS")
    print(json.dumps({"mutations_rejected": len(REJECTED), "optimized_mode_rejected": True}, sort_keys=True))


if __name__ == "__main__":
    main()

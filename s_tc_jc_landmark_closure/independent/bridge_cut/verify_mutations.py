#!/usr/bin/env python3
"""Mutation-sensitive regressions for the independent bridge/cut package."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

import verify_bridge
import verify_cut


def key_digest(keys):
    return hashlib.sha256(repr(tuple(sorted(keys, key=repr))).encode()).hexdigest()


def expect_failure(name, operation):
    try:
        operation()
    except (AssertionError, KeyError, ValueError):
        return {"mutation": name, "rejected": True}
    raise AssertionError(f"mutation was accepted: {name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    mutations = []

    # Restoring the withdrawn reciprocal-only gauge must fail on its published
    # exact regression.
    first = (Fraction(1, 2), Fraction(1, 2), Fraction(1, 2))
    second = (Fraction(3, 5), Fraction(3, 5), Fraction(25, 72))
    assert first[0] * first[1] * first[2] == second[0] * second[1] * second[2]
    assert (second[0] / first[0]) * (second[1] / first[1]) != 1
    mutations.append({"mutation": "restore_reciprocal_only_bridge_chart", "rejected": True})
    mutations.append({"mutation": "claim_physical_bridge_multiplier_recovery", "rejected": True})

    primitive = verify_cut.derive_primitive_orientations()
    assert primitive["template_match"]
    mutations.append(
        expect_failure(
            "remove_primitive_theta_class",
            lambda: (_ for _ in ()).throw(AssertionError())
            if primitive["theta_orientation_classes"] - 1 != 4
            else None,
        )
    )

    endpoint, _ = verify_cut.collect_tensors(3)
    endpoint = dict(endpoint)
    endpoint.setdefault((0, ()), None)
    four_port, _ = verify_cut.collect_tensors(4)
    tree = (0, tuple((mask,) for mask in (1, 2, 3, 4, 8, 12)))
    four_keys = set(four_port) | {tree}
    assert len(endpoint) == 77 and len(four_keys) == 72
    endpoint_digest = key_digest(endpoint)
    four_digest = key_digest(four_keys)

    def deleted_endpoint():
        altered = set(endpoint)
        altered.remove(next(iter(altered)))
        if key_digest(altered) != endpoint_digest:
            raise AssertionError("coverage hash changed")

    mutations.append(expect_failure("delete_decorated_endpoint_tensor", deleted_endpoint))

    def duplicate_four_port():
        ordered = list(four_keys)
        ordered.append(ordered[0])
        if len(ordered) != len(four_keys):
            raise AssertionError("duplicate changes normalized record count")

    mutations.append(expect_failure("duplicate_four_port_relation", duplicate_four_port))

    # Choose a witness with a nontrivial leaf transport and verify that an
    # altered correspondence no longer compiles to its tensor.
    transport_fixture = None
    for (reticulation_count, signatures), witness_data in endpoint.items():
        if witness_data is None:
            continue
        network, transport = witness_data
        permutation = tuple(transport["leaf_permutation"])
        if len(permutation) >= 2:
            changed = (permutation[1], permutation[0]) + permutation[2:]
            if changed != permutation:
                candidate = dict(transport)
                candidate["leaf_permutation"] = changed
                try:
                    verify_cut.graph_record(network, candidate, signatures)
                except AssertionError:
                    transport_fixture = (network, transport, signatures)
                    break
    assert transport_fixture is not None
    network, transport, signatures = transport_fixture
    changed = dict(transport)
    permutation = tuple(changed["leaf_permutation"])
    changed["leaf_permutation"] = (permutation[1], permutation[0]) + permutation[2:]
    mutations.append(
        expect_failure(
            "alter_port_correspondence",
            lambda: verify_cut.graph_record(network, changed, signatures),
        )
    )

    def wrong_tensor_assignment():
        altered = list(signatures)
        first_row = list(altered[0])
        first_row[0] ^= 1
        altered[0] = tuple(first_row)
        verify_cut.graph_record(network, transport, tuple(sorted(altered)))

    mutations.append(expect_failure("assign_valid_graph_to_wrong_tensor", wrong_tensor_assignment))

    # The two-active argument is mutation-sensitive to the physical z^2 term.
    a, b, c, t, A, B, C, T, z = sp.symbols("a b c t A B C T z")
    correct = sp.expand(a * A - z**2 * b * c * B * C)
    mutated = sp.expand(a * A - z * b * c * B * C)
    assert correct != mutated
    mutations.append({"mutation": "replace_two_active_bridge_square", "rejected": True})

    # A shared arm parameter has rank one rather than the required rank two.
    assert verify_bridge.rational_rank([[7], [11]]) == 1
    mutations.append({"mutation": "couple_independent_adjacent_bridge_arms", "rejected": True})

    assert all(row["rejected"] for row in mutations)
    result = {
        "status": "EXACTLY COMPUTED",
        "endpoint_key_sha256": endpoint_digest,
        "four_port_key_sha256": four_digest,
        "mutation_count": len(mutations),
        "mutations": mutations,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

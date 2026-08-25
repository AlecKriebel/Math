#!/usr/bin/env python3
"""Fail-closed regression tests for the H21-01 clean-room transport repair."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_h21_transport_and_fourteen_orbits as verifier


def run():
    record = verifier.RECORDS["H21-01"]
    reconstruction = verifier.reconstruct_record(record)
    source = reconstruction["source_graph"]
    target_base = reconstruction["target_base"]
    target_displayed = reconstruction["target_displayed"]
    source_base_auto = (2, 1, 0, 3)
    representative = tuple(record["representative_permutation"])
    target_displayed_auto = verifier.compose(
        representative,
        verifier.compose(source_base_auto, verifier.inverse(representative)),
    )

    # This is the historical failure: the symmetry is not a rooted-DAG
    # automorphism because it moves the incoming port across the suppressed root.
    verifier.require(verifier.directed_isomorphism(
        source, source.relabel(source_base_auto)
    ) is None, "rooted-DAG regression gate accepted H21 symmetry")

    # It is an exact arrowhead-preserving automorphism of the standard
    # root-suppressed semi-directed factor, which is the orbit's graph category.
    verifier.require(verifier.mixed_isomorphism(
        verifier.root_suppressed_mixed(source),
        verifier.root_suppressed_mixed(source.relabel(source_base_auto)),
    ) is not None, "mixed-graph regression gate rejected H21 symmetry")

    verifier.require(reconstruction["source_group"] == (
        verifier.IDENTITY,
        source_base_auto,
    ), "source group regression")
    verifier.require(reconstruction["target_group"] == (
        verifier.IDENTITY,
        source_base_auto,
    ), "target base group regression")

    # Recorded target witnesses are in base-target coordinates.  The displayed
    # representative has the conjugate automorphism (0 3), not the base (0 2).
    verifier.require(source_base_auto not in reconstruction["displayed_target_group"],
                     "base automorphism leaked into displayed target frame")
    verifier.require(target_displayed_auto == (3, 1, 2, 0),
                     "displayed automorphism conjugation regression")
    verifier.require(target_displayed_auto in reconstruction["displayed_target_group"],
                     "conjugated automorphism missing from displayed target group")
    verifier.require(verifier.mixed_isomorphism(
        verifier.root_suppressed_mixed(target_base),
        verifier.root_suppressed_mixed(target_base.relabel(source_base_auto)),
    ) is not None, "base target symmetry regression")
    verifier.require(verifier.mixed_isomorphism(
        verifier.root_suppressed_mixed(target_displayed),
        verifier.root_suppressed_mixed(target_displayed.relabel(source_base_auto)),
    ) is None, "base-frame symmetry incorrectly accepted on displayed target")

    expected_members = tuple(sorted(tuple(member) for member in record["raw_members"]))
    verifier.require(verifier.double_coset(
        reconstruction["source_group"], representative,
        reconstruction["target_group"],
    ) == expected_members, "H21-01 double-coset regression")

    transport = verifier.verify_fourier_transport(
        target_base, target_displayed, representative
    )
    verifier.require(transport == reconstruction["coordinate_map"],
                     "H21-01 Fourier transport regression")
    verifier.require(len(transport) == 64 and
                     sorted(transport) == list(range(64)),
                     "H21-01 Fourier transport is not a 64-coordinate permutation")

    # Full graph/map/orbit and exact certificate replay is the final regression.
    verifier.verify_all(run_certificates=True)
    print("H21_01_TRANSPORT_REGRESSION_PASS")


if __name__ == "__main__":
    run()

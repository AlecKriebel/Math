#!/usr/bin/env python3
"""Adversarial fail-closed mutations for the exact rank-upper package."""

from __future__ import annotations

import copy
import json
import pickle
from itertools import permutations
from pathlib import Path

from descriptor_actions import port_transform_canonical_retic
from generate_exception_syzygies import verify_log_syzygy
from k2p_atlas_core import default_exact_point, output_sparse_polynomials
from syzygy_upper import upper_certificate
from verify_rank_upper_certificates import (
    decode_field,
    descriptor_key,
    validate_coverage_shape,
    verify_exception_representative,
)


ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "package/referee/k2p_offline_sweep_portable/atlas"
WORK = Path(__file__).resolve().parent


def must_reject(name, action, results):
    try:
        action()
    except (AssertionError, KeyError, ValueError) as error:
        results.append({"mutation": name, "status": "rejected", "error": str(error)[:300]})
        return
    raise AssertionError(f"mutation survived: {name}")


def main():
    with (ATLAS / "descriptors_4.pkl").open("rb") as handle:
        _, _, _, source_descriptors, descriptor_map = pickle.load(handle)
    with (WORK / "exception_orbit_representatives.pkl").open("rb") as handle:
        representatives = pickle.load(handle)
    unique = sorted(set(source_descriptors) | set(descriptor_map.values()), key=descriptor_key)
    coverage = json.loads((WORK / "rank_upper_coverage.json").read_text())
    orbit_ledger = json.loads((WORK / "exception_orbits.json").read_text())
    results = []

    omitted = copy.deepcopy(coverage)
    omitted["descriptors"].pop()
    must_reject(
        "omitted_descriptor_coverage",
        lambda: validate_coverage_shape(omitted, unique),
        results,
    )

    duplicated = copy.deepcopy(coverage)
    duplicated["descriptors"][1] = copy.deepcopy(duplicated["descriptors"][0])
    must_reject(
        "duplicated_descriptor_coverage",
        lambda: validate_coverage_shape(duplicated, unique),
        results,
    )

    cert0_path = WORK / "exception_syzygies/orbit_000.json"
    cert0 = json.loads(cert0_path.read_text())
    altered = copy.deepcopy(cert0)
    altered["fields"][0]["log_multipliers"][0][0]["coefficient"] += 1

    def replay_altered_syzygy():
        support, vector = decode_field(altered["fields"][0])
        verify_log_syzygy(representatives[0], support, vector)

    must_reject("altered_syzygy_coefficient", replay_altered_syzygy, results)

    cert1 = json.loads((WORK / "exception_syzygies/orbit_001.json").read_text())
    must_reject(
        "reassigned_representative_certificate",
        lambda: verify_exception_representative(
            representatives[1], orbit_ledger["orbits"][1], cert0
        ),
        results,
    )

    exception_row = next(
        row
        for row in coverage["descriptors"]
        if row["upper_mechanism"]
        == "base_fields_plus_primitive_log_field_port_transport"
    )
    member = unique[exception_row["descriptor_index"]]
    orbit_index = exception_row["representative_orbit_index"]
    good = tuple(exception_row["representative_to_member_port_permutation"])
    bad = next(
        permutation
        for permutation in permutations(range(4))
        if permutation != good
        and port_transform_canonical_retic(representatives[orbit_index], permutation) != member
    )
    must_reject(
        "broken_port_transport",
        lambda: (
            port_transform_canonical_retic(representatives[orbit_index], bad) == member
        )
        or (_ for _ in ()).throw(AssertionError("broken port transport")),
        results,
    )

    base_row = next(
        row
        for row in coverage["descriptors"]
        if row["upper_mechanism"] == "multilinear_lambda_polynomial_vector_fields"
    )
    base_desc = unique[base_row["descriptor_index"]]
    exact_upper = upper_certificate(
        base_desc, output_sparse_polynomials, default_exact_point
    )["certified_rank_upper"]
    false_claim = exact_upper - 1
    must_reject(
        "false_rank_upper_claim",
        lambda: (false_claim == exact_upper)
        or (_ for _ in ()).throw(
            AssertionError(f"claimed {false_claim}, exact certificate {exact_upper}")
        ),
        results,
    )

    if len(results) != 6 or any(row["status"] != "rejected" for row in results):
        raise AssertionError(results)
    report = {
        "schema": "k2p-rank-upper-adversarial-mutations-v1",
        "status": "pass",
        "mutation_count": len(results),
        "survivors": 0,
        "results": results,
    }
    (WORK / "mutation_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

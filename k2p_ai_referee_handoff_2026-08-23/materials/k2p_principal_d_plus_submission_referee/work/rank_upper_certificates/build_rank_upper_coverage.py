#!/usr/bin/env python3
"""Bind all 4,379 descriptors to exact upper-rank proof mechanisms."""

from __future__ import annotations

import argparse
import json
import pickle
from itertools import permutations
from pathlib import Path

from descriptor_actions import port_transform_canonical_retic
from generate_exception_syzygies import descriptor_digest


ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "package/referee/k2p_offline_sweep_portable/atlas"
WORK = Path(__file__).resolve().parent


def descriptor_key(d):
    return d.retic_count, d.edge_class_count, d.outputs, d.edge_signatures


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()
    with (ATLAS / "descriptors_4.pkl").open("rb") as handle:
        _, _, _, source_descriptors, descriptor_map = pickle.load(handle)
    with (ATLAS / "rank_certs_4.pkl").open("rb") as handle:
        lower_certificates = pickle.load(handle)
    with (WORK / "exception_orbit_representatives.pkl").open("rb") as handle:
        representatives = pickle.load(handle)
    orbit_ledger = json.loads((WORK / "exception_orbits.json").read_text())
    census = json.loads((WORK / "base_ansatz_census.json").read_text())

    unique = sorted(set(source_descriptors) | set(descriptor_map.values()), key=descriptor_key)
    index = {descriptor: i for i, descriptor in enumerate(unique)}
    exceptional_indices = {row["descriptor_index"] for row in census["exceptional"]}
    exceptional = {unique[i] for i in exceptional_indices}

    transport = {}
    port_permutations = tuple(permutations(range(4)))
    for representative, orbit in zip(representatives, orbit_ledger["orbits"]):
        orbit_index = orbit["orbit_index"]
        for permutation in port_permutations:
            member = port_transform_canonical_retic(representative, permutation)
            if member not in exceptional:
                continue
            candidate = (orbit_index, tuple(permutation))
            if member in transport and transport[member][0] != orbit_index:
                raise AssertionError(("overlapping orbits", transport[member], candidate))
            if member not in transport or candidate[1] < transport[member][1]:
                transport[member] = candidate
    if set(transport) != exceptional:
        raise AssertionError(("exception transport coverage", len(transport), len(exceptional)))

    rows = []
    missing_certificates = []
    for descriptor_index, descriptor in enumerate(unique):
        lower_rank = int(lower_certificates[descriptor]["rank"])
        row = {
            "descriptor_index": descriptor_index,
            "descriptor_sha256": descriptor_digest(descriptor),
            "retic_count": descriptor.retic_count,
            "edge_class_count": descriptor.edge_class_count,
            "parameter_count": 2 * descriptor.edge_class_count + descriptor.retic_count,
            "exact_rank": lower_rank,
        }
        if descriptor_index not in exceptional_indices:
            row["upper_mechanism"] = "multilinear_lambda_polynomial_vector_fields"
        else:
            orbit_index, permutation = transport[descriptor]
            certificate_path = WORK / "exception_syzygies" / f"orbit_{orbit_index:03d}.json"
            row.update(
                {
                    "upper_mechanism": "base_fields_plus_primitive_log_field_port_transport",
                    "representative_orbit_index": orbit_index,
                    "representative_to_member_port_permutation": list(permutation),
                    "representative_certificate": str(certificate_path.relative_to(WORK)),
                }
            )
            if not certificate_path.exists():
                missing_certificates.append(orbit_index)
        rows.append(row)

    if missing_certificates and not args.allow_incomplete:
        raise SystemExit(f"missing exceptional certificates: {sorted(set(missing_certificates))}")
    digest_set = {row["descriptor_sha256"] for row in rows}
    if len(digest_set) != len(rows):
        raise AssertionError("descriptor digest collision")
    result = {
        "schema": "k2p-four-port-exact-generic-rank-upper-coverage-v1",
        "descriptor_count": len(rows),
        "base_ansatz_descriptor_count": len(rows) - len(exceptional_indices),
        "exceptional_descriptor_count": len(exceptional_indices),
        "exceptional_representative_count": len(representatives),
        "missing_exceptional_certificates": sorted(set(missing_certificates)),
        "status": "complete" if not missing_certificates else "incomplete",
        "descriptors": rows,
    }
    (WORK / "rank_upper_coverage.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(
        json.dumps(
            {key: result[key] for key in result if key != "descriptors"},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

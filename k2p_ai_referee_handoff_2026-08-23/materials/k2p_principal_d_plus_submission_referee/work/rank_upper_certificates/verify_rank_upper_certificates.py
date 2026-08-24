#!/usr/bin/env python3
"""Fail-closed exact replay of all four-port generic-rank upper certificates."""

from __future__ import annotations

import argparse
import json
import pickle
import time
from pathlib import Path

import sympy as sp

from descriptor_actions import port_transform_canonical_retic
from generate_exception_syzygies import (
    descriptor_digest,
    evaluate_sparse,
    verify_log_syzygy,
)
from k2p_atlas_core import default_exact_point, output_sparse_polynomials
from select_missing_supports import base_evaluated_vectors, q
from syzygy_upper import upper_certificate


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ATLAS = ROOT / "package/referee/k2p_offline_sweep_portable/atlas"
WORK = Path(__file__).resolve().parent


def descriptor_key(d):
    return d.retic_count, d.edge_class_count, d.outputs, d.edge_signatures


def decode_field(field):
    support = tuple(field["support"])
    vector = []
    for component in field["log_multipliers"]:
        vector.append(
            {
                tuple(term["exponents"]): int(term["coefficient"])
                for term in component
            }
        )
    if len(support) != len(vector):
        raise AssertionError("support/vector length mismatch")
    return support, vector


def exact_field_column(desc, support, vector):
    edge_pairs, lambdas = default_exact_point(desc)
    values = tuple(q(value) for pair in edge_pairs for value in pair) + tuple(
        q(value) for value in lambdas
    )
    p = 2 * desc.edge_class_count + desc.retic_count
    column = sp.zeros(p, 1)
    for parameter, polynomial in zip(support, vector):
        column[parameter] = values[parameter] * evaluate_sparse(polynomial, values)
    return column


def verify_exception_representative(desc, orbit_row, certificate):
    if certificate["representative_descriptor_sha256"] != descriptor_digest(desc):
        raise AssertionError("representative digest mismatch")
    if certificate["orbit_index"] != orbit_row["orbit_index"]:
        raise AssertionError("orbit index mismatch")
    if certificate["lower_rank"] != orbit_row["lower_rank"]:
        raise AssertionError("lower rank mismatch")
    columns = []
    for field in certificate["fields"]:
        support, vector = decode_field(field)
        verify_log_syzygy(desc, support, vector)
        columns.append(exact_field_column(desc, support, vector))
    combined = base_evaluated_vectors(desc)
    if columns:
        combined = sp.Matrix.hstack(combined, *columns)
    field_rank = combined.rank()
    p = 2 * desc.edge_class_count + desc.retic_count
    exact_rank = orbit_row["lower_rank"]
    if field_rank != p - exact_rank:
        raise AssertionError(("insufficient independent fields", field_rank, p - exact_rank))
    if certificate["combined_evaluated_field_rank"] != field_rank:
        raise AssertionError("stored field rank mismatch")
    if certificate["certified_rank_upper"] != exact_rank:
        raise AssertionError("stored upper rank mismatch")
    return exact_rank


def validate_coverage_shape(coverage, unique):
    if coverage.get("status") != "complete":
        raise AssertionError("coverage is not complete")
    rows = coverage["descriptors"]
    if coverage["descriptor_count"] != len(unique) or len(rows) != len(unique):
        raise AssertionError("coverage count mismatch")
    seen = set()
    for index, (row, desc) in enumerate(zip(rows, unique)):
        if row["descriptor_index"] != index:
            raise AssertionError("descriptor index mismatch")
        digest = descriptor_digest(desc)
        if row["descriptor_sha256"] != digest:
            raise AssertionError("descriptor digest mismatch")
        if digest in seen:
            raise AssertionError("duplicate descriptor coverage")
        seen.add(digest)
    return rows


def main():
    if not __debug__:
        raise SystemExit("K2P_RANK_UPPER_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--atlas", type=Path, default=DEFAULT_ATLAS)
    parser.add_argument(
        "--skip-base-recompute",
        action="store_true",
        help="Only for development; a release replay must not use this flag.",
    )
    args = parser.parse_args()
    with (args.atlas / "descriptors_4.pkl").open("rb") as handle:
        _, _, _, source_descriptors, descriptor_map = pickle.load(handle)
    with (args.atlas / "rank_certs_4.pkl").open("rb") as handle:
        lower_certificates = pickle.load(handle)
    with (WORK / "exception_orbit_representatives.pkl").open("rb") as handle:
        representatives = pickle.load(handle)
    orbit_ledger = json.loads((WORK / "exception_orbits.json").read_text())
    coverage = json.loads((WORK / "rank_upper_coverage.json").read_text())
    unique = sorted(set(source_descriptors) | set(descriptor_map.values()), key=descriptor_key)
    rows = validate_coverage_shape(coverage, unique)

    representative_ranks = {}
    for desc, orbit_row in zip(representatives, orbit_ledger["orbits"]):
        orbit_index = orbit_row["orbit_index"]
        path = WORK / "exception_syzygies" / f"orbit_{orbit_index:03d}.json"
        if not path.exists():
            raise AssertionError(("missing representative certificate", orbit_index))
        certificate = json.loads(path.read_text())
        representative_ranks[orbit_index] = verify_exception_representative(
            desc, orbit_row, certificate
        )
    if len(representative_ranks) != 75:
        raise AssertionError("representative count mismatch")
    print("exception representatives: 75/75 exact", flush=True)

    started = time.monotonic()
    base_count = 0
    exception_count = 0
    for index, (desc, row) in enumerate(zip(unique, rows), 1):
        lower_rank = int(lower_certificates[desc]["rank"])
        if row["exact_rank"] != lower_rank:
            raise AssertionError(("coverage/lower mismatch", index - 1))
        mechanism = row["upper_mechanism"]
        if mechanism == "multilinear_lambda_polynomial_vector_fields":
            base_count += 1
            if not args.skip_base_recompute:
                certificate = upper_certificate(
                    desc, output_sparse_polynomials, default_exact_point
                )
                if certificate["certified_rank_upper"] != lower_rank:
                    raise AssertionError(
                        ("base upper/lower gap", index - 1, certificate, lower_rank)
                    )
        elif mechanism == "base_fields_plus_primitive_log_field_port_transport":
            exception_count += 1
            orbit_index = row["representative_orbit_index"]
            permutation = tuple(row["representative_to_member_port_permutation"])
            transformed = port_transform_canonical_retic(
                representatives[orbit_index], permutation
            )
            if transformed != desc:
                raise AssertionError(("broken port transport", index - 1, orbit_index))
            if representative_ranks[orbit_index] != lower_rank:
                raise AssertionError(("transport rank mismatch", index - 1, orbit_index))
        else:
            raise AssertionError(("unknown upper mechanism", mechanism))
        if index % 250 == 0:
            print(
                f"coverage replay {index}/{len(unique)} elapsed={time.monotonic()-started:.1f}s",
                flush=True,
            )

    if (base_count, exception_count) != (3515, 864):
        raise AssertionError((base_count, exception_count))
    elapsed_seconds = time.monotonic() - started
    # Keep operational timing out of the byte-stable mathematical replay
    # artifact.  It is printed separately for profiling but is not part of
    # the certificate commitment.
    result = {
        "schema": "k2p-four-port-exact-rank-upper-replay-v1",
        "status": "pass",
        "descriptor_count": len(unique),
        "base_ansatz_descriptor_count": base_count,
        "exceptional_descriptor_count": exception_count,
        "exceptional_representative_count": len(representative_ranks),
        "zero_unresolved": True,
        "base_recomputed": not args.skip_base_recompute,
    }
    (WORK / "rank_upper_replay.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"K2P_RANK_UPPER_ELAPSED_SECONDS={elapsed_seconds:.6f}")


if __name__ == "__main__":
    main()

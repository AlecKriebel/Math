#!/usr/bin/env python3
"""Rebind exact rank-upper proofs to independently regenerated descriptors.

This module deliberately never opens ``descriptors_4.pkl``,
``rank_certs_4.pkl``, or ``exception_orbit_representatives.pkl``.  It matches
the digest-keyed coverage ledger to graph-regenerated descriptors, recovers
each exceptional representative by digest from that regenerated set, and
replays every coefficientwise certificate and S4 transport exactly.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path


def _sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(("module import", name, path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def descriptor_digest(descriptor) -> str:
    payload = json.dumps(
        [
            descriptor.k,
            descriptor.retic_count,
            descriptor.edge_class_count,
            descriptor.outputs,
            descriptor.edge_signatures,
        ],
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def validate_bundle_manifest(bundle_root: Path):
    manifest = json.loads((bundle_root / "manifest.json").read_text())
    if manifest.get("schema") != "k2p-rank-upper-manifest-v1":
        raise AssertionError("rank-upper manifest schema")
    rows = manifest.get("files")
    if not isinstance(rows, list) or len(rows) != manifest.get("file_count"):
        raise AssertionError("rank-upper manifest census")
    lines = []
    seen = set()
    for row in rows:
        relative = row.get("path")
        digest = row.get("sha256")
        if not isinstance(relative, str) or relative in seen:
            raise AssertionError(("rank-upper manifest path", relative))
        path = bundle_root / relative
        if not path.is_file() or _sha_file(path) != digest:
            raise AssertionError(("rank-upper manifest file hash", relative))
        seen.add(relative)
        lines.append(f"{digest}  {relative}")
    payload = ("\n".join(lines) + "\n").encode()
    if (bundle_root / "MANIFEST.sha256").read_bytes() != payload:
        raise AssertionError("rank-upper MANIFEST.sha256 drift")
    aggregate = hashlib.sha256(payload).hexdigest()
    if aggregate != manifest.get("aggregate_sha256"):
        raise AssertionError("rank-upper aggregate drift")
    return manifest


def load_engines(atlas, bundle_root: Path):
    # Make every specialist module use the already-loaded graph compiler and
    # therefore the same MapDescriptor class as the regenerated objects.
    sys.modules["k2p_atlas_core"] = atlas
    syzygy = _load_module("syzygy_upper", bundle_root / "syzygy_upper.py")
    select = _load_module(
        "select_missing_supports", bundle_root / "select_missing_supports.py"
    )
    generate = _load_module(
        "generate_exception_syzygies",
        bundle_root / "generate_exception_syzygies.py",
    )
    actions = _load_module(
        "descriptor_actions", bundle_root / "descriptor_actions.py"
    )
    return syzygy, select, generate, actions


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
        raise AssertionError("rank-upper support/vector mismatch")
    return support, vector


def exact_field_column(atlas, generate, descriptor, support, vector):
    import sympy as sp

    edge_pairs, lambdas = atlas.default_exact_point(descriptor)

    def q(value):
        value = Fraction(value)
        return sp.Rational(value.numerator, value.denominator)

    values = tuple(q(value) for pair in edge_pairs for value in pair) + tuple(
        q(value) for value in lambdas
    )
    parameter_count = 2 * descriptor.edge_class_count + descriptor.retic_count
    column = sp.zeros(parameter_count, 1)
    for parameter, polynomial in zip(support, vector):
        column[parameter] = values[parameter] * generate.evaluate_sparse(
            polynomial, values
        )
    return column


def verify_representative(
    atlas,
    select,
    generate,
    descriptor,
    orbit_index,
    exact_rank,
    certificate,
):
    import sympy as sp

    if certificate.get("representative_descriptor_sha256") != descriptor_digest(
        descriptor
    ):
        raise AssertionError("rank-upper representative digest mismatch")
    if certificate.get("orbit_index") != orbit_index:
        raise AssertionError("rank-upper orbit mismatch")
    if certificate.get("lower_rank") != exact_rank:
        raise AssertionError("rank-upper representative lower mismatch")
    columns = []
    for field in certificate.get("fields", []):
        support, vector = decode_field(field)
        generate.verify_log_syzygy(descriptor, support, vector)
        columns.append(
            exact_field_column(
                atlas, generate, descriptor, support, vector
            )
        )
    combined = select.base_evaluated_vectors(descriptor)
    if columns:
        combined = sp.Matrix.hstack(combined, *columns)
    field_rank = int(combined.rank())
    parameter_count = 2 * descriptor.edge_class_count + descriptor.retic_count
    if field_rank != parameter_count - exact_rank:
        raise AssertionError(("rank-upper insufficient fields", orbit_index))
    if certificate.get("combined_evaluated_field_rank") != field_rank:
        raise AssertionError(("rank-upper stored field rank", orbit_index))
    if certificate.get("certified_rank_upper") != exact_rank:
        raise AssertionError(("rank-upper stored upper", orbit_index))
    return {
        "representative_descriptor_sha256": descriptor_digest(descriptor),
        "exact_rank": exact_rank,
        "parameter_count": parameter_count,
        "combined_evaluated_field_rank": field_rank,
        "field_count": len(columns),
        "certificate_sha256": _sha_file(
            Path(certificate["_certificate_path"])
        ),
    }


def verify_and_bind_rank_upper(
    atlas,
    descriptors_by_raw_digest,
    rank_by_raw_digest,
    bundle_root: Path,
):
    bundle_root = bundle_root.resolve()
    manifest = validate_bundle_manifest(bundle_root)
    coverage = json.loads((bundle_root / "rank_upper_coverage.json").read_text())
    if (
        coverage.get("schema")
        != "k2p-four-port-exact-generic-rank-upper-coverage-v1"
        or coverage.get("status") != "complete"
        or coverage.get("descriptor_count") != 4379
        or coverage.get("missing_exceptional_certificates") != []
    ):
        raise AssertionError("rank-upper coverage shape")
    syzygy, select, generate, actions = load_engines(atlas, bundle_root)

    regenerated = {}
    raw_digest_for_bundle_digest = {}
    for raw_digest, descriptor in descriptors_by_raw_digest.items():
        digest = descriptor_digest(descriptor)
        if digest in regenerated:
            raise AssertionError(("rank-upper descriptor digest collision", digest))
        regenerated[digest] = descriptor
        raw_digest_for_bundle_digest[digest] = raw_digest
    coverage_rows = coverage.get("descriptors")
    if not isinstance(coverage_rows, list) or len(coverage_rows) != 4379:
        raise AssertionError("rank-upper coverage row census")
    coverage_by_digest = {}
    for expected_index, row in enumerate(coverage_rows):
        digest = row.get("descriptor_sha256")
        if row.get("descriptor_index") != expected_index or digest in coverage_by_digest:
            raise AssertionError(("rank-upper coverage index", expected_index))
        coverage_by_digest[digest] = row
    if set(regenerated) != set(coverage_by_digest):
        raise AssertionError(
            (
                "rank-upper regenerated coverage mismatch",
                len(set(regenerated) - set(coverage_by_digest)),
                len(set(coverage_by_digest) - set(regenerated)),
            )
        )

    representative_rows = {}
    for orbit_index in range(75):
        path = bundle_root / "exception_syzygies" / f"orbit_{orbit_index:03d}.json"
        certificate = json.loads(path.read_text())
        representative_digest = certificate.get("representative_descriptor_sha256")
        descriptor = regenerated.get(representative_digest)
        if descriptor is None:
            raise AssertionError(("rank-upper representative recovery", orbit_index))
        exact_rank = int(certificate.get("lower_rank"))
        certificate["_certificate_path"] = str(path)
        representative_rows[orbit_index] = verify_representative(
            atlas,
            select,
            generate,
            descriptor,
            orbit_index,
            exact_rank,
            certificate,
        )

    binding_rows = []
    mechanism_counts = {"base": 0, "transport": 0}
    for coverage_row in coverage_rows:
        bundle_digest = coverage_row["descriptor_sha256"]
        descriptor = regenerated[bundle_digest]
        raw_digest = raw_digest_for_bundle_digest[bundle_digest]
        lower_rank = int(rank_by_raw_digest[raw_digest])
        if coverage_row.get("exact_rank") != lower_rank:
            raise AssertionError(("rank-upper lower binding", raw_digest))
        mechanism = coverage_row.get("upper_mechanism")
        row = {
            "descriptor_index": coverage_row["descriptor_index"],
            "raw_ledger_descriptor_sha256": raw_digest,
            "rank_bundle_descriptor_sha256": bundle_digest,
            "exact_rank": lower_rank,
            "parameter_count": coverage_row["parameter_count"],
        }
        if mechanism == "multilinear_lambda_polynomial_vector_fields":
            certificate = syzygy.upper_certificate(
                descriptor,
                atlas.output_sparse_polynomials,
                atlas.default_exact_point,
            )
            if certificate["certified_rank_upper"] != lower_rank:
                raise AssertionError(("rank-upper base gap", raw_digest))
            row.update(
                {
                    "upper_mechanism": mechanism,
                    "coefficient_system_rank": certificate[
                        "coefficient_system_rank"
                    ],
                    "stacked_system_rank": certificate[
                        "stacked_system_rank"
                    ],
                    "independent_kernel_fields": certificate[
                        "independent_kernel_fields"
                    ],
                }
            )
            mechanism_counts["base"] += 1
        elif mechanism == "base_fields_plus_primitive_log_field_port_transport":
            orbit_index = coverage_row["representative_orbit_index"]
            permutation = tuple(
                coverage_row["representative_to_member_port_permutation"]
            )
            representative_digest = representative_rows[orbit_index][
                "representative_descriptor_sha256"
            ]
            representative = regenerated[representative_digest]
            transformed = actions.port_transform_canonical_retic(
                representative, permutation
            )
            if transformed != descriptor:
                raise AssertionError(("rank-upper broken S4 transport", raw_digest))
            if representative_rows[orbit_index]["exact_rank"] != lower_rank:
                raise AssertionError(("rank-upper transport rank", raw_digest))
            row.update(
                {
                    "upper_mechanism": mechanism,
                    "representative_orbit_index": orbit_index,
                    "representative_descriptor_sha256": representative_digest,
                    "representative_to_member_port_permutation": list(permutation),
                    "representative_certificate_sha256": representative_rows[
                        orbit_index
                    ]["certificate_sha256"],
                }
            )
            mechanism_counts["transport"] += 1
        else:
            raise AssertionError(("rank-upper mechanism", mechanism))
        binding_rows.append(row)
    if mechanism_counts != {"base": 3515, "transport": 864}:
        raise AssertionError(("rank-upper mechanism census", mechanism_counts))
    return {
        "schema": "k2p-four-port-regenerated-rank-upper-binding-v1",
        "claim": "Exact upper equals regenerated exact lower for all descriptors; no frozen descriptor or rank pickle was opened.",
        "bundle": {
            "manifest_sha256": _sha_file(bundle_root / "manifest.json"),
            "aggregate_sha256": manifest["aggregate_sha256"],
            "file_count": manifest["file_count"],
            "coverage_sha256": _sha_file(
                bundle_root / "rank_upper_coverage.json"
            ),
        },
        "descriptor_count": len(binding_rows),
        "base_ansatz_descriptor_count": mechanism_counts["base"],
        "exceptional_transport_descriptor_count": mechanism_counts[
            "transport"
        ],
        "exceptional_representative_count": len(representative_rows),
        "zero_unresolved": True,
        "representatives": {
            str(index): representative_rows[index]
            for index in sorted(representative_rows)
        },
        "descriptors": binding_rows,
    }

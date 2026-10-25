#!/usr/bin/env python3
"""Derive direction-safe direct certificate templates from frozen artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ANALYSIS = Path(__file__).resolve().parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS))

from compression_common import (  # noqa: E402
    PROJECT,
    TEMPLATES,
    direct_terminal_id,
    format_quadratic,
    input_binding,
    iter_gzip_json_lines,
    literal_quadratic_body,
    load_gzip_json,
    load_json,
    project_path,
    reject_optimized_python,
    require,
    sealed,
    sha_object,
    write_json,
    write_text,
)


OUTPUT_JSON = TEMPLATES / "DIRECT_CERTIFICATE_TEMPLATE_TABLE.json"
OUTPUT_MD = TEMPLATES / "DIRECT_CERTIFICATE_TEMPLATE_TABLE.md"


RAW4_REGISTRY = (
    "work/corrected_composite_ledgers/artifacts/"
    "raw4_terminal_certificate_registry.json.gz"
)
RAW4_LEDGER = (
    "work/corrected_composite_ledgers/artifacts/"
    "raw4_corrected_composite_ledger.jsonl.gz"
)
THETA2_PARTITION = "work/theta2_five_port_closure/artifacts/class_partition.json.gz"
THETA2_DIRECT = (
    "work/theta2_five_port_closure/artifacts/direct_proof_certificates.json.gz"
)
CYCLE_QUADRATICS = "work/cycle_three_port_closure/artifacts/quadratic_certificates.json"
DIRECT36 = (
    "package/referee/k2p_offline_sweep_portable/proofs/"
    "four_port_direct_residual_closure_certificate.json"
)
QUINTIC = (
    "package/referee/k2p_offline_sweep_portable/proofs/"
    "theta0_quintic_orbit_certificate.json"
)
CUBIC = (
    "package/referee/k2p_offline_sweep_portable/proofs/"
    "theta3_cubic_obstruction_certificate.json"
)
QUARTIC = (
    "package/referee/k2p_offline_sweep_portable/proofs/"
    "theta_quartic_obstruction_certificates.json"
)
HARD = "package/referee/k2p_offline_sweep_portable/certificates/direct_hard_cases.json"
RAW4_TI = "work/adversarial_proof_review/raw4_tree_sunlet_full_map_certificate.json"
THETA2_TI = "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json"
CYCLE_TI = "work/adversarial_proof_review/cycle_tree_sunlet_full_map_certificate.json"
RANK = "work/rank_upper_certificates/rank_upper_coverage.json"
RESTORATION = (
    "work/restoration_sign_reclassification/corrected_restoration_forest.json"
)


def raw4_presentation_counts() -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in iter_gzip_json_lines(project_path(RAW4_LEDGER)):
        if row["corrected_category"] == "direct_terminal_presentation":
            evidence = row["evidence_binding"]
            require(
                evidence["kind"] == "exact_terminal_class_and_direct_certificate",
                "RAW4_TERMINAL_EVIDENCE_KIND",
            )
            counts[evidence["terminal_class_id"]] += 1
        require(
            "tree_sunlet" not in row["exact_reason"].lower(),
            "FORBIDDEN_ROOTED_REASON",
            row["raw_id"],
        )
    require(sum(counts.values()) == 1472, "RAW4_TERMINAL_PRESENTATION_COUNT")
    require(len(counts) == 934, "RAW4_TERMINAL_CLASS_COUNT")
    return counts


def group_literal_quadratics(
    records: list[dict[str, Any]],
    *,
    prefix: str,
    class_key,
    certificate_key,
    presentation_count,
    coordinate_port_count: int,
    coordinate_convention_id: str,
) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for record in records:
        certificate = certificate_key(record)
        body = literal_quadratic_body(
            certificate,
            coordinate_port_count=coordinate_port_count,
            coordinate_convention_id=coordinate_convention_id,
        )
        body_sha = sha_object(body)
        group = groups.setdefault(
            body_sha,
            {
                "body": body,
                "body_sha256": body_sha,
                "classes": [],
                "source_indices": Counter(),
                "certificate_payload_sha256": set(),
                "source_pullback_term_counts": set(),
                "raw_presentations": 0,
                "assignments": [],
            },
        )
        class_id = class_key(record)
        group["classes"].append(class_id)
        source_index = record["source_index"]
        group["source_indices"][source_index] += 1
        payload = record.get("certificate_payload_sha256")
        if payload is not None:
            group["certificate_payload_sha256"].add(payload)
        for field in ("source_nonzero_terms", "source_pullback_terms", "source_pullback_term_count"):
            value = certificate.get(field)
            if isinstance(value, int):
                group["source_pullback_term_counts"].add(value)
        group["raw_presentations"] += presentation_count(record)
        residual = {
            key: value
            for key, value in certificate.items()
            if key not in ("coefficients", "coordinate_pairs", "degree", "weight")
        }
        group["assignments"].append(
            {
                "canonical_class": class_id,
                "source_index": source_index,
                "raw_presentation_count": presentation_count(record),
                "frozen_certificate_sha256": sha_object(certificate),
                "certificate_residual": residual,
            }
        )

    result: list[dict[str, Any]] = []
    for ordinal, body_sha in enumerate(sorted(groups), 1):
        group = groups[body_sha]
        result.append(
            {
                "template_id": f"{prefix}-{ordinal:02d}",
                "normalization": "literal_exact_coordinate_body_only",
                "body": group["body"],
                "body_sha256": body_sha,
                "display_polynomial": format_quadratic(group["body"]),
                "canonical_classes": sorted(group["classes"]),
                "canonical_class_count": len(group["classes"]),
                "raw_presentation_count": group["raw_presentations"],
                "source_index_class_counts": {
                    str(key): value
                    for key, value in sorted(group["source_indices"].items())
                },
                "certificate_payload_sha256": sorted(
                    group["certificate_payload_sha256"]
                ),
                "source_pullback_term_counts": sorted(
                    group["source_pullback_term_counts"]
                ),
                "assignments": sorted(
                    group["assignments"], key=lambda row: row["canonical_class"]
                ),
            }
        )
    return result


def raw4_templates() -> dict[str, Any]:
    registry = load_gzip_json(project_path(RAW4_REGISTRY))
    rows = registry["rows"]
    require(len(rows) == registry["terminal_class_count"] == 934, "RAW4_REGISTRY_COUNT")
    presentation_counts = raw4_presentation_counts()

    class_ids: list[str] = []
    kind_counts: Counter[str] = Counter()
    kind_presentations: Counter[str] = Counter()
    quadratics: list[dict[str, Any]] = []
    family_assignments: list[dict[str, Any]] = []
    for row in rows:
        class_id = direct_terminal_id(row["source_index"], row["class_id"])
        class_ids.append(class_id)
        require(class_id in presentation_counts, "RAW4_CLASS_WITHOUT_PRESENTATION", class_id)
        terminal = row["terminal_certificate"]
        kind = terminal["kind"]
        kind_counts[kind] += 1
        kind_presentations[kind] += presentation_counts[class_id]
        family_assignments.append(
            {
                "terminal_class_id": class_id,
                "terminal_kind": kind,
                "presentation_count": presentation_counts[class_id],
                "direction": "source_to_target",
                "certificate_binding_sha256": row["certificate_binding_sha256"],
            }
        )
        if kind == "exact_multihomogeneous_quadratic":
            quadratics.append(
                {
                    **row,
                    "certificate_payload_sha256": terminal[
                        "certificate_payload_sha256"
                    ],
                    "quadratic_certificate": terminal["certificate"],
                }
            )
    require(len(set(class_ids)) == 934, "RAW4_DUPLICATE_CLASS")
    require(kind_counts["exact_multihomogeneous_quadratic"] == 839, "RAW4_Q_CLASS_COUNT")
    templates = group_literal_quadratics(
        quadratics,
        prefix="R4Q",
        class_key=lambda row: direct_terminal_id(row["source_index"], row["class_id"]),
        certificate_key=lambda row: row["quadratic_certificate"],
        presentation_count=lambda row: presentation_counts[
            direct_terminal_id(row["source_index"], row["class_id"])
        ],
        coordinate_port_count=4,
        coordinate_convention_id="k2p_four_port_fourier_flat_index_v1",
    )
    require(len(templates) == 8, "RAW4_LITERAL_QUADRATIC_COUNT", len(templates))
    require(
        sorted(template["canonical_class_count"] for template in templates)
        == [8, 12, 24, 52, 68, 131, 252, 292],
        "RAW4_LITERAL_QUADRATIC_MULTIPLICITIES",
    )

    template_by_class = {
        class_id: template["template_id"]
        for template in templates
        for class_id in template["canonical_classes"]
    }
    require(len(template_by_class) == 839, "RAW4_Q_TEMPLATE_COVERAGE")
    for assignment in family_assignments:
        assignment["literal_template_id"] = template_by_class.get(
            assignment["terminal_class_id"]
        )

    return {
        "registry_payload_sha256": registry["payload_sha256"],
        "canonical_terminal_classes": 934,
        "raw_terminal_presentations": sum(presentation_counts.values()),
        "terminal_kind_class_counts": dict(sorted(kind_counts.items())),
        "terminal_kind_presentation_counts": dict(sorted(kind_presentations.items())),
        "quadratic_literal_templates": templates,
        "quadratic_literal_template_count": len(templates),
        "quadratic_certificate_payload_count": len(
            {
                payload
                for template in templates
                for payload in template["certificate_payload_sha256"]
            }
        ),
        "family_assignments": sorted(
            family_assignments, key=lambda row: row["terminal_class_id"]
        ),
    }


def theta2_templates() -> dict[str, Any]:
    partition = load_gzip_json(project_path(THETA2_PARTITION))
    direct = load_gzip_json(project_path(THETA2_DIRECT))
    classes = partition["classes"]
    require(len(classes) == 480, "THETA2_CLASS_COUNT")
    category_classes = Counter(row["category"] for row in classes)
    category_presentations = Counter()
    class_by_key: dict[tuple[int, int], dict[str, Any]] = {}
    for row in classes:
        category_presentations[row["category"]] += row["raw_presentation_count"]
        key = (row["source_index"], row["class_id"])
        require(key not in class_by_key, "THETA2_DUPLICATE_CLASS", key)
        class_by_key[key] = row
    require(
        category_classes
        == Counter(
            {"rank_excluded": 352, "quadratic_separated": 96, "isomorphic": 32}
        ),
        "THETA2_CLASS_PARTITION_DRIFT",
    )
    require(
        category_presentations
        == Counter(
            {"rank_excluded": 800, "quadratic_separated": 240, "isomorphic": 80}
        ),
        "THETA2_PRESENTATION_PARTITION_DRIFT",
    )

    quadratics: list[dict[str, Any]] = []
    for certificate_id, certificate in direct["quadratic_certificates"].items():
        key = (certificate["source_index"], certificate["class_id"])
        row = class_by_key.get(key)
        require(
            row is not None and row["category"] == "quadratic_separated",
            "THETA2_Q_CLASS_LINK",
            key,
        )
        require(row["certificate_id"] == certificate_id, "THETA2_Q_CERTIFICATE_LINK", key)
        quadratics.append(
            {
                "source_index": certificate["source_index"],
                "class_id": certificate["class_id"],
                "certificate_id": certificate_id,
                "quadratic_certificate": certificate,
                "raw_presentation_count": row["raw_presentation_count"],
            }
        )
    require(len(quadratics) == 96, "THETA2_Q_CERTIFICATE_COUNT")
    templates = group_literal_quadratics(
        quadratics,
        prefix="T2Q",
        class_key=lambda row: (
            f"source_{row['source_index']}:class_{row['class_id']:06d}"
        ),
        certificate_key=lambda row: row["quadratic_certificate"],
        presentation_count=lambda row: row["raw_presentation_count"],
        coordinate_port_count=5,
        coordinate_convention_id="k2p_five_port_fourier_flat_index_v1",
    )
    require(len(templates) == 4, "THETA2_LITERAL_QUADRATIC_COUNT", len(templates))
    require(
        sorted(template["canonical_class_count"] for template in templates)
        == [16, 24, 24, 32],
        "THETA2_LITERAL_QUADRATIC_MULTIPLICITIES",
    )
    return {
        "canonical_classes": len(classes),
        "category_class_counts": dict(sorted(category_classes.items())),
        "category_presentation_counts": dict(sorted(category_presentations.items())),
        "quadratic_literal_templates": templates,
        "quadratic_literal_template_count": len(templates),
        "isomorphism_certificate_count": len(direct["isomorphism_certificates"]),
    }


def cycle_templates() -> dict[str, Any]:
    value = load_json(project_path(CYCLE_QUADRATICS))
    certificates = value["certificates"]
    multiplicities = value["raw_multiplicity"]
    records: list[dict[str, Any]] = []
    for certificate_id, certificate in certificates.items():
        require(certificate_id in multiplicities, "CYCLE_Q_MULTIPLICITY_MISSING")
        records.append(
            {
                "source_index": certificate.get("source_index", 0),
                "class_id": certificate_id,
                "certificate_id": certificate_id,
                "quadratic_certificate": certificate,
                "raw_presentation_count": multiplicities[certificate_id],
            }
        )
    require(len(records) == 54, "CYCLE_Q_CLASS_COUNT")
    require(sum(multiplicities.values()) == 132, "CYCLE_Q_PRESENTATION_COUNT")
    templates = group_literal_quadratics(
        records,
        prefix="C3Q",
        class_key=lambda row: row["certificate_id"],
        certificate_key=lambda row: row["quadratic_certificate"],
        presentation_count=lambda row: row["raw_presentation_count"],
        coordinate_port_count=4,
        coordinate_convention_id="k2p_cycle_restored_fourier_flat_index_v1",
    )
    require(len(templates) == 6, "CYCLE_LITERAL_QUADRATIC_COUNT", len(templates))
    require(
        sorted(template["canonical_class_count"] for template in templates)
        == [2, 2, 2, 16, 16, 16],
        "CYCLE_LITERAL_QUADRATIC_MULTIPLICITIES",
    )
    return {
        "descriptor_pair_classes": len(records),
        "raw_presentations": sum(multiplicities.values()),
        "quadratic_literal_templates": templates,
        "quadratic_literal_template_count": len(templates),
    }


def restoration_templates() -> dict[str, Any]:
    value = load_json(project_path(RESTORATION))
    quadratic_rows = [
        row
        for row in value["first_coverage"]
        if row["proof"] == "exact_multihomogeneous_quadratic"
    ]
    multiplicities = Counter(row["certificate_sha256"] for row in quadratic_rows)
    records: list[dict[str, Any]] = []
    for certificate_id, raw_presentations in sorted(multiplicities.items()):
        certificate = value["algebra_certificates"].get(certificate_id)
        require(certificate is not None, "RESTORATION_Q_CERTIFICATE_MISSING", certificate_id)
        require(certificate["proof"] == "exact_multihomogeneous_quadratic", "RESTORATION_Q_PROOF_KIND")
        records.append(
            {
                "source_index": "mixed_restoration",
                "class_id": certificate_id,
                "quadratic_certificate": certificate,
                "raw_presentation_count": raw_presentations,
            }
        )
    require(len(records) == 6, "RESTORATION_Q_CLASS_COUNT")
    require(sum(multiplicities.values()) == 148, "RESTORATION_Q_PRESENTATION_COUNT")
    templates = group_literal_quadratics(
        records,
        prefix="RSQ",
        class_key=lambda row: row["class_id"],
        certificate_key=lambda row: row["quadratic_certificate"],
        presentation_count=lambda row: row["raw_presentation_count"],
        coordinate_port_count=5,
        coordinate_convention_id="k2p_restored_five_port_fourier_flat_index_v1",
    )
    require(len(templates) == 5, "RESTORATION_LITERAL_QUADRATIC_COUNT")
    require(
        sorted(template["canonical_class_count"] for template in templates)
        == [1, 1, 1, 1, 2],
        "RESTORATION_LITERAL_QUADRATIC_MULTIPLICITIES",
    )
    return {
        "certificate_classes": len(records),
        "raw_presentations": sum(multiplicities.values()),
        "quadratic_literal_templates": templates,
        "quadratic_literal_template_count": len(templates),
    }


def direct36_templates() -> dict[str, Any]:
    overlay = load_json(project_path(DIRECT36))
    rows = overlay["coverage"]
    require(len(rows) == 36, "DIRECT36_COUNT")
    require(overlay["remaining_unproved_among_36"] == 0, "DIRECT36_UNPROVED")
    require(overlay["binding_gaps"] == [], "DIRECT36_BINDING_GAPS")
    expected_classes = {
        **{(1, class_id): "theta0_quintic_port_orbit" for class_id in (*range(25, 38), *range(39, 48))},
        **{
            (source_index, class_id): "lower_theta_quartic"
            for source_index in (2, 3)
            for class_id in range(112, 116)
        },
        **{(4, class_id): "lower_theta_quartic" for class_id in range(8, 12)},
        **{(5, class_id): "theta3_cubic" for class_id in range(9, 11)},
    }
    require(len(expected_classes) == 36, "DIRECT36_EXPECTED_CLASS_TABLE")
    observed_classes = {
        (row["source_index"], row["canonical_class_id"]): row["family"]
        for row in rows
    }
    require(len(observed_classes) == 36, "DIRECT36_DUPLICATE_CLASS")
    require(observed_classes == expected_classes, "DIRECT36_EXACT_CLASS_SET")
    require((1, 24) not in observed_classes and (1, 38) not in observed_classes, "DIRECT36_ZERO_ORBIT_ROW_PROMOTED")
    groups: dict[tuple[str, int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        require(row["target_pullback_zero"] is True, "DIRECT36_TARGET_NONZERO")
        require(row["source_pullback_term_count"] > 0, "DIRECT36_SOURCE_ZERO")
        require(row["bridge_multihomogeneous"] is True, "DIRECT36_MULTIHOMOGENEITY")
        groups[(row["family"], row["degree"], row["polynomial_sha256"])].append(row)

    literal_templates: list[dict[str, Any]] = []
    for ordinal, key in enumerate(sorted(groups), 1):
        family, degree, polynomial_sha = key
        group_rows = groups[key]
        polynomial_labels = sorted({row["polynomial"] for row in group_rows})
        require(len(polynomial_labels) == 1, "DIRECT36_BODY_LABEL_AMBIGUOUS")
        body = {
            "family": family,
            "degree": degree,
            "polynomial_sha256": polynomial_sha,
            "polynomial": polynomial_labels[0],
        }
        literal_templates.append(
            {
                "template_id": f"D36-{ordinal:02d}",
                "body": body,
                "body_sha256": sha_object(body),
                "direction": "source_to_target_only",
                "covered_records": [
                    {
                        "source_index": row["source_index"],
                        "canonical_class_id": row["canonical_class_id"],
                        "frozen_record_sha256": sha_object(row),
                        "record_residual": {
                            field: value
                            for field, value in row.items()
                            if field
                            not in ("family", "degree", "polynomial_sha256", "polynomial")
                        },
                    }
                    for row in sorted(
                        group_rows,
                        key=lambda item: (
                            item["source_index"],
                            item["canonical_class_id"],
                        ),
                    )
                ],
            }
        )
    family_counts = Counter(row["family"] for row in rows)
    require(len(literal_templates) == 27, "DIRECT36_LITERAL_TEMPLATE_COUNT")
    require(
        family_counts
        == Counter(
            {
                "theta0_quintic_port_orbit": 22,
                "lower_theta_quartic": 12,
                "theta3_cubic": 2,
            }
        ),
        "DIRECT36_FAMILY_COUNTS",
    )

    quintic = load_json(project_path(QUINTIC))
    cubic = load_json(project_path(CUBIC))
    quartic = load_json(project_path(QUARTIC))
    require(quintic["invariant_degree"] == 5, "QUINTIC_DEGREE")
    quintic_rows = {row["class_id"]: row for row in quintic["rows"]}
    require(set(quintic_rows) == set(range(24, 48)), "QUINTIC_ORBIT_CLASS_SET")
    require(
        {class_id for class_id, row in quintic_rows.items() if row["source_pullback_terms"] == 0}
        == {24, 38},
        "QUINTIC_ZERO_SOURCE_ORBIT_ROWS",
    )
    require(
        all(row["target_pullback_zero"] is True for row in quintic_rows.values()),
        "QUINTIC_TARGET_PULLBACK",
    )
    require(cubic["degree"] == 3, "CUBIC_DEGREE")
    require(len(quartic["certificates"]) == 3, "QUARTIC_BASE_COUNT")
    require(len(quartic["transports"]) == 12, "QUARTIC_TRANSPORT_COUNT")
    return {
        "mathematical_family_count": 3,
        "family_record_counts": dict(sorted(family_counts.items())),
        "directional_transported_literal_body_count": len(literal_templates),
        "historical_production_status_counts_non_authoritative": dict(
            sorted(Counter(row["production_status"] for row in rows).items())
        ),
        "literal_templates": literal_templates,
        "base_formula_count": 5,
        "base_formulas": {
            "theta0_quintic": {
                "degree": quintic["invariant_degree"],
                "multidegree": quintic["invariant_multidegree"],
                "terms": quintic["invariant"],
                "invariant_sha256": quintic["invariant_sha256"],
                "double_coset_representative_classes": quintic[
                    "double_coset_representative_classes"
                ],
                "semidirected_symmetry_generator": quintic[
                    "semidirected_symmetry_generator"
                ],
                "covered_direct_records": 22,
                "zero_port_permutations": len(quintic["zero_permutations"]),
            },
            "lower_theta_quartics": {
                "degree": 4,
                "base_certificates": quartic["certificates"],
                "certified_transports": quartic["transports"],
            },
            "theta3_cubic": {
                "degree": cubic["degree"],
                "multidegree": cubic["bridge_multidegree"],
                "normalization": cubic["normalization"],
                "terms": cubic["normalized_terms"],
                "polynomial_sha256": cubic["normalized_polynomial_sha256"],
                "covered_direct_records": len(cubic["fresh_production_record_bindings"]),
            },
        },
    }


def sign_and_rank_templates() -> dict[str, Any]:
    raw4 = load_json(project_path(RAW4_TI))
    theta2 = load_json(project_path(THETA2_TI))
    cycle = load_json(project_path(CYCLE_TI))
    restoration = load_json(project_path(RESTORATION))
    rank = load_json(project_path(RANK))
    mechanisms = Counter(row["upper_mechanism"] for row in rank["descriptors"])
    require(
        mechanisms
        == Counter(
            {
                "multilinear_lambda_polynomial_vector_fields": 3515,
                "base_fields_plus_primitive_log_field_port_transport": 864,
            }
        ),
        "RANK_MECHANISM_COUNTS",
    )
    restoration_ti_rows = [
        row
        for layer in (restoration["first_coverage"], restoration["second_coverage"])
        for row in layer
        if row["proof"] == "full_map_Ti_zero_strict_sign"
    ]
    restoration_orientation = Counter(
        (
            row["certificate"]["zero_side"],
            row["certificate"]["signed_side"],
            row["certificate"]["orientation"],
        )
        for row in restoration_ti_rows
    )
    expected_restoration_orientation = Counter(
        {
            ("target", "source", 1): 248,
            ("source", "target", 0): 240,
            ("target", "source", 2): 70,
            ("source", "target", 2): 56,
        }
    )
    require(
        restoration_orientation == expected_restoration_orientation,
        "RESTORATION_TI_ORIENTATION_CENSUS",
    )
    require(raw4["full_map_strict_source_sign_rows"] == raw4["claimed_rows"], "RAW4_TI_SIGN_SIDE")
    require(raw4["full_map_target_zero_rows"] == raw4["claimed_rows"], "RAW4_TI_ZERO_SIDE")
    require(theta2["full_map_source_zero_rows"] == theta2["claimed_rows"], "THETA2_TI_ZERO_SIDE")
    require(theta2["full_map_strict_target_sign_rows"] == theta2["claimed_rows"], "THETA2_TI_SIGN_SIDE")
    return {
        "full_map_Ti": {
            "universal_observable_identity": "T_i=V^2 X_g-X_s^2 Y_g Z_g",
            "normalization_boundary": (
                "Polynomial relation classes are retained per frozen full-map "
                "registry; they are not quotiented by rooted restrictions."
            ),
            "raw4": {
                "rows": raw4["claimed_rows"],
                "polynomial_relation_classes": raw4[
                    "canonical_polynomial_relation_classes"
                ],
                "zero_side": "target",
                "signed_side": "source",
                "chosen_orientation_by_source_triple": raw4[
                    "chosen_orientation_by_source_triple"
                ],
                "ordered_truth_row_hash_root": raw4[
                    "ordered_truth_row_hash_root"
                ],
            },
            "theta2": {
                "rows": theta2["claimed_rows"],
                "polynomial_relation_classes": theta2[
                    "canonical_polynomial_relation_classes"
                ],
                "zero_side": "source",
                "signed_side": "target",
                "ordered_truth_row_hash_root": theta2[
                    "ordered_truth_row_hash_root"
                ],
            },
            "cycle": {
                "rows": sum(family["input_rows"] for family in cycle["families"].values()),
                "polynomial_relation_classes": len(cycle["sign_certificates"]),
                "orientation_contract": "retained_per_sign_certificate_presentation",
            },
            "restoration": {
                "rows": len(restoration_ti_rows),
                "orientation_counts": [
                    {
                        "zero_side": zero_side,
                        "signed_side": signed_side,
                        "orientation": orientation,
                        "rows": count,
                    }
                    for (zero_side, signed_side, orientation), count in sorted(
                        restoration_orientation.items()
                    )
                ],
                "orientation_contract": (
                    "Every assignment retains zero_side, signed_side, orientation, "
                    "triple, source/target pullback hashes, and strict-sign binding "
                    "in the frozen forest."
                ),
            },
        },
        "rank_upper": {
            "descriptor_count": rank["descriptor_count"],
            "mechanism_counts": dict(sorted(mechanisms.items())),
            "exceptional_representatives": rank["exceptional_representative_count"],
            "compression_boundary": (
                "Two mechanisms are certified. The 75 exceptional representatives "
                "remain explicit finite evidence and are not collapsed to coarse rank cells."
            ),
        },
    }


def hard_cases() -> dict[str, Any]:
    value = load_json(project_path(HARD))
    require(len(value["cases"]) == 4, "HARD_CASE_COUNT")
    return {
        "case_count": len(value["cases"]),
        "source_identities": value["source_identities"],
        "logical_conclusion": value["logical_conclusion"],
        "cases": value["cases"],
        "direction": "source_to_target_only",
    }


def template_payload() -> dict[str, Any]:
    return {
        "schema": "k2p-direct-certificate-template-table-v1",
        "status": "PASS",
        "scope": (
            "Direction-safe literal and certified-orbit compression of frozen raw4, "
            "theta2, cycle, and direct-36 certificates on D_plus."
        ),
        "normalization_policy": {
            "used": [
                "exact literal coefficient equality",
                "exact literal coordinate-pair equality",
                "exact multidegree equality",
                "explicitly frozen orbit transports in the quintic/quartic/cubic packages",
            ],
            "forbidden": [
                "source_target_reversal",
                "ordinary_triangle_redirection_as_polynomial_symmetry",
                "rooted_tree_sunlet_signature",
                "uncertified_inheritance_complement",
                "uncertified_pole_or_sink_exchange",
                "C_T_exchange_without_an_explicit_bound_transport",
            ],
            "direction_contract": (
                "Every separator remains source-to-target: target pullback is "
                "identically zero and source pullback is nonzero or strict-sign."
            ),
        },
        "raw4": raw4_templates(),
        "theta2": theta2_templates(),
        "cycle": cycle_templates(),
        "restoration": restoration_templates(),
        "direct36": direct36_templates(),
        "hard_F2_F3_F4": hard_cases(),
        "structural_templates": sign_and_rank_templates(),
        "input_bindings": [
            input_binding(relative)
            for relative in (
                RAW4_REGISTRY,
                RAW4_LEDGER,
                THETA2_PARTITION,
                THETA2_DIRECT,
                CYCLE_QUADRATICS,
                DIRECT36,
                QUINTIC,
                CUBIC,
                QUARTIC,
                HARD,
                RAW4_TI,
                THETA2_TI,
                CYCLE_TI,
                RANK,
                RESTORATION,
            )
        ],
    }


def template_rows(label: str, templates: list[dict[str, Any]]) -> str:
    rows = []
    for template in templates:
        rows.append(
            f"| {template['template_id']} | `{template['display_polynomial']}` | "
            f"`{template['body']['weight']}` | {template['canonical_class_count']} | "
            f"{template['raw_presentation_count']} |"
        )
    return (
        f"### {label}\n\n"
        "| Template | Literal polynomial | Weight | Canonical classes | Raw presentations |\n"
        "|---|---|---|---:|---:|\n"
        + "\n".join(rows)
    )


def markdown(value: dict[str, Any]) -> str:
    raw4 = value["raw4"]
    theta2 = value["theta2"]
    cycle = value["cycle"]
    restoration = value["restoration"]
    direct36 = value["direct36"]
    structural = value["structural_templates"]
    return f"""# Direct certificate template table

Status: **PASS**.  Templates are grouped only by literal exact coordinate
bodies or by transports already certified in a frozen orbit package.  No
source-target reversal, triangle quotient, rooted tree/sunlet oracle, or
uncertified inheritance/core symmetry is used.

## Exact census

| Layer | Canonical certificate classes | Literal bodies/templates |
|---|---:|---:|
| Four-port quadratics | 839 | {raw4['quadratic_literal_template_count']} |
| Theta2 quadratics | 96 | {theta2['quadratic_literal_template_count']} |
| Cycle quadratics | {cycle['descriptor_pair_classes']} | {cycle['quadratic_literal_template_count']} |
| Restoration quadratics | {restoration['certificate_classes']} | {restoration['quadratic_literal_template_count']} |
| Direct-36 high-degree records | 36 | {direct36['directional_transported_literal_body_count']} direction-specific bodies in {direct36['mathematical_family_count']} certified families |

The direct-36 families have five stored base formulas: one quintic, three
quartics, and one cubic.  The single quintic orbit proposition has 22
direction-specific transported bodies; the quartic family has 12 records and
four transported bodies; the cubic has two records and one body.  Thus “three
families” must not be reported as “three literal polynomials.”

## Literal quadratic bodies

{template_rows('Four-port', raw4['quadratic_literal_templates'])}

{template_rows('Theta2', theta2['quadratic_literal_templates'])}

{template_rows('Three-port cycle', cycle['quadratic_literal_templates'])}

{template_rows('Restoration', restoration['quadratic_literal_templates'])}

Coordinates are those of each frozen registry.  Equality across different
coordinate conventions is deliberately not inferred.

## Other direct families

The 934 four-port terminal classes partition exactly as

```text
{json.dumps(raw4['terminal_kind_class_counts'], sort_keys=True)}
```

The four hard classes retain the coupled `F2/F3/F4` argument.  Labelled mixed-
graph isomorphisms and ordinary-triangle terminals remain distinct graph
families; triangle redirection is not used to transport a separator.

Full-map `T_i` compression retains {structural['full_map_Ti']['raw4']['polynomial_relation_classes']}
four-port, {structural['full_map_Ti']['theta2']['polynomial_relation_classes']}
theta2, and {structural['full_map_Ti']['cycle']['polynomial_relation_classes']}
cycle polynomial-relation classes under the one universal observable identity.
Its direction bit is not normalized: raw4 is source-sign/target-zero, theta2
is source-zero/target-sign, and the {structural['full_map_Ti']['restoration']['rows']}
restoration leaves retain their mixed zero/sign side and orientation per row.
Rank compression retains the two certified mechanisms and all
{structural['rank_upper']['exceptional_representatives']} exceptional orbit
representatives.

Payload SHA-256: `{value['payload_sha256']}`.
"""


def main() -> None:
    reject_optimized_python()
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    arguments = parser.parse_args()

    value = sealed(template_payload())
    rendered_markdown = markdown(value)
    outputs = (
        (
            OUTPUT_JSON,
            (
                json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False)
                + "\n"
            ).encode("utf-8"),
        ),
        (OUTPUT_MD, (rendered_markdown.rstrip() + "\n").encode("utf-8")),
    )
    if arguments.write:
        write_json(OUTPUT_JSON, value)
        write_text(OUTPUT_MD, rendered_markdown)
    else:
        for path, expected in outputs:
            require(path.is_file(), "DERIVED_OUTPUT_MISSING", path)
            require(path.read_bytes() == expected, "DERIVED_OUTPUT_DRIFT", path)
    print(
        json.dumps(
            {
                "status": "PASS",
                "payload_sha256": value["payload_sha256"],
                "output": str(OUTPUT_JSON.relative_to(PROJECT)),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

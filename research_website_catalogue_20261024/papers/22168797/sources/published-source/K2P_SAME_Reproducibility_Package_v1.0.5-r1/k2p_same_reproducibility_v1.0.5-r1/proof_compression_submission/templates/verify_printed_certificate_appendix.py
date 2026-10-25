#!/usr/bin/env python3
"""Independent replay of the reader-facing printed certificate appendix."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
SUBMISSION = HERE.parent
PROJECT = SUBMISSION.parent
STRICT_JSON_DIR = PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    decode_json_document,
    iter_canonical_gzip_jsonl,
    load_canonical_gzip_json,
)

DEFAULT_APPENDIX = HERE / "PRINTED_CERTIFICATE_APPENDIX.json"
DEFAULT_TEX = SUBMISSION / "supplement" / "certificate_appendix.tex"
DIRECT_TABLE = HERE / "DIRECT_CERTIFICATE_TEMPLATE_TABLE.json"
RAW4_REGISTRY = PROJECT / "work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz"
PROOFS = PROJECT / "package/referee/k2p_offline_sweep_portable/proofs"
QUINTIC = PROOFS / "theta0_quintic_orbit_certificate.json"
QUARTIC = PROOFS / "theta_quartic_obstruction_certificates.json"
CUBIC = PROOFS / "theta3_cubic_obstruction_certificate.json"
DIRECT36 = PROOFS / "four_port_direct_residual_closure_certificate.json"
RESTORATION = PROJECT / "work/restoration_sign_reclassification/corrected_restoration_forest.json"
PROBE_CERTIFICATE = PROJECT / "work/probe_coherence_corrected/probe_coherence_certificate.json"
ONE_PORT = PROJECT / "work/probe_coherence_corrected/one_port_ledger.jsonl.gz"
TWO_PORT = PROJECT / "work/probe_coherence_corrected/two_port_ledger.jsonl.gz"
RESTRICTIONS = PROJECT / "work/probe_coherence_corrected/parent_restriction_ledger.jsonl.gz"
TRANSPORTS = PROJECT / "work/probe_coherence_corrected/exact_transport_ledger.jsonl.gz"

ROOT_ID = "s1:c658:t2792:p1032"
ANCHOR_ID = "tree:k3:identity"
CHARACTERS = ("0", "C", "G", "T")


class ReplayFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: Any | None = None) -> None:
    if not condition:
        suffix = "" if detail is None else f":{detail}"
        raise ReplayFailure(code + suffix)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), "JSON_MISSING", path)
    try:
        return decode_json_document(
            path.read_bytes(), label=str(path), require_object=True
        )
    except (OSError, StrictJSONError) as error:
        raise ReplayFailure(f"JSON_STRICT_DECODE_FAIL:{path}:{error}") from error


def load_gzip_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), "GZIP_JSON_MISSING", path)
    try:
        value = load_canonical_gzip_json(path, label=str(path))
    except (OSError, StrictJSONError) as error:
        raise ReplayFailure(f"GZIP_JSON_STRICT_DECODE_FAIL:{path}:{error}") from error
    require(isinstance(value, dict), "GZIP_JSON_NOT_OBJECT", path)
    return value


def iter_gzip_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    require(path.is_file(), "JSONL_MISSING", path)
    try:
        for line_number, row in enumerate(
            iter_canonical_gzip_jsonl(path, label=str(path)), 1
        ):
            require(isinstance(row, dict), "JSONL_ROW_NOT_OBJECT", line_number)
            yield row
    except (OSError, StrictJSONError) as error:
        raise ReplayFailure(f"JSONL_STRICT_DECODE_FAIL:{path}:{error}") from error


def verify_seal(value: dict[str, Any], code: str) -> None:
    digest = value.get("payload_sha256")
    require(isinstance(digest, str) and len(digest) == 64, f"{code}_SEAL_MISSING")
    payload = dict(value)
    payload.pop("payload_sha256")
    require(digest == sha_object(payload), f"{code}_SEAL_MISMATCH")


def polynomial(terms: list[dict[str, Any]]) -> str:
    pieces = []
    for ordinal, term in enumerate(terms):
        coefficient = term["coefficient"]
        require(isinstance(coefficient, int) and coefficient != 0, "POLYNOMIAL_COEFFICIENT")
        indices = term["indices"]
        require(isinstance(indices, list) and indices, "POLYNOMIAL_INDICES")
        monomial = "".join(f"q_{{{index}}}" for index in indices)
        magnitude = "" if abs(coefficient) == 1 else str(abs(coefficient))
        sign = ("-" if coefficient < 0 else "") if ordinal == 0 else ("+" if coefficient > 0 else "-")
        pieces.append(sign + magnitude + monomial)
    return "".join(pieces)


def normalize_terms(terms: list, reversed_order: bool) -> list[dict[str, Any]]:
    rows = []
    for term in terms:
        if reversed_order:
            indices, coefficient = term
        else:
            coefficient, indices = term
        rows.append({"coefficient": coefficient, "indices": indices})
    return rows


def ct_rep(values: tuple[int, ...]) -> tuple[int, ...]:
    swapped = tuple(3 if value == 1 else 1 if value == 3 else value for value in values)
    return min(values, swapped)


def orbit(port_count: int) -> tuple[tuple[int, ...], ...]:
    rows = set()
    for prefix in itertools.product(range(4), repeat=port_count - 1):
        last = 0
        for value in prefix:
            last ^= value
        rows.add(ct_rep(prefix + (last,)))
    return tuple(sorted(rows))


def expected_quadratics(direct: dict[str, Any]) -> list[dict[str, Any]]:
    layers = (
        ("four-port", "raw4", 8),
        ("five-port theta2", "theta2", 4),
        ("three-port cycle in four-port coordinates", "cycle", 6),
        ("five-port restoration", "restoration", 5),
    )
    result = []
    for layer, key, count in layers:
        source = direct[key]["quadratic_literal_templates"]
        require(len(source) == count, "FROZEN_QUADRATIC_COUNT", key)
        for row in source:
            body = row["body"]
            terms = [
                {"coefficient": coefficient, "indices": pair}
                for coefficient, pair in zip(
                    body["coefficients"], body["coordinate_pairs"], strict=True
                )
                if coefficient
            ]
            result.append(
                {
                    "template_id": row["template_id"],
                    "layer": layer,
                    "coordinate_convention_id": body["coordinate_convention_id"],
                    "degree": body["degree"],
                    "multidegree": body["weight"],
                    "terms": terms,
                    "stored_coordinate_indices": sorted(
                        {index for pair in body["coordinate_pairs"] for index in pair}
                    ),
                    "display_tex": polynomial(terms),
                    "canonical_class_count": row["canonical_class_count"],
                    "raw_presentation_count": row["raw_presentation_count"],
                    "literal_body_sha256": row["body_sha256"],
                }
            )
    return result


def verify_quadratics(value: dict[str, Any], direct: dict[str, Any]) -> None:
    observed = value["quadratic_templates"]
    expected = expected_quadratics(direct)
    require(observed == expected, "QUADRATIC_TABLE_MISMATCH")
    require(value["quadratic_template_count"] == len(observed) == 23, "QUADRATIC_COUNT")
    require(len({row["template_id"] for row in observed}) == 23, "QUADRATIC_DUPLICATE_ID")
    require(sum(row["canonical_class_count"] for row in observed) == 995, "QUADRATIC_CANONICAL_TOTAL")
    require(sum(row["raw_presentation_count"] for row in observed) == 1872, "QUADRATIC_RAW_TOTAL")
    contract = value["quadratic_transport_contract"].lower()
    require("literal" in contract and "does not license" in contract, "QUADRATIC_CONTRACT_WEAK")


def expected_high_degree() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    quintic = load_json(QUINTIC)
    quartic = load_json(QUARTIC)
    cubic = load_json(CUBIC)
    bases = []
    terms = normalize_terms(quintic["invariant"], True)
    bases.append(
        {
            "base_id": "HDQ-01",
            "family": "theta0 quintic",
            "degree": quintic["invariant_degree"],
            "multidegree": quintic["invariant_multidegree"],
            "terms": terms,
            "display_tex": polynomial(terms),
            "formula_sha256": quintic["invariant_sha256"],
        }
    )
    quartic_ids = {}
    for offset, row in enumerate(quartic["certificates"], 2):
        base_id = f"HDQ-{offset:02d}"
        quartic_ids[(row["source_index"], row["canonical_class_id"])] = base_id
        terms = normalize_terms(row["terms"], False)
        bases.append(
            {
                "base_id": base_id,
                "family": "lower-theta quartic",
                "source_index": row["source_index"],
                "canonical_class_id": row["canonical_class_id"],
                "degree": row["degree"],
                "multidegree": row["port_weight"],
                "terms": terms,
                "display_tex": polynomial(terms),
                "formula_sha256": sha_object(row["terms"]),
                "descriptor_sha256": row["descriptor_sha256"],
            }
        )
    terms = normalize_terms(cubic["normalized_terms"], False)
    bases.append(
        {
            "base_id": "HDQ-05",
            "family": "theta3 cubic",
            "degree": cubic["degree"],
            "multidegree": cubic["bridge_multidegree"],
            "terms": terms,
            "display_tex": polynomial(terms),
            "formula_sha256": cubic["normalized_polynomial_sha256"],
        }
    )
    q_transports = [
        {
            "base_id": "HDQ-01",
            "source_index": 1,
            "canonical_class_id": row["class_id"],
            "port_permutation": row["permutation"],
            "source_pullback_term_count": row["source_pullback_terms"],
            "source_pullback_sha256": row["source_pullback_sha256"],
        }
        for row in quintic["rows"]
        if row["source_pullback_terms"]
    ]
    r_transports = []
    for row in quartic["transports"]:
        prefix, suffix = row["base_certificate"].split("-class", 1)
        base_key = (int(prefix.removeprefix("source")), int(suffix))
        r_transports.append(
            {
                "base_id": quartic_ids[base_key],
                "source_index": row["source_index"],
                "canonical_class_id": row["canonical_class_id"],
                "coordinate_permutation": row["coordinate_permutation"],
                "port_match": row["port_match"],
                "multidegree": row["port_weight"],
                "descriptor_sha256": row["descriptor_sha256"],
                "source_pullback_sha256": row["source_pullback_sha256"],
            }
        )
    c_transports = [
        {
            "base_id": "HDQ-05",
            "source_index": row["source_index"],
            "canonical_class_id": row["canonical_class_id"],
            "port_match": row["port_match"],
            "semantic_record_sha256": row["semantic_record_sha256"],
            "record_file_sha256": row["record_file_sha256"],
        }
        for row in cubic["fresh_production_record_bindings"]
    ]
    return bases, {
        "theta0_quintic": q_transports,
        "lower_theta_quartic": r_transports,
        "theta3_cubic": c_transports,
    }


def verify_high_degree(value: dict[str, Any]) -> None:
    expected_bases, expected_transports = expected_high_degree()
    require(value["high_degree_bases"] == expected_bases, "HIGH_DEGREE_BASE_MISMATCH")
    require(value["high_degree_base_count"] == 5, "HIGH_DEGREE_BASE_COUNT")
    observed = value["certified_high_degree_transports"]
    for key, rows in expected_transports.items():
        require(observed[key] == rows, "HIGH_DEGREE_TRANSPORT_MISMATCH", key)
    require(
        [len(observed[key]) for key in expected_transports] == [22, 12, 2],
        "HIGH_DEGREE_TRANSPORT_COUNTS",
    )
    expected_classes = {
        (row["source_index"], row["canonical_class_id"])
        for rows in expected_transports.values()
        for row in rows
    }
    direct36 = load_json(DIRECT36)
    frozen_classes = {
        (row["source_index"], row["canonical_class_id"])
        for row in direct36["coverage"]
    }
    require(expected_classes == frozen_classes and len(frozen_classes) == 36, "DIRECT36_CLASS_BINDING")
    require(observed["covered_directional_records"] == 36, "DIRECT36_PRINTED_COUNT")
    contract = observed["contract"].lower()
    require("only" in contract and "no other" in contract, "HIGH_TRANSPORT_CONTRACT_WEAK")


def verify_coordinates(value: dict[str, Any]) -> None:
    dictionaries = value["coordinate_dictionaries"]
    four = orbit(4)
    five = orbit(5)
    expected_four = [
        {
            "index": index,
            "integer_tuple": list(four[index]),
            "character_tuple": "".join(CHARACTERS[item] for item in four[index]),
        }
        for index in range(36)
    ]
    five_indices = sorted(
        {
            index
            for row in value["quadratic_templates"]
            if row["coordinate_convention_id"] in {
                "k2p_five_port_fourier_flat_index_v1",
                "k2p_restored_five_port_fourier_flat_index_v1",
            }
            for index in row["stored_coordinate_indices"]
        }
    )
    expected_five = [
        {
            "index": index,
            "integer_tuple": list(five[index]),
            "character_tuple": "".join(CHARACTERS[item] for item in five[index]),
        }
        for index in five_indices
    ]
    require(dictionaries["four_port"] == expected_four, "FOUR_COORDINATE_DICTIONARY")
    require(len(expected_four) == 36, "FOUR_COORDINATE_COUNT")
    require(dictionaries["five_port_displayed"] == expected_five, "FIVE_COORDINATE_DICTIONARY")
    require(len(expected_five) == 52, "FIVE_COORDINATE_COUNT")


def compact_restoration(row: dict[str, Any], layer: int) -> dict[str, Any]:
    evidence = row.get("certificate_sha256") or sha_object(row["certificate"])
    if layer == 1:
        return {
            "layer": 1,
            "ordinal": row["ordinal"],
            "restored_label": row["restored_label"],
            "restored_role": row["restored_role"],
            "source_insertion_index": row["source_insertion_index"],
            "remaining_roles": row["remaining_roles"],
            "proof": row["proof"],
            "status": row["status"],
            "evidence_sha256": evidence,
            "row_sha256": row["row_sha256"],
        }
    return {
        "layer": 2,
        "parent_first_coverage_index": row["parent_first_coverage_index"],
        "second_restored_label": row["second_restored_label"],
        "second_restored_role": row["second_restored_role"],
        "second_source_insertion_index": row["second_source_insertion_index"],
        "remaining_roles": row["remaining_roles"],
        "proof": row["proof"],
        "status": row["status"],
        "evidence_sha256": evidence,
        "row_sha256": row["row_sha256"],
    }


def verify_restoration_example(value: dict[str, Any]) -> None:
    example = value["worked_examples"]["restoration_root_s1_c658_t2792_p1032"]
    forest = load_json(RESTORATION)
    first_source = [row for row in forest["first_coverage"] if row["root_id"] == ROOT_ID]
    second_source = [row for row in forest["second_coverage"] if row["root_id"] == ROOT_ID]
    expected_first = [compact_restoration(row, 1) for row in first_source]
    expected_second = [compact_restoration(row, 2) for row in second_source]
    require(example["root_id"] == ROOT_ID, "RESTORATION_ROOT_ID")
    require(example["first_children"] == expected_first and len(expected_first) == 14, "RESTORATION_FIRST_ROWS")
    require(example["second_children"] == expected_second and len(expected_second) == 8, "RESTORATION_SECOND_ROWS")
    require(
        example["first_proof_census"] == dict(sorted(Counter(row["proof"] for row in expected_first).items())),
        "RESTORATION_FIRST_CENSUS",
    )
    require(
        example["second_proof_census"] == dict(sorted(Counter(row["proof"] for row in expected_second).items())),
        "RESTORATION_SECOND_CENSUS",
    )
    continuation = [row for row in expected_first if row["status"] == "continuation"]
    require(len(continuation) == 1, "RESTORATION_CONTINUATION")
    parent = continuation[0]["ordinal"]
    require(all(row["parent_first_coverage_index"] == parent for row in expected_second), "RESTORATION_PARENT")
    require(all(row["status"] == "separated" and row["remaining_roles"] == [] for row in expected_second), "RESTORATION_TERMINATION")
    termination = example["termination"]
    require(
        (termination["continuation_count"], termination["continuation_ordinal"])
        == (1, parent),
        "RESTORATION_TERMINATION_DESCRIPTOR",
    )
    require(
        (termination["terminal_leaf_count"], termination["maximum_depth"], termination["unresolved"], termination["cycles"])
        == (21, 2, 0, 0),
        "RESTORATION_TERMINATION_CENSUS",
    )


def verify_direct_example(value: dict[str, Any], direct: dict[str, Any]) -> None:
    example = value["worked_examples"]["direct_quadratic_R4Q_03"]
    template = next(row for row in direct["raw4"]["quadratic_literal_templates"] if row["template_id"] == "R4Q-03")
    assignment = template["assignments"][0]
    registry = load_gzip_json(RAW4_REGISTRY)
    registry_row = next(row for row in registry["rows"] if row["class_identifier"] == assignment["canonical_class"])
    expected = {
        "template_id": "R4Q-03",
        "formula": template["display_polynomial"],
        "multidegree": template["body"]["weight"],
        "canonical_class_count": template["canonical_class_count"],
        "raw_presentation_count": template["raw_presentation_count"],
        "representative_class": assignment["canonical_class"],
        "representative_raw_presentation_count": assignment["raw_presentation_count"],
        "source_pullback_term_count": assignment["certificate_residual"]["source_nonzero_terms"],
        "certificate_sha256": assignment["frozen_certificate_sha256"],
        "certificate_binding_sha256": registry_row["certificate_binding_sha256"],
        "direction": "source pullback nonzero; target pullback identically zero",
        "conclusion": "This representative certifies source-to-target noncontainment.",
    }
    require(example == expected, "DIRECT_EXAMPLE_MISMATCH")


def rows_for(path: Path, key: str) -> list[dict[str, Any]]:
    return [row for row in iter_gzip_jsonl(path) if row.get(key) == ANCHOR_ID]


def ledger_ids(path: Path, requested: set[str]) -> set[str]:
    return {
        row["record_id"]
        for row in iter_gzip_jsonl(path)
        if row.get("record_id") in requested
    }


def verify_probe_example(value: dict[str, Any]) -> None:
    example = value["worked_examples"]["probe_tree_k3_identity"]
    certificate = load_json(PROBE_CERTIFICATE)
    anchor = next(row for row in certificate["anchor_inventory"]["public_anchors"] if row["anchor_id"] == ANCHOR_ID)
    one_rows = rows_for(ONE_PORT, "parent_anchor_id")
    two_rows = rows_for(TWO_PORT, "base_anchor_id")
    one = next(row for row in one_rows if row["status"] == "isomorphic" and row["source_site_index"] == row["target_site_index"] == 0)
    parent_id = f"P1:{ANCHOR_ID}:0:0"
    two = next(
        row for row in two_rows
        if row["status"] == "isomorphic"
        and row["one_port_parent_id"] == parent_id
        and row["second_source_site_index"] == row["second_target_site_index"] == 0
    )
    expected_anchor = {
        key: anchor[key]
        for key in (
            "anchor_id", "canonical_anchor_class_id", "origin", "relation",
            "labels", "source_graph_sha256", "target_graph_sha256", "transport_id",
        )
    }
    require(example["anchor"] == expected_anchor, "PROBE_ANCHOR")
    require(
        example["anchor_row_census"] == {
            "one_port": dict(sorted(Counter(row["status"] for row in one_rows).items())),
            "two_port": dict(sorted(Counter(row["status"] for row in two_rows).items())),
        },
        "PROBE_CENSUS",
    )
    one_fields = (
        "inserted_label", "source_site_id", "source_site_index", "target_site_id",
        "target_site_index", "source_parent_restriction_id",
        "target_parent_restriction_id", "parent_transport_id", "transport_id",
        "transport_restriction", "status",
    )
    expected_one = {key: one[key] for key in one_fields}
    expected_one["ledger_row_sha256"] = sha_object(one)
    two_fields = (
        "first_label", "second_label", "one_port_parent_id",
        "first_source_site_index", "first_target_site_index", "second_source_site_id",
        "second_source_site_index", "second_target_site_id", "second_target_site_index",
        "source_parent_restriction_id", "target_parent_restriction_id",
        "parent_transport_id", "transport_id", "transport_restriction", "status",
        "reverse_order_certificate",
    )
    expected_two = {key: two[key] for key in two_fields}
    expected_two["ledger_row_sha256"] = sha_object(two)
    require(example["selected_one_port_transport"] == expected_one, "PROBE_ONE_ROW")
    require(example["selected_two_port_transport"] == expected_two, "PROBE_TWO_ROW")
    require(two["parent_transport_id"] == one["transport_id"], "PROBE_PARENT_COHERENCE")
    transport_ids = {
        anchor["transport_id"], one["transport_id"], two["transport_id"],
        two["reverse_order_certificate"]["reverse_parent_transport_id"],
    }
    restriction_ids = {
        one["source_parent_restriction_id"], one["target_parent_restriction_id"],
        two["source_parent_restriction_id"], two["target_parent_restriction_id"],
    }
    require(ledger_ids(TRANSPORTS, transport_ids) == transport_ids, "PROBE_TRANSPORT_LEDGER")
    require(ledger_ids(RESTRICTIONS, restriction_ids) == restriction_ids, "PROBE_RESTRICTION_LEDGER")


def verify_bindings(value: dict[str, Any]) -> None:
    rows = value["input_bindings"]
    require(len(rows) == 12, "INPUT_BINDING_COUNT")
    require(len({row["path"] for row in rows}) == len(rows), "INPUT_BINDING_DUPLICATE")
    for row in rows:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts, "INPUT_PATH_ESCAPE")
        path = PROJECT / relative
        require(path.is_file(), "BOUND_INPUT_MISSING", relative)
        require(row["bytes"] == path.stat().st_size, "BOUND_INPUT_SIZE", relative)
        require(row["sha256"] == sha_file(path), "BOUND_INPUT_HASH", relative)


def verify_tex(value: dict[str, Any], tex_path: Path) -> None:
    require(tex_path.is_file(), "TEX_MISSING")
    tex = tex_path.read_text(encoding="utf-8")
    required = {
        value["schema"],
        value["payload_sha256"],
        value["producer_command"],
        value["check_command"],
        value["independent_replay_command"],
        value["mutation_command"],
        ROOT_ID,
        ANCHOR_ID,
    }
    required.update(row["template_id"] for row in value["quadratic_templates"])
    required.update(row["base_id"] for row in value["high_degree_bases"])
    required.update(row["sha256"] for row in value["input_bindings"])
    required.update(row["character_tuple"] for row in value["coordinate_dictionaries"]["four_port"])
    required.update(row["character_tuple"] for row in value["coordinate_dictionaries"]["five_port_displayed"])
    missing = sorted(token for token in required if token not in tex)
    require(not missing, "TEX_REQUIRED_TOKEN_MISSING", missing[:3])
    for row in value["quadratic_templates"]:
        for term in row["terms"]:
            monomial = "".join(f"q_{{{index}}}" for index in term["indices"])
            require(monomial in tex, "TEX_QUADRATIC_MONOMIAL_MISSING", row["template_id"])
    transports = value["certified_high_degree_transports"]
    for row in transports["theta0_quintic"]:
        exact_row = (
            f"{row['canonical_class_id']} & "
            f"$({','.join(map(str, row['port_permutation']))})$ & "
            f"{row['source_pullback_term_count']}\\\\"
        )
        require(tex.count(exact_row) == 1, "TEX_QUINTIC_TRANSPORT_ROW_CENSUS", row["canonical_class_id"])
    for row in transports["lower_theta_quartic"]:
        coordinate_action = row["coordinate_permutation"].replace("_", r"\_")
        exact_row = (
            f"{row['source_index']} & {row['canonical_class_id']} & {row['base_id']} & "
            f"{coordinate_action} & $({','.join(map(str, row['port_match']))})$\\\\"
        )
        require(
            tex.count(exact_row) == 1,
            "TEX_QUARTIC_TRANSPORT_ROW_CENSUS",
            f"{row['source_index']}:{row['canonical_class_id']}",
        )
    for row in transports["theta3_cubic"]:
        exact_row = (
            f"{row['source_index']} & {row['canonical_class_id']} & {row['base_id']} & "
            f"$({','.join(map(str, row['port_match']))})$\\\\"
        )
        require(
            tex.count(exact_row) == 1,
            "TEX_CUBIC_TRANSPORT_ROW_CENSUS",
            f"{row['source_index']}:{row['canonical_class_id']}",
        )
    require("does not license any graph, port, direction, or coordinate transport" in tex, "TEX_LITERAL_WARNING")
    require("No other port, source-target, inheritance, pole/sink, or C/T transport is inferred" in tex, "TEX_HIGH_WARNING")


def verify(appendix_path: Path, tex_path: Path) -> dict[str, Any]:
    require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")
    value = load_json(appendix_path)
    verify_seal(value, "APPENDIX")
    require(value.get("schema") == "k2p-printed-certificate-appendix-v1", "SCHEMA")
    require(value.get("status") == "PASS", "STATUS")
    direct = load_json(DIRECT_TABLE)
    verify_seal(direct, "DIRECT_TABLE")
    verify_bindings(value)
    verify_quadratics(value, direct)
    verify_high_degree(value)
    verify_coordinates(value)
    verify_direct_example(value, direct)
    verify_restoration_example(value)
    verify_probe_example(value)
    verify_tex(value, tex_path)
    return {
        "status": "PASS",
        "payload_sha256": value["payload_sha256"],
        "quadratic_templates": 23,
        "high_degree_bases": 5,
        "certified_high_degree_transports": 36,
        "four_port_coordinates": 36,
        "five_port_coordinates": 52,
        "worked_examples": 3,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--appendix", type=Path, default=DEFAULT_APPENDIX)
    parser.add_argument("--tex", type=Path, default=DEFAULT_TEX)
    arguments = parser.parse_args()
    print(json.dumps(verify(arguments.appendix, arguments.tex), sort_keys=True))


if __name__ == "__main__":
    main()

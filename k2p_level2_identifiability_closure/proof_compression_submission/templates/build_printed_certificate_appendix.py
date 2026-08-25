#!/usr/bin/env python3
"""Build the compact, reader-facing exact-certificate appendix.

This is a derived presentation layer.  It never edits the frozen theorem
certificates from which its formulas, counts, transports, and examples are
read.
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
SUBMISSION = HERE.parent
PROJECT = SUBMISSION.parent
ANALYSIS = SUBMISSION / "analysis"
sys.path.insert(0, str(ANALYSIS))

from compression_common import (  # noqa: E402
    canonical_bytes,
    load_json,
    reject_optimized_python,
    require,
    sealed,
    sha_file,
    sha_object,
)


OUTPUT_JSON = HERE / "PRINTED_CERTIFICATE_APPENDIX.json"
OUTPUT_TEX = SUBMISSION / "supplement" / "certificate_appendix.tex"

DIRECT_TABLE = SUBMISSION / "templates" / "DIRECT_CERTIFICATE_TEMPLATE_TABLE.json"
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

RESTORATION_ROOT = "s1:c658:t2792:p1032"
PROBE_ANCHOR = "tree:k3:identity"
CHARACTERS = ("0", "C", "G", "T")


def read_gzip_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), "INPUT_MISSING", path)
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        value = json.load(handle)
    require(isinstance(value, dict), "INPUT_NOT_OBJECT", path)
    return value


def iter_gzip_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    require(path.is_file(), "INPUT_MISSING", path)
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            value = json.loads(line)
            require(isinstance(value, dict), "ROW_NOT_OBJECT", f"{path}:{line_number}")
            yield value


def verify_seal(value: dict[str, Any]) -> None:
    observed = value.get("payload_sha256")
    require(isinstance(observed, str) and len(observed) == 64, "SEAL_MISSING")
    payload = dict(value)
    payload.pop("payload_sha256")
    require(observed == sha_object(payload), "SEAL_MISMATCH")


def ct_orbit_rep(characters: tuple[int, ...]) -> tuple[int, ...]:
    swapped = tuple(3 if x == 1 else 1 if x == 3 else x for x in characters)
    return min(characters, swapped)


def orbit_assignments(port_count: int) -> tuple[tuple[int, ...], ...]:
    values = set()
    for prefix in itertools.product(range(4), repeat=port_count - 1):
        last = 0
        for value in prefix:
            last ^= value
        values.add(ct_orbit_rep(prefix + (last,)))
    return tuple(sorted(values))


def normalize_terms(terms: list, convention: str) -> list[dict[str, Any]]:
    rows = []
    for term in terms:
        if convention == "indices_coefficient":
            indices, coefficient = term
        elif convention == "coefficient_indices":
            coefficient, indices = term
        else:  # pragma: no cover - internal misuse guard
            raise ValueError(convention)
        require(isinstance(coefficient, int) and coefficient != 0, "TERM_COEFFICIENT")
        require(isinstance(indices, list) and indices, "TERM_INDICES")
        rows.append({"coefficient": coefficient, "indices": indices})
    return rows


def polynomial_tex(terms: list[dict[str, Any]]) -> str:
    pieces: list[str] = []
    for ordinal, term in enumerate(terms):
        coefficient = term["coefficient"]
        magnitude = abs(coefficient)
        monomial = "".join(f"q_{{{index}}}" for index in term["indices"])
        scalar = "" if magnitude == 1 else str(magnitude)
        if ordinal == 0:
            sign = "-" if coefficient < 0 else ""
        else:
            sign = "+" if coefficient > 0 else "-"
        pieces.append(f"{sign}{scalar}{monomial}")
    return "".join(pieces)


def polynomial_tex_lines(
    terms: list[dict[str, Any]], *, terms_per_line: int, leading_symbol: str = ""
) -> str:
    chunks = [
        terms[index:index + terms_per_line]
        for index in range(0, len(terms), terms_per_line)
    ]
    rows = []
    for ordinal, chunk in enumerate(chunks):
        rendered = polynomial_tex(chunk)
        if ordinal and chunk[0]["coefficient"] > 0:
            rendered = "+" + rendered
        if ordinal == 0 and leading_symbol:
            rows.append(f"{leading_symbol}&={rendered}")
        else:
            rows.append(f"&\\quad {rendered}")
    return r"\\".join(rows)


def quadratic_templates(direct: dict[str, Any]) -> list[dict[str, Any]]:
    layers = (
        ("four-port", "raw4"),
        ("five-port theta2", "theta2"),
        ("three-port cycle in four-port coordinates", "cycle"),
        ("five-port restoration", "restoration"),
    )
    result = []
    expected = {"raw4": 8, "theta2": 4, "cycle": 6, "restoration": 5}
    for label, key in layers:
        templates = direct[key]["quadratic_literal_templates"]
        require(len(templates) == expected[key], "QUADRATIC_TEMPLATE_COUNT", key)
        for template in templates:
            body = template["body"]
            terms = [
                {"coefficient": coefficient, "indices": pair}
                for coefficient, pair in zip(
                    body["coefficients"], body["coordinate_pairs"], strict=True
                )
                if coefficient != 0
            ]
            display = polynomial_tex(terms)
            require(display == template["display_polynomial"], "QUADRATIC_DISPLAY_DRIFT")
            result.append(
                {
                    "template_id": template["template_id"],
                    "layer": label,
                    "coordinate_convention_id": body["coordinate_convention_id"],
                    "degree": body["degree"],
                    "multidegree": body["weight"],
                    "terms": terms,
                    "stored_coordinate_indices": sorted(
                        {index for pair in body["coordinate_pairs"] for index in pair}
                    ),
                    "display_tex": display,
                    "canonical_class_count": template["canonical_class_count"],
                    "raw_presentation_count": template["raw_presentation_count"],
                    "literal_body_sha256": template["body_sha256"],
                }
            )
    require(len(result) == 23, "TOTAL_QUADRATIC_TEMPLATE_COUNT")
    require(sum(row["canonical_class_count"] for row in result) == 995, "Q_CANONICAL_TOTAL")
    require(sum(row["raw_presentation_count"] for row in result) == 1872, "Q_RAW_TOTAL")
    return result


def high_degree_bases_and_transports() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    quintic = load_json(QUINTIC)
    quartic = load_json(QUARTIC)
    cubic = load_json(CUBIC)
    direct36 = load_json(DIRECT36)

    q_terms = normalize_terms(quintic["invariant"], "indices_coefficient")
    bases = [
        {
            "base_id": "HDQ-01",
            "family": "theta0 quintic",
            "degree": quintic["invariant_degree"],
            "multidegree": quintic["invariant_multidegree"],
            "terms": q_terms,
            "display_tex": polynomial_tex(q_terms),
            "formula_sha256": quintic["invariant_sha256"],
        }
    ]
    quartic_base_ids: dict[tuple[int, int], str] = {}
    for offset, certificate in enumerate(quartic["certificates"], 2):
        base_id = f"HDQ-{offset:02d}"
        quartic_base_ids[(certificate["source_index"], certificate["canonical_class_id"])] = base_id
        terms = normalize_terms(certificate["terms"], "coefficient_indices")
        bases.append(
            {
                "base_id": base_id,
                "family": "lower-theta quartic",
                "source_index": certificate["source_index"],
                "canonical_class_id": certificate["canonical_class_id"],
                "degree": certificate["degree"],
                "multidegree": certificate["port_weight"],
                "terms": terms,
                "display_tex": polynomial_tex(terms),
                "formula_sha256": sha_object(certificate["terms"]),
                "descriptor_sha256": certificate["descriptor_sha256"],
            }
        )
    c_terms = normalize_terms(cubic["normalized_terms"], "coefficient_indices")
    bases.append(
        {
            "base_id": "HDQ-05",
            "family": "theta3 cubic",
            "degree": cubic["degree"],
            "multidegree": cubic["bridge_multidegree"],
            "terms": c_terms,
            "display_tex": polynomial_tex(c_terms),
            "formula_sha256": cubic["normalized_polynomial_sha256"],
        }
    )
    require(len(bases) == 5, "HIGH_DEGREE_BASE_COUNT")

    quintic_transports = []
    for row in quintic["rows"]:
        require(row["target_pullback_zero"] is True, "QUINTIC_TARGET_NOT_ZERO")
        if row["source_pullback_terms"] == 0:
            continue
        quintic_transports.append(
            {
                "base_id": "HDQ-01",
                "source_index": 1,
                "canonical_class_id": row["class_id"],
                "port_permutation": row["permutation"],
                "source_pullback_term_count": row["source_pullback_terms"],
                "source_pullback_sha256": row["source_pullback_sha256"],
            }
        )
    require(len(quintic_transports) == 22, "QUINTIC_TRANSPORT_COUNT")
    require(sorted(quintic["zero_permutations"]) == [[0, 1, 2, 3], [2, 1, 0, 3]], "QUINTIC_ZERO_TRANSPORTS")

    quartic_transports = []
    for row in quartic["transports"]:
        base_source, base_class = (
            int(row["base_certificate"].split("-class", 1)[0].removeprefix("source")),
            int(row["base_certificate"].split("-class", 1)[1]),
        )
        base_id = quartic_base_ids[(base_source, base_class)]
        quartic_transports.append(
            {
                "base_id": base_id,
                "source_index": row["source_index"],
                "canonical_class_id": row["canonical_class_id"],
                "coordinate_permutation": row["coordinate_permutation"],
                "port_match": row["port_match"],
                "multidegree": row["port_weight"],
                "descriptor_sha256": row["descriptor_sha256"],
                "source_pullback_sha256": row["source_pullback_sha256"],
            }
        )
    require(len(quartic_transports) == 12, "QUARTIC_TRANSPORT_COUNT")
    require(
        {row["coordinate_permutation"] for row in quartic_transports}
        <= set(quartic["coordinate_permutations"]),
        "UNCERTIFIED_QUARTIC_COORDINATE_PERMUTATION",
    )

    cubic_transports = []
    for row in cubic["fresh_production_record_bindings"]:
        require(row["production_status"] == "separated", "CUBIC_BINDING_NOT_SEPARATED")
        cubic_transports.append(
            {
                "base_id": "HDQ-05",
                "source_index": row["source_index"],
                "canonical_class_id": row["canonical_class_id"],
                "port_match": row["port_match"],
                "semantic_record_sha256": row["semantic_record_sha256"],
                "record_file_sha256": row["record_file_sha256"],
            }
        )
    require(len(cubic_transports) == 2, "CUBIC_TRANSPORT_COUNT")

    expected_direct = {
        (row["source_index"], row["canonical_class_id"])
        for row in direct36["coverage"]
    }
    printed_direct = {
        (row["source_index"], row["canonical_class_id"])
        for row in quintic_transports + quartic_transports + cubic_transports
    }
    require(expected_direct == printed_direct and len(printed_direct) == 36, "DIRECT36_TRANSPORT_COVERAGE")
    return bases, {
        "contract": (
            "Only the 22 port permutations, 12 quartic coordinate transports, "
            "and two cubic record bindings printed here are licensed.  No other "
            "port, source-target, inheritance, pole/sink, or C/T transport is inferred."
        ),
        "theta0_quintic": quintic_transports,
        "lower_theta_quartic": quartic_transports,
        "theta3_cubic": cubic_transports,
        "covered_directional_records": 36,
    }


def coordinate_dictionaries(
    quadratics: list[dict[str, Any]], bases: list[dict[str, Any]]
) -> dict[str, Any]:
    four_indices = {
        index
        for row in quadratics
        if row["coordinate_convention_id"] in {
            "k2p_four_port_fourier_flat_index_v1",
            "k2p_cycle_restored_fourier_flat_index_v1",
        }
        for index in row["stored_coordinate_indices"]
    }
    for base in bases:
        four_indices.update(index for term in base["terms"] for index in term["indices"])
    five_indices = {
        index
        for row in quadratics
        if row["coordinate_convention_id"] in {
            "k2p_five_port_fourier_flat_index_v1",
            "k2p_restored_five_port_fourier_flat_index_v1",
        }
        for index in row["stored_coordinate_indices"]
    }
    four = orbit_assignments(4)
    five = orbit_assignments(5)
    require(four_indices == set(range(36)), "FOUR_PORT_DISPLAYED_INDEX_SET", sorted(four_indices))
    require(len(five_indices) == 52, "FIVE_PORT_DISPLAYED_INDEX_COUNT")
    return {
        "definition": (
            "Start with zero-sum tuples in Z_2 x Z_2, replace each by the "
            "lexicographically smaller of it and its global C/T swap, remove "
            "duplicates, and order the representatives lexicographically."
        ),
        "character_integer_order": list(CHARACTERS),
        "four_port": [
            {
                "index": index,
                "integer_tuple": list(four[index]),
                "character_tuple": "".join(CHARACTERS[value] for value in four[index]),
            }
            for index in sorted(four_indices)
        ],
        "five_port_displayed": [
            {
                "index": index,
                "integer_tuple": list(five[index]),
                "character_tuple": "".join(CHARACTERS[value] for value in five[index]),
            }
            for index in sorted(five_indices)
        ],
    }


def compact_restoration_row(row: dict[str, Any], layer: int) -> dict[str, Any]:
    if layer == 1:
        evidence = row.get("certificate_sha256") or sha_object(row["certificate"])
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
    evidence = row.get("certificate_sha256") or sha_object(row["certificate"])
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


def restoration_example() -> dict[str, Any]:
    forest = load_json(RESTORATION)
    first_source = [row for row in forest["first_coverage"] if row["root_id"] == RESTORATION_ROOT]
    second_source = [row for row in forest["second_coverage"] if row["root_id"] == RESTORATION_ROOT]
    require(len(first_source) == 14 and len(second_source) == 8, "RESTORATION_EXAMPLE_CHILD_COUNTS")
    first = [compact_restoration_row(row, 1) for row in first_source]
    second = [compact_restoration_row(row, 2) for row in second_source]
    continuations = [row for row in first if row["status"] == "continuation"]
    require(len(continuations) == 1, "RESTORATION_EXAMPLE_CONTINUATION_COUNT")
    parent_ordinal = continuations[0]["ordinal"]
    require(
        all(row["parent_first_coverage_index"] == parent_ordinal for row in second),
        "RESTORATION_EXAMPLE_WRONG_SECOND_PARENT",
    )
    require(
        all(row["status"] == "separated" and row["remaining_roles"] == [] for row in second),
        "RESTORATION_EXAMPLE_UNTERMINATED_SECOND_CHILD",
    )
    require(
        all(row["status"] in {"separated", "continuation"} for row in first),
        "RESTORATION_EXAMPLE_BAD_FIRST_STATUS",
    )
    return {
        "root_id": RESTORATION_ROOT,
        "first_children": first,
        "second_children": second,
        "first_proof_census": dict(sorted(Counter(row["proof"] for row in first).items())),
        "second_proof_census": dict(sorted(Counter(row["proof"] for row in second).items())),
        "termination": {
            "continuation_count": 1,
            "continuation_ordinal": parent_ordinal,
            "terminal_leaf_count": 21,
            "maximum_depth": 2,
            "unresolved": 0,
            "cycles": 0,
            "statement": (
                "Thirteen first children terminate; the unique continuation has "
                "exactly eight second children, all separated with no remaining role."
            ),
        },
    }


def find_probe_rows(path: Path, field: str) -> list[dict[str, Any]]:
    return [row for row in iter_gzip_jsonl(path) if row.get(field) == PROBE_ANCHOR]


def record_ids(path: Path, ids: set[str]) -> set[str]:
    found = set()
    for row in iter_gzip_jsonl(path):
        record_id = row.get("record_id")
        if record_id in ids:
            found.add(record_id)
    return found


def probe_example() -> dict[str, Any]:
    certificate = load_json(PROBE_CERTIFICATE)
    anchors = certificate["anchor_inventory"]["public_anchors"]
    anchor = next(row for row in anchors if row["anchor_id"] == PROBE_ANCHOR)
    one_rows = find_probe_rows(ONE_PORT, "parent_anchor_id")
    two_rows = find_probe_rows(TWO_PORT, "base_anchor_id")
    require(len(one_rows) == 9 and len(two_rows) == 75, "PROBE_EXAMPLE_ROW_COUNTS")
    one = next(
        row
        for row in one_rows
        if row["status"] == "isomorphic"
        and row["source_site_index"] == row["target_site_index"] == 0
    )
    parent_id = f"P1:{PROBE_ANCHOR}:0:0"
    two = next(
        row
        for row in two_rows
        if row["status"] == "isomorphic"
        and row["one_port_parent_id"] == parent_id
        and row["second_source_site_index"] == row["second_target_site_index"] == 0
    )
    require(two["parent_transport_id"] == one["transport_id"], "PROBE_EXAMPLE_PARENT_TRANSPORT")
    transport_ids = {
        anchor["transport_id"],
        one["transport_id"],
        two["transport_id"],
        two["reverse_order_certificate"]["reverse_parent_transport_id"],
    }
    restriction_ids = {
        one["source_parent_restriction_id"],
        one["target_parent_restriction_id"],
        two["source_parent_restriction_id"],
        two["target_parent_restriction_id"],
    }
    require(record_ids(TRANSPORTS, transport_ids) == transport_ids, "PROBE_EXAMPLE_TRANSPORT_MISSING")
    require(record_ids(RESTRICTIONS, restriction_ids) == restriction_ids, "PROBE_EXAMPLE_RESTRICTION_MISSING")
    one_compact = {
        key: one[key]
        for key in (
            "inserted_label",
            "source_site_id",
            "source_site_index",
            "target_site_id",
            "target_site_index",
            "source_parent_restriction_id",
            "target_parent_restriction_id",
            "parent_transport_id",
            "transport_id",
            "transport_restriction",
            "status",
        )
    }
    one_compact["ledger_row_sha256"] = sha_object(one)
    two_compact = {
        key: two[key]
        for key in (
            "first_label",
            "second_label",
            "one_port_parent_id",
            "first_source_site_index",
            "first_target_site_index",
            "second_source_site_id",
            "second_source_site_index",
            "second_target_site_id",
            "second_target_site_index",
            "source_parent_restriction_id",
            "target_parent_restriction_id",
            "parent_transport_id",
            "transport_id",
            "transport_restriction",
            "status",
            "reverse_order_certificate",
        )
    }
    two_compact["ledger_row_sha256"] = sha_object(two)
    return {
        "anchor": {
            "anchor_id": anchor["anchor_id"],
            "canonical_anchor_class_id": anchor["canonical_anchor_class_id"],
            "origin": anchor["origin"],
            "relation": anchor["relation"],
            "labels": anchor["labels"],
            "source_graph_sha256": anchor["source_graph_sha256"],
            "target_graph_sha256": anchor["target_graph_sha256"],
            "transport_id": anchor["transport_id"],
        },
        "anchor_row_census": {
            "one_port": dict(sorted(Counter(row["status"] for row in one_rows).items())),
            "two_port": dict(sorted(Counter(row["status"] for row in two_rows).items())),
        },
        "selected_one_port_transport": one_compact,
        "selected_two_port_transport": two_compact,
        "conclusion": (
            "The two-port transport restricts to the selected one-port transport, "
            "and its reversed marginal names a second exact one-port transport on "
            "the same base anchor."
        ),
    }


def direct_example(direct: dict[str, Any]) -> dict[str, Any]:
    template = next(
        row for row in direct["raw4"]["quadratic_literal_templates"]
        if row["template_id"] == "R4Q-03"
    )
    assignment = template["assignments"][0]
    registry = read_gzip_json(RAW4_REGISTRY)
    registry_row = next(
        row for row in registry["rows"]
        if row["class_identifier"] == assignment["canonical_class"]
    )
    require(
        registry_row["terminal_certificate"]["certificate_payload_sha256"]
        == assignment["frozen_certificate_sha256"],
        "R4Q03_ASSIGNMENT_BINDING",
    )
    return {
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


def binding(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(PROJECT)),
        "sha256": sha_file(path),
        "bytes": path.stat().st_size,
    }


def payload() -> dict[str, Any]:
    direct = load_json(DIRECT_TABLE)
    verify_seal(direct)
    quadratics = quadratic_templates(direct)
    bases, transports = high_degree_bases_and_transports()
    coordinates = coordinate_dictionaries(quadratics, bases)
    return {
        "schema": "k2p-printed-certificate-appendix-v1",
        "status": "PASS",
        "scope": (
            "Reader-facing exact formulas, coordinate dictionaries, licensed "
            "high-degree transports, and three worked certificate paths."
        ),
        "quadratic_transport_contract": (
            "The 23 quadratic templates identify literal coefficient, coordinate-pair, "
            "and multidegree bodies only.  Equality of displayed formulas across layers "
            "does not license any graph, port, direction, or coordinate transport."
        ),
        "quadratic_templates": quadratics,
        "quadratic_template_count": len(quadratics),
        "high_degree_bases": bases,
        "high_degree_base_count": len(bases),
        "certified_high_degree_transports": transports,
        "coordinate_dictionaries": coordinates,
        "worked_examples": {
            "direct_quadratic_R4Q_03": direct_example(direct),
            "restoration_root_s1_c658_t2792_p1032": restoration_example(),
            "probe_tree_k3_identity": probe_example(),
        },
        "producer_command": (
            ".venv/bin/python -B proof_compression_submission/templates/"
            "build_printed_certificate_appendix.py --write"
        ),
        "check_command": (
            ".venv/bin/python -B proof_compression_submission/templates/"
            "build_printed_certificate_appendix.py --check"
        ),
        "independent_replay_command": (
            ".venv/bin/python -B proof_compression_submission/templates/"
            "verify_printed_certificate_appendix.py"
        ),
        "mutation_command": (
            ".venv/bin/python -B proof_compression_submission/templates/"
            "test_printed_certificate_appendix_mutations.py"
        ),
        "input_bindings": [
            binding(path)
            for path in (
                DIRECT_TABLE,
                RAW4_REGISTRY,
                QUINTIC,
                QUARTIC,
                CUBIC,
                DIRECT36,
                RESTORATION,
                PROBE_CERTIFICATE,
                ONE_PORT,
                TWO_PORT,
                RESTRICTIONS,
                TRANSPORTS,
            )
        ],
    }


def tex_escape(value: str) -> str:
    return (
        value.replace("\\", r"\textbackslash{}")
        .replace("_", r"\_")
        .replace("%", r"\%")
        .replace("#", r"\#")
        .replace("&", r"\&")
    )


def mdeg_tex(values: list[int]) -> str:
    return "(" + ",".join(str(value) for value in values) + ")"


def dictionary_table(rows: list[dict[str, Any]], columns: int = 4) -> str:
    chunks = [rows[index:index + columns] for index in range(0, len(rows), columns)]
    header = " & ".join([r"index & tuple"] * columns)
    alignment = "".join(["r l"] * columns)
    lines = [f"\\begin{{tabular}}{{{alignment}}}", r"\toprule", header + r"\\", r"\midrule"]
    for chunk in chunks:
        cells: list[str] = []
        for row in chunk:
            cells.extend([f"$q_{{{row['index']}}}$", f"${row['character_tuple']}$"])
        while len(cells) < columns * 2:
            cells.extend(["", ""])
        lines.append(" & ".join(cells) + r"\\")
    lines.extend([r"\bottomrule", r"\end{tabular}"])
    return "\n".join(lines)


def high_transport_tables(value: dict[str, Any]) -> str:
    transports = value["certified_high_degree_transports"]
    lines = [
        r"\paragraph{Quintic port transports.}",
        r"\begin{longtable}{r l r}",
        r"\toprule class & port permutation & source terms\\\midrule\endhead",
    ]
    for row in transports["theta0_quintic"]:
        lines.append(
            f"{row['canonical_class_id']} & $({','.join(map(str,row['port_permutation']))})$ & "
            f"{row['source_pullback_term_count']}\\\\"
        )
    lines.extend([r"\bottomrule", r"\end{longtable}", r"\paragraph{Quartic coordinate transports.}"])
    lines.extend([
        r"\begin{longtable}{r r l l l}",
        r"\toprule source & class & base & coordinate action & port match\\\midrule\endhead",
    ])
    for row in transports["lower_theta_quartic"]:
        lines.append(
            f"{row['source_index']} & {row['canonical_class_id']} & {row['base_id']} & "
            f"{tex_escape(row['coordinate_permutation'])} & "
            f"$({','.join(map(str,row['port_match']))})$\\\\"
        )
    lines.extend([r"\bottomrule", r"\end{longtable}", r"\paragraph{Cubic record bindings.}"])
    lines.extend([
        r"\begin{center}\begin{tabular}{r r l l}",
        r"\toprule source & class & base & port match\\\midrule",
    ])
    for row in transports["theta3_cubic"]:
        lines.append(
            f"{row['source_index']} & {row['canonical_class_id']} & {row['base_id']} & "
            f"$({','.join(map(str,row['port_match']))})$\\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}\end{center}"])
    return "\n".join(lines)


def restoration_table(example: dict[str, Any]) -> str:
    lines = [
        r"\begin{longtable}{@{}r r L{.13\linewidth} r L{.17\linewidth} l L{.26\linewidth}@{}}",
        r"\toprule layer & row & restored role & site & proof & status & row SHA-256\\\midrule\endhead",
    ]
    for row in example["first_children"]:
        lines.append(
            f"1 & {row['ordinal']} & \\path{{{row['restored_role']}}} & "
            f"{row['source_insertion_index']} & \\path{{{row['proof']}}} & "
            f"{row['status']} & \\hashvalue{{{row['row_sha256']}}}\\\\"
        )
    for ordinal, row in enumerate(example["second_children"], 1):
        lines.append(
            f"2 & {ordinal} & \\path{{{row['second_restored_role']}}} & "
            f"{row['second_source_insertion_index']} & \\path{{{row['proof']}}} & "
            f"{row['status']} & \\hashvalue{{{row['row_sha256']}}}\\\\"
        )
    lines.extend([r"\bottomrule", r"\end{longtable}"])
    return "\n".join(lines)


def command_tex(command: str) -> str:
    """Render an exact shell command with visible break opportunities."""

    rendered: list[str] = []
    for token in command.split():
        if "/" in token or "_" in token:
            rendered.append(rf"\path{{{token}}}")
        else:
            rendered.append(rf"\texttt{{{tex_escape(token)}}}")
    return r"\allowbreak{} ".join(rendered)


def render_tex(value: dict[str, Any]) -> str:
    quadratic_rows = []
    for row in value["quadratic_templates"]:
        quadratic_rows.append(
            f"{row['template_id']} & {tex_escape(row['layer'])} & "
            r"$\begin{aligned}"
            + polynomial_tex_lines(row["terms"], terms_per_line=3)
            + r"\end{aligned}$ & "
            f"${mdeg_tex(row['multidegree'])}$ & {row['canonical_class_count']} & "
            f"{row['raw_presentation_count']}\\\\"
        )
    bases = []
    for base in value["high_degree_bases"]:
        bases.append(
            f"\\paragraph{{{base['base_id']}: {tex_escape(base['family'])}.}} "
            f"Degree {base['degree']}, multidegree ${mdeg_tex(base['multidegree'])}$.\n"
            r"\[\begin{aligned}"
            + polynomial_tex_lines(
                base["terms"],
                terms_per_line=4,
                leading_symbol=f"F_{{{base['base_id']}}}",
            )
            + r"\end{aligned}\]"
        )
    direct = value["worked_examples"]["direct_quadratic_R4Q_03"]
    restoration = value["worked_examples"]["restoration_root_s1_c658_t2792_p1032"]
    probe = value["worked_examples"]["probe_tree_k3_identity"]
    one = probe["selected_one_port_transport"]
    two = probe["selected_two_port_transport"]
    provenance_rows = "\n".join(
        f"\\path{{{row['path']}}} & "
        f"\\hashvalue{{{row['sha256']}}}\\\\"
        for row in value["input_bindings"]
    )
    return rf"""% Generated by build_printed_certificate_appendix.py; do not hand edit.
\section{{Printed exact-certificate appendix}}\label{{sec:printed-certificates}}

This appendix exposes the formulas already derived by the first compression
cycle; it is not a second compression claim.  {value['quadratic_transport_contract']}
In particular, the repeated literal bodies in different layers remain
different graph-derived certificates.

\subsection{{Coordinate dictionaries}}

Write the character group in the integer order \(0,C,G,T\).  A coordinate
index is obtained by listing the zero-sum tuples, replacing each tuple by the
lexicographically smaller of it and its global \(C/T\) swap, deleting
duplicates, and sorting.  Thus \(q_i=q_{{h_1\cdots h_k}}\) for the tuple printed
below.  All 36 four-port coordinates occur in the printed quadratic or
higher-degree formulas:

\begin{{center}}\footnotesize
{dictionary_table(value['coordinate_dictionaries']['four_port'])}
\end{{center}}

The following are exactly the 52 five-port indices occurring in the stored
literal coordinate-pair blocks behind the printed theta2 and restoration
quadratics.  Of these, 46 have a nonzero displayed coefficient; six occur only
in zero slots retained by the exact certificate-body normalization:

\begin{{center}}\footnotesize
{dictionary_table(value['coordinate_dictionaries']['five_port_displayed'])}
\end{{center}}

\subsection{{The 23 literal quadratic bodies}}

The multidegree is ordered as
$(s_0,g_0,s_1,g_1,\ldots)$.  ``Canonical'' counts exact certificate classes;
``raw'' counts their raw directional presentations.

\begingroup\scriptsize
\begin{{longtable}}{{l L{{.16\linewidth}} L{{.34\linewidth}} L{{.18\linewidth}} r r}}
\toprule ID & layer & polynomial & multidegree & canonical & raw\\\midrule\endhead
{chr(10).join(quadratic_rows)}
\bottomrule
\end{{longtable}}
\endgroup

\subsection{{Five high-degree bases and their licensed transports}}

{value['certified_high_degree_transports']['contract']}

{chr(10).join(bases)}

{high_transport_tables(value)}

\subsection{{Three worked paths}}

\paragraph{{A direct quadratic separator.}}
Template R4Q-03 is
$$
 {direct['formula']},\qquad
 \operatorname{{mdeg}}={mdeg_tex(direct['multidegree'])}.
$$
It covers {direct['canonical_class_count']} canonical classes and
{direct['raw_presentation_count']} raw directions.  For the representative
\texttt{{{tex_escape(direct['representative_class'])}}}, its source pullback has
{direct['source_pullback_term_count']} nonzero terms and its target pullback is
identically zero.  The exact certificate is
\hashvalue{{{direct['certificate_sha256']}}}, bound to the graph record by
\hashvalue{{{direct['certificate_binding_sha256']}}}.  This proves the stated
source-to-target noncontainment; reversing the direction is not licensed.

\paragraph{{A complete restoration root.}}
For \texttt{{{tex_escape(restoration['root_id'])}}}, the following table prints
every actual first- and second-child archetype.  The row hash binds the role,
insertion site, proof mechanism, transport fields, and evidence certificate.

\begingroup\scriptsize
{restoration_table(restoration)}
\endgroup

There are 14 first children: 12 displayed-quartet terminals, one
full-map \(\mathcal T_i\) terminal, and one continuation (row
{restoration['termination']['continuation_ordinal']}).  That continuation has
exactly eight children: seven displayed-quartet terminals and one
full-map \(\mathcal T_i\) terminal.  Every second child has an empty remaining-role
list.  Hence this exact subtree has {restoration['termination']['terminal_leaf_count']}
leaves, depth {restoration['termination']['maximum_depth']}, zero unresolved
records, and no cycle.

\paragraph{{A one-/two-port word transport.}}
The anchor \texttt{{{tex_escape(PROBE_ANCHOR)}}} is the labelled identity tree
transport \hashvalue{{{probe['anchor']['transport_id']}}}.  At source and target
site zero, inserting label {one['inserted_label']} gives the exact one-port
transport \hashvalue{{{one['transport_id']}}}; both parent restrictions are
\hashvalue{{{one['source_parent_restriction_id']}}}.  Inserting label
{two['second_label']} at the new site zero gives the exact two-port transport
\hashvalue{{{two['transport_id']}}}, whose parent transport is precisely the
one-port transport.  Its two restriction records are
\hashvalue{{{two['source_parent_restriction_id']}}} and
\hashvalue{{{two['target_parent_restriction_id']}}}.  The reversed marginal is
the exact one-port transport
\hashvalue{{{two['reverse_order_certificate']['reverse_parent_transport_id']}}}
on the same base anchor.  The selected ledger rows have hashes
\hashvalue{{{one['ledger_row_sha256']}}} and
\hashvalue{{{two['ledger_row_sha256']}}}.  Thus both deletion orders are bound,
not inferred from an unrecorded symmetry.

\subsection{{Provenance and replay}}

% exact command: {value['producer_command']}
% exact command: {value['check_command']}
% exact command: {value['independent_replay_command']}
% exact command: {value['mutation_command']}

\begin{{center}}\footnotesize
\begin{{tabular}}{{L{{.24\linewidth}}L{{.68\linewidth}}}}
\toprule
field & exact value\\
\midrule
schema/version & \texttt{{{tex_escape(value['schema'])}}}\\
producer & {command_tex(value['producer_command'])}\\
deterministic check & {command_tex(value['check_command'])}\\
independent replay & {command_tex(value['independent_replay_command'])}\\
mutation suite & {command_tex(value['mutation_command'])}\\
sealed payload & \hashvalue{{{value['payload_sha256']}}}\\
\bottomrule
\end{{tabular}}
\end{{center}}

The authoritative input bindings are:

\begingroup\scriptsize
\begin{{longtable}}{{@{{}}L{{.47\linewidth}}L{{.45\linewidth}}@{{}}}}
\toprule path & SHA-256\\\midrule\endhead
{provenance_rows}
\bottomrule
\end{{longtable}}
\endgroup
"""


def write_or_check(mode: str) -> None:
    value = sealed(payload())
    json_text = json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    tex_text = render_tex(value).rstrip() + "\n"
    if mode == "write":
        OUTPUT_JSON.write_text(json_text, encoding="utf-8")
        OUTPUT_TEX.write_text(tex_text, encoding="utf-8")
    else:
        require(OUTPUT_JSON.is_file(), "OUTPUT_JSON_MISSING")
        require(OUTPUT_TEX.is_file(), "OUTPUT_TEX_MISSING")
        require(OUTPUT_JSON.read_text(encoding="utf-8") == json_text, "OUTPUT_JSON_DRIFT")
        require(OUTPUT_TEX.read_text(encoding="utf-8") == tex_text, "OUTPUT_TEX_DRIFT")
    print(
        json.dumps(
            {
                "status": "PASS",
                "mode": mode,
                "payload_sha256": value["payload_sha256"],
                "quadratic_templates": value["quadratic_template_count"],
                "high_degree_bases": value["high_degree_base_count"],
                "four_port_coordinates": len(value["coordinate_dictionaries"]["four_port"]),
                "five_port_coordinates": len(value["coordinate_dictionaries"]["five_port_displayed"]),
            },
            sort_keys=True,
        )
    )


def main() -> None:
    reject_optimized_python()
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    write_or_check("write" if arguments.write else "check")


if __name__ == "__main__":
    main()

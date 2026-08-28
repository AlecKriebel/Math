#!/usr/bin/env python3
"""Bind every promoted displayed-quartet terminal to literal K2P coordinates.

This verifier is intentionally independent of the graph generator,
canonicalizer, classifiers, and layer verifiers.  It treats their displayed
split sets as committed inputs, derives the exact C/T-sector Fourier body for
each commitment, and streams every promoted terminal reference.  The graph
replayers remain responsible for binding a row to its displayed split sets;
this program closes the separate split-set-to-literal-algebra bridge.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import sys
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
DEFAULT_PROJECT = HERE.parents[1]
DEFAULT_SEMANTICS = HERE / "quartet_logic_certificate.json"
STRICT_JSON_DIR = DEFAULT_PROJECT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import (  # noqa: E402
    StrictJSONError,
    decode_json_document,
    iter_canonical_gzip_jsonl,
    load_canonical_gzip_json,
)

RAW4_LEDGER = "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz"
THETA2_LEDGER = "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz"
THETA2_RESTORATION = "work/theta2_five_port_closure/artifacts/fixed_full_restoration_closure.json.gz"
CYCLE_LEDGER = "work/cycle_three_port_closure/promotion/cycle_full_authoritative.jsonl.gz"
CYCLE_REGISTRY = "work/cycle_three_port_closure/artifacts/topology_witnesses.json"
RESTORATION_FOREST = "work/restoration_sign_reclassification/corrected_restoration_forest.json"
PROBE_ONE = "work/probe_coherence_corrected/one_port_ledger.jsonl.gz"
PROBE_TWO = "work/probe_coherence_corrected/two_port_ledger.jsonl.gz"
PROBE_REGISTRY = "work/probe_coherence_corrected/separation_proof_registry.json.gz"

EXPECTED = {
    "raw4": {"rows": 405_216, "quartet": 360_408, "certificates": 18},
    "theta2": {"rows": 2_946_240, "quartet": 2_942_592, "certificates": 19},
    "theta2_restoration": {
        "six_rows": 576,
        "six_quartet": 504,
        "seven_rows": 288,
        "seven_quartet": 256,
        "quartet": 760,
        "certificates": 24,
    },
    "cycle": {"rows": 536_364, "quartet": 535_920, "certificates": 97},
    "restoration": {
        "first_rows": 36_568,
        "first_quartet": 35_758,
        "second_rows": 256,
        "second_quartet": 248,
        "quartet": 36_006,
        "certificates": 92,
    },
    "probe": {
        "one_rows": 29_964,
        "one_quartet": 27_758,
        "two_rows": 544_571,
        "two_quartet": 511_266,
        "quartet": 539_024,
        "certificates": 638,
    },
}


class QuartetTerminalFailure(RuntimeError):
    """Fail-closed diagnostic from the terminal binder."""


def require(condition: bool, code: str, detail: Any = None) -> None:
    if not condition:
        suffix = "" if detail is None else f":{detail}"
        raise QuartetTerminalFailure(f"{code}{suffix}")


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), "JSON_INPUT_MISSING", path)
    try:
        return decode_json_document(
            path.read_bytes(), label=str(path), require_object=True
        )
    except (OSError, StrictJSONError) as error:
        raise QuartetTerminalFailure(
            f"JSON_STRICT_DECODE_FAIL:{path}:{error}"
        ) from error


def load_gzip_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), "GZIP_JSON_INPUT_MISSING", path)
    try:
        value = load_canonical_gzip_json(path, label=str(path))
    except (OSError, StrictJSONError) as error:
        raise QuartetTerminalFailure(
            f"GZIP_JSON_STRICT_DECODE_FAIL:{path}:{error}"
        ) from error
    require(isinstance(value, dict), "GZIP_JSON_INPUT_NOT_OBJECT", path)
    return value


def iter_gzip_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    require(path.is_file(), "GZIP_JSONL_INPUT_MISSING", path)
    try:
        for row in iter_canonical_gzip_jsonl(path, label=str(path)):
            require(isinstance(row, dict), "GZIP_JSONL_ROW_NOT_OBJECT", path)
            yield row
    except (OSError, StrictJSONError) as error:
        raise QuartetTerminalFailure(
            f"GZIP_JSONL_STRICT_DECODE_FAIL:{path}:{error}"
        ) from error


def verify_payload(value: dict[str, Any], code: str) -> None:
    claimed = value.get("payload_sha256")
    body = dict(value)
    body.pop("payload_sha256", None)
    require(type(claimed) is str and claimed == sha_object(body), code)


def normalize_quartet(value: Any) -> tuple[int, int, int, int]:
    require(
        isinstance(value, list)
        and len(value) == 4
        and all(type(label) is int for label in value),
        "QUARTET_SCHEMA_FAIL",
        value,
    )
    quartet = tuple(value)
    require(tuple(sorted(quartet)) == quartet and len(set(quartet)) == 4, "QUARTET_ORDER_FAIL", value)
    return quartet


def normalize_split(value: Any) -> tuple[tuple[int, int], tuple[int, int]]:
    require(isinstance(value, list) and len(value) == 2, "SPLIT_SCHEMA_FAIL", value)
    parts: list[tuple[int, int]] = []
    for part in value:
        require(
            isinstance(part, list)
            and len(part) == 2
            and all(type(label) is int for label in part),
            "SPLIT_PART_SCHEMA_FAIL",
            value,
        )
        ordered = tuple(sorted(part))
        require(len(set(ordered)) == 2, "SPLIT_PART_REPEAT_FAIL", value)
        parts.append(ordered)
    split = tuple(sorted(parts))
    require(set(split[0]).isdisjoint(split[1]), "SPLIT_OVERLAP_FAIL", value)
    return split  # type: ignore[return-value]


def split_json(split: tuple[tuple[int, int], tuple[int, int]]) -> list[list[int]]:
    return [list(split[0]), list(split[1])]


def split_set_json(values: Iterable[tuple[tuple[int, int], tuple[int, int]]]) -> list[list[list[int]]]:
    return [split_json(split) for split in sorted(values)]


def quartet_splits(quartet: tuple[int, int, int, int]) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    a, b, c, d = quartet
    return (
        normalize_split([[a, b], [c, d]]),
        normalize_split([[a, c], [b, d]]),
        normalize_split([[a, d], [b, c]]),
    )


def split_letter(
    quartet: tuple[int, int, int, int],
    split: tuple[tuple[int, int], tuple[int, int]],
) -> str:
    splits = quartet_splits(quartet)
    require(split in splits, "DISTINGUISHED_SPLIT_NOT_ON_QUARTET", {"quartet": quartet, "split": split})
    return ("A", "B", "C")[splits.index(split)]


def content_split_sets(content: dict[str, Any]) -> tuple[
    tuple[int, int, int, int],
    frozenset[tuple[tuple[int, int], tuple[int, int]]],
    frozenset[tuple[tuple[int, int], tuple[int, int]]],
]:
    quartet = normalize_quartet(content.get("quartet"))
    source_raw = content.get("source_displayed_splits", content.get("source_splits"))
    target_raw = content.get("target_displayed_splits", content.get("target_splits"))
    require(isinstance(source_raw, list) and isinstance(target_raw, list), "DISPLAYED_SET_SCHEMA_FAIL")
    source = frozenset(normalize_split(split) for split in source_raw)
    target = frozenset(normalize_split(split) for split in target_raw)
    require(len(source) == len(source_raw) and len(target) == len(target_raw), "DUPLICATE_DISPLAYED_SPLIT_FAIL")
    universe = set(quartet_splits(quartet))
    require(bool(source) and bool(target), "EMPTY_DISPLAYED_SET_FAIL", quartet)
    require(source != target, "EQUAL_DISPLAYED_SET_FAIL", quartet)
    require(source | target <= universe, "DISPLAYED_SPLIT_OUTSIDE_QUARTET_FAIL", quartet)
    return quartet, source, target


def expected_witness(
    quartet: tuple[int, int, int, int],
    source: frozenset[tuple[tuple[int, int], tuple[int, int]]],
    target: frozenset[tuple[tuple[int, int], tuple[int, int]]],
) -> dict[str, Any]:
    if len(source) == 1:
        distinguished = next(iter(source))
        require(bool(target - source), "SINGLETON_SOURCE_NOT_SEPARATED", quartet)
        kind, zero_on, positive_on = "I_singleton", "source", "target"
    elif len(target) == 1:
        distinguished = next(iter(target))
        require(bool(source - target), "SINGLETON_TARGET_NOT_SEPARATED", quartet)
        kind, zero_on, positive_on = "I_singleton", "target", "source"
    elif target - source:
        distinguished = min(target - source, key=repr)
        kind, zero_on, positive_on = "J_membership", "source", "target"
    else:
        distinguished = min(source - target, key=repr)
        kind, zero_on, positive_on = "J_membership", "target", "source"
    return {
        "quartet": quartet,
        "distinguished_split": distinguished,
        "invariant_kind": kind,
        "zero_on": zero_on,
        "strictly_positive_on": positive_on,
    }


def local_word(
    quartet: tuple[int, int, int, int],
    split: tuple[tuple[int, int], tuple[int, int]],
) -> str:
    first = set(split[0])
    second = set(split[1])
    require(first | second == set(quartet), "WORD_SPLIT_QUARTET_FAIL")
    return "".join("C" if label in first else "T" for label in quartet)


def literal_binding(
    witness: dict[str, Any],
    semantics_formulas: dict[str, list[list[Any]]],
) -> dict[str, Any]:
    quartet = witness["quartet"]
    distinguished = witness["distinguished_split"]
    kind = witness["invariant_kind"]
    letter = split_letter(quartet, distinguished)
    family = "F" if kind == "I_singleton" else "J"
    require(kind in {"I_singleton", "J_membership"}, "INVARIANT_KIND_FAIL", kind)
    formula_id = f"{family}_{letter}"
    require(formula_id in semantics_formulas, "SEMANTICS_FORMULA_MISSING", formula_id)

    patterns = {split: local_word(quartet, split) for split in quartet_splits(quartet)}
    if family == "F":
        terms = [[1, "CCCC"], [-1, patterns[distinguished]]]
        zero_splits = [distinguished]
        positive_splits = [split for split in quartet_splits(quartet) if split != distinguished]
        strict_factor = "prod_{leaf in quartet}(s_leaf)*(1-g_internal)"
    else:
        terms = [[1, "CCCC"], [1, patterns[distinguished]]]
        for split in quartet_splits(quartet):
            if split != distinguished:
                terms.append([-1, patterns[split]])
        zero_splits = [split for split in quartet_splits(quartet) if split != distinguished]
        positive_splits = [distinguished]
        strict_factor = "2*prod_{leaf in quartet}(s_leaf)*(1-g_internal)"

    expected_terms = semantics_formulas[formula_id]
    require(
        collections.Counter((coefficient, word) for coefficient, word in terms)
        == collections.Counter((coefficient, word) for coefficient, word in expected_terms),
        "LITERAL_FORMULA_SPEC_MISMATCH",
        formula_id,
    )
    for _coefficient, word in terms:
        codes = {"C": 1, "G": 2, "T": 3}
        total = 0
        for character in word:
            total ^= codes[character]
        require(total == 0, "LITERAL_COORDINATE_NOT_CONSERVED", word)

    coordinate_terms = []
    for coefficient, word in terms:
        coordinate_terms.append(
            [
                coefficient,
                [[label, character] for label, character in zip(quartet, word)],
            ]
        )
    result = {
        "quartet": list(quartet),
        "distinguished_split": split_json(distinguished),
        "invariant_kind": kind,
        "formula_id": formula_id,
        "zero_on": witness["zero_on"],
        "strictly_positive_on": witness["strictly_positive_on"],
        "coordinate_terms": coordinate_terms,
        "unlisted_leaf_characters": "0",
        "zero_tree_splits": split_set_json(zero_splits),
        "strictly_positive_tree_splits": split_set_json(positive_splits),
        "strict_pullback": strict_factor,
        "licensed_character_transport": "identity_or_global_C_T_swap",
    }
    result["binding_sha256"] = sha_object(result)
    return result


def validate_content(
    content: dict[str, Any],
    semantics_formulas: dict[str, list[list[Any]]],
    *,
    require_stored_witness: bool,
) -> dict[str, Any]:
    quartet, source, target = content_split_sets(content)
    expected = expected_witness(quartet, source, target)
    if require_stored_witness:
        observed_split = normalize_split(content.get("distinguished_split"))
        require(observed_split == expected["distinguished_split"], "STORED_DISTINGUISHED_SPLIT_FAIL")
        require(content.get("invariant_kind") == expected["invariant_kind"], "STORED_INVARIANT_KIND_FAIL")
        require(content.get("zero_on") == expected["zero_on"], "STORED_ZERO_SIDE_FAIL")
        require(
            content.get("strictly_positive_on") == expected["strictly_positive_on"],
            "STORED_POSITIVE_SIDE_FAIL",
        )
    zero_set = source if expected["zero_on"] == "source" else target
    positive_set = target if expected["strictly_positive_on"] == "target" else source
    distinguished = expected["distinguished_split"]
    if expected["invariant_kind"] == "I_singleton":
        require(zero_set == frozenset({distinguished}), "I_ZERO_SET_FAIL")
        require(bool(positive_set - {distinguished}), "I_POSITIVE_SET_FAIL")
    else:
        require(distinguished not in zero_set, "J_ZERO_SET_FAIL")
        require(distinguished in positive_set, "J_POSITIVE_SET_FAIL")
    return literal_binding(expected, semantics_formulas)


def historical_content(
    quartet: tuple[int, int, int, int],
    source: frozenset[tuple[tuple[int, int], tuple[int, int]]],
    target: frozenset[tuple[tuple[int, int], tuple[int, int]]],
) -> dict[str, Any]:
    witness = expected_witness(quartet, source, target)
    return {
        "distinguished_split": split_json(witness["distinguished_split"]),
        "invariant_kind": witness["invariant_kind"],
        "quartet": list(quartet),
        "reason": "displayed_quartet_mismatch",
        "source_displayed_splits": split_set_json(source),
        "strictly_positive_on": witness["strictly_positive_on"],
        "target_displayed_splits": split_set_json(target),
        "zero_on": witness["zero_on"],
    }


def compact_evidence(content: dict[str, Any]) -> dict[str, Any]:
    digest = sha_object(content)
    return {
        "kind": "exact_displayed_quartet_witness",
        "witness_id": f"Q:{digest}",
        "witness_payload_sha256": digest,
        "quartet": content["quartet"],
        "distinguished_split": content["distinguished_split"],
        "invariant_kind": content["invariant_kind"],
        "zero_on": content["zero_on"],
        "strictly_positive_on": content["strictly_positive_on"],
        "source_displayed_splits_sha256": sha_object(content["source_displayed_splits"]),
        "target_displayed_splits_sha256": sha_object(content["target_displayed_splits"]),
    }


def compact_candidates(quartet: tuple[int, int, int, int]) -> dict[str, dict[str, Any]]:
    splits = quartet_splits(quartet)
    displayed_sets = [
        frozenset(splits[index] for index in range(3) if mask >> index & 1)
        for mask in range(1, 8)
    ]
    result: dict[str, dict[str, Any]] = {}
    for source in displayed_sets:
        for target in displayed_sets:
            if source == target:
                continue
            content = historical_content(quartet, source, target)
            digest = sha_object(content)
            require(digest not in result, "COMPACT_CANDIDATE_HASH_COLLISION", quartet)
            result[digest] = content
    require(len(result) == 42, "COMPACT_CANDIDATE_CENSUS_FAIL", quartet)
    return result


def validate_compact_evidence(
    evidence: dict[str, Any],
    semantics_formulas: dict[str, list[list[Any]]],
    cache: dict[tuple[int, int, int, int], dict[str, dict[str, Any]]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    require(isinstance(evidence, dict), "COMPACT_EVIDENCE_NOT_OBJECT")
    quartet = normalize_quartet(evidence.get("quartet"))
    candidates = cache.setdefault(quartet, compact_candidates(quartet))
    digest = evidence.get("witness_payload_sha256")
    require(type(digest) is str and digest in candidates, "COMPACT_WITNESS_NOT_RESOLVED", digest)
    content = candidates[digest]
    require(evidence == compact_evidence(content), "COMPACT_EVIDENCE_BINDING_FAIL", evidence.get("witness_id"))
    binding = validate_content(content, semantics_formulas, require_stored_witness=True)
    return content, binding


def semantics_contract(
    path: Path, project: Path | None = None
) -> tuple[dict[str, list[list[Any]]], dict[str, Any]]:
    certificate = load_json(path)
    verify_payload(certificate, "SEMANTICS_CERTIFICATE_PAYLOAD_FAIL")
    require(certificate.get("schema") == "k2p-displayed-quartet-semantics-v2", "SEMANTICS_SCHEMA_FAIL")
    require(certificate.get("status") == "PASS", "SEMANTICS_STATUS_FAIL")
    require(certificate.get("character_order") == ["0", "C", "G", "T"], "SEMANTICS_CHARACTER_ORDER_FAIL")
    require(certificate.get("edge_spectrum") == ["1", "s", "g", "s"], "SEMANTICS_SPECTRUM_FAIL")
    require(certificate.get("equal_nonzero_sector") == ["C", "T"], "SEMANTICS_EQUAL_SECTOR_FAIL")
    require(certificate.get("canonical_formula_count") == 6, "SEMANTICS_CANONICAL_CENSUS_FAIL")
    require(certificate.get("formula_transport_count") == 288, "SEMANTICS_TRANSPORT_CENSUS_FAIL")
    require(certificate.get("displayed_set_count") == 7, "SEMANTICS_DISPLAYED_SET_CENSUS_FAIL")
    require(certificate.get("unequal_pair_count") == 21, "SEMANTICS_PAIR_CENSUS_FAIL")
    rows = certificate.get("canonical_formulas")
    require(isinstance(rows, dict) and set(rows) == {"F_A", "F_B", "F_C", "J_A", "J_B", "J_C"}, "SEMANTICS_FORMULA_CENSUS_FAIL")
    formulas: dict[str, list[list[Any]]] = {}
    for formula_id, row in rows.items():
        require(isinstance(row, dict) and isinstance(row.get("terms"), list), "SEMANTICS_FORMULA_ROW_FAIL")
        formula_payload = {
            "formula_id": formula_id,
            "terms": row["terms"],
            "pullbacks": row.get("pullbacks"),
        }
        require(
            row.get("formula_id") == formula_id
            and row.get("formula_sha256") == sha_object(formula_payload),
            "SEMANTICS_FORMULA_HASH_FAIL",
            formula_id,
        )
        formulas[formula_id] = row["terms"]
    display_path = str(path.relative_to(project)) if project is not None else str(path)
    summary = {
        "path": display_path,
        "sha256": sha_file(path),
        "payload_sha256": certificate["payload_sha256"],
        "spec_sha256": certificate.get("spec_sha256"),
        "canonical_formula_count": certificate.get("canonical_formula_count"),
        "formula_transport_count": certificate.get("formula_transport_count"),
    }
    return formulas, summary


def row_root_update(digest: Any, identity: Any, proof_id: str, binding_sha256: str) -> None:
    digest.update(canonical([identity, proof_id, binding_sha256]))
    digest.update(b"\n")


def registry_rows(
    bindings: dict[str, dict[str, Any]],
    references: collections.Counter[str],
) -> list[dict[str, Any]]:
    require(set(bindings) == set(references), "REGISTRY_REFERENCE_SET_FAIL", {
        "unused": sorted(set(bindings) - set(references))[:3],
        "missing": sorted(set(references) - set(bindings))[:3],
    })
    rows = []
    for proof_id in sorted(bindings):
        binding = bindings[proof_id]
        rows.append(
            {
                "proof_id": proof_id,
                "reference_count": references[proof_id],
                "binding_sha256": binding["binding_sha256"],
                "formula_id": binding["formula_id"],
                "invariant_kind": binding["invariant_kind"],
                "quartet": binding["quartet"],
                "distinguished_split": binding["distinguished_split"],
                "zero_on": binding["zero_on"],
                "strictly_positive_on": binding["strictly_positive_on"],
                "literal_coordinate_terms": binding["coordinate_terms"],
                "unlisted_leaf_characters": binding["unlisted_leaf_characters"],
                "zero_tree_splits": binding["zero_tree_splits"],
                "strictly_positive_tree_splits": binding["strictly_positive_tree_splits"],
                "strict_pullback": binding["strict_pullback"],
                "licensed_character_transport": binding["licensed_character_transport"],
            }
        )
    return rows


def layer_summary(
    *,
    project: Path,
    paths: list[Path],
    total_rows: Any,
    quartet_rows: int,
    bindings: dict[str, dict[str, Any]],
    references: collections.Counter[str],
    row_root: str,
) -> dict[str, Any]:
    rows = registry_rows(bindings, references)
    semantic_classes = {
        canonical(
            [
                row["quartet"],
                row["distinguished_split"],
                bindings[row["proof_id"]]["invariant_kind"],
                row["zero_on"],
                row["strictly_positive_on"],
            ]
        )
        for row in rows
    }
    formula_transports = {
        canonical([row["quartet"], row["distinguished_split"], row["formula_id"]])
        for row in rows
    }
    return {
        "inputs": {str(path.relative_to(project)): sha_file(path) for path in paths},
        "total_rows": total_rows,
        "quartet_terminal_rows": quartet_rows,
        "certificate_count": len(bindings),
        "semantic_class_count": len(semantic_classes),
        "literal_formula_transport_count": len(formula_transports),
        "proof_reference_multiplicity_root_sha256": sha_object(
            [[proof_id, references[proof_id]] for proof_id in sorted(references)]
        ),
        "row_binding_root_sha256": row_root,
        "certificate_bindings": rows,
    }


def audit_compact_layer(
    project: Path,
    relative: str,
    category: str,
    expected: dict[str, int],
    semantics_formulas: dict[str, list[list[Any]]],
) -> dict[str, Any]:
    path = project / relative
    require(path.is_file(), "COMPACT_LEDGER_MISSING", relative)
    total = 0
    quartet_count = 0
    references: collections.Counter[str] = collections.Counter()
    bindings: dict[str, dict[str, Any]] = {}
    evidence_rows: dict[str, dict[str, Any]] = {}
    cache: dict[tuple[int, int, int, int], dict[str, dict[str, Any]]] = {}
    root = hashlib.sha256()
    for row in iter_gzip_jsonl(path):
        require(isinstance(row, dict), "COMPACT_ROW_NOT_OBJECT", total)
        require(row.get("raw_id") == total, "COMPACT_RAW_ID_ORDER_FAIL", total)
        total += 1
        if row.get("corrected_category") != category:
            continue
        quartet_count += 1
        evidence = row.get("evidence_binding")
        require(isinstance(evidence, dict), "COMPACT_ROW_EVIDENCE_FAIL", row["raw_id"])
        proof_id = evidence.get("witness_id")
        require(type(proof_id) is str, "COMPACT_PROOF_ID_FAIL", row["raw_id"])
        previous = evidence_rows.get(proof_id)
        if previous is None:
            _content, binding = validate_compact_evidence(evidence, semantics_formulas, cache)
            evidence_rows[proof_id] = evidence
            bindings[proof_id] = binding
        else:
            require(evidence == previous, "COMPACT_PROOF_ID_DRIFT", proof_id)
            binding = bindings[proof_id]
        references[proof_id] += 1
        row_root_update(root, row["raw_id"], proof_id, binding["binding_sha256"])
    require(total == expected["rows"], "COMPACT_TOTAL_CENSUS_FAIL", total)
    require(quartet_count == expected["quartet"], "COMPACT_QUARTET_CENSUS_FAIL", quartet_count)
    require(len(bindings) == expected["certificates"], "COMPACT_CERTIFICATE_CENSUS_FAIL", len(bindings))
    return layer_summary(
        project=project, paths=[path], total_rows=total, quartet_rows=quartet_count,
        bindings=bindings, references=references, row_root=root.hexdigest(),
    )


def audited_registry(
    values: dict[str, Any],
    prefix: str,
    semantics_formulas: dict[str, list[list[Any]]],
    *,
    require_stored_witness: bool,
) -> dict[str, dict[str, Any]]:
    bindings: dict[str, dict[str, Any]] = {}
    for proof_id, content in values.items():
        require(type(proof_id) is str and isinstance(content, dict), "REGISTRY_ROW_SCHEMA_FAIL")
        expected_id = f"{prefix}{sha_object(content)}"
        require(proof_id == expected_id, "REGISTRY_CERTIFICATE_ID_FAIL", proof_id)
        bindings[proof_id] = validate_content(
            content, semantics_formulas, require_stored_witness=require_stored_witness
        )
    return bindings


def audit_theta2_restoration(project: Path, semantics_formulas: dict[str, list[list[Any]]]) -> dict[str, Any]:
    path = project / THETA2_RESTORATION
    payload = load_gzip_json(path)
    registry = payload.get("topology_witnesses")
    require(isinstance(registry, dict), "THETA2_RESTORATION_REGISTRY_FAIL")
    bindings = audited_registry(registry, "Q:", semantics_formulas, require_stored_witness=True)
    references: collections.Counter[str] = collections.Counter()
    root = hashlib.sha256()
    counts: dict[str, int] = {}
    for name, expected_rows, expected_quartet in (
        ("six_port_rows", EXPECTED["theta2_restoration"]["six_rows"], EXPECTED["theta2_restoration"]["six_quartet"]),
        ("seven_port_rows", EXPECTED["theta2_restoration"]["seven_rows"], EXPECTED["theta2_restoration"]["seven_quartet"]),
    ):
        rows = payload.get(name)
        require(isinstance(rows, list) and len(rows) == expected_rows, "THETA2_RESTORATION_ROW_CENSUS_FAIL", name)
        quartet_count = 0
        for index, row in enumerate(rows):
            require(isinstance(row, dict), "THETA2_RESTORATION_ROW_FAIL")
            if row.get("category") != "quartet_pointwise_excluded":
                continue
            quartet_count += 1
            proof_id = row.get("certificate_id")
            require(proof_id in bindings, "THETA2_RESTORATION_REFERENCE_FAIL", proof_id)
            references[proof_id] += 1
            row_root_update(root, [name, index, row.get("path_id")], proof_id, bindings[proof_id]["binding_sha256"])
        require(quartet_count == expected_quartet, "THETA2_RESTORATION_QUARTET_CENSUS_FAIL", name)
        counts[name] = len(rows)
    quartet_total = sum(references.values())
    require(quartet_total == EXPECTED["theta2_restoration"]["quartet"], "THETA2_RESTORATION_TOTAL_FAIL")
    require(len(bindings) == EXPECTED["theta2_restoration"]["certificates"], "THETA2_RESTORATION_CERTIFICATE_CENSUS_FAIL")
    return layer_summary(
        project=project, paths=[path], total_rows=counts, quartet_rows=quartet_total,
        bindings=bindings, references=references, row_root=root.hexdigest(),
    )


def audit_cycle(project: Path, semantics_formulas: dict[str, list[list[Any]]]) -> dict[str, Any]:
    ledger_path = project / CYCLE_LEDGER
    registry_path = project / CYCLE_REGISTRY
    payload = load_json(registry_path)
    witnesses = payload.get("witnesses")
    require(isinstance(witnesses, dict), "CYCLE_REGISTRY_FAIL")
    quartet = {
        proof_id: content for proof_id, content in witnesses.items()
        if isinstance(content, dict) and content.get("reason") == "displayed_quartet_mismatch"
    }
    bindings = audited_registry(quartet, "QW:", semantics_formulas, require_stored_witness=True)
    references: collections.Counter[str] = collections.Counter()
    root = hashlib.sha256()
    total = 0
    for row in iter_gzip_jsonl(ledger_path):
        require(row.get("raw_id") == total, "CYCLE_RAW_ID_ORDER_FAIL", total)
        total += 1
        if row.get("terminal_kind") != "displayed_quartet_strict_separator":
            continue
        proof_id = row.get("proof_certificate_id")
        require(proof_id in bindings, "CYCLE_REFERENCE_FAIL", proof_id)
        references[proof_id] += 1
        row_root_update(root, row["raw_id"], proof_id, bindings[proof_id]["binding_sha256"])
    require(total == EXPECTED["cycle"]["rows"], "CYCLE_TOTAL_CENSUS_FAIL", total)
    require(sum(references.values()) == EXPECTED["cycle"]["quartet"], "CYCLE_QUARTET_CENSUS_FAIL")
    require(len(bindings) == EXPECTED["cycle"]["certificates"], "CYCLE_CERTIFICATE_CENSUS_FAIL")
    return layer_summary(
        project=project, paths=[ledger_path, registry_path], total_rows=total,
        quartet_rows=sum(references.values()), bindings=bindings,
        references=references, row_root=root.hexdigest(),
    )


def audit_restoration(project: Path, semantics_formulas: dict[str, list[list[Any]]]) -> dict[str, Any]:
    path = project / RESTORATION_FOREST
    payload = load_json(path)
    registry = payload.get("quartet_certificates")
    require(isinstance(registry, dict), "RESTORATION_REGISTRY_FAIL")
    bindings = audited_registry(registry, "", semantics_formulas, require_stored_witness=False)
    references: collections.Counter[str] = collections.Counter()
    root = hashlib.sha256()
    total_rows: dict[str, int] = {}
    for name, expected_rows, expected_quartet in (
        ("first_coverage", EXPECTED["restoration"]["first_rows"], EXPECTED["restoration"]["first_quartet"]),
        ("second_coverage", EXPECTED["restoration"]["second_rows"], EXPECTED["restoration"]["second_quartet"]),
    ):
        rows = payload.get(name)
        require(isinstance(rows, list) and len(rows) == expected_rows, "RESTORATION_ROW_CENSUS_FAIL", name)
        quartet_count = 0
        for index, row in enumerate(rows):
            if row.get("proof") != "displayed_quartet_mismatch":
                continue
            quartet_count += 1
            proof_id = row.get("certificate_sha256")
            require(proof_id in bindings, "RESTORATION_REFERENCE_FAIL", proof_id)
            references[proof_id] += 1
            row_root_update(root, [name, index, row.get("root_id")], proof_id, bindings[proof_id]["binding_sha256"])
        require(quartet_count == expected_quartet, "RESTORATION_QUARTET_CENSUS_FAIL", name)
        total_rows[name] = len(rows)
    require(sum(references.values()) == EXPECTED["restoration"]["quartet"], "RESTORATION_TOTAL_FAIL")
    require(len(bindings) == EXPECTED["restoration"]["certificates"], "RESTORATION_CERTIFICATE_CENSUS_FAIL")
    return layer_summary(
        project=project, paths=[path], total_rows=total_rows, quartet_rows=sum(references.values()),
        bindings=bindings, references=references, row_root=root.hexdigest(),
    )


def audit_probe(project: Path, semantics_formulas: dict[str, list[list[Any]]]) -> dict[str, Any]:
    registry_path = project / PROBE_REGISTRY
    payload = load_gzip_json(registry_path)
    registry = payload.get("separation_proof_registry")
    require(isinstance(registry, dict), "PROBE_REGISTRY_FAIL")
    bindings = audited_registry(registry, "Q:", semantics_formulas, require_stored_witness=False)
    references: collections.Counter[str] = collections.Counter()
    root = hashlib.sha256()
    total_rows: dict[str, int] = {}
    paths = [project / PROBE_ONE, project / PROBE_TWO]
    for stage, path, expected_rows, expected_quartet in (
        ("one_port", paths[0], EXPECTED["probe"]["one_rows"], EXPECTED["probe"]["one_quartet"]),
        ("two_port", paths[1], EXPECTED["probe"]["two_rows"], EXPECTED["probe"]["two_quartet"]),
    ):
        total = 0
        quartet_count = 0
        for row in iter_gzip_jsonl(path):
            total += 1
            if row.get("status") != "displayed_quartet_mismatch":
                continue
            quartet_count += 1
            proof_id = row.get("proof_id")
            require(proof_id in bindings, "PROBE_REFERENCE_FAIL", proof_id)
            references[proof_id] += 1
            identity = [stage, total - 1, row.get("parent_anchor_id", row.get("base_anchor_id"))]
            row_root_update(root, identity, proof_id, bindings[proof_id]["binding_sha256"])
        require(total == expected_rows, "PROBE_ROW_CENSUS_FAIL", stage)
        require(quartet_count == expected_quartet, "PROBE_QUARTET_CENSUS_FAIL", stage)
        total_rows[stage] = total
    require(sum(references.values()) == EXPECTED["probe"]["quartet"], "PROBE_TOTAL_FAIL")
    require(len(bindings) == EXPECTED["probe"]["certificates"], "PROBE_CERTIFICATE_CENSUS_FAIL")
    return layer_summary(
        project=project, paths=[*paths, registry_path], total_rows=total_rows,
        quartet_rows=sum(references.values()), bindings=bindings,
        references=references, row_root=root.hexdigest(),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--semantics-certificate", type=Path, default=DEFAULT_SEMANTICS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    project = args.project.resolve()
    semantics_path = args.semantics_certificate.resolve()
    output = args.output.resolve() if args.output else HERE / "quartet_terminal_binding_certificate.json"
    # A caller-owned explicit output is fail-closed.  The implicit canonical
    # destination is not removed by a diagnostic-only ``-O`` invocation.
    if args.output is not None:
        output.unlink(missing_ok=True)
    if not __debug__:
        raise SystemExit("QUARTET_TERMINAL_BINDING_OPTIMIZED_MODE_FORBIDDEN")
    formulas, semantics = semantics_contract(semantics_path, project)

    layers = {
        "raw4": audit_compact_layer(
            project, RAW4_LEDGER, "displayed_quartet_exclusion", EXPECTED["raw4"], formulas
        ),
        "theta2": audit_compact_layer(
            project, THETA2_LEDGER, "displayed_quartet_exclusion", EXPECTED["theta2"], formulas
        ),
        "theta2_restoration": audit_theta2_restoration(project, formulas),
        "cycle": audit_cycle(project, formulas),
        "restoration": audit_restoration(project, formulas),
        "probe": audit_probe(project, formulas),
    }
    total_terminals = sum(layer["quartet_terminal_rows"] for layer in layers.values())
    total_certificates = sum(layer["certificate_count"] for layer in layers.values())
    require(total_terminals == 4_414_710, "AGGREGATE_TERMINAL_CENSUS_FAIL", total_terminals)
    require(total_certificates == 888, "AGGREGATE_CERTIFICATE_CENSUS_FAIL", total_certificates)
    payload = {
        "schema": "k2p-quartet-terminal-binding-v1",
        "status": "PASS",
        "claim_boundary": (
            "This certificate binds committed displayed-split witnesses to literal "
            "Fourier bodies. Separate graph-derived producer/replayers bind each "
            "row to its committed displayed-split witness."
        ),
        "imports_graph_or_classifier_code": False,
        "coordinate_convention": {
            "character_order": ["0", "C", "G", "T"],
            "edge_spectrum": ["1", "s", "g", "s"],
            "equal_nonzero_sector": ["C", "T"],
            "singleton_nonzero_sector": ["G"],
            "unlisted_marginal_leaf_characters": "0",
        },
        "semantics_certificate": semantics,
        "layers": layers,
        "aggregate": {
            "layer_count": len(layers),
            "quartet_terminal_rows": total_terminals,
            "per_layer_certificate_ids": total_certificates,
            "all_registry_certificates_used": True,
            "missing_references": 0,
            "dangling_certificates": 0,
            "aggregate_layer_binding_root_sha256": sha_object(
                [
                    [name, layer["row_binding_root_sha256"], layer["proof_reference_multiplicity_root_sha256"]]
                    for name, layer in sorted(layers.items())
                ]
            ),
        },
    }
    certificate = dict(payload)
    certificate["payload_sha256"] = sha_object(payload)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("K2P_QUARTET_TERMINAL_BINDING_PASS")
    print(
        json.dumps(
            {
                "quartet_terminal_rows": total_terminals,
                "per_layer_certificate_ids": total_certificates,
                "payload_sha256": certificate["payload_sha256"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except (
        QuartetTerminalFailure,
        KeyError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        print(f"QUARTET_TERMINAL_BINDING_FAIL:{exc}", file=sys.stderr)
        raise SystemExit(1)

#!/usr/bin/env python3
"""Minimal independent fail-closed verifier for the PC-PARTIAL package."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent

SOURCE_PATHS = {
    "baseline": "analysis/PROOF_COMPRESSION_BASELINE.json",
    "equivalence": "analysis/FAMILY_COVERAGE_EQUIVALENCE_CERTIFICATE.json",
    "templates": "templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.json",
    "restoration": "restoration/RESTORATION_ARCHETYPES.json",
    "restoration_verification": "restoration/RESTORATION_ARCHETYPE_VERIFICATION.json",
    "probe": "probe/PROBE_WORD_COVERAGE.json",
    "crosswalk": "THEOREM_TO_TEMPLATE_CROSSWALK.json",
    "result": "PROOF_COMPRESSION_RESULT.json",
}

EXPECTED_PAYLOADS = {
    "baseline": "b22284177292c089a590245c552f59d07a57a0b30929243bc1ed73cdf7c3f8ff",
    "equivalence": "79571b077bb9f11bc2cdee4a21a81142d0d49d1d6f9a5c03196d09bb7297e72b",
    "templates": "859bfc969beeb885a3c7dae13c05d3bb785ea1fb0796eede508bc3625374ab91",
    "restoration": "9ae885812123fb975055a5f388e6d55c4599ee2350b58bd40e5797fe1fffe6e5",
    "restoration_verification": "2ad921d8dd1928750261a843717520d9e8cae1aa0afd79477afa15a7efa22d60",
    "probe": "54928da10e5fe56c68c8e07edf706e1a20deff8ad8f9fbc82d0948e67aa849cb",
    "crosswalk": "d2591c67eb5168b6601efa81b762e905239accd26acf69fe284f1b690de1d480",
    "result": "9bcac0f0d8d645393c456807d05eb27bf9a3fce068fa7c8c18f399c18cf993fa",
}

EXPECTED_SCHEMAS = {
    "baseline": "k2p-proof-compression-baseline-v1",
    "equivalence": "k2p-pc-partial-family-coverage-equivalence-v1",
    "templates": "k2p-direct-certificate-template-table-v1",
    "restoration": "k2p-restoration-descriptive-archetypes-v1",
    "restoration_verification": "k2p-restoration-archetype-verification-v1",
    "probe": "k2p-probe-word-theorem-coverage-v1",
    "crosswalk": "k2p-pc-partial-theorem-template-crosswalk-v1",
    "result": "k2p-principal-d-plus-proof-compression-result-v1",
}

RAW4_CATEGORIES = {
    "direct_terminal_presentation": 1472,
    "displayed_quartet_exclusion": 360408,
    "exact_rank_exclusion": 23822,
    "full_map_Ti_strict_sign": 16974,
    "restoration_member_presentation": 2540,
}
THETA2_CATEGORIES = {
    "direct_quadratic_separator": 240,
    "displayed_quartet_exclusion": 2942592,
    "exact_rank_exclusion": 800,
    "full_map_Ti_strict_sign": 2528,
    "labelled_isomorphism": 80,
}
DIRECT_TERMINALS = {
    "direct_hard_case_F2_F3_F4": 4,
    "exact_direct_polynomial_separator": 36,
    "exact_mixed_graph_isomorphism": 20,
    "exact_multihomogeneous_quadratic": 839,
    "ordinary_triangle_quotient": 35,
}
DIRECT36_FAMILIES = {
    "lower_theta_quartic": 12,
    "theta0_quintic_port_orbit": 22,
    "theta3_cubic": 2,
}
RESTORATION_CENSUS = {
    "canonical_parents": 997,
    "descriptive_archetypes": 297,
    "final_leaves": 36792,
    "first_children": 36568,
    "forest_edges": 36824,
    "max_depth": 2,
    "member_roots": 2540,
    "second_children": 256,
    "unresolved": 0,
}
RESTORATION_FIRST = {
    "displayed_quartet_mismatch": 35758,
    "exact_multihomogeneous_quadratic": 148,
    "full_map_Ti_zero_strict_sign": 606,
    "inherited_exact_F_2_112_quartic": 24,
    "restore_remaining_physical_role": 32,
}
RESTORATION_SECOND = {
    "displayed_quartet_mismatch": 248,
    "full_map_Ti_zero_strict_sign": 8,
}
PROBE_ONE = {
    "displayed_quartet_mismatch": 27758,
    "full_map_Ti_strict_sign": 99,
    "isomorphic": 1915,
    "triangle": 192,
}
PROBE_TWO = {
    "displayed_quartet_mismatch": 511266,
    "full_map_Ti_strict_sign": 576,
    "isomorphic": 30969,
    "triangle": 1760,
}


class VerificationFailure(RuntimeError):
    pass


def need(condition: bool, code: str, detail: Any | None = None) -> None:
    if not condition:
        raise VerificationFailure(code if detail is None else f"{code}:{detail}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_seal(value: dict[str, Any], code: str) -> None:
    observed = value.get("payload_sha256")
    need(isinstance(observed, str), f"{code}_PAYLOAD_MISSING")
    payload = dict(value)
    payload.pop("payload_sha256", None)
    need(observed == object_sha(payload), f"{code}_PAYLOAD_SEAL")


def safe_path(relative: str) -> Path:
    requested = Path(relative)
    need(not requested.is_absolute() and ".." not in requested.parts, "PATH_ESCAPE", relative)
    path = ROOT / requested
    need(path.resolve().is_relative_to(ROOT.resolve()), "PATH_ESCAPE", relative)
    need(path.is_file() and not path.is_symlink(), "FILE_MISSING_OR_SYMLINK", relative)
    return path


def load_bundle() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for name, relative in SOURCE_PATHS.items():
        path = safe_path(relative)
        value = json.loads(path.read_text(encoding="utf-8"))
        need(isinstance(value, dict), "JSON_NOT_OBJECT", relative)
        result[name] = value
    return result


def exact_dict(observed: Any, expected: dict[str, int], code: str) -> None:
    need(isinstance(observed, dict), code)
    need(observed == expected, code, observed)


def verify_file_bindings(bundle: dict[str, dict[str, Any]]) -> None:
    result = bundle["result"]
    bindings = result.get("artifact_bindings")
    need(isinstance(bindings, dict), "ARTIFACT_BINDINGS")
    machine = bindings.get("machine_readable")
    prose = bindings.get("prose")
    need(isinstance(machine, list) and isinstance(prose, list), "ARTIFACT_BINDING_LISTS")
    expected_machine_paths = set(SOURCE_PATHS.values()) - {"PROOF_COMPRESSION_RESULT.json"}
    observed_machine_paths = [row.get("path") for row in machine if isinstance(row, dict)]
    need(len(observed_machine_paths) == len(set(observed_machine_paths)), "DUPLICATE_MACHINE_BINDING")
    need(set(observed_machine_paths) == expected_machine_paths, "MACHINE_BINDING_PATHS")
    reverse = {relative: name for name, relative in SOURCE_PATHS.items()}
    for row in machine:
        need(isinstance(row, dict), "MACHINE_BINDING_ROW")
        relative = row["path"]
        path = safe_path(relative)
        need(row.get("bytes") == path.stat().st_size, "MACHINE_BINDING_BYTES", relative)
        need(row.get("sha256") == file_sha(path), "MACHINE_BINDING_SHA", relative)
        need(
            row.get("payload_sha256") == bundle[reverse[relative]].get("payload_sha256"),
            "MACHINE_BINDING_PAYLOAD",
            relative,
        )
    observed_prose_paths = [row.get("path") for row in prose if isinstance(row, dict)]
    need(len(observed_prose_paths) == len(set(observed_prose_paths)), "DUPLICATE_PROSE_BINDING")
    need(
        set(observed_prose_paths)
        == {
            "analysis/PROOF_COMPRESSION_BASELINE.md",
            "analysis/FINITE_UNIVERSE_COMPLETENESS.md",
            "templates/DIRECT_CERTIFICATE_TEMPLATE_TABLE.md",
            "restoration/RESTORATION_ARCHETYPES.md",
            "probe/PROBE_WORD_THEOREM.md",
            "COMPRESSED_BOUNDED_THEOREM.md",
            "THEOREM_TO_TEMPLATE_CROSSWALK.md",
        },
        "PROSE_BINDING_PATHS",
    )
    for row in prose:
        need(isinstance(row, dict), "PROSE_BINDING_ROW")
        path = safe_path(row["path"])
        need(row.get("bytes") == path.stat().st_size, "PROSE_BINDING_BYTES", row["path"])
        need(row.get("sha256") == file_sha(path), "PROSE_BINDING_SHA", row["path"])


def verify_frozen_lock() -> None:
    path = PROJECT / "work/final_theorem_release/RELEASE_LOCK.json"
    need(path.is_file() and not path.is_symlink(), "FROZEN_LOCK_MISSING")
    need(
        file_sha(path) == "4a084871be2fe212559e3a38306c73deb4ba111e5900e61b680a6db81f0e88fb",
        "FROZEN_LOCK_SHA",
    )
    value = json.loads(path.read_text(encoding="utf-8"))
    need(isinstance(value, dict), "FROZEN_LOCK_NOT_OBJECT")
    verify_seal(value, "FROZEN_LOCK")
    need(
        value.get("payload_sha256")
        == "d95fc7d6ef2b44c9c67be6394d5cf226b04bb3335be507e11da9a6a595e5c75f",
        "FROZEN_LOCK_PAYLOAD",
    )
    need(value.get("candidate_outcome") == "K2P-SAME", "FROZEN_OUTCOME")
    need(value.get("promotion_ready") is True, "FROZEN_NOT_READY")
    need(value.get("blockers") == [] and value.get("missing_required_files") == [], "FROZEN_GAPS")


def verify_bundle(
    bundle: dict[str, dict[str, Any]],
    *,
    enforce_expected_payloads: bool = True,
    verify_files: bool = True,
) -> None:
    need(set(bundle) == set(SOURCE_PATHS), "BUNDLE_KEYS")
    for name, value in bundle.items():
        need(isinstance(value, dict), "BUNDLE_VALUE", name)
        verify_seal(value, name.upper())
        need(value.get("schema") == EXPECTED_SCHEMAS[name], "SCHEMA", name)
        if enforce_expected_payloads:
            need(value.get("payload_sha256") == EXPECTED_PAYLOADS[name], "EXPECTED_PAYLOAD", name)

    baseline = bundle["baseline"]
    equivalence = bundle["equivalence"]
    templates = bundle["templates"]
    restoration = bundle["restoration"]
    restoration_verification = bundle["restoration_verification"]
    probe = bundle["probe"]
    crosswalk = bundle["crosswalk"]
    result = bundle["result"]

    need(baseline.get("status") == "PASS", "BASELINE_STATUS")
    raw4 = baseline["finite_universes"]["raw4"]
    need(raw4.get("rows") == 405216, "RAW4_ROWS")
    exact_dict(raw4.get("category_counts"), RAW4_CATEGORIES, "RAW4_CATEGORY_CENSUS")
    need(sum(raw4["category_counts"].values()) == raw4["rows"], "RAW4_PARTITION_SUM")
    theta2 = baseline["finite_universes"]["theta2"]
    need(theta2.get("rows") == 2946240, "THETA2_ROWS")
    exact_dict(theta2.get("category_counts"), THETA2_CATEGORIES, "THETA2_CATEGORY_CENSUS")
    need(sum(theta2["category_counts"].values()) == theta2["rows"], "THETA2_PARTITION_SUM")
    need(baseline["finite_universes"]["cycle"].get("base_rows") == 13440, "CYCLE_BASE_ROWS")
    finite_cases = {
        name: row["total"]
        for name, row in baseline["finite_universes"]["completion_formula_cases"].items()
    }
    need(
        finite_cases
        == {
            "five_port_marginalized_incoming": 4155,
            "five_port_selected_incoming": 1983,
            "four_port_marginalized_incoming": 1983,
            "four_port_selected_incoming": 831,
            "three_port_marginalized_incoming": 831,
            "three_port_selected_incoming": 289,
        },
        "FINITE_FORMULA_CASES",
    )
    need(6 * (831 + 1983) * 24 == 405216, "RAW4_FORMULA")
    need(4 * (1983 + 4155) * 120 == 2946240, "THETA2_FORMULA")
    need(2 * (289 + 831) * 6 == 13440, "CYCLE_FORMULA")
    need(
        baseline["rank_upper"].get("descriptors") == 4379
        and baseline["rank_upper"].get("base_ansatz_descriptors") == 3515
        and baseline["rank_upper"].get("exceptional_descriptors") == 864
        and baseline["rank_upper"].get("exceptional_representatives") == 75,
        "RANK_EXCEPTION_CENSUS",
    )

    need(equivalence.get("status") == "PASS", "EQUIVALENCE_STATUS")
    exact_dict(equivalence.get("raw4_categories"), RAW4_CATEGORIES, "EQUIVALENCE_RAW4")
    exact_dict(equivalence.get("theta2_categories"), THETA2_CATEGORIES, "EQUIVALENCE_THETA2")
    need(equivalence["finite_formula_cases"] == finite_cases, "EQUIVALENCE_FORMULA_CASES")
    need(equivalence["restoration"].get("canonical_parents") == 997, "EQUIVALENCE_RESTORATION")
    need(equivalence["restoration"].get("edges") == 36824, "EQUIVALENCE_RESTORATION_EDGES")

    need(templates.get("status") == "PASS", "TEMPLATE_STATUS")
    need(templates["raw4"].get("canonical_terminal_classes") == 934, "TERMINAL_CLASS_CENSUS")
    exact_dict(templates["raw4"].get("terminal_kind_class_counts"), DIRECT_TERMINALS, "TERMINAL_KIND_CENSUS")
    need(sum(templates["raw4"]["terminal_kind_class_counts"].values()) == 934, "TERMINAL_PARTITION_SUM")
    need(templates["raw4"].get("quadratic_literal_template_count") == 8, "RAW4_TEMPLATE_COUNT")
    need(templates["theta2"].get("quadratic_literal_template_count") == 4, "THETA2_TEMPLATE_COUNT")
    need(templates["cycle"].get("quadratic_literal_template_count") == 6, "CYCLE_TEMPLATE_COUNT")
    need(templates["restoration"].get("quadratic_literal_template_count") == 5, "RESTORATION_TEMPLATE_COUNT")
    direct36 = templates["direct36"]
    exact_dict(direct36.get("family_record_counts"), DIRECT36_FAMILIES, "DIRECT36_FAMILY_COUNTS")
    need(sum(direct36["family_record_counts"].values()) == 36, "DIRECT36_FAMILY_SUM")
    need(direct36.get("mathematical_family_count") == 3, "DIRECT36_PROPOSITION_FAMILIES")
    need(direct36.get("directional_transported_literal_body_count") == 27, "DIRECT36_LITERAL_BODIES")
    need(direct36.get("base_formula_count") == 5, "DIRECT36_BASE_COUNT")
    base = direct36["base_formulas"]
    need(base["theta0_quintic"].get("degree") == 5, "DIRECT36_QUINTIC_DEGREE")
    need(base["theta3_cubic"].get("degree") == 3, "DIRECT36_CUBIC_DEGREE")
    quartics = base["lower_theta_quartics"]
    need(quartics.get("degree") == 4, "DIRECT36_QUARTIC_DEGREE")
    need(
        len(quartics.get("base_certificates", [])) == 3
        and all(row.get("degree") == 4 for row in quartics["base_certificates"]),
        "DIRECT36_QUARTIC_BASES",
    )

    need(restoration.get("status") == "PC-PARTIAL", "RESTORATION_STATUS")
    observed_restoration_census = restoration.get("census")
    need(isinstance(observed_restoration_census, dict), "RESTORATION_CENSUS")
    need(
        {key: observed_restoration_census.get(key) for key in RESTORATION_CENSUS}
        == RESTORATION_CENSUS,
        "RESTORATION_CENSUS",
        observed_restoration_census,
    )
    need(
        observed_restoration_census.get("archetype_parent_multiplicity")
        == {"1": 154, "2": 72, "4": 38, "7": 1, "12": 4, "14": 9, "18": 15, "24": 4},
        "RESTORATION_ARCHETYPE_MULTIPLICITY",
    )
    exact_dict(restoration["proof_mechanisms"].get("first_layer"), RESTORATION_FIRST, "RESTORATION_FIRST_CENSUS")
    exact_dict(restoration["proof_mechanisms"].get("second_layer"), RESTORATION_SECOND, "RESTORATION_SECOND_CENSUS")
    need(sum(RESTORATION_FIRST.values()) == 36568, "RESTORATION_FIRST_SUM")
    need(sum(RESTORATION_SECOND.values()) == 256, "RESTORATION_SECOND_SUM")
    need(restoration["coverage"].get("every_parent_exactly_once") is True, "RESTORATION_PARENT_COVERAGE")
    need(restoration["coverage"].get("every_member_root_exactly_once") is True, "RESTORATION_ROOT_COVERAGE")
    need(restoration["coverage"].get("every_child_edge_counted") is True, "RESTORATION_EDGE_COVERAGE")
    need(
        restoration["coverage"].get("canonical_parent_assignment_sha256")
        == "486eb27f9b0f98409366c1971738092037b5a461f7b4611213f0bcac9a1c9620",
        "RESTORATION_PARENT_ASSIGNMENT_ROOT",
    )
    residue = restoration["compression_verdict"]["exact_residue"]
    need(
        residue
        == {
            "algebra_transport_certificate_classes": 16,
            "canonical_parent_assignments": 997,
            "member_root_presentations": 2540,
            "parent_child_edges": 36824,
        },
        "RESTORATION_EXACT_RESIDUE",
    )
    need(restoration["compression_verdict"].get("exact_transport_quotient_count") is None, "FALSE_RESTORATION_QUOTIENT")
    need(restoration_verification.get("status") == "PASS", "RESTORATION_VERIFY_STATUS")
    need(restoration_verification.get("deterministic_replay_equal") is True, "RESTORATION_REPLAY")
    need(restoration_verification.get("optimized_mode_rejected") is True, "RESTORATION_OPTIMIZED_GATE")
    need(restoration_verification["coverage"].get("unassigned_parents") == 0, "RESTORATION_UNASSIGNED")
    need(restoration_verification["coverage"].get("multiply_assigned_parents") == 0, "RESTORATION_DUPLICATE_PARENT")
    need(restoration_verification["coverage"].get("orphan_second_rows") == 0, "RESTORATION_ORPHAN")

    need(probe.get("status") == "PASS" and probe.get("compression_status") == "PC-PARTIAL", "PROBE_STATUS")
    need(probe["primitive_anchor_coverage"].get("anchor_records") == 176, "PROBE_ANCHORS")
    exact_dict(probe["one_port"].get("counts"), PROBE_ONE, "PROBE_ONE_CENSUS")
    need(probe["one_port"].get("raw_pairs") == 29964, "PROBE_ONE_ROWS")
    need(sum(PROBE_ONE.values()) == 29964, "PROBE_ONE_SUM")
    exact_dict(probe["two_port"].get("counts"), PROBE_TWO, "PROBE_TWO_CENSUS")
    need(probe["two_port"].get("raw_pairs") == 544571, "PROBE_TWO_ROWS")
    need(sum(PROBE_TWO.values()) == 544571, "PROBE_TWO_SUM")
    transport = probe["transport_coherence"]
    need(transport.get("exact_transport_records") == 67741, "PROBE_TRANSPORT_CENSUS")
    need(transport.get("parent_restriction_records") == 4379, "PROBE_RESTRICTION_CENSUS")
    need(
        all(
            transport.get(key) == 0
            for key in (
                "incoherent",
                "missing_exact_transports",
                "missing_parent_restrictions",
                "unreferenced_exact_transports",
                "unreferenced_parent_restrictions",
            )
        ),
        "PROBE_TRANSPORT_GAPS",
    )
    need(probe["two_port"].get("reversed_marginals_checked") == 32729, "PROBE_REVERSE_CHECKS")
    need(probe["two_port"].get("reversed_marginals_missing") == 0, "PROBE_REVERSE_MISSING")
    need(probe["compression_verdict"]["ledger_residue"] == {
        "anchors": 176,
        "exact_transports": 67741,
        "one_port_rows": 29964,
        "parent_restrictions": 4379,
        "two_port_rows": 544571,
    }, "PROBE_EXACT_RESIDUE")

    need(crosswalk.get("status") == "PASS", "CROSSWALK_STATUS")
    rows = crosswalk.get("rows")
    need(isinstance(rows, list) and len(rows) == 6, "CROSSWALK_ROWS")
    need([row.get("theorem_id") for row in rows] == [f"CBT-{i}" for i in range(1, 7)], "CROSSWALK_IDS")
    need(all(row.get("claim") and row.get("templates") and row.get("evidence") and row.get("residue") and row.get("status") for row in rows), "CROSSWALK_COMPLETENESS")

    need(result.get("status") == "PC-PARTIAL", "RESULT_STATUS")
    need(result["frozen_theorem"].get("outcome") == "K2P-SAME", "RESULT_FROZEN_OUTCOME")
    need(result["frozen_theorem"].get("modified_or_superseded") is False, "RESULT_FROZEN_MUTATION")
    need(result["bounded_census"] == {
        "cycle_base_directions": 13440,
        "probe_two_port_rows": 544571,
        "raw4_directions": 405216,
        "restoration_edges": 36824,
        "restoration_parents": 997,
        "terminal_classes": 934,
        "theta2_directions": 2946240,
        "unresolved_mathematical_records": 0,
    }, "RESULT_BOUNDED_CENSUS")
    need(result["logical_boundaries"] == {
        "ordinary_triangle_is_graph_common_germ_not_polynomial_symmetry": True,
        "restoration_297_is_exact_transport_quotient": False,
        "source_target_reversal_used": False,
        "uncertified_symmetry_used": False,
        "unresolved_compression_obligations": 3,
        "unresolved_mathematical_records": 0,
    }, "RESULT_LOGICAL_BOUNDARY")
    need(result.get("irreducible_exact_ledgers", {}).get("restoration") == residue, "RESULT_RESTORATION_RESIDUE")
    need(result.get("irreducible_exact_ledgers", {}).get("probe") == probe["compression_verdict"]["ledger_residue"], "RESULT_PROBE_RESIDUE")
    need(result.get("equivalence_payload_sha256") == equivalence.get("payload_sha256"), "RESULT_EQUIVALENCE_BINDING")

    if verify_files:
        verify_file_bindings(bundle)
        verify_frozen_lock()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify without writing")
    return parser.parse_args()


def main() -> int:
    parse_args()
    need(__debug__ and sys.flags.optimize == 0, "OPTIMIZED_PYTHON_FORBIDDEN")
    bundle = load_bundle()
    verify_bundle(bundle)
    print(
        json.dumps(
            {
                "compression_status": "PC-PARTIAL",
                "crosswalk_payload_sha256": EXPECTED_PAYLOADS["crosswalk"],
                "result_payload_sha256": EXPECTED_PAYLOADS["result"],
                "status": "PASS",
                "unresolved_mathematical_records": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationFailure as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True))
        raise SystemExit(1)

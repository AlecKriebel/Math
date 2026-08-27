#!/usr/bin/env python3
"""Derive the PC-PARTIAL baseline and finite-universe count lemma."""

from __future__ import annotations

import argparse
import ast
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any

from compression_common import (
    HERE,
    PROJECT,
    input_binding,
    load_json,
    noncomment_sloc,
    project_path,
    reject_optimized_python,
    require,
    sealed,
    sha_file,
    sha_object,
    write_json,
    write_text,
)


BASELINE_JSON = HERE / "PROOF_COMPRESSION_BASELINE.json"
BASELINE_MD = HERE / "PROOF_COMPRESSION_BASELINE.md"
UNIVERSE_MD = HERE / "FINITE_UNIVERSE_COMPLETENESS.md"

RELEASE_LOCK = "work/final_theorem_release/RELEASE_LOCK.json"
RELEASE_LOCK_SHA256 = "30132af1b10f7aba6d49ababf14551f9f914a19dc6a0638517761b6b85cf4c8d"
RELEASE_LOCK_PAYLOAD_SHA256 = (
    "a32e7f04d5c979fc1f9e268ca8a791ae24ad99b296f3e3c72682a3beadadd653"
)
RELEASE_LOCK_SCHEMA = "k2p-principal-d-plus-final-theorem-release-lock-v1"
ATLAS = "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
EXPECTED_PRIMITIVE_GRAMMAR_SHA256 = (
    "d5e7608f70a2243df605dee6e35d0ea6af74e4e47b42142e91ddfa4cbcbad09b"
)


INFRASTRUCTURE_MODULES = {
    "package/referee/k2p_offline_sweep_portable/build_direct_closure_lock.py",
    "package/referee/k2p_offline_sweep_portable/compare_semantic_runs.py",
    "package/referee/k2p_offline_sweep_portable/guarded_run.py",
    "package/referee/k2p_offline_sweep_portable/merge_manifests.py",
    "package/referee/k2p_offline_sweep_portable/verify_direct_closure_release.py",
    "package/referee/k2p_offline_sweep_portable/verify_package.py",
    "work/corrected_composite_ledgers/validate_release_contract.py",
    "work/final_theorem_release/build_release_lock.py",
    "work/final_theorem_release/release_common.py",
    "work/final_theorem_release/verify_final_theorem_release.py",
    "work/global_theorem_closure/promotion_manuscript/verify_promotion_gate.py",
    "work/probe_coherence_corrected/reseal_probe_certificate.py",
    "work/rank_upper_certificates/build_manifest.py",
}


EXPLICIT_INDEPENDENT_MODULES = {
    "package/referee/k2p_offline_sweep_portable/proofs/verify_theta_quartic_obstructions_independent.py",
    "work/adversarial_proof_review/audit_cycle_tree_sunlet_full_map.py",
    "work/adversarial_proof_review/audit_raw4_tree_sunlet_full_map.py",
    "work/adversarial_proof_review/audit_theta2_tree_sunlet_full_map.py",
    "work/adversarial_proof_review/verify_cycle_whole_map_independent.py",
    "work/corrected_composite_ledgers/verify_corrected_composites_independent.py",
    "work/final_theorem_release/verify_composite_reseal_diff.py",
    "work/final_theorem_release/verify_corrected_universe_independent.py",
    "work/final_theorem_release/verify_full_map_reseal.py",
    "work/global_proof_adversary/probe_full_audit/independent_probe_graph_audit.py",
    "work/global_proof_adversary/verify_component_scales.py",
    "work/theta2_sign_reclassification/verify_theta2_full_map_independent.py",
    "work/weak_sharpness_audit/audit_weak_sharpness.py",
}


EXPECTED_CORES = {
    "cycle": {
        "arcs": (("S", "X"), ("S", "X")),
        "retics": ("X",),
        "sinks": ("X",),
        "repairs": ((0,), (1,)),
    },
    "theta0": {
        "arcs": (("S", "U"), ("S", "V"), ("U", "X"), ("V", "X"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (3, 4)),
    },
    "theta1": {
        "arcs": (("S", "U"), ("S", "X"), ("V", "X"), ("U", "V"), ("U", "V")),
        "retics": ("V", "X"),
        "sinks": ("X",),
        "repairs": ((2, 3), (2, 4)),
    },
    "theta2": {
        "arcs": (
            ("S", "U"),
            ("S", "V"),
            ("U", "X0"),
            ("V", "X0"),
            ("U", "X1"),
            ("V", "X1"),
        ),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2, 3), (2, 5), (3, 4), (4, 5)),
    },
    "theta3": {
        "arcs": (
            ("S", "U"),
            ("S", "X0"),
            ("V", "X0"),
            ("U", "X1"),
            ("V", "X1"),
            ("U", "V"),
        ),
        "retics": ("X0", "X1"),
        "sinks": ("X0", "X1"),
        "repairs": ((2,), (4,)),
    },
}


def release_anchor() -> dict[str, Any]:
    path = project_path(RELEASE_LOCK)
    require(sha_file(path) == RELEASE_LOCK_SHA256, "IMMUTABLE_RELEASE_LOCK_SHA256")
    value = load_json(path)
    require(value.get("schema") == RELEASE_LOCK_SCHEMA, "RELEASE_LOCK_SCHEMA")
    require(
        value.get("payload_sha256") == RELEASE_LOCK_PAYLOAD_SHA256,
        "IMMUTABLE_RELEASE_LOCK_PAYLOAD",
    )
    payload = dict(value)
    payload.pop("payload_sha256", None)
    require(sha_object(payload) == RELEASE_LOCK_PAYLOAD_SHA256, "RELEASE_LOCK_SEAL")
    require(value.get("candidate_outcome") == "K2P-SAME", "RELEASE_OUTCOME")
    require(value.get("promotion_ready") is True, "RELEASE_NOT_READY")
    require(value.get("blockers") == [], "RELEASE_BLOCKERS")
    require(value.get("missing_required_files") == [], "RELEASE_MISSING_FILES")
    return value


def locked_cores() -> dict[str, dict[str, tuple[Any, ...]]]:
    source = project_path(ATLAS).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=ATLAS)
    values: list[Any] = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(isinstance(target, ast.Name) and target.id == "CORES" for target in targets):
            values.append(ast.literal_eval(node.value))
    require(len(values) == 1, "ATLAS_CORES_ASSIGNMENT_COUNT", len(values))
    require(values[0] == EXPECTED_CORES, "ATLAS_PRIMITIVE_CORE_DRIFT")
    require(
        sha_object({"CORES": values[0]}) == EXPECTED_PRIMITIVE_GRAMMAR_SHA256,
        "ATLAS_PRIMITIVE_GRAMMAR_HASH_DRIFT",
    )
    return values[0]


def primitive_grammar_binding() -> dict[str, Any]:
    return {
        "path": ATLAS,
        "binding_kind": "CORES literal semantic fingerprint",
        "sha256": EXPECTED_PRIMITIVE_GRAMMAR_SHA256,
    }


def weak_compositions(total: int, bins: int):
    require(total >= 0 and bins > 0, "WEAK_COMPOSITION_DOMAIN")
    if bins == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, bins - 1):
            yield (first,) + rest


def enumerate_target_keys(
    selected_total: int,
    incoming_selected: bool,
    cores: dict[str, dict[str, tuple[Any, ...]]],
) -> list[dict[str, Any]]:
    keys: list[dict[str, Any]] = []
    outgoing = selected_total - int(incoming_selected)
    for core, spec in cores.items():
        sinks = len(spec["sinks"])
        repairs = ((None, ()),) if core == "cycle" else tuple(enumerate(spec["repairs"]))
        for sink_mask in range(1 << sinks):
            ordinary = outgoing - sink_mask.bit_count()
            if ordinary < 0:
                continue
            for composition in weak_compositions(ordinary, len(spec["arcs"])):
                for repair_index, repair in repairs:
                    keys.append(
                        {
                            "core": core,
                            "incoming_selected": incoming_selected,
                            "selected_sink_mask": sink_mask,
                            "weak_composition": list(composition),
                            "repair_index": repair_index,
                            "repair_arc_indices": list(repair),
                        }
                    )
    require(
        len({json.dumps(key, sort_keys=True) for key in keys}) == len(keys),
        "DUPLICATE_TARGET_GRAMMAR_KEY",
    )
    return keys


def parse_manifest(relative: str) -> dict[str, str]:
    base = project_path(relative).parent
    result: dict[str, str] = {}
    for line in project_path(relative).read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        path = base / name
        require(path.is_file(), "NESTED_MANIFEST_FILE_MISSING", path)
        require(sha_file(path) == digest, "NESTED_MANIFEST_HASH_MISMATCH", path)
        result[str(path.relative_to(PROJECT))] = digest
    return result


def recursively_locked_files() -> dict[str, str]:
    outer = release_anchor()
    result: dict[str, str] = {}
    for relative, record in outer["files"].items():
        digest = record["sha256"]
        require(sha_file(project_path(relative)) == digest, "OUTER_LOCK_HASH_MISMATCH", relative)
        result[relative] = digest

    direct_base = PROJECT / "package/referee/k2p_offline_sweep_portable"
    for lock_name in ("DIRECT_CLOSURE_LOCK.json", "INPUT_LOCK.json"):
        lock = load_json(direct_base / lock_name)
        for name, digest in lock["files"].items():
            path = direct_base / name
            require(path.is_file(), "DIRECT_NESTED_FILE_MISSING", path)
            require(sha_file(path) == digest, "DIRECT_NESTED_HASH_MISMATCH", path)
            relative = str(path.relative_to(PROJECT))
            if relative in result:
                require(result[relative] == digest, "NESTED_HASH_CONFLICT", relative)
            result[relative] = digest

    for manifest in (
        "work/rank_upper_certificates/MANIFEST.sha256",
        "work/cycle_three_port_closure/MANIFEST.sha256",
    ):
        for relative, digest in parse_manifest(manifest).items():
            if relative in result:
                require(result[relative] == digest, "MANIFEST_HASH_CONFLICT", relative)
            result[relative] = digest
    return result


def mutation_module(relative: str) -> bool:
    name = Path(relative).name
    return "mutation" in name or name.startswith("mutate_")


def proof_surface(files: dict[str, str]) -> dict[str, Any]:
    python = sorted(relative for relative in files if relative.endswith(".py"))
    require(len(python) == 112, "LOCKED_PYTHON_MODULE_CENSUS_DRIFT", len(python))
    require(INFRASTRUCTURE_MODULES <= set(python), "INFRASTRUCTURE_MODULE_MISSING")
    require(EXPLICIT_INDEPENDENT_MODULES <= set(python), "INDEPENDENT_MODULE_MISSING")
    mutations = {relative for relative in python if mutation_module(relative)}
    require(len(mutations) == 25, "MUTATION_MODULE_CENSUS_DRIFT", len(mutations))
    require(not (mutations & INFRASTRUCTURE_MODULES), "ROLE_PARTITION_OVERLAP_MUTATION_INFRA")
    require(
        not (mutations & EXPLICIT_INDEPENDENT_MODULES),
        "ROLE_PARTITION_OVERLAP_MUTATION_INDEPENDENT",
    )
    require(
        not (INFRASTRUCTURE_MODULES & EXPLICIT_INDEPENDENT_MODULES),
        "ROLE_PARTITION_OVERLAP_INFRA_INDEPENDENT",
    )
    primary = set(python) - mutations - INFRASTRUCTURE_MODULES - EXPLICIT_INDEPENDENT_MODULES

    def census(rows: set[str]) -> dict[str, int]:
        physical = 0
        sloc = 0
        for relative in rows:
            row_physical, row_sloc = noncomment_sloc(PROJECT / relative)
            physical += row_physical
            sloc += row_sloc
        return {"modules": len(rows), "physical_lines": physical, "sloc": sloc}

    categories = {
        "primary_generation_algebra_coverage_upper_bound": census(primary),
        "explicit_independent_adversarial_lower_bound": census(
            EXPLICIT_INDEPENDENT_MODULES
        ),
        "mutation": census(mutations),
        "release_hash_orchestration": census(INFRASTRUCTURE_MODULES),
    }
    require(sum(row["modules"] for row in categories.values()) == 112, "ROLE_MODULE_SUM")
    require(sum(row["physical_lines"] for row in categories.values()) == 58468, "ROLE_LOC_SUM")
    require(sum(row["sloc"] for row in categories.values()) == 53156, "ROLE_SLOC_SUM")
    return {
        "classification_boundary": (
            "Conservative file-level audit: primary is an upper bound and explicit "
            "independent/adversarial is a lower bound. Cross-cutting functions are not "
            "split by line."
        ),
        "categories": categories,
        "total": {"modules": 112, "physical_lines": 58468, "sloc": 53156},
    }


def completion_count(
    selected_total: int,
    incoming_selected: bool,
    cores: dict[str, dict[str, tuple[Any, ...]]],
) -> dict[str, Any]:
    outgoing = selected_total - int(incoming_selected)
    contributions: list[dict[str, Any]] = []
    total = 0
    for core, spec in cores.items():
        segments = len(spec["arcs"])
        sinks = len(spec["sinks"])
        repairs = 1 if core == "cycle" else len(spec["repairs"])
        by_selected_sinks: list[dict[str, int]] = []
        subtotal = 0
        for selected_sinks in range(sinks + 1):
            ordinary = outgoing - selected_sinks
            if ordinary < 0:
                continue
            ways = (
                repairs
                * math.comb(sinks, selected_sinks)
                * math.comb(ordinary + segments - 1, segments - 1)
            )
            subtotal += ways
            by_selected_sinks.append(
                {"selected_sinks": selected_sinks, "completion_count": ways}
            )
        total += subtotal
        contributions.append(
            {
                "core": core,
                "segments": segments,
                "sinks": sinks,
                "repair_choices": repairs,
                "by_selected_sinks": by_selected_sinks,
                "subtotal": subtotal,
            }
        )
    keys = enumerate_target_keys(selected_total, incoming_selected, cores)
    require(len(keys) == total, "FORMULA_ENUMERATION_DISAGREEMENT")
    return {
        "selected_total": selected_total,
        "incoming_selected": incoming_selected,
        "outgoing_selected": outgoing,
        "contributions": contributions,
        "ordered_target_key_sha256": sha_object(keys),
        "total": total,
    }


def baseline_payload() -> dict[str, Any]:
    release = release_anchor()
    cores = locked_cores()
    files = recursively_locked_files()
    require(len(files) == 405, "TRANSITIVE_FILE_CENSUS_DRIFT", len(files))
    extension_counts: Counter[str] = Counter()
    extension_bytes: Counter[str] = Counter()
    for relative in files:
        path = PROJECT / relative
        name = path.name
        if name.endswith(".jsonl.gz"):
            extension = ".jsonl.gz"
        elif name.endswith(".json.gz"):
            extension = ".json.gz"
        elif name.endswith(".sha256"):
            extension = ".sha256"
        else:
            extension = path.suffix or "[none]"
        extension_counts[extension] += 1
        extension_bytes[extension] += path.stat().st_size

    machine_extensions = {".json", ".json.gz", ".jsonl.gz", ".pkl"}
    machine_files = sum(extension_counts[extension] for extension in machine_extensions)
    machine_bytes = sum(extension_bytes[extension] for extension in machine_extensions)
    require((machine_files, machine_bytes) == (240, 476415795), "MACHINE_DATA_CENSUS_DRIFT")

    manuscript = project_path(
        "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md"
    )
    manuscript_text = manuscript.read_text(encoding="utf-8")
    manuscript_lines = manuscript_text.splitlines()
    named_results = sum(
        bool(re.match(r"^### (Lemma|Theorem)", line)) for line in manuscript_lines
    )

    raw4 = load_json(
        project_path(
            "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json"
        )
    )
    theta2 = load_json(
        project_path(
            "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_summary.json"
        )
    )
    restoration = load_json(
        project_path(
            "work/restoration_sign_reclassification/corrected_restoration_forest.json"
        )
    )["census"]
    probe = load_json(
        project_path("work/probe_coherence_corrected/probe_coherence_certificate.json")
    )
    cycle = load_json(
        project_path("work/cycle_three_port_closure/promotion/cycle_promotion_certificate.json")
    )
    rank = load_json(
        project_path("work/rank_upper_certificates/rank_upper_coverage.json")
    )

    formula_cases = {
        "four_port_selected_incoming": completion_count(4, True, cores),
        "four_port_marginalized_incoming": completion_count(4, False, cores),
        "five_port_selected_incoming": completion_count(5, True, cores),
        "five_port_marginalized_incoming": completion_count(5, False, cores),
        "three_port_selected_incoming": completion_count(3, True, cores),
        "three_port_marginalized_incoming": completion_count(3, False, cores),
    }
    expected = {
        "four_port_selected_incoming": 831,
        "four_port_marginalized_incoming": 1983,
        "five_port_selected_incoming": 1983,
        "five_port_marginalized_incoming": 4155,
        "three_port_selected_incoming": 289,
        "three_port_marginalized_incoming": 831,
    }
    require(
        {key: value["total"] for key, value in formula_cases.items()} == expected,
        "FINITE_FORMULA_CENSUS_DRIFT",
    )
    expected_subtotals = {
        "three_port_selected_incoming": [5, 40, 40, 136, 68],
        "three_port_marginalized_incoming": [7, 100, 100, 416, 208],
        "four_port_selected_incoming": [7, 100, 100, 416, 208],
        "four_port_marginalized_incoming": [9, 210, 210, 1036, 518],
        "five_port_selected_incoming": [9, 210, 210, 1036, 518],
        "five_port_marginalized_incoming": [11, 392, 392, 2240, 1120],
    }
    require(
        {
            label: [row["subtotal"] for row in case["contributions"]]
            for label, case in formula_cases.items()
        }
        == expected_subtotals,
        "FINITE_CORE_SUBTOTAL_DRIFT",
    )
    source_support_counts = {
        "raw4": sum(len(cores[core]["repairs"]) for core in ("theta0", "theta1", "theta3")),
        "theta2": len(cores["theta2"]["repairs"]),
        "cycle": len(cores["cycle"]["repairs"]),
    }
    require(source_support_counts == {"raw4": 6, "theta2": 4, "cycle": 2}, "SOURCE_SUPPORT_COUNT")
    require(
        source_support_counts["raw4"]
        * (831 + 1983)
        * math.factorial(4)
        == raw4["total_rows"],
        "RAW4_FORMULA",
    )
    require(
        source_support_counts["theta2"]
        * (1983 + 4155)
        * math.factorial(5)
        == theta2["total_rows"],
        "THETA2_FORMULA",
    )
    require(
        source_support_counts["cycle"]
        * (289 + 831)
        * math.factorial(3)
        == cycle["base"]["rows"],
        "CYCLE_FORMULA",
    )

    release_lock = project_path(RELEASE_LOCK)
    return {
        "schema": "k2p-proof-compression-baseline-v1",
        "status": "PASS",
        "scope": "Principal D_plus PC-PARTIAL baseline; frozen theorem files are read-only.",
        "frozen_release": {
            "release_lock_sha256": sha_file(release_lock),
            "release_lock_payload_sha256": release["payload_sha256"],
            "promotion_ready": release["promotion_ready"],
            "outer_locked_files": len(release["files"]),
            "transitively_locked_evidence_files": len(files),
            "bundle_files_including_release_lock": len(files) + 1,
            "transitive_evidence_bytes": sum(
                (PROJECT / relative).stat().st_size for relative in files
            ),
            "bundle_bytes_including_release_lock": sum(
                (PROJECT / relative).stat().st_size for relative in files
            )
            + release_lock.stat().st_size,
        },
        "manuscript_surface": {
            "path": str(manuscript.relative_to(PROJECT)),
            "sha256": sha_file(manuscript),
            "lines": len(manuscript_lines),
            "words": len(manuscript_text.split()),
            "named_lemmas_and_theorems": named_results,
        },
        "python_proof_surface": proof_surface(files),
        "machine_readable_evidence": {
            "files": machine_files,
            "bytes": machine_bytes,
            "extension_counts": dict(sorted(extension_counts.items())),
            "extension_bytes": dict(sorted(extension_bytes.items())),
        },
        "finite_universes": {
            "raw4": {
                "rows": raw4["total_rows"],
                "category_counts": raw4["category_counts"],
                "terminal_classes": raw4["terminal_class_bindings"]["distinct_class_count"],
                "restoration_parents": raw4["restoration_member_bindings"]["distinct_parent_count"],
            },
            "theta2": {
                "rows": theta2["total_rows"],
                "category_counts": theta2["category_counts"],
                "restoration_descendants": theta2["restoration_descendants"],
            },
            "cycle": {
                "base_rows": cycle["base"]["rows"],
                "base_category_counts": cycle["base"]["terminal_census"],
                "full_children": cycle["fixed_full_restoration"]["children"],
                "full_category_counts": cycle["full"]["terminal_census"],
            },
            "primitive_cores": {
                core: {
                    "segments": len(spec["arcs"]),
                    "path_sinks": len(spec["sinks"]),
                    "minimum_repairs": [list(repair) for repair in spec["repairs"]],
                    "target_repair_choices": (
                        1 if core == "cycle" else len(spec["repairs"])
                    ),
                }
                for core, spec in cores.items()
            },
            "completion_formula_cases": formula_cases,
            "source_support_counts": source_support_counts,
        },
        "restoration": restoration,
        "probe": {
            "anchors": probe["anchor_inventory"]["anchors"],
            "canonical_anchor_classes": probe["anchor_inventory"][
                "canonical_anchor_classes"
            ],
            "one_port": probe["one_port"],
            "two_port": probe["two_port"],
            "registries": probe["registries"],
        },
        "rank_upper": {
            "descriptors": rank["descriptor_count"],
            "base_ansatz_descriptors": rank["base_ansatz_descriptor_count"],
            "exceptional_descriptors": rank["exceptional_descriptor_count"],
            "exceptional_representatives": rank["exceptional_representative_count"],
        },
        "runtime_boundary": {
            "end_to_end_quick_runtime_byte_bound": False,
            "end_to_end_full_runtime_byte_bound": False,
            "note": (
                "Operational runtimes are deliberately excluded from several byte-stable "
                "certificates. Component logs may be cited, but no exact end-to-end full "
                "runtime is inferred here."
            ),
        },
        "input_bindings": [
            input_binding(RELEASE_LOCK),
            primitive_grammar_binding(),
            input_binding(
                "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json"
            ),
            input_binding(
                "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_summary.json"
            ),
            input_binding(
                "work/restoration_sign_reclassification/corrected_restoration_forest.json"
            ),
            input_binding("work/probe_coherence_corrected/probe_coherence_certificate.json"),
            input_binding(
                "work/cycle_three_port_closure/promotion/cycle_promotion_certificate.json"
            ),
            input_binding("work/rank_upper_certificates/rank_upper_coverage.json"),
        ],
    }


def baseline_markdown(value: dict[str, Any]) -> str:
    surface = value["python_proof_surface"]
    categories = surface["categories"]
    raw4 = value["finite_universes"]["raw4"]
    theta2 = value["finite_universes"]["theta2"]
    restoration = value["restoration"]
    probe = value["probe"]
    return f"""# Proof-compression baseline

Status: **PASS**.  This is a read-only measurement of frozen release lock
`{value['frozen_release']['release_lock_sha256']}`.  It does not replace or
modify the promoted theorem.

## Proof surface

| Role | Modules | Physical lines | Nonblank/noncomment lines |
|---|---:|---:|---:|
| Primary generation, algebra, and coverage (upper bound) | {categories['primary_generation_algebra_coverage_upper_bound']['modules']} | {categories['primary_generation_algebra_coverage_upper_bound']['physical_lines']:,} | {categories['primary_generation_algebra_coverage_upper_bound']['sloc']:,} |
| Explicit independent/adversarial consumers (lower bound) | {categories['explicit_independent_adversarial_lower_bound']['modules']} | {categories['explicit_independent_adversarial_lower_bound']['physical_lines']:,} | {categories['explicit_independent_adversarial_lower_bound']['sloc']:,} |
| Mutation code | {categories['mutation']['modules']} | {categories['mutation']['physical_lines']:,} | {categories['mutation']['sloc']:,} |
| Release, hash, and orchestration | {categories['release_hash_orchestration']['modules']} | {categories['release_hash_orchestration']['physical_lines']:,} | {categories['release_hash_orchestration']['sloc']:,} |
| **Total** | {surface['total']['modules']} | {surface['total']['physical_lines']:,} | {surface['total']['sloc']:,} |

The classification is deliberately conservative and file-level.  In
particular, cross-layer release validation is not counted as an independent
mathematical hypothesis, and the primary figure is an upper bound.

The recursively locked evidence set contains
{value['frozen_release']['transitively_locked_evidence_files']} files and
{value['machine_readable_evidence']['files']} machine-readable evidence files
({value['machine_readable_evidence']['bytes']:,} bytes).  The promotion
manuscript has {value['manuscript_surface']['lines']} lines,
{value['manuscript_surface']['words']:,} words, and
{value['manuscript_surface']['named_lemmas_and_theorems']} named lemmas or
theorems.

## Finite theorem surface

| Layer | Exact census |
|---|---:|
| Four-port raw directions | {raw4['rows']:,} |
| Four-port terminal presentations / canonical terminal classes | {raw4['category_counts']['direct_terminal_presentation']:,} / {raw4['terminal_classes']:,} |
| Four-port restoration presentations / canonical parents | {raw4['category_counts']['restoration_member_presentation']:,} / {raw4['restoration_parents']:,} |
| Theta2 raw directions | {theta2['rows']:,} |
| Restoration first / second children | {restoration['first_children']:,} / {restoration['second_children']:,} |
| Restoration final leaves | {restoration['final_leaves']:,} |
| Probe anchors / canonical anchor classes | {probe['anchors']} / {probe['canonical_anchor_classes']} |
| Probe one-port / two-port rows | {probe['one_port']['raw_pairs']:,} / {probe['two_port']['raw_pairs']:,} |

Every authoritative sign row is classified by an original-full-map
`T_i` certificate.  Historical rooted `tree_sunlet` reasons are excluded
from this compression surface.

## Timing boundary

The frozen deterministic payload does not record an end-to-end quick or full
runtime.  This baseline therefore does not invent one from noncomparable
component timings.  Runtime benchmarking belongs in a separate operational
record.

Payload SHA-256: `{value['payload_sha256']}`.
"""


def universe_markdown(value: dict[str, Any]) -> str:
    cases = value["finite_universes"]["completion_formula_cases"]
    rows = []
    for label, case in cases.items():
        subtotals = ", ".join(
            f"{entry['core']}={entry['subtotal']}" for entry in case["contributions"]
        )
        rows.append(
            f"| `{label}` | {case['selected_total']} | "
            f"{str(case['incoming_selected']).lower()} | {subtotals} | {case['total']:,} |"
        )
    table = "\n".join(rows)
    return rf"""# Finite-universe completeness

## Completion-count lemma

For a primitive target core `H`, let `m_H` be its directed core-segment
count, `q_H` its path-sink count, and `r_H` its number of minimum-repair
choices in the target grammar.  The exact tuples are

```text
cycle (2,1,1), theta0 (5,1,2), theta1 (5,1,2),
theta2 (6,2,4), theta3 (6,2,2).
```

For `k` physical selected boundaries and `epsilon=1` when the incoming
boundary is selected (`epsilon=0` when it is the incoming dummy), the number
of target completions is

\[
C(k,\epsilon)=\sum_H r_H\sum_{{j=0}}^{{q_H}}
 \binom{{q_H}}{{j}}
 \binom{{k-\epsilon-j+m_H-1}}{{m_H-1}}.
\]

Indeed, choose `j` selected path sinks and weakly distribute the remaining
`k-epsilon-j` selected boundaries over the `m_H` directed segments.  Empty
repair segments receive their uniquely named dummy boundaries and do not
change the count.  Each minimum repair remains a distinct directed target
record.  Physical label permutations are applied only afterward.

| Case | `k` | Incoming selected | Core subtotals | Total |
|---|---:|---:|---|---:|
{table}

Consequently,

\[
6(831+1983)4!=405{{,}}216,
\]

for the six four-port theta source repairs,

\[
4(1983+4155)5!=2{{,}}946{{,}}240,
\]

for the four minimum-repaired five-port `theta2` sources, and

\[
2(289+831)3!=13{{,}}440
\]

for the two three-port cycle source supports.

## Exhaustiveness boundary

This derivation compresses the arithmetic of the frozen primitive grammar.
The script parses the locked `CORES` literal directly from the atlas, requires
the exact five primitive arc/sink/repair encodings, and independently enumerates
every unique `(core, incoming mode, sink mask, weak composition, repair)` key.
It relies on, and does not re-prove, the frozen primitive-core theorem.  The
cycle target grammar has one repair choice; its two minimum source supports are
counted separately in the leading source factor.  Physical label permutations
are applied only after target enumeration.  No source-target reversal,
ordinary-triangle quotient, inheritance complement, pole exchange, or
uncertified graph symmetry is used in the count.

The uniqueness claim is for directed completion records/presentations, not for
unlabelled graphs.  When a repaired arc is already occupied, different repair
records can construct the same graph.  The record key retains the core,
incoming mode, repair index and arc set, sink mask, ordered segment words,
deterministic dummy roles, and then the exact physical port permutation.

The derived totals agree exactly with the authoritative corrected composite
ledgers bound by baseline payload `{value['payload_sha256']}`.
"""


def main() -> None:
    reject_optimized_python()
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    arguments = parser.parse_args()

    value = sealed(baseline_payload())
    require(value["frozen_release"]["promotion_ready"] is True, "RELEASE_NOT_READY")
    rendered_baseline = baseline_markdown(value)
    rendered_universe = universe_markdown(value)
    outputs = (
        (
            BASELINE_JSON,
            (
                json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False)
                + "\n"
            ).encode("utf-8"),
        ),
        (BASELINE_MD, (rendered_baseline.rstrip() + "\n").encode("utf-8")),
        (UNIVERSE_MD, (rendered_universe.rstrip() + "\n").encode("utf-8")),
    )
    if arguments.write:
        write_json(BASELINE_JSON, value)
        write_text(BASELINE_MD, rendered_baseline)
        write_text(UNIVERSE_MD, rendered_universe)
    else:
        for path, expected in outputs:
            require(path.is_file(), "DERIVED_OUTPUT_MISSING", path)
            require(path.read_bytes() == expected, "DERIVED_OUTPUT_DRIFT", path)
    print(
        json.dumps(
            {
                "status": "PASS",
                "payload_sha256": value["payload_sha256"],
                "outputs": [
                    str(path.relative_to(PROJECT)) for path, _expected in outputs
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

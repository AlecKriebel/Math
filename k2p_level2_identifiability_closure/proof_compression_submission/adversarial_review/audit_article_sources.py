#!/usr/bin/env python3
"""Fail-closed static audit of the K2P article and reader supplement."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def line_number(text: str, needle: str) -> int | None:
    for number, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return number
    return None


def offset_line(text: str, offset: int) -> int:
    """Return the one-based source line containing a character offset."""
    return text.count("\n", 0, offset) + 1


def tex_keys(text: str, command: str) -> list[str]:
    pattern = rf"\\{command}(?:\[[^]]*\])?\{{([^}}]+)\}}"
    values: list[str] = []
    for group in re.findall(pattern, text):
        values.extend(item.strip() for item in group.split(","))
    return values


def main() -> dict[str, object]:
    require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")

    submission = Path(__file__).resolve().parents[1]
    project = submission.parent
    article_path = submission / "article" / "main.tex"
    supplement_path = submission / "supplement" / "supplement.tex"
    compression_path = submission / "supplement" / "compression_tables.tex"
    certificate_tex_path = submission / "supplement" / "certificate_appendix.tex"
    certificate_json_path = submission / "templates" / "PRINTED_CERTIFICATE_APPENDIX.json"
    sharpness_columns_path = submission / "analysis" / "WEAK_SHARPNESS_COLUMN_CROSSWALK.json"
    bib_path = submission / "article" / "references.bib"
    release_path = project / "work" / "final_theorem_release" / "RELEASE_LOCK.json"
    full_replay_path = submission / "output" / "FINAL_CLEAN_FULL_REPLAY.json"
    full_replay_telemetry_path = (
        submission / "output" / "FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"
    )
    universe_path = (
        project
        / "work"
        / "final_theorem_release"
        / "corrected_universe_certificate.json"
    )
    quartet_spec_path = project / "work" / "quartet_separation_closure" / "QUARTET_SEMANTICS_SPEC.json"
    quartet_path = project / "work" / "quartet_separation_closure" / "quartet_logic_certificate.json"
    quartet_mutation_path = project / "work" / "quartet_separation_closure" / "quartet_semantics_mutation_certificate.json"
    terminal_path = project / "work" / "quartet_separation_closure" / "quartet_terminal_binding_certificate.json"
    terminal_mutation_path = project / "work" / "quartet_separation_closure" / "quartet_terminal_binding_mutation_certificate.json"
    canonicalizer_path = project / "work" / "canonicalizer_completeness" / "canonicalizer_completeness_certificate.json"
    canonicalizer_mutation_path = project / "work" / "canonicalizer_completeness" / "canonicalizer_completeness_mutation_certificate.json"
    parameter_transport_path = project / "work" / "canonicalizer_completeness" / "inheritance_transport" / "parameter_transport_certificate.json"
    parameter_transport_mutation_path = project / "work" / "canonicalizer_completeness" / "inheritance_transport" / "parameter_transport_mutation_report.json"
    rank_mutation_path = project / "work" / "rank_upper_certificates" / "mutation_report.json"
    license_path = project / "LICENSES.md"

    for path in (
        article_path,
        supplement_path,
        compression_path,
        certificate_tex_path,
        certificate_json_path,
        sharpness_columns_path,
        bib_path,
        release_path,
        universe_path,
        full_replay_path,
        full_replay_telemetry_path,
        quartet_spec_path,
        quartet_path,
        quartet_mutation_path,
        terminal_path,
        terminal_mutation_path,
        canonicalizer_path,
        canonicalizer_mutation_path,
        parameter_transport_path,
        parameter_transport_mutation_path,
        rank_mutation_path,
        license_path,
    ):
        require(path.is_file(), f"MISSING_REQUIRED_FILE:{path}")

    article = article_path.read_text(encoding="utf-8")
    supplement = supplement_path.read_text(encoding="utf-8")
    compression = compression_path.read_text(encoding="utf-8")
    certificate_tex = certificate_tex_path.read_text(encoding="utf-8")
    certificate_json = read_json(certificate_json_path)
    sharpness_columns = read_json(sharpness_columns_path)
    quartet = read_json(quartet_path)
    quartet_mutation = read_json(quartet_mutation_path)
    terminal = read_json(terminal_path)
    terminal_mutation = read_json(terminal_mutation_path)
    canonicalizer = read_json(canonicalizer_path)
    canonicalizer_mutation = read_json(canonicalizer_mutation_path)
    parameter_transport = read_json(parameter_transport_path)
    parameter_transport_mutation = read_json(parameter_transport_mutation_path)
    rank_mutation = read_json(rank_mutation_path)
    bib = bib_path.read_text(encoding="utf-8")
    supplement_source = supplement + "\n" + compression + "\n" + certificate_tex
    all_tex = article + "\n" + supplement_source

    require(isinstance(certificate_json, dict), "PRINTED_APPENDIX_NOT_OBJECT")
    require(
        certificate_json.get("schema") == "k2p-printed-certificate-appendix-v1"
        and certificate_json.get("status") == "PASS"
        and certificate_json.get("quadratic_template_count") == 23
        and certificate_json.get("high_degree_base_count") == 5,
        "PRINTED_APPENDIX_SCHEMA_OR_CENSUS_DRIFT",
    )
    require(isinstance(sharpness_columns, dict), "SHARPNESS_CROSSWALK_NOT_OBJECT")
    require(
        sharpness_columns.get("schema")
        == "k2p-weak-sharpness-column-crosswalk-v1",
        "SHARPNESS_CROSSWALK_SCHEMA_DRIFT",
    )
    require(
        sha256(certificate_json_path) in supplement
        and sha256(sharpness_columns_path) in supplement,
        "PRINTED_SUBMISSION_HASH_BINDING_STALE",
    )

    require(
        isinstance(quartet, dict)
        and quartet.get("schema") == "k2p-displayed-quartet-semantics-v2"
        and quartet.get("status") == "PASS"
        and quartet.get("character_order") == ["0", "C", "G", "T"]
        and quartet.get("edge_spectrum") == ["1", "s", "g", "s"]
        and quartet.get("equal_nonzero_sector") == ["C", "T"]
        and quartet.get("canonical_formula_count") == 6
        and quartet.get("formula_transport_count") == 288
        and quartet.get("unequal_pair_count") == 21,
        "QUARTET_SEMANTICS_CERTIFICATE_DRIFT",
    )
    require(
        quartet.get("document_sha256", {}).get(
            "proof_compression_submission/article/main.tex"
        )
        == sha256(article_path),
        "QUARTET_ARTICLE_LITERAL_BINDING_STALE",
    )
    require(
        isinstance(quartet_mutation, dict)
        and quartet_mutation.get("schema") == "k2p-quartet-semantics-mutations-v3"
        and quartet_mutation.get("status") == "PASS"
        and quartet_mutation.get("case_count") == 8
        and isinstance(quartet_mutation.get("cases"), list)
        and len(quartet_mutation["cases"]) == 8
        and all(
            isinstance(row, dict)
            and row.get("observed_marker") == row.get("expected_marker")
            and row.get("observed_returncode") == 1
            and row.get("failed_mutation_certificate_written") is False
            and "stdout_sha256" not in row
            for row in quartet_mutation["cases"]
        ),
        "QUARTET_SEMANTICS_MUTATION_DRIFT",
    )
    require(
        quartet.get("spec_sha256") == sha256(quartet_spec_path)
        and quartet_mutation.get("spec_sha256") == sha256(quartet_spec_path),
        "QUARTET_SEMANTICS_SPEC_BINDING_STALE",
    )
    require(
        isinstance(terminal, dict)
        and terminal.get("schema") == "k2p-quartet-terminal-binding-v1"
        and terminal.get("status") == "PASS"
        and terminal.get("aggregate", {}).get("quartet_terminal_rows") == 4_414_710
        and terminal.get("aggregate", {}).get("per_layer_certificate_ids") == 888
        and terminal.get("aggregate", {}).get("missing_references") == 0
        and terminal.get("aggregate", {}).get("dangling_certificates") == 0,
        "QUARTET_TERMINAL_BINDING_DRIFT",
    )
    require(
        isinstance(terminal_mutation, dict)
        and terminal_mutation.get("schema") == "k2p-quartet-terminal-binding-mutations-v1"
        and terminal_mutation.get("status") == "PASS"
        and terminal_mutation.get("case_count") == 12,
        "QUARTET_TERMINAL_MUTATION_DRIFT",
    )
    require(
        terminal.get("semantics_certificate", {}).get("sha256") == sha256(quartet_path)
        and terminal_mutation.get("semantics_certificate_sha256") == sha256(quartet_path),
        "QUARTET_TERMINAL_SEMANTICS_BINDING_STALE",
    )
    require(
        isinstance(canonicalizer, dict)
        and canonicalizer.get("schema") == "k2p-canonicalizer-completeness-v1"
        and canonicalizer.get("status") == "PASS"
        and canonicalizer.get("descriptor_audit", {}).get("primitive_archetypes_compared") == 10_084
        and canonicalizer.get("descriptor_audit", {}).get("slow_fast_disagreements") == 0
        and canonicalizer.get("relation_audit", {}).get("rank_and_topology_eligible_presentations") == 4_012
        and canonicalizer.get("relation_audit", {}).get("disagreements") == 0,
        "CANONICALIZER_COMPLETENESS_DRIFT",
    )
    require(
        isinstance(canonicalizer_mutation, dict)
        and canonicalizer_mutation.get("schema") == "k2p-canonicalizer-completeness-mutations-v1"
        and canonicalizer_mutation.get("status") == "PASS"
        and canonicalizer_mutation.get("rejected") == 2
        and canonicalizer_mutation.get("survived") == 0,
        "CANONICALIZER_MUTATION_DRIFT",
    )
    require(
        canonicalizer_mutation.get("atlas_sha256")
        == canonicalizer.get("inputs", {}).get("atlas_sha256"),
        "CANONICALIZER_MUTATION_ATLAS_BINDING_STALE",
    )
    require(
        isinstance(parameter_transport, dict)
        and parameter_transport.get("schema") == "k2p_graph_derived_parameter_transport_certificate_v1"
        and parameter_transport.get("status") == "PASS"
        and parameter_transport.get("closure", {}).get("all_exact_transport_records_used") == 67_741
        and parameter_transport.get("closure", {}).get("all_frozen_parent_restriction_records_used") == 4_379
        and parameter_transport.get("closure", {}).get("restoration_canonical_parents") == 997
        and parameter_transport.get("closure", {}).get("unresolved_parameter_transports") == 0
        and parameter_transport.get("ledgers", {}).get("probe_relations", {}).get("rows") == 67_741
        and parameter_transport.get("ledgers", {}).get("probe_restrictions", {}).get("rows") == 71_022
        and parameter_transport.get("ledgers", {}).get("restoration_restrictions", {}).get("rows") == 5_540,
        "PARAMETER_TRANSPORT_CERTIFICATE_DRIFT",
    )
    require(
        isinstance(parameter_transport_mutation, dict)
        and parameter_transport_mutation.get("schema") == "k2p_parameter_transport_mutations_v1"
        and parameter_transport_mutation.get("status") == "PASS"
        and parameter_transport_mutation.get("rejected") == 10
        and parameter_transport_mutation.get("survived") == 0,
        "PARAMETER_TRANSPORT_MUTATION_DRIFT",
    )
    require(
        parameter_transport_mutation.get("certificate_payload_sha256")
        == parameter_transport.get("payload_sha256"),
        "PARAMETER_TRANSPORT_MUTATION_BINDING_STALE",
    )
    for ledger_name, ledger in parameter_transport.get("ledgers", {}).items():
        require(isinstance(ledger, dict), f"PARAMETER_LEDGER_ROW_MALFORMED:{ledger_name}")
        ledger_path = parameter_transport_path.parent / str(ledger.get("path"))
        require(
            ledger_path.is_file()
            and not ledger_path.is_symlink()
            and ledger.get("sha256") == sha256(ledger_path)
            and ledger.get("bytes") == ledger_path.stat().st_size,
            f"PARAMETER_LEDGER_BINDING_STALE:{ledger_name}",
        )
    require(
        isinstance(rank_mutation, dict)
        and rank_mutation.get("schema") == "k2p-rank-upper-adversarial-mutations-v1"
        and rank_mutation.get("status") == "pass"
        and rank_mutation.get("mutation_count") == 7
        and rank_mutation.get("survivors") == 0
        and any(
            row.get("mutation") == "sampled_rank_substituted_for_symbolic_upper"
            and row.get("status") == "rejected"
            for row in rank_mutation.get("results", [])
            if isinstance(row, dict)
        ),
        "SAMPLED_RANK_UPPER_MUTATION_NOT_REJECTED",
    )

    release = read_json(release_path)
    require(isinstance(release, dict), "RELEASE_LOCK_NOT_OBJECT")
    release_unsigned = dict(release)
    release_payload = release_unsigned.pop("payload_sha256", None)
    require(
        release.get("schema") == "k2p-principal-d-plus-final-theorem-release-lock-v1"
        and release.get("promotion_ready") is True
        and not release.get("blockers")
        and not release.get("missing_required_files")
        and isinstance(release_payload, str)
        and release_payload == canonical_hash(release_unsigned),
        "RELEASE_NOT_PROMOTION_READY_OR_PAYLOAD_INVALID",
    )
    required_new_release_paths = {
        "LICENSES.md",
        "work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json",
        "work/quartet_separation_closure/quartet_logic_certificate.json",
        "work/quartet_separation_closure/quartet_semantics_mutation_certificate.json",
        "work/quartet_separation_closure/quartet_terminal_binding_certificate.json",
        "work/quartet_separation_closure/quartet_terminal_binding_mutation_certificate.json",
        "work/quartet_separation_closure/verify_quartet_logic.py",
        "work/quartet_separation_closure/verify_quartet_terminal_bindings.py",
        "work/canonicalizer_completeness/canonicalizer_completeness_certificate.json",
        "work/canonicalizer_completeness/canonicalizer_completeness_mutation_certificate.json",
        "work/canonicalizer_completeness/verify_canonicalizer_completeness.py",
        "work/canonicalizer_completeness/inheritance_transport/parameter_transport_certificate.json",
        "work/canonicalizer_completeness/inheritance_transport/parameter_transport_mutation_report.json",
        "work/canonicalizer_completeness/inheritance_transport/probe_relation_parameter_transports.jsonl.gz",
        "work/canonicalizer_completeness/inheritance_transport/probe_restriction_parameter_transports.jsonl.gz",
        "work/canonicalizer_completeness/inheritance_transport/restoration_restriction_parameter_transports.jsonl.gz",
        "work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py",
    }
    release_files = release.get("files")
    require(
        isinstance(release_files, dict)
        and required_new_release_paths <= set(release_files),
        "NEW_EXACT_EVIDENCE_NOT_BOUND_IN_RELEASE_LOCK",
    )

    full_replay = read_json(full_replay_path)
    full_replay_telemetry = read_json(full_replay_telemetry_path)
    require(isinstance(full_replay, dict), "FULL_REPLAY_NOT_OBJECT")
    require(isinstance(full_replay_telemetry, dict), "FULL_REPLAY_TELEMETRY_NOT_OBJECT")
    telemetry_source_paths = {
        "proof_compression_submission/article/main.tex": article_path,
        "proof_compression_submission/article/references.bib": bib_path,
        "proof_compression_submission/supplement/supplement.tex": supplement_path,
        "proof_compression_submission/supplement/compression_tables.tex": compression_path,
        "proof_compression_submission/supplement/certificate_appendix.tex": certificate_tex_path,
    }
    require(
        all(path.is_file() and not path.is_symlink() for path in telemetry_source_paths.values()),
        "FULL_REPLAY_TELEMETRY_SOURCE_MISSING_OR_SYMBOLIC",
    )
    expected_telemetry_sources = {
        relative: {"bytes": len(path.read_bytes()), "sha256": sha256(path)}
        for relative, path in telemetry_source_paths.items()
    }
    require(
        full_replay_telemetry.get("submission_sources")
        == expected_telemetry_sources,
        "FULL_REPLAY_TELEMETRY_SUBMISSION_SOURCE_DRIFT",
    )
    expected_telemetry_lock = {
        "bytes": len(release_path.read_bytes()),
        "path": "work/final_theorem_release/RELEASE_LOCK.json",
        "payload_sha256": release_payload,
        "sha256": sha256(release_path),
    }
    require(
        not release_path.is_symlink()
        and full_replay_telemetry.get("release_lock") == expected_telemetry_lock,
        "FULL_REPLAY_TELEMETRY_RELEASE_LOCK_DRIFT",
    )
    full_layers = full_replay.get("layer_replays")
    require(
        full_replay.get("status") == "PASS"
        and full_replay.get("mode") == "full"
        and full_replay.get("promotion_ready") is True
        and full_replay.get("blockers") == []
        and isinstance(full_layers, list)
        and len(full_layers) > 0
        and full_replay.get("lock_payload_sha256") == release.get("payload_sha256"),
        "FULL_REPLAY_NOT_PROMOTION_READY_PASS",
    )
    wall_seconds = full_replay_telemetry.get("time_l", {}).get("real_seconds")
    internal_seconds = full_replay.get("elapsed_seconds")
    require(
        full_replay_telemetry.get("status") == "PASS"
        and full_replay_telemetry.get("clean_detached_checkout") is True
        and full_replay_telemetry.get("report", {}).get("sha256")
        == sha256(full_replay_path)
        and full_replay_telemetry.get("report", {}).get("lock_payload_sha256")
        == release.get("payload_sha256")
        and full_replay_telemetry.get("report", {}).get("layer_count")
        == len(full_layers)
        and full_replay_telemetry.get("report", {}).get("internal_elapsed_seconds")
        == internal_seconds
        and full_replay_telemetry.get("report", {}).get("promotion_ready") is True
        and full_replay_telemetry.get("report", {}).get("blocker_count") == 0
        and isinstance(wall_seconds, (int, float))
        and not isinstance(wall_seconds, bool)
        and isinstance(internal_seconds, (int, float))
        and not isinstance(internal_seconds, bool)
        and wall_seconds >= internal_seconds > 0,
        "FULL_REPLAY_TELEMETRY_INCOHERENT",
    )

    universe = read_json(universe_path)
    require(isinstance(universe, dict), "UNIVERSE_NOT_OBJECT")
    families = universe.get("families")
    require(isinstance(families, dict), "UNIVERSE_FAMILIES_MISSING")
    expected_inputs = {
        "raw4": 405216,
        "theta2": 2946240,
        "cycle": 13440,
        "restoration": 2540,
        "probe": 574535,
    }
    for family, expected in expected_inputs.items():
        row = families.get(family)
        require(isinstance(row, dict), f"FAMILY_MISSING:{family}")
        require(row.get("input_count") == expected, f"FAMILY_COUNT_DRIFT:{family}")
        require(row.get("unresolved") == 0, f"FAMILY_UNRESOLVED:{family}")

    for token in (
        "405{,}216",
        "2{,}946{,}240",
        "36,824",
        "29,964",
        "544,571",
        "997",
        "297",
        "PC-PARTIAL",
    ):
        require(token in all_tex, f"SUBMISSION_COUNT_OR_STATUS_MISSING:{token}")

    for source_name, source in (("article", article), ("supplement", supplement_source)):
        label_occurrences = re.findall(r"\\label\{([^}]+)\}", source)
        require(
            len(label_occurrences) == len(set(label_occurrences)),
            f"DUPLICATE_TEX_LABEL:{source_name}",
        )
        references: list[str] = []
        for command in ("ref", "eqref", "cref", "Cref"):
            references.extend(tex_keys(source, command))
        require(
            not (set(references) - set(label_occurrences)),
            f"UNRESOLVED_INTERNAL_REFERENCE:{source_name}",
        )

    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    citations = tex_keys(article, "cite") + tex_keys(supplement_source, "cite")
    require(not (set(citations) - bib_keys), "UNRESOLVED_CITATION_KEY")
    require(not (bib_keys - set(citations)), "UNUSED_BIBLIOGRAPHY_ENTRY")

    for relative in re.findall(r"\\path\{([^}]+)\}", supplement_source):
        if (
            "/" not in relative
            or relative.startswith("supplement/")
            or relative.startswith("k2p_")
        ):
            continue
        require((project / relative).exists(), f"CROSSWALK_PATH_MISSING:{relative}")

    require("whole semi-directed maps" in all_tex, "WHOLE_MAP_TI_CLAUSE_MISSING")
    require(
        "A rooted restriction type\nis not used as a topology oracle" in supplement,
        "ROOTED_ORACLE_REJECTION_MISSING",
    )
    require(
        "not asserted to be a\ngraph-transport quotient" in article,
        "RESTORATION_NONQUOTIENT_CLAUSE_MISSING",
    )
    require(
        "not\nmisreported as three literal polynomials" in article,
        "DIRECT36_LITERAL_BODY_WARNING_MISSING",
    )
    require(
        "It does not assert equality of the complete\nstochastic images" in article,
        "COMPLETE_IMAGE_NONCLAIM_GUARD_MISSING",
    )
    require("Huber et al." in article and "HuberEtAl2025" in all_tex, "HUBER_ATTRIBUTION_MISSING")
    require(
        "topology-only primitive theorem of Englander" not in article,
        "STALE_ENGLANDER_OVERATTRIBUTION",
    )
    require(
        "Complete graph-derived marginal descriptor" in article
        and "tensor-invisible" in article
        and "not an inheritance-complement quotient" in article,
        "MARGINAL_DESCRIPTOR_GUARDS_MISSING",
    )
    require(
        "analytic submersion theorem" in article
        and "J_0=" in article
        and "J_\\perp=" in article
        and "The inverse function theorem gives strict analytic sections" not in article,
        "TRIANGLE_SUBMERSION_REPAIR_MISSING",
    )
    require(
        "repair-tagged directed completion descriptors" in article
        and "untagged cycle convention" in article,
        "REPAIR_TAGGED_COMPLETION_SEMANTICS_MISSING",
    )
    require(
        "23 literal quadratic bodies" in certificate_tex
        and "Five high-degree bases" in certificate_tex
        and "Three worked paths" in certificate_tex
        and "schema/version" in certificate_tex,
        "PRINTED_CERTIFICATE_APPENDIX_INCOMPLETE",
    )
    require(
        "\\input{compression_tables.tex}" in supplement
        and "\\IfFileExists{compression_tables.tex}" not in supplement,
        "COMPRESSION_TABLE_NOT_FAIL_CLOSED",
    )
    require(
        "At most one pole is reticulate" in article
        and "no source or\nreticulation-event placement is omitted" in article
        and "minimal transversals of these clause families" in article,
        "DIRECTED_CORE_OR_REPAIR_EXHAUSTIVENESS_MISSING",
    )
    require(
        "r\\le|\\X|-1" in article and "4|\\X|-3" in article,
        "TOPOLOGY_FINITE_UNION_BOUND_MISSING",
    )
    require(
        "All output-row indices below are zero-based" in article
        and "output-row indices in the following table are zero-based"
        in supplement,
        "SHARPNESS_ROW_INDEX_CONVENTION_MISSING",
    )
    require(
        "q\\in\\bigcup_{H\\in\\mathcal C}\\M_+(H)" in article
        and "terminates by quantifier elimination" in article
        and "exactly one class is feasible" in article,
        "RECONSTRUCTION_RIGID_SUPPORT_STEP_INCOMPLETE",
    )
    require(
        "polynomial-sign decisions" in article
        and "exact-real oracle" in article
        and "not a\nbit-complexity or numerical-stability claim" in article,
        "EXACT_INPUT_CONVENTION_UNDEFINED",
    )
    require(
        "s_{ZX}" in article and "s_{VX_1}" in article
        and "WEAK_SHARPNESS_COLUMN_CROSSWALK.json" in supplement,
        "NAMED_SHARPNESS_COLUMNS_MISSING",
    )
    require(
        "Proposition~2.8.2" in article and "generic complex Jacobian rank" in article,
        "GENERIC_DIMENSION_HARDENING_MISSING",
    )
    require(
        "total} source\nrank-drop locus" in article
        and "\\Phi_N(R_N)" in article
        and "deleting \\(\\Phi_N(R_N)\\) cannot lower\nits dimension" in article,
        "TOTAL_RANK_DROP_IMAGE_ARGUMENT_MISSING",
    )
    normalized_compression = " ".join(compression.split())
    normalized_supplement = " ".join(supplement.split())
    replay_layer_count = len(full_layers)
    require(
        "original frozen principal-domain computational-evidence lock" in normalized_compression
        and "For C01--C10 and C12--C13" in normalized_compression
        and "global C11 entry" in normalized_compression
        and "exact candidate commit, layer count, wall and internal times" in normalized_compression
        and "externally bound replay artifacts and generated theorem-to-artifact crosswalk" in normalized_compression
        and "No byte-bound end-to-end quick-suite runtime is claimed" in normalized_compression
        and "No byte-bound end-to-end quick or full runtime is present" not in normalized_compression
        and "exact candidate commit, layer count, internal and wall times" in normalized_supplement
        and "without a self-referential source edit after the run" in normalized_supplement
        and "1e9ff6c6" not in normalized_supplement,
        "RUNTIME_BOUNDARY_WORDING_STALE",
    )
    require(
        "finite principal-domain theorem and classification universe remain unchanged"
        in normalized_supplement.lower()
        and "separately versioned submission sources"
        in normalized_supplement.lower(),
        "COMPUTATIONAL_LOCK_SOURCE_VERSION_DISTINCTION_MISSING",
    )

    require(
        "F_A&=q_{CCCC}-q_{CCTT}" in article
        and "G_B&=q_{CCCC}-q_{CCTT}-q_{CTTC}+q_{CTCT}" in article
        and "q_{GGGG}-q_{GGTT}" not in article,
        "CORRECTED_QUARTET_FORMULAS_NOT_PRINTED",
    )
    active_metadata_source = article + "\n" + supplement
    require(
        "pending human" not in active_metadata_source.lower()
        and "pending explicit human confirmation" not in active_metadata_source.lower(),
        "STALE_PENDING_HUMAN_METADATA",
    )
    for approved in (
        "me@aleckriebel.com",
        "No specific funding supported this work.",
        "The author declares no competing interests.",
        "k2p-same-biorxiv-v1.0.1",
        "CC BY 4.0",
        "MIT License",
        "no DOI is claimed",
    ):
        require(approved in active_metadata_source, f"APPROVED_METADATA_MISSING:{approved}")
    require(
        "No GitHub\nRelease, Zenodo deposit, or DOI is claimed" in supplement,
        "EXTERNAL_RELEASE_BOUNDARY_MISSING",
    )
    licenses = license_path.read_text(encoding="utf-8")
    normalized_licenses = " ".join(licenses.split())
    require(
        "Creative Commons Attribution 4.0 International License" in normalized_licenses
        and "MIT License" in normalized_licenses,
        "LICENSE_FILE_INCOMPLETE",
    )

    findings: list[dict[str, object]] = []
    local_relation_is_defined = (
        "\\Theta_+(H)" in article
        or "projective local containment" in article.lower()
        or "ported-factor containment" in article.lower()
    )
    if "H\\preceqplus H'" in article and not local_relation_is_defined:
        findings.append(
            {
                "severity": "major_formal",
                "code": "LOCAL_PROJECTIVE_RELATION_UNDEFINED",
                "lines": [
                    line_number(article, "source-relative full-dimensional regular germ"),
                    line_number(article, "H\\preceqplus H'"),
                ],
            }
        )

    if (
        "smooth\nsemialgebraic constant-rank strata" in article
        and "Nash" not in article
        and "physical analytic target section" in article
    ):
        findings.append(
            {
                "severity": "major_formal",
                "code": "ANALYTIC_SECTION_NOT_JUSTIFIED_BY_SMOOTH_STRATIFICATION",
                "lines": [
                    line_number(article, "semialgebraic constant-rank strata"),
                    line_number(article, "constant-rank theorem supplies a physical analytic"),
                ],
            }
        )

    if (
        "Adjoin the zero\nsets of only those finitely many" in article
        and "\\V_N\\cap Z(" not in article
    ):
        findings.append(
            {
                "severity": "major_formal",
                "code": "PARAMETER_PULLBACK_ZERO_SET_ADJOINED_TO_OUTPUT_VARIETY",
                "lines": [line_number(article, "sets of only those finitely many")],
                "note": (
                    "Use output zero sets V_N intersect Z(P), with nonzero "
                    "P composed with Phi_N proving properness; use closures of "
                    "images for parameter-only rank loci."
                ),
            }
        )

    if "\\binom" not in article + supplement + compression:
        findings.append(
            {
                "severity": "minor_exposition",
                "code": "CLAIMED_COMPLETION_FORMULA_NOT_DISPLAYED_IN_PAPER",
                "lines": [line_number(article, "one stars-and-bars formula")],
            }
        )

    if "three orbit propositions" in article:
        findings.append(
            {
                "severity": "minor_precision",
                "code": "ORBIT_WORDING_BROADER_THAN_CERTIFIED_FAMILY_WORDING",
                "lines": [line_number(article, "three orbit propositions")],
            }
        )

    if "Q_{j=C,a=C,b=0" not in all_tex:
        findings.append(
            {
                "severity": "moderate_proof_exposition",
                "code": "CHERRY_QUANTITIES_NOT_SHOWN_TO_BE_TENSOR_OBSERVABLES",
                "lines": [line_number(article, "use the four local observables")],
                "note": (
                    "The exact Fourier ratios and recovery-by-division are "
                    "available in work/weak_sharpness_audit/PROOF_AUDIT.md."
                ),
            }
        )

    crosswalk_fields = (
        "schema/version",
        "producer command",
        "replay command",
        "mutation command",
        "file SHA-256",
    )
    if not all(field in supplement_source for field in crosswalk_fields):
        findings.append(
            {
                "severity": "moderate_submission",
                "code": "READER_CROSSWALK_OMITS_REQUESTED_PER_LAYER_FIELDS",
                "lines": [
                    line_number(supplement, "Theorem-to-artifact crosswalk"),
                    line_number(supplement, "Frozen hash anchors"),
                    line_number(supplement, "Replay protocol"),
                ],
                "note": (
                    "The machine-readable crosswalk carries more detail, but "
                    "the reader supplement does not tabulate every requested "
                    "schema/payload/runtime/command field per theorem layer."
                ),
            }
        )

    sharpness = re.search(
        r"\\begin\{theorem\}\[Weak-class.*?\\end\{theorem\}",
        article,
        flags=re.DOTALL,
    )
    require(sharpness is not None, "SHARPNESS_THEOREM_MISSING")
    if "full-dimensional" not in sharpness.group(0):
        findings.append(
            {
                "severity": "minor_precision",
                "code": "SHARPNESS_STATEMENT_OMITS_FULL_DIMENSIONAL_QUALIFIER",
                "lines": [line_number(article, "contain a common regular analytic germ")],
            }
        )

    if "\\M_{\\mathrm{CT}}(N)" not in article:
        findings.append(
            {
                "severity": "minor_definition",
                "code": "CONTINUOUS_TIME_IMAGE_AND_MAXIMAL_RANK_NOT_DEFINED",
                "lines": [line_number(article, "\\Theta_{\\mathrm{CT}}(N)")],
                "note": (
                    "Define the CT image and note that openness gives the same "
                    "maximal rank and complex image closure as the principal domain."
                ),
            }
        )

    englander = re.search(
        r"@article\{EnglanderEtAl2026,.*?year\s*=\s*\{(\d{4})\}",
        bib,
        flags=re.DOTALL,
    )
    require(englander is not None, "ENGLANDER_BIB_ENTRY_MISSING")
    if englander.group(1) != "2025":
        findings.append(
            {
                "severity": "minor_bibliography",
                "code": "ENGLANDER_ISSUED_YEAR_NEEDS_RECONCILIATION",
                "lines": [offset_line(bib, englander.start(1))],
                "note": "Crossref issued/posted metadata are 24 April 2025; version 4 is dated 4 July 2026.",
            }
        )

    require(
        not findings,
        "OPEN_ARTICLE_FINDINGS:"
        + ",".join(str(row.get("code")) for row in findings),
    )
    result = {
        "schema": "k2p-submission-article-static-audit-v2",
        "status": "PASS",
        "source_sha256": {
            "article/main.tex": sha256(article_path),
            "article/references.bib": sha256(bib_path),
            "supplement/supplement.tex": sha256(supplement_path),
            "supplement/compression_tables.tex": sha256(compression_path),
            "supplement/certificate_appendix.tex": sha256(certificate_tex_path),
            "templates/PRINTED_CERTIFICATE_APPENDIX.json": sha256(certificate_json_path),
            "analysis/WEAK_SHARPNESS_COLUMN_CROSSWALK.json": sha256(sharpness_columns_path),
        },
        "frozen_release_sha256": sha256(release_path),
        "clean_full_replay": {
            "status": full_replay["status"],
            "layers": replay_layer_count,
            "wall_seconds": wall_seconds,
            "maximum_resident_set_size_bytes": full_replay_telemetry["time_l"]["maximum_resident_set_size_bytes"],
            "peak_memory_footprint_bytes": full_replay_telemetry["time_l"]["peak_memory_footprint_bytes"],
            "report_sha256": sha256(full_replay_path),
            "telemetry_sha256": sha256(full_replay_telemetry_path),
        },
        "frozen_counts": expected_inputs,
        "new_exact_evidence": {
            "quartet_formula_transports": quartet["formula_transport_count"],
            "quartet_terminal_rows": terminal["aggregate"]["quartet_terminal_rows"],
            "quartet_terminal_certificate_ids": terminal["aggregate"]["per_layer_certificate_ids"],
            "canonicalizer_primitive_archetypes": canonicalizer["descriptor_audit"]["primitive_archetypes_compared"],
            "canonicalizer_strict_relation_presentations": canonicalizer["relation_audit"]["rank_and_topology_eligible_presentations"],
            "probe_parameter_transports": parameter_transport["ledgers"]["probe_relations"]["rows"],
            "probe_restriction_occurrences": parameter_transport["ledgers"]["probe_restrictions"]["rows"],
            "restoration_restriction_occurrences": parameter_transport["ledgers"]["restoration_restrictions"]["rows"],
        },
        "submission_metadata": {
            "corresponding_email": "me@aleckriebel.com",
            "author_contributions": "approved sole-author contribution statement",
            "funding": "No specific funding supported this work.",
            "competing_interests": "The author declares no competing interests.",
            "paper_and_data_license": "CC BY 4.0",
            "code_license": "MIT",
            "immutable_submission_tag": "k2p-same-biorxiv-v1.0.1",
            "doi": None,
            "external_release_actions_performed": False,
        },
        "findings": findings,
    }
    result["payload_sha256"] = canonical_hash(result)
    return result


if __name__ == "__main__":
    try:
        require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--write", action="store_true")
        group.add_argument("--check", action="store_true")
        args = parser.parse_args()
        audit = main()
        encoded = json.dumps(audit, indent=2, sort_keys=True) + "\n"
        output = Path(__file__).with_name("STATIC_AUDIT_RESULT.json")
        if args.write:
            output.write_text(encoded, encoding="utf-8")
        elif args.check:
            require(
                output.is_file()
                and not output.is_symlink()
                and output.read_text(encoding="utf-8") == encoded,
                "STATIC_AUDIT_RESULT_STALE",
            )
        print(encoded, end="")
    except AuditFailure as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        raise SystemExit(1) from exc

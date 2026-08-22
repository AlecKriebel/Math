#!/usr/bin/env python3
"""Build the deterministic reviewer-facing v1.1.7 proof-certificate bundle.

The selection below is intentionally explicit. It is the transitive closure
of the mathematical entry points, not a copy of the development worktree.
Sealing independently re-prepares that closure from the current clean source
commit, compares it byte-for-byte with the requested stage, and archives only
the fresh rebuild.
"""

from __future__ import annotations

import argparse
import csv
from functools import lru_cache
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile


PROJECT = Path(__file__).resolve().parents[1]
VERSION = "1.1.7"
ROOT_NAME = f"stc_jc_sharp_boundary_atlas_certificates_v{VERSION}"


def clean_subprocess_environment() -> dict[str, str]:
    """Minimal environment for Git and detached Python subprocesses."""
    allowed = {
        "PATH", "LANG", "LC_ALL", "LC_CTYPE", "TMPDIR", "TEMP", "TMP",
        "SYSTEMROOT",
    }
    environment = {
        key: value for key, value in os.environ.items() if key in allowed
    }
    environment["LC_ALL"] = "C"
    return environment

STATIC = (
    "README_FIRST.md", "PROOF_BOUNDARY.md", "THEOREM_CERTIFICATE_CROSSWALK.md",
    "ATLAS_SUMMARY.md", "REGENERATION_MAP.md", "RUNTIME_AND_HARDWARE.md",
    "CITATION.cff", "verify.sh",
)

PRIMARY_CODE = (
    "COMPACT_PROBE_SCHEMA.md", "atlas_compiler.py", "compact_probe_extension_compiler.py",
    "completion_universe.py", "core_universe.py", "cycle_theta_union_compiler.py",
    "graph_model.py", "hard_cover_compiler.py", "jc_tensor.py",
    "merge_bounded_relation_shards.py", "merge_compact_probe_shards.py",
    "merge_hard_cover_shards.py", "probe_extension_compiler.py", "seventh_invariant.json",
    "sign_certificate.py", "support_universe.py", "verify_bounded_relations.py",
    "verify_compact_probe_extension.py", "verify_hard_cover_artifacts.py",
    "verify_multihomogeneity.py", "verify_probe_extension.py",
    "verify_relation_hard_cover_crosswalk.py", "verify_triangle_redirection.py",
    "verify_zero_sum_root_normalization.py",
)

PRIMARY_CERTS = (
    "core_universe.json", "completion_universe.json", "support_universe.json",
    "invariant_multihomogeneity.json", "zero_sum_root_normalization.json",
    "jc_triangle_redirection_active.json", "descriptor_bits_cache.json.gz",
    "bounded_relation_n3_all_filtered_summary.json",
    "bounded_relation_n3_cycle_filtered_summary.json",
    "bounded_relation_n3_theta0_filtered_summary.json",
    "bounded_relation_n3_theta1_filtered_summary.json",
    "bounded_relation_n3_theta3_filtered_summary.json",
    "bounded_relations_n3_schema3_n3_cycle_filtered.jsonl.gz",
    "bounded_relations_n3_schema3_n3_theta0_filtered.jsonl.gz",
    "bounded_relations_n3_schema3_n3_theta1_filtered.jsonl.gz",
    "bounded_relations_n3_schema3_n3_theta3_filtered.jsonl.gz",
    "bounded_relation_n3_schema3_n3_all_filtered_graphs.jsonl.gz",
    "bounded_relation_n3_schema3_n3_all_filtered_polynomials.jsonl.gz",
    "bounded_relation_n3_schema3_n3_all_filtered_relations.jsonl.gz",
    "bounded_relation_n3_schema3_n3_all_filtered_signs.json",
    "bounded_relation_n3_hard_cover_crosswalk.jsonl.gz",
    "bounded_relation_n3_hard_cover_crosswalk.summary.json",
    "hard_cover_graphs_n3_schema3_n3_full.jsonl.gz",
    "hard_cover_n3_schema3_n3_full.jsonl.gz",
    "hard_cover_polynomials_n3_schema3_n3_full.jsonl.gz",
    "hard_cover_root_cases_n3_schema3_n3_full.jsonl.gz",
    "hard_cover_schema3_n3_full_summary.json",
    "hard_cover_graphs_n4_schema3_theta2_full.jsonl.gz",
    "hard_cover_n4_schema3_theta2_full.jsonl.gz",
    "hard_cover_polynomials_n4_schema3_theta2_full.jsonl.gz",
    "hard_cover_root_cases_n4_schema3_theta2_full.jsonl.gz",
    "hard_cover_schema3_theta2_full_summary.json",
)

ROOT_PROBE = (
    "verify_active_structural.py", "verify_root_probe.py", "verify_probe_coherence.py",
    "verify_incoming_coverage.py", "verify_parameter_submersion.py",
    "root_probe_certificate.json", "probe_coherence_certificate.json",
    "incoming_coverage_certificate.json", "parameter_submersion_certificate.json",
    "counterexamples/fixed_incoming_relative_role.json",
)

N3_UNIVERSE = (
    "generate_universe.py", "verify_manifest.py", "n3_universe_certificate.json",
    "n3_normalized_raw_relations.jsonl.gz", "n3_normalized_merged_relations.jsonl.gz",
)

BOUNDED_CLEANROOM = (
    "cleanroom_verify.py", "INPUT_LOCK.json",
)

THETA_GATE = (
    "verify_gate.py", "canonicalize_relations.py", "verify_manifest.py",
    "signature_certificate.json", "canonical_quotient_certificate.json",
    "presentation_crosswalk.jsonl", "canonical_duplicate_transports.jsonl",
    "frozen_presentation_transports.jsonl", "mutation_results.json",
)

FINAL_HARD_COVER = (
    "audit_candidate_stream.py", "derived_invariants.py", "family_engine.py",
    "graph_model.py", "jc_exact.py", "pq_extension.py", "relation_universe.py",
    "mutation_schema3_stream.py", "verify_schema3_n4_certificates.py",
    "certificates/schema3_n3_path_audit.json",
    "certificates/schema3_n4_theta2_full_audit.json",
    "certificates/schema3_n4_theta2_mutation_certificate.json",
    "certificates/schema3_n4_theta2_terminal_records.jsonl.gz",
    "certificates/family_n3.json.gz",
    "certificates/family_n4_minimum.json.gz",
)

COMPACT_GATE = (
    "COMPACT_PROBE_SCHEMA_LOCKED.md", "TRACKED_INPUTS.json", "semantic_gate.py",
    "mutation_tests.py", "invariant_templates.py", "verify_tracked_inputs.py",
    "verify_quick.py", "certificates/compact_only_semantic_replay.json",
    "certificates/mutation_tests.json",
)


@lru_cache(maxsize=1)
def source_provenance() -> tuple[str, bool]:
    override = os.environ.get("STC_JC_SOURCE_COMMIT")
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=PROJECT.parent, text=True,
            env=clean_subprocess_environment(),
        ).strip()
        status = subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=all", "--",
             PROJECT.name],
            cwd=PROJECT.parent, text=True, env=clean_subprocess_environment(),
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        if override and os.environ.get("STC_JC_ALLOW_DIRTY_SOURCE") == "1":
            return override, False
        raise AssertionError("cannot determine certificate source provenance")
    clean = not status
    if override:
        if os.environ.get("STC_JC_ALLOW_DIRTY_SOURCE") != "1":
            raise AssertionError(
                "STC_JC_SOURCE_COMMIT is permitted only for an explicitly unsealed dry run"
            )
        return override, False
    if not clean and os.environ.get("STC_JC_ALLOW_DIRTY_SOURCE") != "1":
        raise AssertionError(
            "refusing to seal a certificate bundle from a dirty project tree"
        )
    return commit, clean


def source_commit() -> str:
    return source_provenance()[0]


def require_unchanged_clean_source(expected_commit: str) -> None:
    """Reject a checkout change during fresh preparation or archive creation."""
    source_provenance.cache_clear()
    commit, clean = source_provenance()
    if not clean or commit != expected_commit:
        raise AssertionError({
            "source_changed_during_seal": True,
            "expected_commit": expected_commit,
            "observed_commit": commit,
            "observed_clean": clean,
        })


def export_project_commit(commit: str, destination: Path) -> Path:
    """Export the tracked project bytes from exactly ``commit``.

    The release payload is never rebuilt from the ambient working tree.  This
    excludes ignored and untracked files by construction.
    """
    destination.mkdir(parents=True, exist_ok=True)
    archive_path = destination.parent / "source-commit.tar"
    with archive_path.open("wb") as stream:
        subprocess.run(
            ["git", "archive", "--format=tar", commit, "--", PROJECT.name],
            cwd=PROJECT.parent,
            env=clean_subprocess_environment(),
            stdout=stream,
            check=True,
        )
    root = destination.resolve()
    with tarfile.open(archive_path, "r:") as archive:
        members = archive.getmembers()
        for member in members:
            target = (destination / member.name).resolve()
            if target != root and root not in target.parents:
                raise AssertionError(f"unsafe Git-archive path: {member.name}")
            if member.issym() or member.islnk():
                raise AssertionError(f"symlink not permitted in source export: {member.name}")
        archive.extractall(destination)
    archive_path.unlink()
    project = destination / PROJECT.name
    if not project.is_dir():
        raise AssertionError("Git archive omitted the project directory")
    return project


def prepare_from_commit(commit: str, stage: Path, scratch: Path) -> None:
    """Run the committed builder against an isolated export of ``commit``."""
    exported_project = export_project_commit(commit, scratch / "source")
    committed_builder = exported_project / "reproducibility/build_certificate_bundle.py"
    if not committed_builder.is_file():
        raise AssertionError("recorded commit lacks the certificate builder")
    # Do not inherit Python startup hooks.  ``-I`` ignores PYTHON* variables,
    # while ``-S`` disables global ``sitecustomize``; the explicit allow-list
    # also keeps startup variables out of the child environment.
    environment = clean_subprocess_environment()
    environment["STC_JC_SOURCE_COMMIT"] = commit
    environment["STC_JC_ALLOW_DIRTY_SOURCE"] = "1"
    result = subprocess.run(
        [sys.executable, "-I", "-S", str(committed_builder),
         "prepare", "--stage", str(stage)],
        cwd=exported_project,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise AssertionError({
            "committed_prepare_failed": True,
            "exit_status": result.returncode,
            "stdout": result.stdout[-2000:],
            "stderr": result.stderr[-2000:],
        })


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def payload_records(stage: Path) -> dict[str, tuple[int, int, str]]:
    """Return the exact pre-seal payload, including executable-mode bits."""
    excluded = {"ACTIVE_MANIFEST.json", "SHA256SUMS"}
    records: dict[str, tuple[int, int, str]] = {}
    for path in sorted(stage.rglob("*")):
        if (not path.is_file() or path.name in excluded
                or "__pycache__" in path.parts):
            continue
        relative = path.relative_to(stage).as_posix()
        records[relative] = (
            path.stat().st_size,
            path.stat().st_mode & 0o111,
            digest(path),
        )
    return records


def payload_commitment(records: dict[str, tuple[int, int, str]]) -> str:
    """Commit to every payload path, byte count, executable bit, and digest."""
    commitment = hashlib.sha256()
    for relative, (size, executable_bits, sha256) in sorted(records.items()):
        commitment.update(relative.encode("utf-8") + b"\0")
        commitment.update(str(size).encode("ascii") + b"\0")
        commitment.update(f"{executable_bits:o}".encode("ascii") + b"\0")
        commitment.update(sha256.encode("ascii") + b"\n")
    return commitment.hexdigest()


def require_identical_payload(candidate: Path, fresh: Path) -> str:
    """Reject a stale, incomplete, or locally altered prepared stage."""
    candidate_records = payload_records(candidate)
    fresh_records = payload_records(fresh)
    if candidate_records != fresh_records:
        candidate_keys = set(candidate_records)
        fresh_keys = set(fresh_records)
        missing = sorted(fresh_keys - candidate_keys)[:5]
        extra = sorted(candidate_keys - fresh_keys)[:5]
        changed = sorted(
            key for key in candidate_keys & fresh_keys
            if candidate_records[key] != fresh_records[key]
        )[:5]
        raise AssertionError({
            "stage_does_not_match_clean_source": True,
            "missing": missing,
            "extra": extra,
            "changed": changed,
        })
    return payload_commitment(fresh_records)


def copy_file(relative: str | Path, stage: Path) -> None:
    relative = Path(relative)
    source = PROJECT / relative
    if not source.is_file():
        raise FileNotFoundError(relative)
    destination = stage / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if source.suffix == ".sh" or os.access(source, os.X_OK):
        destination.chmod(destination.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def copy_file_as(source_relative: str | Path, destination_relative: str | Path,
                 stage: Path) -> None:
    source = PROJECT / Path(source_relative)
    destination = stage / Path(destination_relative)
    if not source.is_file():
        raise FileNotFoundError(source_relative)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if source.suffix == ".sh" or os.access(source, os.X_OK):
        destination.chmod(destination.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP
                          | stat.S_IXOTH)


def copy_group(prefix: str, names: tuple[str, ...], stage: Path) -> None:
    for name in names:
        copy_file(Path(prefix) / name, stage)


def compact_certificates() -> tuple[str, ...]:
    names: list[str] = []
    for shard in range(4):
        names.extend((
            f"compact_probe_paths_schema3_n3_compact_s{shard}.jsonl.gz",
            f"compact_probe_polynomials_schema3_n3_compact_s{shard}.jsonl.gz",
            f"compact_probe_schema3_n3_compact_s{shard}_summary.json",
            f"compact_probe_transports_schema3_n3_compact_s{shard}.jsonl.gz",
            f"compact_probe_witnesses_schema3_n3_compact_s{shard}.jsonl.gz",
            f"compact_probe_paths_theta2_compact_n4_s{shard}.jsonl.gz",
            f"compact_probe_polynomials_theta2_compact_n4_s{shard}.jsonl.gz",
            f"compact_probe_theta2_compact_n4_s{shard}_summary.json",
            f"compact_probe_transports_theta2_compact_n4_s{shard}.jsonl.gz",
            f"compact_probe_witnesses_theta2_compact_n4_s{shard}.jsonl.gz",
        ))
    return tuple(names)


def copy_direct_anchor(stage: Path) -> None:
    copy_group("reviews/direct_anchor_probe_closure", (
        "compile_direct_anchor_probes.py", "exact_engine.py", "mutation_tests.py",
        "verify_direct_anchor_probes.py", "certificates/anchors.jsonl.gz",
        "certificates/graphs.jsonl.gz", "certificates/p_relations.jsonl.gz",
        "certificates/q_relations.jsonl.gz", "certificates/witnesses.jsonl.gz",
        "certificates/summary.json", "certificates/mutation_results.json",
    ), stage)


def copy_omega(stage: Path) -> None:
    copy_file_as(
        "omega_audit/frozen_input/historical/jc_omega_move.json",
        "sharpness/omega/inputs/jc_omega_move.json", stage,
    )
    historical = (
        "enumerate_four_leaf_root_theta.py", "enumerate_theta_orientation_cores.py",
        "fourier_models.py", "generic_fourier_network.py", "model_robustness_invariants.py",
        "probe_four_leaf_jc_atlas.py", "verify_jc_four_network_class.py",
        "verify_jc_omega_move.py", "verify_jc_omega_move_stdlib.py",
        "verify_model_robustness.py",
    )
    for name in historical:
        copy_file_as(
            f"omega_audit/frozen_input/historical/src/{name}",
            f"sharpness/omega/inputs/producer_engine/{name}", stage,
        )
    copy_file_as(
        "omega_audit/frozen_input/prior_audit/independent/audit_omega_algebra.py",
        "sharpness/omega/cleanroom/algebra_engine.py", stage,
    )
    copy_file_as(
        "omega_audit/frozen_input/prior_audit/independent/audit_omega_graphs.py",
        "sharpness/omega/cleanroom/graph_engine.py", stage,
    )
    copy_file_as(
        "omega_audit/frozen_input/prior_audit/independent/exact_fourier.py",
        "sharpness/omega/cleanroom/exact_fourier.py", stage,
    )
    for name in ("verify_omega_release.py", "verify_omega_rank_readability.py"):
        copy_file_as(
            f"omega_audit/independent/{name}",
            f"sharpness/omega/cleanroom/{name}", stage,
        )
    for source_name, destination_name in (
        ("probe_four_leaf_jc_atlas.py", "probe_four_leaf_jc_atlas.py"),
        ("verify_orbit_constant.py", "verify_orbit_constant.py"),
        ("run_historical_omega.py", "run_producer_replay.py"),
    ):
        copy_file_as(
            f"omega_audit/runtime_compat/{source_name}",
            f"sharpness/omega/compat/{destination_name}", stage,
        )

    release = stage / "sharpness/omega/cleanroom/verify_omega_release.py"
    release.write_text(
        release.read_text(encoding="utf-8")
        .replace("``omega_audit/frozen_input/prior_audit/independent``",
                 "the co-located clean-room engines")
        .replace("ROOT = HERE.parents[1]", "ROOT = HERE.parents[2]")
        .replace('FROZEN = ROOT / "omega_audit" / "frozen_input"',
                 'FROZEN = HERE.parent / "inputs"')
        .replace('CERTIFICATE = FROZEN / "historical" / "jc_omega_move.json"',
                 'CERTIFICATE = FROZEN / "jc_omega_move.json"')
        .replace('INDEPENDENT = FROZEN / "prior_audit" / "independent"',
                 'INDEPENDENT = HERE')
        .replace('INDEPENDENT / "audit_omega_graphs.py"',
                 'INDEPENDENT / "graph_engine.py"')
        .replace('INDEPENDENT / "audit_omega_algebra.py"',
                 'INDEPENDENT / "algebra_engine.py"'),
        encoding="utf-8",
    )
    rank = stage / "sharpness/omega/cleanroom/verify_omega_rank_readability.py"
    rank.write_text(
        rank.read_text(encoding="utf-8")
        .replace("ROOT = HERE.parents[1]", "ROOT = HERE.parents[2]")
        .replace('INDEPENDENT = ROOT / "omega_audit/frozen_input/prior_audit/independent"',
                 'INDEPENDENT = HERE')
        .replace('CERTIFICATE = ROOT / "omega_audit/frozen_input/historical/jc_omega_move.json"',
                 'CERTIFICATE = HERE.parent / "inputs/jc_omega_move.json"'),
        encoding="utf-8",
    )
    orbit = stage / "sharpness/omega/compat/verify_orbit_constant.py"
    orbit.write_text(
        orbit.read_text(encoding="utf-8")
        .replace('HERE.parent\n    / "frozen_input"\n    / "historical"\n    / "src"',
                 'HERE.parent\n    / "inputs"\n    / "producer_engine"'),
        encoding="utf-8",
    )
    producer = stage / "sharpness/omega/compat/run_producer_replay.py"
    producer.write_text(
        producer.read_text(encoding="utf-8")
        .replace("Execute the untouched historical Omega proof",
                 "Execute the immutable active Omega producer proof")
        .replace('HISTORICAL = HERE.parent / "frozen_input" / "historical" / "src"',
                 'PRODUCER = HERE.parent / "inputs" / "producer_engine"')
        .replace('SCRIPT = HISTORICAL / "verify_jc_omega_move.py"',
                 'SCRIPT = PRODUCER / "verify_jc_omega_move.py"')
        .replace("str(HISTORICAL)", "str(PRODUCER)"),
        encoding="utf-8",
    )


def copy_theta(stage: Path) -> None:
    for source_name, destination_name in (
        ("networks.json", "inputs/networks.json"),
        ("verify_math.py", "verify_math.py"),
        ("verify_primary.py", "verify_primary.py"),
        ("independent/verify_sharpness.py", "cleanroom/verify_sharpness.py"),
        ("independent/instance.json", "cleanroom/instance.json"),
        ("independent/expected_certificate.json", "cleanroom/expected_certificate.json"),
    ):
        copy_file_as(
            f"s_tc_jc_sharp_boundary/reproducibility/{source_name}",
            f"sharpness/theta/{destination_name}", stage,
        )
    # The producer scripts use paths relative to the former project directory.
    for name in ("verify_math.py", "verify_primary.py"):
        path = stage / "sharpness/theta" / name
        path.write_text(
            path.read_text(encoding="utf-8")
            .replace('HERE / "networks.json"', 'HERE / "inputs/networks.json"')
            .replace('HERE / "independent/', 'HERE / "cleanroom/'),
            encoding="utf-8",
        )


def prepare(stage: Path) -> None:
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    static = PROJECT / "certificate_bundle"
    for name in STATIC:
        destination = stage / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(static / name, destination)
        if name.endswith(".sh"):
            destination.chmod(destination.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    for path in sorted((static / "verifiers").glob("*.py")):
        destination = stage / "verifiers" / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)

    copy_group("primary", PRIMARY_CODE, stage)
    copy_group("primary/certificates", PRIMARY_CERTS + compact_certificates(), stage)
    copy_group("reviews/root_probe", ROOT_PROBE, stage)
    copy_group("reviews/n3_universe_generator", N3_UNIVERSE, stage)
    copy_group("reviews/bounded_directed_relation_cleanroom", BOUNDED_CLEANROOM, stage)
    copy_group("reviews/theta2_signature_gate", THETA_GATE, stage)
    copy_group("reviews/final_hard_cover_cleanroom", FINAL_HARD_COVER, stage)
    copy_group("reviews/compact_probe_clean_clone_gate", COMPACT_GATE, stage)
    copy_direct_anchor(stage)

    copy_group("reviews/final_standard_convention", ("verify_conventions.py", "convention_certificate.json"), stage)
    copy_group("reviews/global_bridge", (
        "exact_audit.py", "mutation_tests.py", "exact_audit_certificate.json",
        "mutation_certificate.json", "verify_palette_cleanroom.py",
        "palette_cleanroom_certificate.json", "upstream_bridge_replay.json",
        "upstream_cut_replay.json", "upstream_mutation_replay.json",
    ), stage)
    copy_group("independent/bridge_cut", (
        "PROOF.md", "CUT_PALETTE_REDUCTION.md", "verify_bridge.py",
        "verify_palette_reduction.py", "verify_cut.py", "verify_mutations.py",
        "bridge_certificate.json", "palette_reduction_certificate.json",
        "cut_certificate.json", "mutation_certificate.json",
    ), stage)
    copy_group("reviews/base_gate_adversarial_referee_n3", (
        "referee_n3.py", "regenerate_strict_factors.py", "certificate.json",
        "strict_factor_certificate.json", "mutation_results.json",
    ), stage)
    copy_group("reviews/base_gate_adversarial_referee", (
        "referee.py", "certificate.json", "mutation_results.json",
    ), stage)
    copy_group("reviews/compact_probe_format/final_n3_cleanroom", ("engine_n3.py",), stage)
    copy_group("reviews/compact_probe_format/final_n4_cleanroom", ("engine.py",), stage)
    copy_group("reviews/triangle_redirection_cleanroom", (
        "cleanroom_verify.py", "certificate.json", "mutation_results.json",
    ), stage)
    copy_file("strong_level2_phylo_identifiability/src/jc_root_spanning_atlas_data.py", stage)
    copy_file("docs/DEFINITIONS_LOCK.md", stage)
    copy_omega(stage)
    copy_theta(stage)

    (stage / "environment").mkdir()
    (stage / "environment/requirements.txt").write_text(
        "mpmath==1.3.0\nnetworkx==3.2.1\nsympy==1.14.0\n", encoding="utf-8"
    )
    (stage / "environment/exact_tool_versions.txt").write_text(
        "Python >= 3.10\nmpmath 1.3.0\nnetworkx 3.2.1\nsympy 1.14.0\n", encoding="utf-8"
    )
    (stage / "LICENSES").mkdir()
    shutil.copy2(PROJECT / "s_tc_jc_sharp_boundary/LICENSE-CODE.txt",
                 stage / "LICENSES/CODE_MIT.txt")

    lock_path = stage / "reviews/compact_probe_clean_clone_gate/TRACKED_INPUTS.json"
    lock = json.loads(lock_path.read_text())
    for row in lock["inputs"]:
        row["path"] = row["path"].removeprefix("s_tc_jc_landmark_closure/")
    # This hash records the commit that originally produced the compact-probe
    # input lock.  It is provenance for that component, not the source commit
    # of the assembled bundle (which is recorded in ACTIVE_MANIFEST.json and
    # the external envelope).
    producer_commit = lock.pop("git_commit", None)
    lock["producer_commit"] = producer_commit or source_commit()
    lock_path.write_text(json.dumps(lock, sort_keys=True, indent=2) + "\n")
    verifier_path = stage / "reviews/compact_probe_clean_clone_gate/verify_tracked_inputs.py"
    verifier_path.write_text(
        verifier_path.read_text().replace("REPO = HERE.parents[2]", "REPO = HERE.parents[1]")
    )

    build_atlas_index(stage)
    build_expected_counts(stage)


def gzip_csv(path: Path, fields: tuple[str, ...], rows: list[dict]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)


def build_atlas_index(stage: Path) -> None:
    atlas = stage / "atlas"
    atlas.mkdir()
    module_path = stage / "verifiers/evidence_bindings.py"
    spec = importlib.util.spec_from_file_location("bundle_evidence_builder", module_path)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load evidence-binding builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    closure_rows = module.reconstruct_closure_rows(stage)
    module.write_rows(
        atlas / "COMPACT_PATH_CLOSURE_BINDINGS.jsonl.gz", closure_rows[0]
    )
    module.write_rows(
        atlas / "RESTORATION_CLOSURE_BINDINGS.jsonl.gz", closure_rows[1]
    )
    module.write_rows(
        atlas / "DIRECT_ANCHOR_CLOSURE_BINDINGS.jsonl.gz", closure_rows[2]
    )
    evidence_rows = module.reconstruct_rows(stage, closure_rows)
    module.write_rows(atlas / "ATLAS_EVIDENCE_BINDINGS.jsonl.gz", evidence_rows)

    # This compact table is for human navigation.  The JSONL file above is the
    # authoritative, verifier-reconstructed record-level evidence map.
    fields = (
        "universe", "relation_id", "presentation_ordinal", "source_graph_id",
        "target_graph_id", "direction", "disposition", "base_verifier",
        "closure_verifier", "evidence_binding_sha256",
    )
    rows = [{field: row.get(field, "") for field in fields} for row in evidence_rows]
    gzip_csv(atlas / "ATLAS_INDEX.csv.gz", fields, rows)


def build_expected_counts(stage: Path) -> None:
    expected = stage / "expected_outputs"
    expected.mkdir()
    counts = {
        "schema": "stc-jc-atlas-expected-counts-v1",
        "bounded_three_outgoing": {
            "raw_presentations": 10826, "canonical_relations": 10466,
            "strict": 5284, "pending_restoration": 5120, "isomorphism_or_T": 62,
        },
        "four_outgoing": {
            "completion_records": 6138, "raw_survivors": 192,
            "direct": 18, "rooting_duplicates": 42, "restoration_roots": 132,
        },
        "restoration_states": {"three_outgoing": 68584, "four_outgoing": 2106},
        "direct_anchors": {"one_port": 2642, "two_port": 18224},
        "compact_probes": {"three_outgoing": 101148, "four_outgoing": 168582},
        "record_level_closure_bindings": {
            "compact_paths": 276,
            "restoration_roots": 5476,
            "direct_anchors": 62,
        },
        "cut_word_reduction": {
            "balanced_four_through_eight_port_words": 808642,
            "direct_three_run_obstructions": 229988,
            "short_palette_reductions": 578654,
            "valid_reduced_palette_presentations": 379742,
            "all_switching_survivors": 0,
        },
    }
    (expected / "expected_counts.json").write_text(
        json.dumps(counts, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )


def seal(stage: Path, prepared_payload_sha256: str, source_commit_sha: str) -> None:
    files = []
    categories = {
        "primary": "primary generator or frozen exact certificate",
        "independent": "separately implemented replay",
        "reviews": "clean-room verifier or replay certificate",
        "sharpness": "active Omega and Theta sharpness inputs and verifiers",
        "atlas": "per-relation reviewer index",
        "verifiers": "standalone orchestration and integrity checks",
        "environment": "runtime lock", "LICENSES": "license",
        "expected_outputs": "machine-readable expected results",
    }
    for path in sorted(stage.rglob("*")):
        if (not path.is_file() or path.name in {"ACTIVE_MANIFEST.json", "SHA256SUMS"}
                or ".venv" in path.parts or "__pycache__" in path.parts):
            continue
        relative = path.relative_to(stage).as_posix()
        top = relative.split("/", 1)[0]
        files.append({
            "path": relative, "bytes": path.stat().st_size, "sha256": digest(path),
            "executable_bits": path.stat().st_mode & 0o111,
            "role": categories.get(top, "bundle metadata"),
        })
    payload = {
        "schema": "stc-jc-proof-bundle-manifest-v1", "version": VERSION,
        "source_commit": source_commit_sha,
        "source_tree_clean": True,
        "prepared_payload_sha256": prepared_payload_sha256,
        "paper_title": "Strong Tree-Childness Is a Sharp Generic-Identifiability Boundary for Level-2 Jukes-Cantor Networks",
        "files": files,
    }
    (stage / "ACTIVE_MANIFEST.json").write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    (stage / "SHA256SUMS").write_text(
        "\n".join(f"{row['sha256']}  {row['path']}" for row in files) + "\n",
        encoding="utf-8",
    )


def deterministic_tar(stage: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="stc-jc-tar-") as raw:
        plain = Path(raw) / "bundle.tar"
        with tarfile.open(plain, "w", format=tarfile.PAX_FORMAT) as archive:
            paths = [stage, *stage.rglob("*")]
            for path in sorted(paths, key=lambda p: p.relative_to(stage.parent).as_posix()):
                if ".venv" in path.parts or "__pycache__" in path.parts:
                    continue
                arcname = path.relative_to(stage.parent).as_posix()
                info = archive.gettarinfo(str(path), arcname)
                info.uid = info.gid = 0
                info.uname = info.gname = ""
                info.mtime = 0
                if path.is_file():
                    with path.open("rb") as handle:
                        archive.addfile(info, handle)
                else:
                    archive.addfile(info)
        with plain.open("rb") as source, output.open("wb") as raw_out:
            with gzip.GzipFile(filename="", fileobj=raw_out, mode="wb", mtime=0, compresslevel=9) as compressed:
                shutil.copyfileobj(source, compressed, length=1 << 20)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("prepare", "seal"))
    parser.add_argument("--stage", type=Path,
                        default=PROJECT / "release_artifacts" / ROOT_NAME)
    parser.add_argument("--output", type=Path,
                        default=PROJECT / "release_artifacts" / f"{ROOT_NAME}.tar.gz")
    args = parser.parse_args()
    if not sys.flags.isolated or not sys.flags.no_site:
        raise AssertionError(
            "certificate preparation and sealing require isolated Python "
            "with site startup disabled: invoke this script with `python -I -S`"
        )
    if args.command == "prepare":
        prepare(args.stage)
        print(args.stage)
        return
    # Never trust a previously prepared directory merely because the project
    # checkout is clean. Export the recorded Git object, run its committed
    # builder in isolation, compare every payload byte and executable bit, and
    # archive only that detached reconstruction. This rejects a modified
    # external --stage, a stale default stage, and ignored source injection.
    if not args.stage.is_dir():
        raise FileNotFoundError(args.stage)
    seal_commit = source_commit()
    with tempfile.TemporaryDirectory(prefix="stc-jc-source-bound-stage-") as raw:
        scratch = Path(raw)
        fresh_stage = scratch / ROOT_NAME
        fresh_archive = scratch / args.output.name
        prepare_from_commit(seal_commit, fresh_stage, scratch)
        payload_sha256 = require_identical_payload(args.stage, fresh_stage)
        require_unchanged_clean_source(seal_commit)
        seal(fresh_stage, payload_sha256, seal_commit)
        deterministic_tar(fresh_stage, fresh_archive)
        require_unchanged_clean_source(seal_commit)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        os.replace(fresh_archive, args.output)
        shutil.rmtree(args.stage)
        shutil.copytree(fresh_stage, args.stage, copy_function=shutil.copy2)
    checksum = digest(args.output)
    checksum_path = args.output.with_suffix(args.output.suffix + ".sha256")
    checksum_path.write_text(f"{checksum}  {args.output.name}\n", encoding="utf-8")
    previous_envelope = args.output.parent / "CERTIFICATE_BUNDLE_ENVELOPE.json"
    zenodo_doi = "ZENODO_DOI_PENDING"
    if previous_envelope.is_file():
        prior = json.loads(previous_envelope.read_text(encoding="utf-8"))
        zenodo_doi = prior.get("zenodo_doi", zenodo_doi)
    envelope = {
        "schema": "stc-jc-certificate-bundle-envelope-v1",
        "version": VERSION,
        "archive": args.output.name,
        "archive_sha256": checksum,
        "archive_bytes": args.output.stat().st_size,
        "source_commit": seal_commit,
        "source_tree_clean": True,
        "prepared_payload_sha256": payload_sha256,
        "zenodo_doi": zenodo_doi,
        "verification_commands": [
            "bash verify.sh quick",
            "bash verify.sh full",
            "bash verify.sh regenerate-all",
        ],
        "finite_universe": {"three_outgoing": 10466, "four_outgoing_survivors": 192},
    }
    envelope_path = previous_envelope
    envelope_path.write_text(json.dumps(envelope, sort_keys=True, indent=2) + "\n",
                             encoding="utf-8")
    print(json.dumps({"archive": str(args.output), "sha256": checksum}, sort_keys=True))


if __name__ == "__main__":
    main()

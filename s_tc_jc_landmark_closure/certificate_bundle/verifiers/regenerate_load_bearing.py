#!/usr/bin/env python3
"""Regenerate every load-bearing bounded-atlas stream from primitive inputs.

This program works in a disposable clone of the extracted bundle.  It invokes
the primary core/completion/support, atlas, hard-cover, crosswalk, compact
probe, and direct-anchor compilers, then runs the independent all-record n=4
symbolic audit.  Every regenerated final stream is compared with the frozen
proof object.  No development-repository file is required.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def logical_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    opener = gzip.open if path.suffix == ".gz" else open
    mode = "rb"
    with opener(path, mode) as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run(work: Path, *command: str) -> None:
    print("\n==> " + " ".join(command), flush=True)
    env = os.environ.copy()
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"})
    subprocess.run(command, cwd=work, env=env, check=True)


def restore_bundled_program(work: Path, relative: str) -> None:
    """Stage the immutable bundled program immediately before execution."""
    source = ROOT / relative
    destination = work / relative
    if not source.is_file():
        raise AssertionError(("missing bundled regeneration program", relative))
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    if sha256(source) != sha256(destination):
        raise AssertionError(("regeneration program staging mismatch", relative))


def normalize_json(value):
    if isinstance(value, dict):
        return {
            key: normalize_json(item)
            for key, item in sorted(value.items())
            if key not in {"elapsed_seconds", "summary_sha256"}
        }
    if isinstance(value, list):
        return [normalize_json(item) for item in value]
    if isinstance(value, str):
        for marker in ("primary/", "reviews/", "independent/"):
            position = value.find(marker)
            if position >= 0 and (position == 0 or value[position - 1] == "/"):
                return value[position:]
    return value


def compare_json(generated: Path, expected: Path) -> None:
    left = normalize_json(json.loads(generated.read_text(encoding="utf-8")))
    right = normalize_json(json.loads(expected.read_text(encoding="utf-8")))
    if left != right:
        raise AssertionError(("normalized JSON mismatch", generated, expected))


def normalized_n4_audit(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    summary_path = "primary/certificates/hard_cover_schema3_theta2_full_summary.json"
    value["inputs"].pop(summary_path, None)
    value.pop("normalized_sha256_without_hash", None)
    value["summary_audit"].pop("physical_sha256", None)
    return value


def compare_n4_audit(generated: Path, expected: Path) -> dict:
    value = normalized_n4_audit(generated)
    if value != normalized_n4_audit(expected):
        raise AssertionError(("substantive n4 audit mismatch", generated, expected))
    return value


def compare_exact(work: Path, relative: str, commitments: dict[str, object]) -> None:
    generated = work / relative
    expected = ROOT / relative
    if not generated.is_file() or not expected.is_file():
        raise AssertionError(("missing final proof object", relative))
    generated_logical = logical_sha256(generated)
    expected_logical = logical_sha256(expected)
    if generated_logical != expected_logical:
        raise AssertionError(("logical stream mismatch", relative,
                              generated_logical, expected_logical))
    commitments[relative] = {
        "logical_sha256": generated_logical,
        "frozen_physical_sha256": sha256(expected),
        "frozen_bytes": expected.stat().st_size,
    }


def primary_regeneration(work: Path) -> None:
    run(work, PYTHON, "primary/core_universe.py")
    run(work, PYTHON, "primary/completion_universe.py")
    run(work, PYTHON, "primary/support_universe.py")

    cache = "primary/certificates/descriptor_bits_cache.json.gz"
    cache_path = work / cache
    # The extracted proof object contains this performance cache so that
    # ordinary verification is fast.  A complete regeneration must not trust
    # it.  Delete it, reconstruct all descriptor bits from the freshly rebuilt
    # primitive core/completion/support inputs and invariant templates, and
    # require the reconstructed cache to equal the frozen one before any
    # downstream compiler is allowed to load it.
    if not cache_path.is_file():
        raise AssertionError(("missing frozen descriptor cache", cache))
    cache_path.unlink()
    if cache_path.exists():
        raise AssertionError(("failed to remove derived descriptor cache", cache))
    run(
        work, PYTHON, "primary/atlas_compiler.py", "--sizes", "3", "4",
        "--disable-target-signature-prefilter",
        "--write-bit-cache", cache,
        "--output", "primary/certificates/primitive_cache_regeneration_summary.json",
    )
    if sha256(cache_path) != sha256(ROOT / cache):
        raise AssertionError(("primitive cache regeneration mismatch", cache))

    shard_specs = (
        ("cycle", "schema3_n3_cycle_filtered", "bounded_relation_n3_cycle_filtered_summary.json"),
        ("theta-0", "schema3_n3_theta0_filtered", "bounded_relation_n3_theta0_filtered_summary.json"),
        ("theta-1", "schema3_n3_theta1_filtered", "bounded_relation_n3_theta1_filtered_summary.json"),
        ("theta-3", "schema3_n3_theta3_filtered", "bounded_relation_n3_theta3_filtered_summary.json"),
    )
    summaries = []
    for core, tag, summary_name in shard_specs:
        summary = f"primary/certificates/{summary_name}"
        summaries.append(summary)
        run(
            work, PYTHON, "primary/atlas_compiler.py", "--sizes", "3", "--relations",
            "--source-core-id", core, "--relation-tag", tag,
            "--load-bit-cache", cache, "--write-bit-cache", cache,
            "--output", summary,
        )
    merge_command = [
        PYTHON, "primary/merge_bounded_relation_shards.py",
        "--outgoing", "3", "--tag", "schema3_n3_all_filtered",
        "--output", "primary/certificates/bounded_relation_n3_all_filtered_summary.json",
    ]
    for summary in summaries:
        merge_command.extend(("--summary", summary))
    run(work, *merge_command)

    ranges = ((0, 1336), (1336, 2672), (2672, 4008), (4008, 5344))
    hard_summaries = []
    for shard, (start, stop) in enumerate(ranges):
        tag = f"schema3_n3_s{shard}"
        summary = f"primary/certificates/hard_cover_{tag}_summary.json"
        hard_summaries.append(summary)
        run(
            work, PYTHON, "primary/hard_cover_compiler.py", "--sizes", "3",
            "--bit-cache", cache, "--root-start", str(start), "--root-stop", str(stop),
            "--tag", tag, "--output", summary,
        )
    merge_command = [
        PYTHON, "primary/merge_hard_cover_shards.py",
        "--tag", "schema3_n3_full",
        "--output", "primary/certificates/hard_cover_schema3_n3_full_summary.json",
    ]
    for summary in hard_summaries:
        merge_command.extend(("--summary", summary))
    run(work, *merge_command)
    run(
        work, PYTHON, "primary/verify_relation_hard_cover_crosswalk.py",
        "--relation-summary", "primary/certificates/bounded_relation_n3_all_filtered_summary.json",
        "--root-stream", "primary/certificates/hard_cover_root_cases_n3_schema3_n3_full.jsonl.gz",
        "--output", "primary/certificates/bounded_relation_n3_hard_cover_crosswalk.jsonl.gz",
    )

    run(
        work, PYTHON, "primary/hard_cover_compiler.py", "--sizes", "4",
        "--bit-cache", cache, "--source-core-id", "theta-2",
        "--source-extra-count", "0", "--tag", "schema3_theta2_full",
        "--output", "primary/certificates/hard_cover_schema3_theta2_full_summary.json",
    )

    compact_specs = (
        ("primary/certificates/hard_cover_schema3_n3_full_summary.json",
         "schema3_n3_compact", ((0, 36), (36, 72), (72, 108), (108, 144))),
        ("primary/certificates/hard_cover_schema3_theta2_full_summary.json",
         "theta2_compact_n4", ((0, 33), (33, 66), (66, 99), (99, 132))),
    )
    for base_summary, prefix, shard_ranges in compact_specs:
        for shard, (start, stop) in enumerate(shard_ranges):
            tag = f"{prefix}_s{shard}"
            output = f"primary/certificates/compact_probe_{tag}_summary.json"
            restore_bundled_program(work, "primary/compact_probe_extension_compiler.py")
            run(
                work, PYTHON, "primary/compact_probe_extension_compiler.py",
                "--base-summary", base_summary, "--bit-cache", cache,
                "--path-start", str(start), "--path-stop", str(stop),
                "--tag", tag, "--output", output,
            )

    restore_bundled_program(
        work, "reviews/direct_anchor_probe_closure/compile_direct_anchor_probes.py"
    )
    run(work, PYTHON, "reviews/direct_anchor_probe_closure/compile_direct_anchor_probes.py")


def full_n4_audit(work: Path) -> None:
    summary = work / "primary/certificates/hard_cover_schema3_theta2_full_summary.json"
    for relative in (
        "reviews/final_hard_cover_cleanroom/audit_candidate_stream.py",
        "reviews/final_hard_cover_cleanroom/mutation_schema3_stream.py",
        "reviews/final_hard_cover_cleanroom/verify_schema3_n4_certificates.py",
    ):
        restore_bundled_program(work, relative)
    run(
        work, PYTHON, "reviews/final_hard_cover_cleanroom/audit_candidate_stream.py",
        "--relations", "primary/certificates/hard_cover_n4_schema3_theta2_full.jsonl.gz",
        "--graphs", "primary/certificates/hard_cover_graphs_n4_schema3_theta2_full.jsonl.gz",
        "--roots", "primary/certificates/hard_cover_root_cases_n4_schema3_theta2_full.jsonl.gz",
        "--polynomials", "primary/certificates/hard_cover_polynomials_n4_schema3_theta2_full.jsonl.gz",
        "--summary", "primary/certificates/hard_cover_schema3_theta2_full_summary.json",
        "--expected-summary-sha256", sha256(summary),
        "--invariant-metadata", "primary/certificates/invariant_multihomogeneity.json",
        "--family-tag", "n4_minimum",
        "--output", "reviews/final_hard_cover_cleanroom/certificates/schema3_n4_theta2_full_audit.json",
        "--terminal-records-output", "reviews/final_hard_cover_cleanroom/certificates/schema3_n4_theta2_terminal_records.jsonl.gz",
    )
    run(work, PYTHON, "reviews/final_hard_cover_cleanroom/mutation_schema3_stream.py")


def verify_regeneration(work: Path) -> dict[str, object]:
    commitments: dict[str, object] = {}
    exact = [
        "primary/certificates/core_universe.json",
        "primary/certificates/completion_universe.json",
        "primary/certificates/support_universe.json",
        "primary/certificates/descriptor_bits_cache.json.gz",
        "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_relations.jsonl.gz",
        "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_graphs.jsonl.gz",
        "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_polynomials.jsonl.gz",
        "primary/certificates/bounded_relation_n3_schema3_n3_all_filtered_signs.json",
        "primary/certificates/hard_cover_n3_schema3_n3_full.jsonl.gz",
        "primary/certificates/hard_cover_graphs_n3_schema3_n3_full.jsonl.gz",
        "primary/certificates/hard_cover_polynomials_n3_schema3_n3_full.jsonl.gz",
        "primary/certificates/hard_cover_root_cases_n3_schema3_n3_full.jsonl.gz",
        "primary/certificates/bounded_relation_n3_hard_cover_crosswalk.jsonl.gz",
        "primary/certificates/hard_cover_n4_schema3_theta2_full.jsonl.gz",
        "primary/certificates/hard_cover_graphs_n4_schema3_theta2_full.jsonl.gz",
        "primary/certificates/hard_cover_polynomials_n4_schema3_theta2_full.jsonl.gz",
        "primary/certificates/hard_cover_root_cases_n4_schema3_theta2_full.jsonl.gz",
        "reviews/final_hard_cover_cleanroom/certificates/schema3_n4_theta2_terminal_records.jsonl.gz",
        "reviews/direct_anchor_probe_closure/certificates/anchors.jsonl.gz",
        "reviews/direct_anchor_probe_closure/certificates/graphs.jsonl.gz",
        "reviews/direct_anchor_probe_closure/certificates/p_relations.jsonl.gz",
        "reviews/direct_anchor_probe_closure/certificates/q_relations.jsonl.gz",
        "reviews/direct_anchor_probe_closure/certificates/witnesses.jsonl.gz",
        "reviews/direct_anchor_probe_closure/certificates/summary.json",
    ]
    for prefix in ("schema3_n3_compact", "theta2_compact_n4"):
        for shard in range(4):
            tag = f"{prefix}_s{shard}"
            exact.extend(
                f"primary/certificates/compact_probe_{kind}_{tag}.jsonl.gz"
                for kind in ("paths", "polynomials", "transports", "witnesses")
            )
            exact.append(f"primary/certificates/compact_probe_{tag}_summary.json")
    for relative in exact:
        compare_exact(work, relative, commitments)

    n4_audit = "reviews/final_hard_cover_cleanroom/certificates/schema3_n4_theta2_full_audit.json"
    normalized_audit = compare_n4_audit(work / n4_audit, ROOT / n4_audit)
    commitments[n4_audit] = {
        "substantive_audit_sha256": hashlib.sha256(
            json.dumps(normalized_audit, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
    }

    summaries = (
        "primary/certificates/bounded_relation_n3_all_filtered_summary.json",
        "primary/certificates/hard_cover_schema3_n3_full_summary.json",
        "primary/certificates/bounded_relation_n3_hard_cover_crosswalk.summary.json",
        "primary/certificates/hard_cover_schema3_theta2_full_summary.json",
    )
    for relative in summaries:
        compare_json(work / relative, ROOT / relative)
        commitments[relative] = {"normalized_json_sha256": hashlib.sha256(
            json.dumps(normalize_json(json.loads((work / relative).read_text())),
                       sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()}
    return commitments


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--keep-work",
        type=Path,
        help="diagnostic only: retain the disposable regenerated bundle here",
    )
    args = parser.parse_args()

    def regenerate_at(work: Path) -> dict[str, object]:
        shutil.copytree(
            ROOT, work,
            ignore=shutil.ignore_patterns(".venv", "__pycache__", "*.pyc", "*.pyo"),
        )
        for relative in (
            "primary/atlas_compiler.py",
            "primary/hard_cover_compiler.py",
            "primary/compact_probe_extension_compiler.py",
            "reviews/direct_anchor_probe_closure/compile_direct_anchor_probes.py",
            "reviews/final_hard_cover_cleanroom/audit_candidate_stream.py",
        ):
            if not (work / relative).is_file():
                raise AssertionError(("disposable copy omitted bundled program", relative))
        primary_regeneration(work)
        full_n4_audit(work)
        return verify_regeneration(work)

    if args.keep_work is not None:
        if args.keep_work.exists():
            raise AssertionError(("diagnostic work path already exists", args.keep_work))
        commitments = regenerate_at(args.keep_work)
    else:
        with tempfile.TemporaryDirectory(prefix="stc-jc-primitive-regeneration-") as raw:
            commitments = regenerate_at(Path(raw) / "bundle")
    payload = {
        "schema": "stc-jc-complete-primitive-regeneration-v1",
        "status": "VERIFIED",
        "objects": commitments,
        "object_count": len(commitments),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": "VERIFIED", "objects": len(commitments)}, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build or check byte-stable telemetry for one clean detached full replay.

The long verifier is deliberately not launched here.  This producer consumes
its final JSON report and the stderr captured from macOS ``/usr/bin/time -l``.
It then binds those observations to an exact, clean, detached source checkout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import stat
import subprocess
from pathlib import Path, PurePosixPath
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = (
    PROJECT
    / "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"
)
REPORT_DISPLAY_PATH = (
    "proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json"
)
LOCK_RELATIVE = "work/final_theorem_release/RELEASE_LOCK.json"
SOURCE_FILES = (
    "proof_compression_submission/article/main.tex",
    "proof_compression_submission/article/references.bib",
    "proof_compression_submission/supplement/supplement.tex",
    "proof_compression_submission/supplement/compression_tables.tex",
    "proof_compression_submission/supplement/certificate_appendix.tex",
)
TELEMETRY_SCHEMA = "k2p-final-clean-full-replay-telemetry-v1"
REPORT_SCHEMA = "k2p-principal-d-plus-final-theorem-replay-report-v1"
LOCK_SCHEMA = "k2p-principal-d-plus-final-theorem-release-lock-v1"
EXPECTED_FULL_REPLAY_LAYER_NAMES = (
    "promotion_manuscript_guard",
    "full_map_domain_reseal",
    "corrected_universe_independent_replay",
    "three_port_no_assert",
    "domain_rooting",
    "quartet_sign_logic",
    "quartet_terminal_bindings",
    "raw_displayed_quartet_direction",
    "canonicalizer_completeness_structural",
    "graph_derived_parameter_transports_structural",
    "bridge_marginal_gluing",
    "analytic_adversarial_audit",
    "global_component_scale_audit",
    "raw4_corrected_overlay_independent",
    "theta2_full_map_independent",
    "four_port_raw_structural_provenance",
    "four_port_direct36",
    "theta2_structural_provenance",
    "cycle_three_port_authoritative_promotion",
    "corrected_probe_independent_streaming_replay",
    "corrected_probe_site_transport_partition",
    "weak_sharpness_primary",
    "weak_sharpness_independent",
    "canonicalizer_completeness_full",
    "graph_derived_parameter_transports_full",
    "corrected_restoration_independent_full_replay",
    "corrected_universe_cross_layer_mutations",
    "raw4_full_map_Ti_truth",
    "theta2_full_map_Ti_truth",
    "composite_domain_reseal_diff",
    "four_port_exact_rank_staged_atlas_omission_mutation",
    "four_port_exact_rank_import_preflight",
    "four_port_exact_rank_full",
    "raw4_corrected_overlay_full_regeneration",
    "four_port_raw_full_regeneration_provenance",
    "four_port_direct36_full",
    "theta2_full_regeneration_provenance",
    "corrected_probe_full_primitive_regeneration",
    "corrected_probe_full_independent_replay",
    "corrected_probe_full_site_transport_partition",
    "corrected_probe_independent_primitive_graph_full",
)
EXPECTED_FULL_REPLAY_LAYER_COUNT = len(EXPECTED_FULL_REPLAY_LAYER_NAMES)
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
DECIMAL = r"(?:0|[1-9][0-9]*)(?:\.[0-9]+)?"
ORDINARY_LAYER_FIELDS = frozenset(
    {
        "elapsed_seconds",
        "name",
        "returncode",
        "status",
        "stderr_sha256",
        "stdout_sha256",
    }
)
INTENTIONAL_MUTATION_LAYER_FIELDS = frozenset(
    {
        "elapsed_seconds",
        "name",
        "observed_nonzero_returncode",
        "status",
        "stderr_sha256",
        "stdout_sha256",
    }
)
INTENTIONAL_MUTATION_LAYERS = {
    "four_port_exact_rank_staged_atlas_omission_mutation": 1,
}
RESTORATION_REPLAY_LAYER = "corrected_restoration_independent_full_replay"
RESTORATION_REPLAY_LAYER_FIELDS = ORDINARY_LAYER_FIELDS | frozenset(
    {"command_sha256", "source_sha256"}
)
RESTORATION_REPLAY_SEMANTIC_COMMAND = (
    "<qualified-python>",
    "-B",
    "work/restoration_sign_reclassification/verify_corrected_restoration_forest.py",
    "--certificate",
    "work/restoration_sign_reclassification/corrected_restoration_forest.json",
    "--crosswalk",
    "work/restoration_sign_reclassification/corrected_restoration_historical_crosswalk.json",
    "--report",
    "<external-report-path>",
)
RESTORATION_REPLAY_SOURCE_FILES = (
    "work/restoration_sign_reclassification/verify_corrected_restoration_forest.py",
    "work/restoration_sign_reclassification/corrected_restoration_forest.json",
    "work/restoration_sign_reclassification/corrected_restoration_historical_crosswalk.json",
)


class TelemetryFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise TelemetryFailure(code if detail is None else f"{code}:{detail}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value: object) -> str:
    return sha256_bytes(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    )


def encoded_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def read_json_object(path: Path, label: str) -> tuple[dict[str, Any], bytes]:
    require(path.is_file() and not path.is_symlink(), f"{label}_MISSING_OR_SYMBOLIC", path)
    data = path.read_bytes()
    try:
        value = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise TelemetryFailure(f"{label}_JSON_INVALID:{error}") from error
    require(isinstance(value, dict), f"{label}_NOT_OBJECT")
    return value, data


def run_git(root: Path, *arguments: str, allow_failure: bool = False) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if not allow_failure:
        require(
            result.returncode == 0,
            "GIT_COMMAND_FAIL",
            f"{' '.join(arguments)}:{result.stderr.decode('utf-8', 'replace').strip()}",
        )
    return result


def parse_project_in_repo(value: str) -> PurePosixPath:
    if value == ".":
        return PurePosixPath()
    require(
        bool(value)
        and not value.startswith("/")
        and all(part not in {"", ".", ".."} for part in value.split("/")),
        "UNSAFE_PROJECT_IN_REPO",
        value,
    )
    pure = PurePosixPath(value)
    require(not pure.is_absolute() and bool(pure.parts), "UNSAFE_PROJECT_IN_REPO", value)
    return pure


def current_project_in_repo() -> PurePosixPath:
    result = run_git(PROJECT, "rev-parse", "--show-toplevel")
    repository = Path(result.stdout.decode().strip()).resolve()
    try:
        relative = PROJECT.resolve().relative_to(repository)
    except ValueError as error:
        raise TelemetryFailure("CURRENT_PROJECT_OUTSIDE_GIT_TOPLEVEL") from error
    value = relative.as_posix()
    require(value != ".", "CURRENT_PROJECT_IN_REPO_PREFIX_EMPTY")
    return parse_project_in_repo(value)


def repo_lookup(project_in_repo: PurePosixPath, relative: str) -> PurePosixPath:
    pure = PurePosixPath(relative)
    require(
        not pure.is_absolute()
        and bool(pure.parts)
        and all(part not in {"", ".", ".."} for part in pure.parts),
        "UNSAFE_CHECKOUT_PATH",
        relative,
    )
    return project_in_repo / pure


def safe_checkout_file(
    root: Path, project_in_repo: PurePosixPath, relative: str
) -> Path:
    lookup = repo_lookup(project_in_repo, relative)
    cursor = root
    for part in lookup.parts:
        cursor = cursor / part
        try:
            mode = cursor.lstat().st_mode
        except FileNotFoundError as error:
            raise TelemetryFailure(f"CHECKOUT_FILE_MISSING:{lookup.as_posix()}") from error
        require(not stat.S_ISLNK(mode), "CHECKOUT_PATH_SYMBOLIC", lookup.as_posix())
    require(cursor.is_file(), "CHECKOUT_PATH_NOT_REGULAR", lookup.as_posix())
    return cursor


def validate_checkout(raw_root: Path, source_commit: str) -> Path:
    require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")
    require(HEX40.fullmatch(source_commit) is not None, "SOURCE_COMMIT_MUST_BE_FULL_HEX40")
    require(raw_root.exists() and raw_root.is_dir(), "CHECKOUT_ROOT_MISSING", raw_root)
    require(not raw_root.is_symlink(), "CHECKOUT_ROOT_SYMBOLIC", raw_root)
    root = raw_root.resolve()
    top = run_git(root, "rev-parse", "--show-toplevel").stdout.decode().strip()
    require(Path(top).resolve() == root, "CHECKOUT_ROOT_NOT_GIT_TOPLEVEL", top)
    head = run_git(root, "rev-parse", "--verify", "HEAD^{commit}").stdout.decode().strip()
    require(head == source_commit, "SOURCE_COMMIT_MISMATCH", f"expected={source_commit}:actual={head}")
    symbolic = run_git(root, "symbolic-ref", "-q", "HEAD", allow_failure=True)
    require(symbolic.returncode == 1, "DETACHED_HEAD_REQUIRED")
    status_result = run_git(
        root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
    )
    require(status_result.stdout == b"", "DIRTY_CHECKOUT")
    return root


def tracked_file_row(
    root: Path, project_in_repo: PurePosixPath, relative: str
) -> dict[str, Any]:
    lookup = repo_lookup(project_in_repo, relative).as_posix()
    path = safe_checkout_file(root, project_in_repo, relative)
    tracked = run_git(root, "ls-files", "--error-unmatch", "--", lookup, allow_failure=True)
    require(tracked.returncode == 0, "CHECKOUT_FILE_NOT_TRACKED", lookup)
    committed = run_git(root, "cat-file", "-e", f"HEAD:{lookup}", allow_failure=True)
    require(committed.returncode == 0, "CHECKOUT_FILE_NOT_IN_COMMIT", lookup)
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha256_bytes(data)}


def validate_release_lock(
    root: Path, project_in_repo: PurePosixPath
) -> tuple[dict[str, Any], dict[str, Any]]:
    path = safe_checkout_file(root, project_in_repo, LOCK_RELATIVE)
    lock, data = read_json_object(path, "RELEASE_LOCK")
    require(lock.get("schema") == LOCK_SCHEMA, "RELEASE_LOCK_SCHEMA_MISMATCH")
    claimed = lock.get("payload_sha256")
    unsigned = dict(lock)
    unsigned.pop("payload_sha256", None)
    require(
        isinstance(claimed, str)
        and HEX64.fullmatch(claimed) is not None
        and claimed == canonical_hash(unsigned),
        "RELEASE_LOCK_PAYLOAD_MISMATCH",
    )
    require(lock.get("promotion_ready") is True, "RELEASE_LOCK_NOT_PROMOTION_READY")
    require(lock.get("blockers") == [], "RELEASE_LOCK_HAS_BLOCKERS")
    require(lock.get("missing_required_files") == [], "RELEASE_LOCK_MISSING_FILES")
    tracked_file_row(root, project_in_repo, LOCK_RELATIVE)
    row = {
        "bytes": len(data),
        "path": LOCK_RELATIVE,
        "payload_sha256": claimed,
        "sha256": sha256_bytes(data),
    }
    return lock, row


def positive_finite_number(value: object, code: str) -> float:
    require(
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and float(value) > 0,
        code,
    )
    return float(value)


def validate_report(
    report_path: Path,
    lock_payload_sha256: str,
    root: Path,
    project_in_repo: PurePosixPath,
) -> tuple[dict[str, Any], bytes, dict[str, Any]]:
    report, data = read_json_object(report_path, "FULL_REPLAY_REPORT")
    require(report.get("schema") == REPORT_SCHEMA, "FULL_REPLAY_REPORT_SCHEMA_MISMATCH")
    require(report.get("mode") == "full", "FULL_REPLAY_REPORT_NOT_FULL")
    require(report.get("status") == "PASS", "FULL_REPLAY_REPORT_NOT_PASS")
    require(report.get("promotion_ready") is True, "FULL_REPLAY_REPORT_NOT_PROMOTION_READY")
    require(report.get("blockers") == [], "FULL_REPLAY_REPORT_HAS_BLOCKERS")
    require(report.get("optimized_mode") is False, "FULL_REPLAY_REPORT_OPTIMIZED_MODE")
    require(
        report.get("lock_payload_sha256") == lock_payload_sha256,
        "FULL_REPLAY_REPORT_LOCK_MISMATCH",
    )
    internal_elapsed = positive_finite_number(
        report.get("elapsed_seconds"), "FULL_REPLAY_REPORT_ELAPSED_INVALID"
    )
    layers = report.get("layer_replays")
    require(isinstance(layers, list) and bool(layers), "FULL_REPLAY_REPORT_LAYERS_EMPTY")
    names: set[str] = set()
    for index, row in enumerate(layers):
        require(isinstance(row, dict), "FULL_REPLAY_LAYER_NOT_OBJECT", index)
        name = row.get("name")
        require(isinstance(name, str) and bool(name), "FULL_REPLAY_LAYER_NAME_INVALID", index)
        require(name not in names, "FULL_REPLAY_LAYER_NAME_DUPLICATE", name)
        names.add(name)
        require(row.get("status") == "PASS", "FULL_REPLAY_LAYER_NOT_PASS", name)
        if name in INTENTIONAL_MUTATION_LAYERS:
            require(
                frozenset(row) == INTENTIONAL_MUTATION_LAYER_FIELDS,
                "FULL_REPLAY_INTENTIONAL_MUTATION_SCHEMA_INVALID",
                name,
            )
            require(
                isinstance(row.get("observed_nonzero_returncode"), int)
                and not isinstance(row["observed_nonzero_returncode"], bool)
                and row["observed_nonzero_returncode"]
                == INTENTIONAL_MUTATION_LAYERS[name],
                "FULL_REPLAY_INTENTIONAL_MUTATION_RETURNCODE_INVALID",
                name,
            )
        elif name == RESTORATION_REPLAY_LAYER:
            require(
                frozenset(row) == RESTORATION_REPLAY_LAYER_FIELDS,
                "FULL_REPLAY_RESTORATION_LAYER_SCHEMA_INVALID",
                name,
            )
            require(
                row.get("returncode") == 0,
                "FULL_REPLAY_LAYER_RETURNCODE",
                name,
            )
            require(
                row.get("command_sha256")
                == canonical_hash(RESTORATION_REPLAY_SEMANTIC_COMMAND),
                "FULL_REPLAY_RESTORATION_COMMAND_HASH_INVALID",
            )
            expected_sources = {
                relative: tracked_file_row(root, project_in_repo, relative)["sha256"]
                for relative in RESTORATION_REPLAY_SOURCE_FILES
            }
            require(
                row.get("source_sha256") == expected_sources,
                "FULL_REPLAY_RESTORATION_SOURCE_HASH_INVALID",
            )
        else:
            require(
                frozenset(row) == ORDINARY_LAYER_FIELDS,
                "FULL_REPLAY_ORDINARY_LAYER_SCHEMA_INVALID",
                name,
            )
            require(
                isinstance(row.get("returncode"), int)
                and not isinstance(row["returncode"], bool)
                and row["returncode"] == 0,
                "FULL_REPLAY_LAYER_RETURNCODE",
                name,
            )
        elapsed = row.get("elapsed_seconds")
        require(
            isinstance(elapsed, (int, float))
            and not isinstance(elapsed, bool)
            and math.isfinite(float(elapsed))
            and float(elapsed) >= 0,
            "FULL_REPLAY_LAYER_ELAPSED_INVALID",
            name,
        )
        for field in ("stdout_sha256", "stderr_sha256"):
            require(
                isinstance(row.get(field), str)
                and HEX64.fullmatch(row[field]) is not None,
                "FULL_REPLAY_LAYER_HASH_INVALID",
                f"{name}:{field}",
            )
    require(
        len(layers) == EXPECTED_FULL_REPLAY_LAYER_COUNT,
        "FULL_REPLAY_LAYER_COUNT_INVALID",
        f"expected={EXPECTED_FULL_REPLAY_LAYER_COUNT}:observed={len(layers)}",
    )
    require(
        RESTORATION_REPLAY_LAYER in names,
        "FULL_REPLAY_RESTORATION_LAYER_MISSING",
    )
    require(
        tuple(row["name"] for row in layers) == EXPECTED_FULL_REPLAY_LAYER_NAMES,
        "FULL_REPLAY_LAYER_SEQUENCE_INVALID",
    )
    runtime = report.get("runtime")
    require(isinstance(runtime, dict), "FULL_REPLAY_RUNTIME_INVALID")
    for field in ("python", "networkx", "sympy"):
        require(
            isinstance(runtime.get(field), str) and bool(runtime[field]),
            "FULL_REPLAY_RUNTIME_FIELD_INVALID",
            field,
        )
    summary = {
        "blocker_count": 0,
        "internal_elapsed_seconds": internal_elapsed,
        "layer_count": len(layers),
        "lock_payload_sha256": lock_payload_sha256,
        "path": REPORT_DISPLAY_PATH,
        "promotion_ready": True,
        "sha256": sha256_bytes(data),
    }
    return report, data, summary


def unique_match(text: str, pattern: str, code: str, flags: int = re.MULTILINE) -> re.Match[str]:
    matches = list(re.finditer(pattern, text, flags))
    require(len(matches) == 1, code, f"matches={len(matches)}")
    return matches[0]


def parse_time_l(path: Path, internal_elapsed: float) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "TIME_L_MISSING_OR_SYMBOLIC", path)
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise TelemetryFailure(f"TIME_L_NOT_UTF8:{error}") from error
    timing = unique_match(
        text,
        rf"^\s*({DECIMAL})\s+real\s+({DECIMAL})\s+user\s+({DECIMAL})\s+sys\s*$",
        "TIME_L_TIMING_LINE_INVALID",
    )

    def integer_field(labels: tuple[str, ...], code: str) -> int:
        alternation = "|".join(re.escape(label) for label in labels)
        match = unique_match(
            text,
            rf"^\s*([0-9]+)\s+(?:{alternation})\s*$",
            code,
        )
        return int(match.group(1))

    real_seconds, user_seconds, system_seconds = (
        float(timing.group(index)) for index in (1, 2, 3)
    )
    require(real_seconds > 0, "TIME_L_REAL_SECONDS_NOT_POSITIVE")
    require(user_seconds >= 0 and system_seconds >= 0, "TIME_L_CPU_SECONDS_NEGATIVE")
    require(
        real_seconds >= internal_elapsed,
        "TIME_L_REAL_SHORTER_THAN_INTERNAL",
        f"real={real_seconds}:internal={internal_elapsed}",
    )
    maximum_resident = integer_field(
        ("maximum resident set size",), "TIME_L_MAXIMUM_RESIDENT_INVALID"
    )
    footprint = integer_field(
        ("maximum memory footprint", "peak memory footprint"),
        "TIME_L_MEMORY_FOOTPRINT_INVALID",
    )
    require(maximum_resident > 0, "TIME_L_MAXIMUM_RESIDENT_NOT_POSITIVE")
    require(footprint > 0, "TIME_L_MEMORY_FOOTPRINT_NOT_POSITIVE")
    return {
        "maximum_resident_set_size_bytes": maximum_resident,
        "page_faults": integer_field(("page faults",), "TIME_L_PAGE_FAULTS_INVALID"),
        "page_reclaims": integer_field(
            ("page reclaims",), "TIME_L_PAGE_RECLAIMS_INVALID"
        ),
        "peak_memory_footprint_bytes": footprint,
        "real_seconds": real_seconds,
        "source_sha256": sha256_bytes(data),
        "swaps": integer_field(("swaps",), "TIME_L_SWAPS_INVALID"),
        "system_seconds": system_seconds,
        "user_seconds": user_seconds,
    }


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    root = validate_checkout(args.checkout_root, args.source_commit)
    project_in_repo = parse_project_in_repo(args.project_in_repo)
    sources = {
        relative: tracked_file_row(root, project_in_repo, relative)
        for relative in SOURCE_FILES
    }
    _, lock_row = validate_release_lock(root, project_in_repo)
    report, _, report_row = validate_report(
        args.report,
        lock_row["payload_sha256"],
        root,
        project_in_repo,
    )
    time_l = parse_time_l(args.time_l, report_row["internal_elapsed_seconds"])
    # Close the observation window: a concurrent or accidental edit while the
    # external report was being checked must not leave the source tree dirty.
    validate_checkout(args.checkout_root, args.source_commit)
    command = (
        "/usr/bin/time -l .venv/bin/python -B "
        "work/final_theorem_release/verify_final_theorem_release.py --full "
        f"--timeout-seconds {args.timeout_seconds:g} --output <external-report-path>"
    )
    return {
        "schema": TELEMETRY_SCHEMA,
        "status": "PASS",
        "git_commit": args.source_commit,
        "clean_detached_checkout": True,
        "project_in_repo": args.project_in_repo,
        "command": command,
        "submission_sources": sources,
        "release_lock": lock_row,
        "report": report_row,
        "time_l": time_l,
        "runtime": report["runtime"],
        "notes": [
            "The source checkout was at the exact full commit, detached, and clean when this telemetry was produced.",
            "The maximum-resident-set-size and memory-footprint fields are distinct metrics parsed from macOS /usr/bin/time -l.",
            "The replay report and telemetry output are outside the detached checkout, so observation does not modify the checked source tree or enter the release lock.",
        ],
    }


def path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def write_atomic(path: Path, data: bytes, replace_existing: bool) -> str:
    require(not path.is_symlink(), "OUTPUT_SYMBOLIC", path)
    if path.exists():
        require(path.is_file(), "OUTPUT_NOT_REGULAR", path)
        if path.read_bytes() == data:
            return "ALREADY_CURRENT"
        require(replace_existing, "OUTPUT_EXISTS_DIFFERENT_USE_REPLACE_EXISTING", path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    require(not temporary.exists(), "OUTPUT_TEMPORARY_EXISTS", temporary)
    try:
        with temporary.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    return "WRITTEN"


def main() -> int:
    if not __debug__:
        raise SystemExit("CLEAN_FULL_REPLAY_TELEMETRY_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--checkout-root", type=Path, required=True)
    parser.add_argument("--project-in-repo")
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--time-l", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--timeout-seconds", type=float, default=7200.0)
    parser.add_argument("--replace-existing", action="store_true")
    args = parser.parse_args()
    if args.project_in_repo is None:
        prefix = current_project_in_repo()
        args.project_in_repo = prefix.as_posix()
    else:
        prefix = parse_project_in_repo(args.project_in_repo)
        args.project_in_repo = prefix.as_posix() if prefix.parts else "."
    require(
        math.isfinite(args.timeout_seconds) and args.timeout_seconds > 0,
        "TIMEOUT_SECONDS_INVALID",
    )
    require(
        not args.replace_existing or args.write,
        "REPLACE_EXISTING_REQUIRES_WRITE",
    )
    root = args.checkout_root.resolve()
    output = args.output.resolve()
    require(not path_is_within(output, root), "OUTPUT_MUST_BE_OUTSIDE_CHECKOUT", output)
    require(
        not path_is_within(args.report, root),
        "REPORT_MUST_BE_OUTSIDE_CHECKOUT",
        args.report,
    )
    require(
        not path_is_within(args.time_l, root),
        "TIME_L_MUST_BE_OUTSIDE_CHECKOUT",
        args.time_l,
    )
    require(output not in {args.report.resolve(), args.time_l.resolve()}, "OUTPUT_COLLIDES_WITH_INPUT")
    payload = build_payload(args)
    expected = encoded_json(payload)
    if args.check:
        require(
            output.is_file() and not output.is_symlink(),
            "TELEMETRY_OUTPUT_MISSING_OR_SYMBOLIC",
            output,
        )
        require(output.read_bytes() == expected, "TELEMETRY_OUTPUT_DRIFT")
        action = "CHECKED"
    else:
        action = write_atomic(output, expected, args.replace_existing)
    print(
        json.dumps(
            {
                "action": action,
                "git_commit": args.source_commit,
                "layer_count": payload["report"]["layer_count"],
                "report_sha256": payload["report"]["sha256"],
                "status": "PASS",
                "telemetry_sha256": sha256_bytes(expected),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except TelemetryFailure as error:
        raise SystemExit(f"CLEAN_FULL_REPLAY_TELEMETRY_FAIL:{error}") from error

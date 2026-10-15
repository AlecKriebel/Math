#!/usr/bin/env python3
"""Static administrative PR38 builder. Only root may execute after actual replay.

No mathematical search, module import of research code, verifier execution,
network access, Git mutation, or shared/canonical write is performed. Original
and closed-family inputs are immutable. A new whole-current gate stays pending.
"""
from __future__ import annotations

import argparse
import ctypes
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import traceback

HEAD = "980719c79e13ffbc3f5cfbf149c325ea2fb51df0"
BASE = "c6975ca76f9f667f1250ba403d0e6da2aafe14d0"
SNAPSHOT_SHA = "2c58f3aa5f73920fa62c7103648deee899db3a12f3f48c940576f99eff74dfe2"
SCOPE_SHA = "4e042ef2328c73cf871627ccf15c3ffe98366019c67c34951a7d9a221e1a47fa"
STATEMENT_SHA = "8a46410ba42da5d97fe46476751376072b945b1735639c3512284818a58deac2"
PAIR_SHA = "1c7d4e8927310321916aec789766a236321da4d43da89b426c239eb54cbf9cc0"
PR_URL = "https://github.com/AlecKriebel/Math/pull/38"
GATE = "pending_NEW_whole_current_packet_source_first_adversary"
FAMILIES = {
    "primary_scope_family": ("FAMILY_MANIFEST.json", "56cbbc079ee9f05dd3f43f75b068bfc1ec691a363f44ab94054925a0cedba09c", 52, "ignoredtmp"),
    "current_measure_family": ("artifact_manifest.json", "1e6905dddeb96b57e8d5362724947ab2862791ded39f174b4de4b57c850d0082", 63, "tmp"),
    "trace_geometry_family": ("authored_manifest.json", "82ec472f35d4e4b45dea5128c58e2d0ec61318c285bcf9ca5e88de3bf5d2aeac", 54, "tmp"),
}
HEADER = ["Rank", "ID / code", "Problem", "EV", "Impact (/10)", "Difficulty", "Proposed", "Status", "Turns", "Chat", "Findings", "DOI"]
FORBIDDEN = {".git", "__pycache__"}
HISTORICAL_TOP = ["RESULTS.md", "verify.py", "verification.json", "source_record.json", "source_provenance.json", "prior_report.json", "turns.json", "review/independent_checks.py", "review/independent_results.json"]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def relative(value):
    require(isinstance(value, str) and value and "\\" not in value, "Invalid relative path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and str(path) == value and not {".", ".."}.intersection(path.parts), "Noncanonical/unsafe path: " + value)
    require(not FORBIDDEN.intersection(path.parts) and path.suffix not in {".pdf", ".pyc", ".tmp"}, "Scratch/foreign path prohibited: " + value)
    return value


def entries(manifest):
    rows = manifest.get("files", manifest.get("authored_files"))
    if isinstance(rows, dict):
        rows = [{"path": key, **value} for key, value in rows.items()]
    require(isinstance(rows, list), "Manifest needs explicit files/authored_files")
    return rows


def git(repo, *arguments):
    return subprocess.check_output(["git", *arguments], cwd=repo)


def publish_absent(stage, destination):
    """macOS exclusive atomic rename; never replace a raced-in destination."""
    require(sys.platform == "darwin", "Exclusive atomic rename implementation requires this macOS host")
    libc = ctypes.CDLL(None, use_errno=True)
    rename = libc.renamex_np
    rename.argtypes, rename.restype = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint], ctypes.c_int
    if rename(os.fsencode(stage), os.fsencode(destination), 0x00000004) != 0:  # RENAME_EXCL
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number), str(destination))


def regular_inventory(root, cache_prefix=None):
    """Only the explicitly authorized top-level external cache is excluded."""
    found = set()
    for path in root.rglob("*"):
        name = path.relative_to(root).as_posix()
        if cache_prefix and PurePosixPath(name).parts[0] == cache_prefix:
            continue
        require(not path.is_symlink(), "Symlink in strict inventory: " + name)
        if path.is_file():
            found.add(relative(name))
        else:
            require(path.is_dir(), "Nonregular inventory member: " + name)
    return found


def arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--root-receipt", default="ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json")
    parser.add_argument("--root-receipt-sha256", required=True)
    parser.add_argument("--root-replay-script", required=True)
    parser.add_argument("--root-replay-script-sha256", required=True)
    parser.add_argument("--root-scope-certificate-sha256", required=True)
    parser.add_argument("--root-read-ledger-sha256", required=True)
    parser.add_argument("--root-retention-manifest", required=True)
    parser.add_argument("--root-retention-manifest-sha256", required=True)
    parser.add_argument("--root-support-manifest")
    parser.add_argument("--root-support-manifest-sha256")
    return parser.parse_args()


def main():
    args = arguments()
    require(args.execute, "Static preparation only: root must explicitly provide --execute after actual replay")
    for key, value in vars(args).items():
        if key.endswith("sha256") and value is not None:
            require(re.fullmatch(r"[0-9a-f]{64}", value) is not None, "Explicit SHA256 required: " + key)
    require(bool(args.root_support_manifest) == bool(args.root_support_manifest_sha256), "Optional support path/hash must be paired")
    script = Path(__file__).resolve()
    require(script.parent.name == "current_execution_revision" and script.parent.parent.name == "pr38_2765", "Keep revised builder at its dedicated audit anchor")
    audit, repo = script.parent.parent, script.parent.parent.parents[2]
    preparation_prefix = script.parent.relative_to(audit).as_posix()
    destination = audit / "reviewed_candidate"
    require(git(repo, "branch", "--show-current").strip() == b"main", "Stay on main")
    require(not destination.exists() and not destination.is_symlink(), "Never overwrite an existing candidate")
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    dependencies, retained = {}, {}

    def bind(name, role, expected=None):
        name = relative(name)
        path = audit / name
        require(path.is_file() and not path.is_symlink(), "Missing/nonregular input: " + name)
        require(all(not parent.is_symlink() for parent in path.parents if parent != audit.parent), "Symlink ancestor: " + name)
        data = path.read_bytes()
        record = {"path": name, "bytes": len(data), "sha256": sha(data), "role": role}
        require(expected is None or record["sha256"] == expected, "Explicit input pin changed: " + name)
        require(name not in dependencies or dependencies[name]["sha256"] == record["sha256"], "Input changed during build: " + name)
        dependencies[name] = record
        return data

    root_raw = bind(args.root_receipt, "actual_root_full_reproduction_receipt", args.root_receipt_sha256)
    root = json.loads(root_raw)
    require(root.get("status") == "PASS" and root.get("head") == HEAD and root.get("base") == BASE, "Actual PASS receipt for this exact head/base required")
    require(root.get("exact_original_file_count") == 16 and root.get("changed_diff_path_count") == 17, "Actual original16/17 provenance required")
    require(root.get("closed_family_count") == 3 and root.get("authored_members_verified_before_and_after") == 169, "All169 closed members before AND after actual replay required")
    require(root.get("original_substantive_turns") == 2 and root.get("turn_limit") == 5 and root.get("new_substantive_attempts") == 0 and root.get("audit_turns") == 0, "Preserve original2/5, new0/audit0")
    require(root.get("root_script_path") == relative(args.root_replay_script) and root.get("root_script_sha256") == args.root_replay_script_sha256, "Receipt must bind actual root collector path/hash")
    collector = bind(args.root_replay_script, "actual_root_owned_collector_source", args.root_replay_script_sha256)
    executed_collector = bind(root["executed_collector_path"], "actual_executed_replay_collector_source", root["executed_collector_sha256"])
    scope = bind("ROOT_PARTIAL_SCOPE_CERTIFICATE.md", "root_direct_proof_and_source_scope_certificate", args.root_scope_certificate_sha256)
    require(args.root_scope_certificate_sha256 == SCOPE_SHA, "Original root scope certificate exact pin required")
    ledger_raw = bind("ROOT_PRIMARY_READ_LEDGER.json", "root_current_clock_direct_primary_proof_reading", args.root_read_ledger_sha256)
    ledger = json.loads(ledger_raw)
    require(ledger.get("scope_certificate_sha256") == SCOPE_SHA and ledger.get("reading_completed") and ledger.get("new_substantive_attempts") == 0, "Exact direct root proof-reading ledger required")
    read_pin = root.get("root_primary_read_ledger", {})
    require(read_pin.get("path") == "ROOT_PRIMARY_READ_LEDGER.json" and read_pin.get("sha256") == args.root_read_ledger_sha256 and read_pin.get("size") == len(ledger_raw), "Actual receipt must bind exact root reading input")
    for key in ["actual_outer_program_runs", "actual_nested_program_runs", "full_structured_receipt_comparisons"]:
        require(isinstance(root.get(key), list) and root[key], "Actual complete retained evidence list required: " + key)
    require(all(row.get("exit", row.get("exit_code", row.get("returncode"))) == 0 for row in root["actual_outer_program_runs"]), "Final successful outer actual runs must succeed; retain earlier failures separately")
    require(root.get("strict_root_exact_recursive_closure_verified") is True and root.get("primary_nested_manifest_exploit_rejected_by_strict_root") is True, "Fresh strict root closure and nested-manifest exploit rejection required")
    closure = root["strict_root_closure_before_and_after"]
    require(closure["equal"] is True and closure["before"] == closure["after"], "Actual before/after strict closure must agree")
    guard_findings = root["administrative_guard_findings"]
    require({row["case"] for row in guard_findings} == {"nested_manifest_extra", "nested_ignoredtmp_extra"}, "Both old-helper coverage gaps must be explicitly tested")
    require(all(row["family"] == "primary_scope_family" and row["expected_pass"] is True and row["actual_pass"] is True and row["strict_root_guard_pass"] is False and row["strict_root_guard_failure"] for row in guard_findings), "Keep historical helper acceptance distinct from strict-root rejection")
    for comparison in root["full_structured_receipt_comparisons"]:
        require(comparison["all_remaining_fields_equal"] is True, "Every whole structured comparison must close")
        differences, qualifications = comparison["full_JSON_differences"], comparison["precise_qualifications"]
        require(all(row["path"] in qualifications and row == qualifications[row["path"]]["difference"] for row in differences), "Every residual difference needs an exact retained qualification")
        require(bool(differences) != comparison["equal_after_explicit_clock_and_private_path_exclusions"], "Whole comparison equality/difference flags disagree")
    policy = root["comparison_exclusion_policy"]
    require(set(policy["clock_keys"]) == {"utc", "time_utc", "at", "started_utc", "ended_utc"} and policy["qualified_differences_remain_in_full_JSON"] is True and policy["broad_runtime_or_native_ignoring"] is False, "Only exact clock and single private-prefix normalization may be used")

    snapshot_raw = bind("snapshot_manifest.json", "exact_original16_snapshot_manifest", SNAPSHOT_SHA)
    snapshot = json.loads(snapshot_raw)
    require(snapshot["head"] == HEAD and snapshot["base"] == BASE and snapshot["pr"] == 38 and str(snapshot["problem"]) == "2765", "Wrong original target")
    require(len(snapshot["files"]) == 16 and len(snapshot["changed_paths"]) == 17, "Exact original16/17diff required")
    original = {}
    for member in snapshot["files"]:
        name = relative(member["path"])
        require(name not in original, "Duplicate original member")
        data = bind("source_snapshot/" + name, "original16_immutable_git_input", member["sha256"])
        require(len(data) == member["size"], "Original size differs: " + name)
        path = "unsolved_math_prioritization/attempts/2765/" + name
        require(git(repo, "show", HEAD + ":" + path) == data, "Original Git bytes differ: " + name)
        require(git(repo, "ls-tree", HEAD, "--", path).decode().strip() == member["mode"] + " blob " + member["git_blob"] + "\t" + path, "Original Git mode/blob differs: " + name)
        original[name] = data
    require(regular_inventory(audit / "source_snapshot") == set(original), "Original archive needs exactly16 regular files")
    diff = bind("pr_input/diff.patch", "complete_exact_original17_path_diff", snapshot["diff_sha256"])
    require(len(diff) == snapshot["diff_bytes"] and git(repo, "diff", BASE, HEAD) == diff, "Exact original diff bytes required")
    require(git(repo, "diff", "--name-only", BASE, HEAD).decode().splitlines() == snapshot["changed_paths"], "Exact17 Git diff paths required")
    metadata_raw = bind("pr_input/metadata.json", "frozen_original_draft_metadata")
    metadata = json.loads(metadata_raw)
    require(metadata["number"] == 38 and metadata["headRefOid"] == HEAD and metadata["isDraft"] is True, "Frozen draft metadata differs")
    problem, attempt, turns = [json.loads(original[name]) for name in ["source_record.json", "attempt.json", "turns.json"]]
    require(problem["id"] == 2765 and problem["problem_number"] == "KP-2.17" and "problem" not in problem, "Entire flat original source required")
    require(original["prior_report.json"] == b"null\n", "Original null prior-report bytes must remain exact")
    require(attempt["substantive_attempts_used"] == len(turns) == 2 and attempt["substantive_attempt_limit"] == 5 and [row["turn"] for row in turns] == [1, 2], "Original authored ledger differs")
    require(not attempt["full_closed_surface_resolution_claimed"] and not attempt["novel_result_claimed"], "No full-resolution/novelty promotion")
    require(sha(problem["statement"].encode()) == STATEMENT_SHA and sha(json.dumps([problem, {}], sort_keys=True).encode()) == PAIR_SHA, "Entire native source/fallback semantics differ")

    provenance = root["provenance"]
    require(provenance.get("status") == "PASS_READONLY_PROVENANCE_REPRODUCTION", "Actual source/native provenance required")
    require(provenance["complete_flat_problem"] == problem and provenance["prior_raw_key_present"] is False and provenance["original_prior_literal"] is None and provenance["native_importer_prior_fallback"] == {}, "Full raw source/null/qualified fallback must agree semantically")
    require(provenance["head"] == HEAD and provenance["base"] == BASE and len(provenance["original_git_files"]) == 16 and provenance["changed_diff_paths"] == snapshot["changed_paths"], "Full actual original Git/provenance required")
    expected_git = [{"path": "unsolved_math_prioritization/attempts/2765/" + row["path"], "mode": row["mode"], "git_blob": row["git_blob"], "size": row["size"], "sha256": row["sha256"]} for row in snapshot["files"]]
    require(provenance["original_git_files"] == expected_git, "Actual every original Git blob/mode/size/hash must agree")
    require(provenance["raw_corpus_bytes"] == 149266659 and provenance["problem_count"] == 15458 and provenance["research_report_count"] == 6701 and provenance["full_raw_and_SQL_importer_join_checked"] is True, "Entire raw corpus/SQL object join required")
    require(provenance["SQL_mode"] == "ro, immutable, query_only" and provenance["pure_queue_score"]["review_hash"] == PAIR_SHA, "Read-only native importer semantics required")
    native = provenance["current_native_target"]
    require(native["state"] is None and native["history_events"] == [] and native["catalog"]["local_status"] == "queued" and native["catalog"]["turns_used"] == 0, "Initial native target absence/queued0 must remain visible")
    replay_rows = root.get("original_replays")
    require(isinstance(replay_rows, list) and len(replay_rows) == 2, "Actual author30 and independent72 original replays required")
    for row, program, receipt, count in zip(replay_rows, ["verify.py", "review/independent_checks.py"], ["verification.json", "review/independent_results.json"], [30, 72]):
        require(row["program"] == program and row["program_sha256"] == sha(original[program]) and row["assertions"] == count and row["exit_code"] == 0, "Original actual program/count pin differs")
        require(row["generated_receipt_sha256"] == sha(original[receipt]) and row["generated_complete_receipt_BYTE_equal"] is True and row["generated_complete_receipt_JSON_equal"] is True, "Whole generated original receipt comparison required")
        require("Collector" in row["generated_receipt_behavior"] and "stdout" in row["generated_receipt_behavior"] and "writes no result file" in row["generated_receipt_behavior"], "Materialized stdout must not be mislabelled as original program file output")
        require(row["whole_stdout_BYTE_equal"] is True and row["whole_stdout_JSON_equal"] is True, "PR38 BOTH stdout streams must equal WHOLE JSON receipts; metadata-only convention is inapplicable")
    require(root.get("original_runtime_python") == "/usr/bin/python3" and root.get("original_runtime_python_version", "").startswith("3.9") and root.get("original_runtime_sympy_version") == "1.14.0", "Actual compatible Python3.9/SymPy1.14 runtime required")
    require(root.get("default_python314_missing_sympy_failure_retained") is True, "Default3.14 missing-SymPy failure evidence must remain visible")

    historical_states = {}
    for revision in [BASE, HEAD]:
        data = git(repo, "show", revision + ":unsolved_math_prioritization/state.json")
        require("2765" not in json.loads(data), "Do not manufacture original native target events")
        historical_states[revision] = data
    copied_families = {}
    for family, (manifest_name, digest, count, cache_prefix) in FAMILIES.items():
        manifest_path = family + "/" + manifest_name
        data = bind(manifest_path, "exact_closed_first_party_family_manifest", digest)
        pin = root["family_manifests"][family]
        require(pin["manifest_path"] == manifest_path and pin["manifest_sha256"] == digest and pin["member_count"] == count and pin["strict_recursive_coverage"] is True, "Actual family manifest pin differs: " + family)
        require(closure["before"][family] == pin and pin["exclusions"] == [manifest_name, cache_prefix + "/"], "Exact before/after family self/cache exclusion required")
        rows, names = entries(json.loads(data)), set()
        require(len(rows) == count, "Closed family count differs: " + family)
        copied_families["family_evidence/" + manifest_path] = data
        for member in rows:
            name = relative(member["path"])
            require(name not in names and name != manifest_name, "Duplicate/self-included closed family entry")
            names.add(name)
            raw = bind(family + "/" + name, "closed_authored_member", member["sha256"])
            require(len(raw) == member.get("bytes", member.get("size")), "Closed family size differs")
            copied_families["family_evidence/" + family + "/" + name] = raw
        require(regular_inventory(audit / family, cache_prefix) == names | {manifest_name}, "Strict exact recursive family inventory differs: " + family)
    require(set(root["family_manifests"]) == set(FAMILIES), "Exactly the three closed families required")

    def retention_manifest(name, digest, role):
        raw = bind(name, role, digest)
        manifest, names, retained_rows = json.loads(raw), set(), {}
        require(manifest.get("status") == "PASS" and manifest.get("root_reproduction_receipt_sha256") == args.root_receipt_sha256, "Retention manifest must bind exact actual receipt")
        require(manifest.get("root_reproduction_receipt") == {"path": relative(args.root_receipt), "size": len(root_raw), "sha256": args.root_receipt_sha256}, "Retention manifest must bind actual complete root receipt path/size/hash")
        require(manifest.get("path_base") == "support_directory", "Explicit support-directory member path base required")
        support_directory = relative(manifest["support_directory"])
        require(name == support_directory + "/ROOT_SUPPORT_MANIFEST.json" and manifest.get("self_excluding") is True and manifest.get("excluded") == ["ROOT_SUPPORT_MANIFEST.json"], "Retention self-exclusion must be exact root manifest only")
        require(manifest.get("foreign_corpus_SQL_PDF_OCR_cache_or_private_scratch_retained") is False, "Retention must explicitly exclude foreign/raw/SQL/cache/scratch content")
        for member in entries(manifest):
            path = relative(member["path"])
            require(path not in names and path != "ROOT_SUPPORT_MANIFEST.json", "Duplicate/self-included retention member")
            require(PurePosixPath(path).suffix in {".py", ".json", ".jsonl", ".stdin", ".stdout", ".stderr", ".patch", ".md", ".txt"} or PurePosixPath(path).name == ".gitignore", "Unsupported first-party retention capability: " + path)
            names.add(path)
            data = bind(support_directory + "/" + path, "retained_actual_first_party_code_stream_receipt_failure_revision", member["sha256"])
            require(len(data) == member.get("bytes", member.get("size")), "Retained evidence size differs")
            retained["root_verification/evidence/" + support_directory + "/" + path] = data
            retained_rows[support_directory + "/" + path] = {"bytes": len(data), "sha256": sha(data)}
        require(regular_inventory(audit / support_directory) == names | {"ROOT_SUPPORT_MANIFEST.json"}, "Exact recursive retained first-party coverage required")
        retained["root_verification/evidence/" + name] = raw
        return {"path": name, "sha256": digest, "member_count": len(names), "members": retained_rows}

    retention = retention_manifest(relative(args.root_retention_manifest), args.root_retention_manifest_sha256, "required_actual_root_complete_retention_manifest")
    hashes = {row["sha256"] for row in retention["members"].values()}
    require({sha(collector), sha(executed_collector)} <= hashes, "Both root wrapper and actual collector code must survive in retention")

    def artifact_record(record, must_be_retained=True):
        path = Path(record["path"])
        name = path.relative_to(audit).as_posix() if path.is_absolute() else relative(record["path"])
        require(not must_be_retained or name in retention["members"], "Referenced actual artifact not retained: " + name)
        raw = bind(name, "whole_actual_or_saved_artifact_reference", record["sha256"])
        require(len(raw) == record.get("bytes", record.get("size")), "Referenced artifact size differs: " + name)
        return raw

    for row in root["actual_outer_program_runs"]:
        require(row["script_sha256"] in hashes, "Every actual outer program source must be retained")
        for channel in ["stdout", "stderr"]:
            artifact_record(row[channel])
    original_stdin_names = set()
    for row in root["actual_nested_program_runs"]:
        if row.get("script"):
            require(row["script"]["sha256"] in hashes, "Every actual nested program source must be retained")
        for channel in ["stdout", "stderr"]:
            artifact_record(row[channel])
        if "stdin" in row:
            stdin = artifact_record(row["stdin"])
            require(row["outer_label"] == "current_measure_original_code_and_prose_controls" and row["argv"] == ["git", "hash-object", "--stdin"], "Only exact original-input Git stdin capability is authorized")
            matched = [member for member in snapshot["files"] if stdin == original[member["path"]]]
            require(matched and row["exit_code"] == 0 and artifact_record(row["stdout"]).strip() in {member["git_blob"].encode() for member in matched}, "Whole retained stdin input and returned Git blob must match immutable original source")
            original_stdin_names.update(member["path"] for member in matched)
    require(original_stdin_names == set(original), "Every original16 whole stdin input must be retained and checked")
    for comparison in root["full_structured_receipt_comparisons"]:
        artifact_record(comparison["actual"])
        artifact_record(comparison["saved"], False)
        for qualification in comparison["precise_qualifications"].values():
            for key in ["actual_complete_stream", "saved_complete_stream"]:
                if key in qualification:
                    artifact_record(qualification[key], key == "actual_complete_stream")
    artifact_record(root["source_native_inspection_receipt"])
    for row, receipt in zip(replay_rows, ["verification.json", "review/independent_results.json"]):
        generated = artifact_record(row["generated_receipt"])
        stdout = artifact_record(row["actual_stdout"])
        require(generated == stdout == original[receipt] and json.loads(stdout) == json.loads(original[receipt]), "Actual complete original stdout/materialized artifact bytes and JSON must match")
        require(artifact_record(row["actual_stderr"]) == b"", "Original successful diagnostic stderr must be empty")
    failure = root["default_python314_actual_failure"]
    artifact_record(failure["actual_receipt"])
    failure_path = Path(failure["actual_receipt"]["path"])
    failure_name = failure_path.relative_to(audit).as_posix() if failure_path.is_absolute() else relative(failure["actual_receipt"]["path"])
    failure_case = json.loads((audit / failure_name).read_bytes())[failure["case_index"]]
    require(failure_case["case"] == "default_runtime_initial" and failure_case["exit_code"] != 0 and "3.14" in failure_case["runtime_version"] and "ModuleNotFoundError: No module named 'sympy'" in failure_case["stderr"], "Actual default3.14 missing-SymPy failure body must be retained")
    optional = None
    if args.root_support_manifest:
        optional = retention_manifest(relative(args.root_support_manifest), args.root_support_manifest_sha256, "optional_additional_root_retention_manifest")
    for path in regular_inventory(script.parent):
        bind(preparation_prefix + "/" + path, "static_builder_contract_and_closure_source")

    queue_path = repo / "unsolved_math_prioritization/QUEUE.md"
    queue_raw = queue_path.read_bytes()
    lines = queue_raw.decode().splitlines(keepends=True)
    header = [part.strip() for part in next(line for line in lines if line.startswith("| Rank |")).split("|")[1:-1]]
    require(header == HEADER, "Exact twelve named queue columns required")
    matches = [line for line in lines if len(line.split("|")) == 14 and line.split("|")[2].strip() == "2765 / KP-2.17"]
    require(len(matches) == 1, "Unique numeric/code queue preimage required")
    before, fields = matches[0], matches[0].split("|")
    index = {name: position + 1 for position, name in enumerate(header)}
    require(fields[index["Status"]].strip() == "queued" and fields[index["Turns"]].strip() == "0/5", "Queued0/5 required; otherwise prepare a reviewed fresh named-row rebase")
    findings = "2026-10-02: Closed oriented genus>=2 partial current-fiber reductions; arbitrary self-intersecting reference remains unsolved. Separate complete finite-area cusped Radon S_0,3 example does not settle literal complete-only conventions. Exact original2/5, new0/audit0; three closed families and actual root reproduction bound; NEW whole-current source-first gate pending. " + PR_URL + "."
    changed = list(fields)
    for name, value in {"Status": "unsolved", "Turns": "2/5", "Findings": findings}.items():
        changed[index[name]] = " " + value + " "
    allowed = {index[name] for name in ["Status", "Turns", "Findings"]}
    require(all(fields[i] == changed[i] for i in range(14) if i not in allowed), "Only named Status/Turns/Findings changes permitted")
    after = "|".join(changed)
    prospective = b"".join(after.encode() if line == before.encode() else line for line in queue_raw.splitlines(keepends=True))
    require(queue_raw.count(before.encode()) == 1, "Unique full row byte preimage required")

    outputs = {"original_archive/" + name: data for name, data in original.items()}
    outputs.update({name: original[name] for name in HISTORICAL_TOP})
    outputs.update(copied_families)
    outputs.update(retained)
    outputs.update({"CURRENT_PARTIAL_SCOPE_CERTIFICATE.md": scope, "primary_evidence/ROOT_PRIMARY_READ_LEDGER.json": ledger_raw,
                    "root_verification/ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json": root_raw,
                    "native_importer_prior_fallback.json": encoded({}),
                    "build/prepare_current_packet.py": script.read_bytes(), "original_diff.patch": diff,
                    "original_pr_metadata.json": metadata_raw, "original_snapshot_manifest.json": snapshot_raw,
                    "queue_proposal/QUEUE_PREIMAGE.md": queue_raw, "queue_proposal/QUEUE_PROSPECTIVE.md": prospective})
    for revision, data in historical_states.items():
        outputs["historical_native_state/" + revision + ".json"] = data
    for name, record in dependencies.items():
        if name.startswith(preparation_prefix + "/"):
            outputs["build/" + name.split("/", 1)[1]] = (audit / name).read_bytes()
    summary = """# PR38 / 2765 / KP-2.17: partial reductions; complete target unsolved

The complete flat source asks whether every positive geodesic current with a
closed-geodesic length function on the full permitted metric space is a finite
convex combination of closed curves. The reference may self-intersect.
For closed connected oriented genus>=2, the original results give the exact
all-metric fiber, its nonempty compact convex structure, the necessary measured-
lamination intersection equality (no converse), and simple-reference rigidity.
The arbitrary self-intersecting reference still lacks a finite periodic-orbit
support theorem and a finite convex decomposition. Compactness supplies no
classification of extreme points. Finite support here means finitely many
closed-geodesic lift orbits/periodic components, not finitely many universal-
cover geodesics. Atomicity, conical representation and convex representation
are distinct claims.

The separate S_0,3 example uses complete finite-area cusp metrics and all
invariant positive Radon currents. Its marked metric space is a singleton,
and a scaled nonatomic Liouville current has the chosen closed-curve length.
The general noncompact intersection is extended-valued. The local Crofton
calculation gives i(L,L)=(pi/2)area=pi^2 here; it does not transplant global
closed-surface continuity. Compact-core currents and complete infinite-area
funnels with variable boundary lengths are different settings. K3's chapter
defaults allow finite-type oriented surfaces with boundary/punctures and say
complete metrics without requiring finite area. The scoped example therefore
does not settle the literal unrestricted source or the closed-surface target.

The operative numbered problem and remarks are in the author-hosted K3 book,
printed pp98-99, with defaults p84 and complete metrics p96. The original raw
dated triage's AIM workshop-summary pointer stays untouched as historical data.
The correct pointer is
https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf .
Root directly read the primary proofs/pages recorded in the exact current-clock
read ledger and scope certificate. This was a bounded source audit, not an
exhaustive literature/novelty certificate. No new solution/priority is claimed.

Original16 archive, RESULTS mathematics, author/reviewer code, whole saved
receipts, source/provenance and two authored turns are byte exact. Original2/5;
new substantive attempts0; audit turns0. Actual /usr/bin Python3.9 with SymPy
1.14 reproduced author30 and independent72: BOTH stdout streams and generated
receipts equal the WHOLE saved JSON objects and bytes. The failed default
Python3.14 missing-SymPy attempt remains retained. Finite controls supplement
the written argument; they do not test all metrics or classify current support.

The closed primary family's old helper excludes FAMILY_MANIFEST.json by
basename and ignoredtmp by any path component. Its PASS does not protect all
nested extras. The current builder and actual root closure exclude only the
exact self-manifest path and authorized top-level external cache. Root retains
the actual private nested-manifest exploit and strict-root rejection. All169
members and exact three manifest hashes are checked before and after actual
root reproduction; no closed-family code has been silently repaired.

Historical original/review/family PASS labels are evidence, with no transferred
current verdict. No verified native historical worker transcript exists.
Historical base/head native target absence is preserved. A later acceptance
may record the present acceptance only, without earlier readiness/proof/turn
events. Original dated gpt-6-astra/xhigh/deadline fields are archival only;
current model/reasoning exposure is unavailable and current deadline is null.

A NEW whole-current source-first gate remains PENDING after this administrative
freeze. The outcome remains unsolved/source-scope hold. No paper, new DOI,
tracker row, release, external-person communication or shared write is made.
"""
    context = """
original_archive/ has exactly16 original files, including historical README,
body, status, reviews and log. Top-level historical copies have an explicit
notice and keep RESULTS, code, receipts, source and ledger exact. The original
prior_report.json is literally null, because the raw research_results key is
absent; native {} is only a semantically qualified importer fallback. It is not
a retrieved report. Whole source objects are compared semantically; their
original ASCII/Unicode serializations and original bytes are preserved, without
assuming one serialization reproduces another byte hash.

CURRENT_PROOF_DEPENDENCIES.json uses audit-relative paths resolved against
repository_root/draft_pr_publication_program_20260930/audits/pr38_2765, including
after a canonical copy. Copied helpers retain their original audit dependencies;
no copied script implies that its dependency base moves. Every retained first-
party family/member/root source/program/stream/failure/receipt and the actual
builder source are bound. Foreign PDFs, caches and scratch are excluded.
The recursive current MANIFEST.json excludes only itself. CURRENT_QUEUE_PATCH
is a twelve-column named-only prospective queued0/5 -> unsolved2/5 patch;
every unrelated byte and Chat/DOI is preserved. It performs no live queue write.
"""
    outputs["README.md"] = (summary + context).encode()
    outputs["SOURCE_AUDIT.md"] = (summary + "\nFull first-party source/provenance/read/failure ledgers are in family_evidence and root_verification; foreign primary bytes are not redistributed.\n").encode()
    outputs["pr_body.md"] = (summary + "\nCurrent verification is pending the NEW whole-source-first gate; this body is a local proposed replacement only.\n").encode()
    outputs["CURRENT_CONTEXT.md"] = (summary + context).encode()
    outputs["HISTORICAL_ORIGINAL_NOTICE.md"] = ("# Historical original evidence\n\n" + context + "\nThe original historical review is under original_archive/review; no current review is supplied here.\n").encode()
    common = {"id": "2765", "problem_number": "KP-2.17", "status": "unsolved_source_scope_hold_pending_NEW_whole_gate", "original_head": HEAD, "original_base": BASE,
              "original_substantive_attempts": 2, "substantive_attempt_limit": 5, "new_substantive_attempts": 0, "audit_turns": 0,
              "full_resolution_claimed": False, "novelty_claimed": False, "current_gate": GATE,
              "current_model": None, "current_reasoning_effort": None, "current_deadline_utc": None,
              "original_model_reasoning_deadline_historical_only": True, "historical_worker_transcript": "not_verified",
              "native_historical_events_inferred": False, "later_acceptance_is_present_only": True,
              "closed_family_count": 3, "closed_authored_members": 169, "root_receipt_sha256": args.root_receipt_sha256,
              "closed_scope": "Closed connected oriented genus>=2; necessary ML tests, compact convex fiber, simple-reference rigidity only; arbitrary self-intersecting reference unsolved",
              "separate_cusp_scope": "Complete finite-area cusp metrics and all invariant positive Radon currents on S_0,3 only; scaled nonatomic Liouville example",
              "literal_K3_complete_only_scope": "Complete metrics without finite area; scoped S_0,3 example does not settle full literal convention",
              "finite_support_definition": "Finitely many closed-geodesic lift orbits/periodic components, not finitely many universal-cover geodesics",
              "noncompact_pairing_may_be_infinite": True, "local_liouville_normalization": "i(L,L)=(pi/2)area=pi^2 on the finite-area S_0,3",
              "extreme_point_classification_claimed": False, "exact_remaining_gap": "Finite periodic-orbit support and finite convex decomposition for an arbitrary self-intersecting closed reference",
              "current_workflow_completion_estimate_percent": 75, "full_target_completion_estimate_percent": 15,
              "full_target_estimate_is_heuristic_partial_progress_not_solution_probability": True}
    outputs["attempt.json"] = encoded(common)
    outputs["status.json"] = encoded(common)
    outputs["readiness.json"] = encoded({**common, "success_criterion": "Proof or counterexample for the full literal permitted metric/current conventions; the closed arbitrary-reference finite periodic-orbit and convex-decomposition gap remains",
                                        "original_or_family_verdict_transferred": False, "mathematical_repair_required": False})
    outputs["CURRENT_SOURCE_SERIALIZATION_RECEIPT.json"] = encoded({"entire_flat_source_JSON_equal": provenance["complete_flat_problem"] == problem,
        "original_source_record_sha256": sha(original["source_record.json"]), "original_source_record_bytes": len(original["source_record.json"]),
        "original_source_bytes_preserved": True, "comparison_rule": "Object equality for full content; all stored original/source evidence bytes retained independently. No forced ASCII/Unicode reserialization.",
        "prior_raw_key_present": False, "original_prior_literal": None, "native_importer_prior_fallback": {}, "fallback_is_retrieved_report": False,
        "statement_hash": STATEMENT_SHA, "native_pair_hash": PAIR_SHA})
    outputs["CURRENT_NATIVE_HISTORICAL_STATE.json"] = encoded({"states": {key: {"bytes": len(data), "sha256": sha(data), "target_entry_present": False} for key, data in historical_states.items()},
        "scope": "Original base/head target absent; full bytes preserved. No earlier native worker/turn/readiness/proof events fabricated."})
    outputs["CURRENT_QUEUE_PATCH.json"] = encoded({"phase": "Prospective named-only patch; no shared write", "id": 2765, "header_names": header, "column_count": 12,
        "whole_queue_preimage_sha256": sha(queue_raw), "whole_queue_prospective_sha256": sha(prospective), "row_before": before, "row_prospective": after,
        "allowed_named_changes": ["Status", "Turns", "Findings"], "all_unrelated_bytes_Chat_DOI_preserved": True,
        "integration_guard": "Recheck whole preimage; if unrelated acceptances intervene, receipt a fresh named-row rebase. Never replay the original full PR diff."})
    outputs["CURRENT_AUDIT_SCOPE.md"] = ("# NEW whole-current source-first adversarial gate pending\n\n" + summary + "\nRead the entire flat source and qualified missing-report evidence first. Independently test every scope, hypothesis, proof import, current-source/status/body/context/log field, normalization, positivity/Radon/compact-carrier boundary, metric-space singleton justification, no-converse/extreme-point leap, exact archive, source serialization, whole30/72 outputs, strict169 closure/exploit, all actual streams/failures, audit anchor and named twelve-column queue patch. Hash equality certifies retained bytes, not mathematics. No current verdict is claimed.\n").encode()
    outputs["RESEARCH_LOG.md"] = ("# Current PR38 administrative checkpoint\n\n" + now + " — current audit workflow75%; full-target partial-progress estimate15% (heuristic, not a solution probability). Strongest result and exact gap are as recorded in the root certificate. No mathematical repair or search; original2/5,new0,audit0. Original16/17diff and code/math/whole receipts/source/two-turn ledger exact; all169 closed inputs and actual root replay retained. Full literal and closed arbitrary-reference targets unsolved; finite-area cusp observation separately scoped. NEW whole-current source-first gate pending. Original model/reasoning/deadline archival; current exposures unavailable, deadline null. No shared/remote/canonical write, paper, new DOI, tracker or release.\n").encode()
    outputs["CURRENT_PROOF_DEPENDENCIES.json"] = encoded({"utc": now, "dependency_anchor_repository_relative": audit.relative_to(repo).as_posix(),
        "resolution_rule": "Resolve each files.path against repository_root/dependency_anchor_repository_relative, including canonical copies",
        "closed_family_member_counts": {key: value[2] for key, value in FAMILIES.items()}, "closed_authored_member_count": 169,
        "retention_manifest": {key: value for key, value in retention.items() if key != "members"},
        "optional_support_manifest": {key: value for key, value in optional.items() if key != "members"} if optional else None,
        "files": sorted(dependencies.values(), key=lambda row: row["path"])})
    outputs["CURRENT_BUILD_RECEIPT.json"] = encoded({"utc": now, "kind": "Administrative exact-input freeze; no mathematical or verifier execution",
        "original_archive_count": 16, "original_diff_path_count": 17, "original_modes_blobs_bytes_verified": True,
        "RESULTS_math_and_code_and_whole_receipts_and_source_and_turns_BYTE_exact": True,
        "actual_builder_path": script.relative_to(audit).as_posix(), "actual_builder_sha256": sha(script.read_bytes()),
        "root_receipt_sha256": args.root_receipt_sha256, "root_collector_sha256": sha(collector), "root_scope_sha256": sha(scope), "root_read_ledger_sha256": sha(ledger_raw),
        "actual_outer_program_run_count": len(root["actual_outer_program_runs"]), "actual_nested_program_run_count": len(root["actual_nested_program_runs"]),
        "full_structured_comparison_count": len(root["full_structured_receipt_comparisons"]), "closed_authored_members": 169,
        "current_gate": GATE, "new_substantive_attempts": 0, "audit_turns": 0, "shared_git_remote_inventory_canonical_writes": 0})
    for record in dependencies.values():
        data = (audit / record["path"]).read_bytes()
        require(len(data) == record["bytes"] and sha(data) == record["sha256"], "Input changed before freeze: " + record["path"])
    require(queue_path.read_bytes() == queue_raw, "Live queue changed during preparation; use fresh reviewed named-row preimage")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    stage = audit / ("reviewed_candidate.preparation_" + stamp)
    stage.mkdir(exist_ok=False)
    try:
        for name, data in sorted(outputs.items()):
            path = stage / relative(name)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as handle:
                handle.write(data)
        require(regular_inventory(stage / "original_archive") == set(original), "Exactly16 archived members required")
        for name, data in original.items():
            require((stage / "original_archive" / name).read_bytes() == data, "Original archive byte difference")
        for name in HISTORICAL_TOP:
            require((stage / name).read_bytes() == original[name], "Unchanged mathematical/source/diagnostic copy differs")
        manifest_rows = [{"path": name, "bytes": len((stage / name).read_bytes()), "sha256": sha((stage / name).read_bytes())} for name in sorted(regular_inventory(stage))]
        manifest = {"utc": now, "schema": "strict_self_excluded_recursive_current_packet_v1", "self_excluded": ["MANIFEST.json"], "files_count": len(manifest_rows), "files": manifest_rows, "current_gate": GATE}
        with (stage / "MANIFEST.json").open("xb") as handle:
            handle.write(encoded(manifest))
        require(regular_inventory(stage) == {row["path"] for row in manifest_rows} | {"MANIFEST.json"}, "Strict self-excluded recursive current manifest differs")
        for row in manifest_rows:
            data = (stage / row["path"]).read_bytes()
            require(len(data) == row["bytes"] and sha(data) == row["sha256"], "Staged output hash differs")
        require(not destination.exists() and not destination.is_symlink(), "Destination appeared; preserve stage")
        publish_absent(stage, destination)
    except BaseException:
        with (stage / "BUILD_FAILURE.json").open("xb") as handle:
            handle.write(encoded({"utc": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "FAILED_BUILD_PRESERVED", "traceback": traceback.format_exc(), "new_substantive_attempts": 0}))
        raise
    print(json.dumps({"status": "CURRENT_PACKET_FROZEN_NEW_WHOLE_GATE_PENDING", "destination": str(destination), "members": len(manifest_rows), "manifest_sha256": sha((destination / "MANIFEST.json").read_bytes()), "proposed_status": "unsolved", "attempts": "2/5", "new_substantive_attempts": 0, "audit_turns": 0, "shared_writes": 0}, indent=2))


if __name__ == "__main__":
    main()

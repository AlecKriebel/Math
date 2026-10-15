#!/usr/bin/env python3
"""Prepared administrative PR37 freeze; only root may execute this program.

This program does no mathematical search, import, verifier replay, network access,
queue/state/history/inventory write, Git mutation, or canonical-attempt write.
It requires explicit final root evidence and closed-family pins. Failed stages
are retained. The new whole-current-packet source-first gate remains pending.
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import traceback

HEAD = "84bb43d21b36e4d97229806e2518fbc135bee786"
BASE = "c6975ca76f9f667f1250ba403d0e6da2aafe14d0"
ID = 3009
CODE = "KP-5.2"
PR_URL = "https://github.com/AlecKriebel/Math/pull/37"
PAIR_HASH = "8f3665cacdf68423f3c6475ca476c0ad445db19ca331704971dafc545616cd72"
STATEMENT_HASH = "db58be07fe00108409bf8f492aaf0e5ed3c8915719ceb32c96618e111831ac31"
CLOSED_TWO = {
    "planar_fixed_continuum_family": ("authored_manifest.json", "8165a184bc02e3c6f940c45fbf8aeea4f4a034225c2788a35949849880cf5dd6", 10),
    "primary_scope_family": ("FIRST_PARTY_MANIFEST.json", "d53bc8be2de3767f25c5c1576628027750c787b319ff4935c6d1991164acc590", 17),
}
THIRD = "recurrence_orientation_family"
THIRD_COUNT = 21  # Root declared CLOSED21; the digest is still supplied explicitly.
QUEUE_HEADER = ["Rank", "ID / code", "Problem", "EV", "Impact (/10)", "Difficulty", "Proposed", "Status", "Turns", "Chat", "Findings", "DOI"]
FORBIDDEN_PARTS = {"tmp", "ignoredtmp", "private_tmp", "private_sources", "foreign_downloads", "foreign_sources", "__pycache__"}
GATE = "pending_NEW_whole_current_packet_source_first_adversary"
SOURCE_QUALIFIER = ("The disk corollary was directly read in the accessible arXiv v3, revised 2 March 2009, "
                    "of the paper first published in 1998. The printed 1998 disk passage remains unverified.")
ROOT_SUPPORT = [
    "snapshot_original.py", "reproduce_root_original.py", "retrieve_root_sources.py",
    "snapshot_manifest.json", "pinned_problem.json", "pinned_importer_prior_fallback.json",
    "pr_input/metadata.json", "pr_input/diff.patch", "ROOT_PRIMARY_RETRIEVAL.json",
    "ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json", "ROOT_PARTIAL_SCOPE_CERTIFICATE.md",
    "ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json",
]
EXACT_CURRENT_IMPORTS = {
    "ROOT_PARTIAL_SCOPE_CERTIFICATE.md": "CURRENT_PARTIAL_SCOPE_CERTIFICATE.md",
    "ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json": "root_verification/ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json",
    "ROOT_PRIMARY_RETRIEVAL.json": "primary_evidence/ROOT_PRIMARY_RETRIEVAL.json",
    "ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json": "root_verification/ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json",
}
HISTORICAL_TOP = [
    "source_record.json", "turns.json", "check_controls.py", "check_results.json",
    "independent_review/independent_checks.py", "independent_review/independent_results.json",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def safe_relative(value: str) -> PurePosixPath:
    require(isinstance(value, str) and bool(value) and "\\" not in value, "Invalid member path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts and "." not in path.parts, f"Unsafe path: {value}")
    require(str(path) == value, f"Noncanonical relative path: {value}")
    require(not set(path.parts) & FORBIDDEN_PARTS, f"Excluded scratch/foreign path: {value}")
    require(path.suffix not in {".pyc", ".tmp"}, f"Excluded temporary path: {value}")
    return path


def members(manifest):
    entries = manifest["files"]
    if isinstance(entries, dict):
        return [{"path": name, **entry} for name, entry in entries.items()]
    require(isinstance(entries, list), "Manifest files must be a list or map")
    return entries


def git_bytes(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=repo)


def args_parse():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--third-manifest-path", default="RECURRENCE_FAMILY_ROOT_CLOSURE.json", help="Explicit external audit-relative root closure for all21 recurrence files, including its original allowlist")
    parser.add_argument("--third-manifest-sha256", required=True)
    parser.add_argument("--third-member-count", type=int, required=True)
    parser.add_argument("--root-receipt-sha256", required=True)
    parser.add_argument("--root-replay-script", default="reproduce_root_closed_families.py")
    parser.add_argument("--root-replay-script-sha256", required=True)
    parser.add_argument("--root-scope-certificate-sha256", required=True)
    parser.add_argument("--root-support-manifest", help="Optional explicit audit-relative first-party root failure/revision/stream manifest")
    parser.add_argument("--root-support-manifest-sha256")
    return parser.parse_args()


def patch_current_partial(raw: bytes):
    replacements = [
        (
            "Problem 3009 / KP-5.2. Checked 30 September 2026. Model: gpt-6-astra, xhigh. One substantive response of five allowed.",
            "Problem 3009 / KP-5.2. Original substantive budget: 1/5; new substantive attempts: 0; audit attempts: 0. "
            "The original checked-date/model/reasoning/deadline fields are archival only, retained byte-exact in original_archive/. "
            "Current runtime model and reasoning are not independently exposed; no current deadline is inferred. "
            "A NEW whole-current-packet source-first adversarial gate remains pending.",
        ),
        (
            "The boundary-fixed disk consequence is explicitly stated immediately after its theorem; it is not a new result of this attempt.",
            "The boundary-fixed disk consequence is explicitly stated immediately after its theorem in the directly read accessible arXiv v3 (2 March 2009) of the 1998-published paper. "
            "The printed 1998 disk passage has not been directly verified. It is not a new result of this attempt.",
        ),
        (
            "Equivalently, this is the disk corollary already stated in Kolev–Pérouème.",
            "Equivalently, this is the disk corollary directly read in Kolev–Pérouème's accessible arXiv v3 (2009) of the 1998-published paper; the printed 1998 disk passage remains unverified.",
        ),
    ]
    current = raw
    changes = []
    for old, new in replacements:
        before, after = old.encode(), new.encode()
        require(raw.count(before) == 1 and current.count(before) == 1, "Source-only patch preimage must occur exactly once")
        changes.append({"original_byte_offset": raw.index(before), "before": old, "after": new,
                        "before_bytes": len(before), "after_bytes": len(after),
                        "before_sha256": sha(before), "after_sha256": sha(after)})
        current = current.replace(before, after, 1)
    patch = "".join(difflib.unified_diff(raw.decode().splitlines(keepends=True), current.decode().splitlines(keepends=True),
                                       fromfile="original_archive/PARTIAL.md", tofile="PARTIAL.md"))
    receipt = {"kind": "Current source/date/runtime administration only; no mathematical proof search or repair",
               "original_sha256": sha(raw), "current_sha256": sha(current), "original_bytes": len(raw),
               "current_bytes": len(current), "replacements": changes, "replacement_count": 3,
               "deductions_equations_hypotheses_unchanged": True,
               "new_substantive_attempts": 0, "verification_attempts": 0}
    return current, patch.encode(), receipt


def main() -> None:
    args = args_parse()
    require(args.execute, "Prepared source only; root must explicitly supply --execute and final pins")
    for name in ["third_manifest_sha256", "root_receipt_sha256", "root_replay_script_sha256", "root_scope_certificate_sha256"]:
        require(re.fullmatch(r"[0-9a-f]{64}", getattr(args, name)) is not None, f"Explicit SHA256 required: {name}")
    require(args.third_member_count == THIRD_COUNT, "Root-declared CLOSED21 third family is required; final digest remains explicit")
    require(bool(args.root_support_manifest) == bool(args.root_support_manifest_sha256), "Optional root support manifest needs both path and SHA")
    script = Path(__file__).resolve()
    matches = [p for p in script.parents if p.name == "pr37_3009"]
    require(len(matches) == 2 and matches[0] == Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr37_3009/root_source_first_private_reexecution/tmp/private_repository/draft_pr_publication_program_20260930/audits/pr37_3009') and matches[1] == Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr37_3009'), "Exact nested private audit anchors required")
    audit = matches[0]
    repo = audit.parents[2]
    source = audit / "source_snapshot"
    destination = audit / "reviewed_candidate"
    require(git_bytes(repo, "branch", "--show-current").strip() == b"main", "Stay on main")
    require(not destination.exists(), "Never overwrite an existing current packet")
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    dependencies = {}

    def bind(path: Path, role: str) -> bytes:
        require(path.is_file() and not path.is_symlink(), f"Missing/nonregular/symlink input: {path}")
        rel = str(path.relative_to(audit))
        safe_relative(rel)
        require(all(not parent.is_symlink() for parent in path.parents if parent != audit.parent), f"Symlink ancestor: {path}")
        raw = path.read_bytes()
        entry = {"path": rel, "bytes": len(raw), "sha256": sha(raw), "role": role}
        if rel in dependencies:
            require(dependencies[rel]["sha256"] == entry["sha256"] and dependencies[rel]["bytes"] == len(raw), f"Input changed: {rel}")
        else:
            dependencies[rel] = entry
        return raw

    root_receipt_raw = bind(audit / "ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json", "final_root_actual_three_family_reproduction")
    require(sha(root_receipt_raw) == args.root_receipt_sha256, "Final root actual receipt changed after explicit review")
    root_receipt = json.loads(root_receipt_raw)
    require(root_receipt.get("status") == "PASS" and root_receipt.get("closed_family_count") == 3, "Root must actually close and reproduce all three families")
    require(root_receipt.get("authored_members_verified_before_and_after") == 27 + args.third_member_count, "Final root must verify every closed authored member before and after actual execution")
    require(root_receipt.get("original_substantive_turns") == 1 and root_receipt.get("turn_limit") == 5 and root_receipt.get("new_substantive_attempts") == 0, "Root must preserve original1/5 and new0")
    require(isinstance(root_receipt.get("actual_outer_program_runs"), list) and root_receipt["actual_outer_program_runs"], "Actual root program runs required")
    require(all(run.get("exit", run.get("returncode")) == 0 for run in root_receipt["actual_outer_program_runs"]), "Final successful runs must actually succeed; failures belong in preserved supporting evidence")
    require(isinstance(root_receipt.get("full_structured_receipt_comparisons"), list) and root_receipt["full_structured_receipt_comparisons"], "Actual full structured comparisons required")
    require(root_receipt.get("hamilton1954_complete_three_page_proof_read_by_root") is True, "Root must directly read Hamilton1954 all three proof pages before current primary wording")
    root_script_rel = str(safe_relative(args.root_replay_script))
    require(root_script_rel == "reproduce_root_closed_families.py", "Require the actual root three-family collector")
    root_script_raw = bind(audit / root_script_rel, "actual_root_family_replay_collector")
    require(sha(root_script_raw) == args.root_replay_script_sha256 == root_receipt.get("root_script_sha256"), "Root actual receipt must bind the exact actual collector")
    scope_raw = bind(audit / "ROOT_PARTIAL_SCOPE_CERTIFICATE.md", "final_root_scientific_source_scope_certificate")
    require(sha(scope_raw) == args.root_scope_certificate_sha256, "Root final scope certificate changed after review")
    require(b"ROOT_FINAL_CURRENT_ADDENDUM" in scope_raw and b"Hamilton" in scope_raw, "Final certificate must preserve dated prior evidence and a completed current root-reading addendum")

    sm = json.loads(bind(audit / "snapshot_manifest.json", "exact_original_snapshot_manifest"))
    require(sm["head"] == HEAD and sm["base"] == BASE and sm["pr"] == 37 and str(sm["problem"]) == str(ID), "Wrong original target/head/base")
    require(len(sm["files"]) == 13 and len(sm["changed_paths"]) == 14, "Exactly original13/14diff required")
    original = {}
    for member in sm["files"]:
        rel = str(safe_relative(member["path"]))
        require(rel not in original, "Duplicate original member")
        raw = bind(source / rel, "original13_exact_git_input")
        require(len(raw) == member["size"] and sha(raw) == member["sha256"], f"Original snapshot changed: {rel}")
        git_path = f"unsolved_math_prioritization/attempts/{ID}/{rel}"
        require(raw == git_bytes(repo, "show", f"{HEAD}:{git_path}"), f"Original Git bytes changed: {rel}")
        require(git_bytes(repo, "ls-tree", HEAD, "--", git_path).decode().strip() == f"{member['mode']} blob {member['git_blob']}\t{git_path}", f"Original Git mode/blob/path differs: {rel}")
        original[rel] = raw
    diff_raw = bind(audit / "pr_input/diff.patch", "complete_original14_path_diff")
    require(diff_raw == git_bytes(repo, "diff", BASE, HEAD), "Full original diff bytes differ")
    require(len(diff_raw) == sm["diff_bytes"] and sha(diff_raw) == sm["diff_sha256"], "Original full diff hash differs")
    require(git_bytes(repo, "diff", "--name-only", BASE, HEAD).decode().splitlines() == sm["changed_paths"], "Original changed paths differ")
    metadata = json.loads(bind(audit / "pr_input/metadata.json", "frozen_original_pr_metadata"))
    require(metadata["number"] == 37 and metadata["headRefOid"] == HEAD and metadata["isDraft"] is True and metadata["state"] == "OPEN", "Wrong frozen original PR metadata")
    problem_raw = bind(audit / "pinned_problem.json", "entire_flat_raw_problem_with_complete_dated_triage")
    fallback_raw = bind(audit / "pinned_importer_prior_fallback.json", "native_importer_fallback_not_a_retrieved_report")
    problem, fallback = json.loads(problem_raw), json.loads(fallback_raw)
    require(problem == json.loads(original["source_record.json"]), "Entire flat source content must match the complete pinned problem")
    require((json.dumps(problem, indent=2) + "\n").encode() == original["source_record.json"], "Original full raw-problem default ASCII serialization must remain byte-exact")
    require(problem["id"] == ID and problem["problem_number"] == CODE and "problem" not in problem and fallback == {}, "Do not fabricate a nested source or separate report")
    require(sha(json.dumps([problem, fallback], sort_keys=True).encode()) == PAIR_HASH and sha(problem["statement"].encode()) == STATEMENT_HASH, "Native source pair/statement hashes differ")
    turns = json.loads(original["turns.json"])
    require(turns["substantive_turns_used"] == 1 and turns["turn_limit"] == 5 and turns["outcome"] == "unsolved" and [r["turn"] for r in turns["responses"]] == [1], "Preserve exact original1/5 unsolved ledger")
    historical_state = {}
    for revision in [BASE, HEAD]:
        state_raw = git_bytes(repo, "show", f"{revision}:unsolved_math_prioritization/state.json")
        require(json.loads(state_raw) == {}, "Original native state must remain empty; do not invent readiness/proof events")
        historical_state[revision] = {"sha256": sha(state_raw), "bytes": len(state_raw), "entire_object": {}, "target_entry_present": False}
    require(historical_state[BASE] == historical_state[HEAD], "Original native state bytes must be identical empty objects")
    original_receipt = json.loads(bind(audit / "ROOT_ORIGINAL_INTEGRITY_AND_REPLAY.json", "actual_original_root_replay_and_corpus_receipt"))
    require(original_receipt["status"] == "PASS" and original_receipt["separate_prior_report_present"] is False and original_receipt["SQL_readonly"] is True, "Root original/source provenance required")
    require(original_receipt["head"] == HEAD and original_receipt["base"] == BASE and original_receipt["original_git_files"] == 13 and original_receipt["changed_diff_paths"] == 14, "Root original receipt must bind this exact13/14 input")
    require(original_receipt["source_pair_review_hash"] == PAIR_HASH and original_receipt["statement_hash"] == STATEMENT_HASH and original_receipt["original_ledger_sha256"] == sha(original["turns.json"]), "Root original receipt source/ledger pins differ")
    require(original_receipt["full_raw_corpus_bytes"] == 149266659 and original_receipt["SQL_count"] == 15458 and original_receipt["original_budget"] == "1/5", "Exact corpus/budget evidence required")
    original_runs = original_receipt["actual_original_replays"]
    require(len(original_runs) == 2 and [r["checks"] for r in original_runs] == [31, 8462], "Require actual original31/8462 replay")
    require(all(r["exit"] == 0 and r["generated_complete_receipt_BYTE_equal"] is True and r["generated_complete_receipt_JSON_equal"] is True for r in original_runs), "Full generated receipt byte/JSON equality required")
    for run, program, receipt in zip(original_runs, ["check_controls.py", "independent_review/independent_checks.py"], ["check_results.json", "independent_review/independent_results.json"]):
        require(run["program"] == program and run["program_sha256"] == sha(original[program]) and run["generated_receipt_sha256"] == sha(original[receipt]), "Actual original program/generated receipt must bind exact archived bytes")
    require("metadata" in original_runs[1]["stdout_comparison"], "Independent stdout is metadata-only, not full8462 receipt")

    families = dict(CLOSED_TWO)
    third_manifest_rel = str(safe_relative(args.third_manifest_path))
    require(PurePosixPath(third_manifest_rel).parts[0] != THIRD, "The third hashed closure must be external to the closed recurrence family")
    families[THIRD] = (third_manifest_rel, args.third_manifest_sha256, args.third_member_count)
    family_counts = {}
    copied_families = {}
    receipt_family_pins = root_receipt.get("family_manifests")
    require(isinstance(receipt_family_pins, dict) and set(receipt_family_pins) == set(families), "Actual final receipt must explicitly bind all three closed manifests")
    for family, (manifest_name, expected_sha, count) in families.items():
        manifest_rel = manifest_name if family == THIRD else f"{family}/{manifest_name}"
        manifest_role = "external_root_hashed_closure_of_all21_original_recurrence_files" if family == THIRD else "closed_first_party_self_excluding_family_manifest"
        manifest_raw = bind(audit / manifest_rel, manifest_role)
        require(sha(manifest_raw) == expected_sha, f"Closed manifest changed: {family}")
        pin = receipt_family_pins[family]
        require(pin["manifest_path"] == manifest_rel and pin["sha256"] == expected_sha and pin["member_count"] == count, f"Actual root family pin differs: {family}")
        entries = members(json.loads(manifest_raw))
        require(len(entries) == count, f"Closed member count differs: {family}")
        seen = set()
        copied_families[f"family_evidence/{manifest_rel}"] = manifest_raw
        for member in entries:
            rel = str(safe_relative(member["path"]))
            require(rel not in seen, f"Duplicate family member: {family}/{rel}")
            if family != THIRD:
                require(rel != manifest_name, f"Self-included hashed family manifest: {family}/{rel}")
            seen.add(rel)
            raw = bind(audit / family / rel, "closed_first_party_authored_family_member")
            require(len(raw) == member.get("bytes", member.get("size")) and sha(raw) == member["sha256"], f"Closed family member changed: {family}/{rel}")
            if PurePosixPath(rel).suffix == ".json":
                json.loads(raw)
            copied_families[f"family_evidence/{family}/{rel}"] = raw
        if family == THIRD:
            require({"authored_manifest.json", "manifest_verification.json"} <= seen, "External closure must bind original recurrence allowlist and its verifier receipt")
            actual_third = set()
            for path in (audit / THIRD).rglob("*"):
                if not path.is_file():
                    continue
                rel = str(path.relative_to(audit / THIRD))
                relative = PurePosixPath(rel)
                if set(relative.parts) & FORBIDDEN_PARTS or relative.suffix in {".pyc", ".tmp"}:
                    continue
                safe_relative(rel)
                actual_third.add(rel)
            require(actual_third == seen and len(seen) == THIRD_COUNT, "Require exact21 non-scratch recurrence-family inventory, including original allowlist; do not relabel it a self-excluding hashed manifest")
        family_counts[family] = count
    for rel in ROOT_SUPPORT:
        bind(audit / rel, "explicit_root_source_git_metadata_or_actual_receipt")
    optional_support = {}
    if args.root_support_manifest:
        support_rel = str(safe_relative(args.root_support_manifest))
        support_raw = bind(audit / support_rel, "explicit_root_safe_first_party_retention_failure_revision_manifest")
        require(sha(support_raw) == args.root_support_manifest_sha256, "Explicit root support manifest changed")
        support = json.loads(support_raw)
        require(support.get("status") == "PASS" and support.get("root_reproduction_receipt_sha256") == args.root_receipt_sha256, "Safe retained outputs must bind exact final root receipt")
        support_entries = members(support)
        seen = set()
        for member in support_entries:
            rel = str(safe_relative(member["path"]))
            require(rel not in seen and rel != support_rel, "Duplicate/self root-support member")
            require(PurePosixPath(rel).suffix in {".py", ".json", ".jsonl", ".stdout", ".stderr", ".patch", ".md"}, "Only explicit first-party streams/receipts/code/revisions allowed")
            seen.add(rel)
            raw = bind(audit / rel, "exact_root_retained_first_party_actual_stream_receipt_failure_or_source_revision")
            require(len(raw) == member.get("bytes", member.get("size")) and sha(raw) == member["sha256"], f"Root support member changed: {rel}")
        optional_support = {"manifest_path": support_rel, "manifest_sha256": sha(support_raw), "member_count": len(support_entries)}
    bind(script, "actual_executed_administrative_builder")

    queue_path = repo / "unsolved_math_prioritization/QUEUE.md"
    queue_raw = queue_path.read_bytes()
    queue_lines = queue_raw.decode().splitlines(keepends=True)
    headers = [x.strip() for x in next(line for line in queue_lines if line.startswith("| Rank |")).split("|")[1:-1]]
    require(headers == QUEUE_HEADER, "Exact twelve-column queue schema required")
    rows = [line for line in queue_lines if len(line.split("|")) == 14 and line.split("|")[2].strip() == f"{ID} / {CODE}"]
    require(len(rows) == 1, "One exact numeric/code queue row required")
    before = rows[0]
    fields = before.split("|")
    require(fields[8].strip() == "queued" and fields[9].strip() == "0/5", "Require unchanged queued0/5 preimage; otherwise preserve and review a fresh named-row rebase")
    findings = ("2026-10-02: Credited known dimension1/2 and boundary-fixed interval/disk consequence; complete KP-5.2 remains unsolved, including n>=3/local/manifold/stronger smooth variants. "
                "Disk corollary directly read in 2009 arXiv v3 of 1998-published paper; printed1998 disk passage unverified. "
                "Three closed families and actual root reproduction bound; NEW whole current source-first gate pending. Original1/5, new0/audit0; no paper/newDOI/tracker. " + PR_URL + ".")
    after_fields = list(fields)
    after_fields[8], after_fields[9], after_fields[11] = " unsolved ", " 1/5 ", f" {findings} "
    after = "|".join(after_fields)
    require(all(fields[i] == after_fields[i] for i in range(14) if i not in {8, 9, 11}), "Only Status/Turns/Findings may change; preserve Chat/DOI and every other field")
    require(queue_raw.count(before.encode()) == 1, "Unique queue preimage required")
    prospective_queue = queue_raw.replace(before.encode(), after.encode(), 1)
    require(prospective_queue.splitlines(keepends=True) == [after.encode() if line == before.encode() else line for line in queue_raw.splitlines(keepends=True)], "Every unrelated queue byte must remain exact")

    outputs = {f"original_archive/{rel}": raw for rel, raw in original.items()}
    outputs.update({rel: original[rel] for rel in HISTORICAL_TOP})
    outputs.update(copied_families)
    for origin, target in EXACT_CURRENT_IMPORTS.items():
        outputs[target] = bind(audit / origin, "exact_imported_final_root_certificate_or_receipt")
    outputs["pinned_problem.json"] = problem_raw
    outputs["pinned_importer_prior_fallback.json"] = fallback_raw
    outputs["CURRENT_SOURCE_SERIALIZATION_RECEIPT.json"] = json_bytes({
        "scope": "Same entire flat raw problem, two exactly preserved historical/root JSON serializations; no content replacement",
        "source_record": {"path": "source_record.json", "bytes": len(original["source_record.json"]), "sha256": sha(original["source_record.json"]), "serialization": "Original default indent-two ASCII-escaped JSON plus newline; BYTE exact original Git input"},
        "root_pinned_problem": {"path": "pinned_problem.json", "bytes": len(problem_raw), "sha256": sha(problem_raw), "serialization": "Exact root-pinned full-object bytes; reproduce_root_original.py used ensure_ascii=False"},
        "full_JSON_content_equal": True, "BYTE_equal": problem_raw == original["source_record.json"],
        "native_source_pair_hash_uses_semantic_sort_keys_serialization": PAIR_HASH,
        "separate_retrieved_report_present": False, "importer_fallback_path": "pinned_importer_prior_fallback.json",
        "new_substantive_attempts": 0, "verification_attempts": 0,
    })
    outputs["build/prepare_current_packet.py"] = script.read_bytes()
    current_partial, partial_patch, patch_receipt = patch_current_partial(original["PARTIAL.md"])
    outputs["PARTIAL.md"] = current_partial
    outputs["CURRENT_PARTIAL_SOURCE_ONLY.patch"] = partial_patch
    outputs["CURRENT_PARTIAL_SOURCE_PATCH_RECEIPT.json"] = json_bytes(patch_receipt)
    outputs["HISTORICAL_ORIGINAL_NOTICE.md"] = (f"""# Original13 archive and historical diagnostic copies

original_archive/ contains exactly all thirteen Git artifacts from PR37 head
{HEAD}, base {BASE}, byte for byte.
The complete original fourteen-path diff and metadata are bound at the audit
anchor. Its original PARTIAL and old printed1998 source wording remain exact
as historical evidence. CURRENT_PARTIAL_SOURCE_ONLY.patch and its precise
receipt enumerate the three current-only source/runtime wording replacements;
every mathematical deduction and equation is unchanged.

Top-level source_record.json, turns.json, checking programs and saved receipts
are unchanged historical inputs. The independent_review directory here holds
only original diagnostic code/data, not a new current review. Historical
original reviews, provenance, README, PR draft and log remain in the archive.
Original model/reasoning/date/deadline/branch/verdict fields describe that dated
packet only. Neither original empty native state supplies a readiness/proof
event; the original manual QUEUE change is not reconstructed as native history.
The new current source-first whole-packet gate is pending.
""").encode()
    summary = f"""# PR37: credited low-dimensional consequence; complete KP-5.2 unsolved

The complete flat source asks about one common full-orbit diameter bound and
compact-open recurrence on R^n, plus the boundary-fixed closed-ball question.
It also discusses informal local/manifold variants and stronger smooth
recurrence. The original proof verifies the line and plane homeomorphism
cases and boundary-fixed interval/disk cases. Diffeomorphisms in dimensions
one and two follow after forgetting smoothness. Dimensions at least three,
general local/manifold claims and stronger smooth recurrence there remain
unresolved. No full resolution, counterexample or novelty is claimed.

{SOURCE_QUALIFIER} Brown1977 remains inaccessible and is not claimed as read.
Hamilton1954's complete proof, printed pp522–524, was directly read by root;
the closed planar family preserves its primary proof ledger. Cartwright–
Littlewood and Kolev–Pérouème are established theorem imports. Finite controls
do not certify their global topological content or the cited proof texts.

Original substantive budget1/5; new substantive attempts0; audit attempts0.
Three closed first-party families and finalized actual root reproduction are
bound. Original complete31/8462 generated receipts were BYTE/fullJSON equal;
the independent program's stdout is metadata only and was checked against its
specified metadata serialization. Current model/reasoning are not independently
exposed; no current deadline is inferred. Original dated metadata is archival.
A NEW whole-current-packet source-first adversarial gate is PENDING; no old
verdict transfers. No paper, new DOI, tracker, release, or external human review
is claimed. No outside individual was contacted.
"""
    outputs["README.md"] = (summary + """
PARTIAL.md preserves the original mathematics with three enumerated current
source/runtime wording replacements. original_archive/ is exact original13.
pinned_problem.json and source_record.json preserve the same entire flat source,
including its dated literature triage, in their two exact stored serializations.
The original ASCII-escaped source_record bytes and root's Unicode-preserving
pinned_problem bytes have fullJSON equality; their distinct byte hashes/sizes
and actual byte-equality result are explicitly receipted in
CURRENT_SOURCE_SERIALIZATION_RECEIPT.json. pinned_importer_prior_fallback.json is
the native {} fallback for an absent separate research_results entry; it is
not a retrieved report. The full149,266,659-byte corpus and read-only15,458-row
join are bound by actual root and primary-family provenance.

CURRENT_PROOF_DEPENDENCIES.json resolves every dependency against the explicit
repository audit anchor draft_pr_publication_program_20260930/audits/pr37_3009,
including after canonical copies. First-party family manifests and all members
are copied exactly under family_evidence/; source PDFs, tmp, ignoredtmp, foreign
downloads and scratch replicas are excluded. Scripts whose original dependencies
use audit/repository context run at that anchor. No copied script implies a
relocated dependency base. No replay is performed by this builder.

The first two family manifests are their original self-excluding hashed
inventories. The recurrence family's authored_manifest.json is an original
21-file allowlist that includes itself, and manifest_verification.json pins
the other20 files except its own hash. These exact files are preserved.
The external audit-root RECURRENCE_FAMILY_ROOT_CLOSURE.json (or explicitly
selected closure path) supplies all21 exact byte hashes, including both
original inventory files. The external closure is bound and copied exactly;
no internal recurrence manifest is falsely called self-excluding.

CURRENT_PARTIAL_SCOPE_CERTIFICATE.md is copied exactly from root's final scope
certificate. Its earlier dated await note is preserved history; the dated
ROOT_FINAL_CURRENT_ADDENDUM records the actual later completed Hamilton reading
and closure. The actual root receipt independently binds the completion flag.

CURRENT_QUEUE_PATCH.json is a prospective exact twelve-column named-row patch,
limited to Status, Turns and Findings. It requires queued0/5 and preserves Chat,
DOI, all other selected fields and every unrelated byte. Integration must guard
the live preimage anew and separately receipt any rebase for intervening work.
""").encode()
    outputs["PR_DRAFT.md"] = summary.encode()
    outputs["pr_body.md"] = (summary + f"\nOriginal PR: {PR_URL}. Research/evidence anchor: draft_pr_publication_program_20260930/audits/pr37_3009.\n").encode()
    source_scope = f"""# Current source, import and priority qualification

{SOURCE_QUALIFIER} The directly read v3 PDF SHA256 is
da60bbeee27d9d5a19fe8c7f2efb08c1c4e430a419fd7c351cdd8b7661683be7.
Its recurrence definition, Theorem1.1, prime-end recurrence mechanism and
operative sphere proof are imported as established mathematics. Root's failed
versioned endpoint returned406; the unversioned endpoint supplied exact v3 bytes
and version header. That failed retrieval remains failed evidence.

Cartwright–Littlewood's orientation-preserving invariant nonseparating-continuum
theorem is directly supported by Boroński v1 TheoremA and Section3, SHA256
722b2fd6934a1f790a69064e5e36b972448ab9e4b492d4d3775998d9f681dcb6,
and the full Hamilton1954 proof, pp522–524, SHA256
d5078dc430f11464abea5bee8e3b72a1b50958b9fd1aee185dbabc7c461a2fbd,
read by the planar family and root. Brown1977 direct access failed; it is not
represented as having been read. The continuum constructed in the original
proof contains a positive-radius ball and satisfies nondegeneracy. No finite
computed certificate replaces either imported topological theorem.

K3 printed pp302–303, SHA256
ae56518166fe38aaaf555c58614329228afe734e743b111badec4060877fa12f,
is the complete target and remarks. The full flat raw record and complete dated
literature triage remain exact. There is no separate KP-5.2 research report;
native importer{{}} is an explicitly labelled default for an absent key, not
a retrieved report. The conventional recurrence interpretation uses distinct
return powers tending to infinity; constant zeroth powers cannot supply it.
General-manifold informal diameter wording is not silently replaced by a new
metric target. Pardon requires a locally compact acting group and supplies no
cyclic-closure compactness. Euclidean-uniform plane recurrence is not substituted
for compact-open recurrence. Periodicity does not follow from recurrence here.

The line/plane and boundary-fixed interval/disk consequences are credited
established-source applications. All bundled n>=3, arbitrary local/manifold and
stronger smooth variants there remain unresolved. No discovery, full solution,
exhaustive novelty audit, earliest worldwide recognition, paper/newDOI/tracker
or external human review is claimed. Original1/5, new0/audit0. Current model,
reasoning and deadline are not inferred from original archival labels. The NEW
whole-current-packet source-first gate remains pending without verdict transfer.

Primary references: https://arxiv.org/pdf/math/0303258 ;
https://doi.org/10.1017/S0305004197002272 ;
https://arxiv.org/pdf/1510.06663v1 ;
https://www.cambridge.org/core/services/aop-cambridge-core/content/view/0C64B48E1D93B4C117C7A327B79613D7/S0008414X00024007a.pdf/div-class-title-a-short-proof-of-the-cartwright-littlewood-fixed-point-theorem-div.pdf ;
https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf .
"""
    outputs["SOURCES.md"] = source_scope.encode()
    outputs["CURRENT_SOURCE_SCOPE.md"] = source_scope.encode()
    outputs["CURRENT_CONTEXT.md"] = (summary + "\nThe exact complete statement follows without editing:\n\n" + problem["statement"] + "\n\nThe exact complete background and dated literature triage follow without editing:\n\n" + problem["background"] + "\n").encode()
    budget = {"original_substantive_attempts": 1, "used_substantive_attempts": 1, "maximum_substantive_attempts": 5,
              "cumulative_attempts": "1/5", "new_substantive_attempts": 0, "verification_attempts": 0,
              "current_model": None, "current_reasoning_effort": None, "current_deadline_utc": None,
              "current_runtime_exposure": "Model/reasoning not independently exposed; no new deadline inferred",
              "historical_original_model": turns["model"], "historical_original_reasoning_effort": turns["reasoning_effort"],
              "historical_original_time_cap_utc": turns["time_cap_utc"], "historical_original_response_date": turns["responses"][0]["date"],
              "historical_only": True}
    common_admin = {"utc": now, "id": ID, "code": CODE, "pr": 37, "current_gate": GATE,
                    "queue_outcome_requested": "unsolved", "budget": budget, "source_qualification": SOURCE_QUALIFIER,
                    "review_hash": PAIR_HASH, "statement_hash": STATEMENT_HASH, "exact_target": problem["statement"],
                    "source_record_sha256": sha(original["source_record.json"]), "current_partial_sha256": sha(current_partial),
                    "root_pinned_problem_sha256": sha(problem_raw), "entire_flat_source_full_JSON_equal": True,
                    "original_partial_sha256": sha(original["PARTIAL.md"]), "original_turns_sha256": sha(original["turns.json"]),
                    "native_queue_lifecycle_claimed": False, "native_historical_readiness_or_proof_event_claimed": False,
                    "current_model": None, "current_reasoning_effort": None, "current_deadline_utc": None,
                    "full_problem_solved": False, "positive_novelty_claim": False, "paper_or_new_doi_or_tracker": False,
                    "current_workflow_completion_estimate_percent": 75, "full_resolution_completion_estimate_percent": 0,
                    "low_dimensional_known_consequence_verified": True,
                    "closed_family_count": 3, "root_actual_reproduction_receipt_sha256": args.root_receipt_sha256,
                    "no_original_or_family_verdict_transferred": True,
                    "unresolved_scope": ["n>=3 full-space", "n>=3 boundary-fixed balls", "arbitrary local/manifold variants", "stronger smooth recurrence there"],
                    "separate_prior_report_present": False, "importer_empty_fallback_is_not_retrieved_report": True}
    outputs["readiness.json"] = json_bytes({**common_admin, "status": GATE,
                                             "primary_sources": "Exact version/page/proof/read/failure ledgers in SOURCES.md, final root certificate and all three closed families",
                                             "success_test": "Entire exact bundled target requires a proof/counterexample; current verified low-dimensional deduction does not meet it",
                                             "prior_attempt_gap": "No n>=3/local/manifold/stronger smooth mechanism; no compact cyclic closure supplied"})
    outputs["status.json"] = json_bytes({**common_admin, "status": "unsolved_proposed_pending_NEW_whole_gate", "original_head": HEAD, "actual_original_base": BASE})
    outputs["CURRENT_NATIVE_HISTORICAL_STATE.json"] = json_bytes({"scope": "Actual original head/base native state bytes are both empty; no event reconstructed", "states": historical_state, "original_ledger_preserved": True})
    outputs["CURRENT_QUEUE_PATCH.json"] = json_bytes({"utc": now, "phase": "Prospective exact named-row patch only; no live queue write", "id": ID,
                                                      "header_names": headers, "column_count": 12, "whole_queue_preimage_sha256": sha(queue_raw),
                                                      "whole_queue_prospective_sha256": sha(prospective_queue), "row_before": before, "row_prospective": after,
                                                      "allowed_named_changes": ["Status", "Turns", "Findings"], "allowed_split_field_indices": [8, 9, 11],
                                                      "all_unrelated_bytes_and_Chat_DOI_preserved": True, "current_gate": GATE,
                                                      "integration_guard": "Recheck whole live preimage. If unrelated acceptances intervene, prepare and receipt a fresh exact named-row rebase preserving every other byte; never replay original PR diff."})
    outputs["CURRENT_AUDIT_SCOPE.md"] = ("""# NEW whole-current-packet source-first gate remains pending

Begin with the entire flat pinned source, dated triage and labelled importer
fallback, then independently challenge every current proof/source/credit/body/
metadata/status/log/ledger/queue field and exact original/family/root dependency.
Test all-power common bound, D=0, proper joint homotopy, orientation, chordal
tail and compact-region recurrence, connected orbit-ball union, closure/filling,
unbounded component invariance, strict >6D separation, imported theorem hypotheses,
interval/disk pasting, source publication-versus-version wording, actual proof
reading and access failures, model/date/deadline archival scope, original1/5,
new0/audit0, native empty historical state, metadata-only independent stdout,
byte/fullJSON receipts, canonical audit anchor and twelve-column queue preservation.

All original/family verdicts are input evidence only. Hashes detect changed bytes,
not false mathematics. No current clean verdict or acceptance is claimed.
All n>=3/local/manifold/stronger smooth variants remain unresolved; theorem
imports are not finite computed certificates. No new mathematical search is
performed here. Audit workflow estimate75%; full-target resolution estimate0%.
""" + "\n" + SOURCE_QUALIFIER + "\n").encode()
    outputs["RESEARCH_LOG.md"] = (f"# Current PR37 research/audit log\n\n{now} — checkpoint: current workflow75%; full-target resolution0%. Credited low-dimensional consequence verified and complete target unsolved. Original13 exact artifacts and14-path diff, unchanged1/5 ledger and empty historical native states preserved; three closed first-party families and actual root reproduction bound. Three current PARTIAL replacements affect source/runtime wording only; precise old/new bytes and patch retained. {SOURCE_QUALIFIER} Root directly read Hamilton1954 all three pp522–524; Brown1977 access remains failed. Original complete31/8462 generated files BYTE/fullJSON equal; independent stdout is separately checked metadata serialization. No mathematical search/repair, new0/audit0. Original dated model/reasoning/deadline archival; current exposures unverified and current deadline null. NEW whole current source-first gate pending, no transferred verdict, paper/newDOI/tracker, outside-person communication or shared write.\n").encode()
    outputs["CURRENT_PROOF_DEPENDENCIES.json"] = json_bytes({"utc": now, "dependency_anchor_repository_relative": str(audit.relative_to(repo)),
                                                           "resolution_rule": "Resolve every path against repository_root/dependency_anchor_repository_relative, including copies in canonical attempts; never against the packet parent",
                                                           "closed_family_count": 3, "closed_authored_member_count": sum(family_counts.values()),
                                                           "family_member_counts": family_counts, "optional_root_support": optional_support,
                                                           "third_family_closure_manifest_path": third_manifest_rel,
                                                           "third_family_inventory_schema": "External root hashed closure of all21 unchanged recurrence files, including original self-including allowlist and20-pin verifier receipt; not a self-excluding original hash manifest",
                                                           "scope": "Two original self-excluding hashed family manifests and external root hashed closure of all21 recurrence files, every48 authored member; exact original13/14diff/frozenmetadata/entire flat source/fallback/unchangedledger; explicit actual root collector/receipts/final source certificate/executedbuilder. Foreign source bytes and scratch excluded.",
                                                           "files": sorted(dependencies.values(), key=lambda x: x["path"])})
    outputs["CURRENT_BUILD_RECEIPT.json"] = json_bytes({"utc": now, "kind": "Administrative exact-input/source-wording freeze, not mathematical replay or current approval",
                                                       "original13_git_bytes_modes_blobs_verified": True, "original14_diff_verified": True,
                                                       "original_archive_member_count": 13, "original_turns_BYTE_exact": True,
                                                       "source_record_entire_flat_raw_BYTE_exact": True, "source_only_current_partial_patch_receipt": "CURRENT_PARTIAL_SOURCE_PATCH_RECEIPT.json",
                                                       "root_receipt_sha256": args.root_receipt_sha256, "root_scope_certificate_sha256": args.root_scope_certificate_sha256,
                                                       "actual_builder_audit_relative": str(script.relative_to(audit)), "actual_builder_sha256": sha(script.read_bytes()),
                                                       "actual_root_family_replay_script": root_script_rel, "actual_root_family_replay_script_sha256": args.root_replay_script_sha256,
                                                       "closed_family_count": 3, "closed_authored_members_bound": sum(family_counts.values()),
                                                       "third_external_root_closure_manifest_path": third_manifest_rel, "third_original_allowlist_preserved_with_self_inclusion": True,
                                                       "root_actual_outer_runs": len(root_receipt["actual_outer_program_runs"]), "root_full_structured_comparisons": len(root_receipt["full_structured_receipt_comparisons"]),
                                                       "optional_root_support": optional_support, "current_gate": GATE,
                                                       "new_substantive_attempts": 0, "verification_attempts": 0, "live_queue_state_history_inventory_remote_canonical_writes": 0})
    for member in dependencies.values():
        raw = (audit / member["path"]).read_bytes()
        require(len(raw) == member["bytes"] and sha(raw) == member["sha256"], f"Input changed before freeze: {member['path']}")
    require(queue_path.read_bytes() == queue_raw, "Live queue changed during preparation; retain evidence and restart after reviewed fresh preimage")
    stage = audit / f"reviewed_candidate.preparation_{stamp}"
    require(not stage.exists(), "Unique staging collision")
    stage.mkdir()
    try:
        for rel, raw in sorted(outputs.items()):
            path = stage / str(safe_relative(rel))
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("xb") as handle:
                handle.write(raw)
        require({str(p.relative_to(stage / "original_archive")) for p in (stage / "original_archive").rglob("*") if p.is_file()} == set(original), "Archive must contain exactly original13")
        for rel, raw in original.items():
            require((stage / "original_archive" / rel).read_bytes() == raw, f"Archive byte difference: {rel}")
        for rel in HISTORICAL_TOP:
            require((stage / rel).read_bytes() == original[rel], f"Historical unchanged diagnostic/source/ledger changed: {rel}")
        manifest_members = [{"path": str(p.relative_to(stage)), "bytes": p.stat().st_size, "sha256": sha(p.read_bytes())} for p in sorted(stage.rglob("*")) if p.is_file()]
        manifest = {"utc": now, "schema": "strict_self_excluding_current_packet_v1", "self_excluded": ["MANIFEST.json"],
                    "files_count": len(manifest_members), "files": manifest_members, "scope": "Exact original13 archive plus current credited low-dimensional partial administration; NEW whole gate pending", "queue_outcome_proposed": "unsolved"}
        with (stage / "MANIFEST.json").open("xb") as handle:
            handle.write(json_bytes(manifest))
        actual = {str(p.relative_to(stage)) for p in stage.rglob("*") if p.is_file()}
        require(actual == {entry["path"] for entry in manifest_members} | {"MANIFEST.json"}, "Strict self-excluding inventory mismatch")
        for member in manifest_members:
            raw = (stage / member["path"]).read_bytes()
            require(len(raw) == member["bytes"] and sha(raw) == member["sha256"], f"Current binding differs: {member['path']}")
        require(not destination.exists(), "Current destination appeared; preserve stage and review separately")
        os.rename(stage, destination)
    except BaseException:
        failure = {"utc": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "FAILED_BUILD_PRESERVED", "stage": str(stage),
                   "traceback": traceback.format_exc(), "new_substantive_attempts": 0}
        with (stage / "BUILD_FAILURE.json").open("xb") as handle:
            handle.write(json_bytes(failure))
        raise
    print(json.dumps({"status": "CURRENT_PACKET_FROZEN_NEW_WHOLE_GATE_PENDING", "destination": str(destination),
                      "members": len(manifest_members), "dependencies": len(dependencies), "manifest_sha256": sha((destination / "MANIFEST.json").read_bytes()),
                      "proposed_queue_status": "unsolved", "attempts": "1/5", "new_substantive_attempts": 0, "verification_attempts": 0, "shared_writes": 0}, indent=2))


if __name__ == "__main__":
    main()

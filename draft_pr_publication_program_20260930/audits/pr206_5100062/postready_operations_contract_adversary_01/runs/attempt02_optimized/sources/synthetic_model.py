"""Explicitly synthetic offline model. No actual records are read or copied.

This module invents all checkpoint, blob, file and package identities. PR206 and
original HEAD are fixed interface constants required to exercise those guards;
the model is never operational authority and no service action is possible.
"""
import hashlib
import json

PREFIX = "draft_pr_publication_program_20260930/audits/pr206_5100062/"
PROGRAM = "draft_pr_publication_program_20260930/"
HEAD = "488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7"
CHECKPOINT = "f" * 40
PARENT = "e" * 40
QUEUE = "unsolved_math_prioritization/QUEUE.md"
FIVE = [PREFIX + "CURRENT_CASE_STATUS.json", PREFIX + "RESEARCH_LOG.md", PROGRAM + "CURRENT_PROGRESS.json", PROGRAM + "CURRENT_PROGRESS.md", PROGRAM + "RESEARCH_LOG.md"]
ALIASES = {"Root_publication_gate_pin", "package", "package_seal", "publication_ready", "NEW_whole_package_reviews_completed", "whole_package_review_loop_complete", "mathematical_clearance", "source_contract_clearance", "priority_clearance", "priority_novelty_clearance", "historical_firstness_independence_established", "actual_publication_verified", "actual_tracker_row_verified", "actual_original_PR_merged", "completed", "fully_completed_count", "published_count", "last_completed_PR", "next_numeric_intake_cursor", "advance_to_next_PR_authorized_now", "goal_complete"}

def enc(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()

def pin(raw):
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def identity(raw):
    return {**pin(raw), "git_blob": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()}

def map_digest(selected):
    return hashlib.sha256(json.dumps(selected, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def selected_map(inputs=None):
    result = {QUEUE: identity(b"EXPLICIT SYNTHETIC QUEUE\n")}
    for index, name in enumerate(FIVE):
        result[name] = identity(("EXPLICIT SYNTHETIC POSTIMAGE %d\n" % index).encode())
    result.update(inputs or {})
    index = 0
    while len(result) < 4788:
        result["SYNTHETIC_OFFLINE_SELECTED/file_%05d.txt" % index] = identity(("EXPLICIT SYNTHETIC SELECTED %d\n" % index).encode())
        index += 1
    if len(result) != 4788:
        raise RuntimeError("Synthetic map input count exceeded expected actual contract count")
    return result

def acceptance(selected, gate_pin, package="SYNTHETIC_PACKAGE", package_seal=None, map_pin=None):
    facts = {"Root_publication_gate_pin": gate_pin, "package": package,
        "package_seal": package_seal or pin(b"EXPLICIT SYNTHETIC PACKAGE SEAL\n"),
        "publication_ready": True, "NEW_whole_package_reviews_completed": 2,
        "whole_package_review_loop_complete": True, "mathematical_clearance": True,
        "source_contract_clearance": True, "priority_clearance": True,
        "priority_novelty_clearance": False, "historical_firstness_independence_established": False,
        "actual_publication_verified": False, "actual_tracker_row_verified": False,
        "actual_original_PR_merged": False, "completed": False,
        "fully_completed_count": 48, "published_count": 32, "last_completed_PR": 205,
        "next_numeric_intake_cursor": 206, "advance_to_next_PR_authorized_now": False,
        "goal_complete": False, "bounded_priority_audit_complete": True,
        "qualified_attributed_note_editorially_cleared": True,
        "priority_clearance_scope": "qualified_attributed_note_only", "case_percent": 90,
        "actual_merge_accepted": False, "actual_factual_accepted": False,
        "record_id": None, "DOI": None, "tracker_range": None}
    result = {"schema": "pr206-lifecycle-actual-acceptance-v1", "evidence_scope": "ACTUAL_ROOT_RECEIPT",
        "UTC": "2000-01-01T00:00:00+00:00", "PR": 206, "phase": "ready", "accepted": True,
        "case_percent": 90, "checkpoint_commit": CHECKPOINT, "parents": [PARENT],
        "sole_parent": PARENT, "main_observed": CHECKPOINT, "actual_tree": "d" * 40,
        "original_head": HEAD, "selected_files": len(selected),
        "selected_map_sha256": map_digest(selected),
        "actual_current_selected_map_sha256": map_digest(selected),
        "actual_current_map_file": map_pin or pin(enc({"selected_files": selected, "selected_map_sha256": map_digest(selected), "foreign_QUEUE_reconciliation_after_checkpoint": {}})),
        "every_selected_identity_checked_at_actual_observed_MAIN": True,
        "all_overlay_body_identities_verified": True, "full_foreign_tree_scope_preserved": True,
        "original_native_custody_retained": True, "actual_original_PR_head": HEAD,
        "actual_original_PR_is_draft": True, "actual_original_PR_state": "open", "facts": facts}
    result.update({name: facts[name] for name in ALIASES})
    return result

def pointer(acceptance_pin):
    return {"schema": "pr206-lifecycle-actual-pointer-v1", "PR": 206, "phase": "ready",
        "Root_recorded_only_after_actual_full_scope_acceptance": True,
        "UTC": "2000-01-01T00:00:00+00:00", "directory": "SYNTHETIC_OFFLINE_READY",
        "acceptance_pin": acceptance_pin, "checkpoint_commit": CHECKPOINT,
        "main_observed": CHECKPOINT, "fresh_MAIN_revalidated_before_pointer": CHECKPOINT}

def proof(selected, gate_pin, pointer_pin, acceptance_pin, map_pin):
    return {"schema": "pr206-root-actual-ready-verification-v1", "evidence_scope": "ACTUAL_ROOT_RECEIPT",
        "UTC": "2000-01-01T00:00:00+00:00", "PR": 206, "accepted": True,
        "actual_ready90_fully_accepted_synced_and_pointer_verified": True,
        "checkpoint_commit": CHECKPOINT, "actual_main_observed": CHECKPOINT,
        "selected_files": 4788, "actual_selected_map_sha256": map_digest(selected),
        "actual_acceptance_pin": acceptance_pin, "actual_ready_pointer_pin": pointer_pin,
        "actual_selected_map_file_pin": map_pin, "actual_publication_gate_pin": gate_pin,
        "ready_candidate_changed_path_count": 377,
        "ready_candidate_changed_paths_exclude_QUEUE_and_all_native_attempts": True,
        "original_native_custody_retained": True, "actual_original_PR_head": HEAD,
        "actual_original_PR_is_draft": True, "actual_original_PR_state": "open",
        "every_selected_identity_checked_at_actual_observed_MAIN": True,
        "all_overlay_body_identities_verified": True, "full_foreign_tree_scope_preserved": True,
        "all_three_actual_steps_and_six_alias_cleanups_verified": True,
        "all_five_local_readonly_native_postimages": [{"path": path, "identity": selected[path], "mode": "0o444", "regular": True} for path in FIVE],
        "actual_original_PR_merged": False, "actual_publication": False, "actual_tracker": False,
        "advance": False, "case_completion_estimate_percent": 90,
        "completed_count": 48, "published_count": 32, "cursor": 206,
        "QUEUE_parent_and_checkpoint_entries": [["100644", "blob", "c" * 40], ["100644", "blob", "c" * 40]],
        "native_attempt_parent_and_checkpoint_entries": [None, None],
        "independent_native_tree_objects_authenticated": 4,
        "fresh_PR_API_info_pin": pin(b"EXPLICIT SYNTHETIC PR INFO\n"),
        "historical_final07_publisher_contract_mismatch": "EXPLICIT SYNTHETIC OFFLINE FIXTURE; never actual authority"}

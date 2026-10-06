"""Record completed public access checks while retaining unresolved priority."""
from pathlib import Path
import datetime as dt
import hashlib
import json

F = Path(__file__).resolve().parent
A = F.parent
P = A.parents[1]
C = A.parent / "pr45_9900007"
N = A / "nencka_cpt_access_20261004"

def pin(path):
    body = path.read_bytes()
    return {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}

static = json.loads((F / "STATIC_ARCHIVE_READBACK.json").read_text())
assert len(static["indexes"]) == 5
assert all(item["http_status"] == 200 and item["status"] == "FULL_STATIC_INDEX_ACCESSED" for item in static["indexes"])
assert all(match["count"] == 0 for item in static["indexes"] for match in item["literal_index_matches"])
pr = json.loads((C / "root_pr50_priority_blocker_current_pr_20261004_actual_capture/stdout.bin").read_text())
assert pr["state"] == "OPEN" and pr["isDraft"] is True
assert pr["headRefOid"] == "7260315f8b8b193020c09d4ef6df9d943a3a13ff"
final = json.loads((A / "root_current_promotion_20261004/V3_FINAL_REVIEW_AND_PRIORITY_HOLD.json").read_text())
for name, expected in final["reviewed_upload_pins"].items():
    actual = pin(A / "publication_package_v3" / name)
    assert actual["bytes"] == expected["size"] and actual["sha256"] == expected["sha256"]
catalog = json.loads((N / "private/catalog_scan_summary.json").read_text())
assert [record["page"] for record in catalog["records"]] == list(range(322, 331))
assert all(record["bytes"] > 17000 and record["exact_target_or_related_word_matches"] == [] for record in catalog["records"])
now = dt.datetime.now(dt.timezone.utc).isoformat()
record = {"schema": "pr50-public-source-access-continuation/v1", "UTC": now,
    "previous_goal_turn": "progress: repaired v3 payload and NEW complete review checkpoint committed and pushed as b1d6064eb0053255c3c3d438de5ecc83f97e27d9",
    "current_goal_turn": "progress: newly authenticated CPT and relocated mp_arc access routes completed with actual retained evidence",
    "same_priority_blocking_condition_observed_goal_turns_in_current_run": 2,
    "persistent_goal_status": "active; blocked threshold not yet reached",
    "current_PR_readback": pr,
    "four_reviewed_upload_pins_unchanged": True,
    "public_access_bindings": {
        "CPT_ROUTE_ACCESS.json": pin(F / "CPT_ROUTE_ACCESS.json"),
        "MP_ARC_ROUTE_ACCESS.json": pin(F / "MP_ARC_ROUTE_ACCESS.json"),
        "STATIC_ARCHIVE_READBACK.json": pin(F / "STATIC_ARCHIVE_READBACK.json"),
        "independent_CPT_ACCESS_LIMIT.md": pin(N / "ACCESS_LIMIT.md"),
        "independent_CPT_RESEARCH_LOG.md": pin(N / "RESEARCH_LOG.md")},
    "static_archive_limit": "Complete fetched1995-1999 indexes contain no literal Nencka/Cantorian/braid matches; actual author search returned500 and did not supply a result. Archive coverage is not the whole literature.",
    "independent_CPT_limit": "Historical Alexandrie link404; current catalog pages322-330 and visible fuzzy search yield no usable target. Historical catalog coverage is unverified.",
    "full_Nencka_body_acquired": False,
    "exact_remaining_requirement": "Legitimate full1998/1999 Nencka text or alternate1996 CPT96/P.3381 body, followed by full individual source assessment of its model, closure equivalence, all-even convention and proof.",
    "institution_or_full_text_information_request": "already pending; no answer received in this goal turn",
    "AMS_browser_access": "Previous tab handle was missing. A new official chapter navigation reaches institutional login; no institution, credentials or authentication submission used. New tab retained for handoff.",
    "no_inference_from_failed_access": ["novelty", "absence", "invalidity", "different proven model", "already_solved disposition"],
    "new_central_proof_attempts": 0, "submitted_attempt_budget": "1/5",
    "outside_outreach_or_credential_use": False,
    "priority_clearance": False, "publication_approval": False,
    "PR_merge_close_or_advance": False, "Zenodo_or_tracker_action": False,
    "completion_estimates": {"new_bounded_access_routes_percent": 100, "v3_math_and_package_review_percent": 100, "priority_audit_percent": 60, "PR50_publication_workflow_percent": 0, "program_complete_percent": 3.030303},
    "goal_complete": False}
dest = F / "SOURCE_ACCESS_CONTINUATION.json"
assert not dest.exists()
dest.write_text(json.dumps(record, indent=2) + "\n")
progress_path = P / "CURRENT_PROGRESS.json"
progress = json.loads(progress_path.read_text())
assert progress["current_PR"] == 50 and progress["current_priority_clearance"] is False
progress["UTC"] = now
progress["current_priority_access_readback"] = str(dest.relative_to(P))
progress_path.write_text(json.dumps(progress, indent=2) + "\n")
entry = (f"\n\n## {now} — new public source routes exhausted; priority remains unresolved\n\n"
    "Followed the actually reachable CPT historical preprint locator and current official laboratory links. The independently audited Alexandrie route returns404; nine relevant-period catalog pages and visible site search produced no usable target. Followed the relocated University of Texas mp_arc homepage after the old link failed. Its live author search returns500, not zero matches. All five observed1995-1999 static index links were fetched completely and checked without finding the literal author/title/related word. These bounded access results certify neither absence nor invalidity nor novelty. No full Nencka body was acquired.\n\n"
    "Fresh remote PR50 readback is OPEN/draft at unchanged head7260315f8b8b193020c09d4ef6df9d943a3a13ff. All four reviewed v3 payload pins remain unchanged; no scientific repair, extra central attempt or publication-state action was made. The institutional/full-text information request is still pending. The missing old browser handle was replaced with a new official AMS login page without entering credentials or choosing an institution. Raw bodies and historical form details remain ignored/private; embedded guest credentials were not used.\n\n"
    "Previous goal turn: concrete v3 repair/review/push progress. Current goal turn: new bounded source-access evidence. The same fuller-source priority blocker has now appeared in two consecutive goal turns; the persistent goal remains active and is not marked complete or blocked prematurely. New access-route audit100%; broad priority audit60%; v3 mathematics/package review100%; PR50 publication workflow0%; program3/99=3.030303%. These are workflow estimates.\n")
(F / "RESEARCH_LOG.md").write_text("# PR50 alternate public preprint access\n" + entry)
with (A / "ROOT_RESEARCH_LOG.md").open("a") as stream:
    stream.write(entry)
print(json.dumps({"UTC": now, "status": "PASS_SOURCE_ACCESS_LIMITS_AND_UNCHANGED_PAYLOAD_BINDINGS", "full_body_acquired": False, "priority_clearance": False, "record": str(dest), "goal_complete": False}, indent=2))

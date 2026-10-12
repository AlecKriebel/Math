"""Bind the completed fresh v3 review without changing any reviewed payload."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import zipfile

F = Path(__file__).resolve().parent
A = F.parent
P = A.parents[1]
B = A / "publication_package_v3"
V = A / "v3_wholepackage_adversary_20261004"

def pin(path):
    body = path.read_bytes()
    return {"size": len(body), "sha256": hashlib.sha256(body).hexdigest()}

inputs = json.loads((V / "INPUT_PINS.json").read_text())
verdict = json.loads((V / "VERDICT.json").read_text())
names = ["even_strand_markov.tex", "even_strand_markov.pdf", "even-strand-markov-verification-v3.zip", "zenodo-deposit.json"]
for name in names:
    assert pin(B / name) == inputs[name], name
assert verdict["mandatory_upload_package_repairs_found"] == []
assert verdict["portable_package"] == "PASS_ACTUAL_REPRODUCTION"
assert verdict["mathematical_scope"] == "PASS_CONDITIONAL_ON_EXPLICIT_ESTABLISHED_IMPORTS"
assert verdict["priority"] == "HOLD_FULLER_PRIMARY_BODIES_UNREAD"
assert verdict["publication_approval"] is False
assert verdict["global_novel_contribution_certified"] is False
assert verdict["checks"] == 7114 and verdict["new_central_proof_attempts"] == 0
with zipfile.ZipFile(B / names[2]) as archive:
    members = archive.infolist()
    assert [m.filename for m in members] == [m["name"] for m in inputs["zip_members"]]
    for actual, expected in zip(members, inputs["zip_members"]):
        data = archive.read(actual)
        assert actual.filename == Path(actual.filename).name
        assert len(data) == expected["size"]
        assert hashlib.sha256(data).hexdigest() == expected["sha256"]
        assert data == (B / actual.filename).read_bytes()
        assert tuple(actual.date_time) == tuple(expected["date_time"])
        assert actual.external_attr == expected["external_attr"]
now = dt.datetime.now(dt.timezone.utc).isoformat()
decision = {
    "schema": "pr50-root-final-v3-review-and-priority-hold/v1", "UTC": now,
    "submitted_head": verdict["submitted_head"], "submitted_status": "claimed_solved 1/5",
    "new_central_proof_attempts": 0,
    "exact_target": "Fenn-Ilyutko-Kauffman-Manturov Problem42; only-even-strand ordinary oriented unframed classical and virtual braid closure",
    "mathematical_review": verdict["mathematical_scope"],
    "portable_package_review": verdict["portable_package"],
    "mandatory_upload_package_repairs_found": [],
    "review_chain": [
        {"version": 1, "finding": "Fair credit to authenticated Nencka1996 announcement required; priority hold"},
        {"version": 2, "finding": "Zero-shift mutant survived shared-helper diagnostics; independent literal source controls required; priority hold"},
        {"version": 3, "finding": "Fresh from-scratch whole-package review finds no further mathematics or payload repair; priority hold remains"}
    ],
    "fresh_review_bindings": {name: pin(V / name) for name in ["REPORT.md", "VERDICT.json", "INPUT_PINS.json", "INDEPENDENT_RECONSTRUCTION.md", "PRIMARY_PINS.json"]},
    "reviewed_upload_pins": {name: inputs[name] for name in names},
    "reviewed_zip_members": inputs["zip_members"],
    "root_post_review_pin_readback": "PASS; four pins and all ten members match the fresh review",
    "actual_reproduction": {key: verdict[key] for key in ["actual_checker_pid", "actual_checker_exit", "checks", "actual_result_sha256", "actual_zip_builder_pid", "actual_zero_shift_mutant_pid", "actual_zero_shift_mutant_exit", "actual_tex_rebuild_pid", "five_rebuilt_page_pngs_byte_identical"]},
    "priority_clearance": False, "global_novel_contribution_certified": False,
    "publication_approval": False, "Zenodo_stage_or_publish_performed": False,
    "DOI": None, "tracker_append_performed": False, "PR_merge_performed": False,
    "PR_close_performed": False, "advance_to_next_PR_authorized_now": False,
    "exact_remaining_gap": "Read and individually assess the fuller Nencka1998/1999 bodies, or authenticated alternate1996 CPT96/P.3381 preprint, for ordinary-closure meaning, complete proof, one-strand levels and priority; globally correct and commission a NEW exact-input review if payloads change.",
    "unread_sources_are_not_evidence_of": ["absence of an earlier resolution", "invalidity", "a proved different model", "already_solved disposition"],
    "human_peer_review": False, "formal_proof_certification": False,
    "completion_estimates": {"v3_mathematical_and_package_review_percent": 100, "diagnostic_repair_percent": 100, "priority_audit_percent": 60, "current_PR_publication_workflow_percent": 0, "fully_completed_program_percent": 3.030303},
    "completion_estimate_meaning": "Workflow progress, not mathematical certainty; source access remains substantive and may change the outcome.",
    "goal_complete": False,
    "preserved_preparatory_snapshots": ["V3_REPAIR_BINDING_AND_PRIORITY_HOLD.json", "V2_PREPARATION_AND_PRIORITY_HOLD.json"]
}
dest = F / "V3_FINAL_REVIEW_AND_PRIORITY_HOLD.json"
assert not dest.exists(), "Preserve previous decisions instead of overwriting them"
dest.write_text(json.dumps(decision, indent=2) + "\n")
progress_path = P / "CURRENT_PROGRESS.json"
progress = json.loads(progress_path.read_text())
assert progress["current_PR"] == 50 and progress["fully_completed_eligible_PRs"] == [9, 16, 18]
progress.update(UTC=now,
    remaining_current_step="Fresh v3 whole-package review completed cleanly for mathematics and payloads. Resolve fuller Nencka primary-source scope and priority before any publication, tracker append, merge or advance.",
    current_review_and_hold=str(dest.relative_to(P)),
    current_mathematical_and_package_review_percent=100,
    current_priority_audit_percent=60,
    current_priority_clearance=False)
progress_path.write_text(json.dumps(progress, indent=2) + "\n")
readme_path = P / "README.md"
text = readme_path.read_text()
old = "A NEW whole-package reviewer is checking v3 from scratch; the genuine strengthened author run passes7,114 checks and rejects the actual zero-shift mutant."
new = "A NEW whole-package reviewer completed v3 from scratch with no further mathematics or payload repairs; its actual 7,114-check reproduction matches exactly, and the strengthened controls reject an actual zero-shift mutant. This is mathematical/package clearance only: publication and novelty remain held pending fuller Nencka source assessment."
assert text.count(old) == 1
readme_path.write_text(text.replace(old, new))
entry = (f"\n\n## {now} — fresh v3 whole-package review complete; priority hold preserved\n\n"
    "ROOT fully read the NEW adversary's complete report and verdict and independently rechecked all four exact upload pins and every one of the ten ZIP members. No further mathematical or upload-package repair was found. The actual extracted 7,114-check run matches the shipped expected bytes; a genuine zero-shift mutant fails the literal primary-source control. The universal proof remains conditional on the explicitly credited established classical and virtual Markov imports. The review is AI verification, not conventional human peer review or formal proof certification.\n\n"
    "The earlier fair-credit and shared-helper diagnostic findings were repaired globally in v2/v3. The fuller Nencka1998/1999 bodies and possible alternate1996 twelve-page preprint remain unread. Their absence from accessible full text proves neither novelty nor invalidity nor a different closure model. The exact ordinary-closure priority comparison is the sole substantive promotion gate. The institution/full-text information request remains pending; no outside outreach was prepared or initiated. No deposition, DOI, tracker row, merge, close or advance occurred. The original submitted proof budget remains1/5 and this audit introduces zero central proof attempts.\n\n"
    "Completion estimates: v3 mathematics/package review100%; diagnostic repair100%; priority audit60%; PR50 publication workflow0%; fully completed program3/99=3.030303%. Estimates describe workflow, not mathematical certainty. Preserve prior timestamped preparatory records. Current decision: `root_current_promotion_20261004/V3_FINAL_REVIEW_AND_PRIORITY_HOLD.json`.\n")
for name in ["ROOT_CURRENT_REVIEW_20261004.md", "ROOT_RESEARCH_LOG.md"]:
    with (A / name).open("a") as f:
        f.write(entry)
print(json.dumps({"UTC": now, "status": "PASS_REVIEW_BINDINGS_AND_PRIORITY_HOLD", "decision": str(dest), "four_upload_pins_unchanged": True, "ten_members_unchanged": True, "publication_approval": False, "goal_complete": False}, indent=2))

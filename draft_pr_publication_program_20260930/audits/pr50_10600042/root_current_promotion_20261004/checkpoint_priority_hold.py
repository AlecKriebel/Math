"""Bind actual v2 preparation evidence and update only owned current progress."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import zipfile

F = Path(__file__).resolve().parent
A = F.parent
P = A.parents[1]
C = A.parent / "pr45_9900007"
V = A / "publication_package_v2"
now = dt.datetime.now(dt.timezone.utc).isoformat()
output = F / "V2_PREPARATION_AND_PRIORITY_HOLD.json"
assert not output.exists()
def binding(path):
    body = path.read_bytes()
    return {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
captures = {}
for name in (
    "root_pr50_v2_pdf_operation_marker_20261004_actual_capture",
    "root_pr50_v2_priority_revision_authoring_20261004_actual_capture",
    "root_pr50_v2_pdf_export_20261004_actual_capture",
    "root_pr50_v2_archive_build_20261004_actual_capture",
    "root_pr50_v2_pdf_info_20261004_actual_capture",
    "root_pr50_v2_pdf_render_20261004_actual_capture",
    "root_pr50_v2_pdf_text_20261004_actual_capture",
    "root_pr50_v2_manifest_check_20261004_actual_capture",
):
    record = json.loads((C / name / "CAPTURE.json").read_text())
    assert record["status"] == "PASS" and record["actual_execution"] and record["completed"]
    assert record["operator_unchanged"] and record["exit_code"] == 0 and type(record["pid"]) is int
    for stream in ("stdout", "stderr"):
        assert binding(C / name / record[stream]["path"]) == {"bytes": record[stream]["bytes"], "sha256": record[stream]["sha256"]}
    captures[name] = {"record_binding": binding(C / name / "CAPTURE.json"), "actual_child_pid": record["pid"],
                      "started_utc": record["started_utc"], "finished_utc": record["finished_utc"]}
members = ("LICENSE-CODE.txt", "LICENSE-TEXT.md", "README.md", "SHA256SUMS", "SOURCE_QUALIFICATIONS.md", "VERIFICATION_RECORD.json", "build_verification_zip.py", "even_strand_markov.tex", "expected_results.json", "verify_even_calculus.py")
member_bindings = {name: binding(V / name) for name in members}
checksums = dict(row.split("  ", 1)[::-1] for row in (V / "SHA256SUMS").read_text().splitlines())
assert set(checksums) == set(members) - {"SHA256SUMS"}
for name, digest in checksums.items():
    assert member_bindings[name]["sha256"] == digest
with zipfile.ZipFile(V / "even-strand-markov-verification-v2.zip") as z:
    assert tuple(z.namelist()) == members and z.testzip() is None
    for name in members:
        info = z.getinfo(name)
        assert z.read(name) == (V / name).read_bytes()
        assert info.date_time == (1980, 1, 1, 0, 0, 0) and info.external_attr >> 16 == 0o100644
    assert not any("private" in name.lower() for name in z.namelist())
manifest = json.loads((V / "zenodo-deposit.json").read_text())
assert set(manifest) == {"metadata", "files"}
assert manifest["metadata"]["creators"] == [{"name": "Kriebel, Alec", "orcid": "0009-0001-9320-500X"}]
assert manifest["files"] == [{"path": "even_strand_markov.pdf", "name": "even_strand_markov.pdf"}, {"path": "even-strand-markov-verification-v2.zip", "name": "even-strand-markov-verification-v2.zip"}]
tex = (V / "even_strand_markov.tex").read_text()
assert "\\bibitem{Nencka}" in tex and "natural induction" not in tex and "zeroth" not in tex
assert "Neither a minimal" in tex and "No historical-priority or present-openness claim" in tex
record = json.loads((V / "VERIFICATION_RECORD.json").read_text())
assert record["manuscript_provenance"]["submission_tex_binding"] == member_bindings["even_strand_markov.tex"]
assert record["actual_completed_run"]["child_pid"] == 95899
assert record["checker_binding"] == member_bindings["verify_even_calculus.py"]
assert record["expected_result_binding"] == member_bindings["expected_results.json"]
root_dated = json.loads((V / "REVISION_PREPARATION.json").read_text())
for name, digest in root_dated["frozen_v1_four_pins_unchanged"].items():
    assert binding(A / "publication_package_v1" / name)["sha256"] == digest
verdict = json.loads((A / "current_promotion_adversary_20261004" / "VERDICT.json").read_text())
assert verdict["review_complete"] and verdict["publication_clearance"] is False
assert verdict["publication_package"] == "HOLD_PENDING_NAMED_PRIOR_WORK_QUALIFICATION"
pdf_info = (C / "root_pr50_v2_pdf_info_20261004_actual_capture" / "stdout.bin").read_text()
assert "Pages:           5" in pdf_info
assert len(list((F / "tmp" / "pdfs").glob("v2-page-*.png"))) == 5
log = (V / "even_strand_markov.log").read_text()
assert not any(term in log for term in ("Overfull", "Undefined", "undefined references", "Missing character"))
result = {
    "schema": "pr50-current-v2-preparation-priority-hold/v1", "UTC": now,
    "status": "PASS_PREPARATION_BINDINGS_HOLD_PRIORITY_AND_NEW_REVIEW",
    "final_payloads": {name: binding(V / name) for name in ("even_strand_markov.tex", "even_strand_markov.pdf", "even-strand-markov-verification-v2.zip", "zenodo-deposit.json")},
    "zip_members": member_bindings, "actual_captures": captures,
    "root_personally_viewed_v2_pdf_pages": 5,
    "native_compiler": {"api": "mcp__codex_app__compile_latex_document", "response": "The current source compiled successfully with the desktop editor's compiler.", "kind": "success", "tool_response_not_shell_execution": True},
    "named_prior_work_repair": "1996 announcement credited in source, bibliography, qualifications, README, verification provenance and intended metadata; full follow-up source priority decision pending.",
    "review_correction": "Actual Theorem3 says natural induction map, not zeroth induction map; unspecified natural-number convention alone justifies the possible one-strand caveat. The v2 payload does not repeat that transcription error.",
    "frozen_v1_unchanged": True, "new_substantive_proof_attempts": 0, "original_budget": "1/5",
    "new_v2_wholepackage_review_complete": False, "fuller_source_priority_decision_complete": False,
    "publication_approval": False, "DOI": None, "tracker_row": None, "merge": None,
    "mathematical_estimate_percent": 95, "revision_preparation_percent": 100, "priority_resolution_percent": 60,
    "PR50_workflow_percent": 0, "whole_goal_complete": False,
}
output.write_text(json.dumps(result, indent=2) + "\n")
progress_path = P / "CURRENT_PROGRESS.json"
progress = json.loads(progress_path.read_text())
assert progress["fully_completed_eligible_PRs"] == [9, 16, 18] and progress["current_PR"] == 50
progress.update(UTC=now, current_PR_workflow_percent=0,
                remaining_current_step="Complete NEW v2 whole-package adversarial review and resolve the authenticated Nencka1996/1998/1999 prior-work lead from fuller primary sources before publication.",
                next_eligible_PR_after_current_completion=55, advance_to_next_PR_authorized_now=False,
                current_priority_hold="Exact earlier ordinary-closure resolution unverified; fuller institutional full text requested, not inferred absent or invalid.",
                current_review_and_hold="audits/pr50_10600042/root_current_promotion_20261004/V2_PREPARATION_AND_PRIORITY_HOLD.json")
progress_path.write_text(json.dumps(progress, indent=2) + "\n")
readme_path = P / "README.md"
readme = readme_path.read_text()
anchor = "estimate: 100%. The next eligible PR is PR50. See `CURRENT_PROGRESS.json`."
assert readme.count(anchor) == 1
readme = readme.replace(anchor, "estimate: 100%. PR50 is now under active review: the mathematical theorem passes the fresh adversary, and a new v2 package credits Nencka's related 1996 announcement. Exact earlier ordinary-closure priority remains unresolved pending fuller 1998/1999 sources. A new whole-package reviewer is checking v2 from scratch. No PR50 publication, DOI, tracker entry or merge has occurred. The next eligible PR after completing PR50 is PR55. See `CURRENT_PROGRESS.json`.")
readme_path.write_text(readme)
append = "\n## " + now + " — fresh adversary hold and synchronized revision\n\nThe NEW v1 current-promotion adversary passed the universal theorem, literal ordinary-closure target, 1,760 independent legal pairs/5,280 necessary-invariant comparisons, exact extracted author result, rebuilt archive and all four original PDF pages. It correctly withheld publication for mandatory named Nencka1996 prior-work qualification; exact earlier valid resolution remains unverified. ROOT read its complete report/verdict and the actual two printed contribution pages and frontmatter. Correct the reviewer transcription: Theorem3 says natural induction map, not zeroth induction map. The possible n=0 caveat comes solely from an unspecified natural-number convention. The OCR-positive-only objection is withdrawn because the actual tail has ± signs. Preserve dated original reports and package.\n\nROOT prepared new publication_package_v2, crediting and carefully qualifying the announcement globally in the deliverable; the original scheme statements, proof and checker remain unchanged. Built-in compiler success, actual exported five-page PDF, all five personally viewed clean page images, normalized ten-member ZIP and local upload-manifest check are genuinely completed and bound in V2_PREPARATION_AND_PRIORITY_HOLD.json. New v2 whole-package review is in progress. An independent priority family authenticated 1998 and 1999 fuller follow-up identities, whose bodies are not yet accessible. Human institutional portal/full-text information was requested; no outreach was initiated. No publication approval follows from disclaimers alone. Mathematical estimate95%; revision preparation100%; priority resolution60%; current workflow0%; program3/99complete; goalunfinished. Budget remains1/5 with0newcentralattempts.\n"
with (A / "ROOT_CURRENT_REVIEW_20261004.md").open("a") as f:
    f.write(append)
with (A / "ROOT_RESEARCH_LOG.md").open("a") as f:
    f.write(append)
with (V / "RESEARCH_LOG.md").open("a") as f:
    f.write("\n## " + now + " — prepared artifact readbacks\n\nRevision preparation100%; priority resolution60%; current publication workflow0%. Built-in compiler succeeded. Actual PDF export PID64750, archive builder64751, PDF-info65019, render65018, text65017 and local manifest check66895 all exit0 with complete captured streams. ROOT personally inspected all5pages, with no layout defects. Ten portable members match exact source and checksums. New adversary and fuller-source priority disposition remain pending; no publication approval, DOI, tracker or merge.\n")
print(json.dumps({"status": result["status"], "UTC": now, "final_payloads": result["final_payloads"], "publication_approval": False, "priority_pending": True}, indent=2))

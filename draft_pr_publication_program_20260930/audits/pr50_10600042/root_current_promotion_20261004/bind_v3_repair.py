"""Read back the actual repaired v3 payload and preserve both unresolved gates."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import zipfile

F = Path(__file__).resolve().parent
A = F.parent
P = A.parents[1]
C = A.parent / "pr45_9900007"
V = A / "publication_package_v3"
def pin(path):
    b = path.read_bytes()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
def capture(name, expected_exit=0):
    d = C / name
    c = json.loads((d / "CAPTURE.json").read_text())
    assert c["status"] == "PASS" and c["exit_code"] == expected_exit
    assert c["actual_execution"] and c["completed"] and c["operator_unchanged"] and type(c["pid"]) is int
    for stream in ("stdout", "stderr"):
        assert pin(d / (stream + ".bin")) == {"bytes": c[stream]["bytes"], "sha256": c[stream]["sha256"]}
    return {"capture_binding": pin(d / "CAPTURE.json"), "actual_pid": c["pid"],
            "started_utc": c["started_utc"], "finished_utc": c["finished_utc"], "exit_code": expected_exit}
captures = {name: capture(name) for name in (
    "root_pr50_v3_diagnostic_revision_authoring_20261004_actual_capture",
    "root_pr50_v3_checker_actual_capture", "root_pr50_v3_interpreter_version_actual_capture",
    "root_pr50_v3_pdf_export_20261004_actual_capture", "root_pr50_v3_materials_finalization_20261004_actual_capture",
    "root_pr50_v3_archive_build_20261004_actual_capture", "root_pr50_v3_pdf_render_20261004_actual_capture",
    "root_pr50_v3_pdf_info_20261004_actual_capture", "root_pr50_v3_manifest_check_20261004_actual_capture")}
captures["root_pr50_v3_zero_shift_mutant_actual_capture"] = capture("root_pr50_v3_zero_shift_mutant_actual_capture", 1)
stderr = (C / "root_pr50_v3_zero_shift_mutant_actual_capture" / "stderr.bin").read_text()
assert stderr.endswith("ValueError: primary literal unrestricted left index shift\n")
mutant = (F / "tmp" / "zero_shift_v3.py").read_text()
source = (V / "verify_even_calculus.py").read_text()
assert mutant == source.replace("def shift(w): return tuple((t, i + 1, e) for t, i, e in w)", "def shift(w): return tuple((t, i, e) for t, i, e in w)") and mutant != source
expected = (V / "expected_results.json").read_bytes()
assert expected == (C / "root_pr50_v3_checker_actual_capture" / "stdout.bin").read_bytes()
result = json.loads(expected)
assert result["checks"] == 7114 and result["source_bound_left_controls"]["checks"] == 8
record = json.loads((V / "VERIFICATION_RECORD.json").read_text())
assert record["checker_binding"] == pin(V / "verify_even_calculus.py")
assert record["expected_result_binding"] == pin(V / "expected_results.json")
assert record["manuscript_provenance"]["submission_tex_binding"] == pin(V / "even_strand_markov.tex")
assert record["actual_completed_run"]["child_pid"] == 76825
members = ("LICENSE-CODE.txt", "LICENSE-TEXT.md", "README.md", "SHA256SUMS", "SOURCE_QUALIFICATIONS.md", "VERIFICATION_RECORD.json", "build_verification_zip.py", "even_strand_markov.tex", "expected_results.json", "verify_even_calculus.py")
checksums = dict(row.split("  ", 1)[::-1] for row in (V / "SHA256SUMS").read_text().splitlines())
assert set(checksums) == set(members) - {"SHA256SUMS"}
with zipfile.ZipFile(V / "even-strand-markov-verification-v3.zip") as archive:
    assert tuple(archive.namelist()) == members and archive.testzip() is None
    for name in members:
        assert archive.read(name) == (V / name).read_bytes()
        if name != "SHA256SUMS":
            assert pin(V / name)["sha256"] == checksums[name]
manifest = json.loads((V / "zenodo-deposit.json").read_text())
assert set(manifest) == {"metadata", "files"}
assert manifest["files"] == [{"path": "even_strand_markov.pdf", "name": "even_strand_markov.pdf"}, {"path": "even-strand-markov-verification-v3.zip", "name": "even-strand-markov-verification-v3.zip"}]
assert "ordinary-closure priority remains unresolved" in manifest["metadata"]["description"]
assert "**7,114 checks**" in (V / "README.md").read_text()
assert "Pages:           5" in (C / "root_pr50_v3_pdf_info_20261004_actual_capture" / "stdout.bin").read_text()
assert len(list((F / "tmp" / "pdfs").glob("v3-page-*.png"))) == 5
assert not any(term in (V / "even_strand_markov.log").read_text() for term in ("Overfull", "Undefined", "undefined references", "Missing character"))
prep = json.loads((V / "REVISION_PREPARATION.json").read_text())
for name, digest in prep["frozen_v2_pins"].items():
    assert pin(A / "publication_package_v2" / name)["sha256"] == digest
old_verdict = json.loads((A / "v2_wholepackage_adversary_20261004" / "VERDICT.json").read_text())
assert old_verdict["publication_as_user_requested_novel_contribution_approved"] is False
assert [x["id"] for x in old_verdict["findings"]] == ["F01", "F02"]
now = dt.datetime.now(dt.timezone.utc).isoformat()
output = F / "V3_REPAIR_BINDING_AND_PRIORITY_HOLD.json"
assert not output.exists()
receipt = {"schema": "pr50-v3-repair-and-priority-hold/v1", "UTC": now,
    "status": "PASS_SOURCE_BOUND_REPAIR_BINDINGS_ACTUAL_FAULT_REJECTION_PRIORITY_AND_NEW_REVIEW_PENDING",
    "payloads": {name: pin(V / name) for name in ("even_strand_markov.tex", "even_strand_markov.pdf", "even-strand-markov-verification-v3.zip", "zenodo-deposit.json")},
    "portable_members": {name: pin(V / name) for name in members}, "actual_captures": captures,
    "actual_stronger_checker": {"checks": 7114, "source_bound_left_checks": 8, "child_pid": 76825},
    "zero_shift_mutant": {"source_binding": pin(F / "tmp" / "zero_shift_v3.py"), "actual_child_pid": 78925, "actual_exit_code": 1, "failure": "primary literal unrestricted left index shift"},
    "root_personally_viewed_latest_pdf_pages": 5, "native_editor_compiler_success": True,
    "frozen_v1_v2_originals_not_replaced": True, "universal_proof_scheme_statements_unchanged": True,
    "new_independent_v3_review": "v3_wholepackage_adversary_20261004", "new_review_complete": False,
    "priority_full_source_access": "Pending human institutional portal/full-text information; official browser access reaches institution selector.",
    "publication_approval": False, "DOI": None, "tracker_row": None, "merge": None,
    "original_budget": "1/5", "new_central_proof_attempts": 0,
    "diagnostic_repair_preparation_percent": 100, "priority_resolution_estimate_percent": 60,
    "PR50_workflow_percent": 0, "completed_workflows": "3/99", "whole_goal_complete": False}
output.write_text(json.dumps(receipt, indent=2) + "\n")
progress_path = P / "CURRENT_PROGRESS.json"
progress = json.loads(progress_path.read_text())
assert progress["current_PR"] == 50 and progress["fully_completed_eligible_PRs"] == [9,16,18]
progress.update(UTC=now, remaining_current_step="Complete NEW v3 whole-package review after the source-bound diagnostic repair; resolve full Nencka primary follow-up scope/priority before any publication.",
                current_review_and_hold="audits/pr50_10600042/root_current_promotion_20261004/V3_REPAIR_BINDING_AND_PRIORITY_HOLD.json")
progress_path.write_text(json.dumps(progress, indent=2) + "\n")
readme_path = P / "README.md"
readme = readme_path.read_text()
old = "a new v2 package credits Nencka's related 1996 announcement."
assert readme.count(old) == 1
readme = readme.replace(old, "a new v3 package credits Nencka's related 1996 announcement and identified fuller texts, and adds source-bound left-exchange controls to repair a diagnostic common-mode weakness.")
readme = readme.replace("A new whole-package reviewer is checking v2 from scratch.", "A NEW whole-package reviewer is checking v3 from scratch; the genuine strengthened author run passes7,114 checks and rejects the actual zero-shift mutant.")
readme_path.write_text(readme)
append = "\n## " + now + " — source-bound diagnostic repair prepared\n\nROOT read the complete NEW v2 whole-package report/verdict. Universal theorem and exact target pass, but F01 identified an actual shared-helper shift-erasure mutant that falsely passed unchanged finite diagnostics. F02 separately retains unresolved Nencka full-source priority. ROOT preserves v2 and has added8literal primary-grounded L/BL endpoint/buffer/matrix/sign-type controls in v3, with truthful shared-helper terminology and globally synchronized current source/support/metadata/README/provenance. Genuine ROOT checker76825 passes7,114; genuine zero-shift mutant78925 exit1 is rejected at the literal primary index-shift control. New expected stdout, current execution attribution and separate genuine historical attribution are exact. Archive10members,5-pagePDF built-in/exported compilation, all5personally inspected pages and local manifest check pass. ROOT also opened the official AMS chapter in Chrome; its legitimate flow requires an institution, with none selected or credentials supplied. Human source information remains pending. A NEW v3 adversary is now reviewing from scratch. Repair preparation100%; mathematical estimate95%; priority resolution60%; currentworkflow0%; program3/99; goalunfinished. No new central attempt (original1/5), upload/DOI/tracker/merge or external-human communication.\n"
for name in ("ROOT_CURRENT_REVIEW_20261004.md", "ROOT_RESEARCH_LOG.md"):
    with (A / name).open("a") as f:
        f.write(append)
print(json.dumps({"status": receipt["status"], "UTC": now, "payloads": receipt["payloads"], "publication_approval": False}, indent=2))

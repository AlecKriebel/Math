"""Attribute the actual v3 checker run and prepare portable member checksums."""
from pathlib import Path
import datetime as dt
import hashlib
import json

F = Path(__file__).resolve().parent
A = F.parent
V = A / "publication_package_v3"
C = A.parent / "pr45_9900007"
def pin(path):
    body = path.read_bytes()
    return {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}
run_dir = C / "root_pr50_v3_checker_actual_capture"
capture = json.loads((run_dir / "CAPTURE.json").read_text())
assert capture["status"] == "PASS" and capture["exit_code"] == 0 and capture["pid"] == 76825
assert capture["actual_execution"] and capture["completed"] and capture["operator_unchanged"]
body = (run_dir / "stdout.bin").read_bytes()
assert pin(run_dir / "stdout.bin") == {"bytes": capture["stdout"]["bytes"], "sha256": capture["stdout"]["sha256"]}
assert (run_dir / "stderr.bin").read_bytes() == b""
result = json.loads(body)
assert result["status"] == "PASS_BOUNDED_DIAGNOSTICS" and result["checks"] == 7114
assert result["source_bound_left_controls"]["checks"] == 8
assert result["edge_cases"] == 316 and result["relation_context_cases"] == 1716
old_record = json.loads((A / "publication_package_v2" / "VERIFICATION_RECORD.json").read_text())
version_dir = C / "root_pr50_v3_interpreter_version_actual_capture"
version_capture = json.loads((version_dir / "CAPTURE.json").read_text())
assert version_capture["status"] == "PASS" and version_capture["exit_code"] == 0
version = (version_dir / "stdout.bin").read_text().strip()
assert version == "Python 3.9.6"
(V / "expected_results.json").write_bytes(body)
old_hash = "729d2e4d5532db6420fb9248d4b4a3aad909e0c8603e548848eccf35351d8fff"
readme = (V / "README.md").read_text()
assert readme.count("**7,106 checks**") == 1 and readme.count(old_hash) == 1
readme = readme.replace("**7,106 checks**", "**7,114 checks**").replace(old_hash, capture["stdout"]["sha256"])
readme = readme.replace("full output of the retained successful author run", "full output of the genuine strengthened-checker author run")
(V / "README.md").write_text(readme)
record = {
    "schema": "even-strand-markov-portable-verification-record/v2",
    "record_kind": "Attribution of a genuine completed strengthened-checker author run; no proof or priority certification",
    "checker": "verify_even_calculus.py", "checker_binding": pin(V / "verify_even_calculus.py"),
    "expected_result": "expected_results.json", "expected_result_binding": pin(V / "expected_results.json"),
    "actual_completed_run": {"child_pid": capture["pid"], "interpreter": version,
        "operator_interval_utc": {"started": capture["started_utc"], "finished": capture["finished_utc"], "separately_instrumented_child_timestamps": False},
        "exit_code": capture["exit_code"], "stdin_supplied": capture["stdin_supplied"], "full_stderr_bytes": 0,
        "result_status": result["status"], "checks": result["checks"], "edge_cases": result["edge_cases"],
        "relation_context_cases": result["relation_context_cases"], "source_bound_left_checks": 8},
    "manuscript_provenance": {"submission_tex_binding": pin(V / "even_strand_markov.tex"),
        "change": "Preserve universal proof and scheme statements; credit and qualify the identified fuller Nencka texts and describe source-bound left controls."},
    "historical_pre_strengthening_verification": {"package": "publication_package_v2", "record_binding": pin(A / "publication_package_v2" / "VERIFICATION_RECORD.json"),
        "checker_binding": old_record["checker_binding"], "expected_result_binding": old_record["expected_result_binding"],
        "actual_completed_run": old_record["actual_completed_run"], "not_represented_as_current_v3_execution": True},
    "diagnostic_repair": "Fixed expected nonempty L/BL words are transcribed literally from the primary formulas, without the shared shift helper. Ordered crossing countercontrols distinguish false zero-shift pairs even when component counts agree. Shared elementary helpers are not described as independent proof.",
    "limits": ["Finite diagnostics supplement the written universal proof", "Imported unrestricted Alexander/Markov theorems are not proved by this checker",
        "No braid word solver, link-equivalence oracle, historical-priority certificate, human peer review or formal proof certification",
        "The identified fuller prior sources have not been accessed; exact ordinary-closure priority remains unresolved",
        "The verification result supplies no publication, DOI or deposition assertion"],
}
(V / "VERIFICATION_RECORD.json").write_text(json.dumps(record, indent=2) + "\n")
members = ("LICENSE-CODE.txt", "LICENSE-TEXT.md", "README.md", "SHA256SUMS", "SOURCE_QUALIFICATIONS.md", "VERIFICATION_RECORD.json", "build_verification_zip.py", "even_strand_markov.tex", "expected_results.json", "verify_even_calculus.py")
(V / "SHA256SUMS").write_text("".join(pin(V / name)["sha256"] + "  " + name + "\n" for name in members if name != "SHA256SUMS"))
mutant = (V / "verify_even_calculus.py").read_text()
anchor = "def shift(w): return tuple((t, i + 1, e) for t, i, e in w)"
assert mutant.count(anchor) == 1
mutant = mutant.replace(anchor, "def shift(w): return tuple((t, i, e) for t, i, e in w)")
destination = F / "tmp" / "zero_shift_v3.py"
assert not destination.exists()
destination.write_text(mutant)
report = {"UTC": dt.datetime.now(dt.timezone.utc).isoformat(), "status": "PASS_ACTUAL_V3_RUN_ATTRIBUTION_AND_MEMBER_CHECKSUM_PREPARATION",
          "checker": record["checker_binding"], "source": record["manuscript_provenance"]["submission_tex_binding"],
          "expected": record["expected_result_binding"], "actual_checker_child_pid": capture["pid"],
          "zero_shift_mutant": pin(destination), "actual_mutant_execution_pending": True,
          "archive_visual_checks_new_review_pending": True, "priority_hold": True, "publication_approval": False,
          "repair_preparation_percent": 75, "publication_workflow_percent": 0, "whole_goal_complete": False}
(V / "ACTUAL_RUN_AND_MATERIALS.json").write_text(json.dumps(report, indent=2) + "\n")
with (V / "RESEARCH_LOG.md").open("a") as f:
    f.write("\n## " + report["UTC"] + " — actual stronger run attributed\n\nDiagnostic repair preparation75%; priority resolution60%; publication workflow0%. Genuine checker child76825 exit0 passed7114 checks,316edges,1716relationcontexts and8sourceboundleftcontrols. Exact stdout1342bytesSHA7020f461836f140681e88115a03cdc253aa26eed4bd97f4e59a797808d56b7ee copied into portable expected result; current record has genuine new execution and distinct historical attribution. A zero-shift mutant has been authored but its actual failure is not yet claimed. Archive build, final PDF visual readback and a new reviewer remain pending. No upload/DOI/tracker/merge or new central attempt.\n")
print(json.dumps(report, indent=2))

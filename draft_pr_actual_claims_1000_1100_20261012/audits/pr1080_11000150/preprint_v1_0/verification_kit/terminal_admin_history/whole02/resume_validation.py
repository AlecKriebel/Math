#!/usr/bin/env python3
"""Finish the interrupted review without replacing its completed evidence.

All candidate reads are read-only. One temporary extraction contains all new
mutations. Earlier command receipts, derivation and source records stay intact.
"""
from pathlib import Path
import collections
import datetime
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
DELIVERY = AUDIT / "preprint_v1_0"
REPO = AUDIT.parents[2]


def require(test, message):
    if not test:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check(path, row):
    require(path.is_file() and not path.is_symlink(), "nonregular " + str(path))
    data = path.read_bytes()
    require(len(data) == row["bytes"] and sha(data) == row["sha256"], "pin mismatch " + str(path))


def check_prior_review_output(row):
    path = HERE / row["path"]
    if row["path"] in ["REPORT.md", "RESEARCH_LOG.md"]:
        # Terminal completion appends to these two records only; their earlier
        # complete bytes must remain the exact original prefix on later replay.
        require(path.is_file() and not path.is_symlink(), "nonregular prior review record")
        data = path.read_bytes()
        require(len(data) >= row["bytes"] and sha(data[:row["bytes"]]) == row["sha256"], "old review record prefix changed")
    else:
        check(path, row)


def main():
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    results = {"utc": utc, "status": "PASS", "scope": "Completion of existing whole02; no new independent whole review counted."}
    baseline = json.loads((HERE / "RESUME_BASELINE.json").read_text())
    for row in baseline["existing_review_outputs"]:
        check_prior_review_output(row)
    results["completed_earlier_review_files_preserved"] = len(baseline["existing_review_outputs"])
    spec = importlib.util.spec_from_file_location("original_whole02_reproduction", HERE / "reproduce.py")
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    capture = {}
    original.save = lambda name, obj: capture.update({name: obj})
    original.history_and_archive()
    results["current_custody_and_closed_archive"] = capture["CUSTODY_AND_ARCHIVE_RESULTS.json"]
    counts = {}
    for name in ["CURRENT_INPUT_PINS.json", "PROTECTED_INPUT_PINS.json", "OUTPUT_PINS.json"]:
        inv = AUDIT / "repairs/package01_metadata_date02" / name
        data = json.loads(inv.read_text())
        base = inv.parent if name == "OUTPUT_PINS.json" else AUDIT
        for row in data["files"]:
            check(base / row["path"], row)
        counts[name] = len(data["files"])
    results["current_successor_inventory_rows"] = counts
    scope = json.loads((HERE / "SOURCE_READ_SCOPE.json").read_text())
    for row in scope["sources"] + scope["primary_page_images_actually_viewed"]:
        check(AUDIT / (row.get("local_path") or row["path"]), row)
    results["retained_primary_pdfs_rehashed"] = len(scope["sources"])
    results["retained_primary_images_rehashed"] = len(scope["primary_page_images_actually_viewed"])
    git = json.loads((HERE / "ORIGINAL_GIT_AUTHENTICATION.json").read_text())
    for row in git["files"]:
        actual = subprocess.check_output(["git", "cat-file", "blob", row["git_blob_oid"]], cwd=REPO)
        require(actual == (AUDIT / row["snapshot_path"]).read_bytes(), "actual Git blob differs")
    results["actual_original_git_blobs_reauthenticated"] = len(git["files"])
    derivation = json.loads((HERE / "DERIVATION_FREEZE.json").read_text())
    check(HERE / derivation["path"], derivation)
    prior = [json.loads(line) for line in (HERE / "REPRODUCTION_RECEIPTS.jsonl").read_text().splitlines()]
    require(len(prior) == 37 and all((r["exit_code"] == 0) == r["expected_success"] for r in prior), "prior outcome receipt")
    for row in prior:
        if row["exit_code"] != 0:
            require("RuntimeError:" in row["stderr"], "prior negative receipt not mechanism rejection")
    for label in ["normal:fault_checks.py", "optimized:fault_checks.py"]:
        data = json.loads(next(r["stdout"] for r in prior if r["label"] == label))
        require(data["status"] == "PASS" and data["count"] == 22 and all(r["detected"] for r in data["negative_controls"]), "prior built-in faults")
    for label in ["normal:output_guard_checks.py", "optimized:output_guard_checks.py"]:
        data = json.loads(next(r["stdout"] for r in prior if r["label"] == label))
        require(data["status"] == "PASS" and data["rejection_count"] == 386 and data["protected_file_count"] == 184, "prior output guards")
        require(all(r["returncode"] != 0 and r["all_protected_bytes_unchanged"] for r in data["rejections"]), "prior output guard outcomes")
    results["preserved_prior_top_level_command_receipts"] = len(prior)
    receipts = []

    def command(argv, cwd, expected=True, label=None):
        proc = subprocess.run([str(x) for x in argv], cwd=cwd, text=True, capture_output=True, timeout=180)
        rec = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "argv": [str(x) for x in argv], "cwd": str(cwd), "label": label, "exit_code": proc.returncode, "expected_success": expected, "stdout": proc.stdout, "stderr": proc.stderr}
        receipts.append(rec)
        require((proc.returncode == 0) == expected, "resumed command outcome " + str(label) + ": " + proc.stderr[-1000:])
        if not expected:
            require("RuntimeError:" in proc.stderr, "fault did not exercise runtime guard")
        return proc

    math = []
    adapters = []
    with tempfile.TemporaryDirectory(dir=HERE / "private", prefix="resume-") as temp:
        scratch = Path(temp)
        with zipfile.ZipFile(DELIVERY / "verification_kit.zip") as archive:
            archive.extractall(scratch)
        kit = scratch / "verification_kit"
        for opt in [False, True]:
            prefix = [sys.executable, "-I", "-B"] + (["-O"] if opt else [])
            command(prefix + [kit / "verify.py"], kit, label="resumed clean internal verification")
            proc = command(prefix + [kit / "run_checks.py"], kit, label="resumed preserved adapters")
            adapters.append(json.loads(proc.stdout))
            built = scratch / ("optimized.zip" if opt else "normal.zip")
            command(prefix + [kit / "build_archive.py", "--output", built], kit, label="resumed fresh deterministic rebuild")
            require(built.read_bytes() == (DELIVERY / "verification_kit.zip").read_bytes(), "resumed rebuilt archive bytes")
            command(prefix + [kit / "verify.py", "--require-binding", "--binding", DELIVERY / "EXTERNAL_BINDING.json", "--pdf", DELIVERY / "preprint.pdf", "--archive", built], kit, label="resumed strict relocated binding")
            built.unlink()
            command(prefix + [kit / "verify.py", "--require-binding"], kit, expected=False, label="resumed missing required binding")
            proc = command(prefix + [HERE / "independent_checks.py"], HERE, label="resumed independently authored math controls")
            math.append(json.loads(proc.stdout))
            for fault in ["conjugation", "erasing", "parity"]:
                command(prefix + [HERE / "independent_checks.py", fault], HERE, expected=False, label="resumed independent fault " + fault)
    require(math[0] == math[1] == json.loads((HERE / "INDEPENDENT_RESULTS.json").read_text()), "full independent result JSON differs")
    require(adapters[0] == adapters[1] == json.loads(next(r["stdout"] for r in prior if r["label"] == "normal:run_checks.py")), "full adapter result JSON differs")
    proc = command([sys.executable, "-I", "-B", REPO / "zenodo_deposit_tool/zenodo.py", "check", DELIVERY / "deposit_metadata.json"], REPO, label="resumed actual entirely local native uploader check")
    native = json.loads(proc.stdout)
    require([r["sha256"] for r in native["files"]] == [sha((DELIVERY / "preprint.pdf").read_bytes()), sha((DELIVERY / "verification_kit.zip").read_bytes())], "native exact attachments")
    results["resumed_actual_commands"] = len(receipts)
    results["resumed_expected_runtime_rejections"] = sum(r["exit_code"] != 0 for r in receipts)
    results["full_normal_optimized_math_json_equal_original"] = True
    results["full_normal_optimized_adapter_json_equal_original"] = True
    visual = json.loads((HERE / "VISUAL_QA.json").read_text())
    compiled_pin = json.loads((HERE / "CLEAN_COMPILE_PINS.json").read_text())
    check(HERE / "private/clean_compiled.pdf", {"bytes": compiled_pin["bytes"], "sha256": compiled_pin["pdf_sha256"]})
    page_receipts = []
    for row in visual["pages"]:
        retained = HERE / row["delivered_render_path"]
        require(retained.stat().st_size == row["bytes"] and sha(retained.read_bytes()) == row["delivered_render_sha256"], "retained actual page image")
        page = str(row["page"])
        command_args = ["pdftoppm", "-f", page, "-singlefile", "-r", "115", "-png"]
        canonical = subprocess.check_output(command_args + [str(DELIVERY / "preprint.pdf")])
        compiled = subprocess.check_output(command_args + [str(HERE / "private/clean_compiled.pdf")])
        require(canonical == compiled == retained.read_bytes(), "retained clean/canonical page render differs")
        page_receipts.append({"page": row["page"], "retained_path": row["delivered_render_path"], "bytes": len(canonical), "sha256": sha(canonical), "canonical_rerender_byte_equal": True, "retained_real_clean_compilation_rerender_byte_equal": True, "actually_viewed_on_resumption": True, "visual_findings": []})
    results["canonical_and_retained_real_compile_pages"] = page_receipts
    results["new_compilation_performed_on_resumption"] = False
    results["source_interfaces_directly_reread_on_resumption"] = {"CT_v3": "complete PDF pp19-21", "Smith_v1": "complete PDF pp9-12", "HKM_v1": "complete PDF pp2-4"}
    capture.clear()
    original.history_and_archive()
    for row in baseline["existing_review_outputs"]:
        check_prior_review_output(row)
    results["all_candidate_inputs_unchanged_and_prior_review_content_preserved"] = True
    results["report_and_log_may_have_additive_completion"] = True
    (HERE / "RESUME_REPRODUCTION_RECEIPTS.jsonl").write_text("".join(json.dumps(r) + "\n" for r in receipts))
    (HERE / "RESUME_VALIDATION_RESULTS.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({k: v for k, v in results.items() if k not in ["canonical_and_retained_real_compile_pages", "current_custody_and_closed_archive"]}, indent=2))


if __name__ == "__main__":
    main()

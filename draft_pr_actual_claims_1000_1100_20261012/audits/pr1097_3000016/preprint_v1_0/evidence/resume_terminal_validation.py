#!/usr/bin/env python3
"""Read-only revalidation after the original preparation worker handle ended.

Writes only its own new receipt. It does not regenerate or modify the package.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import datetime
import hashlib
import io
import json
import subprocess
import zipfile

P = Path(__file__).resolve().parent.parent
R = P.parent
K = P / "kit"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def pin(path):
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def main():
    prior = json.loads((P / "INPUT_PINS.json").read_text())
    for row in prior["entries"]:
        need(pin(R / row["path"]) == {k: row[k] for k in ("bytes", "sha256")},
             "captured original changed: " + row["path"])
    custody = json.loads((K / "provenance/CUSTODY.json").read_text())["entries"]
    need(len(custody) == 165 and len(prior["entries"]) == 165, "baseline count")
    decisions = {row["original_path"]: row for row in custody}
    need(len(decisions) == len(custody) and set(decisions) == {r["path"] for r in prior["entries"]},
         "complete individual custody coverage")
    copies = 0
    for before in prior["entries"]:
        row = decisions[before["path"]]
        need({k: row[k] for k in ("bytes", "sha256")} ==
             {k: before[k] for k in ("bytes", "sha256")}, "custody pin")
        if row["decision"] == "EXACT_AUTHORED_COPY":
            need(pin(K / row["copy_path"]) == {k: row[k] for k in ("bytes", "sha256")}, "exact custody copy")
            copies += 1
        else:
            need(row["decision"] == "EXCLUDED" and row.get("reason"), "individual omission reason")
    need(copies == 83, "exact copy count")

    names = sorted(q.relative_to(K).as_posix() for q in K.rglob("*") if q.is_file())
    raw = (P / "pr1097_support_v1_0.zip").read_bytes()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        need(archive.namelist() == names and archive.testzip() is None and not archive.comment, "ZIP inventory/CRC")
        for info in archive.infolist():
            need(archive.read(info.filename) == (K / info.filename).read_bytes(), "ZIP payload")
            need(info.date_time == (1980, 1, 1, 0, 0, 0) and info.compress_type == zipfile.ZIP_STORED,
                 "ZIP storage/time")
            need(info.create_system == 3 and info.external_attr == 0o100644 << 16 and not info.extra and not info.comment,
                 "ZIP mode/comment/extra")
    independent = io.BytesIO()
    with zipfile.ZipFile(independent, "w", compression=zipfile.ZIP_STORED) as archive:
        for name in names:
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (K / name).read_bytes())
    need(independent.getvalue() == raw, "independent closed ZIP")

    expected = json.loads((K / "EXPECTED_RESULTS.json").read_text())
    commands = []
    results = {}
    for optimized in (False, True):
        mode = "optimized" if optimized else "normal"
        prefix = [sys.executable] + (["-O", "-B"] if optimized else ["-B"])
        for script, args, good in (("verify.py", ["--require-binding"], True),
                                   ("run_checks.py", [], True),
                                   ("run_checks.py", ["--inject-failure"], False)):
            cmd = prefix + [str(K / "scripts" / script)] + args
            run = subprocess.run(cmd, cwd=K, capture_output=True, check=False)
            need((run.returncode == 0) == good, "resumption command exit: " + repr(cmd))
            commands.append({"mode": mode, "command": cmd, "exit": run.returncode,
                             "stdout_sha256": hashlib.sha256(run.stdout).hexdigest(),
                             "stderr_sha256": hashlib.sha256(run.stderr).hexdigest()})
            if script == "run_checks.py" and good:
                results[mode] = json.loads(run.stdout)
                need(results[mode] == expected, "complete fresh mathematical control JSON")
                need(results[mode] == json.loads((P / "evidence" / ("CHECK_" + mode.upper() + ".json")).read_text()),
                     "retained exact control result")
            if script == "verify.py":
                need(json.loads(run.stdout)["binding"]["state"] == "PRESENT_VERIFIED", "strict binding")
    need(results["normal"] == results["optimized"], "full normal/optimized JSON equality")
    native_cmd = [sys.executable, "-B", str(R.parents[2] / "zenodo_deposit_tool/zenodo.py"),
                  "check", str(P / "zenodo-deposit.json")]
    native = subprocess.run(native_cmd, cwd=R.parents[2], capture_output=True, check=False)
    need(native.returncode == 0, "local native uploader check")
    commands.append({"mode": "local_only", "command": native_cmd, "exit": native.returncode,
                     "stdout_sha256": hashlib.sha256(native.stdout).hexdigest(),
                     "stderr_sha256": hashlib.sha256(native.stderr).hexdigest()})
    previous = json.loads((P / "evidence/COMMAND_RECEIPTS.json").read_text())["entries"]
    need(len(previous) == 73 and sum(r["exit"] != 0 for r in previous) == 54, "original completed command receipt totals")
    need(json.loads((P / "evidence/FINAL_VERIFICATION.json").read_text())["status"] == "PASS", "original terminal validation")
    for row in prior["entries"]:
        need(pin(R / row["path"]) == {k: row[k] for k in ("bytes", "sha256")}, "post-validation original unchanged")
    result = {
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": "PASS",
        "reason": "Original worker handle missing, but authoritative retained receipts prove its 73-command validation completed. Finish missing terminal inventory/seal without restarting preparation.",
        "prior_actual_commands": 73, "prior_expected_rejections": 54,
        "resumption_actual_commands": len(commands), "commands": commands,
        "baseline_files_unchanged": 165, "exact_authored_copies": copies, "individual_exclusions": 82,
        "ZIP_members": len(names), "independent_closed_ZIP_byte_equal": True,
        "complete_control_JSON_normal_optimized_equal": True,
        "actual_local_native_check_passed": True,
        "paper": pin(P / "paper.pdf"), "source": pin(P / "paper.tex"),
        "archive": pin(P / "pr1097_support_v1_0.zip"),
        "canonical_package_modified": False, "repeated_compilation_or_rendering": False,
        "git_or_external_service_actions": False,
        "fresh_whole_package_reviews_of_new_edition": 0,
        "minimum_fresh_whole_package_reviews_required": 2,
        "publication_ready": False, "ordered_service_hold_pr": 1032,
    }
    (P / "evidence/RESUMPTION_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "commands"}, sort_keys=True))


if __name__ == "__main__":
    main()

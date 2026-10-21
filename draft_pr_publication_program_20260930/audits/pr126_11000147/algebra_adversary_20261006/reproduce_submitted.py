"""Replay immutable submitted verifiers in own isolated copies only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parent / "original_head_authentication_20261006" / "original_attempt"
PY = "/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14"

def require(value, why):
    if not value:
        raise RuntimeError(why)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def hashes():
    return {str(p.relative_to(ORIGINAL)): digest(p) for p in ORIGINAL.rglob("*") if p.is_file()}

before = hashes()
require(len(before) == 16, "all16 original artifacts required")
records = []
for kind in ("author", "independent", "independent_explicit_guard_repair"):
    for optimized in (False, True):
        for corrupted in (False, True):
            name = kind + ("_optimized" if optimized else "_normal") + ("_corrupted" if corrupted else "_valid")
            work = HERE / "isolated_reproduction" / name
            work.mkdir(parents=True, exist_ok=True)
            if kind == "author":
                source = ORIGINAL / "verify.py"
                destination = work / "verify.py"
                shutil.copy2(ORIGINAL / "CANDIDATE.md", work / "CANDIDATE.md")
                expected = ORIGINAL / "verification.json"
                receipt = work / "verification.json"
                token = "C = ((8, -11), (3, -4))"
                replacement = "C = ((8, -11), (4, -4))"
            else:
                source = ORIGINAL / "review" / "independent_checks.py"
                destination = work / "independent_checks.py"
                (work / "author_replay").mkdir(exist_ok=True)
                shutil.copy2(ORIGINAL / "review" / "author_replay" / "CANDIDATE.md", work / "author_replay" / "CANDIDATE.md")
                expected = ORIGINAL / "review" / "independent_checks.json"
                receipt = work / "independent_checks.json"
                token = "C=((8,-11),(3,-4))"
                replacement = "C=((8,-11),(4,-4))"
            source_text = source.read_text()
            if kind == "independent_explicit_guard_repair":
                require(source_text.count("    assert p,cat") == 1, "one narrow guard replacement")
                source_text = source_text.replace("    assert p,cat", "    if not p:\n        raise AssertionError(cat)")
            if corrupted:
                require(source_text.count(token) == 1, "one matrix corruption only")
                source_text = source_text.replace(token, replacement)
            destination.write_text(source_text)
            if receipt.exists():
                receipt.unlink()
            command = [PY, "-E", "-S", "-B", "-P"] + (["-O"] if optimized else []) + [str(destination)]
            result = subprocess.run(command, cwd=work, capture_output=True, timeout=60)
            (work / "stdout.txt").write_bytes(result.stdout)
            (work / "stderr.txt").write_bytes(result.stderr)
            receipt_written = receipt.is_file()
            record = {"case": name, "command": command, "returncode": result.returncode,
                      "copied_verifier_sha256": digest(destination),
                      "candidate_sha256": digest(work / ("CANDIDATE.md" if kind == "author" else "author_replay/CANDIDATE.md")),
                      "receipt_written": receipt_written,
                      "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
                      "stderr_sha256": hashlib.sha256(result.stderr).hexdigest()}
            if receipt_written:
                record["receipt_sha256"] = digest(receipt)
                record["submitted_receipt_byte_identical"] = receipt.read_bytes() == expected.read_bytes()
                record["stdout_parsed_equals_generated_receipt"] = json.loads(result.stdout) == json.loads(receipt.read_bytes())
                record["stdout_byte_identical_submitted_receipt"] = result.stdout == expected.read_bytes()
                record["control_count"] = json.loads(receipt.read_bytes()).get("total_assertions", json.loads(receipt.read_bytes()).get("exact_assertions"))
            if not corrupted:
                require(result.returncode == 0 and receipt_written, name + " clean replay must succeed")
                require(record["submitted_receipt_byte_identical"], name + " submitted receipt must reproduce")
                require(record["stdout_parsed_equals_generated_receipt"], name + " stdout and receipt must agree")
            elif kind == "independent" and optimized:
                require(result.returncode == 0 and receipt_written, "documented optimized-assert false positive expected")
                require(record["control_count"] == 3156, "optimized counter remains3156 despite false matrix")
            else:
                require(result.returncode != 0 and not receipt_written, name + " corruption must be rejected")
                require(b"AssertionError" in result.stderr, name + " rejection must be assertion failure")
            records.append(record)
after = hashes()
require(before == after, "immutable originals must remain unchanged")
out = {"schema": "pr126-truthful-submitted-reproduction-and-guard-diagnostics/v1",
       "UTC": datetime.now(timezone.utc).isoformat(), "actual_operator_PID": os.getpid(),
       "interpreter": PY, "interpreter_version": sys.version,
       "PASS": True, "original_head": "a1df84a64fa96d53f3a8c6fec9db8bc48bd1533c",
       "original16_hashes_before_after_equal": before == after, "original16_hashes": before,
       "cases": records,
       "interpretation": "Normal-mode submitted receipts reproduce exactly: author311 and independent3156. A single C(2,1) perturbation is rejected in normal mode by both. The author's explicit check survives -O (inv's auxiliary assert does not); the original independent verifier's ck predicates are erased by -O and falsely retain3156 controls for corrupted C. A narrow explicit guard replacement in an isolated copy preserves normal receipts and rejects corruption under both modes. This computational robustness issue does not refute the valid written theorem. Original artifact bytes have not been changed.",
       "original_budget": "1/5", "new_central_proof_search_turns": 0}
(HERE / "submitted_reproduction_result.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps({"PASS": True, "UTC": out["UTC"], "PID": os.getpid(), "case_count": len(records), "normal_receipts_exact": True, "optimized_independent_corruption_false_positive": True}))

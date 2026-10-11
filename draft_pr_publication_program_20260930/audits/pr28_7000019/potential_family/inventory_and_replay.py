#!/usr/bin/env python3
"""Read-only original inventory; all foreign executable copies run under ignored tmp."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = HERE.parents[3]
HEAD = "90a81313f3f65a7914fb6d5a9950fa087ea7467e"
BASE = "c6975ca76f9f667f1250ba403d0e6da2aafe14d0"
PREFIX = "unsolved_math_prioritization/attempts/7000019/"
manifest = json.loads((AUDIT / "snapshot_manifest.json").read_text())

def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO)

files = []
for entry in manifest["files"]:
    raw = (AUDIT / "source_snapshot" / entry["path"]).read_bytes()
    head_raw = git("show", HEAD + ":" + PREFIX + entry["path"])
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    digest = hashlib.sha256(raw).hexdigest()
    record = {
        "path": entry["path"], "bytes": len(raw), "sha256": digest,
        "git_blob_sha1": blob, "snapshot_matches_exact_git_head": raw == head_raw,
        "manifest_length_matches": len(raw) == entry["bytes"],
        "manifest_sha256_matches": digest == entry["sha256"],
        "manifest_git_blob_matches": blob == entry["git_blob_sha1"],
    }
    assert all(record[k] for k in record if k.endswith("matches") or k == "snapshot_matches_exact_git_head")
    files.append(record)
assert len(files) == 17
changed = git("diff", "--name-only", BASE, HEAD).decode().splitlines()
assert changed == manifest["changed_paths"] and len(changed) == 18
queue_path = "unsolved_math_prioritization/QUEUE.md"
queue_rows = {}
for ref in (BASE, HEAD):
    data = git("show", ref + ":" + queue_path).decode()
    rows = [line for line in data.splitlines() if "7000019 / AMR-069-0019" in line]
    assert len(rows) == 1
    queue_rows[ref] = rows[0]
assert "| queued | 0/5 |" in queue_rows[BASE]
assert "| unsolved | 2/5 |" in queue_rows[HEAD]
attempt = json.loads((AUDIT / "source_snapshot/attempt.json").read_text())
log = (AUDIT / "source_snapshot/RESEARCH_LOG.md").read_text()
assert attempt["substantive_attempts_used"] == 2
assert attempt["substantive_attempt_limit"] == 5
assert "substantive attempt 1/5" in log and "substantive attempt 2/5" in log
assert not attempt["full_resolution_claimed"]
inventory = {
    "utc": datetime.now(timezone.utc).isoformat(), "head": HEAD, "base": BASE,
    "early_reconstruction_sha256": hashlib.sha256((HERE / "EARLY_INDEPENDENT_RECONSTRUCTION.md").read_bytes()).hexdigest(),
    "original_files_verified": len(files), "changed_paths_including_QUEUE": len(changed),
    "files": files, "changed_paths": changed, "queue_rows": queue_rows,
    "budget": {"used": 2, "limit": 5, "ledger_consistent": True,
               "limitation": "This verifies the frozen ledger and log, not unobservable historical model turns."},
}
(HERE / "inventory_receipts.json").write_text(json.dumps(inventory, indent=2) + "\n")

isolation = HERE / "tmp/frozen_replay"
if isolation.exists():
    shutil.rmtree(isolation)
shutil.copytree(AUDIT / "source_snapshot", isolation)
replays = []
for relative in ("verify.py", "review/submitted_verify.py", "review/independent_checks.py"):
    path = isolation / relative
    source_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    completed = subprocess.run([sys.executable, str(path)], cwd=path.parent,
                               capture_output=True, text=True)
    rec = {"path": relative, "sha256": source_digest, "returncode": completed.returncode,
           "stdout": completed.stdout, "stderr": completed.stderr}
    assert completed.returncode == 0
    if relative.endswith("independent_checks.py"):
        result = json.loads(path.with_name("independent_results.json").read_text())
        frozen = json.loads((AUDIT / "source_snapshot/review/independent_results.json").read_text())
        assert result == frozen
        rec["replayed_assertions"] = result["passed"]
        rec["receipt_identical_to_original"] = True
    else:
        result = json.loads(completed.stdout)
        frozen = json.loads((AUDIT / "source_snapshot/verification.json").read_text())
        assert result == frozen
        rec["replayed_assertions"] = result["total_assertions"]
        rec["receipt_identical_to_original"] = True
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source_digest
    replays.append(rec)

# These deliberate proof mutations demonstrate that the old verifier does not
# read PROOF.md. It is a control script, not a proof integrity or proof certificate.
proof = (isolation / "PROOF.md").read_text()
mutations = {
    "drop_full_width_factor_2": (r"U(x)=\frac{C}{a}=\frac{2C}{h}", r"U(x)=\frac{C}{a}=\frac{C}{h}"),
    "drop_strict_core_guard": (r"h<2r_{\rm in}(K)", r"h<\operatorname{diam}(K)"),
    "replace_open_continuation_set_with_point": ("nonempty open set E", "a single point of E"),
    "omit_constant_density_hypothesis": ("the density in (2.3) is identically one", "the density in (2.3) is any positive function"),
}
mutant_receipts = []
for name, (old, new) in mutations.items():
    assert old in proof
    mutant_dir = HERE / "tmp/proof_mutants" / name
    mutant_dir.mkdir(parents=True, exist_ok=True)
    mutant_text = proof.replace(old, new, 1)
    (mutant_dir / "PROOF.md").write_text(mutant_text)
    shutil.copyfile(isolation / "verify.py", mutant_dir / "verify.py")
    completed = subprocess.run([sys.executable, str(mutant_dir / "verify.py")],
                               cwd=mutant_dir, capture_output=True, text=True)
    assert completed.returncode == 0
    result = json.loads(completed.stdout)
    mutant_receipts.append({"name": name,
        "mutant_proof_sha256": hashlib.sha256(mutant_text.encode()).hexdigest(),
        "old_verifier_returncode": completed.returncode,
        "old_verifier_assertions_passed": result["total_assertions"],
        "interpretation": "Deliberately false/unsupported proof alteration is invisible to the old arithmetic verifier."})

(HERE / "replay_receipts.json").write_text(json.dumps({
    "utc": datetime.now(timezone.utc).isoformat(), "interpreter": sys.executable,
    "python": sys.version, "isolation_under_git_ignored_tmp": True,
    "replays": replays, "deliberate_proof_mutants": mutant_receipts,
    "scope": "Replay and limitation demonstration; no finite check certifies analytic rigidity."
}, indent=2) + "\n")
print("Verified exact original17, changed18, ledger2/5; replayed1056+1056+266; four proof mutants remain invisible to old verifier.")

"""Read-only reviewed-source authentication and isolated finite-check replay.

Reviewed code and receipts are never overwritten. This is source/evidence
authentication plus finite falsification probes, not a Lean kernel build or
a proof of the infinite-dimensional theorem.
"""
from contextlib import redirect_stdout
from datetime import datetime, timezone
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def authenticate(entries):
    checked, mismatches = [], []
    for entry in entries:
        path = ROOT / entry["path"]
        actual = digest(path)
        row = {"path": entry["path"], "sha256": actual}
        checked.append(row)
        if actual != entry["sha256"]:
            mismatches.append(row)
    return {"checked": len(checked), "mismatches": mismatches, "files": checked}


review_manifest = json.loads((ROOT / "reviews/versions/draft_v2/review_manifest.json").read_text())
pinned_manifest = json.loads((ROOT / "receipts/pinned_sources.json").read_text())
priority_hashes = json.loads((ROOT / "receipts/priority_source_hashes.json").read_text())
lean_manifest = json.loads((ROOT / "research/lean_audit/import_closure.json").read_text())
lean_mismatches = []
for entry in lean_manifest["sources"]:
    original = Path(entry["path"])
    copied = ROOT / "research/lean_audit/build" / Path(*entry["module"].split(".")).with_suffix(".lean")
    original_hash, copied_hash = digest(original), digest(copied)
    if original_hash != entry["sha256"] or copied_hash != entry["sha256"]:
        lean_mismatches.append({"module": entry["module"], "original": original_hash, "copied": copied_hash})

replays = []
for stem, suffix in [("cohomology_adversary_checks", "cohomology"), ("draft_whole_review_1_checks", "noncommutative")]:
    original = ROOT / "research" / (stem + ".py")
    isolated_name = ROOT / "research" / ("revised_checkpoint_review_" + suffix + "_probe.py")
    output = isolated_name.with_suffix(".json")
    namespace = {"__name__": "__main__", "__file__": str(isolated_name)}
    buffer = StringIO()
    executable = original.read_text()
    if stem == "cohomology_adversary_checks":
        # Its output basename is fixed rather than derived from __file__.
        # Redirect only that basename; preserve the entire check algorithm.
        assert executable.count('"cohomology_adversary_checks.json"') == 1
        executable = executable.replace('"cohomology_adversary_checks.json"', repr(output.name))
    with redirect_stdout(buffer):
        exec(compile(executable, str(original), "exec"), namespace)
    original_result = json.loads(original.with_suffix(".json").read_text())
    replay_result = json.loads(output.read_text())
    replays.append({"source": str(original.relative_to(ROOT)), "source_sha256": digest(original),
                    "output": str(output.relative_to(ROOT)), "receipt_exact_match": original_result == replay_result,
                    "stdout": buffer.getvalue().strip()})

result = {
    "utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Source authentication and isolated exact finite replays only; no kernel build or full theorem proof.",
    "v2_manifest": authenticate(review_manifest["files"]),
    "pinned_source_manifest": authenticate(pinned_manifest["files"]),
    "priority_pdf_hashes": authenticate([{"path": path, "sha256": hash_} for path, hash_ in priority_hashes.items()]),
    "lean_original_and_copied_sources": {"checked": len(lean_manifest["sources"]), "mismatches": lean_mismatches, "kernel_build": False},
    "isolated_finite_replays": replays,
}
target = ROOT / "research/revised_checkpoint_review_checks.json"
target.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"output": str(target), "v2_mismatches": result["v2_manifest"]["mismatches"],
                  "pinned_mismatches": result["pinned_source_manifest"]["mismatches"],
                  "priority_mismatches": result["priority_pdf_hashes"]["mismatches"],
                  "lean_mismatches": lean_mismatches,
                  "finite_replays_match": all(x["receipt_exact_match"] for x in replays)}, indent=2))

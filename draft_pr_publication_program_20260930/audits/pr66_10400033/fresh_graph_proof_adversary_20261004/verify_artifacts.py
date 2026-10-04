#!/usr/bin/env python3
"""Verify existing audit receipts and save a non-self-referential inventory."""
from pathlib import Path
import datetime
import hashlib
import json


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


root = Path(__file__).resolve().parent
first_receipt = json.loads((root / "FIRST_CONCLUSION.receipt.json").read_text())
assert digest(root / "FIRST_CONCLUSION.md") == first_receipt["sha256"]
assert (root / "FIRST_CONCLUSION.md").stat().st_size == first_receipt["bytes"]
for name in ["restricted_input_read", "graph_diagnostics"]:
    receipt = json.loads((root / (name + ".receipt.json")).read_text())
    assert receipt["exit_code"] == 0
    assert receipt["cwd"] == str(root)
    assert isinstance(receipt["pid"], int) and receipt["pid"] > 0
    for stream in ["stdout", "stderr"]:
        path = root / receipt[stream + "_file"]
        assert path.stat().st_size == receipt[stream + "_bytes"]
        assert digest(path) == receipt[stream + "_sha256"]
diagnostics = json.loads((root / "graph_diagnostics.stdout").read_text())
assert diagnostics["status"] == "PASS"
assert digest(root / "graph_diagnostics.py") == diagnostics["source_sha256"]
sizes = diagnostics["formal_chord_checks"]["sizes"]
totals = {
    "chord_words": sum(row["rooted_unlabeled_chord_words"] for row in sizes),
    "sign_assignments": sum(row["sign_assignments_checked"] for row in sizes),
    "chord_graph_completions": sum(row["completion_tournaments_checked"] for row in sizes),
    "tournaments": sum(row["tournaments_checked"] for row in diagnostics["tournament_checks"]),
}
assert totals == {"chord_words": 1815, "sign_assignments": 27893,
                  "chord_graph_completions": 39775, "tournaments": 33868}
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (root / "RESEARCH_LOG.md").open("a") as handle:
    handle.write(f"- {now}: Independent exact diagnostics passed; universal conditional graph verdict unchanged. All n≤4 directed chord words/signs/completions and n≤6 tournaments checked. Assigned graph-audit completion estimate: 95%; final receipts/inventory verification underway.\n")
    handle.write(f"- {now}: Adversarial report completed and retained. Assigned graph-audit completion estimate: 100%. Primary imported knot bridge remains external and pending. No original or external opinion/code inspected at any point.\n")
excluded = {"MANIFEST.json", "MANIFEST.sha256", "verify_artifacts.stdout",
            "verify_artifacts.stderr", "verify_artifacts.receipt.json"}
files = [{"path": p.name, "bytes": p.stat().st_size, "sha256": digest(p)}
         for p in sorted(root.iterdir()) if p.is_file() and p.name not in excluded]
manifest = {
    "created_utc": now,
    "verdict": "CONDITIONAL_GRAPH_ARGUMENT_VALID",
    "assigned_graph_audit_completion_percent": 100,
    "first_conclusion_sha256": first_receipt["sha256"],
    "files": files,
    "excluded_from_manifest": sorted(excluded),
    "excluded_reason": "Inventory and final verification receipt are excluded to avoid cyclic/self hashes; final verification receipt separately binds its stdout/stderr.",
    "diagnostic_totals": totals,
    "original_or_other_graph_opinion_inspected": False,
}
(root / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
manifest_hash = digest(root / "MANIFEST.json")
(root / "MANIFEST.sha256").write_text(manifest_hash + "  MANIFEST.json\n")
print(json.dumps({"status": "PASS", "verified_first_conclusion_sha256": first_receipt["sha256"],
                  "manifest_sha256": manifest_hash, "totals": totals,
                  "inventoried_files": len(files), "audit_completion_percent": 100}, indent=2))

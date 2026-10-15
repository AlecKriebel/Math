"""Local document-history checks only; no mathematical verification."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

audit_root = Path(__file__).resolve().parents[3]
candidate = audit_root / "reviewed_candidate"
snapshot = audit_root / "source_snapshot"

current_files = [
    "PROOF.md", "SOURCE_AUDIT.md", "PRIORITY_AUDIT.md", "README.md",
    "attempt_status.json", "pr_draft.md", "source_provenance.json",
    "source_record.json", "RESEARCH_LOG.md", "review_request.md", "attempt.json",
]
history_files = ["source_record.json", "source_provenance.json"] + [
    str(p.relative_to(snapshot))
    for p in sorted((snapshot / "review").rglob("*")) if p.is_file()
]

def sha(data):
    return hashlib.sha256(data).hexdigest()

checks = []
for rel in history_files:
    old, new = (snapshot / rel).read_bytes(), (candidate / rel).read_bytes()
    checks.append({"file": rel, "relation": "identical", "passed": new == old,
                   "snapshot_sha256": sha(old), "candidate_sha256": sha(new)})
for rel in ["SOURCE_AUDIT.md", "RESEARCH_LOG.md"]:
    old, new = (snapshot / rel).read_bytes(), (candidate / rel).read_bytes()
    checks.append({"file": rel, "relation": "original is prefix", "passed": new.startswith(old),
                   "snapshot_sha256": sha(old), "candidate_sha256": sha(new)})
old, new = (snapshot / "review_request.md").read_bytes(), (candidate / "review_request.md").read_bytes()
checks.append({"file": "review_request.md", "relation": "original is suffix", "passed": new.endswith(old),
               "snapshot_sha256": sha(old), "candidate_sha256": sha(new)})

result = {
    "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "document claims and historical preservation only; no mathematical correctness or source validity audit",
    "candidate": str(candidate),
    "candidate_sha256": {rel: sha((candidate / rel).read_bytes()) for rel in current_files},
    "checks": checks,
    "all_preservation_checks_passed": all(c["passed"] for c in checks),
}
Path(__file__).with_name("preservation_checks.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"all_preservation_checks_passed": result["all_preservation_checks_passed"],
                  "checks": len(checks), "checked_at_utc": result["checked_at_utc"]}, indent=2))

"""Explicit audit whitelist: no recursive publication or implied permission."""
from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parent
public_paths = [
    "SOURCE_CONTRACT.md", "INDEPENDENT_DERIVATION.md", "FROZEN_ANALYTIC_VERDICT.md",
    "REPORT.md", "DECISION.json", "RESEARCH_LOG.md", "independent_finite_checks.py",
    "independent_completion_checks.py", "FINITE_CHECK_RESULTS.json",
    "FINITE_CHECK_RESULTS_OPTIMIZED.json", "COMPLETION_CHECK_RESULTS.json",
    "EXECUTION_SUMMARY.json", "build_public_manifest.py",
]
entries = []
for name in public_paths:
    if Path(name).name != name:
        raise RuntimeError("Manifest paths must be explicit safe basenames")
    path = base / name
    if path.is_symlink() or not path.is_file():
        raise RuntimeError("Manifest requires regular authored files")
    body = path.read_bytes()
    if path.suffix == ".json":
        json.loads(body)
    entries.append({"path": name, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
by_name = {entry["path"]: entry for entry in entries}
summary = json.loads((base / "EXECUTION_SUMMARY.json").read_bytes())
for checker in summary["checkers"]:
    if by_name[checker["path"]]["sha256"] != checker["checker_sha256"]:
        raise RuntimeError("Checker authentication mismatch")
    if by_name[checker["stdout_path"]]["sha256"] != checker["stdout_sha256_both"]:
        raise RuntimeError("Saved stdout authentication mismatch")
if (base / "FINITE_CHECK_RESULTS.json").read_bytes() != (base / "FINITE_CHECK_RESULTS_OPTIMIZED.json").read_bytes():
    raise RuntimeError("Optimized finite stdout differs")
private_receipts = json.loads((base / "PRIVATE_EXECUTION_RECEIPTS.json").read_bytes())
for run in private_receipts["runs"]:
    if run["cmd"] in {"python3 -I -S -B independent_completion_checks.py",
                      "python3 -I -S -B -O independent_completion_checks.py"}:
        if run["completion"]["output"].encode("utf-8") != (base / "COMPLETION_CHECK_RESULTS.json").read_bytes():
            raise RuntimeError("Captured completion stdout differs from saved bytes")
manifest = {
    "scope": "Explicit authored relative paths only; no recursive permission or publication authorization",
    "excluded": "Primary source bodies, original corpus and audits, renders, credentials, private receipts, and machine-specific paths",
    "self_hash_policy": "This manifest excludes itself to avoid recursive hashing",
    "files": entries,
}
(base / "PUBLIC_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"public_files": len(entries), "public_bytes": sum(e["bytes"] for e in entries)}))

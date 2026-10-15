#!/usr/bin/env python3
"""Check actual frozen receipt/manifest bytes with optimization-safe failures."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
ROOT = CASE / "source_snapshot"
PAYLOAD = ROOT / "unsolved_math_prioritization/attempts/2569"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_rows(root, rows):
    out = []
    for binding in rows:
        relative = Path(binding["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("Unsafe binding path")
        data = (root / relative).read_bytes()
        checked = {"path": str(relative), "actual_bytes": len(data),
                   "actual_sha256": sha(data),
                   "matches": len(data) == binding["bytes"] and sha(data) == binding["sha256"]}
        out.append(checked)
    return out


def main():
    receipt = json.loads((CASE / "SOURCE_RECEIPT.json").read_text())
    manifest = json.loads((PAYLOAD / "MANIFEST.json").read_text())
    root_bindings = check_rows(ROOT, receipt["files"])
    historical_bindings = check_rows(PAYLOAD, manifest["files"])
    extant = {str(p.relative_to(PAYLOAD)) for p in PAYLOAD.rglob("*") if p.is_file()}
    declared = {row["path"] for row in manifest["files"]}
    receipt_paths = {row["path"] for row in receipt["files"]}
    payload_prefix = "unsolved_math_prioritization/attempts/2569/"
    expected_receipt_paths = {payload_prefix + p for p in extant}
    scripts = []
    for script in sorted(PAYLOAD.rglob("*.py")):
        tree = ast.parse(script.read_text())
        statements = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
        scripts.append({"path": str(script.relative_to(PAYLOAD)),
                        "source_assert_statements": len(statements),
                        "assert_lines": sorted(node.lineno for node in statements),
                        "random_imports": [n.name for n in ast.walk(tree)
                                           if isinstance(n, ast.alias) and n.name in ("random", "numpy.random")],
                        "embedded_private_path_literals": [n.value for n in ast.walk(tree)
                                                           if isinstance(n, ast.Constant) and isinstance(n.value, str)
                                                           and any(t in n.value for t in ("/Users/", "/tmp/", "private_sources/"))]})
    success = (len(root_bindings) == 26 and len(historical_bindings) == 25
               and all(r["matches"] for r in root_bindings + historical_bindings)
               and extant == declared | {"MANIFEST.json"}
               and receipt_paths == expected_receipt_paths)
    result = {"checked_utc": datetime.now(timezone.utc).isoformat(),
              "head_sha": receipt["head_sha"], "root_receipt_sha256": sha((CASE / "SOURCE_RECEIPT.json").read_bytes()),
              "root_bindings": root_bindings, "historical_manifest_bindings": historical_bindings,
              "historical_manifest_self_excluded": "MANIFEST.json" not in declared,
              "manifest_externally_bound_by_root_receipt": payload_prefix + "MANIFEST.json" in receipt_paths,
              "unexpected_payload_paths": sorted(extant - declared - {"MANIFEST.json"}),
              "receipt_exactly_covers_extant_payload": receipt_paths == expected_receipt_paths,
              "script_inventory": scripts, "all_integrity_checks_passed": success}
    (HERE / "INTEGRITY_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"root_bindings": len(root_bindings), "historical_manifest_bindings": len(historical_bindings),
                      "source_assert_statements": sum(s["source_assert_statements"] for s in scripts),
                      "all_integrity_checks_passed": success}))
    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

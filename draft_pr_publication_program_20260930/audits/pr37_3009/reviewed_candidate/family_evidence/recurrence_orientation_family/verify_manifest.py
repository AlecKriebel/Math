#!/usr/bin/env python3
"""Verify exact authored allowlist and immutable source/proof seals."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


m = json.loads((HERE/"authored_manifest.json").read_text())
expected = set(m["authored_files"])
actual_before_receipt = {str(p.relative_to(HERE)) for p in HERE.rglob("*")
                         if p.is_file() and "tmp" not in p.relative_to(HERE).parts}
missing = expected-actual_before_receipt-{"manifest_verification.json"}
unexpected = actual_before_receipt-expected
assert not missing and not unexpected, (missing, unexpected)
seal = json.loads((HERE/"PROOF_SEAL.json").read_text())
assert sha(HERE/"SEALED_PROOF.md") == seal["proof_sha256"]
source_seal = json.loads((HERE/"SOURCE_FIRST_SEAL.json").read_text())
assert sha(ROOT/source_seal["source_path"]) == source_seal["source_sha256"]
assert sha(HERE.parent/"source_snapshot/PARTIAL.md") == "c24cf9578f26202c2af4e25d017a5e44d7047ad32e7f35ebac0604275399f00f"
p = subprocess.run(["git", "check-ignore", "-v", str(HERE/"tmp/foreign_source")],
                   cwd=ROOT, capture_output=True, text=True)
assert p.returncode == 0
replay = json.loads((HERE/"original_replay_receipts.json").read_text())
assert replay["all_expected_outcomes"]
assert all(c["structurally_equal"] for r in replay["receipts"]
           for c in r.get("saved_result_comparison", {}).values())
result = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "exact_allowlist": True, "authored_files_count": len(expected),
          "missing": sorted(missing), "unexpected": sorted(unexpected),
          "proof_seal_unchanged": True, "frozen_source_record_unchanged": True,
          "frozen_PARTIAL_unchanged": True, "tmp_is_ignored": p.stdout.strip(),
          "fresh_replays_match_saved_results": True,
          "authored_file_hashes_except_self_receipt": {
              f: sha(HERE/f) for f in sorted(expected) if f != "manifest_verification.json"}}
(HERE/"manifest_verification.json").write_text(json.dumps(result, indent=2)+"\n")
actual_after = {str(p.relative_to(HERE)) for p in HERE.rglob("*")
               if p.is_file() and "tmp" not in p.relative_to(HERE).parts}
assert actual_after == expected
print(json.dumps({k:v for k,v in result.items() if k != "authored_file_hashes_except_self_receipt"}, indent=2))

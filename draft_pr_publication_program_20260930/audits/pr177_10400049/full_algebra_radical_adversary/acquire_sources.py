#!/usr/bin/env python3
"""Acquire the exact primary PDF and record clean provenance metadata."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import os
import platform
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / "private_sources"
PRIVATE.mkdir(exist_ok=True)
URL = "https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf"
out = PRIVATE / "ohtsuki.pdf"
body = urllib.request.urlopen(URL, timeout=45).read()
if not body.startswith(b"%PDF"):
    raise RuntimeError("Acquired body is not a PDF")
out.write_bytes(body)
inputs = []
original = ROOT.parent / "original_submission/files/unsolved_math_prioritization/attempts/10400049"
for name in ("CANDIDATE.md", "source_record.json", "source_manifest.json"):
    path = original / name
    content = path.read_bytes()
    inputs.append({"path": str(path), "bytes": len(content), "sha256": sha256(content).hexdigest(),
                   "read_scope": "complete body", "submission_head": "cee82300baaa2e209aba8b62ae34673419237451"})
receipt = {
    "acquired_utc": datetime.now(timezone.utc).isoformat(),
    "primary_sources": [{"url": URL, "path": str(out.relative_to(ROOT)), "bytes": len(body),
                         "sha256": sha256(body).hexdigest(), "private_third_party_body": True,
                         "actual_coverage": "Acquired full body; reading limited to printed 398 and 422 (PDF indices 25 and 49)."}],
    "consumed_submission_inputs": inputs,
    "runtime": {"python_executable": sys.executable, "python_version": sys.version,
                "platform": platform.platform(), "optimized": sys.flags.optimize},
    "public_exact_allowlist_policy": "Exclude private_sources/ and all third-party body derivatives. Own proofs, portable code, clean receipts and notes may be public."
}
(ROOT / "source_ledger.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"status": "acquired", "bytes": len(body), "sha256": sha256(body).hexdigest()}))

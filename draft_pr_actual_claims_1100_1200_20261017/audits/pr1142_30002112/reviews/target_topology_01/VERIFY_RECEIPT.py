from pathlib import Path
import hashlib
import json
import sys

root = Path(__file__).resolve().parent
receipt_path = root / "RECEIPT.json"
receipt_bytes = receipt_path.read_bytes()
expected_receipt = (root / "RECEIPT.json.sha256").read_text().split()[0]
def digest(data):
    return hashlib.sha256(data).hexdigest()
def require(condition, message):
    if not condition:
        raise RuntimeError(message)
require(digest(receipt_bytes) == expected_receipt, "Receipt sidecar mismatch")
receipt = json.loads(receipt_bytes)
for entry in receipt["artifacts"]:
    body = (root / entry["relative_path"]).read_bytes()
    require(digest(body) == entry["sha256"], "Artifact mismatch: " + entry["relative_path"])
for entry in receipt["external_semantic_inputs"]:
    body = Path(entry["path"]).read_bytes()
    require(digest(body) == entry["sha256"], "External input mismatch: " + entry["path"])
require(digest(receipt_bytes + b"\x00") != expected_receipt, "Corrupted-receipt negative control failed")
report = next(e for e in receipt["artifacts"] if e["relative_path"] == "REPORT.md")
require(digest((root / "REPORT.md").read_bytes() + b"\x00") != report["sha256"], "Corrupted-artifact negative control failed")
print(json.dumps({"verified": True, "optimization_level": sys.flags.optimize, "artifact_count": len(receipt["artifacts"]), "external_input_count": len(receipt["external_semantic_inputs"]), "negative_controls": ["appended-byte receipt rejected", "appended-byte report rejected"], "mathematical_claim": "Integrity checks only; not a computational proof of topology or spectral existence."}, sort_keys=True))

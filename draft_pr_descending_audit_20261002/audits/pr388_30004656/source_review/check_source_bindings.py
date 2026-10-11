"""Check independently fetched PDFs against the frozen candidate's source pins.

This is a provenance check only; it does not prove any probability theorem.
"""
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent
CANDIDATE = BASE.parent / "snapshot" / "problems" / "30004656_robustness"
LOCAL_MAP = {
    "sources/bln2020.pdf": "bln2020.pdf",
    "sources/bln2021-published.pdf": "bln2021-published.pdf",
    "sources/owr2021-15.pdf": "owr2021-15.pdf",
    "sources/shmalo2026.pdf": "shmalo2026.pdf",
    "sources/wu2023.pdf": "wu2202.pdf",
}
results = []
for record in json.loads((CANDIDATE / "SOURCE_MANIFEST.json").read_text())["files"]:
    if record["path"] not in LOCAL_MAP:
        continue  # Historical rendered PNG is deliberately not byte-certified here.
    data = (BASE / "raw_sources" / LOCAL_MAP[record["path"]]).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert len(data) == record["bytes"] and digest == record["sha256"], record["path"]
    results.append({"candidate_path": record["path"], "matched": True, "sha256": digest})
assert len(results) == 5
official_wu = (BASE / "raw_sources" / "wu2023.pdf").read_bytes()
official_wu_hash = hashlib.sha256(official_wu).hexdigest()
assert official_wu_hash == "d78924eb42898db89ee0a3e59c1a761d3e4d699ad5f2933d90b2f73c4cfcba53"
assert official_wu_hash != results[-1]["sha256"]
print(json.dumps({
    "verdict": "PASS_SOURCE_AND_SCOPE",
    "candidate_pdf_bindings_reproduced": results,
    "official_wu_pdf_bytes": len(official_wu),
    "official_wu_pdf_sha256": official_wu_hash,
    "candidate_wu_endpoint": "https://arxiv.org/pdf/2202.11592v2",
    "historical_rendered_png_byte_binding_checked": False,
    "original_status": "unsolved",
    "full_literature_or_priority_certification": False,
    "full_shmalo_proof_recertification": False,
}, indent=2) + "\n")

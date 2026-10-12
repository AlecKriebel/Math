#!/usr/bin/env python3
"""Deterministic standard-library ZIP builder with an exact payload manifest."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import zipfile

if sys.flags.optimize:
    raise RuntimeError("Archive construction requires nonoptimized execution.")
if sys.argv[1:]:
    raise RuntimeError("Usage: python -B build_archive.py")
root = Path(__file__).resolve().parent
names = [
    "LICENSE.md", "PROVENANCE.md", "README.md", "SOURCE_BINDING.json",
    "build_archive.py", "paper.tex", "primary_source_scope.json",
    "run_capture.py", "source/CANDIDATE.md", "verification.json",
    "verify.py", "zenodo_metadata.json",
]
if (root/"common_tangent_nullness.pdf").exists():
    names += ["common_tangent_nullness.pdf","PDF_BINDING.json"]
names.sort()
payload = {}
for name in names:
    p = root/name
    s = p.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1:
        raise RuntimeError("Payload must be an ordinary unlinked regular file: "+name)
    payload[name] = p.read_bytes()
def digest(body):
    return hashlib.sha256(body).hexdigest()
receipt = json.loads(payload["verification.json"])
if receipt["status"] != "PASS_FINITE_CONTROLS" or receipt["optimization"] != 0:
    raise RuntimeError("Passing nonoptimized finite-control receipt required")
for receipt_key, name in (("verify_sha256","verify.py"),
                          ("manuscript_sha256","paper.tex"),
                          ("candidate_sha256","source/CANDIDATE.md")):
    if receipt[receipt_key] != digest(payload[name]):
        raise RuntimeError("Verification receipt is stale for "+name)
binding = json.loads(payload["SOURCE_BINDING.json"])
if binding["candidate"]["sha256"] != digest(payload["source/CANDIDATE.md"]):
    raise RuntimeError("Candidate binding mismatch")
if "common_tangent_nullness.pdf" in payload:
    pdf_binding = json.loads(payload["PDF_BINDING.json"])
    if (pdf_binding["paper_sha256"] != digest(payload["paper.tex"]) or
        pdf_binding["pdf_sha256"] != digest(payload["common_tangent_nullness.pdf"]) or
        pdf_binding["pdf_bytes"] != len(payload["common_tangent_nullness.pdf"])):
        raise RuntimeError("Exported PDF binding is stale for current manuscript/PDF")
manifest = {
    "schema": "common-tangent-nullness-portable-archive/v1",
    "scope": "Exact included bytes; finite controls do not certify the universal theorem or publication approval",
    "publication_date": "2026-10-03",
    "package_kind": "manuscript_pdf_and_supporting_source" if "common_tangent_nullness.pdf" in payload else "source_only_no_exported_pdf",
    "pdf_present": "common_tangent_nullness.pdf" in payload,
    "source_PDF_binding_checked": "PDF_BINDING.json" in payload,
    "payload_domain": names,
    "self_excluded": ["ARCHIVE_MANIFEST.json","common_tangents_null_locus_v1.zip"],
    "entries": {name:{"bytes":len(payload[name]),"sha256":digest(payload[name]),
                       "archive_full_mode": "0100644"} for name in names},
    "ZIP": {"entry_timestamp":[2026,10,3,0,0,0],"compression":"ZIP_STORED",
            "entry_order":"lexicographic","entry_permissions":"0100644",
            "excluded_local_domains":["captures","draft_history","RESEARCH_LOG.md","PREPARATION_NOTES.md"]},
}
manifest_body = (json.dumps(manifest,indent=2,sort_keys=True)+"\n").encode()
(root/"ARCHIVE_MANIFEST.json").write_bytes(manifest_body)
all_payload = dict(payload)
all_payload["ARCHIVE_MANIFEST.json"] = manifest_body
archive = root/"common_tangents_null_locus_v1.zip"
temporary = root/"common_tangents_null_locus_v1.zip.tmp"
if temporary.exists():
    raise RuntimeError("Unexpected retained temporary archive; inspect it before retrying")
with zipfile.ZipFile(temporary,"w",compression=zipfile.ZIP_STORED) as z:
    for name in sorted(all_payload):
        entry = zipfile.ZipInfo(name,(2026,10,3,0,0,0))
        entry.create_system = 3
        entry.external_attr = 0o100644 << 16
        entry.compress_type = zipfile.ZIP_STORED
        z.writestr(entry,all_payload[name])
with zipfile.ZipFile(temporary) as z:
    if z.namelist() != sorted(all_payload):
        raise RuntimeError("ZIP domain/order mismatch")
    for entry in z.infolist():
        if z.read(entry.filename) != all_payload[entry.filename]:
            raise RuntimeError("ZIP byte mismatch: "+entry.filename)
        if entry.date_time != (2026,10,3,0,0,0) or entry.external_attr >> 16 != 0o100644:
            raise RuntimeError("ZIP metadata mismatch: "+entry.filename)
temporary.replace(archive)
body = archive.read_bytes()
print(json.dumps({"actual_pid":os.getpid(),
    "UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "archive":archive.name,"bytes":len(body),"sha256":digest(body),
    "manifest_sha256":digest(manifest_body),"payload_count":len(names),
    "package_kind":manifest["package_kind"],"readback":"all bytes/domain/order/modes/timestamps passed"},
    indent=2,sort_keys=True))

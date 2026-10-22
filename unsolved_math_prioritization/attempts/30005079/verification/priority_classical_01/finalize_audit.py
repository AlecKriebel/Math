"""Finalize explicit safe allowlist and unchanged-source receipts.
No Git, network, external state or source mutations.
"""
from pathlib import Path
import datetime, hashlib, json, re

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SAFE = [
    "INDEPENDENT_FREEZE_01.md", "RESEARCH_LOG.md", "REPORT.md",
    "SOURCE_LEDGER.json", "SEARCH_LEDGER.json", "PINNED_SOURCE_RECEIPTS.json",
    "FINAL_STATUS.json", "SOURCE_PIN_CHECKS.json", "PRIVACY_SCAN.json", "finalize_audit.py",
]
def pin(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
def write(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

expected = json.loads((BASE / "SOURCE_MANIFEST.json").read_text())
checks = []
for item in expected["files"]:
    actual = pin(BASE / "source" / item["path"])
    checks.append({"path": item["path"], **actual,
                   "matches_external_manifest": all(actual[k] == item[k] for k in ("bytes", "sha256"))})
assert len(checks) == 21 and all(c["matches_external_manifest"] for c in checks)

ledger = json.loads((HERE / "SOURCE_LEDGER.json").read_text())
for body in ledger["bodies"]:
    source = HERE / body["path"]
    body.update(pin(source))
    if body["path"].startswith("../private_sources/"):
        text_path = HERE / "private_tmp" / (source.stem + ".txt")
    else:
        text_path = source.with_suffix(".txt")
    body["private_extraction_pin"] = {"path": str(text_path.relative_to(HERE)), **pin(text_path)}
    text = text_path.read_text()
    body["pdf_pages_in_extraction"] = len(text.rstrip("\f\n").split("\f"))
    body["literal_term_counts"] = {
        "irrational": len(re.findall("irrational", text, re.I)),
        "nondivisorial_or_non_divisorial": len(re.findall(r"non[ -]?divisorial", text, re.I)),
    }
write("SOURCE_LEDGER.json", ledger)
write("SOURCE_PIN_CHECKS.json", {
    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "expected_head": expected["head"], "original_source_files": checks,
    "original_source_unchanged": True, "manifest": pin(BASE / "SOURCE_MANIFEST.json"),
    "primary_bodies": len(ledger["bodies"]), "no_source_payload_written": True,
    "incidents": [
        "Initial pdftotext fourth output failed; first three extractions existed.",
        "Initial zsh here-document creation failed ENOSPC before Python script ran; no successful initial log write.",
        "Later Python-c writes succeeded after parent recovered its own completed runtime space.",
        "MWv1 web-open returned406; direct primary download succeeded and was pinned.",
        "Final report link update via a delete-plus-add patch was rejected before changes because duplicate targets are disallowed; a correctly quoted Python-c write then succeeded.",
    ],
})
findings = []
patterns = {
    "credential": r"(?i)(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._-]{20,})",
    "email_address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
}
for name in SAFE:
    if name in {"PRIVACY_SCAN.json", "finalize_audit.py"}:
        continue
    content = (HERE / name).read_text()
    for label, pattern in patterns.items():
        if re.search(pattern, content):
            findings.append({"file": name, "rule": label})
assert not findings, findings
write("PRIVACY_SCAN.json", {
    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "safe_allowlist": SAFE, "findings": findings, "status": "PASS",
    "scope": "Authored summaries/metadata only; raw bodies/extractions/web outputs excluded from safe payloads.",
    "manual_review": "No copied author email addresses, credentials, personal communications or raw source bodies in safe payloads. Source URLs and relative private-source provenance are intentional metadata. Audit script manually reviewed.",
    "limitations": "Pattern scan plus manual review is bounded, not a universal privacy proof.",
})
write("SAFE_MANIFEST.json", {
    "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "scope": "Explicit allowlist only; manifest excludes itself; private_tmp and unlisted files are not releasable by this manifest.",
    "self_excluded": True,
    "files": [{"path": name, **pin(HERE / name)} for name in SAFE],
})
print(json.dumps({"source_files_unchanged": 21, "primary_bodies": len(ledger["bodies"]),
                  "safe_payloads": len(SAFE), "privacy": "PASS",
                  "manifest": pin(HERE / "SAFE_MANIFEST.json")}, indent=2))


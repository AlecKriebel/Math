#!/usr/bin/env python3
"""Verify cached source integrity and priority metadata; no mathematical test."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re


def main():
    here = Path(__file__).resolve().parent
    manifest = json.loads((here / "SOURCE_MANIFEST.json").read_text())
    checked, failed_retrievals = [], []
    for entry in manifest["sources"]:
        if "sha256" not in entry:
            assert "error" in entry
            failed_retrievals.append({k: entry[k] for k in ("url", "error")})
            continue
        path = (here / entry["file"]).resolve()
        path.relative_to(here)
        data = path.read_bytes()
        assert len(data) == entry["bytes"], entry["file"]
        assert hashlib.sha256(data).hexdigest() == entry["sha256"], entry["file"]
        checked.append(entry["file"])
    main_text = (here / "sources/notebook21_fresh.txt").read_text()
    update_text = (here / "sources/notebook_updates_fresh.txt").read_text()
    start, end = main_text.index("21.123."), main_text.index("21.124.")
    statement = main_text[start:end]
    assert "Definition 66" in statement and "A. Smoktunowicz" in statement
    assert main_text[start - 1] == "\n"
    assert len(re.findall(r"21\.123", update_text)) == 0
    accepted = (here / "sources/smoktunowicz_accepted_pure.txt").read_text()
    for number in (18, 19, 23, 26):
        assert "Definition " + str(number) + "." in accepted
    old = (here / "sources/smoktunowicz2410.20440v2.txt").read_text()
    for number in (59, 60, 64, 66):
        assert "Definition " + str(number) + "." in old
    crossref = json.loads((here / "sources/fraga_crossref.json").read_text())["message"]
    assert crossref["DOI"] == "10.20944/preprints202608.2109.v1"
    assert crossref["published"]["date-parts"] == [[2026, 8, 28]]
    assert len(crossref["author"]) == 1
    assert crossref["author"][0]["family"] == "Fraga"
    assert crossref["type"] == "posted-content"
    out = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS_SOURCE_INTEGRITY_AND_METADATA_ONLY",
        "authenticated_artifacts": len(checked),
        "files_checked": checked,
        "failed_retrievals": failed_retrievals,
        "notebook_pdf_page_one_based": 1 + main_text[:start].count("\f"),
        "notebook_statement_line": 1 + main_text[:start].count("\n"),
        "update_mentions": 0,
        "prior_claim_doi": crossref["DOI"],
        "mathematical_claim_reviewed": False,
        "source_manifest_sha256": hashlib.sha256((here / "SOURCE_MANIFEST.json").read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (here / "source_check.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("files_checked", "failed_retrievals")}, indent=2))


if __name__ == "__main__":
    main()

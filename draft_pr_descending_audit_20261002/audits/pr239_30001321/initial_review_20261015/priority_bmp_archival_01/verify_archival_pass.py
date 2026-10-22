#!/usr/bin/env python3
"""Verify saved metadata/index coverage; this does not authenticate target theorems."""
from pathlib import Path
import hashlib
import json
import re
import urllib.parse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / "private_sources"
OAI_SHA256 = "46cc83874dd00868b8a3e8fd0438bc180d651c812c7a69f47a124bec83e2ea98"


def main():
    oai = (PRIVATE / "sapienza_bmp1999_oai.html").read_bytes()
    assert len(oai) == 2913
    assert hashlib.sha256(oai).hexdigest() == OAI_SHA256
    tree = ET.fromstring(oai)
    descriptions = [x.text for x in tree.iter() if x.tag == "{http://purl.org/dc/elements/1.1/}description"]
    assert len(descriptions) == 1
    assert "finite set" in descriptions[0]
    assert "stochastic term is small" in descriptions[0]
    assert "final point" in descriptions[0]

    years = [f"{year % 100:02d}" for year in range(1991, 2009)]
    checked = []
    for year in years:
        # The historical indexes contain Latin-1 names; all query strings are ASCII.
        text = (PRIVATE / f"mparc_index_{year}.html").read_bytes().decode("latin-1")
        assert "<html" in text.lower()
        assert not re.search(r"boldrighini|pellegrinotti|integral and local", text, re.I)
        checked.append(year)

    library = json.loads((PRIVATE / "nasplib_tsp_years.json").read_text())
    children = library["_embedded"]["subcommunities"]
    assert library["page"]["totalElements"] == 4
    assert library["page"]["totalPages"] == 1
    annual_names = [child["name"] for child in children]
    assert [re.search(r"20\d\d", name).group() for name in annual_names] == ["2005", "2006", "2007", "2008"]

    inventory = json.loads((PRIVATE / "private_source_sha256.json").read_text())
    for item in inventory:
        data = (ROOT / item["path"]).read_bytes()
        assert len(data) == item["bytes"], item["path"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"], item["path"]
    assert not list(PRIVATE.glob("*.pdf")), "Unexpected PDF needs source authentication"

    sanitation = json.loads((ROOT / "sanitation_receipt.json").read_text())
    preserved_receipt_path = ROOT / sanitation["private_original_receipt_path"]
    assert preserved_receipt_path.resolve().is_relative_to(PRIVATE.resolve())
    preserved_receipt_bytes = preserved_receipt_path.read_bytes()
    assert hashlib.sha256(preserved_receipt_bytes).hexdigest() == sanitation["private_original_receipt_sha256"]
    preserved = json.loads(preserved_receipt_bytes)
    snapshot = preserved_receipt_path.parent
    assert len(preserved["preserved_artifacts"]) == 7
    for item in preserved["preserved_artifacts"]:
        data = (snapshot / item["path"]).read_bytes()
        assert len(data) == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
    original_manifest_bytes = (snapshot / "authored_manifest.json").read_bytes()
    assert hashlib.sha256(original_manifest_bytes).hexdigest() == sanitation["original_authored_manifest_sha256"]
    original_manifest = json.loads(original_manifest_bytes)
    assert len(original_manifest["artifacts"]) == 6
    for item in original_manifest["artifacts"]:
        data = (snapshot / item["path"]).read_bytes()
        assert len(data) == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
    original_log = (snapshot / "access_attempts.jsonl").read_bytes()
    sanitized_log = (ROOT / "access_attempts.jsonl").read_bytes()
    assert hashlib.sha256(original_log).hexdigest() == sanitation["original_access_log_sha256"]
    assert hashlib.sha256(sanitized_log).hexdigest() == sanitation["sanitized_access_log_sha256"]
    old_lines = original_log.splitlines(keepends=True)
    new_lines = sanitized_log.splitlines(keepends=True)
    assert len(old_lines) == len(new_lines)
    assert old_lines[:19] == new_lines[:19] and old_lines[20:] == new_lines[20:]
    old_row, new_row = json.loads(old_lines[19]), json.loads(new_lines[19])
    old_url = urllib.parse.urlsplit(old_row["final_url"])
    assert old_url.hostname == "validate.perfdrive.com" and old_url.query
    old_row["final_url"] = urllib.parse.urlunsplit((old_url.scheme, old_url.netloc, old_url.path, "", ""))
    redaction = new_row.pop("redaction")
    assert old_row == new_row
    assert redaction["private_original_receipt_sha256"] == sanitation["private_original_receipt_sha256"]
    assert redaction["reason"] == sanitation["reason"]
    assert redaction["removed_query_parameter_count"] == len(urllib.parse.parse_qsl(old_url.query)) == 13
    for line in new_lines:
        row = json.loads(line)
        for field in ("url", "final_url"):
            url = urllib.parse.urlsplit(row.get(field, ""))
            if url.hostname == "validate.perfdrive.com":
                assert not url.query and not url.fragment
    assert sanitation["primary_evidence_changed"] is False
    result = {
        "status": "saved_metadata_and_scoped_coverage_verified",
        "target_full_primary_acquired": False,
        "target_theorem_authenticated": False,
        "mparc_years_checked": list(range(1991, 2009)),
        "tsp_library_annual_children": annual_names,
        "oai_bytes": len(oai),
        "oai_sha256": OAI_SHA256,
        "saved_response_hashes_verified": len(inventory),
        "sanitized_public_challenge_urls": True,
        "original_six_artifacts_and_manifest_preserved": True,
        "primary_evidence_changed": False,
        "private_original_receipt_sha256": sanitation["private_original_receipt_sha256"],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

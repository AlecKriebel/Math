#!/usr/bin/env python3
"""Seal only an explicit list of this reviewer's original artifact bytes."""
from pathlib import Path
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
control = json.loads((HERE / "CONTROL_RESULTS.json").read_text())
at = datetime.datetime.now(datetime.timezone.utc).isoformat()
sources = []
urls = {
    "original_target": "https://ems.press/content/serial-article-files/46543",
    "precursor": "https://arxiv.org/pdf/1310.0267v2",
    "published_spin": "https://www.aimsciences.org/data/article/export-pdf?id=62f0b16d2d80b744cabd75fa"}
pages = {
    "original_target": [10,11], "precursor": [2,3],
    "published_spin": [8,11,12,19,20,21,22,23,26,27,28,29,32,33,34,35]}
for record in control["primary_source_bindings"]:
    sources.append({**record, "url": urls[record["role"]],
                    "complete_pdf_pages_visually_inspected_by_this_reviewer": pages[record["role"]]})
receipt = {
    "at_utc": at,
    "source_acquisition": "Local ignored primary PDFs provided by root; actual bytes independently hashed and relevant complete pages personally viewed",
    "sources": sources,
    "published_pdf_all_37_pages_read": False,
    "complete_relevant_published_pages_read": True,
    "online_metadata_reads": [
        {"url": "https://www.aimsciences.org/article/doi/10.3934/dcds.2022105",
         "own_observation": "Journal issue 42(11), pages 5399-5435, 2022; online date 2022-08-08; Table 1 matches PDF values and stated error"},
        {"url": "https://arxiv.org/abs/2108.08642v1",
         "own_observation": "Versioned record states 2021-08-19 submission; prior-v1 PDF not independently read in this audit"}],
    "original_record_read": "queue.py show 30002737 read only; complete imported statement/context/prior_research(empty) inspected",
    "frozen_input_count": len(control["frozen_input_bindings"]),
    "frozen_input_bindings_in": "CONTROL_RESULTS.json",
    "foreign_source_bytes_public": False,
    "private_renders_under": "private_sources/",
    "initial_independent_checkpoint": "INITIAL_CHECKPOINT.md",
    "later_parent_source_inference": "Positive weighting proposal exposed after initial checkpoint and initial written report; independently checked, explicitly identified in final report",
    "final_root_priority_verdict_or_peer_final_report_read": False}
(HERE / "SOURCE_RECEIPTS.json").write_text(json.dumps(receipt, indent=2)+"\n")
result = json.loads((HERE / "RESULT.json").read_text())
result["at_utc"] = at
(HERE / "RESULT.json").write_text(json.dumps(result, indent=2)+"\n")
with (HERE / "RESEARCH_LOG.md").open('a') as out:
    out.write(f"- {at} - Final classification audit package sealed. Completion estimate: 100%. Qualified prior-application PASS; zero structural blockers or mandatory repairs; one local independent integral-certificate gap explicitly retained. Original proof-search attempts 0. No foreign source bytes included in positive public allowlist.\n")
own_files = [
    "INITIAL_CHECKPOINT.md", "RESEARCH_LOG.md", "REPORT.md", "RESULT.json",
    "RAW_FINDINGS.md", "check_controls.py", "CONTROL_RESULTS.json",
    "SOURCE_RECEIPTS.json", "seal_package.py"]
records = []
for name in own_files:
    path = HERE / name
    assert path.is_file() and 'private_sources' not in path.parts
    data = path.read_bytes()
    records.append({"path": name, "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "provenance": "this reviewer's original prose, code, or generated own-code results/metadata"})
manifest = {"at_utc": at,
            "kind": "positive own-byte allowlist",
            "scope": "only the listed files plus this self-excluding manifest; no globs or private input files",
            "files": records,
            "file_count_excluding_manifest": len(records),
            "manifest_self_sha256_excluded": True}
(HERE / "PUBLIC_FILES.json").write_text(json.dumps(manifest, indent=2)+"\n")
print(json.dumps({"public_file_count_excluding_manifest": len(records),
                  "frozen_bound_files": len(control["frozen_input_bindings"]),
                  "classification_blockers": result["classification_blockers"],
                  "independent_integral_certificate_here": False,
                  "at_utc": at}, indent=2))

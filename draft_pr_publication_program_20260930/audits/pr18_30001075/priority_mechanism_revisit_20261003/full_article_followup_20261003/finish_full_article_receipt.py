"""Own dated reading/source handoff; no ROOT custody or priority approval."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

if sys.flags.optimize or not __debug__:
    raise RuntimeError("Active assertions required")
base = Path(__file__).resolve().parent
receipt_path = base / "SOURCE_RECEIPT_FULL_ARTICLE.json"
if receipt_path.exists():
    raise RuntimeError("Preserve a dated receipt; never overwrite it")
def pin(p, relative=False):
    b = p.read_bytes()
    return dict(path=str(p.relative_to(base)) if relative else str(p),
        bytes=len(b), sha256=hashlib.sha256(b).hexdigest(),
        full_mode_07777=format(stat.S_IMODE(p.stat().st_mode),"04o"))
pdf = Path("/Users/alec/Downloads/Some-New-Results-on-Geometric-Transversals.pdf")
source = pin(pdf)
assert source["bytes"]==596169 and source["sha256"]=="478c879b6fea91b1aa17b0ea90172c10e01432b90e11c0873881f864151fdafc"
extraction = json.loads((base / "EXTRACTION_RECEIPT.json").read_text())
render = json.loads((base / "RENDER_RECEIPT.json").read_text())
assert source == extraction["source"] == render["source"]
assert extraction["pages"] == 30
assert all(x["exit_code"] == 0 and x["stderr"]["bytes"] == 0 for x in extraction["captures"])
assert all(x["exit_code"] == 0 and x["stderr"]["bytes"] == 0 for x in render["captures"])
now = datetime.now(timezone.utc).isoformat()
with (base / "RESEARCH_LOG.md").open("a") as log:
    log.write("- "+now+":100% of the full published-article follow-up. All30 pages personally read;9 selected page images inspected; authored exact scope/non-adapters complete. Source body unchanged; owned files frozen. No combined-body access gap remains in this family. ROOT priority decision/publication remain later steps; new attempt/audit/novelty0.\n")
files = sorted(p for p in base.rglob("*") if p.is_file())
for p in files:
    p.chmod(0o444)
dirs = [base] + sorted(p for p in base.rglob("*") if p.is_dir())
for p in dirs:
    p.chmod(0o755)
public = [pin(p,True) for p in files if "private_inputs" not in p.relative_to(base).parts]
private = [pin(p,True) for p in files if "private_inputs" in p.relative_to(base).parts]
pages = []
for n in range(1,31):
    p = base / "private_inputs" / ("page_%02d.txt"%n)
    pages.append(dict(pdf_page_index=n-1, printed_page=673+n,
        text=pin(p,True), personal_text_read=True,
        personal_text_read_completed_by_utc="2026-10-03T21:19:47Z",
        individual_page_read_time_not_recorded=True,
        selected_visual_inspection=n in render["rendered_pages"]))
receipt = dict(schema="pr18-full-published-article-reading-source/v1", utc=now,
    actual_preparer_pid=os.getpid(), source_pdf_external_in_place=source,
    original_head="99e403e85d38d92b021198c4a57bbad3cd8775ba",
    candidate_sha256="8ac19b70bd9081107e903ca47bb9dd6ad05274f604d03000a7fd18e3cfb3bf12",
    published_article_doi="10.1007/s00454-023-00573-2", printed_pages="674-703",
    page_reading=pages,
    textual_read_scope="All30 pages, all presented proofs/remarks/references; six complete five-page reads",
    selected_visual_pages=render["rendered_pages"], all_page_pixel_read_claim=False,
    presented_proofs_read=["Theorem1.1/Lemmas2.1-2.2 and k-flat lift",
        "Proposition1.2/Claims3.1-3.2", "Theorem1.3/Lemmas4.1-4.4 and compact/Mnev sketches",
        "Theorem1.4/Lemmas5.1-5.2", "Theorem1.5/Lemma6.1 and stated matroid extension"],
    imported_background_proofs_independently_recertified=False,
    published_Theorem6_2_has_no_proof_in_this_body=True,
    public_handoff_members=public, private_inputs_excluded_from_publication=private,
    full_directory_modes=[dict(path=str(p.relative_to(base)) or ".",
        full_mode_07777=format(stat.S_IMODE(p.stat().st_mode),"04o")) for p in dirs],
    source_receipt_self_absent=True,
    historical_parent_snapshot_in_place=pin(base.parent / "SOURCE_RECEIPT.json"),
    historical_report_in_place=pin(base.parent / "REPORT.md"),
    historical_actual_control_in_place=pin(base.parent / "actual_scope_controls_capture/CAPTURE.json"),
    controls_rerun_or_newly_credited=False,
    mode_chronology="All owned capture descriptors preserve dated0644; current own file modes0444. External sourcePDF remains0644 unchanged. Parent historical snapshot files unchanged.",
    actual_extraction=dict(controller_pid=95874, pdfinfo_child_pid=95884,
        pdftotext_child_pid=95889, stdout_bytes=[807,94676], stderr_bytes=[0,0]),
    actual_render=dict(controller_pid=97274,
        child_pids=[97275,97276,97277,97278,97279,97282,97283,97284,97285],
        all_exit0=True, all_stdout_stderr0=True),
    scoped_scientific_finding="No exact prior spatial tritangent nullness theorem or complete adapter located in the full published body; former body-access concern resolved",
    recommendation_to_ROOT="Make fresh bounded priority decision; no global-earliest/exhaustive claim",
    ROOT_custody=False, ROOT_priority_approval=False, publication_ready_asserted=False,
    new_attempts=0, audit_credit=0, novelty_credit=0,
    native_Git_remote_publication_mutations=False, copyrighted_primary_bodies_publicly_copied=False)
receipt_path.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
receipt_path.chmod(0o444)
print(json.dumps(dict(status="OWN_FULL_ARTICLE_HANDOFF_COMPLETE", pid=os.getpid(),utc=now,
    report=pin(base / "REPORT_FULL_ARTICLE.md"), receipt=pin(receipt_path),
    public_members=len(public), excluded_private_members=len(private),
    ROOT_custody=False, ROOT_priority_approval=False),indent=2,sort_keys=True))

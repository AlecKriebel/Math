#!/usr/bin/env python3
"""Apply the bounded editorial package01 repairs once, preserving frozen history.
No proof rewrite, proof replay, Git command, service action or publication.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json, shutil, datetime, hashlib
ROOT=Path(__file__).resolve().parents[2]
PUB=ROOT/'publication'
HISTORY=PUB/'evidence/history/pre_whole01'
UTC=datetime.datetime.now(datetime.timezone.utc).isoformat()
def write_json(p,o): p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def replace(p,old,new):
 text=p.read_text(); count=text.count(old)
 if count != 1: raise RuntimeError(f'Expected one occurrence in {p}: {count}')
 p.write_text(text.replace(old,new))
HISTORY.mkdir(parents=True,exist_ok=False)
for name in ['PREPARATION_REPORT.md','BUILD_VALIDATION.json','PACKAGE_INPUT_PINS.json','PACKAGE_MANIFEST.json','CANDIDATE_INTEGRITY.json','metadata.json','zenodo_metadata_wrapper.json','evidence/COMPILATION.json','evidence/CURRENT_REVIEW_STATE.json']:
 src=PUB/name; dest=HISTORY/src.name
 shutil.copyfile(src,dest)
replace(PUB/'research_note.tex',r'+sum_{i<j<h}',r'+\sum_{i<j<h}')
replace(PUB/'research_note.tex','The accompanying package awaits a fresh whole-package review.','The accompanying kit records the review history through 13 October 2026\nand the current preparation state.')
replace(PUB/'README.md','This is a prepared, unrefereed application-note candidate. **Fresh whole-package review NEWwhole01 is pending; publication readiness is false.** Mathematical acceptance of the original scoped statements and adoption of a credited application framing are earlier, separate stages.','This is a prepared, unrefereed application-note candidate. The accompanying kit records the review history through 13 October 2026 and the current preparation state in `evidence/CURRENT_REVIEW_STATE.json`. Publication readiness remains false after the two repairs requested by whole-package review NEWwhole01; fresh exact-candidate review NEWwhole02 and root adoption are required. Mathematical acceptance and adoption of credited application framing are earlier, separate stages.')
replace(PUB/'README.md','Neither is evidence of an upload or deposit.','`zenodo-deposit.json` is a local repo-tool input with exactly the same metadata plus the two file paths/upload names; it is prepared configuration, not evidence of an upload or deposit.')
replace(PUB/'README.md','or `tectonic --outdir tmp/pdfs research_note.tex` for a disk PDF,','or run the following commands for a disk PDF:\n\n```sh\nmkdir -p tmp/pdfs\ntectonic --outdir tmp/pdfs research_note.tex\n```\n\nThen')
replace(PUB/'README.md','Then then copy','Then copy') if 'Then then copy' in (PUB/'README.md').read_text() else None
replace(PUB/'SUPPLEMENT.md','`evidence/CURRENT_REVIEW_STATE.json` records pending NEWwhole01 with `publication_ready=false`.','The kit records review history through 13 October 2026 and its current preparation state in `evidence/CURRENT_REVIEW_STATE.json`, with `publication_ready=false`. NEWwhole01 requested the two editorial/package repairs documented in `reviews/package_01/REPORT.md`; their application is documented in `reviews/package_repair_01/REPAIR_REPORT.md`. The changed exact candidate requires NEWwhole02.')
replace(PUB/'AUTHORSHIP_LICENSE.md','The pending NEWwhole01 state is a workflow gate and should not be mistaken for an accepted journal result or a published deposit.','The accompanying kit records the review history through 13 October 2026 and the current preparation state. Internal review records do not establish an accepted journal result or a published deposit.')
replace(PUB/'evidence/INDEX.md','6. **Current authored preparation**: `publication/research_note.tex/.pdf`, metadata and exact wrapper, README, SUPPLEMENT, source/framing/omission ledgers, log, and deterministic builder. Current state is `publication/evidence/CURRENT_REVIEW_STATE.json`: **PENDING NEWwhole01; not publication-ready**.','6. **Frozen first assembled-candidate review**: `reviews/package_01/REPORT.md`, `VERDICT.json`, complete independent derivation, fresh interface/check/package records and unchanged output pins record NEWwhole01: REPAIR_REQUIRED, with one missing summation operator and one clean-build directory omission. `ROOT_PREPRINT_REVIEW_01.json` is the frozen root page/source inspection of that earlier candidate. Its source/PDF pins remain historical.\n7. **Current authored repair preparation**: `publication/research_note.tex/.pdf`, metadata, exact wrapper and local repo-tool deposit configuration, README, SUPPLEMENT, ledgers, log, and the extended existing deterministic builder. `reviews/package_repair_01/REPAIR_REPORT.md` documents the bounded repairs. Current state is `publication/evidence/CURRENT_REVIEW_STATE.json`: **PENDING NEWwhole02; not publication-ready**. `publication/evidence/MAP.json` identifies old-input stages; `publication/evidence/history/pre_whole01/` preserves the prior preparation/compilation/manifest receipts verbatim. Their old visual observations are not validation of the repaired candidate.')
state=json.loads((PUB/'evidence/CURRENT_REVIEW_STATE.json').read_text())
state.update(utc=UTC,required_review='NEWwhole02',review_assigned=False,review_verdict=None,previous_review={'review':'NEWwhole01','status':'REPAIR_REQUIRED','verdict':'reviews/package_01/VERDICT.json','candidate_tex_sha256':'56a869e03a2ef0ee2f17fba48ad7f9fd07278d954938036bbcb8f3725e7c6d0d','candidate_pdf_sha256':'9dc9ff1198294fa7d64d6bc0f94d0466572cddcd1fda11a8e28e545a6afa5841'},repair_state='REVIEW1_ISSUES_REPAIRS_APPLIED_NOT_FINAL_CLEARANCE',applied_issue_ids=['PACKAGE01-P2-01','PACKAGE01-P3-02'],stage_wording_advice_applied=True)
write_json(PUB/'evidence/CURRENT_REVIEW_STATE.json',state)
metadata=json.loads((PUB/'metadata.json').read_text())
metadata['notes']=metadata['notes'].replace('Prepared candidate; pending fresh whole-package review NEWwhole01.','The accompanying kit records the review history through 13 October 2026 and the current preparation state.')
write_json(PUB/'metadata.json',metadata); write_json(PUB/'zenodo_metadata_wrapper.json',{'metadata':metadata})
write_json(PUB/'zenodo-deposit.json',{'metadata':metadata,'files':[{'path':'research_note.pdf','name':'free-exterior-string-links-v1.0.pdf'},{'path':'source_audit_kit.zip','name':'free-exterior-string-links-v1.0-source-audit-kit.zip'}]})
build=PUB/'build_package.py'
replace(build,'"tmp", "duplicateinputarchives"','"tmp", "duplicateinputarchives", "reconstruction", "extracted", "render", "renders", "original_bytes"')
replace(build,'state["required_review"] == "NEWwhole01"','state["required_review"] == "NEWwhole02"')
replace(build,'this preparation builder binds the pending NEWwhole01 candidate only','this preparation builder binds the repaired pending NEWwhole02 candidate only')
replace(build,'"stage": "prepared_application_note_pending_NEWwhole01"','"stage": "repaired_application_note_pending_NEWwhole02"')
replace(build,'"required_review": "NEWwhole01"','"required_review": "NEWwhole02"')
replace(build,'require(wrapper == {"metadata": metadata}, "Zenodo wrapper differs from exact metadata")','require(wrapper == {"metadata": metadata}, "Zenodo wrapper differs from exact metadata")\n    deposit = json.loads(files["publication/zenodo-deposit.json"])\n    require(deposit == {"metadata": metadata, "files": [\n        {"path": "research_note.pdf", "name": "free-exterior-string-links-v1.0.pdf"},\n        {"path": "source_audit_kit.zip", "name": "free-exterior-string-links-v1.0-source-audit-kit.zip"},\n    ]}, "local repo-tool deposit configuration differs from exact metadata/file names")')
print(json.dumps({'utc':UTC,'editorial_repairs_applied':True,'new_review':'NEWwhole02','proof_changes':'one missing summation backslash only; disclosure sentence updated; no proof rewrite'},indent=2))

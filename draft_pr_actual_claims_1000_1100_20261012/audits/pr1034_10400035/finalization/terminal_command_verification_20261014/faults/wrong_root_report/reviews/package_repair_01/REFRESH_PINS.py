#!/usr/bin/env python3
"""Refresh current authored pins and omission metadata; no archive build/action."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json, hashlib, datetime
ROOT=Path(__file__).resolve().parents[2]
PUB=ROOT/'publication'
def write_json(p,o):p.write_text(json.dumps(o,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
def main():
 allow=json.loads((PUB/'PACKAGE_ALLOWLIST.json').read_text());names=allow['files'];selected=set(names)
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 generated={'publication/PACKAGE_INPUT_PINS.json','publication/PACKAGE_MANIFEST.json','publication/CANDIDATE_INTEGRITY.json','publication/source_audit_kit.zip','publication/BUILD_VALIDATION.json','reviews/package_repair_01/VERIFY_FINAL_RESULT.json','reviews/package_repair_01/CHANGED_PATHS.json','reviews/package_repair_01/NEW_CANDIDATE_PINS.json','reviews/package_repair_01/OUTPUT_PINS.json'}
 omitted=[];transient={'tmp','reconstruction','render','renders','cache','caches','__pycache__'}
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file():continue
  n=p.relative_to(ROOT).as_posix();parts=p.relative_to(ROOT).parts
  if n in selected or n in generated or set(x.lower() for x in parts)&transient:continue
  if any(x.lower() in {'raw','rawprivate','private'} for x in parts):reason='Third-party/private source body, extract or source derivative; excluded regardless of suffix.'
  elif p.suffix.lower() in {'.txt','.stdout','.stderr','.html','.ps','.eps','.png','.jpg','.jpeg','.gif','.webp','.pyc','.pyo'}:reason='Extracted/verbatim/source-body text, rendered/source image, stream or cache; excluded even outside raw.'
  elif p.suffix.lower()=='.zip':reason='Input/duplicate/generated archive excluded; only the output archive is delivered outside its own payload.'
  elif p.suffix.lower()=='.pdf':reason='Duplicate historical manuscript or third-party PDF; only current authored manuscript PDF is admitted.'
  elif 'history' in parts:reason='Local byte custody of prior candidate; selected preserved preparation receipts are archived separately with historical-stage map.'
  else:reason='Outside explicitly selected authored payload, or external noncircular generated/verification record.'
  omitted.append({'path':n,'bytes':p.stat().st_size,'reason':reason})
 ledger={'schema':'actual-stable-file-exclusion-ledger-v2','utc':utc,'policy':'No third-party bodies/rawprivate/verbatim extracts including .txt outside raw/OCR/images/caches/bytecode/duplicate input archives. Only authored records and the current manuscriptPDF admitted.','stable_omitted_files_snapshot':omitted,'transient_excluded_trees':['Any tmp, reconstruction, extracted, render, renders, cache, caches or __pycache__ directory at any depth; their contents are never admitted. Transient generated/extracted inventory is not a current-package hash scope.'],'internal_generated_records_added_to_archive_without_self_hash':['publication/PACKAGE_INPUT_PINS.json','publication/PACKAGE_MANIFEST.json'],'external_generated_records_excluded':['publication/BUILD_VALIDATION.json','publication/CANDIDATE_INTEGRITY.json','publication/source_audit_kit.zip','reviews/package_repair_01/VERIFY_FINAL_RESULT.json','reviews/package_repair_01/CHANGED_PATHS.json','reviews/package_repair_01/NEW_CANDIDATE_PINS.json','reviews/package_repair_01/OUTPUT_PINS.json'],'actual_current_archive_checked_independently':'reviews/package_repair_01/VERIFY_FINAL.py','original_19_preserved':True,'original_historical_meanings_preserved':True,'historical_omitted_scripts_replayed':False,'new_review_checks_are_stage_evidence':True}
 write_json(PUB/'evidence/OMISSIONS.json',ledger)
 rows=[]
 for n in names:
  b=(ROOT/n).read_bytes();rows.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 write_json(PUB/'PACKAGE_INPUT_PINS.json',{'schema':'authored-candidate-input-pins-v1','stage':'repaired_application_note_pending_NEWwhole02','hash_scope':'Every allowlisted authored input; excludes this pin record to avoid circularity. Historical pin meanings are preserved in publication/evidence/MAP.json.','files':rows})
 print(json.dumps({'payload_files':len(rows),'stable_omitted_files':len(omitted),'stage':'repaired_application_note_pending_NEWwhole02'},indent=2))
if __name__=='__main__':main()

#!/usr/bin/env python3
"""Publish-safe local final report/freeze after the actual eight-PR offline analysis."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
OUT=Path(__file__).resolve().parent
NUMBERS=(615,618,623,628,630,662,672,681)
def sha(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(path.read_text())
def dump(path,data):path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def require(ok,message):
 if not ok:raise SystemExit(message)
def main():
 require((OUT/'RECONCILIATION_RESULT.json').is_file(),'Actual completed-eight analysis has not run; no final report can be prepared.')
 require(not (OUT/'FINAL_FREEZE.json').exists(),'Final freeze already exists; do not overwrite frozen findings.')
 result=load(OUT/'RECONCILIATION_RESULT.json');entries=result['entries']
 require(result['status']=='PASS' and result['mandatory_findings']==0 and tuple(x['pr'] for x in entries)==NUMBERS,'Actual completed-eight reconciliation does not pass.')
 expected=load(OUT/'EXPECTED_COMPLETED_EIGHT.json')['entries'];ours={tuple(x['tracker_row']) for x in expected if 'doi' in x}
 raw=load(OUT/'tmp/tracker_all_A_D.json')['response'].get('values',[])
 unrelated={tuple((x+['']*4)[:4]) for x in raw[1:] if tuple((x+['']*4)[:4]) not in ours}
 violations=[]
 def scan(obj,name):
  if isinstance(obj,dict):
   if 'sheetId' in obj and obj['sheetId']!=1254632077:violations.append({'file':name,'type':'unrelated_sheet_properties'})
   for value in obj.values():scan(value,name)
  elif isinstance(obj,list):
   if len(obj)>=3 and all(isinstance(x,str) for x in obj) and tuple((obj+['']*4)[:4]) in unrelated:violations.append({'file':name,'type':'unrelated_full_tracker_row'})
   for value in obj:scan(value,name)
 for path in OUT.glob('*.json'):
  if path.name not in ('PREPARATION_FREEZE.json','FINAL_FREEZE.json'):scan(load(path),path.name)
 now=datetime.now(timezone.utc).isoformat()
 dump(OUT/'PRIVACY_OUTPUT_SCAN.json',{'utc':now,'status':'PASS' if not violations else 'FAIL','unrelated_raw_row_payloads_compared':len(unrelated),'public_JSON_files_scanned':len(list(OUT.glob('*.json'))),'unrelated_row_or_tab_payloads_found':violations,'raw_contents_not_included':True,'external_calls_made':0})
 require(not violations,'Publication privacy scan failed; retain unexpected data privately before freezing.')
 closed=[x['pr'] for x in entries if x['disposition']=='CLOSED_WITHOUT_MERGE'];published=[x for x in entries if x['disposition']=='MERGED_PUBLISHED_TRACKED']
 lines=['# Final eight-PR read-only reconciliation','',f'Completed {now}. All {result["checks"]} checks pass with 0 mandatory findings. No external mutations, shared Git checkout/index changes, mathematical reaudit or skipped-PR processing occurred. This artifact does not modify the persistent goal status.','',f'The closed-without-merge PRs {closed} match their saved original heads, closure timestamps, exact posted comment bodies and URLs. Every original and accepted GitHub commit still resolves.','',f'The {len(published)} published PRs match their saved accepted heads, actual merge commits, scoped file inventories and selected queue rows. Their production public Zenodo records match every supplied metadata field under explicit native schema mapping and the exact normalization recorded in that same record’s actual production publication receipt. Only PR681 record23387442 may use the exact html.escape(local_description, quote=False) transformation, and only with the singleton plain_text_html_entities receipt and unchanged kit plain-text eligibility; all other fields stay exact. The other three records must retain empty normalization lists. Unknown normalization lists fail. Raw local and native metadata are preserved separately in METADATA_COMPARISON records. Exact public PDF/ZIP downloads match accepted local bytes and saved SHA-256/MD5/size evidence; each DOI resolves to its exact production record.','',"The spreadsheet ID, Math Puzzles tab, gid 1254632077, header, exact saved A:D rows and global normalized DOI uniqueness all match.",'','| PR | DOI | Exact tracker row |','| --- | --- | --- |']
 for item in published:lines.append(f'| #{item["pr"]} | {item["doi"]} | {item["tracker_range"]} |')
 lines.extend(['','Actual record-specific metadata normalization evidence:'])
 for item in published:lines.append(f'- PR #{item["pr"]}, {item["doi"]}: {json.dumps(item["metadata_receipt_normalizations"],ensure_ascii=False)}; comparison {item["description_comparison_rule"]["comparison"]}.')
 lines.extend(['','All spreadsheet responses, including full-column values, all-tab metadata and exact-row requests, are retained only in ignored tmp/ before allowlisted evidence is emitted. Public sheet artifacts contain only our exact matching rows, expected tab/header identities, counts/indices and private-cache hashes. Unexpected row contents remain private. The privacy output scan found no unrelated full rows or other-tab properties.','', 'RECONCILIATION_RESULT.json contains every check. INPUT_BINDINGS.json binds local source receipts, accepted files, reconciliation scripts and private response hashes. EXPECTED_COMPLETED_EIGHT.json preserves the actual completed-eight decision snapshot. Individual JSON readbacks and immutable scoped Git inventories provide checkable evidence. Raw public downloads and raw spreadsheet responses are recoverable under ignored tmp/.','', 'These readbacks establish consistency at their recorded UTC times. They do not re-audit mathematics, strengthen earlier priority conclusions or certify human peer review.'])
 (OUT/'FINDINGS.md').write_text('\n'.join(lines)+'\n')
 with (OUT/'RESEARCH_LOG.md').open('a') as stream:stream.write(f'- {now}: Actual completed-eight readback and offline analysis pass {result["checks"]} checks; privacy output scan passes. Final reconciliation completion estimate: 100%. No external mutation or persistent-goal update occurred.\n')
 files={}
 for path in sorted(OUT.rglob('*')):
  if not path.is_file() or 'tmp' in path.relative_to(OUT).parts or path.name=='FINAL_FREEZE.json':continue
  require(not path.is_symlink(),'Unexpected symlink in final reconciliation')
  data=path.read_bytes();files[path.relative_to(OUT).as_posix()]={'bytes':len(data),'sha256':sha(data)}
 dump(OUT/'FINAL_FREEZE.json',{'frozen_utc':now,'scope':'Eight completed eligible PRs only, publication-safe sheet evidence','status':'PASS','checks':result['checks'],'mandatory_findings':0,'files':files,'excluded':'Ignored tmp/ raw spreadsheet responses/public downloads and this self-referential freeze file','completion_estimate_percent_subtask':100,'persistent_program_goal_modified':False})
 print(json.dumps({'status':'PASS','frozen_files':len(files),'freeze_sha256':sha((OUT/'FINAL_FREEZE.json').read_bytes()),'result_sha256':sha((OUT/'RECONCILIATION_RESULT.json').read_bytes())},indent=2))
if __name__=='__main__':main()

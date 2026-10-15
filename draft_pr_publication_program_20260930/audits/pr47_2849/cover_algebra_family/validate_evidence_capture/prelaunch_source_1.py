#!/usr/bin/env python3
"""Verify existing captured evidence, not rerun mathematical helper tests."""
from pathlib import Path
from datetime import datetime
import hashlib,json
B=Path(__file__).resolve().parent
def bodyok(p,e):
 b=p.read_bytes();assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],str(p)
captures=[]
for cap in sorted(B.rglob('CAPTURE.json')):
 r=json.loads(cap.read_bytes());assert r['completed'] and isinstance(r['actual_child_pid'],int) and r['actual_child_pid']>0
 assert datetime.fromisoformat(r['started_utc'])<=datetime.fromisoformat(r['finished_utc'])
 for key in ['prelaunch','stdout','stderr']:bodyok(Path(r[key]['path']),r[key])
 pre=json.loads(Path(r['prelaunch']['path']).read_bytes());assert pre['argv']==r['argv'] and pre['cwd']==r['cwd']
 assert datetime.fromisoformat(pre['prepared_utc'])<=datetime.fromisoformat(r['started_utc'])
 bodyok(Path(pre['operator']['path']),pre['operator'])
 for pair in pre.get('prelaunch_source_copies',[]):bodyok(Path(pair['copy']['path']),pair['copy']);assert pair['copy']['sha256']==pair['original']['sha256']
 captures.append({'path':str(cap.relative_to(B)),'actual_child_pid':r['actual_child_pid'],'returncode':r['returncode'],'complete_output_bindings_valid':True})
terms={'wrong_square':'incorrect unsquared vanishing asserted for adjoint','false_general_vanishing':'incorrect universal target-premise normal H1 vanishing','null_equals_absent_fallback':'incorrect literal null equals absent default object','primitive_from_cover':'incorrect cover-positive implies same primitive twist positive'}
for mode,term in terms.items():
 text=(B/('own_'+mode+'_capture')/'stderr.bin').read_text();assert 'AssertionError: '+term in text
auth=json.loads((B/'PRIMARY_AUTHENTICATION_RECEIPT.json').read_bytes());original=json.loads((B.parent/'source_snapshot/source_checksums.json').read_bytes())
observed={r['url']:r for r in auth['sources']}
for r in original['sources']:
 a=observed[r['url']];assert a['sha256']==r['sha256'] and a['bytes']==r['bytes']
assert observed[original['original_k3']['url']]['sha256']==original['original_k3']['sha256']
sourcefiles=sorted(p for p in (B.parent/'source_snapshot').rglob('*') if p.is_file())
receipt=json.loads((B/'FULL_READ_AND_PREPARATION_RECEIPT.json').read_bytes());assert len(sourcefiles)==len(receipt['all_science_files'])==16
for p,r in zip(sourcefiles,receipt['all_science_files']):bodyok(p,r)
own=json.loads((B/'own_exact_results.json').read_bytes());assert own['passed']==189 and own['seifert_noncentral_adjoint_H1_real_dimension']==2
native=json.loads((B/'FRESH_NATIVE_SELECTED_RECEIPT.json').read_bytes());assert native['no_actual_report_present'] and native['future_mirror_status']=='PENDING' and not native['transition_or_writes']
out={'completed_capture_count':len(captures),'captures':captures,'all_completed_captures_bound_to_actual_full_outputs':True,'all_negative_controls_failed_for_intended_assertion':True,'all_seven_original_primary_source_hashes_freshly_match':True,'foreign_bodies_retained':False,'audit_verdict':'REPAIR_REQUIRED_EXACT_REMAINING_ROUTE','full_problem_solved':False,'old_PASS_transfer':False}
(B/'EVIDENCE_VALIDATION_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='captures'},indent=2))

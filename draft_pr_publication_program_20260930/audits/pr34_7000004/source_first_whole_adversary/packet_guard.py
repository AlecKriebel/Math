"""Independent complete current-packet provenance/schema/budget guard; no writes."""
from pathlib import Path
import datetime,hashlib,json,sys
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def guard(c,queue):
 ready=load(c/'readiness.json');st=load(c/'current_status.json');context=load(c/'CURRENT_SOURCE_CONTEXT.json');pa=load(c/'CURRENT_QUEUE_PATCH.json')
 p=load(c/'source_record.json');r=load(c/'prior_report.json');orig=load(c/'original_archive/readiness.json');ver=load(c/'original_archive/review/verdict.json')
 assert p['id']==ready['id']==st['id']==context['id']==7000004,'numeric_id'
 assert p['problem_number']==context['problem_number']=='AMR-069-0004','problem_code'
 assert p==load(c/'original_archive/source_record.json') and r==load(c/'original_archive/prior_report.json'),'original_raw_records'
 pair=sha(json.dumps([p,r],sort_keys=True).encode());statement=sha(p['statement'].encode())
 assert ready['review_hash']==orig['review_hash']==context['review_hash']==pair,'source_pair_hash'
 assert ready['statement_hash']==orig['statement_hash']==context['statement_hash']==statement,'statement_hash'
 reviewdoc=sha((c/'original_archive/review/REVIEW.md').read_bytes())
 assert ver['review_sha256']==reviewdoc!=pair,'review_document_distinct_role'
 assert ready['reviewed_artifact_sha256']==sha((c/'RESULT.md').read_bytes()),'operative_result_binding'
 b=ready['budget'];hist=ready['historical_original_attempt_metadata']
 assert b['maximum_substantive_attempts']==5 and b['used_substantive_attempts']==2,'cumulative_budget'
 assert b['original_substantive_attempts']==b['new_substantive_attempts']==1 and b['verification_attempts']==0,'substantive_charge'
 assert b['time_cap_utc'] is None and 'persistent human-authorized' in b['time_scope'],'current_deadline'
 assert 'not exposed' in b['model'] and 'Not independently exposed'==b['reasoning_effort'].split(' in this runtime')[0],'current_model_provenance'
 assert hist['budget']==orig['budget'] and hist['literature_checked_at']==orig['literature_checked_at'],'exact_historical_metadata'
 assert hist['readiness_sha256']==sha((c/'original_archive/readiness.json').read_bytes()),'historical_binding'
 assert context['historical_original_literature_checked_at']==orig['literature_checked_at'],'source_historical_timestamp'
 assert ready['literature_checked_at']==context['current_source_check_checkpoint_utc'],'current_timestamp_consistency'
 assert datetime.datetime.fromisoformat(ready['literature_checked_at'])>datetime.datetime.fromisoformat(orig['literature_checked_at'].replace('Z','+00:00')),'current_timestamp_scope'
 assert ready['queue_outcome_requested']==st['queue_status_proposed']==context['current_disposition_proposed']=='already_solved','credited_disposition'
 assert ready['positive_novelty_claim'] is False and ready['paper_or_new_doi_or_tracker'] is False,'no_novel_publication'
 assert st['earliest_historical_recognition_established'] is False and st['narrower_negative_curvature_target_resolved'] is False,'scope_limitation'
 assert context['narrower_negative_curvature_target_resolved'] is False and context['paper_or_new_doi_or_tracker'] is False,'source_scope_limitation'
 assert st['original_budget']=='1/5' and st['new_substantive_attempts']==1 and st['cumulative_attempts']=='2/5' and st['verification_attempts']==0,'status_budget'
 turn=(c/'turns.jsonl').read_bytes();oldturn=(c/'original_archive/turns.jsonl').read_bytes();a=[json.loads(z) for z in turn.splitlines()]
 assert turn.startswith(oldturn) and len(a)==2 and [z['turn'] for z in a]==[1,2],'original_ledger_prefix'
 assert a[1]['original_charge_checkpoint']=='ROOT_COUNTEREXAMPLE_CHECKPOINT.md' and 'One new substantive' in a[1]['accounting'],'new_route_charge'
 assert a[1]['model']==b['model'] and a[1]['reasoning_effort']==b['reasoning_effort'],'current_ledger_provenance'
 headers=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
 q=queue.read_bytes();lines=q.decode().splitlines(keepends=True)
 assert sha(q)==pa['whole_queue_preimage_sha256'],'actual_queue_preimage'
 assert [z.strip() for z in next(z for z in lines if z.startswith('| Rank |')).split('|')[1:-1]]==headers,'actual_twelve_column_schema'
 assert pa['header_names']==headers and pa['allowed_named_changes']==['Status','Turns','Findings'],'patch_schema'
 matches=[z for z in lines if len(z.split('|'))==14 and z.split('|')[2].strip().split(' / ')[0]=='7000004']
 assert len(matches)==1 and matches[0]==pa['row_before'],'unique_queue_target'
 before=pa['row_before'].split('|');after=pa['row_prospective'].split('|');assert len(after)==14,'prospective_twelve_columns'
 assert after[8].strip()=='already_solved' and after[9].strip()=='2/5','prospective_status_budget'
 assert not after[10].strip() and not after[12].strip(),'blank_chat_doi'
 assert 'verified elementary consequence' in after[11] and 'stationary' in after[11] and 'no paper/newDOI/tracker' in after[11],'findings_attribution'
 assert all(before[i]==after[i] for i in range(14) if i not in [8,9,11]),'only_named_fields_change'
 new=q.replace(pa['row_before'].encode(),pa['row_prospective'].encode())
 assert sha(new)==pa['whole_queue_prospective_sha256'] and new.replace(pa['row_prospective'].encode(),pa['row_before'].encode())==q,'whole_queue_exact_patch'
 return {'source_pair':pair,'review_document':reviewdoc,'statement':statement,'attempts':'2/5','verification_attempts':0,'queue_names':headers}
if __name__=='__main__':
 print(json.dumps(guard(Path(sys.argv[1]),Path(sys.argv[2])),sort_keys=True))

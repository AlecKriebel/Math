from pathlib import Path
import json,gzip,base64,hashlib,datetime,os
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');A=R/'audits';D=A/'root_final_actual_join_overlay01';J=A/'final_reconciliation_join_preparation01'
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda v:json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def pin(p,h=None):
 b=p.read_bytes()
 if h:assert H(b)==h
 return {'path':str(p),'bytes':len(b),'sha256':H(b)}
def obj(p,h=None):pin(p,h);b=p.read_bytes();return json.loads(gzip.decompress(b)if str(p).endswith('.gz')else b)
def save(name,v,compressed=False):
 b=(json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();b=gzip.compress(b,mtime=0)if compressed else b;p=D/name
 with p.open('xb')as f:os.fchmod(f.fileno(),0o600);f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
cp=D/'ROOT_OVERLAY_INPUT_CANDIDATE.json';v=obj(cp,'c770de5e75deaf26ca8ef56adf6ee36fa6feed6702d60df43ab34ac4aceaa5ab')
assert v['material_claim_changes_or_gaps']==[]and v['administrative_state_draft_merge_changes']==[]and v['highest']==1446 and v['numeric_slots']==1438
for k in ['all252_typed_prefix_values_and_formulas_exact','all34_frozen_literal_identities_and_unique_rows_checked','PR1131_literal_DOI_record_unique287_and_native_merge_head_bound','numeric_original_request_and_chronology_checks_passed']:assert v[k]is True
nativep=A/'ROOT_FINAL_OVERLAY_CANDIDATE_STRICT_NATIVE_ACTUAL_NATIVE02.json';n=obj(nativep,'bb5f3f1e0729081170e62a9256d5673a7162b3192add3919a093d45fa595d517');assert n['returncode']==0 and n['error']is None and base64.b64decode(n['stderr_base64'])==b''and n['effective_cwd']==str(R)
summary=json.loads(base64.b64decode(n['stdout_base64']));assert summary['candidate']==pin(cp)and summary['deltas']==[]and summary['administrative_changes']==[]
payload=v['payload']
for rec in payload['completion_outcomes']:pin(Path(rec['receipt']['path']),rec['receipt']['sha256'])
adoption={'kind':'ROOT_ADOPTED_FINAL_JOIN_OVERLAY','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_native_receipts_reviewed':True,'payload_sha256':H(C(payload)),'candidate':pin(cp),'actual_strict_candidate_native':pin(nativep),'actual_full_collection':v['full_native_collection'],'ROOT_read_entire_candidate_and_strict_driver':True,'ROOT_reviewed_all_four_original_indexed_numeric43_requests_and_outcomes':True,'exact_unformatted_FORMULA_and_complete_metadata_agree':True,'current_highest':1446,'material_claim_changes_or_gaps':[],'administrative_changes':[],'publication_receipts_preserve_qualified_science_and_actual_negative_events':True,'no_service_actions':True,'final_independent_review_and_Root_report_adoption_still_required':True,'completion_estimate_percent':98}
ap=save('ROOT_OVERLAY_ADOPTION.json',adoption);overlay={'schema':'root-adopted-final-join-overlay-v1','payload':payload,'root_adoption':ap};op=save('ROOT_ADOPTED_OVERLAY.json',overlay)
p=J/'join_readonly.py';b=p.read_bytes();assert H(b)=='612b8e085f388e133e94a4c87cc3514e69d0f2931cec5999809f80d7ffaf0b1d'
ns={'__file__':str(p),'__name__':'_root_actual_complete_join'};exec(compile(b,str(p),'exec',optimize=0),ns);ns['verify_closed']('620f22164fe099650f31196258b55ab21fc52b8da0c6a8c0912c875fe2816417')
result=ns['apply_overlay'](ns['baseline'](),op)
assert result['final_reconciliation_requirements_satisfied']is True and result['final_reconciliation_complete']is False and result['unresolved_final_requirements']==['Root final report adoption still required']
assert result['unresolved_new_changed_or_gap_claims']==[]and result['pending_family_count']==0 and result['pending_associated_PR_count']==0 and result['uncompleted_new_publication_PRs']==[]
assert len(result['rows'])==1438 and len(result['own_publications'])==14 and result['ledger_rows_observed_dated']==287
expected={'publication_recorded':257,'explicit_negative_status_excluded':987,'documented_priority_scope_or_accounting_hold':18,'documented_nonfull_or_prior_disposition':173,'root_adopted_partial_original_scope':3};assert result['counts']==expected
jp=save('ACTUAL_COMPLETE_EFFECTIVE_JOIN.json.gz',result,True)
summary={k:v for k,v in result.items()if k not in ['rows','pending_family_obligations','own_publications','DOI_to_PR_coverage_families','duplicate_DOI_multi_PR_families']}
sp=save('ACTUAL_COMPLETE_EFFECTIVE_JOIN_SUMMARY.json',summary)
print(json.dumps({'overlay':op,'overlay_adoption':ap,'join':jp,'summary':sp,'counts':result['counts'],'historical_claimed':result['cohorts']['historical_claimed_marker']['count'],'missing_status':result['cohorts']['missing_usable_explicit_QUEUE_status']['count'],'all_requirements_except_final_review_and_report_satisfied':True,'final_reconciliation_complete':False}))

from pathlib import Path
import json,hashlib,os,datetime,base64
R=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');A=R/'audits';P=A/'pr1131_30005455';RT=P/'operations19/runtime'
H=lambda b:hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p,h=None):
 b=p.read_bytes();assert p.is_file()and not any(q.is_symlink()for q in[p,*p.parents])
 if h is not None:assert H(b)==h
 return {'path':str(p),'bytes':len(b),'sha256':H(b)}
def obj(p,h=None):pin(p,h);return json.loads(p.read_bytes())
def save(p,v):
 b=(json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:os.fchmod(f.fileno(),0o600);f.write(b);f.flush();os.fsync(f.fileno())
 return pin(p)
cp=P/'get_only_external_completion_candidate02/ROOT_CANDIDATE_RECEIPT.json'
candidate=obj(cp,'dbd6438050b1def49b13f433bd1eb3d0bc1cab10a14404282ed23759d88d5127')
builder=pin(A/'ROOT_PR1131_EXTERNAL_GET_ONLY_COMPLETION_CANDIDATE_BUILDER02.py','f3adc7b842839e9d64fc2fe1e62f3bb74b5f438584ecb490c6dc269443940148')
review=pin(Path("/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/final_reconciliation_new_independent_adversary01/external1131_mapping_review02/REPORT.json"),"6b7a5597a91ce2800103ae0c15b739411dc65aff6441ff9cfd4ceaf529c23076")
mappingcold=pin(A/'ROOT_PR1131_EXTERNAL_MAPPING02_SEPARATE_COLD_NATIVE01.json','665d0bdd3bb7a1cfc8b3c662d0c9fa3db71897fa125a251325ca1c5772d1e775')
mc=obj(Path(mappingcold['path']));assert mc['returncode']==0 and mc['error']is None and base64.b64decode(mc['stderr_base64'])==b''
mr=json.loads(base64.b64decode(mc['stdout_base64']));assert mr['status']=='CLEAN_EXACT_CANDIDATE02_EXTERNAL_COMPLETION_FIELD_MAPPING'and mr['remaining_substantive_mapping_concerns']==[]and mr['closed_review_namespace_verified']is True
r=candidate['receipt'];assert candidate['ROOT_final_adoption_pending']is True and r['complete']is True and r['ledger_actor_returncode']==1 and r['all_four_actor_actions_succeeded']is False and r['ledger_actor_certification']is False
for e in r['evidence']:assert pin(Path(e['path']),e['sha256'])==e
for k in ['ROOT_external_proof_separate_cold','independent_external_actual_proof','scientific_and_base_whole_review_adoption','actual_source21_joint_adoption','actual_ROOT_execution_adoption','original_failed_ledger_parent','read_only_public_acceptance']:
 e=r[k];assert pin(Path(e['path']),e['sha256'])==e
for e in r['independent_complete_postappend_review'].values():assert pin(Path(e['path']),e['sha256'])==e
assert not(RT/'LEDGER_VERIFIED.json').exists()and not(P/'root_actual21_known23592692_actions01/ledger.parsed.json').exists()
assert r['append_attempts']==1 and r['append_retries']==0 and r['future_service_write_allowance']==0 and all(x is True for x in r['required_native_checks'].values())
adoption={'kind':'ROOT_KNOWN23592692_GET_ONLY_PUBLISHED_AND_RECORDED_EXTERNAL_COMPLETION_ADOPTION','at':now(),'pr':1131,'accepted_external_completion':True,'candidate':pin(cp),'candidate_builder':builder,'candidate_original_native':pin(A/'ROOT_PR1131_EXTERNAL_COMPLETION_CANDIDATE_ACTUAL_NATIVE02.json','c4974c8780347da7c8dd938a37b3763f98840a89a946b8d6c99b377518624990'),'independent_complete_receipt_mapping_review':review,'ROOT_mapping_review_separate_cold':mappingcold,'ROOT_read_complete_candidate_builder_candidate_mapping_review_and_both_proof_reports':True,'ROOT_separate_complete_colds':{'broad':r['ROOT_external_proof_separate_cold'],'closed42':r['independent_complete_postappend_review']['ROOT_separate_cold']},'accepted_facts':'Same one-created record published; original acknowledged single row287 append; full286 typed prefix unchanged; DOI and both complete public files match final reviewed package. Subsequent independent GET-only evidence closes external completion.','actor_failure_preserved':{'ledger_returncode':1,'all_four_actions_succeeded':False,'ledger_certification':False,'LEDGER_VERIFIED_exists':False,'ledger_parsed_exists':False,'original_public_at_age_at_retained_child_finish_seconds':185.366128,'exact_guard_evaluation_timestamp_logged':False,'actual_original_freshness_default_seconds':180},'no_actor_reexecution_or_service_writes':True,'no_retroactive_timestamp_freshness_or_authority_claim':True,'Completion05_permanently_inapplicable':True,'scientific_and_priority_limits_unchanged':True,'final_global_reconciliation_complete':False,'completion_estimate_percent':97}
ap=P/'ROOT_KNOWN23592692_GET_ONLY_PUBLISHED_AND_RECORDED_EXTERNAL_COMPLETION_ADOPTION.json';adoptpin=save(ap,adoption)
r['at']=now();r['ROOT_external_completion_adoption']=adoptpin;r['independent_receipt_mapping_review']=review;r['global_final_reconciliation_pending']=True
rp=R/'PR1131_PUBLICATION_VERIFICATION.json';receiptpin=save(rp,r)
sp=R/'STATE.json';sb=sp.read_bytes();v=json.loads(sb);v['status']='final_full_inventory_and_global_reconciliation_pending';v['completion_estimate_percent']=97;v['estimated_overall_completion_percent']=97
v['active_candidate']=None;v['pending_unallocated_publication']=None;v['ledger_row_count']=287;v['last_live_ledger_rows']=287;v['ledger_verified_at']='2026-10-23T12:40:10.314163+00:00';v['updated_at']=now()
assert all(e['pr']!=1131 for e in v['completed_publications'])
v['completed_publications'].append({'pr':1131,'problem_id':'30005455','doi':r['doi'],'record':r['record'],'ledger_row':287,'merge_commit':r['merge_commit'],'verification':rp.name,'verification_mode':r['publication_verification_mode']})
v['remaining_work']='Final full all-state ascending PR inventory through actual current highest, independent strict indexed43-column ledger refresh, delta classification, complete effective coverage join, fresh adversarial final reconciliation, final report and narrow publication checkpoint.'
v['current_PR1131_actual']={'status':'complete_published_recorded_external_GET_only_adoption_preserved_actor_failure','publication_receipt':receiptpin,'ROOT_adoption':adoptpin,'published':True,'spreadsheet_row':287,'ledger_actor_returncode':1,'ledger_actor_certification':False,'append_retried':False,'service_writes_remaining':0}
v['latest_resumption_evidence']=adoptpin
for e in v.get('reopened_candidates',[]):
 if e['pr']==1131:e.update({'status':'complete_merged_published_DOI_full_public_payloads_and_row287_verified_external_GET_only','not_publication_ready':False,'resolved':True,'scientific_disposition_final':True,'must_resolve_before_final_reconciliation':False,'must_resolve_or_document_before_final_reconciliation':False,'verification':rp.name,'doi':r['doi'],'record':r['record'],'ledger_row':287})
assert len(v['completed_publications'])==14
tmp=R/'STATE.known_external_completion97.tmp'
with tmp.open('x')as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
assert sp.read_bytes()==sb;os.replace(tmp,sp)
lp=R/'research_log.md';assert lp.exists()
with lp.open('a')as f:f.write('\n## '+now()+' — PR1131 external publication and accounting completion (97%)\n\nFourteen new papers are published and fully recorded. Root adopts two independent GET-only reconciliations, two separate complete Root reruns, and an independent complete review of the exact receipt mapping. PR1131 DOI10.5281/zenodo.23592692 resolves to the published record; full public PDF and45-member source ZIP match the final reviewed bytes; unique literal row287 and all286 prior rows are verified. The original ledger actor remains rc1 after its one acknowledged append: the public fact was185.366128s old at the retained child finish, while the actual guard reported Expired/future observation under its180s default; its exact evaluation timestamp was not logged. No retry, old ledger certificate, fourth rc0, timestamp renewal or retrospective freshness/authority claim is created. The former Completion05 is permanently inapplicable. Final inventory through the actual highest PR, strict indexed43-column ledger and global final review remain required.\n');f.flush();os.fsync(f.fileno())
print(json.dumps({'adoption':adoptpin,'receipt':receiptpin,'fully_completed_new_publications':14,'verified_sheet_rows_including_header':287,'completion_percent':97,'actual_service_writes':0,'final_global_reconciliation_complete':False}))

"""No-remote adversarial proposal tests; only disposable copies under this folder."""
from pathlib import Path
import copy,hashlib,importlib.util,json,shutil,tempfile,types
D=Path(__file__).resolve().parent;CASE_ROOT=D.parent
spec=importlib.util.spec_from_file_location('proposed_191_controls',D/'lifecycle_common.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
results={'checks':[],'remote_calls':0,'production_modules_imported':0,'proposal_only':True}
def check(n,x):
 if not x:raise AssertionError(n)
 results['checks'].append({'name':n,'passed':True})
def reject(n,f,part=None):
 try:f()
 except (RuntimeError,FileNotFoundError) as e:check(n,part is None or part in str(e))
 else:raise AssertionError('Expected rejection '+n)
def plain(p):return {k:v for k,v in c.pin(p).items() if k!='git_blob'}
source_before={p.relative_to(CASE_ROOT).as_posix():plain(p) for p in [CASE_ROOT/'CURRENT_PROOF_V4.md',CASE_ROOT/'ROOT_WHOLE_REVIEW_INPUT_01.json',CASE_ROOT/'integration_preparation/NATIVE_TEMPLATE_PENDING_01_MANIFEST.json']}
source_packet={p.name:plain(p) for p in (CASE_ROOT/'publication_package_v1').iterdir() if p.is_file()}
OLD=D.parent/'lifecycle_controls_preparation_01'
oldseal=json.loads((OLD/'FINAL_SEAL.json').read_text());old_before={x['path']:plain(OLD/x['path']) for x in oldseal['manifest']};oldsealpin=plain(OLD/'FINAL_SEAL.json')
spec=importlib.util.spec_from_file_location('frozen_01_controls',OLD/'lifecycle_common.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
OLD2=D.parent/'lifecycle_controls_preparation_02';old2seal=json.loads((OLD2/'FINAL_SEAL.json').read_text());old2pin=plain(OLD2/'FINAL_SEAL.json')
spec=importlib.util.spec_from_file_location('frozen_02_controls',OLD2/'lifecycle_common.py');old2=importlib.util.module_from_spec(spec);spec.loader.exec_module(old2)
OLD3=D.parent/'lifecycle_controls_preparation_03';old3seal=json.loads((OLD3/'FINAL_SEAL.json').read_text());old3pin=plain(OLD3/'FINAL_SEAL.json')
spec=importlib.util.spec_from_file_location('frozen_03_controls',OLD3/'lifecycle_common.py');old3=importlib.util.module_from_spec(spec);spec.loader.exec_module(old3)
OLD4=D.parent/'lifecycle_controls_preparation_04';old4seal=json.loads((OLD4/'FINAL_SEAL.json').read_text());old4pin=plain(OLD4/'FINAL_SEAL.json')
spec=importlib.util.spec_from_file_location('frozen_04_controls',OLD4/'lifecycle_common.py');old4=importlib.util.module_from_spec(spec);spec.loader.exec_module(old4)
# Synthetic authority-schema compatibility only: older validators see the declared06
# factual key names. Their original vulnerable guards remain unmodified.
old4.CASE_FACTUAL_KEYS |= c.CASE_FACTUAL_KEYS
OLD5=D.parent/'lifecycle_controls_preparation_05';old5seal=json.loads((OLD5/'FINAL_SEAL.json').read_text());old5pin=plain(OLD5/'FINAL_SEAL.json')
spec=importlib.util.spec_from_file_location('frozen_05_controls',OLD5/'lifecycle_common.py');old5=importlib.util.module_from_spec(spec);spec.loader.exec_module(old5);old5.CASE_FACTUAL_KEYS |= c.CASE_FACTUAL_KEYS
frozen= json.loads((CASE_ROOT/'ROOT_WHOLE_REVIEW_INPUT_01.json').read_text())
def fixture(F):
 c.A=F;c._helpers=None
 shutil.copytree(CASE_ROOT/'publication_package_v1',F/'publication_package_v9')
 (F/'integration_preparation').mkdir();shutil.copytree(CASE_ROOT/'integration_preparation/native_template_pending_01',F/'integration_preparation/native_template_pending_09')
 nm=json.loads((CASE_ROOT/'integration_preparation/NATIVE_TEMPLATE_PENDING_01_MANIFEST.json').read_text());nm['current_template']='native_template_pending_09';c.write(F/'integration_preparation/NATIVE_TEMPLATE_PENDING_09_MANIFEST.json',nm)
 for n in ['ORIGINAL_FILE_MANIFEST.json','INTAKE_CHECKPOINT_ACCEPTANCE.json','CURRENT_CASE_STATUS.json']:shutil.copyfile(CASE_ROOT/n,F/n)
 shutil.copyfile(CASE_ROOT/'CURRENT_PROOF_V4.md',F/'CURRENT_PROOF_V9.md');c.write(F/'RESEARCH_LOG.md','FIXTURE LOG\n');c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',{'current_template':nm['current_template'],'files':list(nm['files'])})
 for n in ['REVIEW_A.json','REVIEW_B.json','SEAL_A.json','SEAL_B.json','AUTH_A.json','AUTH_B.json','ROOT_WHOLE_REVIEW_INPUT_09.json']:c.write(F/n,{'fixture':'synthetic final review, not actual clearance'})
 c.write(F/'PR_PROPOSAL.json',{'title':'Credited signed-angle research note PR191','body_before_publication':c.CLAIM})
 c.write(F/'TRACKER_PROPOSAL.json',{'original_problem':'Fuchs Conjecture2.6 /5000005','solution_chat_url':'','notes':c.CLAIM})
 def binding(n):return {'path':n,**plain(F/n)}
 reviews=[{'reviewer_id':letter,'disposition':'PASS','authoritative':True,'report':binding('REVIEW_'+letter+'.json'),'seal':binding('SEAL_'+letter+'.json'),'root_authentication':binding('AUTH_'+letter+'.json')} for letter in ['A','B']]
 g={'UTC':c.now(),'schema':'PR191_LIFECYCLE_GATE_V1','status':'READY_FOR_AUTHORIZED_PUBLICATION','PR':191,'original_head':c.HEAD,'qualified_note_route_authorized':True,'historical_priority_clearance':False,'all_required_findings_globally_resolved':True,'whole_package_reviews':reviews,'last_review_required_repairs':0,'package_name':'publication_package_v9','paper_files':{'pdf':'parallel_short_trajectories.pdf','source':'parallel_short_trajectories.tex','support':'verification-package.zip','metadata':'zenodo-deposit.json'},'payloads':{n:plain(F/'publication_package_v9'/n) for n in frozen['package_files']},'current_proof':binding('CURRENT_PROOF_V9.md'),'native_pending_manifest':binding('integration_preparation/NATIVE_TEMPLATE_PENDING_09_MANIFEST.json'),'native_pending_template':nm['current_template'],'native_final_template':'native_template_final_09','native_complete_template':'native_template_complete_09','native_proof_paths':['CANDIDATE.md','PROOF_V4.md'],'native_json_status_paths':sorted(c.JSON_FACTS),'native_text_status_replacements':{'README.md':'PUBLICATION.json contains dated assembly-time publication facts, pending until actual publication and repository acceptance.','review/REVIEW.md':'Those are pending at this dated assembly snapshot.'},'pr_metadata_proposal':binding('PR_PROPOSAL.json'),'tracker_row_proposal':binding('TRACKER_PROPOSAL.json'),'review_input':binding('ROOT_WHOLE_REVIEW_INPUT_09.json'),'public_case_paths':[],'public_case_pins':{}}
 for n in c.CONTROL_FILES:shutil.copyfile(D/n,F/n)
 for n in ['OP_REPORT.json','OP_SEAL.json','OP_AUTH.json']:c.write(F/n,{'SYNTHETIC_FIXTURE':'no actual operational clearance'})
 clearance={'UTC':c.now(),'status':'ROOT_AUTHENTICATED_OPERATIONAL_LIFECYCLE_CLEARANCE','PR':191,'original_head':c.HEAD,'all_required_findings_globally_resolved':True,'outstanding_required_repairs':[],'runtime_pins':{n:plain(F/n) for n in c.CONTROL_FILES},'independent_adversary_review':{'disposition':'PASS','report':binding('OP_REPORT.json'),'seal':binding('OP_SEAL.json'),'root_authentication':binding('OP_AUTH.json')}};c.write(F/c.OP_CLEARANCE,clearance);g['public_case_pins'][c.OP_CLEARANCE]=plain(F/c.OP_CLEARANCE)
 case=c.read(F/'CURRENT_CASE_STATUS.json');case.update(current_proof=g['current_proof']['path'],current_proof_SHA256=g['current_proof']['sha256']);c.write(F/'CURRENT_CASE_STATUS.json',case);c.write(F/c.CASE_PROJECTION,c.case_scientific_projection(case));g['public_case_pins'][c.CASE_PROJECTION]=plain(F/c.CASE_PROJECTION)
 c.write(F/c.CASE_BASELINE,case);c.write(F/c.CASE_LOG_BASELINE,(F/'RESEARCH_LOG.md').read_text())
 for name in [c.CASE_BASELINE,c.CASE_LOG_BASELINE]:g['public_case_pins'][name]=plain(F/name)
 c.write(F/'PINNED_SUPPORT.md','SYNTHETIC approved immutable support\n');g['public_case_pins']['PINNED_SUPPORT.md']=plain(F/'PINNED_SUPPORT.md')
 c.write(F/'ROOT_PUBLICATION_GATE.json',g)
 z={'id':999999,'state':'published','environment':'production','doi':'10.9999/AUDIT-MOCK','doi_url':'https://doi.org/10.9999/AUDIT-MOCK','record_url':'https://zenodo.org/records/999999','verified_utc':c.now(),'receipt_saved':True,'metadata_normalizations':[],'doi_resolution':{'status':'resolved'},'gate_sha256':c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'],'files':[{'name':g['paper_files'][k],'size':g['payloads'][g['paper_files'][k]]['bytes'],'sha256':g['payloads'][g['paper_files'][k]]['sha256']} for k in ['pdf','source','support']]};c.save_published(g,z,'inspect')
 tr={'status':'TRACKER_APPEND_AND_TWO_FRESH_READS_ACCEPTED','DOI':z['doi'],'spreadsheet_id':c.SID,'gid':c.GID,'tab':c.TAB,'range':"'Math Puzzles'!A3:D3",'actual_fresh_reads':2,'gate_sha256':z['gate_sha256']};c.write(F/'TRACKER_ACCEPTANCE.json',tr)
 install_acceptance(F,g,z,tr)
 return g,z,tr,nm
def install_acceptance(F,g,z,tr):
 c.write(F/'ZENODO_STAGE_READBACK.json',{'id':z['id'],'gate_sha256':z['gate_sha256'],'state':'ready_to_publish'});c.save_published(g,z,'inspect');proposal=c.read(F/g['tracker_row_proposal']['path']);row=[proposal['original_problem'],'',z['doi_url'],proposal['notes']];tr.update(UTC=c.now(),row=row,proposal=g['tracker_row_proposal'])
 c.write(F/'lifecycle_private/TRACKER_FOREIGN_BASELINE.json',{'gate_sha256':z['gate_sha256'],'DOI':z['doi'],'spreadsheet_id':c.SID,'gid':c.GID,'tab':c.TAB,'rows':[c.HEADER,['OTHER PRIVATE PROBLEM','','https://doi.org/10.9999/OTHER','private notes']]})
 c.write(F/'sheets_tracking/TARGET_VALIDATION.json',{'spreadsheet_id':c.SID,'gid':c.GID,'tab':c.TAB,'header':c.HEADER,'UTC':c.now()})
 for i in [1,2]:
  c.write(F/f'sheets_tracking/ROW_READBACK_{i}.json',{'UTC':c.now(),'range':tr['range'],'values':[row]})
  c.write(F/f'sheets_tracking/POSTAPPEND_UNIQUENESS_{i}.json',{'UTC':c.now(),'range':tr['range'],'DOI':z['doi'],'own_row':row,'matching_DOI_rows':1,'preexisting_foreign_rows_retained':True})
 tr.update(UTC=c.now(),evidence={n:c.exact_binding('sheets_tracking/'+n) for n in ['TARGET_VALIDATION.json','ROW_READBACK_1.json','ROW_READBACK_2.json','POSTAPPEND_UNIQUENESS_1.json','POSTAPPEND_UNIQUENESS_2.json']},private_foreign_baseline=plain(F/'lifecycle_private/TRACKER_FOREIGN_BASELINE.json'));c.write(F/'TRACKER_ACCEPTANCE.json',tr)
 def tracker(resource,method,params,body=None):
  if resource=='spreadsheet':return {'spreadsheetId':c.SID,'sheets':[{'properties':{'sheetId':c.GID,'title':c.TAB}}]}
  if params['range']=="'Math Puzzles'!A:D":return {'values':[c.HEADER,['OTHER PRIVATE PROBLEM','','https://doi.org/10.9999/OTHER','private notes'],row]}
  return {'values':[row]}
 c._runtime={'inspect':lambda gate:copy.deepcopy(z),'tracker':tracker}
 if not (F/'integration_preparation'/g['native_final_template']).exists():
  c.write(F/'CURRENT_CASE_STATUS.json',c.derive_case_ready(c.read(F/c.CASE_BASELINE),g,z['gate_sha256']));(F/'RESEARCH_LOG.md').write_bytes(c.derive_case_log((F/c.CASE_LOG_BASELINE).read_bytes(),g,z,tr,{},90))

def prog():
 return {'current_PR':191,'fully_completed_count':39,'published_count':23,'last_completed_PR':190,'fully_completed_eligible_PRs':list(range(1,39))+[190],'published_PRs':list(range(1,23))+[190],'dated_eligible_total':99,'active_checkpoint_commit':'STALE','remaining_current_step':'STALE PR190','next_step':'STALE next191','program_snapshot_authority_condition':'STALE authority','last_completed_writer_operation_finished':'OLD WINDOW','read_only_next_case':{'PR':1},'current_operational_lifecycle_audit_active':True,'current_operational_required_repairs':['dated R1','dated R2','dated R3'],'historical_completed_case_records':[{'keep':'exact dated history'}]}

with tempfile.TemporaryDirectory(prefix='selftest_',dir=D) as t:
 F=Path(t);g,z,tr,nm=fixture(F)
 wrong=copy.deepcopy(g);wrong['whole_package_reviews'][1]['reviewer_id']='A';c.write(F/'ROOT_PUBLICATION_GATE.json',wrong);reject('same_reviewer_cannot_supply_two_rounds',c.gate,'Distinct successive')
 wrong=copy.deepcopy(g);wrong['whole_package_reviews']=[wrong['whole_package_reviews'][0]['report'],wrong['whole_package_reviews'][0]['seal']];c.write(F/'ROOT_PUBLICATION_GATE.json',wrong);reject('one_report_plus_one_seal_not_two_rounds',c.gate,'Per-review')
 wrong=copy.deepcopy(g);wrong['whole_package_reviews'][1]={**wrong['whole_package_reviews'][0],'reviewer_id':'B'};c.write(F/'ROOT_PUBLICATION_GATE.json',wrong);reject('relabeling_one_review_evidence_rejected',c.gate,'Distinct per-review evidence')
 c.write(F/'ROOT_PUBLICATION_GATE.json',g)
 mirror='verification_support_v9/paper/parallel_short_trajectories.pdf';c.write(F/mirror,'placeholder');(F/mirror).write_bytes((F/g['package_name']/g['paper_files']['pdf']).read_bytes());g['public_case_pins'][mirror]=plain(F/mirror);c.write(F/'ROOT_PUBLICATION_GATE.json',g);check('exact_reviewed_authored_pdf_mirror_allowed',c.gate()['public_case_pins'][mirror]['sha256']==g['payloads'][g['paper_files']['pdf']]['sha256'])
 p=F/mirror;p.write_bytes(b'UNREVIEWED EXTERNAL BODY');wrong=copy.deepcopy(g);wrong['public_case_pins'][mirror]=plain(p);c.write(F/'ROOT_PUBLICATION_GATE.json',wrong);reject('different_body_mirror_rejected',c.gate,'Unapproved body');p.write_bytes((F/g['package_name']/g['paper_files']['pdf']).read_bytes());c.write(F/'ROOT_PUBLICATION_GATE.json',g)
 # Gate fixtures below use the current gate hash, exactly as actual receipts do.
 z['gate_sha256']=c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'];tr['gate_sha256']=z['gate_sha256'];install_acceptance(F,g,z,tr)
 extra=F/'integration_preparation'/g['native_pending_template']/'UNMANIFESTED.txt';extra.write_text('extra');reject('pending_native_extra_file_rejected',c.gate,'inventory');extra.unlink()
 clearfile=F/c.OP_CLEARANCE;clearbytes=clearfile.read_bytes();clearance=json.loads(clearbytes)
 for label,mutation in [('missing_pin',None),('false_resolved',{'all_required_findings_globally_resolved':False}),('outstanding_repairs',{'outstanding_required_repairs':['R1']}),('stale_runtime',{'runtime_pins':{}}),('nonpass_review',{'independent_adversary_review':{**clearance['independent_adversary_review'],'disposition':'REPAIR_REQUIRED'}})]:
  wrong=copy.deepcopy(g)
  if mutation is None:wrong['public_case_pins'].pop(c.OP_CLEARANCE)
  else:c.write(clearfile,{**clearance,**mutation});wrong['public_case_pins'][c.OP_CLEARANCE]=plain(clearfile)
  c.write(F/'ROOT_PUBLICATION_GATE.json',wrong);reject('operational_clearance_gate_rejects_'+label,c.gate)
  clearfile.write_bytes(clearbytes)
 c.write(F/'ROOT_PUBLICATION_GATE.json',g)
 projection_bytes=(F/c.CASE_PROJECTION).read_bytes();projection=c.read(F/c.CASE_PROJECTION)
 for label,mutate in [('missing',None),('priority_true',lambda j:j['protected_values'].update(priority_clearance=True)),('wrong_head',lambda j:j['protected_values'].update(original_head='0'*40)),('new_protected_key',lambda j:j['protected_values'].update(novelty_certified=True))]:
  wrong=copy.deepcopy(g)
  if mutate is None:wrong['public_case_pins'].pop(c.CASE_PROJECTION)
  else:j=copy.deepcopy(projection);mutate(j);c.write(F/c.CASE_PROJECTION,j);wrong['public_case_pins'][c.CASE_PROJECTION]=plain(F/c.CASE_PROJECTION)
  c.write(F/'ROOT_PUBLICATION_GATE.json',wrong);reject('case_projection_gate_rejects_'+label,c.gate);(F/c.CASE_PROJECTION).write_bytes(projection_bytes)
 c.write(F/'ROOT_PUBLICATION_GATE.json',g)
 check('dynamic_final_package_proof_and_native_versions',c.gate()['package_name']=='publication_package_v9')
 for name,change in [('unready',{'status':'PREPARED'}),('wrong_original_head',{'original_head':'0'*40}),('last_review_repairs',{'last_review_required_repairs':1})]:
  c.write(F/'ROOT_PUBLICATION_GATE.json',{**g,**change});reject('gate_rejects_'+name,c.gate)
 c.write(F/'ROOT_PUBLICATION_GATE.json',g)
 p=F/g['package_name']/g['paper_files']['source'];b=p.read_bytes();p.chmod(0o644);p.write_bytes(b+b'WRONG');reject('gate_rejects_changed_payload',c.gate,'Bound bytes drift');p.write_bytes(b)
 p=F/g['current_proof']['path'];b=p.read_bytes();p.write_bytes(b+b'WRONG');reject('gate_rejects_changed_current_proof',c.gate,'Bound bytes drift');p.write_bytes(b)
 for bad in ['../escape','lifecycle_private/source.pdf','sheets_tracking/PREAPPEND_FRESH_READ.stdout.json','.zenodo-state/state.json']:
  reject('private_or_escaping_path_rejected_'+bad,lambda:c.safe_rel(bad))
 class PRHelper:
  def api(self,n):return {'head':{'sha':'0'*40},'state':'open','merged':False,'draft':True}
 c._helpers=PRHelper();reject('original_head_drift_rejected',c.original_ready,'Original head');c._helpers=None
 j95=c.progress(prog(),g,z,tr,95)
 check('phase95_counts_aliases_and_no_advance',(j95['fully_completed_count'],j95['published_count'],j95['last_completed_PR'],j95['fully_completed_fraction_percent'],j95['next_numeric_intake_cursor'],j95['advance_to_next_PR_authorized_now'])==(39,23,190,39.39,191,False) and 'active_checkpoint_commit' not in j95 and 'PR191' in j95['remaining_current_step'] and 'Actual credited PR191' in j95['program_snapshot_semantics'])
 c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',{'merge_commit':'fixture-merge','PR_merged':True,'every_selected_identity_checked_at_actual_observed_MAIN':True,'original_head':c.HEAD,'UTC':c.now()})
 j100=c.progress(copy.deepcopy(j95),g,z,tr,100)
 check('phase100_counts_unique_and_conditional_next',(j100['fully_completed_count'],j100['published_count'],j100['last_completed_PR'],j100['fully_completed_fraction_percent'],j100['next_numeric_intake_cursor'])==(40,24,191,40.4,191) and j100['conditional_next_numeric_intake_cursor']==192 and j100['next_intake_requires_actual_completion_receipt'] and j100['advance_to_next_PR_authorized_now'] is False and j100['historical_completed_case_records']==j95['historical_completed_case_records'])
 reject('wrong_phase_census_rejected',lambda:c.normalize(prog(),100),'census')
 check('no_window_or_future_self_commit',j100['next_intake_requires_explicit_writer_release'] is False and j100['peer_pause_or_exclusive_writer_window_assumed'] is False and 'active_checkpoint_commit' not in j100 and j100['retired_live_aliases_PR191'][0]['values']['active_checkpoint_commit']=='STALE')
 baseline_case=c.read(F/c.CASE_BASELINE);baseline_log=(F/c.CASE_LOG_BASELINE).read_bytes();ready_case=(F/'CURRENT_CASE_STATUS.json').read_bytes();ready_log=(F/'RESEARCH_LOG.md').read_bytes()
 for name in [c.CASE_BASELINE,c.CASE_LOG_BASELINE]:
  b=(F/name).read_bytes();(F/name).write_bytes(b+b' ');reject('gate_rejects_immutable_baseline_drift_'+name,c.gate,'Bound bytes drift');(F/name).write_bytes(b)
 for label,path,body in [('alias','CURRENT_CASE_STATUS.json',c.encoded({**json.loads(ready_case),'actual_factual_checkpoint_accepted':True})),('log','RESEARCH_LOG.md',ready_log+b'FALSE NEW COMPLETION ENTRY\n')]:
  (F/path).write_bytes(body);reject('ready90_generation_rejects_current_'+label,lambda:c.prepare_native(False),'Source90');check('invalid_ready90_no_native_generation_'+label,not (F/'integration_preparation'/g['native_final_template']).exists());(F/'CURRENT_CASE_STATUS.json').write_bytes(ready_case);(F/'RESEARCH_LOG.md').write_bytes(ready_log)
 saved_pure=(c.read,c.now);no_effect=lambda *a,**kw:(_ for _ in ()).throw(AssertionError('pure function attempted external input'));stamp=c.now();pure_before={**prog(),'last_completed_actual_final_receipt':'audits/pr190_5000007/ROOT_FINAL_FACTUAL_ACCEPTANCE.json','last_completed_DOI':'PR190 PRIOR DOI'};pure_inputs=copy.deepcopy((baseline_case,g,z,tr,pure_before));intake=c.read(F/'INTAKE_CHECKPOINT_ACCEPTANCE.json');c.read=no_effect;c.now=no_effect
 pure_ready=c.derive_case_ready(baseline_case,g,z['gate_sha256']);pure95=c.derive_case_stage(baseline_case,g,z,tr,{'published':stamp},95,z['gate_sha256']);pure100=c.derive_case_stage(baseline_case,g,z,tr,{'published':stamp,'merged':stamp},100,z['gate_sha256']);pureprog95=c.derive_programme_stage(pure_before,g,z,tr,95,stamp,intake,z['gate_sha256']);pureprog100=c.derive_programme_stage(pureprog95,g,z,tr,100,stamp,intake,z['gate_sha256'],'synthetic-accepted-merge');purelog=c.derive_case_log(baseline_log,g,z,tr,{'published':stamp,'merged':stamp},100);c.read,c.now=saved_pure
 check('pure_constructors_require_no_clock_files_process_or_service',pure_ready==json.loads(ready_case) and purelog.startswith(baseline_log+c.ready_case_log_suffix(g['UTC']).encode()))
 check('pure_derivations_leave_all_inputs_unchanged',pure_inputs==(baseline_case,g,z,tr,pure_before))
 check('full_case_historical_baseline_and_protected18_preserved',pure100['historical_case_baseline_PR191']['values']==baseline_case and all(pure100[k]==baseline_case[k] for k in c.CASE_PROTECTED_KEYS))
 check('all_case_whole_review_readiness_aliases_current',all(pure_ready[k] is v for k,v in [('whole_package_reviews_complete',True),('whole_package_review_active',False),('whole_package_reviews_pending',False),('successive_NEW_whole_package_reviews_complete',True),('publication_clearance',True)]))
 check('prior190_receipt_and_completion_facts_explicitly_historical',pureprog100['historical_completion_snapshots_PR191'][-1]['values']['last_completed_DOI']=='PR190 PRIOR DOI' and pureprog100['last_completed_actual_final_receipt']==pure_before['last_completed_actual_final_receipt'])
 check('all_prepared95_100_acceptance_aliases_remain_pending',all(j['actual_factual_checkpoint_accepted'] is False and j['completion_metadata_checkpoint_pending_at_snapshot'] is True and j['next_intake_requires_actual_completion_receipt'] is True and j['next_numeric_intake_cursor']==191 and j['advance_to_next_PR_authorized_now'] is False for j in [pure95,pure100,pureprog95,pureprog100]))
 before={n:plain(F/'integration_preparation'/g['native_pending_template']/n) for n in nm['files']};cur=c.prepare_native(False);T=F/'integration_preparation'/cur['current_template']
 check('native_final_exact50_and_original16',len(cur['files'])==50 and sum(n.startswith('ORIGINAL_SUBMISSION/') for n in cur['files'])==16 and all(plain(T/n)==before[n] for n in before if n.startswith('ORIGINAL_SUBMISSION/')))
 check('native_science_unchanged',all(plain(T/n)==before[n] for n in before if n not in cur['only_declared_factual_paths_changed']))
 incomplete=copy.deepcopy(cur);incomplete['files'].pop('verify.py');c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',incomplete);reject('incomplete_current_native_manifest_rejected',lambda:c.current_native(g,False),'incomplete');c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',cur)
 extra=T/'UNLISTED';extra.write_text('extra');reject('current_native_extra_file_rejected',lambda:c.current_native(g,False),'inventory');extra.unlink()
 for n in c.JSON_FACTS:
  j=c.read(T/n)
  check('native_live_aliases_'+n,all(j.get(k) is expected for k,expected in [('whole_package_reviews_pending',False),('successive_NEW_whole_package_reviews_complete',True),('publication_clearance',True),('publication_and_tracker_actions_not_yet_performed',False)] if k in j))
 check('native_readme_review_pending_sentences_replaced',all(needle not in (T/n).read_text() for n,needle in g['native_text_status_replacements'].items()))
 case95=c.read(F/'CURRENT_CASE_STATUS.json');check('actual_case_ops_aliases_normalized_only_after_fixture_clearance',case95['operational_lifecycle_audit_active'] is False and case95['operational_required_repairs']==[] and case95['operational_clearance_gate_sha256']==z['gate_sha256'])
 check('programme_ops_negatives_retired_and_clean_aliases_bound',j95['current_operational_lifecycle_audit_active'] is False and j95['current_operational_required_repairs']==[] and j95['retired_operational_aliases_PR191'][0]['values']['current_operational_lifecycle_audit_active'] is True)
 check('native_does_not_preclaim_merge',c.read(T/'CURRENT_RESULT.json')['actual_original_PR_merged'] is False and c.read(F/'CURRENT_CASE_STATUS.json')['original_PR_merged'] is False and c.read(F/'CURRENT_CASE_STATUS.json')['first_whole_package_review_active'] is False)
 historical95={n:(T/n).read_bytes() for n in g['native_text_status_replacements']}
 baseline_native=F/'baseline_native';shutil.copytree(T,baseline_native);old.A=F;old.native_status(baseline_native,g,z,tr,True)
 check('baseline01_reproduces_contradictory_current_native_prose',all(c.factual_sentence(z,tr,False) in (baseline_native/n).read_text() and c.factual_sentence(z,tr,True) in (baseline_native/n).read_text() for n in g['native_text_status_replacements']))
 # Exact independent02 R1 reproducer: rehashed current manifest cannot bless science in a factual file.
 cur95=copy.deepcopy(cur);old2.A=F
 n='CURRENT_RESULT.json';original_bytes=(T/n).read_bytes();mutant=json.loads(original_bytes);mutant.update(novelty_clearance=True,historical_priority_clearance=True,positive_result='All imported conjunctions solved; priority certified');c.write(T/n,mutant);bad=copy.deepcopy(cur95);bad['files'][n]=c.pin(T/n);c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',bad)
 old2.current_native(g,False);check('baseline02_reproduces_rehashed_status_science_forgery',True);reject('fixed03_rejects_exact_status_science_forgery',lambda:c.current_native(g,False),'deterministic expected');(T/n).write_bytes(original_bytes);c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',cur95)
 for n in sorted(c.JSON_FACTS):
  original_bytes=(T/n).read_bytes();j=json.loads(original_bytes);j['UNAPPROVED_SCIENTIFIC_PRIORITY_OR_AI_FLAG']=True;c.write(T/n,j);bad=copy.deepcopy(cur95);bad['files'][n]=c.pin(T/n);c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',bad);reject('full_factual_json_unapproved_key_rejected_'+n,lambda:c.current_native(g,False));(T/n).write_bytes(original_bytes)
 c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',cur95)
 for n in ['README.md','review/REVIEW.md','RESEARCH_LOG.md']:
  b=(T/n).read_bytes();(T/n).chmod(0o644);(T/n).write_bytes(b'UNAPPROVED PRIOR HISTORY/SCIENCE/AI CHANGE\n'+b);bad=copy.deepcopy(cur95);bad['files'][n]=c.pin(T/n);c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',bad);reject('full_current_prose_history_mutation_rejected_'+n,lambda:c.current_native(g,False));(T/n).write_bytes(b)
 c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',cur95)
 for value in ['2026-10-15T05:00:00+00:00\nNOVELTY CERTIFIED','2026-99-15T05:00:00+00:00','2026-10-15T05:00:00-07:00',None]:
  bad=copy.deepcopy(cur95);bad['factual_timestamps']['published']=value;c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',bad);reject('native_factual_timestamp_schema_value_'+str(value),lambda:c.current_native(g,False),'timestamp')
 c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',cur95)
 check('pure_native_derivation_exact_every50_file',c.derive_native(g,z,tr,c.pending_native_bytes(g),cur95['factual_timestamps'],False)=={n:(T/n).read_bytes() for n in cur95['files']})
 source95case=(F/'CURRENT_CASE_STATUS.json').read_bytes();source95log=(F/'RESEARCH_LOG.md').read_bytes()
 for label,path,body in [('alias','CURRENT_CASE_STATUS.json',c.encoded({**json.loads(source95case),'factual_MAIN_complete':True})),('log','RESEARCH_LOG.md',source95log+b'FALSE NEW ACCEPTANCE/INTAKE ENTRY\n')]:
  (F/path).write_bytes(body);reject('existing95_retry_rejects_current_'+label,lambda:c.prepare_native(False),'Interrupted existing');reject('native100_prepare_rejects_source95_'+label,lambda:c.prepare_native(True),'Source95');check('invalid_source95_no_complete_generation_'+label,not (F/'integration_preparation'/g['native_complete_template']).exists());(F/'CURRENT_CASE_STATUS.json').write_bytes(source95case);(F/'RESEARCH_LOG.md').write_bytes(source95log)
 a=c.read(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json');a['UTC']=c.now();c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',a)
 cur100=c.prepare_native(True);T100=F/'integration_preparation'/cur100['current_template'];check('postaccepted_merge_native_current_flags_true',c.read(T100/'CURRENT_RESULT.json')['actual_original_PR_merged'] is True and c.read(T100/'PUBLICATION.json')['actual_original_PR_merged'] is True and all(plain(T100/n)==before[n] for n in before if n not in cur100['only_declared_factual_paths_changed']))
 check('fixed02_current_native_prose_only_accepted',all((T100/n).read_text().count(c.factual_sentence(z,tr,True))==1 and c.factual_sentence(z,tr,False) not in (T100/n).read_text() for n in g['native_text_status_replacements']))
 check('immutable95_generation_prose_preserved',all((T/n).read_bytes()==b for n,b in historical95.items()))
 source100case=(F/'CURRENT_CASE_STATUS.json').read_bytes();source100log=(F/'RESEARCH_LOG.md').read_bytes()
 for label,path,body in [('alias','CURRENT_CASE_STATUS.json',c.encoded({**json.loads(source100case),'factual_MAIN_complete':True})),('log','RESEARCH_LOG.md',source100log+b'FALSE NEW ACCEPTANCE/INTAKE ENTRY\n')]:
  (F/path).write_bytes(body);reject('existing100_retry_rejects_current_'+label,lambda:c.prepare_native(True),'Interrupted existing');(F/'CURRENT_CASE_STATUS.json').write_bytes(source100case);(F/'RESEARCH_LOG.md').write_bytes(source100log)

 times=copy.deepcopy(cur100['factual_timestamps']);times['merged']='2000-01-01T00:00:00+00:00';reject('native_timestamp_stage_order_rejected',lambda:c.derive_native(g,z,tr,c.pending_native_bytes(g),times,True),'out of order')
 n='CURRENT_RESULT.json';p=T100/n;b=p.read_bytes();j=json.loads(b);j['historical_priority_clearance']=True;c.write(p,j);bad=copy.deepcopy(cur100);bad['files'][n]=c.pin(p);c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',bad);reject('completed100_rehashed_priority_forgery_rejected',lambda:c.current_native(g,True),'deterministic expected');p.write_bytes(b);c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',cur100)
 check('prepared100_cursor191_and_only_conditional192',j100['next_numeric_intake_cursor']==191 and j100['advance_to_next_PR_authorized_now'] is False and j100['conditional_next_numeric_intake_cursor']==192 and j100['conditional_next_intake_requires_actual_factual_acceptance'])
 old2.read=c.read;old2.A=F;old2.gate=lambda:g;oldj=old2.normalize(prog(),95);check('baseline02_reproduces_premature95_cursor192',oldj['next_numeric_intake_cursor']==192)
 old3.A=F;old3.published_tracked=lambda:(g,z,tr);old3._runtime=c._runtime
 for label,stamp in [('future','2099-01-01T00:00:00+00:00'),('before_evidence','2000-01-01T00:00:00+00:00')]:
  bad=copy.deepcopy(cur95);bad['factual_timestamps']={'published':stamp};bad['UTC']=stamp;expected=c.derive_native(g,z,tr,c.pending_native_bytes(g),bad['factual_timestamps'],False)
  for n,b in expected.items():(T/n).chmod(0o644);(T/n).write_bytes(b)
  bad['files']={n:c.pin(T/n) for n in expected};c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',bad);old3.current_native(g,False);check('baseline03_reproduces_coherent_native_time_'+label,True);reject('native_receipt_clock_evidence_bounds_'+label,lambda:c.current_native(g,False),'interval')
 # Restore immutable95 and current100 states after counterexample copies.
 expected=c.derive_native(g,z,tr,c.pending_native_bytes(g),cur95['factual_timestamps'],False)
 for n,b in expected.items():(T/n).write_bytes(b)
 c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',cur100)
 bad=copy.deepcopy(cur100);bad['factual_timestamps']['merged']=cur95['factual_timestamps']['published'];expected=c.derive_native(g,z,tr,c.pending_native_bytes(g),bad['factual_timestamps'],True)
 for n,b in expected.items():(T100/n).chmod(0o644);(T100/n).write_bytes(b)
 bad['files']={n:c.pin(T100/n) for n in expected};c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',bad);old3.current_native(g,True);check('baseline03_reproduces_merge_time_before_acceptance',True);reject('merged_native_timestamp_binds_actual_merge_acceptance',lambda:c.current_native(g,True),'interval')
 expected=c.derive_native(g,z,tr,c.pending_native_bytes(g),cur100['factual_timestamps'],True)
 for n,b in expected.items():(T100/n).write_bytes(b)
 c.write(F/'integration_preparation/CURRENT_TEMPLATE.json',cur100)
 badz={**z,'verified_utc':'2099-01-01T00:00:00+00:00'};reject('future_publication_observation_rejected',lambda:c.validate_publication(g,badz),'future');badtr={**tr,'UTC':'2099-01-01T00:00:00+00:00'};reject('future_tracker_acceptance_observation_rejected',lambda:c.validate_tracker(g,z,badtr),'future')
 request=c.metadata_request();check('metadata_191_dynamic_actual_DOI_and_credit',request['request']['pr_number']==191 and c.HEAD in request['expected_original_head'] and z['doi_url'] in request['request']['body'] and 'all16' in request['request']['body'].lower() and '5000007' not in request['request']['body'])
 accept={'status':'ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED','PR':191,'original_head':c.HEAD,'gate_sha256':z['gate_sha256'],'request_sha256':c.pin(F/'PR_METADATA_REQUEST.json')['sha256']};c.write(F/'PR_METADATA_ACCEPTANCE.json',accept);p={'title':request['request']['title'],'body':request['request']['body']};c.require_metadata(g,z,tr,p);check('metadata_exact_actual_request_accepted',True)
 reject('metadata_actual_body_mutant_rejected',lambda:c.require_metadata(g,z,tr,{**p,'body':'WRONG CLAIM'}),'Actual PR metadata')
 c.write(F/'PR_METADATA_ACCEPTANCE.json',{**accept,'request_sha256':'0'*64});reject('metadata_receipt_wrong_request_binding_rejected',lambda:c.require_metadata(g,z,tr,p),'acceptance binding');c.write(F/'PR_METADATA_ACCEPTANCE.json',accept)
 c.write(F/'ZENODO_PUBLICATION_READBACK.json',{**z,'files':[]});reject('publication_missing_uploaded_file_pins_rejected',lambda:c.publication(g),'exact uploaded');c.save_published(g,z,'inspect')

# R3 practical provenance and fresh actual observations. All services are injected stubs.
with tempfile.TemporaryDirectory(prefix='fresh_services_',dir=D) as t:
 F=Path(t);g,z,tr,nm=fixture(F);old2.A=F;old2.gate=c.gate;real_services=c._runtime;good_z=copy.deepcopy(z);good_tr=copy.deepcopy(tr)
 forged=copy.deepcopy(z);forged.update(id=191919,doi='10.9999/INVENTED',doi_url='https://doi.org/10.9999/INVENTED',record_url='https://zenodo.org/records/191919');c.save_published(g,forged,'inspect');stage_good=c.read(F/'ZENODO_STAGE_READBACK.json');c.write(F/'ZENODO_STAGE_READBACK.json',{**stage_good,'id':forged['id']})
 old2.publication(g);check('baseline02_reproduces_invented_publication_acceptance',True);reject('fresh_exact_kit_observation_rejects_forged_published_identity',lambda:c.publication(g),'Fresh exact-kit');c.save_published(g,z,'inspect');c.write(F/'ZENODO_STAGE_READBACK.json',stage_good)
 bad=copy.deepcopy(tr);bad['row']=['deliberately false own row'];c.write(F/'TRACKER_ACCEPTANCE.json',bad);old2.published_tracked();check('baseline02_reproduces_false_tracker_row_acceptance',True);reject('fixed03_rejects_false_tracker_row_assertion',c.published_tracked,'Exact tracker');c.write(F/'TRACKER_ACCEPTANCE.json',tr)
 stage=c.read(F/'ZENODO_STAGE_READBACK.json');c.write(F/'ZENODO_STAGE_READBACK.json',{**stage,'id':888});reject('publication_staged_ID_continuity_rejected',lambda:c.publication(g),'continuity');c.write(F/'ZENODO_STAGE_READBACK.json',stage)
 p=F/'ZENODO_PUBLICATION_EVIDENCE.json';b=p.read_bytes();j=json.loads(b);j['published_output']['doi']='10.9999/FALSE';c.write(p,j);reject('publication_exact_kit_output_evidence_disagreement',lambda:c.publication(g),'disagreement');p.write_bytes(b)
 for label,mutate in [('range',lambda j:j.update(range="'Math Puzzles'!A999:D999")),('readcount_bool',lambda j:j.update(actual_fresh_reads=True)),('missing_evidence',lambda j:j.pop('evidence')),('wrong_proposal',lambda j:j.update(proposal={})),('wrong_gate',lambda j:j.update(gate_sha256='0'*64))]:
  bad=copy.deepcopy(tr);mutate(bad);c.write(F/'TRACKER_ACCEPTANCE.json',bad);reject('tracker_consumption_rejects_'+label,c.published_tracked)
 c.write(F/'TRACKER_ACCEPTANCE.json',tr)
 p=F/'sheets_tracking/ROW_READBACK_2.json';b=p.read_bytes();j=json.loads(b);j['values']=[['wrong']];c.write(p,j);reject('tracker_consumption_rejects_changed_readback_pin',c.published_tracked,'evidence');p.write_bytes(b)
 p=F/'sheets_tracking/POSTAPPEND_UNIQUENESS_2.json';b=p.read_bytes();j=json.loads(b);j['matching_DOI_rows']=2;c.write(p,j);bad=copy.deepcopy(tr);bad['evidence']['POSTAPPEND_UNIQUENESS_2.json']=c.exact_binding('sheets_tracking/POSTAPPEND_UNIQUENESS_2.json');c.write(F/'TRACKER_ACCEPTANCE.json',bad);reject('tracker_consumption_rejects_rehashed_duplicate_evidence',c.published_tracked,'uniqueness');p.write_bytes(b);c.write(F/'TRACKER_ACCEPTANCE.json',tr)
 for mode in ['positive','duplicate_first','duplicate_second','foreign_loss','wrong_tab','wrong_header','wrong_own_row','foreign_addition']:
  calls=[];full_count=[0];row=tr['row']
  def service(resource,method,params,body=None):
   calls.append((resource,method,params.get('range')));require_no_write=method=='get';check('fresh_trust_observation_read_only_'+mode+'_'+str(len(calls)),require_no_write)
   if resource=='spreadsheet':return {'spreadsheetId':c.SID,'sheets':[{'properties':{'sheetId':c.GID,'title':'WRONG' if mode=='wrong_tab' else c.TAB}}]}
   if params['range']=="'Math Puzzles'!A:D":
    full_count[0]+=1;rows=[c.HEADER,['OTHER PRIVATE PROBLEM','','https://doi.org/10.9999/OTHER','private notes'],row]
    if mode=='wrong_header':rows[0]=['WRONG']
    if mode=='foreign_loss':rows[1]=['FOREIGN CHANGED']
    if mode=='foreign_addition':rows.append(['NEW FOREIGN','','other','addition'])
    if mode=='duplicate_first' or mode=='duplicate_second' and full_count[0]==2:rows.append(row)
    return {'values':rows}
   return {'values':[['WRONG']] if mode=='wrong_own_row' else [row]}
  c._runtime={**real_services,'tracker':service}
  if mode in ['positive','foreign_addition']:c.published_tracked();check('fresh_two_trust_observations_'+mode,full_count[0]==2)
  else:reject('fresh_tracker_trust_rejects_'+mode,c.published_tracked)
 c._runtime=real_services
 def unresolved(g):raise RuntimeError('SIMULATED fresh publication inspection unresolved')
 c._runtime={**real_services,'inspect':unresolved};reject('unresolved_fresh_publication_cannot_advance',c.published_tracked,'unresolved');c._runtime=real_services
 c._runtime=None;c._helpers=None;reject('default_publication_without_explicit_services_rejected',lambda:c.publication(g),'explicit production');reject('default_GWS_without_explicit_entrypoint_rejected',lambda:c.gws('values','get',{}),'explicit production');reject('default_uploader_without_explicit_entrypoint_rejected',lambda:c.run_zenodo('check'),'explicit production');reject('default_helper_import_without_explicit_entrypoint_rejected',c.helpers,'explicit production');c._runtime=real_services

def verify_seal(folder,seal):return all(plain(folder/x['path'])=={k:x[k] for k in ['bytes','sha256']} and ((folder/x['path']).stat().st_mode & 0o777)==0o444 for x in seal['manifest'])
check('frozen04_all_manifest_members_and_seal_unchanged0444',verify_seal(OLD4,old4seal) and plain(OLD4/'FINAL_SEAL.json')==old4pin)
check('frozen03_all_manifest_members_and_seal_unchanged0444',verify_seal(OLD3,old3seal) and plain(OLD3/'FINAL_SEAL.json')==old3pin)
check('frozen02_all_manifest_members_and_seal_unchanged0444',verify_seal(OLD2,old2seal) and plain(OLD2/'FINAL_SEAL.json')==old2pin)

# Tracker controls: callbacks never invoke GWS. Other rows stay only in memory.
for mode in ['append','existing','concurrent_addition','post_duplicate','second_post_duplicate','post_foreign_loss','post_conflict','unknown_absent','false_duplicate','two_duplicates','wrong_header','wrong_tab','lost_append','bad_row_read']:
 with tempfile.TemporaryDirectory(prefix='tracker_',dir=D) as t:
  F=Path(t);g,z,tr,nm=fixture(F);proposal=c.read(F/'TRACKER_PROPOSAL.json');row=[proposal['original_problem'],'',z['doi_url'],proposal['notes']];calls=[];appends=[];full_reads=[]
  if mode in ['unknown_absent','existing']:c.write(F/'sheets_tracking/APPEND_ATTEMPT_STARTED.json',{'unknown':True})
  def call(resource,method,params,body=None):
   calls.append((resource,method,params.get('range')))
   if resource=='spreadsheet':return {'spreadsheetId':c.SID,'sheets':[{'properties':{'sheetId':c.GID,'title':'WRONG' if mode=='wrong_tab' else c.TAB}}]}
   if method=='append':
    appends.append(body);check('append_is_RAW_and_one_own_row_'+mode,params['valueInputOption']=='RAW' and body['values']==[row])
    if mode=='lost_append':raise RuntimeError('SIMULATED unknown outcome')
    return {'updates':{'updatedRange':"'Math Puzzles'!A3:D3",'updatedRows':1,'updatedColumns':4}}
   if params['range']=="'Math Puzzles'!A1:D1":return {'values':[['WRONG'] if mode=='wrong_header' else c.HEADER]}
   if params['range']=="'Math Puzzles'!A:D":
    full_reads.append(1)
    rows=[c.HEADER,['OTHER PRIVATE PROBLEM','','https://doi.org/10.9999/OTHER','private notes']]
    if mode=='existing' or appends:rows.append(row)
    if appends and mode=='concurrent_addition':rows.append(['NEW FOREIGN','','other','addition'])
    if appends and (mode=='post_duplicate' or mode=='second_post_duplicate' and len(full_reads)==3):rows.append(row)
    if appends and mode=='post_foreign_loss':rows[1]=['CHANGED FOREIGN','','other','changed']
    if appends and mode=='post_conflict':rows[-1]=[row[0],row[1],row[2],'CONFLICT']
    if mode=='false_duplicate':rows.append(['foreign','','otherdoi','mentions '+z['doi']])
    if mode=='two_duplicates':rows.extend([row,row])
    return {'values':rows}
   return {'values':[['WRONG']] if mode=='bad_row_read' else [row]}
  if mode=='post_duplicate':
   old.A=F;old.record_tracker(call);check('baseline01_reproduces_concurrent_duplicate_acceptance',c.read(F/'TRACKER_ACCEPTANCE.json')['actual_fresh_reads']==2);(F/'TRACKER_ACCEPTANCE.json').unlink();(F/'sheets_tracking/APPEND_ATTEMPT_STARTED.json').unlink();appends.clear();calls.clear();full_reads.clear()
  if mode in ['append','existing','concurrent_addition']:
   out=c.record_tracker(call);check('tracker_success_'+mode,out['actual_fresh_reads']==2 and len(appends)==(0 if mode=='existing' else 1) and len([x for x in calls if x[2] and x[2] not in ["'Math Puzzles'!A1:D1","'Math Puzzles'!A:D"]])==2)
  else:
   reject('tracker_rejects_'+mode,lambda:c.record_tracker(call));check('tracker_no_acceptance_'+mode,not (F/'TRACKER_ACCEPTANCE.json').exists())
   check('tracker_no_extra_append_'+mode,len(appends)<= (1 if mode in ['lost_append','bad_row_read','post_duplicate','second_post_duplicate','post_foreign_loss','post_conflict'] else 0))
  if mode=='lost_append':check('unknown_append_marker_written_before_call',(F/'sheets_tracking/APPEND_ATTEMPT_STARTED.json').exists())
  check('other_tracker_rows_never_saved_'+mode,all('OTHER PRIVATE PROBLEM' not in p.read_text() for p in (F/'sheets_tracking').glob('*.json')))

# Exact object/control functions, using immutable tree identity maps.
def bp(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
class Git:
 def __init__(self):
  self.maps={'base':{'foreign/file':('100644','blob','f'*40)},'prepared':{},'actual':{}};self.bodies={};self.posts=[];self.foreign_mutant=False
  self.m=types.SimpleNamespace(m=types.SimpleNamespace(h=types.SimpleNamespace(warm_selected_directories=lambda *x:None)))
 def api(self,n,method=None,body=None):
  if method=='POST':
   self.posts.append(n)
   if n=='git/trees':
    table=dict(self.maps['base'])
    for x in body['tree']:table[x['path']]=('100644','blob',bp(x['content'].encode())['git_blob'])
    if self.foreign_mutant:table['foreign/UNAUTHORIZED']=('100644','blob','e'*40)
    self.maps['new']=table;return {'sha':'new'}
   if n=='git/commits':return {'sha':'commit'}
  if n=='git/commits/fresh':return {'tree':{'sha':'base'}}
  if n=='git/commits/actual':return {'tree':{'sha':'actual'}}
  if n=='git/commits/commit':return {'tree':{'sha':'new'},'parents':[{'sha':'fresh'},{'sha':c.HEAD}]}
  if n=='git/ref/heads/main':return {'object':{'sha':'fresh'}}
  raise RuntimeError('Unexpected mock path '+n)
 def lookup(self,t,n):return self.maps[t].get(n)
 def changed_leaves(self,a,b):return {n for n in set(self.maps[a])|set(self.maps[b]) if self.maps[a].get(n)!=self.maps[b].get(n)}

# Full no-remote lifecycle acceptance plus a concrete stale-MAIN factual retry.
class FullGit:
 def __init__(self,F,g,j95,cur):
  self.F=F;self.g=g;self.main='mainold';self.advance=False;self.ref_reads=0;self.posts=0;self.blobs={};self.maps={};self.commits={};self.m=types.SimpleNamespace(m=types.SimpleNamespace(h=types.SimpleNamespace(warm_selected_directories=lambda *a:None)))
  plan=c.read(F/'FINAL_MAIN_SCOPE.json');content={c.CASE+n:(F/n).read_bytes() for n in plan['case_paths']};content.update({c.NATIVE+n:(F/'integration_preparation'/cur['current_template']/n).read_bytes() for n in cur['files']});content[c.PREFIX+'CURRENT_PROGRESS.json']=(json.dumps(j95)+'\n').encode();content[c.PREFIX+'CURRENT_PROGRESS.md']=b'BEFORE PROGRESS\n'+b'\n'+(j95['UTC']+c.programme_suffix(95)).encode();content[c.PREFIX+'RESEARCH_LOG.md']=b'BEFORE LOG\n'+b'\n'+(j95['UTC']+c.programme_suffix(95)).encode();provenance=c.read(F/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json');qr={x['commit']:x['row'] for x in provenance['rows']};self.original_queue=('HEADER\n'+qr[c.HEAD]+'\nFOREIGN QUEUE ROW EXACT\n').encode();self.base_queue=('HEADER\n'+qr[c.ORIGINAL_BASE]+'\nFOREIGN QUEUE ROW EXACT\n').encode();z=c.read(F/'ZENODO_PUBLICATION_READBACK.json');content['unsolved_math_prioritization/QUEUE.md']=c.queue_update(self.base_queue.decode(),self.original_queue.decode(),self.base_queue.decode(),z['doi'],z['doi_url']).encode()
  table={n:('100644','blob',self.put(b)) for n,b in content.items()};self.maps['original_queue']={'unsolved_math_prioritization/QUEUE.md':('100644','blob',self.put(self.original_queue))};self.maps['base_queue']={'unsolved_math_prioritization/QUEUE.md':('100644','blob',self.put(self.base_queue))};self.maps['pre']={'unsolved_math_prioritization/QUEUE.md':('100644','blob',self.put(self.base_queue)),'draft_pr_publication_program_20260930/CURRENT_PROGRESS.md':('100644','blob',self.put(b'BEFORE PROGRESS\n')),'draft_pr_publication_program_20260930/RESEARCH_LOG.md':('100644','blob',self.put(b'BEFORE LOG\n')),'foreign/base':('100644','blob',self.put(b'foreign before')),c.PREFIX+'CURRENT_PROGRESS.json':('100644','blob',self.put(c.encoded(prog())))};self.maps['merged']={**self.maps['pre'],**table};self.maps['tipold']={**self.maps['merged'],'foreign/descendant':('100644','blob',self.put(b'foreign allowed'))};self.maps['tipnew']={**self.maps['tipold'],'foreign/newer':('100644','blob',self.put(b'foreign newer'))}
  self.commits={c.HEAD:{'tree':{'sha':'original_queue'},'parents':[]},c.ORIGINAL_BASE:{'tree':{'sha':'base_queue'},'parents':[]},'premerge':{'tree':{'sha':'pre'},'parents':[]},'acceptedmerge':{'tree':{'sha':'merged'},'parents':[{'sha':'premerge'},{'sha':c.HEAD}]},'mainold':{'tree':{'sha':'tipold'},'parents':[{'sha':'acceptedmerge'}]},'mainnew':{'tree':{'sha':'tipnew'},'parents':[{'sha':'mainold'}]}}
  selected={n:bp(b) for n,b in content.items()};self.commits['acceptedmerge']['message']=c.operative_message(c.read(F/'ZENODO_PUBLICATION_READBACK.json'),['premerge',c.HEAD],c.selected_digest(selected));c.write(F/'SCOPED_MERGE_PREPARATION.json',{'commit':'acceptedmerge','tree':'merged','parent_tree':'pre','expected_main':'premerge','selected_files':selected,'selected_map_sha256':c.selected_digest(selected),'original_head':c.HEAD,'gate_sha256':c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'],'changed_paths':list(selected)})
 def put(self,b):x=bp(b)['git_blob'];self.blobs[x]=b;return x
 def api(self,n,method=None,body=None):
  if method=='POST':
   self.posts+=1
   if n=='git/blobs':return {'sha':self.put(__import__('base64').b64decode(body['content']))}
   if n=='git/trees':
    name='tree'+str(self.posts);table=dict(self.maps[body['base_tree']])
    for x in body['tree']:table[x['path']]=('100644','blob',self.put(x['content'].encode()) if 'content' in x else x['sha'])
    self.maps[name]=table;return {'sha':name}
   if n=='git/commits':name='candidate'+str(self.posts);self.commits[name]={'tree':{'sha':body['tree']},'parents':[{'sha':x} for x in body['parents']],'message':body['message']};return {'sha':name}
  if n=='git/ref/heads/main':
   self.ref_reads+=1
   if self.advance and self.ref_reads>=2:self.main='mainnew'
   return {'object':{'sha':self.main}}
  if n.startswith('git/commits/'):return self.commits[n.split('/')[-1]]
  if n.startswith('compare/'):return {'status':'ahead'}
  if n=='pulls/191':return {'merged':True,'state':'closed','head':{'sha':c.HEAD},'merge_commit_sha':'acceptedmerge'}
  raise RuntimeError('Unexpected full mock path '+n)
 def lookup(self,t,n):return self.maps[t].get(n)
 def changed_leaves(self,a,b):return {n for n in set(self.maps[a])|set(self.maps[b]) if self.maps[a].get(n)!=self.maps[b].get(n)}
 def body_at(self,n,ref):return self.blobs[self.maps[self.commits[ref]['tree']['sha']][n][2]]
with tempfile.TemporaryDirectory(prefix='full_retry_',dir=D) as t:
 F=Path(t);g,z,tr,nm=fixture(F);cur=c.prepare_native(False);j95=c.progress(prog(),g,z,tr,95)
 for n in c.CONTROL_FILES:shutil.copyfile(D/n,F/n)
 shutil.copyfile(CASE_ROOT/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json',F/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json')
 request=c.metadata_request();c.write(F/'PR_METADATA_ACCEPTANCE.json',{'status':'ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED','PR':191,'original_head':c.HEAD,'gate_sha256':z['gate_sha256'],'request_sha256':c.pin(F/'PR_METADATA_REQUEST.json')['sha256']})
 for n in ['ZENODO_LOCAL_CHECK.json','ZENODO_STAGE_READBACK.json','ZENODO_DRAFT_READBACK.json','ZENODO_POSTPUBLICATION_INSPECTION.json']:c.write(F/n,z)
 original_ready=c.original_ready;c.original_ready=lambda draft=None:{'head':{'sha':c.HEAD},'state':'open','merged':False,'draft':False,'title':request['request']['title'],'body':request['request']['body']};plan=c.final_scope();c.original_ready=original_ready
 h=FullGit(F,g,j95,cur);c._helpers=h
 accepted=c.integration_accept();check('actual_integration_accept_all_native50_and_packet',accepted['every_selected_identity_checked_at_actual_observed_MAIN'] and accepted['original_head']==c.HEAD)
 cur_merge=c.read(F/'SCOPED_MERGE_PREPARATION.json');incomplete=copy.deepcopy(cur_merge);incomplete['selected_files'].pop(c.NATIVE+'verify.py');reject('incomplete_native_merge_map_rejected',lambda:c.require_merge_scope(g,incomplete),'omits reviewed')
 # R1 concrete baseline exploit plus exact-map and current-tree regressions.
 accepted_good=c.read(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json');r_good=copy.deepcopy(cur_merge);main_good=h.main;old.A=F;old._helpers=h
 old3.A=F;old3._helpers=h;old3._runtime=c._runtime;old3.gate=c.gate
 def rebuilt(parent_receipt,name,changes,message=None):
  r=copy.deepcopy(parent_receipt);r.update(commit=name,tree=name+'_tree');h.maps[r['tree']]=dict(h.maps[parent_receipt['tree']])
  for path,b in changes.items():h.maps[r['tree']][path]=('100644','blob',h.put(b));r['selected_files'][path]=bp(b)
  parents=[r['expected_main']]+([c.HEAD] if parent_receipt is r_good else []);r['selected_map_sha256']=c.selected_digest(r['selected_files']);r['changed_paths']=sorted(h.changed_leaves(r['parent_tree'],r['tree']));h.commits[name]={'tree':{'sha':r['tree']},'parents':[{'sha':x} for x in parents],'message':message or c.operative_message(z,parents,r['selected_map_sha256'])};return r
 #05: coherent producer rehashes cannot authorize QUEUE rows or unbounded programme dates.
 old4.A=F;old4._helpers=h;old4._runtime=c._runtime;old4.gate=c.gate
 q='unsolved_math_prioritization/QUEUE.md';good_queue=h.body_at(q,r_good['commit'])
 for label,body in [('foreign',good_queue.replace(b'FOREIGN QUEUE ROW EXACT',b'FOREIGN QUEUE ROW CORRUPTED')),('own_status_effort',good_queue.replace(b' claimed_solved ',b' solved ').replace(b' 2/5 ',b' 5/5 '))]:
  bad=rebuilt(r_good,'bad_queue_'+label,{q:body});c.verify_prepared(h,bad,[bad['expected_main'],c.HEAD]);c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);h.main=bad['commit'];old4.integration_accept();check('baseline04_reproduces_full_queue_acceptance_'+label,c.read(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')['PR_merged']);(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').unlink();reject('full_merge_rederives_queue_'+label,c.integration_accept,'Prepared QUEUE');check('invalid_queue_no_acceptance_'+label,not (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').exists());c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good)
 c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);h.main=main_good
 old5.A=F;old5._helpers=h;old5._runtime=c._runtime;old5.gate=c.gate
 alias_mutations=[('actual_receipt',{'actual_factual_checkpoint_accepted':True}),('receipt_requirement',{'next_intake_requires_actual_completion_receipt':False}),('prior_final_receipt',{'last_completed_actual_final_receipt':'audits/pr191_5000005/ROOT_FINAL_FACTUAL_ACCEPTANCE.json'}),('metadata_pending',{'completion_metadata_checkpoint_pending_at_snapshot':False}),('new_equivalent_alias',{'factual_MAIN_complete':True}),('deleted_alias',None)]
 for label,change in alias_mutations:
  path=c.PREFIX+'CURRENT_PROGRESS.json';j=json.loads(h.body_at(path,r_good['commit']))
  if change is None:j.pop('next_intake_requires_actual_completion_receipt')
  else:j.update(change)
  bad=rebuilt(r_good,'alias95_'+label,{path:c.encoded(j)});c.verify_prepared(h,bad,[bad['expected_main'],c.HEAD]);c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);h.main=bad['commit'];old5.integration_accept();check('baseline05_reproduces95_completion_alias_'+label,True);(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').unlink();reject('exact95_programme_rejects_'+label,c.integration_accept,'Complete programme');check('alias95_has_no_acceptance_'+label,not (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').exists());c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good)
 c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);h.main=main_good
 for label,change in [('new_equivalent_alias',{'factual_MAIN_complete':True}),('inherited_review_alias',{'whole_package_reviews_pending':True}),('actual_receipt',{'actual_factual_checkpoint_accepted':True}),('history_modified',{'historical_case_baseline_PR191':{}}),('protected_proof',{'current_proof_SHA256':'0'*64}),('protected_priority',{'priority_clearance':True})]:
  path=c.CASE+'CURRENT_CASE_STATUS.json';j=json.loads(h.body_at(path,r_good['commit']));j.update(change);bad=rebuilt(r_good,'case95_'+label,{path:c.encoded(j)});c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);h.main=bad['commit'];(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').unlink(missing_ok=True);reject('full95_case_projection_rejects_'+label,c.integration_accept);check('case95_has_no_acceptance_'+label,not (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').exists());c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good)
 for label,body in [('false_suffix',h.body_at(c.CASE+'RESEARCH_LOG.md',r_good['commit'])+b'\n2026-10-15T07:00:00+00:00 - PR191 actual factual MAIN acceptance complete; PR192 intake is already authorized and complete.\n'),('changed_generated_entry',h.body_at(c.CASE+'RESEARCH_LOG.md',r_good['commit']).replace(b'No intake192',b'Authorized completed intake192')),('changed_trusted_prefix',b'CHANGED HISTORY\n'+h.body_at(c.CASE+'RESEARCH_LOG.md',r_good['commit']))]:
  bad=rebuilt(r_good,'log95_'+label,{c.CASE+'RESEARCH_LOG.md':body});c.verify_prepared(h,bad,[bad['expected_main'],c.HEAD]);c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);h.main=bad['commit'];old5.integration_accept();check('baseline05_reproduces95_case_log_'+label,True);(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').unlink();reject('full95_log_projection_rejects_'+label,c.integration_accept,'Complete current case log');check('log95_has_no_acceptance_'+label,not (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').exists());c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good)
 c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);h.main=main_good
 for field in ['UTC','updated_UTC']:
  for label,value in [('future','2099-01-01T00:00:00+00:00'),('predates','2000-01-01T00:00:00+00:00'),('malformed','not-a-timestamp')]:
   path=c.PREFIX+'CURRENT_PROGRESS.json';j=json.loads(h.body_at(path,r_good['commit']));j[field]=value;bad=rebuilt(r_good,'bad95date_'+field+'_'+label,{path:c.encoded(j)});c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);h.main=bad['commit'];old4.integration_accept();check('baseline04_reproduces95_date_'+field+'_'+label,True);(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').unlink();reject('full95_programme_date_rejects_'+field+'_'+label,c.integration_accept);check('invalid95_date_no_acceptance_'+field+'_'+label,not (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').exists());c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good)
 c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);h.main=main_good
 before95=json.loads(h.body_at(c.PREFIX+'CURRENT_PROGRESS.json',r_good['expected_main']));after95=json.loads(h.body_at(c.PREFIX+'CURRENT_PROGRESS.json',r_good['commit']));saved_now=c.now;c.now=lambda:'2030-01-01T00:00:00+00:00';lower95=max(z['verified_utc'],tr['UTC'])
 for label,value in [('lower_equal',lower95),('upper_equal',c.now())]:
  j=c.derive_programme_stage(before95,g,z,tr,95,value,c.read(F/'INTAKE_CHECKPOINT_ACCEPTANCE.json'),z['gate_sha256']);c.validate_programme_stage(before95,j,g,z,tr,95);check('programme95_boundary_'+label,True)
 j=copy.deepcopy(after95);j.update(UTC=c.now(),updated_UTC=lower95);reject('programme95_reversed_field_order',lambda:c.validate_programme_stage(before95,j,g,z,tr,95),'later than updated');c.now=saved_now
 targets={**{'package_'+n:c.CASE+g['package_name']+'/'+n for n in g['payloads']},'case_proof':c.CASE+g['current_proof']['path'],'support':c.CASE+'PINNED_SUPPORT.md','review':c.CASE+g['whole_package_reviews'][0]['report']['path'],'manifest':c.CASE+g['native_pending_manifest']['path'],'root_gate':c.CASE+'ROOT_PUBLICATION_GATE.json','runtime':c.CASE+'lifecycle_common.py','operational':c.CASE+c.OP_CLEARANCE,'case_projection':c.CASE+c.CASE_PROJECTION,'pr_proposal':c.CASE+g['pr_metadata_proposal']['path'],'tracker_proposal':c.CASE+g['tracker_row_proposal']['path']}
 for label,path in targets.items():
  bad=rebuilt(r_good,'trusted_swap_'+label.replace('.','_'),{path:('UNAPPROVED '+label).encode()});c.verify_prepared(h,bad,[bad['expected_main'],c.HEAD]);check('coherent_swap_passes_parent_delta_message_'+label,True);c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);h.main=bad['commit']
  if label in ['case_proof','package_'+g['paper_files']['source']]:old3.integration_accept();check('baseline03_reproduces_full_integration_swap_'+label,c.read(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')['PR_merged'])
  (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').unlink(missing_ok=True);reject('direct_trusted_selected_identity_rejects_'+label,c.integration_accept,'trusted gate/source');check('coherent_swap_has_no_acceptance_'+label,not (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').exists());c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good)
 c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);h.main=main_good
 for label,message in [('prefix','Firstness and novelty certified.\n'+h.commits[r_good['commit']]['message']),('suffix',h.commits[r_good['commit']]['message']+'\nAll imported cases solved and human reviewed.'),('extra_marker',h.commits[r_good['commit']]['message']+'\nPR191 selected-map SHA256: '+r_good['selected_map_sha256'])]:
  bad=rebuilt(r_good,'message_'+label,{},message);c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);h.main=bad['commit']
  if label=='suffix':old3.integration_accept();check('baseline03_reproduces_unsupported_commit_claim_acceptance',True)
  (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').unlink(missing_ok=True);reject('exact_operative_merge_message_rejects_'+label,c.integration_accept,'operative commit message');c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good)
 c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);h.main=main_good
 for label,which,mutate in [('programme_counts','programme',lambda j:j.update(fully_completed_count=40)),('programme_early_cursor','programme',lambda j:j.update(next_numeric_intake_cursor=192,advance_to_next_PR_authorized_now=True)),('case_premature_merge','case',lambda j:j.update(original_PR_merged=True)),('case_priority','case',lambda j:j.update(novelty_clearance=True)),('case_stale_actual_alias','case',lambda j:j.update(actual_Zenodo_published=False))]:
  path=c.PREFIX+'CURRENT_PROGRESS.json' if which=='programme' else c.CASE+'CURRENT_CASE_STATUS.json';j=json.loads(h.body_at(path,r_good['commit']));mutate(j);bad=rebuilt(r_good,'bad95_'+label,{path:c.encoded(j)});c.verify_prepared(h,bad,[bad['expected_main'],c.HEAD]);c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);h.main=bad['commit'];(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').unlink(missing_ok=True);reject('merge95_semantic_stage_rejects_'+label,c.integration_accept);check('bad95_facts_no_acceptance_'+label,not (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').exists());c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good)
 c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);h.main=main_good
 old2.A=F;old2._helpers=h;old2.gate=c.gate
 bad=copy.deepcopy(r_good);bad.update(tree='bad_native_tree',commit='bad_native_merge');h.maps[bad['tree']]=dict(h.maps[r_good['tree']]);nativepath=c.NATIVE+'CURRENT_RESULT.json';j=json.loads(h.blobs[h.maps[r_good['tree']][nativepath][2]]);j.update(novelty_clearance=True,historical_priority_clearance=True,positive_result='unsupported all cases and firstness');body=c.encoded(j)
 pointer=c.CASE+'integration_preparation/CURRENT_TEMPLATE.json';curbad=json.loads(h.body_at(pointer,r_good['commit']));curbad['files']['CURRENT_RESULT.json']=bp(body)
 for path,content in [(nativepath,body),(c.CASE+'integration_preparation/'+g['native_final_template']+'/CURRENT_RESULT.json',body),(pointer,c.encoded(curbad))]:h.maps[bad['tree']][path]=('100644','blob',h.put(content));bad['selected_files'][path]=bp(content)
 bad['selected_map_sha256']=c.selected_digest(bad['selected_files']);h.commits[bad['commit']]={**copy.deepcopy(h.commits[r_good['commit']]),'tree':{'sha':bad['tree']},'message':c.operative_message(z,[bad['expected_main'],c.HEAD],bad['selected_map_sha256'])};c.verify_prepared(h,bad,[bad['expected_main'],c.HEAD]);check('malicious_prepared_native_passes_object_guards',True);h.main=bad['commit'];c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').unlink();reject('integration_accept_independent_native_derivation_rejects_status_science',c.integration_accept);c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good);h.main=main_good

 def descendant(name,parent,path,body):
  tree=name+'_tree';h.maps[tree]=dict(h.maps[h.commits[parent]['tree']['sha']]);h.maps[tree][path]=('100644','blob',h.put(body));h.commits[name]={'tree':{'sha':tree},'parents':[{'sha':parent}]};h.main=name
 bad=copy.deepcopy(r_good);bad['selected_files'].pop(c.CASE+'CURRENT_CASE_STATUS.json');c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);descendant('bad_case','mainold',c.CASE+'CURRENT_CASE_STATUS.json',b'UNEXPECTED CASE MUTATION')
 old.integration_accept();check('baseline01_reproduces_pruned_case_map_acceptance',c.read(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json')['PR_merged'])
 (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').unlink();reject('fixed02_rejects_same_pruned_case_exploit',c.integration_accept);check('pruned_case_exploit_no_acceptance',not (F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json').exists());c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good)
 c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);h.main=main_good
 classes={'case_status':c.CASE+'CURRENT_CASE_STATUS.json','metadata_proposal':c.CASE+g['pr_metadata_proposal']['path'],'tracker_proposal':c.CASE+g['tracker_row_proposal']['path'],'review':c.CASE+g['whole_package_reviews'][0]['report']['path'],'control':c.CASE+'lifecycle_common.py','publication_receipt':c.CASE+'ZENODO_PUBLICATION_READBACK.json','tracker_readback':c.CASE+'sheets_tracking/ROW_READBACK_1.json','original_manifest':c.CASE+'ORIGINAL_FILE_MANIFEST.json','case_native_mirror':c.CASE+'integration_preparation/'+g['native_final_template']+'/verify.py','native_code':c.NATIVE+'verify.py','native_original':c.NATIVE+'ORIGINAL_SUBMISSION/README.md','payload_pdf':c.CASE+g['package_name']+'/'+g['paper_files']['pdf'],'payload_zip':c.CASE+g['package_name']+'/'+g['paper_files']['support'],'programme':c.PREFIX+'CURRENT_PROGRESS.json','queue':'unsolved_math_prioritization/QUEUE.md','scope':c.CASE+'FINAL_MAIN_SCOPE.json','gate':c.CASE+'ROOT_PUBLICATION_GATE.json'}
 # Select actual immutable original filename without assuming its basename.
 classes['native_original']=next(n for n in r_good['selected_files'] if n.startswith(c.NATIVE+'ORIGINAL_SUBMISSION/'))
 for label,path in classes.items():
  bad=copy.deepcopy(r_good);bad['selected_files'].pop(path);reject('exact_map_pruning_rejected_'+label,lambda:c.verify_merge_scope(h,g,bad))
  descendant('drift_'+label,main_good,path,('MUTANT '+label).encode());reject('actual_descendant_drift_rejected_'+label,c.integration_accept,'Selected current MAIN identity');h.main=main_good
 # Even a new prepared commit with a fresh fingerprint cannot omit immutable intended scope.
 bad=copy.deepcopy(r_good);bad['selected_files'].pop(c.CASE+'CURRENT_CASE_STATUS.json');bad['selected_map_sha256']=c.selected_digest(bad['selected_files']);bad['commit']='pruned_fingerprint';bad['changed_paths']=list(bad['selected_files']);h.commits[bad['commit']]={**copy.deepcopy(h.commits[r_good['commit']]),'message':c.operative_message(z,[bad['expected_main'],c.HEAD],bad['selected_map_sha256'])}
 reject('refingerprinted_pruned_scope_rejected',lambda:c.verify_merge_scope(h,g,bad))
 # Isolate exact immutable-scope protection: omitted path is already unchanged in true parent,
 # so valid fingerprint and exact actual delta independently pass before scope rejection.
 path=c.CASE+'CURRENT_CASE_STATUS.json';h.maps['case_already_present']={**h.maps['pre'],path:h.maps['merged'][path]};h.commits['case_parent']={'tree':{'sha':'case_already_present'},'parents':[]};bad['expected_main']='case_parent';bad['parent_tree']='case_already_present';h.commits['pruned_fingerprint']['parents']=[{'sha':'case_parent'},{'sha':c.HEAD}]
 c.verify_prepared(h,bad,[bad['expected_main'],c.HEAD]);check('refingerprinted_pruning_passes_true_parent_and_delta_before_exact_scope',True);reject('immutable_exact_scope_rejects_rebound_pruned_map',lambda:c.verify_merge_scope(h,g,bad),'Exact immutable selected')

 bad=copy.deepcopy(r_good);bad['selected_files']['foreign/extra']=bp(b'extra');reject('extra_selected_path_rejected',lambda:c.verify_merge_scope(h,g,bad))
 bad=copy.deepcopy(r_good);bad['parent_tree']=bad['tree'];bad['changed_paths']=[];old.verify_prepared(h,bad,[bad['expected_main'],c.HEAD]);check('baseline01_reproduces_forged_parent_tree',True);reject('actual_parent_tree_binding_rejects_forgery',lambda:c.verify_merge_scope(h,g,bad),'actual first parent')
 bad=copy.deepcopy(r_good);bad['changed_paths']=[];reject('exact_actual_delta_rejects_receipt_omission',lambda:c.verify_merge_scope(h,g,bad),'Full-tree foreign')
 bad=copy.deepcopy(r_good);tree='foreign_bad_merge_tree';h.maps[tree]=dict(h.maps['merged']);h.maps[tree]['foreign/base']=('100644','blob',h.put(b'UNAUTHORIZED FOREIGN CHANGE'));bad.update(tree=tree,commit='foreign_bad_merge',parent_tree=tree,changed_paths=[]);h.commits[bad['commit']]={**copy.deepcopy(h.commits[r_good['commit']]),'tree':{'sha':tree}}
 old.verify_prepared(h,bad,[bad['expected_main'],c.HEAD]);check('baseline01_reproduces_foreign_scope_parent_forgery',True);reject('true_parent_rejects_foreign_scope_forgery',lambda:c.verify_merge_scope(h,g,bad),'actual first parent');bad['parent_tree']='pre';bad['changed_paths']=list(r_good['selected_files']);reject('full_delta_rejects_new_foreign_change',lambda:c.verify_merge_scope(h,g,bad),'Full-tree foreign')
 bad=copy.deepcopy(r_good);bad['original_head']='0'*40;reject('prepared_original_head_binding_rejects_forgery',lambda:c.verify_merge_scope(h,g,bad),'head/gate');bad=copy.deepcopy(r_good);bad['gate_sha256']='0'*64;reject('prepared_gate_binding_rejects_forgery',lambda:c.verify_merge_scope(h,g,bad),'head/gate')
 scope_bytes=(F/'FINAL_MAIN_SCOPE.json').read_bytes();c.write(F/'FINAL_MAIN_SCOPE.json',{**plan,'case_paths':[]});reject('local_scope_drift_rejected',lambda:c.verify_merge_scope(h,g,r_good),'scope bytes');(F/'FINAL_MAIN_SCOPE.json').write_bytes(scope_bytes)
 bad=copy.deepcopy(r_good);bad['selected_files'].pop(c.CASE+g['pr_metadata_proposal']['path']);c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);reject('factual_prepare_revalidates_original_merged_map',lambda:c.factual_prepare('factual_preparation_pruned'));check('bad_merge_map_rejected_before_native_complete_or_workflow',not (F/'integration_preparation'/g['native_complete_template']).exists() and not (F/'WORKFLOW_COMPLETION.json').exists());c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good)
 plan=c.read(F/'FINAL_MAIN_SCOPE.json')
 bad=rebuilt(r_good,'bad_original_for_factual',{c.CASE+g['package_name']+'/'+g['paper_files']['source']:b'UNAPPROVED ORIGINAL SCIENCE'});c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);a=copy.deepcopy(accepted_good);a.update(merge_commit=bad['commit'],merge_tree=bad['tree'],selected_map_sha256=bad['selected_map_sha256']);c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',a);h.main=bad['commit'];reject('factual_prepare_rechecks_direct_trusted_original_science',lambda:c.factual_prepare('factual_preparation_bad_original'),'trusted gate/source');c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good);h.main=main_good
 gatehash=c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'];h.advance=True;h.ref_reads=0
 reject('full_factual_prepare_detects_MAIN_advance',lambda:c.factual_prepare('factual_preparation_first'),'MAIN advanced');first=c.read(F/'FINAL_FACTUAL_PREPARATION.json');nativefirst=c.read(F/'integration_preparation/CURRENT_TEMPLATE.json');check('first_stale_preparation_preserved_before_retry',(F/'integration_preparation/factual_preparation_first/CURRENT_PROGRESS.json').is_file())
 h.advance=False;h.ref_reads=0;second=c.factual_prepare('factual_preparation_second')
 check('fresh_retry_reuses_exact_native_complete_generation',c.read(F/'integration_preparation/CURRENT_TEMPLATE.json')==nativefirst and first['commit']!=second['commit'])
 history=F/'integration_preparation/receipt_history'/('FINAL_FACTUAL_PREPARATION_'+first['commit']+'.json');check('fresh_retry_archives_immutable_first_receipt',c.read(history)==first and (history.stat().st_mode & 0o777)==0o444)
 check('fresh_retry_does_not_rewrite_gate',c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256']==gatehash)
 h.main=second['commit'];out=c.factual_accept();check('actual_factual_accept_combined_overrides_and_all_selected',out['every_selected_identity_checked_at_actual_observed_MAIN'] and out['fully_completed_count']==40 and out['published_count']==24);check('only_actual_factual_receipt_authorizes192',out['subsequent_status_only_intake_authorized'] and out['next_numeric_intake_cursor_authorized_after_this_acceptance']==192 and out['live_programme_cursor_update_requires_next_own_checkpoint'])
 good_final=copy.deepcopy(out);old3.A=F;old3._helpers=h;old3._runtime=c._runtime;old3.gate=c.gate
 old5.A=F;old5._helpers=h;old5._runtime=c._runtime;old5.gate=c.gate
 for label,change in alias_mutations:
  path=c.PREFIX+'CURRENT_PROGRESS.json';j=json.loads(h.body_at(path,second['commit']))
  if change is None:j.pop('next_intake_requires_actual_completion_receipt')
  else:j.update(change)
  bad=rebuilt(second,'alias100_'+label,{path:c.encoded(j)});c.verify_prepared(h,bad,[bad['expected_main']]);c.write(F/'FINAL_FACTUAL_PREPARATION.json',bad);h.main=bad['commit'];(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink(missing_ok=True);old5.factual_accept();check('baseline05_reproduces100_completion_alias_'+label,True);(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink();reject('exact100_programme_rejects_'+label,c.factual_accept,'Complete programme');check('alias100_has_no_acceptance_'+label,not (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').exists())
 for label,change in [('new_equivalent_alias',{'factual_MAIN_complete':True}),('inherited_review_alias',{'whole_package_reviews_pending':True}),('actual_receipt',{'actual_factual_checkpoint_accepted':True}),('history_modified',{'historical_case_baseline_PR191':{}}),('protected_proof',{'current_proof_SHA256':'0'*64}),('protected_priority',{'priority_clearance':True})]:
  path=c.CASE+'CURRENT_CASE_STATUS.json';j=json.loads(h.body_at(path,second['commit']));j.update(change);bad=rebuilt(second,'case100_'+label,{path:c.encoded(j)});c.write(F/'FINAL_FACTUAL_PREPARATION.json',bad);h.main=bad['commit'];(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink(missing_ok=True);reject('full100_case_projection_rejects_'+label,c.factual_accept);check('case100_has_no_acceptance_'+label,not (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').exists())
 for label,body in [('false_suffix',h.body_at(c.CASE+'RESEARCH_LOG.md',second['commit'])+b'\n2026-10-15T07:00:00+00:00 - PR191 actual factual MAIN acceptance complete; PR192 intake is already authorized and complete.\n'),('changed_generated_entry',h.body_at(c.CASE+'RESEARCH_LOG.md',second['commit']).replace(b'No intake192',b'Authorized completed intake192')),('changed_trusted_prefix',b'CHANGED HISTORY\n'+h.body_at(c.CASE+'RESEARCH_LOG.md',second['commit']))]:
  bad=rebuilt(second,'log100_'+label,{c.CASE+'RESEARCH_LOG.md':body});c.verify_prepared(h,bad,[bad['expected_main']]);c.write(F/'FINAL_FACTUAL_PREPARATION.json',bad);h.main=bad['commit'];(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink(missing_ok=True);old5.factual_accept();check('baseline05_reproduces100_case_log_'+label,True);(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink();reject('full100_log_projection_rejects_'+label,c.factual_accept,'Complete current case log');check('log100_has_no_acceptance_'+label,not (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').exists())
 c.write(F/'FINAL_FACTUAL_PREPARATION.json',second);h.main=second['commit'];c.write(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json',good_final)
 # Factual consumption independently revalidates the original95 current records.
 for label,path,body in [('alias',c.PREFIX+'CURRENT_PROGRESS.json',c.encoded({**json.loads(h.body_at(c.PREFIX+'CURRENT_PROGRESS.json',r_good['commit'])),'actual_factual_checkpoint_accepted':True})),('log',c.CASE+'RESEARCH_LOG.md',h.body_at(c.CASE+'RESEARCH_LOG.md',r_good['commit'])+b'FALSE CURRENT ACCEPTANCE/INTAKE\n')]:
  bad=rebuilt(r_good,'bad_original95_'+label,{path:body});c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);a=copy.deepcopy(accepted_good);a.update(merge_commit=bad['commit'],merge_tree=bad['tree'],selected_map_sha256=bad['selected_map_sha256']);c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',a);h.main=bad['commit'];reject('factual_prepare_rechecks_full_original95_'+label,lambda:c.factual_prepare('factual_preparation_reject_original95_'+label));c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good);h.main=second['commit'];(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink(missing_ok=True);reject('factual_accept_rechecks_full_original95_'+label,c.factual_accept);check('invalid_original95_no_final_authority_'+label,not (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').exists())
 c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);c.write(F/'ROOT_ACTUAL_MERGE_ACCEPTANCE.json',accepted_good);c.write(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json',good_final)
 old4.A=F;old4._helpers=h;old4._runtime=c._runtime;old4.gate=c.gate
 for field in ['UTC','updated_UTC']:
  for label,value in [('future','2099-01-01T00:00:00+00:00'),('predates','2000-01-01T00:00:00+00:00'),('malformed','not-a-timestamp')]:
   path=c.PREFIX+'CURRENT_PROGRESS.json';j=json.loads(h.body_at(path,second['commit']));j[field]=value;bad=rebuilt(second,'bad100date_'+field+'_'+label,{path:c.encoded(j)});c.write(F/'FINAL_FACTUAL_PREPARATION.json',bad);h.main=bad['commit'];(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink(missing_ok=True);old4.factual_accept();check('baseline04_reproduces100_date_'+field+'_'+label,True);(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink();reject('full100_programme_date_rejects_'+field+'_'+label,c.factual_accept);check('invalid100_date_no_acceptance_'+field+'_'+label,not (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').exists())
 c.write(F/'FINAL_FACTUAL_PREPARATION.json',second);h.main=second['commit'];c.write(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json',good_final)
 before100=json.loads(h.body_at(c.PREFIX+'CURRENT_PROGRESS.json',second['expected_main']));after100=json.loads(h.body_at(c.PREFIX+'CURRENT_PROGRESS.json',second['commit']));saved_now=c.now;saved_services=c._runtime;c.now=lambda:'2030-01-01T00:00:00+00:00';lower100=max(z['verified_utc'],tr['UTC'],accepted_good['UTC'])
 for label,value in [('lower_equal',lower100),('upper_equal',c.now())]:
  j=c.derive_programme_stage(before100,g,z,tr,100,value,c.read(F/'INTAKE_CHECKPOINT_ACCEPTANCE.json'),z['gate_sha256'],accepted_good['merge_commit']);c.validate_programme_stage(before100,j,g,z,tr,100,accepted_good['merge_commit']);check('programme100_boundary_'+label,True)
 j=copy.deepcopy(after100);j.update(UTC=c.now(),updated_UTC=lower100);reject('programme100_reversed_field_order',lambda:c.validate_programme_stage(before100,j,g,z,tr,100,accepted_good['merge_commit']),'later than updated')
 j=copy.deepcopy(after100);j.update(UTC=tr['UTC'],updated_UTC=tr['UTC']);reject('programme100_actual_merge_lower_bound',lambda:c.validate_programme_stage(before100,j,g,z,tr,100,accepted_good['merge_commit']),'interval')
 # No age expiry: old exact native/postimage bytes remain valid when the observation clock advances.
 c._runtime={**saved_services,'inspect':lambda gate:{**copy.deepcopy(z),'verified_utc':c.now()}};c.factual_accept();check('old_immutable_generation_and_postimage_have_no_recency_expiry',c.read(F/'integration_preparation/CURRENT_TEMPLATE.json')==nativefirst);c.now=saved_now;c._runtime=saved_services;c.write(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json',good_final)

 for label,which,mutate in [('counts','programme',lambda j:j.update(fully_completed_count=39,published_count=23)),('cursor','programme',lambda j:j.update(next_numeric_intake_cursor=192,advance_to_next_PR_authorized_now=True)),('membership','programme',lambda j:j['published_PRs'].pop()),('case95','case',lambda j:j.update(case_percent=95,original_PR_merged=False,PR_closed=False)),('case_priority','case',lambda j:j.update(priority_clearance=True)),('workflow','workflow',lambda j:j.update(status='NOT_COMPLETE')),('workflow_extra_claim','workflow',lambda j:j.update(novelty_certified=True))]:
  path={'programme':c.PREFIX+'CURRENT_PROGRESS.json','case':c.CASE+'CURRENT_CASE_STATUS.json','workflow':c.CASE+'WORKFLOW_COMPLETION.json'}[which];j=json.loads(h.body_at(path,second['commit']));mutate(j);bad=rebuilt(second,'bad100_'+label,{path:c.encoded(j)});c.verify_prepared(h,bad,[bad['expected_main']]);c.write(F/'FINAL_FACTUAL_PREPARATION.json',bad);h.main=bad['commit'];(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink(missing_ok=True)
  if label=='counts':old3.factual_accept();check('baseline03_reproduces_full_factual_invalid_postimage_authority',c.read(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json')['fully_completed_count']==40);(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink()
  reject('factual100_semantic_stage_rejects_'+label,c.factual_accept);check('invalid100_postimage_no_acceptance_'+label,not (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').exists())
 c.write(F/'FINAL_FACTUAL_PREPARATION.json',second);h.main=second['commit'];c.write(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json',good_final)
 # Factual commit message and native companion metadata are independently exact.
 bad=rebuilt(second,'bad_factual_message',{},h.commits[second['commit']]['message']+'\nPriority and novelty certified.');c.write(F/'FINAL_FACTUAL_PREPARATION.json',bad);h.main=bad['commit'];reject('factual_message_extra_scientific_claim_rejected',c.factual_accept,'operative commit message');c.write(F/'FINAL_FACTUAL_PREPARATION.json',second);h.main=second['commit']
 path=c.CASE+'integration_preparation/'+g['native_complete_template']+'_MANIFEST.json';j=json.loads(h.body_at(path,second['commit']));j['unsupported_science_claim']=True;bad=rebuilt(second,'bad_companion',{path:c.encoded(j)});c.write(F/'FINAL_FACTUAL_PREPARATION.json',bad);h.main=bad['commit'];reject('native_companion_producer_rehash_rejected',c.factual_accept,'companion manifest');c.write(F/'FINAL_FACTUAL_PREPARATION.json',second);h.main=second['commit']
 badfact=copy.deepcopy(second);badfact.update(commit='bad_factual_native',tree='bad_factual_native_tree');h.maps[badfact['tree']]=dict(h.maps[second['tree']]);pointer=c.CASE+'integration_preparation/CURRENT_TEMPLATE.json';badcur=json.loads(h.body_at(pointer,second['commit']));nativepath=c.NATIVE+'CURRENT_RESULT.json';j=json.loads(h.body_at(nativepath,second['commit']));j['historical_priority_clearance']=True;body=c.encoded(j);badcur['files']['CURRENT_RESULT.json']=bp(body)
 for path,content in [(nativepath,body),(c.CASE+'integration_preparation/'+g['native_complete_template']+'/CURRENT_RESULT.json',body),(pointer,c.encoded(badcur))]:h.maps[badfact['tree']][path]=('100644','blob',h.put(content));badfact['selected_files'][path]=bp(content)
 badfact['selected_map_sha256']=c.selected_digest(badfact['selected_files']);h.commits[badfact['commit']]={**copy.deepcopy(h.commits[second['commit']]),'tree':{'sha':badfact['tree']},'message':c.operative_message(z,[badfact['expected_main']],badfact['selected_map_sha256'])};c.verify_prepared(h,badfact,[badfact['expected_main']]);check('malicious_factual_native_passes_true_parent_full_delta_and_fingerprint',True);c.write(F/'FINAL_FACTUAL_PREPARATION.json',badfact);h.main=badfact['commit'];reject('factual_accept_rechecks_deterministic_native_derivation',c.factual_accept,'deterministic expected');c.write(F/'FINAL_FACTUAL_PREPARATION.json',second);h.main=second['commit']
 # Merged-only metadata omission after factual overlay is the adversary's second exploit.
 (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink();bad=copy.deepcopy(r_good);path=c.CASE+g['pr_metadata_proposal']['path'];bad['selected_files'].pop(path);c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);descendant('bad_merged_only',second['commit'],path,b'CORRUPT MERGED-ONLY PROPOSAL')
 old.factual_accept();check('baseline01_reproduces_factual_merged_only_pruning_acceptance',c.read(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json')['fully_completed_count']==40);(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink();reject('fixed02_rejects_same_merged_only_factual_exploit',c.factual_accept);check('factual_pruned_merged_map_has_no_acceptance',not (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').exists());c.write(F/'SCOPED_MERGE_PREPARATION.json',r_good);h.main=second['commit']
 bad=copy.deepcopy(second);bad['selected_files'].pop(c.CASE+'WORKFLOW_COMPLETION.json');c.write(F/'FINAL_FACTUAL_PREPARATION.json',bad);reject('factual_postimage_map_pruning_rejected',c.factual_accept);c.write(F/'FINAL_FACTUAL_PREPARATION.json',second)
 tree='mutant';h.maps[tree]=dict(h.maps[second['tree']]);h.maps[tree][c.NATIVE+'verify.py']=('100644','blob',h.put(b'WRONG SCIENCE'));h.commits['descendant_mutant']={'tree':{'sha':tree},'parents':[{'sha':second['commit']}]};h.main='descendant_mutant';reject('actual_factual_accept_rejects_later_native_mutant',c.factual_accept,'Selected current MAIN identity')
 check('failed_factual_accept_has_no_receipt',not (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').exists())
with tempfile.TemporaryDirectory(prefix='queue_whole_flow_',dir=D) as t:
 F=Path(t);g,z,tr,nm=fixture(F);cur=c.prepare_native(False);j95=c.progress(prog(),g,z,tr,95)
 shutil.copyfile(CASE_ROOT/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json',F/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json');request=c.metadata_request();c.write(F/'PR_METADATA_ACCEPTANCE.json',{'status':'ACTUAL_ORIGINAL_HEAD_METADATA_AND_READY_STATE_ACCEPTED','PR':191,'original_head':c.HEAD,'gate_sha256':z['gate_sha256'],'request_sha256':c.pin(F/'PR_METADATA_REQUEST.json')['sha256']})
 for n in ['ZENODO_LOCAL_CHECK.json','ZENODO_STAGE_READBACK.json','ZENODO_DRAFT_READBACK.json','ZENODO_POSTPUBLICATION_INSPECTION.json']:c.write(F/n,z)
 saved_ready=c.original_ready;c.original_ready=lambda draft=None:{'head':{'sha':c.HEAD},'state':'open','merged':False,'draft':False,'title':request['request']['title'],'body':request['request']['body']};c.final_scope();c.original_ready=saved_ready;h=FullGit(F,g,j95,cur);c._helpers=h;old4.A=F;old4._helpers=h;old4._runtime=c._runtime;old4.gate=c.gate
 r=c.read(F/'SCOPED_MERGE_PREPARATION.json');q='unsolved_math_prioritization/QUEUE.md';bad=copy.deepcopy(r);bad.update(commit='corrupt_original_queue',tree='corrupt_original_queue_tree');h.maps[bad['tree']]=dict(h.maps[r['tree']]);body=h.body_at(q,r['commit']).replace(b'FOREIGN QUEUE ROW EXACT',b'FOREIGN QUEUE ROW CORRUPTED');h.maps[bad['tree']][q]=('100644','blob',h.put(body));bad['selected_files'][q]=bp(body);bad['selected_map_sha256']=c.selected_digest(bad['selected_files']);bad['changed_paths']=sorted(h.changed_leaves(bad['parent_tree'],bad['tree']));h.commits[bad['commit']]={'tree':{'sha':bad['tree']},'parents':[{'sha':bad['expected_main']},{'sha':c.HEAD}],'message':c.operative_message(z,[bad['expected_main'],c.HEAD],bad['selected_map_sha256'])};h.main=bad['commit'];c.write(F/'SCOPED_MERGE_PREPARATION.json',bad);old4.integration_accept()
 reject('factual_prepare_rederives_original_queue_before_new_generation',lambda:c.factual_prepare('factual_preparation_reject_corrupt_queue'),'Prepared QUEUE');check('corrupt_queue_stops_before_complete_generation',not (F/'integration_preparation'/g['native_complete_template']).exists())
 # Isolate the retained queue defect across the06 authority schema: use honest06
 # producers only for unrelated current records; old04 acceptance remains unchanged.
 saved_old_producers=(old4.progress,old4.prepare_native,old4.now,c.now);fixed=c.now();old4.progress=c.progress;old4.prepare_native=c.prepare_native;old4.now=lambda:fixed;c.now=lambda:fixed
 original_fact=old4.factual_prepare('factual_preparation_old04_corrupt_queue');old4.progress,old4.prepare_native,old4.now,c.now=saved_old_producers;h.main=original_fact['commit'];old4.factual_accept();check('baseline04_queue_corruption_survives_whole_factual_flow',c.read(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json')['fully_completed_count']==40);(F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').unlink();reject('factual_accept_rederives_original_queue_after_old04_whole_flow',c.factual_accept,'Prepared QUEUE');check('corrupt_queue_no_final_authority',not (F/'ROOT_FINAL_FACTUAL_ACCEPTANCE.json').exists())

for mutation in [None,'native','pdf','zip','deleted','foreign_only']:
 with tempfile.TemporaryDirectory(prefix='identity_',dir=D) as t:
  fixture(Path(t));h=Git();selected={n:bp(n.encode()) for n in ['native/check.py','packet/paper.pdf','packet/support.zip']};h.maps['actual']={n:('100644','blob',v['git_blob']) for n,v in selected.items()}
  if mutation in ['native','pdf','zip']:n={'native':'native/check.py','pdf':'packet/paper.pdf','zip':'packet/support.zip'}[mutation];h.maps['actual'][n]=('100644','blob','b'*40)
  if mutation=='deleted':h.maps['actual'].pop('native/check.py')
  if mutation=='foreign_only':h.maps['actual']['foreign/changed']=('100644','blob','c'*40)
  if mutation not in [None,'foreign_only']:reject('current_tree_rejects_'+mutation,lambda:c.selected_current(h,'actual',selected),'Selected current MAIN identity')
  else:check('current_tree_accepts_'+str(mutation),c.selected_current(h,'actual',selected)=='actual')
  merged=selected;factual={'native/status.json':bp(b'new factual status')};combined={**merged,**factual};h.maps['actual']={n:('100644','blob',x['git_blob']) for n,x in combined.items()};check('combined_factual_override_allowed_'+str(mutation),c.selected_current(h,'actual',combined)=='actual')
with tempfile.TemporaryDirectory(prefix='scope_',dir=D) as t:
 F=Path(t);fixture(F);p=F/'own.txt';p.write_text('owned');h=Git();h.foreign_mutant=True
 reject('full_tree_foreign_scope_mutant',lambda:c.prepare_tree(h,'fresh',{'case/own.txt':p},['fresh',c.HEAD],'fixture','PREP.json'),'Full-tree foreign scope drift');check('foreign_scope_rejected_before_commit','git/commits' not in h.posts)
row='|'+'|'.join(['x']*12)+'|';cells=row.split('|');cells[1]=' 5000005 / TARGET ';cells[8]=' claimed_solved ';cells[9]=' 2/5 ';row='|'.join(cells);original='HEADER\n'+row+'\nFOREIGN ROW\n'
check('queue_changes_only_target',c.queue_update(original,original,original,'10.9999/X','https://doi.org/10.9999/X').endswith('FOREIGN ROW\n'))
reject('foreign_target_row_drift',lambda:c.queue_update(original.replace('TARGET','FOREIGN CHANGE'),original,original,'x','y'),'Foreign target-row drift')
provenance=json.loads((CASE_ROOT/'ROOT_ORIGINAL_PARENT_AND_QUEUE_GUARD_01.json').read_text());rows={x['commit']:x['row'] for x in provenance['rows']};observed=provenance['actual_MAIN_observed'];before='HEADER\n'+rows[observed]+'\nFOREIGN ROW\n';orig='HEADER\n'+rows[c.HEAD]+'\nFOREIGN ROW\n';base='HEADER\n'+rows[c.ORIGINAL_BASE]+'\nFOREIGN ROW\n';updated=c.queue_update(before,orig,base,'10.9999/X','https://doi.org/10.9999/X');cells=updated.splitlines()[1].split('|')
check('actual_original_base_and_queue_PR_link',c.ORIGINAL_BASE==provenance['original_proof_parent_base'] and cells[10].strip()=='https://github.com/AlecKriebel/Math/pull/191' and cells[9].strip()=='2/5' and updated.endswith('FOREIGN ROW\n'))

# Zenodo calls are stub processes only: recover stage/publish, never blind retries.
for mode in ['stage_new','stage_unknown','stage_wrong_gate','publish_already','publish_unknown']:
 with tempfile.TemporaryDirectory(prefix='zenodo_',dir=D) as t:
  F=Path(t);g,z,tr,nm=fixture(F);c.original_ready=lambda draft=None:{'head':{'sha':c.HEAD}};calls=[]
  if mode in ['stage_unknown','stage_wrong_gate']:c.write(F/'lifecycle_private/ZENODO_STAGE_ATTEMPT_STARTED.json',{'unknown':True,'gate_sha256':c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256'] if mode=='stage_unknown' else 'WRONG_GATE'})
  if mode.startswith('publish'):
   c.write(F/'ZENODO_STAGE_READBACK.json',{'id':99,'gate_sha256':c.pin(F/'ROOT_PUBLICATION_GATE.json')['sha256']})
   if mode=='publish_unknown':c.write(F/'lifecycle_private/ZENODO_PUBLISH_ATTEMPT_STARTED.json',{'id':99})
  def runner(args,**kwargs):
   action=args[6];calls.append(action)
   if mode=='stage_unknown':return types.SimpleNamespace(returncode=1,stdout=b'',stderr=b'unknown draft state')
   out={'environment':'production','id':99,'state':'published' if mode=='publish_already' else 'ready_to_publish'}
   if out['state']=='published':out.update({k:v for k,v in z.items() if k!='gate_sha256'});out['id']=99;out['record_url']='https://zenodo.org/records/99'
   return types.SimpleNamespace(returncode=0,stdout=json.dumps(out).encode(),stderr=b'')
  if mode=='stage_new':check('zenodo_one_stage_creation',c.run_zenodo('stage',runner=runner)['id']==99 and calls==['stage'])
  elif mode=='publish_already':check('zenodo_existing_publication_no_second_POST',c.run_zenodo('publish','99',runner)['state']=='published' and calls==['inspect'])
  else:reject('zenodo_no_blind_retry_'+mode,lambda:c.run_zenodo('stage' if mode.startswith('stage') else 'publish','99',runner));check('zenodo_retry_never_posts_'+mode,all(x=='inspect' for x in calls))
  if mode=='stage_wrong_gate':check('stage_wrong_gate_rejected_before_external_runner',calls==[])

spec=importlib.util.spec_from_file_location('canonical_guard',D/'protect_canonical_outputs.py');guard=importlib.util.module_from_spec(spec);spec.loader.exec_module(guard)
with tempfile.TemporaryDirectory(prefix='guard_',dir=D) as t:
 F=Path(t);(F/'audited.py').write_text('SENTINEL');reject('generator_canonical_protection',lambda:guard.require_new_outputs(F,['audited.py']),'Refuse overwriting');check('generator_existing_bytes_unchanged',(F/'audited.py').read_text()=='SENTINEL')
check('root_frozen_inputs_unchanged',all(plain(CASE_ROOT/n)==x for n,x in source_before.items()) and all(plain(CASE_ROOT/'publication_package_v1'/n)==x for n,x in source_packet.items()))
check('frozen01_all_sealed_bytes_and_modes_unchanged',plain(OLD/'FINAL_SEAL.json')==oldsealpin and all(plain(OLD/n)==x and ((OLD/n).stat().st_mode & 0o777)==0o444 for n,x in old_before.items()))
check('frozen05_all_manifest_members_and_seal_unchanged0444',verify_seal(OLD5,old5seal) and plain(OLD5/'FINAL_SEAL.json')==old5pin)
retained_names={v['name'] for v in json.loads((OLD5/'SELFTEST_RESULTS.json').read_text())['checks']};check('all_prior440_named_controls_retained',len(json.loads((OLD5/'SELFTEST_RESULTS.json').read_text())['checks'])==440 and retained_names<={v['name'] for v in results['checks']})
results.update(UTC=c.now(),verdict='PASS_OFFLINE_PROPOSAL_CONTROLS',checks_passed=len(results['checks']),root_inputs_unchanged=True,original16_preserved=True,external_actions_untested=True)
(D/'SELFTEST_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps({'verdict':results['verdict'],'checks':len(results['checks']),'remote_calls':0}))

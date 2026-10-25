"""Seal own additive recheck packet, preserving every earlier original."""
from pathlib import Path
import ast,datetime,hashlib,json
O=Path(__file__).resolve().parent;P=O.parents[1];S=P/'verification/local-cylinder-discotope-stage-sol-20261025';A=P/'verification/cylinder-discotope-code-audit-sol-20261025'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
if (O/'FINAL_SEAL.json').exists():raise RuntimeError('preserve_final_original')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat();bindings=[]
for name,key in [('protected-before.json','files'),('AUDITOR_INPUT_CUSTODY.json','original_files')]:
    for item in json.loads((O/name).read_text())[key]:
        p=Path(item['path'])
        if not p.is_file() or p.stat().st_size!=item['bytes'] or sha(p)!=item['SHA256']:raise RuntimeError('original_changed:'+str(p))
        bindings.append(item)
results=json.loads((O/'RECHECK_RESULTS.json').read_text())
if results['executions']!=44 or results['per_mode_former_false_accepts_now_rejected']!=7:raise RuntimeError('all_expected_cases_required')
root_input=O/'inputs/final-content-check.proposed.py'
if sha(root_input)!='7a452efabbcb95335d1a4617faa4c10136a67de95c923d472896db5c5f7b4b80':raise RuntimeError('root_guard_input_changed')
save('PRESERVATION_RECEIPT.json',{'UTC':utc,'status':'ALL_BOUND_ORIGINALS_UNCHANGED','bindings_rehashed':len(bindings),'distinct_original_paths':len({x['path'] for x in bindings}),'source_helper_renderer_overlay_unchanged':True,'source_configs_reviews_and_custom_objects_unchanged':True,'original_stage_seal_SHA256':sha(S/'FINAL_SEAL.json'),'original_auditor_seal_SHA256':sha(A/'FINAL_SEAL.json'),'root_corrected_checker_SHA256':sha(root_input),'production_public_files_unchanged':484,'no_production_installation':True})
early=json.loads((O/'EARLY_MECHANISM.json').read_text())
save('READ_LEDGER.json',{'UTC':utc,'entire_root_checker_diff_and_target_block_read_before_auditor_cases':True,'early_mechanism_seal_SHA256':sha(O/'EARLY_MECHANISM_SEAL.json'),'entire_auditor_fault_checker_and_report_read_after_final_seal':True,'auditor_seal_SHA256':sha(A/'FINAL_SEAL.json'),'auditor_fault_driver_SHA256':sha(A/'fault_checker.py'),'entire_own_adaptation_diffs_and_execution_code_read':True,'all44_actual_outcomes_checked':True,'same_mutation_receipts_exactly_compared_to_original_auditor':True,'whole_old59_checker_suite_reread_or_reexecuted':False,'old59_scope_mechanism':'Single insertion only inside CD_IDS; exact byte/AST excision and old59 disjoint; original code retained everywhere else.','new_scientific_manuscript_review_claim':False})
save('VERDICT.json',{'UTC':utc,'assignment_status':'COMPLETE','completion_estimate_percent':100,'website_checker_verdict':'BOUNDED_ROOT_CORRECTION_RECHECK_PASS','root_corrected_checker_SHA256':sha(root_input),'normal_pristine_accepted':2,'normal_faults_rejected':20,'optimized_pristine_accepted':2,'optimized_faults_rejected':20,'former_seven_false_accepts_rejected_each_mode':True,'original_stage_and_audit_kept_immutable':True,'old59_behavior_unchanged_by_exact_guard_scope':True,'old59_full_suite_rerun':False,'renderer_or_overlay_regenerated':False,'new_scientific_verdict':None,'source_correction_required':False,'scope_limit':'Exact approved2 page structures and sealed20 faults; no universal HTML/CSS/parser-security claim.','production_installed':False,'publication_clearance_granted_by_this_recheck':False,'human_peer_review':False,'formal_certification':False,'root_authority_retained':True,'overall203_programme_complete':False})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('* '+utc+' — Exact44 checker executions completed once:2 pristine accepted and20 faults rejected in each normal/-O mode; all former7 reject through specified new guards. Root input hash and outcomes sent to root before final sealing. All protected and auditor originals unchanged. Completion estimate100%; root integration authority retained and203programme ongoing.\n')
files=[]
for p in sorted(O.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']:
        if p.is_symlink():raise RuntimeError('no_owned_symlinks')
        files.append({'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'SHA256':sha(p)})
save('FINAL_MANIFEST.json',{'UTC':utc,'status':'IMMUTABLE_CORRECTION_RECHECK','files':files,'root_guard_input_SHA256':sha(root_input),'original_stage_and_audit_mutated':False})
save('FINAL_SEAL.json',{'UTC':utc,'status':'SEALED_COMPLETE_BOUNDED_CHECKER_RECHECK_PASS','manifest':'FINAL_MANIFEST.json','manifest_SHA256':sha(O/'FINAL_MANIFEST.json'),'owned_bindings':len(files),'completion_estimate_percent':100,'production_or_publication_authority':False,'overall203_programme_complete':False,'preserve_immutable':True})
print(json.dumps({'status':'SEALED','owned_bindings':len(files),'manifest_SHA256':sha(O/'FINAL_MANIFEST.json'),'seal_SHA256':sha(O/'FINAL_SEAL.json'),'REPORT_SHA256':sha(O/'REPORT.md')},indent=2))

"""Freeze only own additive correction recheck, once."""
from pathlib import Path
import datetime,hashlib,json
O=Path(__file__).resolve().parent;P=O.parents[1];S=P/'verification/local-spanning-sos-gin-stage-sol-20261025';A=P/'verification/audit-spanning-sos-gin-code-sol-20261025'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
if (O/'FINAL_SEAL.json').exists():raise RuntimeError('preserve_final_original')
utc=datetime.datetime.now(datetime.timezone.utc).isoformat();bound=[]
for n,k in [('protected-before.json','files'),('AUDITOR_INPUT_CUSTODY.json','original_files')]:
    for x in json.loads((O/n).read_text())[k]:
        p=Path(x['path'])
        if not p.is_file() or p.stat().st_size!=x['bytes'] or sha(p)!=x['SHA256']:raise RuntimeError('original_changed:'+str(p))
        bound.append(x)
prior=json.loads((O/'PRIOR_RESULTS.json').read_text());auditor=json.loads((O/'AUDITOR_REPLAY_RESULTS.json').read_text())
if prior['status']!=auditor['status'] or prior['status']!='PASS' or len(prior['faults'])!=70 or len(auditor['cases'])!=62:raise RuntimeError('complete_cases_required')
save('PRESERVATION_RECEIPT.json',{'UTC':utc,'status':'ALL_BOUND_ORIGINALS_UNCHANGED','bindings_rehashed':len(bound),'distinct_original_paths':len({x['path'] for x in bound}),'original_stage_seal_SHA256':sha(S/'FINAL_SEAL.json'),'original_auditor_seal_SHA256':sha(A/'FINAL_SEAL.json'),'root_input_SHA256':sha(O/'inputs/final-content-check.proposed.py'),'production_public_files_unchanged':492,'helper_renderer_overlay_sources_configs_custom_objects_unchanged':True,'no_integration':True})
save('READ_LEDGER.json',{'UTC':utc,'full_root_diff_and_SG_block_read_before_auditor_variant_code':True,'early_mechanism_seal_SHA256':sha(O/'EARLY_MECHANISM_SEAL.json'),'independent_HTMLParser_whole_body_h1_Gin_label_reconstruction':True,'entire_sealed_auditor_report_plan_and_checker_control_read_after_seal':True,'auditor_REPORT_SHA256':sha(A/'REPORT.md'),'auditor_FINAL_SEAL_SHA256':sha(A/'FINAL_SEAL.json'),'complete_own_dispatch_diffs_and_execution_code_read':True,'all_prior_and_auditor_mutation_byte_identities_compared':True,'all_actual_outcomes_checked':True,'no_new_science_or_browser_review_claim':True,'helper_structural_scalar_type_caveat_preserved_not_retested':True})
save('VERDICT.json',{'UTC':utc,'assignment_status':'COMPLETE','completion_estimate_percent':100,'website_checker_verdict':'BOUNDED_EXACT_ROOT_CORRECTION_RECHECK_PASS','root_checker_SHA256':sha(O/'inputs/final-content-check.proposed.py'),'pristine_records_accepted_each_normal_optimized_mode':3,'prior_faults_rejected_each_mode':35,'auditor_faults_rejected_each_mode':31,'former_seven_rejected_each_mode':True,'negative_dispatches':132,'pristine_record_checks':6,'checker_subprocesses':134,'single_13_line_SG_IDS_insertion_exact_excision':True,'old61_behavior_unchanged_by_guard_scope':True,'old61_suite_rerun':False,'renderer_rerun':False,'source_or_scientific_repair':False,'whole_body_contract':'Fixed approved normalized text under normal current HTML structure; no arbitrary CSS/browser/hostile-parser guarantee.','source_helper_scalar_type_equality_caveat':'Existing auditor finding preserved; outside checker-only correction; not repaired or retested here.','production_installed':False,'human_peer_review':False,'formal_certification':False,'publication_clearance':False,'root_authority_retained':True,'overall203_programme_complete':False})
with (O/'RESEARCH_LOG.md').open('a') as f:f.write('* '+utc+' — Pristine3 passes194 checks each mode; all prior35 and auditor31 faults reject each normal/-O mode; former7 fail expected new guards.132 negative dispatches plus2 batched pristine processes; no duplicate pristine/old61 suite/renderer execution. All bound originals unchanged; exact input/results sent to root before final seal. Completion100%; root integration authority retained;203 programme ongoing.\n')
files=[]
for p in sorted(O.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']:
        if p.is_symlink():raise RuntimeError('no_owned_symlinks')
        files.append({'path':str(p.relative_to(O)),'bytes':p.stat().st_size,'SHA256':sha(p)})
save('FINAL_MANIFEST.json',{'UTC':utc,'status':'IMMUTABLE_ADDITIVE_SG_CHECKER_RECHECK','files':files,'original_stage_auditor_and_production_mutated':False})
save('FINAL_SEAL.json',{'UTC':utc,'status':'SEALED_COMPLETE_BOUNDED_ROOT_CHECKER_RECHECK_PASS','manifest':'FINAL_MANIFEST.json','manifest_SHA256':sha(O/'FINAL_MANIFEST.json'),'owned_bindings':len(files),'completion_estimate_percent':100,'integration_or_publication_authority':False,'overall203_programme_complete':False,'preserve_immutable':True})
print(json.dumps({'status':'SEALED','owned_bindings':len(files),'manifest_SHA256':sha(O/'FINAL_MANIFEST.json'),'seal_SHA256':sha(O/'FINAL_SEAL.json'),'REPORT_SHA256':sha(O/'REPORT.md')},indent=2))

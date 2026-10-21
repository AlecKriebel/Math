#!/usr/bin/env python3
"""Seal only public installed engineering evidence; never adopt workflow/freeze."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];ROOT=P.parent;A=P/'audits/pr952_10400145';W=A/'publication/workflow'
NEW='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec';AUTH='88c70b6d71f2674fa5593a70c2924a949408fadd6b36f731127db1aaef469063';READY='14bd1137e83f974e7dbf8153614533d72b5fe93d6382cea33e220580e396d603';INVENTORY='9650f0baf87ac6d83a5a7eb934d212cc66ea67dea4c8758813bec47f5a24cc05'
def need(ok,m):
 if not ok:raise RuntimeError(m)
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(path):
 path=Path(path);parts=path.relative_to(ROOT).parts;need(all(x not in ('','.','..') for x in parts),'safe input')
 for i in range(len(parts)+1):need(not ROOT.joinpath(*parts[:i]).is_symlink(),'no linked input')
 need(path.is_file() and stat.S_ISREG(path.stat().st_mode),'regular input');return path.read_bytes()
def pin(path):
 b=raw(path);return {'bytes':len(b),'sha256':sha(b),'mode':format(path.stat().st_mode,'06o')}
def new(name,value):
 with (OWN/name).open('x') as stream:json.dump(value,stream,indent=2,ensure_ascii=False,allow_nan=False);stream.write('\n')
need(pin(A/'ROOT_OPERATIONS04_INSTALLATION_AUTHORIZATION.json')['sha256']==AUTH,'root installation authorization');need(pin(P/'accept_pr952.py')['sha256']==NEW and raw(P/'accept_pr952.py')==raw(OWN/'PROPOSED_accept_pr952.py'),'actual installed exact approved bytes');need(pin(OWN/'PROPOSAL_READINESS.json')['sha256']==READY,'preserved proposal seal');readiness=json.loads(raw(OWN/'PROPOSAL_READINESS.json'))
for name,item in readiness['files'].items():need(pin(ROOT/name)==item,'preserved399 closure changed '+name)
# Exact three root-owned changes, explicitly attested in trusted root message.
root_after={str((P/'CURRENT_STATE.json').relative_to(ROOT)):'92921ecdf1b1c0bb709b43b9ff9af46d4bbc7e4a78e907e650d5b8dee1a0b2ea',str((P/'RESEARCH_LOG.md').relative_to(ROOT)):'667175cada1edc1bd493152aa0ea68604bf0403590a6189fc1b05a38cc4deb21',str((A/'RESEARCH_LOG.md').relative_to(ROOT)):'c6658ccdca8e13fab60329e114c44f4f1654a7880a18507f026f1d550f516d11'}
before=json.loads(raw(OWN/'INSTALL_BEFORE_PROTECTED_SNAPSHOT.json'))['files'];changed={};unchanged=0
for name,item in before.items():
 actual=pin(ROOT/name)
 if actual!=item:changed[name]={'before':item,'after':actual,'attribution':'ROOT_OWNED_TRUSTED_CONCURRENT_UPDATE','root_update_utc':'2026-10-16T18:49:23.097250Z'}
 else:unchanged+=1
need(set(changed)==set(root_after) and unchanged==1191 and len(before)==1194,'no blanket shared-file change waiver')
for name,expected in root_after.items():need(changed[name]['after']['sha256']==expected,'exact root after pin')
guard={'schema':'pr952-engineering04-protected-shared-files-final-guard-v1','observed_utc':now(),'path_base':'repository_root','baseline_snapshot':pin(OWN/'INSTALL_BEFORE_PROTECTED_SNAPSHOT.json'),'baseline_noncore_files':len(before),'unchanged_count':unchanged,'changed_count':len(changed),'exact_root_owned_changes':changed,'trusted_root_confirmation':'Parent root reported these exact3 updates at2026-10-16T18:49:23.097250Z, independently confirmed the listed after hashes/exact3 changes and1191unchanged, and promised no further shared mutation before seal. These are root changes, not engineering writes.','engineering_shared_change':'Only exact authorized accept_pr952.py replacement','mutable_active_files_are_NOT_seal_members':True,'all_other_noncore_guarded_paths_exact':True}
new('FINAL_PROTECTED_SHARED_GUARD.json',guard)
final={};count=0
for family,expected,script in [('finalization',129,'test_finalization_logs_recovery.py'),('operations',61,'test_operations_proposal.py'),('source_gate',18,'test_source_gate_proposal.py'),('native_recovery',35,'test_native_recovery_proposal.py')]:
 final[family]={}
 for mode,opt in [('normal',0),('O',1),('OO',2)]:
  prefix=OWN/('TEST_INSTALLED04_'+family+'_'+mode);launch=json.loads(raw(Path(str(prefix)+'.launch.json')));result=json.loads(raw(Path(str(prefix)+'.stdout.json')))
  need(launch['returncode']==0 and launch['installed'] is True and '--installed' in launch['command'] and launch['proposal_sha256']==NEW and launch['requested_compile_optimization']==opt and launch['test_source_sha256']==pin(OWN/script)['sha256'],'actual installed launch pins')
  need(result['event_count']==expected and result['outer_optimization']==opt and result['installed_actual_source_executed'] is True,'actual installed source/count/optimization')
  final[family][mode]={'event_count':expected,'actual_compile_optimization':opt,'installed_actual_source_executed':True,'test_source':pin(OWN/script),'launch':pin(Path(str(prefix)+'.launch.json')),'stdout':pin(Path(str(prefix)+'.stdout.json')),'stderr':pin(Path(str(prefix)+'.stderr.txt'))};count+=expected
need(count==729,'full installed scope')
new('INSTALLED_TEST_SUMMARY.json',{'schema':'pr952-installed-engineering04-test-summary-v1','utc':now(),'actual_installed_core_sha256':NEW,'installed_observation_count':count,'per_mode_controls':243,'actual_compile_modes':[0,1,2],'families':final,'failed_installed_runs':0,'prior_proposal_failures_preserved':True,'actual_remote_mutations_or_services_or_Git_calls':0,'explicit_inert_trust_boundaries':True,'acceptance_authority':False,'fresh_whole_review_credit':False})
inv=raw(OWN/'GENERATED_OPERATIONS_INVENTORY.json');need(sha(inv)==INVENTORY,'exact generated installed inventory');inventory=json.loads(inv);need(len(inventory['files'])==7,'six core/wrappers plus kit')
for name,item in inventory['files'].items():need({k:pin(ROOT/name)[k] for k in ('bytes','sha256')}==item,'current exact seven-file operations inventory')
full=json.loads(raw(OWN/'FULL_GENERATOR_VALIDATION.json'));need(len(full['results'])==3 and all(x['status']=='PASS_READONLY_FULL_GENERATION_NOT_ADOPTED' for x in full['results']),'actual full generator validation')
receipt={'schema':'pr952-installed-operations04-engineering-receipt-v1','utc':now(),'status':'EXACT_ROOT_AUTHORIZED_CORE_INSTALLED_AND_INERT_VERIFIED_NO_WORKFLOW_ADOPTION','root_authorization':{'path':str((A/'ROOT_OPERATIONS04_INSTALLATION_AUTHORIZATION.json').relative_to(ROOT)),'sha256':AUTH},'preserved_proposal_readiness_sha256':READY,'preserved_proposal_public_files':399,'installation_action_receipt':pin(OWN/'INSTALL_ACTION_RECEIPT.json'),'actual_installed_core':pin(P/'accept_pr952.py'),'actual_installed_source_tests':pin(OWN/'INSTALLED_TEST_SUMMARY.json'),'installed_observation_count':count,'operations_inventory':pin(OWN/'GENERATED_OPERATIONS_INVENTORY.json'),'full_readonly_generator':pin(OWN/'FULL_GENERATOR_VALIDATION.json'),'canonical_workflow_operations_inventory_or_freeze_adopted':False,'protected_shared_final_guard':pin(OWN/'FINAL_PROTECTED_SHARED_GUARD.json'),'noncore_installed_action_exact_count':1194,'final_noncore_exact_count':1191,'root_concurrent_changed_files':list(changed),'engineering_changed_shared_files':[str((P/'accept_pr952.py').relative_to(ROOT))],'five_wrappers_and_global_kit_unchanged':True,'original_math_PDF_ZIP_FREEZE_workflow_native_source_unchanged_by_engineer':True,'actual_service_Git_PR_or_remote_mutations':0,'accepted':False,'acceptance_authority':False,'fresh_whole_review_credit':False,'remaining':'Root final intake; explicit full seal expansion/adoption into candidate4; static/current live gates; fresh entire full03/full04; no premature acceptance.'}
new('INSTALL_RECEIPT.json',receipt)
with (OWN/'INSTALL_RESEARCH_LOG.md').open('a') as stream:
 stream.write('\n'+now()+' — Actual installed-source129+61+18+35 controls PASS at compile0/1/2,729 observations, no failed installed runs. Full read-only candidate4 generator executed successfully in all3 modes, own-output only, current protocol20c8... and both adverse histories retained. Exact seven-file inventory9650f0... generated but not adopted. Installation-validation estimate90%.\n')
 stream.write('\n'+now()+' — Preserved original399 proposal files unchanged. Final guard finds1191 unchanged noncore paths and EXACTLY3 root-owned state/log updates with individually fixed after hashes and trusted root timestamp; no blanket waiver. Mutable shared state/logs are excluded from final closure. Final receipts/integration/public MANIFEST prepared; authorized installed engineering100%, root final intake/candidate4/fresh full03/full04 remain pending. No acceptance or service action.\n')
files=dict(readiness['files'])
for path in sorted(OWN.rglob('*')):
 if not path.is_file():continue
 rel=path.relative_to(OWN)
 if rel.parts[0]=='private_tmp' or '__pycache__' in rel.parts or path.suffix=='.pyc' or (rel.parts[0]=='history' and 'evidence' in rel.parts):continue
 if path.name in ('MANIFEST.json','MANIFEST.sha256'):continue
 files[str(path.relative_to(ROOT))]=pin(path)
for name in inventory['files']:files[name]=pin(ROOT/name)
extras=[A/'ROOT_OPERATIONS04_INSTALLATION_AUTHORIZATION.json',A/'ROOT_FULL02_PROCESS_UPDATE.json',*sorted(path for path in (A/'root_operations04_revised_probe').iterdir() if path.is_file())]
for path in extras:files[str(path.relative_to(ROOT))]=pin(path)
mutable={str((P/name).relative_to(ROOT)) for name in ['CURRENT_STATE.json','inventory.json','RESEARCH_LOG.md']}|{str((A/'RESEARCH_LOG.md').relative_to(ROOT))}
need(not(set(files)&mutable) and not any((ROOT/name).is_relative_to(W) for name in files),'never seal mutable shared state/log/workflow files')
need(not any('/evidence/' in name or '/private_tmp/' in name for name in files),'no private historical or fixture payloads in explicit public closure')
manifest={'schema':'pr952-operations-engineering-seal-v1','utc':now(),'phase':'AUTHORIZED_INSTALLED_INERT_VALIDATION_COMPLETE','pr':952,'problem_id':'10400145','original_pr_head':'989a532ae1d50894190d010a0a02ba8c3d71ee05','installed_core_sha256':NEW,'operations_inventory_sha256':INVENTORY,'root_installation_authorization_sha256':AUTH,'historical_proposal_readiness_sha256':READY,'installed_observation_count':count,'actual_compile_optimization_modes':[0,1,2],'public_file_count':len(files),'path_base':'repository_root','files':dict(sorted(files.items())),'explicit_public_allowlist':sorted(files),'mutable_shared_active_paths_excluded':True,'private_scratch_and_private_historical_payloads_excluded':True,'scientific_or_publication_acceptance':False,'acceptance_authority':False,'fresh_whole_review_credit':False,'services_or_Git_or_remote_mutations':0,'installation_receipt':pin(OWN/'INSTALL_RECEIPT.json'),'prior_adverse_full01_full02_and_candidate1_3_preserved':True}
new('MANIFEST.json',manifest)
print(json.dumps({'status':manifest['phase'],'MANIFEST':pin(OWN/'MANIFEST.json'),'INSTALL_RECEIPT':pin(OWN/'INSTALL_RECEIPT.json'),'INSTALLED_TEST_SUMMARY':pin(OWN/'INSTALLED_TEST_SUMMARY.json'),'INTEGRATION':pin(OWN/'INTEGRATION.md'),'public_file_count':len(files),'operations_inventory_sha256':INVENTORY,'installed_core_sha256':NEW},indent=2))

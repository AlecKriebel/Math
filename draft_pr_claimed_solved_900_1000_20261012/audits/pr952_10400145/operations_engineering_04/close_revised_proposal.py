#!/usr/bin/env python3
"""Close own public engineering proposal; never install or edit external files."""
from pathlib import Path
from datetime import datetime,timezone
import ast,difflib,hashlib,json,stat
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];ROOT=P.parent;A=P/'audits/pr952_10400145'
def need(ok,m):
 if not ok:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(path):
 path=Path(path);need(path.is_relative_to(ROOT) and not path.is_symlink() and path.is_file() and stat.S_ISREG(path.stat().st_mode),'regular trusted input');return path.read_bytes()
def pin(path):
 b=raw(path);return {'bytes':len(b),'sha256':sha(b),'mode':format(path.stat().st_mode,'06o')}
def put(name,value): (OWN/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def now():return datetime.now(timezone.utc).isoformat()
BASE='888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8';NEW='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec';OLD='07d1088bcbf8a81c71f15f5f096fcced98e4638244eb794df7efffcd0783688b'
base=raw(OWN/'BASE_accept_pr952.py');proposed=raw(OWN/'PROPOSED_accept_pr952.py');need(sha(base)==BASE and sha(proposed)==NEW,'external base/proposal pins')
# Preserve the first emitted log revision, which preceded its one-line checked
# short-write refinement. Reversal reproduces its actual emitted SHA exactly.
first=proposed.replace(b"need(stream.write(raw)==len(raw),'local temporary short write');stream.flush();os.fsync(stream.fileno())",b'stream.write(raw);stream.flush();os.fsync(stream.fileno())')
need(sha(first)=='9458214a4739ca6786edf7ae2ea9939f38a6d1ac335e8ce570735c43071f970c','initial emitted revision pin')
for name,data in [('PROPOSED_LOGREV_v01_untested_accept_pr952.py',first),('PROPOSED_LOGREV_v02_tested_accept_pr952.py',proposed)]:
 path=OWN/name
 if path.exists():need(raw(path)==data,'immutable revision copy')
 else:path.write_bytes(data)
# Existing production function/constant source must remain byte-identical except finalize.
bt=base.decode();pt=proposed.decode();ba=ast.parse(bt);pa=ast.parse(pt)
functions=lambda text,tree:{node.name:ast.get_source_segment(text,node) for node in tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}
bf=functions(bt,ba);pf=functions(pt,pa);changed=[name for name in bf if bf[name]!=pf.get(name)];added=sorted(set(pf)-set(bf));need(changed==['finalize'] and len(added)==7,'exact function scope')
assignments=lambda text,tree:[ast.get_source_segment(text,node) for node in tree.body if isinstance(node,(ast.Assign,ast.AnnAssign))]
need(assignments(bt,ba)==assignments(pt,pa),'module identity/required-finding assignments changed')
authorities=['accepted_package','accepted_review_check','source_gate','premerge_gate','merged_gate','publication_links','independent_public_verify','native_verify','native_write','finalize_pr_metadata','gate_next','review_check','gws','save','read_regular']
put('UNCHANGED_AUTHORITIES.json',{'schema':'pr952-proposal04-authority-preservation-v2','utc':now(),'base_sha256':BASE,'proposal_sha256':NEW,'changed_preexisting_functions':changed,'new_local_functions':added,'all_other_preexisting_function_sources_byte_identical':True,'all_module_assignments_byte_identical':True,'unchanged_authority_functions':{name:sha(bf[name].encode()) for name in authorities},'no_inherited_or_root_finding_ID_hardcoding_added':True})
# Authenticate both old history representations without rewriting either one.
snapshot=OWN/'history/proposal04_v01_authenticated/SNAPSHOT_MANIFEST.json';need(pin(snapshot)['sha256']=='e3a8a851c49cafde20e265ee3064a35d20966c2c7a7584b69fabf8a2a3774245','historical local snapshot manifest')
public=A/'operations04_v01_public_snapshot/MANIFEST.json';need(pin(public)['sha256']=='f1e27cc4e126a787de3c98f409a96b0fa15d033a1f78434bb5f216203f4bb234','root portable public manifest');history=json.loads(raw(public));need(len(history['files'])==118,'exact old public closure')
for original,item in history['files'].items():need(pin(ROOT/item['path'])=={k:item[k] for k in ('bytes','sha256','mode')},'old public relocation changed')
versions={name:pin(OWN/name) for name in ['PROPOSED_v01_accept_pr952.py','PROPOSED_v02_accept_pr952.py','PROPOSED_v03_accept_pr952.py','HISTORICAL_PROPOSAL04_LOG_GAP_accept_pr952.py','PROPOSED_LOGREV_v01_untested_accept_pr952.py','PROPOSED_LOGREV_v02_tested_accept_pr952.py','PROPOSED_accept_pr952.py']}
need(versions['HISTORICAL_PROPOSAL04_LOG_GAP_accept_pr952.py']['sha256']==OLD,'exact old proposed source')
put('PROPOSAL_VERSIONS.json',{'schema':'pr952-proposal04-version-history-v2','utc':now(),'base':pin(OWN/'BASE_accept_pr952.py'),'versions':versions,'old_116_closure_and_readiness_preserved':True,'old_snapshot_manifest':pin(snapshot),'portable_public_copy_manifest':pin(public),'v01_log_revision_provenance':'Untested first emitted9458214... bytes recovered exactly from the subsequent one-line checked-short-write refinement and matched to its actual generation output hash; no passing test claim for9458214.','old07d_status':'UNINSTALLED_COUNTEREXAMPLE_REPRODUCED_LOG_COMPLETION_GAP','current_status':'TESTED_UNINSTALLED_SAME_FINDING_REPAIR','failed_launches_retained':['TEST_FINALIZATION_ATTEMPT01_normal/O/OO','TEST_LOGREV_ATTEMPT01_finalization_normal/O/OO'],'fresh_whole_review_credit':False})
# Refresh explicit harness diffs and source pins. Existing old records are frozen.
adapt=json.loads(raw(OWN/'HARNESS_ADAPTATIONS.json'))
for name,item in adapt.items():
 source=A/item['source_path'];item['adapted_sha256']=pin(OWN/name)['sha256'];item['optional_installed_flag_available']=True;item['installed_flag_executed_in_this_proposal_phase']=False
 diff=''.join(difflib.unified_diff(raw(source).decode().splitlines(keepends=True),raw(OWN/name).decode().splitlines(keepends=True),fromfile=item['source_path'],tofile='operations_engineering_04/'+name));(OWN/(name+'.HARNESS.diff')).write_text(diff)
newtest=OWN/'test_finalization_logs_recovery.py';adapt[newtest.name]={'source_path':'operations_engineering_04/test_finalization_recovery.py','source_sha256':pin(OWN/'test_finalization_recovery.py')['sha256'],'adapted_sha256':pin(newtest)['sha256'],'actual_core_compile_optimization':'sys.flags.optimize','installed':False,'explicit_inert_upstream_boundaries':True,'old53_scope_preserved_and_extended_to129':True,'optional_installed_flag_available':True,'installed_flag_executed_in_this_proposal_phase':False}
(OWN/'test_finalization_logs_recovery.py.HARNESS.diff').write_text(''.join(difflib.unified_diff(raw(OWN/'test_finalization_recovery.py').decode().splitlines(keepends=True),raw(newtest).decode().splitlines(keepends=True),fromfile='old53/test_finalization_recovery.py',tofile='revised129/test_finalization_logs_recovery.py')))
put('HARNESS_ADAPTATIONS.json',adapt)
protected={}
for key,path,expected in [('current_core',P/'accept_pr952.py',BASE),('current_candidate03_freeze',A/'preprint/FREEZE.json','87e6753c48153e6bbc82ad77181339dd4d4fe64e0c855be507da6b47b7438424'),('operations03_seal',A/'operations_engineering_03/MANIFEST.json','086efa2e47bb9ba3cbd6befa5307fc7dfe667bb7687b26f30161263075891b61')]:
 need(pin(path)['sha256']==expected,'protected input changed');protected[key]={'path':path.relative_to(ROOT).as_posix(),'sha256':expected,'observed_utc':now()}
put('PROTECTED_INPUTS.json',protected)
final={};total=0
for suite,count,script in [('finalization',129,'test_finalization_logs_recovery.py'),('operations',61,'test_operations_proposal.py'),('source_gate',18,'test_source_gate_proposal.py'),('native_recovery',35,'test_native_recovery_proposal.py')]:
 final[suite]={}
 for mode,opt in [('normal',0),('O',1),('OO',2)]:
  prefix=OWN/('TEST_LOGREV_CLOSED_'+suite+'_'+mode);launch=json.loads(raw(Path(str(prefix)+'.launch.json')));result=json.loads(raw(Path(str(prefix)+'.stdout.json')))
  need(launch['returncode']==0 and result['event_count']==count and result['outer_optimization']==opt and launch['proposal_sha256']==NEW and launch['test_source_sha256']==pin(OWN/script)['sha256'] and launch['installed'] is False,'final actual test closure')
  need(result.get('installed_actual_source_executed',False) is False,'no installed run authority')
  final[suite][mode]={'returncode':0,'event_count':count,'actual_compile_optimization':opt,'proposal_sha256':NEW,'test_source_sha256':pin(OWN/script)['sha256'],'launch_path':Path(str(prefix)+'.launch.json').relative_to(ROOT).as_posix(),'launch':pin(Path(str(prefix)+'.launch.json')),'stdout':pin(Path(str(prefix)+'.stdout.json')),'stderr':pin(Path(str(prefix)+'.stderr.txt'))};total+=count
need(total==729,'complete final scope')
put('FINAL_TEST_SUMMARY.json',{'schema':'pr952-proposal04-log-recovery-final-test-summary-v2','utc':now(),'proposal_sha256':NEW,'final_tests':final,'final_observation_count':total,'per_mode_control_count':243,'generator_preview_controls':12,'generator_full_after_install_path_executed':False,'real_services_or_Git_or_remote_mutations':0,'all_prior_failures_and_versions_retained':True,'installed':False,'fresh_whole_review_credit':False,'accepted':False})
with (OWN/'RESEARCH_LOG.md').open('a') as stream:
 stream.write('\n'+now()+' — Revised after root preinstall counterexample: same R952-FULL02-OPS-01 now includes both independently recoverable completion logs. Old118 exact inputs preserved before revision under e3a8a851... and root public f1e27cc... anchor; old07d independent actual gap reproduced. First revised short-write test expectation omitted the existing PR952 guard prefix; all three actual failures/raw launches/source retained, harness text alone corrected. A mistyped generator directory produced no test execution. Engineering repair estimate95%.\n')
 stream.write('\n'+now()+' — Final proposed14ac4e... passes actual129 finalization/log +61 operations +18 source +35 native controls at compile0/1/2,729 observations; final TEST_LOGREV_CLOSED sources/launches/raw outputs pinned. Twelve generator preview/uninstalled-guard controls also pass; full generator and installed branches remain unexecuted until explicit root authorization. Four-file canonical success requires both logs and real reconciliation times. Current888... core,87e675... freeze and086efa... prior seal rechecked unchanged. Engineering proposal100%; installation, root acceptance and fresh full03/full04 remain pending.\n')
# Freeze the entire explicit public closure. Historical private-path payload
# trees and scratch are deliberately absent; the portable public copy closes
# all118 old inputs with an authenticated original-path relocation mapping.
files={}
for path in sorted(OWN.rglob('*')):
 if not path.is_file():continue
 rel=path.relative_to(OWN)
 if rel.parts[0]=='private_tmp' or '__pycache__' in rel.parts or path.suffix=='.pyc' or (rel.parts[0]=='history' and 'evidence' in rel.parts):continue
 if path.name in ('PROPOSAL_READINESS.json','PROPOSAL_READINESS.sha256'):continue
 files[path.relative_to(ROOT).as_posix()]=pin(path)
files[public.relative_to(ROOT).as_posix()]=pin(public)
for item in history['files'].values():files[item['path']]=pin(ROOT/item['path'])
readiness={'schema':'pr952-proposal04-tested-readiness-v2','utc':now(),'status':'TESTED_REVISED_PROPOSAL_ONLY_AWAITING_ROOT_INTAKE_AND_EXPLICIT_INSTALLATION','target_finding':'R952-FULL02-OPS-01','same_existing_finding_includes_both_research_logs':True,'proposal_completion_estimate_percent':100,'proposal_core':pin(OWN/'PROPOSED_accept_pr952.py'),'patch':pin(OWN/'PROPOSED.patch'),'plan':pin(OWN/'PROPOSAL_PLAN.md'),'test_summary':pin(OWN/'FINAL_TEST_SUMMARY.json'),'harness_adaptations':pin(OWN/'HARNESS_ADAPTATIONS.json'),'protected_inputs':protected,'old_authenticated_proposal':{'core_sha256':OLD,'readiness_sha256':'d9600ee1aaf536a81e000a7ad66ec6713e10b489a4462d8f0e95565320998528','local_snapshot_manifest':snapshot.relative_to(ROOT).as_posix(),'local_snapshot_manifest_sha256':pin(snapshot)['sha256'],'portable_public_manifest':public.relative_to(ROOT).as_posix(),'portable_public_manifest_sha256':pin(public)['sha256'],'relocated_file_count':118},'final_tests':final,'final_observation_count':total,'generator_preview_control_count':12,'generator_full_after_installation_path_executed':False,'canonical_success_requires':['P/CURRENT_STATE.json','P/inventory.json','P/RESEARCH_LOG.md','A/RESEARCH_LOG.md'],'new_helper_count':7,'current_adapter_state_inventory_workflow_paper_Git_service_edits':0,'actual_remote_mutation_calls':0,'scientific_acceptance_authority':False,'fresh_whole_review_credit':False,'path_base':'repository_root','files':dict(sorted(files.items())),'explicit_public_allowlist':sorted(files)}
put('PROPOSAL_READINESS.json',readiness)
print(json.dumps({'status':readiness['status'],'readiness_sha256':pin(OWN/'PROPOSAL_READINESS.json')['sha256'],'proposal':pin(OWN/'PROPOSED_accept_pr952.py'),'patch':pin(OWN/'PROPOSED.patch'),'plan':pin(OWN/'PROPOSAL_PLAN.md'),'test_summary':pin(OWN/'FINAL_TEST_SUMMARY.json'),'public_files':len(files),'controls':total},indent=2))

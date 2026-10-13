"""PR148 active checkpoint: scoped audit overlay and separate three-program install.

Source preparation only. Every actual action needs genuine completed PR147 final
acceptance and a fresh independent exact source/request/postimage/plan review.
"""
from pathlib import Path,PurePosixPath
import argparse,base64,hashlib,json,os,stat,types
R=Path('/Users/alec/Documents/Math')
C=R/'draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout'
A147=C/'draft_pr_publication_program_20260930/audits/pr147_5100001'
A=C/'draft_pr_publication_program_20260930/audits/pr148_5100002'
D=A/'active_checkpoint_operator_preparation_20261008'
DEPENDENCY=A147/'native_sparse_operator_preparation_20261008/native_sparse_operator_v1.py'
DEPENDENCY_SHA='9eed88db21f9018eedf6cd48ba79f3ea87b4499ea118c6d2817f8cd4574cc8ca'
BASELINE_GATE=A147/'ROOT_FINAL_METADATA_ACCEPTANCE_20261008.json'
BASELINE_SHA='d69d5b9d92422969f69156ebf2fca144eba1ca7d8dc78cb76cb2ab83e0f1f7c5'
FINAL_SOURCE=A147/'final_completion_operator_preparation_20261008/final_completion_operator.py'
FINAL_SOURCE_SHA='74eef283454986dcd2d8678465465fab4141896d8bb77b69068a1eda52ca69a8'
FINAL_COMMIT='b2a0447e66c472a61b8d43251fa301e56457a679'
ORIGINAL_HEAD='538fd2584f7dc7375e4eaa91d73daddde3d073cd'
ORIGINAL_MANIFEST=A/'ORIGINAL_SUBMITTED_ATTEMPT_MANIFEST.json'
ORIGINAL_MANIFEST_SHA='efd273eb031989bddae0ae89cad8d2e92cc6f531d2076d20d09155a8b508cb02'
MATHEMATICAL_GATE=A/'ROOT_MATHEMATICAL_GATE_20261008.json'
MATHEMATICAL_GATE_SHA='7c19c3bb1b1ac652360b989655c324ce6b7c241c5780bba91fa91eb073ea7883'
MATHEMATICAL_GATE_REFERENCE='audits/pr148_5100002/ROOT_MATHEMATICAL_GATE_20261008.json'
HEAD='502de2f863a63ca205814da4194411847797a7c3'
MERGE='e8621548039130d471eae99580a29b32925f3c8f'
AUDIT=A.relative_to(C).as_posix()+'/'
PROGRAM={str(PurePosixPath('draft_pr_publication_program_20260930')/p) for p in ('CURRENT_PROGRESS.json','CURRENT_PROGRESS.md','RESEARCH_LOG.md')}
# Load only one immutable audited dependency body; no builders or actual inputs.
body=DEPENDENCY.read_bytes()
if len(body)!=66660 or hashlib.sha256(body).hexdigest()!=DEPENDENCY_SHA:raise RuntimeError('audited dependency mismatch')
n=types.ModuleType('native_gate_audited_mechanisms');n.__file__=str(DEPENDENCY);exec(compile(body,str(DEPENDENCY),'exec'),n.__dict__)
m=types.ModuleType('final_checkpoint_audited_mechanisms');m.__file__=str(DEPENDENCY);exec(compile(body,str(DEPENDENCY),'exec'),m.__dict__);m.D=D
final_body=FINAL_SOURCE.read_bytes()
if len(final_body)!=31924 or hashlib.sha256(final_body).hexdigest()!=FINAL_SOURCE_SHA:raise RuntimeError('audited final baseline source mismatch')
f=types.ModuleType('completed147_final_audited_mechanisms');f.__file__=str(FINAL_SOURCE);exec(compile(final_body,str(FINAL_SOURCE),'exec'),f.__dict__)
require=m.require;pin=m.pin;full_pin=m.full_pin;absolute=m.absolute;canonical=m.canonical;digest=m.digest;sha_value=m.sha_value;oid=m.tree_oid

def path_pin(path):return {'path':str(m.safe(path)),**pin(path)}
def read(spec):return m.read_pinned(spec)
def raw_spec(path):
 spec=path_pin(absolute(path));require(spec['mode']==420,'proposal mode100644');return spec

def relative(value):
 require(isinstance(value,str) and value and '\0' not in value and '\\' not in value,'relative path string')
 p=PurePosixPath(value);require(not p.is_absolute() and str(p)==value and all(x not in ('.','..') for x in p.parts),'canonical relative path')
 require(not any(x.casefold()=='.git' for x in p.parts),'no Git controls in selected overlay');return value

INTAKE='draft_pr_publication_program_20260930/ordered_intake_20261008/after_PR147/'
INTAKE_NAMES={'PR148_STATUS_ONLY.json','intake_status_only.py','ROOT_INTAKE_ACCEPTANCE.json','RESEARCH_LOG.md','INTAKE_AFTER_PR147.json'}
FINAL_AUDIT=A147.relative_to(C).as_posix()+'/'
FINAL_COMPACT={FINAL_AUDIT+p for p in (
 'ROOT_FINAL_METADATA_ACCEPTANCE_20261008.json','ROOT_FINAL_METADATA_PLAN_REVIEW_ACCEPTANCE_20261008.json',
 'ROOT_FINAL_PROGRAM_WRITER_RELEASE_20261008.json','ROOT_FINAL_PROGRAM_INSTALLATION_WRITER_EXCLUSION_20261008.json',
 'final_completion_operator_preparation_20261008/final_completion_operator.py',
 'final_completion_operator_preparation_20261008/REQUEST_CONTRACT.json',
 'final_completion_operator_preparation_20261008/REPORT.md',
 'final_completion_operator_preparation_20261008/SOURCE_PREPARATION_RESULT.json',
 'final_completion_operator_preparation_20261008/FINAL_MANIFEST.json',
 'final_completion_operator_preparation_20261008/FINAL_READBACK.json',
 'final_completion_source_data_plan_adversary_20261008/RESULT.json',
 'final_completion_source_data_plan_adversary_20261008/REPORT.md',
 'final_completion_source_data_plan_adversary_20261008/FINAL_MANIFEST.json',
 'final_completion_source_data_plan_adversary_20261008/FINAL_READBACK.json')}
def scope(artifacts):
 require(isinstance(artifacts,list) and 0<len(artifacts)<=128,'explicit bounded artifact list')
 require(all(isinstance(p,str) for p in artifacts),'typed artifact paths')
 require(len(artifacts)==len(set(artifacts))==len({p.casefold() for p in artifacts}),'unique artifact paths')
 for value in artifacts:
  relative(value)
  if value.startswith(AUDIT):
   parts=PurePosixPath(value[len(AUDIT):]).parts
   require(parts and not any(x.casefold() in {'private','raw','original_submitted_attempt','capture_operations_20261008','primary_sources','cache'} or x.casefold().startswith(('publication_package','raw_','fixture','pure_fixture')) for x in parts),'only compact own148 audit/source artifacts')
   require(parts[-1] not in {'ORIGINAL_PR_PROVIDER.json','ORIGINAL_COMMIT_PROVIDER.json'} and PurePosixPath(value).suffix in {'.json','.md','.py','.txt','.tsv'},'raw third-party and binary artifacts excluded')
  else:require(value in FINAL_COMPACT or value.startswith(INTAKE) and value[len(INTAKE):] in INTAKE_NAMES,'explicit147 final summaries or after147 intake only')
 return PROGRAM|set(artifacts)

def compact(spec):return {k:spec[k] for k in ('bytes','mode','sha256')}

def baseline_acceptance(spec):
 require(spec['path']==str(BASELINE_GATE) and spec['sha256']==BASELINE_SHA,'genuine completed147 FINAL gate exact path/SHA; native/public-only gates rejected')
 gate=m.native_json(read(spec))
 require(gate['schema']=='pr147-root-actual-final-metadata-acceptance/v1' and gate['status']=='ACCEPTED_FINAL_PUBLIC_PACKAGE_AND_LOCAL_PROGRAM3','completed147 final acceptance required')
 require(type(gate['actual_ROOT_PID']) is int and gate['actual_ROOT_PID']>0 and isinstance(gate['UTC'],str) and gate['UTC'],'actual147 ROOT custody')
 require(gate['PR']==147 and gate['original_head']==HEAD and gate['original_merge']==MERGE and gate['final_commit']==FINAL_COMMIT and gate['sole_parent']==gate['native_commit'],'completed147 exact ancestry')
 require(type(gate['fully_completed_count']) is int and gate['fully_completed_count']==26 and type(gate['published_count']) is int and gate['published_count']==14 and type(gate['local_install_path_count']) is int and gate['local_install_path_count']==3,'accepted147 totals26/14 and program3')
 for key in ('public_full_body_mode_readback','local_full_body_mode_readback','whole_parent_tree_preserved_outside_exact_overlay','real_git_controls_preserved','current_native32_preserved','original20_package90_preserved','cooperative_known_selected_writer_exclusion_confirmed','own_operation_lock_released','all_obtained_children_complete'):require(gate[key] is True,'completed147 full acceptance '+key)
 require(gate['original_effort']=='2/5' and type(gate['new_central_proof_search_turns']) is int and gate['new_central_proof_search_turns']==0 and gate['overall_goal_complete'] is False and gate['persistent_goal_status']=='active','faithful completed147 and active persistent goal')
 evidence={key:gate[key] for key in ('source','dependency','plan','request','review','published','installed','independent_ROOT_execution')}
 for value in evidence.values():full_pin(value)
 require(evidence['source']==path_pin(FINAL_SOURCE) and evidence['source']['sha256']==FINAL_SOURCE_SHA and evidence['dependency']==path_pin(DEPENDENCY),'accepted exact immutable final sources')
 plan=m.native_json(read(evidence['plan']));review=m.native_json(read(evidence['review']));pub=m.native_json(read(evidence['published']));ins=m.native_json(read(evidence['installed']));root=m.native_json(read(evidence['independent_ROOT_execution']))
 require(plan['schema']=='pr147-final-program-audit-overlay/v1' and plan['source']==evidence['source'] and plan['dependency']==evidence['dependency'] and plan['request']==evidence['request'] and plan['base_commit']==gate['sole_parent'],'exact accepted147 final plan/request')
 j={'source_sha256':FINAL_SOURCE_SHA,'plan_sha256':evidence['plan']['sha256'],'review_sha256':evidence['review']['sha256'],'request_sha256':evidence['request']['sha256'],'native_acceptance_sha256':plan['native_acceptance']['sha256']}
 commit,object_root=f.prior_public(pub,plan,j);require(commit==FINAL_COMMIT,'completed147 final-public receipt')
 require(review['schema']=='pr147-final-checkpoint-source-plan-review/v1' and review['actual_review'] is True and review['verdict']=='PASS' and review['mandatory_findings']==[] and review['actual_native_final_gate_authenticated'] is True and review['actual_postimage_data_and_current_protections_authenticated'] is True,'actual147 final source/data/plan review')
 for key,expected in (('source_sha256',FINAL_SOURCE_SHA),('dependency_sha256',DEPENDENCY_SHA),('plan_sha256',evidence['plan']['sha256']),('request_sha256',evidence['request']['sha256']),('native_acceptance_sha256',plan['native_acceptance']['sha256'])):require(review[key]==expected,'accepted147 review '+key)
 require(ins['schema']=='pr147-final-checkpoint-operation-receipt/v1' and ins['status']=='public_and_program_install_verified' and ins['action']=='install' and ins['fixture_only'] is False and ins['published_commit']==FINAL_COMMIT and ins['own_operation_lock_released'] is True and 'error_type' not in ins,'completed147 actual program installation')
 for key,expected in j.items():require(ins[key]==expected,'completed147 installer '+key)
 require(ins['local_full_body_mode_readback'] is True and type(ins['local_readback_path_count']) is int and ins['local_readback_path_count']==3 and set(ins['installed'])==PROGRAM and ins['known_selected_writer_exclusion_confirmed'] is True and f.m.children_custody_complete(ins),'completed147 all3 local bodies/custody')
 for child in ins['children']:f.m.authenticate_child_custody(child);require(child['exit_code']==0,'successful147 installer child')
 require(evidence['independent_ROOT_execution']['path']==str(FINAL_SOURCE.parent/'private/ROOT_ACTUAL_FINAL_READBACK_01/RECEIPT.json'),'genuine147 final ROOT readback path')
 require(root['schema']=='pr147-root-actual-final-checkpoint-readback/v1' and root['status']=='PASS' and root['actual_ROOT_PID']==gate['actual_ROOT_PID'] and root['final_commit']==FINAL_COMMIT and root['local_readback_path_count']==3 and root['current_native32_preserved'] is True and root['original20_package90_preserved'] is True and root['real_git_controls_preserved'] is True and f.m.children_custody_complete(root),'independent147 final readback')
 for key,expected in j.items():require(root[key]==expected,'completed147 independent ROOT '+key)
 for child in root['children']:f.m.authenticate_child_custody(child);require(child['exit_code']==0,'successful147 independent ROOT child')
 native=f.native_acceptance(plan['native_acceptance']);require(native==plan['native'],'current147 native32 and accepted original20/package90 custody')
 members=[v for v in plan['members'] if v['path'] in PROGRAM];require(len(members)==3 and set(v['path'] for v in members)==PROGRAM,'accepted147 final program3')
 program={str(C/v['path']):v['post'] for v in members}
 for path,value in program.items():m.check(path,value)
 require({v['path']:compact(v) for v in ins['installed_postimages']}==program and {v['path']:compact(v) for v in root['local_program_readbacks']}==program,'exact accepted147 final program3 body/mode proof')
 original_spec=path_pin(ORIGINAL_MANIFEST);require(original_spec['bytes']==5703 and original_spec['mode']==420 and original_spec['sha256']==ORIGINAL_MANIFEST_SHA,'immutable original148 manifest')
 original=m.native_json(read(original_spec));require(original['schema']=='pr148-original-source-manifest/v1' and original['PR']==148 and original['original_head']==ORIGINAL_HEAD and original['original_effort']=='1/5' and original['literal_original_status']=='claimed_solved' and original['original_author_turn_ledger_present'] is False and original['original_native_transition_ledger_present'] is False and original['new_central_proof_search_turns']==0,'original148 one approach summary is not author/native turn ledger')
 files=[];directories=set()
 for member in original['original_files']:
  path=relative(member['path']);files.append({'relative':path,**compact(member)})
  directories.update(p.as_posix() for p in PurePosixPath(path).parents if str(p)!='.')
 require(len(files)==20 and len({v['relative'] for v in files})==20,'immutable original14820')
 original_dir={'path':str(A/'original_submitted_attempt'),'files':sorted(files,key=lambda v:v['relative']),'directories':sorted(directories)}
 m.closed_directory(original_dir)
 approach_pin=path_pin(A/'original_submitted_attempt/turns.json');approach=m.native_json(read(approach_pin))
 require(isinstance(approach,list) and len(approach)==1 and isinstance(approach[0],dict) and type(approach[0]['family']) is int and approach[0]['family']==1 and isinstance(approach[0]['mechanism'],str) and approach[0]['mechanism'].strip() and isinstance(approach[0]['result'],str) and approach[0]['result'].strip(),'original148 one substantive approach summary present; no timestamped chat turn reconstructed')
 return {**native,'gate':path_pin(BASELINE_GATE),'program_preimages':program,'completed147_commit':FINAL_COMMIT,'object_workspace':object_root,'final_source':path_pin(FINAL_SOURCE),'final_evidence_pins':evidence,'original148_manifest':original_spec,'original148_directory':original_dir,'original148_author_approach_ledger_present':True,'original148_author_approach_ledger_path':'turns.json','original148_substantive_author_approach_count':1,'original148_approach_ledger_source':approach_pin,'actual_timestamped_author_chat_turn_ledger_present':False}

def mathematical_gate_source():
 spec=path_pin(MATHEMATICAL_GATE)
 require(spec['bytes']==28807 and spec['mode']==420 and spec['sha256']==MATHEMATICAL_GATE_SHA,'genuine ROOT148 mathematical gate whole body/mode/SHA')
 gate=m.native_json(read(spec))
 require(gate['schema']=='pr148-root-mathematical-gate/v1' and gate['status']=='PASS_LITERAL_K108_COUNTEREXAMPLE' and gate['mathematical_clearance'] is True and gate['mandatory_mathematical_findings']==[],'actual ROOT148 mathematical acceptance')
 require(type(gate['actual_ROOT_PID']) is int and gate['actual_ROOT_PID']>0 and isinstance(gate['UTC'],str) and gate['UTC'] and gate['PR']==148 and gate['original_head']==ORIGINAL_HEAD,'actual ROOT148 gate identity/custody')
 require(type(gate['mathematical_audit_percent']) is int and gate['mathematical_audit_percent']==100 and type(gate['PR148_best_guess_workflow_percent']) is int and gate['PR148_best_guess_workflow_percent']==30,'ROOT148 mathematical audit100 and workflow30')
 require(gate['native_acceptance'] is None and gate['priority_acceptance'] is None and gate['publication_acceptance'] is None and gate['persistent_goal_complete'] is False,'mathematical acceptance distinct from pending final native/publication/priority')
 require(gate['original_effort']=='1/5' and gate['original_author_approach_ledger_present'] is True and gate['original_author_approach_ledger_path']=='turns.json' and type(gate['original_reported_substantive_approach_count']) is int and gate['original_reported_substantive_approach_count']==1 and gate['actual_timestamped_author_chat_turn_ledger_present'] is False and gate['original_native_transition_ledger_present'] is False and type(gate['new_central_proof_search_turns']) is int and gate['new_central_proof_search_turns']==0 and gate['original20_preserved'] is True,'faithful accepted mathematical original148 provenance')
 return spec

def active_program(data,prior):
 current=m.native_json(data);old=m.native_json(prior)
 for key,count in (('fully_completed_count',26),('published_count',14)):require(type(current[key]) is int and current[key]==old[key]==count,'active148 totals remain26/14')
 for key in ('fully_completed_eligible_PRs','published_PRs','closed_without_publication_PRs','accepted_partial_prior_result_PRs','accepted_partial_priority_unestablished_PRs','skipped_since_last_completion','status_only_skips_before_PR134_completion'):require(current[key]==old[key],'preserve previous case ledger '+key)
 require(type(current['current_PR']) is int and current['current_PR']==148 and str(current['current_problem_id'])=='5100002' and current['current_code']=='AMR-050-0002' and current['current_original_head']==ORIGINAL_HEAD and current['current_original_budget']=='1/5' and current['current_original_literal_status']=='claimed_solved','literal active148 identity/effort')
 require(current['current_original_author_approach_ledger_present'] is True and current['current_original_author_approach_ledger_path']=='turns.json' and type(current['current_original_substantive_author_approach_count']) is int and current['current_original_substantive_author_approach_count']==1,'original148 actual one substantive approach ledger')
 require(current['current_actual_timestamped_author_chat_turn_ledger_present'] is False and current['current_original_native_transition_ledger_present'] is False and type(current['current_new_central_proof_search_turns']) is int and current['current_new_central_proof_search_turns']==0,'no invented148 timestamped chat/native turn ledgers or new proofsearch')
 for key in ('current_core_disposition_complete','current_priority_clearance','current_publication_ready','current_Zenodo_published','current_tracker_updated','current_novelty_established','current_absolute_priority_established','current_exclusive_priority_established','current_independent_discovery_established','current_copying_or_collaboration_inferred','current_closed_without_merging','current_closed_without_publication'):require(current[key] is False,'active148 no acceptance '+key)
 for key in ('current_DOI','current_tracker_range','current_native_completion_acceptance','current_native_completion_acceptance_sha256','current_native_disposition_checkpoint_commit','active_checkpoint_acceptance_receipt','active_checkpoint_commit'):require(current[key] is None,'active148 no invented future actual fact '+key)
 for key in ('current_native_local_installed_path_count','current_native_public_changed_path_count'):require(type(current[key]) is int and current[key]==0,'active148 native untouched '+key)
 require(current['last_completed_PR']==147 and current['last_published_PR']==147 and current['persistent_goal_complete'] is False and current['persistent_goal_status']=='active','completed147 retained and persistent goal active')
 for key in ('active_checkpoint_publication_performed_by_this_preparation','active_checkpoint_local_installation_performed_by_this_preparation','advance_to_next_PR_authorized_now'):require(current[key] is False,'active148 publication/installation/intake not preclaimed '+key)
 require(current['current_active_checkpoint_pending'] is True and current['active_checkpoint_actual_readback_required'] is True and current['active_checkpoint_source_plan_review_required'] is True,'conditional active148 checkpoint only')
 require(current['current_mathematical_clearance'] is True and current['current_mathematical_gate']==MATHEMATICAL_GATE_REFERENCE and current['current_mathematical_gate_sha256']==MATHEMATICAL_GATE_SHA,'actual accepted ROOT148 mathematical gate recorded')
 require(type(current['current_mathematical_audit_percent']) is int and current['current_mathematical_audit_percent']==100 and type(current['current_PR_workflow_percent']) is int and current['current_PR_workflow_percent']==30 and type(current['current_workflow_estimate_percent']) is int and current['current_workflow_estimate_percent']==30,'accepted mathematical audit100 and pending workflow30')
 return current

def protection(plan,check_bodies=True):
 files=plan['protected'];absences=plan['protected_absences'];dirs=plan['protected_directories']
 require(isinstance(files,list) and isinstance(absences,list) and isinstance(dirs,list),'complete protection lists')
 present={v['path'] for v in files};absent=set(absences);roots={v['path'] for v in dirs}
 require(len(present)==len(files) and len(absent)==len(absences) and not present&absent and len(roots)==len(dirs),'unique protection inventory')
 require(len(present|absent)==len({p.casefold() for p in present|absent}),'protection case aliases')
 required={str(root/'.git'/name) for root in (R,C) for name in n.GIT_FILES+n.GIT_LOCKS}
 required|={str(R/'unsolved_math_prioritization'/name) for name in n.BACKEND+('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}
 required|={str(R/p) for p in PROGRAM}|{str(C/'unsolved_math_prioritization'/name) for name in ('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}
 required|={v['pin']['path'] for v in plan['native']['native_members']}
 require(required<=present|absent,'full current real/native32/program protections')
 require({str(root/'.git'/name) for root in (R,C) for name in n.GIT_LOCKS}<=absent,'real writer locks absent')
 require({str(C/'unsolved_math_prioritization'/name) for name in ('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}<=absent,'C backend-source/cache remain absent')
 require({v['pin']['path'] for v in plan['native']['native_members']}<=present,'all actual native32 must stay present')
 native_pins={v['pin']['path']:v['pin'] for v in plan['native']['native_members']};protected_pins={v['path']:v for v in files}
 require(all(protected_pins[p]==v for p,v in native_pins.items()),'native32 protected pins equal accepted installed bodies')
 require({str(R/'unsolved_math_prioritization'/name) for name in n.BACKEND+('queue.py','manifest.json','policy.json','cache/catalog.sqlite')}<=present,'R backend/source/cache must remain present')
 require(str(R/'draft_pr_publication_program_20260930/CURRENT_PROGRESS.md') in absent,'R progress document remains absent')
 require(not {str(C/p) for p in PROGRAM}&(present|absent),'selected C program preimages are separate mutable protection')
 required_roots={str(root/'.git/refs') for root in (R,C)}|{str(R/'unsolved_math_prioritization/cache'),str(A147/'original_submitted_attempt'),str(A147/'publication_package_v2'),str(A/'original_submitted_attempt'),str(C/n.ATTEMPT_PREFIX.rstrip('/')),plan['postimage_root']}
 require(required_roots<=roots,'closed refs/cache/original20/package90/native24/postimage protections')
 for accepted in plan['native']['original_package_directories']+[plan['native']['original148_directory']]:
  require(next(v for v in dirs if v['path']==accepted['path'])==accepted,'immutable accepted147 original20/package90 and148 original20 bodies')
 for root in roots:
  absolute(root);require(not any(Path(root)==C/p or Path(root) in (C/p).parents for p in PROGRAM),'immutable directory cannot contain selected C program files')
  require(Path(root)!=D/'private' and not (D/'private').is_relative_to(Path(root)),'action receipts outside immutable roots')
 if check_bodies:
  for value in files:full_pin(value)
  for value in absences:require(not m.local_case_guard(value).exists(),'protected absence changed')
  for value in dirs:m.closed_directory(value)


def proposal(request_spec):
 q=m.native_json(read(request_spec))
 fields={'schema','baseline_acceptance','fresh_base_commit','R_HEAD','C_HEAD','git_executable','gh_executable','postimage_root','artifact_paths','postimages','remote_preimages','program_preimages','protected','protected_absences','protected_directories','commit_message'}
 require(set(q)==fields and q['schema']=='pr148-active-checkpoint-request/v1','exact actual final request contract')
 selected=scope(q['artifact_paths']);require(set(q['postimages'])==set(q['remote_preimages'])==selected and set(q['program_preimages'])==PROGRAM,'exact selected/three-program inventories')
 native=baseline_acceptance(q['baseline_acceptance']);math_gate=mathematical_gate_source();root=absolute(q['postimage_root']);require(D/'private' in root.parents,'immutable future postimage root')
 members=[];total=0
 for path in sorted(selected):
  spec=q['postimages'][path];full_pin(spec);require(spec['path']==str(root/path) and spec['mode']==420 and spec['bytes']<=256*1024,'bounded exact postimage source')
  data=read(spec);total+=len(data);pre=q['remote_preimages'][path]
  if path.endswith('/CURRENT_PROGRESS.json') and path in PROGRAM:active_program(data,Path(C/path).read_bytes())
  if path.endswith('/RESEARCH_LOG.md') and path in PROGRAM:require(data.startswith(Path(C/path).read_bytes()),'program research log append preserves full prior bytes')
  if pre is not None:
   require(set(pre)=={'bytes','mode','sha256','Git_blob'} and type(pre['bytes']) is int and pre['bytes']>=0 and type(pre['mode']) is int and pre['mode']==420,'typed remote preimage');sha_value(pre['sha256']);oid(pre['Git_blob'])
   require(pre['sha256']!=spec['sha256'],'every selected remote path must change')
  local=q['program_preimages'][path] if path in PROGRAM else None
  if path in PROGRAM:
   require(isinstance(local,dict) and set(local)=={'bytes','mode','sha256'} and type(local['bytes']) is int and local['bytes']>=0 and type(local['mode']) is int and local['mode']==420,'complete current C program preimages')
   sha_value(local['sha256']);require(local==native['program_preimages'][str(C/path)],'unchanged native-accepted C program preimage');m.check(C/path,local)
  members.append({'path':path,'source':spec['path'],'storage':{'encoding':'raw','pin':spec},'post':compact(spec),'post_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),'remote_pre':pre,'local_pre':local,'install':path in PROGRAM})
 require(total<=8*1024*1024,'small final overlay; no backend/package duplication')
 message=q['commit_message'];require(isinstance(message,str) and message.strip()==message and '148' in message and '\0' not in message,'scoped commit message')
 p={'schema':'pr148-active-program-audit-overlay/v1','source':path_pin(Path(__file__).resolve()),'dependency':path_pin(DEPENDENCY),'request':request_spec,'baseline_acceptance':q['baseline_acceptance'],'mathematical_gate':math_gate,'native':native,'base_commit':oid(q['fresh_base_commit']),
 'R_HEAD':oid(q['R_HEAD']),'C_HEAD':oid(q['C_HEAD']),'git_executable':q['git_executable'],'gh_executable':q['gh_executable'],'postimage_root':str(root),'artifact_paths':q['artifact_paths'],'members':members,'program_paths':sorted(PROGRAM),
 'protected':q['protected'],'protected_absences':q['protected_absences'],'protected_directories':q['protected_directories'],'commit_message':message,'new_central_proof_search_turns':0,'overall_goal_completion_claimed':False,'PR148_native_publication_acceptance_claimed':False,'original148_effort':'1/5','original148_author_approach_ledger_present':True,'original148_author_approach_ledger_path':'turns.json','original148_substantive_author_approach_count':1,'actual_timestamped_author_chat_turn_ledger_present':False,'original148_native_transition_ledger_present':False}
 require(p['source']['path']==str(D/'active_checkpoint_operator_v3.py'),'fixed final operator source path')
 require(p['git_executable']['path']==n.G and p['gh_executable']['path']==n.GH,'fixed audited executable paths');full_pin(p['git_executable']);full_pin(p['gh_executable']);protection(p)
 return p

def guard(plan,j):
 for value in (plan['source'],plan['dependency'],plan['request'],plan['baseline_acceptance'],plan['mathematical_gate'],plan['native']['final_source'],plan['native']['original148_manifest'],plan['git_executable'],plan['gh_executable']):full_pin(value)
 protection(plan)
 for member in plan['members']:m.read_postimage(member)
 for root,expected in ((R,plan['R_HEAD']),(C,plan['C_HEAD'])):require(m.git(['rev-parse','HEAD','refs/heads/main'],j,root=root).decode().splitlines()==[expected,expected],'real HEAD/main unchanged')

def local_preimages(plan):
 for member in plan['members']:
  if member['install']:m.check(C/member['path'],member['local_pre'])

def load(plan_path,plan_sha,review_path,review_sha):
 raw=read({'path':str(absolute(plan_path)),**pin(plan_path)});require(digest(raw)==sha_value(plan_sha),'explicit whole plan SHA');p=m.native_json(raw)
 require(p['schema']=='pr148-active-program-audit-overlay/v1' and p['source']['sha256']==digest(Path(__file__).read_bytes()),'exact running final source')
 review_body=absolute(review_path).read_bytes();require(digest(review_body)==sha_value(review_sha),'independent complete review SHA');v=m.native_json(review_body)
 require(v['schema']=='pr148-active-checkpoint-source-plan-review/v1' and v['verdict']=='PASS' and v['mandatory_findings']==[] and v['actual_review'] is True and v['actual_completed147_final_gate_authenticated'] is True and v['actual_PR148_mathematical_gate_authenticated'] is True and v['actual_postimage_data_and_current_protections_authenticated'] is True,'fresh independent actual final source/data/plan PASS')
 require(type(v['actual_reviewer_PID']) is int and v['actual_reviewer_PID']>0 and v['actual_reviewer_PID']!=os.getpid() and isinstance(v['reviewer_identity'],str) and v['reviewer_identity'].strip()==v['reviewer_identity'] and v['reviewer_identity'],'actual independent reviewer identity')
 for key,expected in (('source_sha256',p['source']['sha256']),('dependency_sha256',DEPENDENCY_SHA),('final_baseline_source_sha256',FINAL_SOURCE_SHA),('request_sha256',p['request']['sha256']),('baseline_acceptance_sha256',p['baseline_acceptance']['sha256']),('mathematical_gate_sha256',p['mathematical_gate']['sha256']),('plan_sha256',plan_sha),('postimage_root',p['postimage_root'])):require(v[key]==expected,'exact review '+key)
 require(v['local_install_path_count']==3 and type(v['local_install_path_count']) is int and type(v['remote_changed_path_count']) is int and v['remote_changed_path_count']==len(p['members']),'exact reviewed final scopes')
 require(canonical(proposal(p['request']))==raw,'canonical deterministic exact final plan replay');return p

def workspace(plan,j,run_dir):
 m.initialize_object_workspace(j,run_dir)
 # Replace only our own initial alternate file, after durable explicit intent.
 path=Path(j['object_workspace'])/'objects/info/alternates';old=path_pin(path);alternate=absolute(plan['native']['object_workspace'])/'objects';m.safe(alternate);require(alternate.is_dir(),'native actual private objects alternate')
 data=(str(alternate)+'\n').encode();j['completed147_readonly_alternate_intent']={'path':str(path),'prior':old,'new_body_sha256':digest(data),'state':'intended'};m.dump(run_dir/'RECEIPT.json',j)
 temporary=path.with_name('alternates.active.tmp');fd=os.open(temporary,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,420)
 try:
  os.fchmod(fd,420);info=os.fstat(fd);j['completed147_readonly_alternate_intent'].update(temporary_path=str(temporary),temporary_identity={'dev':info.st_dev,'ino':info.st_ino},state='temporary_created');m.dump(run_dir/'RECEIPT.json',j)
  view=memoryview(data)
  while view:
   written=os.write(fd,view);require(written>0,'alternate write progress');view=view[written:];j['completed147_readonly_alternate_intent']['written_bytes']=len(data)-len(view)
  os.fsync(fd)
 finally:os.close(fd)
 info=temporary.lstat();require(j['completed147_readonly_alternate_intent']['temporary_identity']=={'dev':info.st_dev,'ino':info.st_ino} and stat.S_ISREG(info.st_mode) and info.st_nlink==1,'owned alternate temporary inode');m.check(temporary,{'bytes':len(data),'mode':420,'sha256':digest(data)})
 m.check(path,old);os.replace(temporary,path);j['completed147_readonly_alternate_intent'].update(state='replaced',temporary_transferred_to_target=True);m.dump(run_dir/'RECEIPT.json',j)
 m.check(path,{'bytes':len(data),'mode':420,'sha256':digest(data)});j['completed147_readonly_alternate_intent']['post']=path_pin(path);m.dump(run_dir/'RECEIPT.json',j)
 # No fetch route: missing current base/native closure stops before push.
 m.git(['cat-file','-e',plan['base_commit']+'^{commit}'],j);m.git(['merge-base','--is-ancestor',plan['native']['completed147_commit'],plan['base_commit']],j);m.git(['merge-base','--is-ancestor',HEAD,plan['base_commit']],j)

def record(member,post=False):return m.expected_tree_record(member,post)
def remote_preimages(plan,j):
 for member in plan['members']:
  require(m.git(['ls-tree','-z',plan['base_commit'],'--',member['path']],j)==record(member),'selected remote preimage path/mode/blob')
  if member['remote_pre'] is not None:
   data=m.git(['cat-file','blob',member['remote_pre']['Git_blob']],j);require(len(data)==member['remote_pre']['bytes'] and digest(data)==member['remote_pre']['sha256'],'complete selected small remote preimage')
 for member in plan['native']['native_members']:
  require(m.git(['ls-tree','-z',plan['base_commit'],'--',member['path']],j)==('100644 blob '+member['post_blob']+'\t'+member['path']+'\0').encode(),'preserve native32 public tree')

def tree(plan,j):
 for member in plan['members']:require(m.tree_oid_output(m.git(['hash-object','-w','--stdin'],j,data=m.read_postimage(member)))==member['post_blob'],'exact final blob')
 base=m.tree_oid_output(m.git(['rev-parse',plan['base_commit']+'^{tree}'],j))
 proposed=m.sparse_overlay_tree(base,{x['path']:x['post_blob'] for x in plan['members']},lambda x:m.git(['ls-tree','-z',x],j),lambda x:m.tree_oid_output(m.git(['mktree','-z'],j,data=x)))
 changes=m.git(['diff','--no-ext-diff','--no-textconv','--no-renames','--name-only','-z',plan['base_commit'],proposed],j).split(b'\0')
 require(changes[-1]==b'' and sorted(x.decode() for x in changes[:-1])==sorted(x['path'] for x in plan['members']),'whole parent tree exact selected overlay only')
 return proposed

def public_readback(plan,j,commit):
 require(m.remote(j)==commit,'direct main must remain exact final commit')
 for member in plan['members']:
  require(m.git(['ls-tree','-z',commit,'--',member['path']],j)==record(member,True),'public final path/mode/blob')
  raw=m.native_json(m.run([n.GH,'api','repos/AlecKriebel/Math/git/blobs/'+member['post_blob']],j));require(raw['sha']==member['post_blob'] and raw['encoding']=='base64' and type(raw['size']) is int and raw['size']==member['post']['bytes'],'provider final blob identity')
  data=base64.b64decode(raw['content'].replace('\n',''),validate=True);require(len(data)==member['post']['bytes'] and digest(data)==member['post']['sha256'],'complete final public body')
  j.setdefault('public_readbacks',[]).append({'path':member['path'],**member['post'],'Git_blob':member['post_blob']})
 require(m.remote(j)==commit,'direct main unchanged after full public readback')

def publish(plan,j,run_dir):
 guard(plan,j);local_preimages(plan);require(m.remote(j)==plan['base_commit'],'fresh main changed; no retry')
 workspace(plan,j,run_dir);remote_preimages(plan,j);proposed=tree(plan,j)
 commit=m.tree_oid_output(m.git(['commit-tree',proposed,'-p',plan['base_commit']],j,data=(plan['commit_message']+'\n').encode()))
 data=m.git(['cat-file','commit',commit],j);headers=data.split(b'\n\n',1)[0].splitlines()
 require([h for h in headers if h.startswith(b'parent ')]==[b'parent '+plan['base_commit'].encode()] and [h for h in headers if h.startswith(b'tree ')]==[b'tree '+proposed.encode()],'sole exact final parent/tree')
 j.update(proposed_commit=commit,tree=proposed,status='push_dispatch_pending');m.dump(run_dir/'RECEIPT.json',j)
 guard(plan,j);local_preimages(plan);require(m.remote(j)==plan['base_commit'],'dispatch direct-main guard')
 j['status']='push_outcome_unresolved';m.dump(run_dir/'RECEIPT.json',j)
 m.git(['push','--no-verify','--no-follow-tags',n.URL,commit+':refs/heads/main'],j)
 j.update(published_commit=commit,status='public_published_program_install_pending_readback');m.dump(run_dir/'RECEIPT.json',j)
 public_readback(plan,j,commit);guard(plan,j);local_preimages(plan)
 j.update(status='published_program_install_pending',public_full_body_mode_readback=True,remote_changed_path_count=len(plan['members']),local_install_path_count=3,whole_parent_tree_preserved_outside_exact_overlay=True,sole_parent=plan['base_commit'])

def prior_public(prior,plan,j):
 require(prior['schema']=='pr148-active-checkpoint-operation-receipt/v1' and prior['action']=='publish' and prior['status']=='published_program_install_pending' and prior['fixture_only'] is False and 'error_type' not in prior and prior['own_operation_lock_released'] is True,'actual completed final public receipt')
 for key in ('source_sha256','plan_sha256','review_sha256','request_sha256','baseline_acceptance_sha256','mathematical_gate_sha256'):require(prior[key]==j[key],'same reviewed final publication '+key)
 require(type(prior['actual_PID']) is int and prior['actual_PID']>0 and m.children_custody_complete(prior) and prior['children'],'actual closed final publication children')
 require(prior['public_full_body_mode_readback'] is True and prior['whole_parent_tree_preserved_outside_exact_overlay'] is True and prior['sole_parent']==plan['base_commit'] and type(prior['remote_changed_path_count']) is int and prior['remote_changed_path_count']==len(plan['members']) and type(prior['local_install_path_count']) is int and prior['local_install_path_count']==3,'exact final public proof/scopes')
 for child in prior['children']:m.authenticate_child_custody(child);require(child['exit_code']==0,'successful final publisher child')
 root=absolute(prior['object_workspace']);require(D/'private' in root.parents and root.name=='object_workspace' and root.is_dir(),'prior final-public private workspace')
 return oid(prior['published_commit']),str(root)

def install(plan,j,run_dir,path,sha,exclusive):
 require(exclusive is True,'ROOT must confirm cooperative exclusion of all selected program writers now')
 spec=path_pin(absolute(path));require(spec['sha256']==sha_value(sha),'explicit whole final-public receipt SHA')
 prior=m.native_json(read(spec));commit,root=prior_public(prior,plan,j);j.update(object_workspace=root,published_commit=commit,known_selected_writer_exclusion_confirmed=True,status='public_program_install_pending',installed=[])
 guard(plan,j);local_preimages(plan);public_readback(plan,j,commit)
 j['published_receipt']=spec;m.dump(run_dir/'RECEIPT.json',j)
 for member in plan['members']:
  if member['install']:m.install_one(member,j,run_dir)
 installed=[]
 for member in plan['members']:
  if member['install']:
   spec=path_pin(C/member['path']);require(compact(spec)==member['post'],'complete installed program body/mode');installed.append(spec)
 require(len(installed)==3 and set(j['installed'])==PROGRAM,'exact three installed selected program files')
 guard(plan,j);require(m.remote(j)==commit,'final direct main unchanged after local install')
 j.update(status='public_and_program_install_verified',local_full_body_mode_readback=True,local_readback_path_count=3,installed_postimages=installed,whole_install_atomic=False,compare_and_swap_claimed=False,overall_goal_completion_claimed=False,independent_ROOT_active_checkpoint_acceptance_pending=True)

def operation(args):
 run_dir=absolute(args.run_dir);require(run_dir.parent==D/'private','fresh operation run-directory scope');run_dir.mkdir(exist_ok=False)
 j={'schema':'pr148-active-checkpoint-operation-receipt/v1','actual_PID':os.getpid(),'UTC_start':m.utc(),'action':args.action,'children':[],'child_custody_root':str(run_dir/'raw'),'source_sha256':digest(Path(__file__).read_bytes()),'dependency_sha256':DEPENDENCY_SHA,'final_baseline_source_sha256':FINAL_SOURCE_SHA,'plan_sha256':args.plan_sha,'review_sha256':args.review_sha,'fixture_only':False,'status':'starting','auto_retry_performed':False,'overall_goal_completion_claimed':False,'PR148_native_publication_acceptance_claimed':False,'original148_effort':'1/5','original148_author_approach_ledger_present':True,'original148_author_approach_ledger_path':'turns.json','original148_substantive_author_approach_count':1,'actual_timestamped_author_chat_turn_ledger_present':False,'original148_native_transition_ledger_present':False}
 lock=D/'private/OPERATION_LOCK.json';identity=None;owned=None
 try:
  m.local_case_guard(lock);fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,420)
  try:
   info=os.fstat(fd);identity=(info.st_dev,info.st_ino);j['operation_lock_identity']={'dev':info.st_dev,'ino':info.st_ino}
   view=memoryview(canonical({'actual_PID':os.getpid(),'UTC':m.utc(),'plan_sha256':args.plan_sha}))
   while view:written=os.write(fd,view);require(written>0,'owned lock write progress');view=view[written:]
   os.fsync(fd)
  finally:os.close(fd)
  owned=path_pin(lock);j['operation_lock']=owned;j['status']='plan_validation_pending';m.dump(run_dir/'RECEIPT.json',j);plan=load(args.plan,args.plan_sha,args.review,args.review_sha);j.update(request_sha256=plan['request']['sha256'],baseline_acceptance_sha256=plan['baseline_acceptance']['sha256'],mathematical_gate_sha256=plan['mathematical_gate']['sha256']);j['status']='actual_plan_authenticated';m.dump(run_dir/'RECEIPT.json',j)
  if args.action=='publish':publish(plan,j,run_dir)
  else:install(plan,j,run_dir,args.published_receipt,args.published_receipt_sha,args.exclusive_known_writers_confirmed)
 except BaseException as error:
  j.update(error_type=type(error).__name__,error=str(error)[:4096])
  if isinstance(error,m.JournalWriteFailure):j['journal_write_failure']=error.journal_write_failure
  if j.get('published_commit'):j['failure_state']='public_published_program_install_pending'
  raise
 finally:
  safe=m.children_custody_complete(j);j['all_obtained_children_complete']=safe
  if identity is not None and safe:
   try:
    m.safe(lock);info=lock.lstat();require((info.st_dev,info.st_ino)==identity,'owned operation lock inode');require(owned is not None,'owned lock body pin unavailable; retain barrier');full_pin(owned);lock.unlink();j['own_operation_lock_released']=True
   except BaseException as error:j.update(own_operation_lock_released=False,lock_release_error=str(error))
  elif identity is not None:j.update(own_operation_lock_released=False,lock_retained_for_unresolved_custody=True)
  j['UTC_end']=m.utc()
  try:m.dump(run_dir/'RECEIPT.json',j)
  except BaseException:
   print(json.dumps({'final_receipt_persistence_failed':True,'journal':j},sort_keys=True));raise
 require(j.get('own_operation_lock_released') is True,'owned barrier release incomplete')
 print(json.dumps({'status':j['status'],'receipt':path_pin(run_dir/'RECEIPT.json')}))

def main():
 parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='action',required=True)
 for action in ('plan-sha','prepare'):
  p=sub.add_parser(action);p.add_argument('--request',required=True);p.add_argument('--request-sha',required=True)
  if action=='prepare':p.add_argument('--expected-plan-sha',required=True);p.add_argument('--plan',required=True)
 for action in ('publish','install'):
  p=sub.add_parser(action)
  for key in ('plan','plan-sha','review','review-sha','run-dir'):p.add_argument('--'+key,required=True)
  if action=='install':p.add_argument('--published-receipt',required=True);p.add_argument('--published-receipt-sha',required=True);p.add_argument('--exclusive-known-writers-confirmed',action='store_true')
 args=parser.parse_args()
 if args.action in ('plan-sha','prepare'):
  spec=path_pin(absolute(args.request));require(spec['sha256']==sha_value(args.request_sha),'explicit complete actual request SHA');plan=proposal(spec);data=canonical(plan);sha=digest(data)
  if args.action=='prepare':
   require(sha==sha_value(args.expected_plan_sha),'exact expected plan SHA');path=absolute(args.plan);require(D/'private' in path.parents and not path.exists(),'fresh private canonical plan')
   with path.open('xb') as handle:handle.write(data);handle.flush();os.fchmod(handle.fileno(),420);os.fsync(handle.fileno())
   require(path.read_bytes()==data,'whole prepared plan readback')
  print(json.dumps({'status':'PLAN_ONLY_NOT_PR148_ACCEPTANCE','plan_sha256':sha,'remote_paths':len(plan['members']),'local_install_paths':3}))
 else:operation(args)
if __name__=='__main__':main()

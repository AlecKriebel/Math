"""Ordinary scoped main checkpoint, executed only after actual writer handoff."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
A=Path(__file__).resolve().parent
P=A.parent.parent
C=P.parent
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
BASE=sys.argv[1]
D=A/'actual_math_checkpoint_20261006'
PRIVATE={'private_sources','private_renders','private_backend','pdfs','tmp','__pycache__'}
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise ValueError(label)
def sha(body):return hashlib.sha256(body).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(args):
    start=now()
    child=subprocess.Popen([GIT,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    events.append({'argv':[GIT,*args],'PID':child.pid,'UTC_start':start,'UTC_end':now(),
      'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),
      'small_stdout':out.decode('utf-8','replace') if len(out)<1200 else None,
      'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf-8','replace')})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,'Actual Git action failed; inspect journal before retry')
    return out
def pin(path):
    require(path.is_relative_to(C) and path.is_file() and not path.is_symlink(),'Public regular file required')
    require(not PRIVATE.intersection(path.parts),'Private source/render selected')
    body=path.read_bytes()
    return {'path':str(path.relative_to(C)),'bytes':len(body),'sha256':sha(body)}
require(not D.exists(),'Existing actual checkpoint; inspect rather than repeat')
D.mkdir()
window=json.loads((A/'ACTUAL_WRITER_HANDOFF_20261006.json').read_text())
require(window['explicit_release_received'] and window['remote_main']==BASE,'Actual writer release/base required')
require(run(['branch','--show-current']).strip()==b'main','Not main')
require(run(['rev-parse','HEAD']).decode().strip()==BASE,'Local base changed')
require(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==BASE,'Remote base changed')
require(not run(['diff','--cached','--name-only']),'Index not empty')
gate=json.loads((A/'MATHEMATICAL_SOURCE_GATE_20261006.json').read_text())
require(gate['status']=='PASS' and gate['original_attempts']=='1/5','Math/source gate mismatch')
ready=json.loads((A/'ROOT_DISPOSITION_READY_20261006.json').read_text())
require(ready['fresh_disposition_review_PASS'] and ready['exact_prior_same_example_authenticated'],'Fresh priority disposition gate required')
previous=P/'audits/pr111_4900006'
release=json.loads((previous/'FINAL_COMPLETION_OWNER_RELEASE_20261006.json').read_text())
require(release['writer_ownership_released'] and release['completion_metadata_commit']=='b1431b74e93b4b55d981a654d5cdd6badccbd0ae','PR111 actual final release missing')
progress_path=P/'CURRENT_PROGRESS.json'
old=progress_path.read_bytes()
data=json.loads(old)
require(data['fully_completed_count']==19 and data['last_completed_PR']==111,'Unexpected completed cursor')
snapshot=A/'PR111_COMMITTED_PROGRESS_AT_PR117_CHECKPOINT_20261006.json'
require(not snapshot.exists(),'Existing prior progress snapshot')
snapshot.write_bytes(old)
for key in list(data):
    if key.startswith('current_'):del data[key]
stamp=now()
data.update({'UTC':stamp,'updated_UTC':stamp,'current_PR':117,'current_problem_id':30001234,'current_code':'OWR-3471-008',
 'current_original_head':'8163ee0dc7a0f944570925984cef2dc0fb291ad8','current_original_literal_status':'claimed_solved',
 'current_original_budget':'1/5','current_new_central_proof_search_turns':0,
 'current_source_authentication_complete':True,'current_source_authentication_percent':100,
 'current_sourcepair_record':'audits/pr117_30001234/original_head_authentication_20261006/SOURCEPAIR_AUTHENTICATION.json',
 'current_mathematical_clearance':True,'current_mathematical_audit_percent':100,
 'current_mathematical_gate':'audits/pr117_30001234/MATHEMATICAL_SOURCE_GATE_20261006.json',
 'current_mathematical_remaining_findings':[],'current_repaired_diagnostics':'audits/pr117_30001234/repaired_diagnostics_v1',
 'current_original_assert_guard_weakness_repaired_in_separate_diagnostic_copies':True,
 'current_priority_audit_percent':100,'current_priority_adjudication_complete':True,'current_priority_clearance':False,
 'current_fresh_disposition_review_pending':False,'current_fresh_disposition_review_PASS':True,'current_novelty_established':False,
 'current_priority_threat':'Exact same Takagi Example4.4 published2013 and present in actual2011v1; third sign/order/ambient bridge independently verified.',
 'current_disposition':'already_solved exact original target; same-head closure and additive native correction pending.',
 'current_publication_preparation_percent':0,'current_publication_ready':False,'current_DOI':None,
 'current_Zenodo_published':False,'current_tracker_updated':False,'current_native_assessment_performed':False,
 'current_PR_workflow_percent':75,'current_workflow_estimate_percent':75,
 'current_human_disposition_question_pending':False,'current_human_source_access_question_pending':False,
 'current_remaining_required_steps':'Authorized same-head closure and additive native correction; actual full readbacks/checkpoints and writer release before next intake.',
 'current_this_goal_turn_classification':'progress','advance_to_next_PR_authorized_now':False,
 'completion_metadata_checkpoint_pending_at_snapshot':False,
 'last_completed_metadata_checkpoint_commit':release['completion_metadata_commit'],
 'last_completed_final_completion_readback':'audits/pr111_4900006/FINAL_COMPLETION_OWNER_RELEASE_20261006.json',
 'last_completed_audit_checkpoint_push_pending':False,'last_completed_late_release_audit_checkpoint_pending':False,
 'latest_ordered_intake_record':'ordered_intake_20261006/after_PR111/INTAKE_AFTER_PR111.json',
 'next_numeric_intake_cursor':118,'next_eligible_PR_after_current_completion':None,
 'next_step':'Complete PR117 fresh priority disposition and appropriate authorized correction/closure; no preprint for a known counterexample.',
 'remaining_current_step':'PR117 priority disposition.',
 'main_writer_owner_at_snapshot':'This chat: actual exclusive ordinary math checkpoint; writer release pending readback.',
 'skipped_since_last_completion':[{key:row[key] for key in ['PR','literal_status','effort']} for row in json.loads((P/'ordered_intake_20261006/after_PR111/INTAKE_AFTER_PR111.json').read_text())['ascending_status_only_rows'] if not row['eligible']],
 'persistent_goal_status':'active','persistent_goal_complete':False})
dump(progress_path,data)
closed_path=A/'actual_closure_20261006/RECEIPT.json'
if closed_path.exists():
    closed=json.loads(closed_path.read_text())
    require(closed['same_head_closed_without_merge'] and closed['original_head']==ready['original_head'],'Actual closure scope')
    data.update({'current_closed_without_merging':True,'current_actual_closed_at':closed['after']['closedAt'],
      'current_actual_closing_comment_url':closed['closing_comment_url'],'current_PR_workflow_percent':85,'current_workflow_estimate_percent':85,
      'current_disposition':'already_solved exact target; same-head closure verified, additive native correction pending.',
      'current_remaining_required_steps':'Additive native correction, actual full readbacks/checkpoints, completion metadata and explicit writer release before next intake.'})
    if 117 not in data['closed_without_publication_PRs']:data['closed_without_publication_PRs'].append(117)
    dump(progress_path,data)
line='\n'+stamp+': PR117 source/math PASS and explicit Takagi2011/2013 prior confirmed by three root-authenticated priority families and fresh disposition adversary. Original1/5 proof preserved; diagnostic guard repair separate. Already_solved exact target; actual closure flag='+str(closed_path.exists())+'; native correction pending. Ordinary scoped main checkpoint preserves actual PR111 metadata/readback/release. Math/priority100%, workflow'+str(data['current_PR_workflow_percent'])+'%, program19/99=19.19%,11published; goal active. No PR/native/publication/tracker mutation in this checkpoint.\n'
for path in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md']:
    with path.open('a') as handle:handle.write(line)
selected={progress_path,P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md',snapshot,A/'RESEARCH_LOG.md',A/'ACTUAL_WRITER_HANDOFF_20261006.json',Path(__file__).resolve()}
root_names=['EFFECTIVE_GUARD_VALIDATION_PROCESS_JOURNAL_20261006.json','ROOT_MATHEMATICAL_REASONING_20261006.json',
 'repair_verification_guards_20261006.py','ROOT_EFFECTIVE_GUARD_VALIDATION_20261006.json','validate_effective_guard_diagnostics_20261006.py',
 'guard_false_control_20261006.py','MATHEMATICAL_SOURCE_GATE_20261006.json','authenticate_original_and_source_20261006.py',
 'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json','reproduce_original_checkers_20261006.py',
 'authenticate_and_reproduce_math_families_20261006.py','authenticate_original_and_source_v1_failed_20261006.py',
 'ORIGINAL_AUTHENTICATION_SCHEMA_REPAIR_20261006.json','record_root_mathematical_reasoning_20261006.py',
 'root_family_false_guard_probe_20261006.py','ROOT_ORIGINAL_CHECKER_REPRODUCTION_20261006.json']
selected.update(A/name for name in root_names)
selected.update(x for x in A.iterdir() if x.is_file() and not x.is_symlink() and x.suffix in {'.py','.md','.json'})
for dirname in ['original_head_authentication_20261006','repaired_diagnostics_v1']:
    selected.update(x for x in (A/dirname).rglob('*') if x.is_file() and not PRIVATE.intersection(x.parts))
for dirname,expected in [('ideal_hypotheses_adversary_20261006','863931986a6222285d3ab840bb16b2e5054a2dabba008cc119a0f1ed9e51b9a2'),
 ('polytope_fiber_adversary_20261006','91cfa9cfe70d53c8c238815521dbff44137873190a7e70c55a398a3dcc994f69'),
 ('primary_source_scope_adversary_20261006','88b1428cbdd72deafe782eff2bdafaf4565c58b2adabfe68b95cd32be6ea76af')]:
    folder=A/dirname
    manifest=folder/'OUTPUT_MANIFEST.json'
    require(sha(manifest.read_bytes())==expected,'Sealed math manifest changed')
    body=json.loads(manifest.read_text())
    selected.add(manifest)
    for item in body.get('members',body.get('files',[])):
        path=folder/item['path'];actual=pin(path)
        require(actual['bytes']==item.get('bytes',item.get('byte_count')) and actual['sha256']==item['sha256'],'Sealed math member changed')
        selected.add(path)
for dirname,expected,count in [('original_question_priority_adversary_20261006','1235924906c6fb09a18dcf1a324d06cbf42621c0c2c86758b8da0e2ce7f2d584',34),
 ('determinantal_priority_adversary_20261006','851eae3623b022dc5b33003b410cc7431ef1d2a5126e826a382c1869840b1066',39),
 ('later_binomial_priority_adversary_20261006','f7832ca2499adef7307a9d84eecc435d32693571f7f231e5116d8f21ab4fae6e',26),
 ('exact_prior_disposition_adversary_20261006','d59f9dfe58c6d00b3090cd3d325a8251d161579c81a2ba0497d228038ece64bc',58)]:
    folder=A/dirname;manifest=folder/'OUTPUT_MANIFEST.json'
    require(sha(manifest.read_bytes())==expected,'Sealed priority manifest changed')
    members=json.loads(manifest.read_text())['members'];require(len(members)==count,'Priority member count')
    selected.add(manifest)
    for member in members:
        relative=member.get('path',member.get('relative_path'))
        require(relative is not None,'Priority manifest path schema')
        path=Path(relative) if Path(relative).is_absolute() else folder/relative
        require(path.is_relative_to(folder) and 'private' not in path.relative_to(folder).parts,'Priority public scope')
        actual=pin(path);require(actual['bytes']==member.get('bytes',member.get('byte_count')) and actual['sha256']==member['sha256'],'Priority sealed member changed')
        selected.add(path)
selected.update(x for x in (A/'root_priority_audit_20261006').rglob('*') if x.is_file() and not PRIVATE.intersection(x.parts) and (x.suffix in {'.md','.json','.py'} or x.name=='.gitignore'))
selected.update(x for x in (A/'actual_closure_20261006').rglob('*') if x.is_file() and x.suffix in {'.json','.md','.py'})
selected.update(x for x in (A/'actual_reconciliation_20261006').rglob('*') if x.is_file() and x.suffix in {'.json','.md','.py'})
selected.update(x for x in (A/'actual_reconciliation_verified_20261006').rglob('*') if x.is_file() and x.suffix in {'.json','.md','.py'})
selected.update(x for x in (A/'actual_reconciliation_verified_v3_20261006').rglob('*') if x.is_file() and x.suffix in {'.json','.md','.py'})
intake=P/'ordered_intake_20261006/after_PR111'
selected.update(x for x in intake.rglob('*') if x.is_file() and not PRIVATE.intersection(x.parts))
for name in ['FINAL_COMPLETION_OWNER_RELEASE_20261006.json','record_final_writer_release_20261006.py',
 'actual_completion_metadata_20261006/RECEIPT.json','actual_completion_metadata_20261006/PROCESS_JOURNAL.json',
 'actual_final_completion_readback_20261006/RECEIPT.json','actual_final_completion_readback_20261006/PROCESS_JOURNAL.json']:
    selected.add(previous/name)
members=[pin(x) for x in sorted(selected)]
selection=A/'MATH_CHECKPOINT_SELECTION_20261006.json'
dump(selection,{'schema':'pr117-ordinary-math-checkpoint-selection/v1','UTC':now(),'base':BASE,'members':members,
 'private_bodies_included':False,'math_gate':'PASS','priority_disposition':'fresh-adversary cleared already_solved exact target','program_completed':19,
 'workflow_percent':data['current_PR_workflow_percent'],'goal_active':True,'self_hash_omitted':True})
selected.add(selection)
pins={str(x.relative_to(C)):pin(x) for x in selected}
materialized_changes=set(run(['diff','--name-only','--diff-filter=ACMRTUXB','-z']).decode().split('\0'))-{''}
require(materialized_changes<=set(pins),'Foreign materialized tracked edits')
run(['add','--',*sorted(pins)])
staged=set(run(['diff','--cached','--name-only','-z']).decode().split('\0'))-{''}
require(staged<=set(pins) and len(staged)>100,'Staged scope mismatch')
require(not run(['diff','--cached','--diff-filter=D','--name-only']),'Deletion staged')
for path in staged:
    body=run(['show',':'+path]);require(len(body)==pins[path]['bytes'] and sha(body)==pins[path]['sha256'],'Staged body mismatch')
run(['commit','-m','Audit PR117 mathematics and explicit prior; preserve PR111 release receipts'])
commit=run(['rev-parse','HEAD']).decode().strip()
require(run(['rev-parse','HEAD^']).decode().strip()==BASE,'Unexpected commit parent')
changed=set(run(['diff-tree','--no-commit-id','--name-only','-r','-z',commit]).decode().split('\0'))-{''}
require(changed==staged,'Unexpected committed paths')
for path in staged:
    body=run(['show',commit+':'+path]);require(len(body)==pins[path]['bytes'] and sha(body)==pins[path]['sha256'],'Committed body mismatch')
run(['push','origin','HEAD:refs/heads/main'])
require(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==commit,'Remote push readback mismatch')
run(['fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main'])
require(run(['rev-parse','origin/main']).decode().strip()==commit,'Fetched main mismatch')
for path in staged:
    body=run(['show','origin/main:'+path]);require(len(body)==pins[path]['bytes'] and sha(body)==pins[path]['sha256'],'Remote body mismatch')
require(not run(['diff','--cached','--name-only']),'Index not empty after checkpoint')
receipt={'schema':'pr117-ordinary-math-checkpoint-actual/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'base':BASE,'commit':commit,'selected_count':len(pins),'changed_count':len(staged),
 'changed_members':[pins[x] for x in sorted(staged)],'nonforce_push_passed':True,
 'full_changed_selected_bodies_verified_in_index_commit_and_fetched_main':True,
 'PR_native_publication_tracker_mutations':False,'priority_disposition_complete':True,'native_correction_pending':True,
 'PR117_already_closed_at_checkpoint':closed_path.exists(),
 'program_completed':19,'published':11,'workflow_percent':data['current_PR_workflow_percent'],'persistent_goal_status':'active','writer_release_pending':True}
dump(D/'RECEIPT.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k!='changed_members'},sort_keys=True))

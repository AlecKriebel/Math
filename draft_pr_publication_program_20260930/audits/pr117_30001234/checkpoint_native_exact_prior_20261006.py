"""Actual scoped main correction checkpoint with full body readbacks."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
A=Path(__file__).resolve().parent
C=A.parents[2]
P=A.parent.parent
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
BASE=sys.argv[1]
D=A/'actual_native_checkpoint_20261006'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise ValueError(label)
def sha(body):return hashlib.sha256(body).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(args):
    start=now();child=subprocess.Popen([GIT,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    events.append({'argv':[GIT,*args],'PID':child.pid,'UTC_start':start,'UTC_end':now(),'exit_code':child.returncode,
      'stdout_bytes':len(out),'stdout_sha256':sha(out),'small_stdout':out.decode('utf-8','replace') if len(out)<1200 else None,
      'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf-8','replace')})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,'Git action failed; inspect actual journal/state before retry')
    return out
def pin(path):
    require(path.is_relative_to(C) and path.is_file() and not path.is_symlink(),'Regular selected path required')
    body=path.read_bytes();return {'path':str(path.relative_to(C)),'bytes':len(body),'sha256':sha(body)}
require(not D.exists(),'Existing checkpoint run; inspect rather than repeat')
D.mkdir()
require(run(['branch','--show-current']).strip()==b'main','Not main')
require(run(['rev-parse','HEAD']).decode().strip()==BASE,'Local base changed')
require(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==BASE,'Remote changed')
require(not run(['diff','--cached','--name-only']),'Index not empty')
ready=json.loads((A/'ROOT_DISPOSITION_READY_20261006.json').read_text())
native=json.loads((A/'native_exact_prior_disposition_20261006/PREPARED_RECEIPT.json').read_text())
closed=json.loads((A/'actual_closure_20261006/RECEIPT.json').read_text())
require(ready['fresh_disposition_review_PASS'] and not ready['publication_authorization'],'Fresh gate')
require(native['base_commit']==BASE and native['same_head_closed_without_merge'] and native['original_budget']=='1/5','Native prepared scope')
require(closed['same_head_closed_without_merge'] and closed['original_head']==ready['original_head'],'Closure scope')
progress_path=P/'CURRENT_PROGRESS.json';progress=json.loads(progress_path.read_text())
require(progress['current_PR']==117 and progress['fully_completed_count']==19,'Progress cursor mismatch')
stamp=now()
progress.update({'UTC':stamp,'updated_UTC':stamp,'current_disposition':'already_solved_exact_Takagi_2011_2013_same_example',
 'current_native_assessment_performed':True,'current_native_status':'already_solved','current_native_correction_checkpoint_pending':True,
 'current_actual_closed_at':closed['after']['closedAt'],'current_actual_closing_comment_url':closed['closing_comment_url'],
 'current_closed_without_merging':True,'current_core_disposition_complete':False,
 'current_source_catalog_openness_correction_prepared':True,'current_source_catalog_openness_correction_committed':False,
 'current_PR_workflow_percent':95,'current_workflow_estimate_percent':95,
 'current_remaining_required_steps':'Actual native correction commit/push/full readback, completion metadata, final readback and explicit writer release.',
 'next_step':'Complete and read back PR117 native exact-prior correction; release writer before next numeric intake118.',
 'remaining_current_step':'PR117 native exact-prior correction checkpoint and completion metadata/readback/release.',
 'main_writer_owner_at_snapshot':'This chat: actual exclusive native correction checkpoint; release pending readbacks.',
 'persistent_goal_status':'active','persistent_goal_complete':False})
if 117 not in progress['closed_without_publication_PRs']:progress['closed_without_publication_PRs'].append(117)
dump(progress_path,progress)
line='\n'+stamp+': PR117 actual same-head unmerged closure '+closed['closing_comment_url']+' verified. Native source-bound already_solved assessment and original1/5 import prepared; all20originals, unrelated assessments/states/history/campaign rows preserved, rank-only projections permitted. Science/source/priority100%; workflow95% pending actual native push/readback and metadata/release. Program19/99=19.19%,11published; no paper/DOI/tracker; goal active.\n'
for path in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md']:
    with path.open('a') as h:h.write(line)
private={'private_sources','private_renders','private_backend','private','__pycache__'}
def public(path):return path.is_file() and not path.is_symlink() and not private.intersection(path.parts) and (path.suffix in {'.py','.md','.json','.txt','.log'} or path.name=='.gitignore')
selected={x for x in A.iterdir() if public(x)}
for name in ['actual_closure_20261006','native_exact_prior_disposition_20261006','actual_math_checkpoint_20261006','root_priority_audit_20261006']:
    selected.update(x for x in (A/name).rglob('*') if public(x))
selected.update([progress_path,P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md'])
for entry in native['native_pins']:
    path=C/entry['path'];require(pin(path)==entry,'Prepared native body changed');selected.add(path)
members=[pin(x) for x in sorted(selected)]
selection=A/'NATIVE_CHECKPOINT_SELECTION_20261006.json'
dump(selection,{'schema':'pr117-native-exact-prior-checkpoint-selection/v1','UTC':now(),'base_commit':BASE,
 'members':members,'private_bodies_included':False,'same_head_closed_without_merge':True,'publication':False,
 'original_budget':'1/5','new_central_proof_turns':0,'program_completed':19,'workflow_percent':95,'self_hash_omitted':True})
selected.add(selection);pins={str(x.relative_to(C)):pin(x) for x in selected}
changed_before=set(run(['diff','--name-only','--diff-filter=ACMRTUXB','-z']).decode().split('\0'))-{''}
require(changed_before<=set(pins),'Foreign tracked changes')
run(['add','--',*sorted(pins)])
staged=set(run(['diff','--cached','--name-only','-z']).decode().split('\0'))-{''}
require(staged<=set(pins) and len(staged)>15,'Unexpected staged scope')
require(not run(['diff','--cached','--diff-filter=D','--name-only']),'Deletion staged')
for path in staged:
    body=run(['show',':'+path]);require(len(body)==pins[path]['bytes'] and sha(body)==pins[path]['sha256'],'Staged body mismatch')
run(['commit','-m','Record PR117 explicit prior and close the already solved target'])
commit=run(['rev-parse','HEAD']).decode().strip()
require(run(['rev-parse','HEAD^']).decode().strip()==BASE,'Wrong parent')
changes=set(run(['diff-tree','--no-commit-id','--name-only','-r','-z',commit]).decode().split('\0'))-{''}
require(changes==staged,'Unexpected committed paths')
for path in staged:
    body=run(['show',commit+':'+path]);require(len(body)==pins[path]['bytes'] and sha(body)==pins[path]['sha256'],'Committed body mismatch')
run(['push','origin','HEAD:refs/heads/main'])
require(run(['ls-remote','origin','refs/heads/main']).decode().split()[0]==commit,'Remote push readback mismatch')
run(['fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main'])
require(run(['rev-parse','origin/main']).decode().strip()==commit,'Fetched main mismatch')
for path in staged:
    body=run(['show','origin/main:'+path]);require(len(body)==pins[path]['bytes'] and sha(body)==pins[path]['sha256'],'Fetched body mismatch')
require(not run(['diff','--cached','--name-only']),'Post-checkpoint index not empty')
receipt={'schema':'pr117-native-exact-prior-checkpoint-actual/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'base_commit':BASE,'commit':commit,'selected_count':len(pins),'changed_count':len(staged),
 'changed_members':[pins[x] for x in sorted(staged)],'actual_nonforce_push_passed':True,
 'actual_full_changed_selected_bodies_verified_in_index_commit_and_fetched_main':True,
 'native_correction_committed':True,'same_head_closed_without_merge':True,'completion_metadata_pending':True,
 'writer_release_pending':True,'PR_workflow_percent':95,'program_completed':19,'published':11,'persistent_goal_status':'active'}
dump(D/'RECEIPT.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k!='changed_members'},sort_keys=True))

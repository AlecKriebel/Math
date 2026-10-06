"""Actual completion metadata only after closed-head and native remote readbacks."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
A=Path(__file__).resolve().parent;C=A.parents[2];P=A.parent.parent
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git';GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
BASE=sys.argv[1];D=A/'actual_completion_metadata_20261006';events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise ValueError(label)
def sha(body):return hashlib.sha256(body).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(exe,args):
    start=now();child=subprocess.Popen([exe,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    events.append({'argv':[exe,*args],'PID':child.pid,'UTC_start':start,'UTC_end':now(),'exit_code':child.returncode,
      'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),
      'small_stdout':out.decode('utf-8','replace') if len(out)<1200 else None,'stderr':err.decode('utf-8','replace')})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,'Actual readback/checkpoint action failed; inspect journal before retry')
    return out
def git(*args):return run(GIT,list(args))
def pin(path):
    require(path.is_file() and not path.is_symlink(),'Regular metadata body required')
    b=path.read_bytes();return {'path':str(path.relative_to(C)),'bytes':len(b),'sha256':sha(b)}
require(not D.exists(),'Existing metadata action; inspect rather than repeat')
D.mkdir()
native=json.loads((A/'actual_native_checkpoint_20261006/RECEIPT.json').read_text())
closed=json.loads((A/'actual_closure_20261006/RECEIPT.json').read_text())
require(native['commit']==BASE and native['native_correction_committed'],'Native checkpoint required')
require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==BASE,'Main base mismatch')
require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==BASE,'Remote changed')
require(not git('diff','--cached','--name-only'),'Index not empty')
require(git('rev-parse','origin/main').decode().strip()==BASE,'Fetched main mismatch')
for item in native['changed_members']:
    body=git('show','origin/main:'+item['path'])
    require(len(body)==item['bytes'] and sha(body)==item['sha256'],'Native checkpoint full body mismatch')
live=json.loads(run(GH,['pr','view','117','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,closedAt,mergedAt,url']))
require(live['state']=='CLOSED' and live['headRefOid']==closed['original_head'] and live['mergedAt'] is None and live['closedAt'],'Closed same-head readback mismatch')
comment=json.loads(run(GH,['api','repos/AlecKriebel/Math/issues/comments/'+str(closed['closing_comment_id'])]))
require(comment['body']==(A/'CLOSURE_COMMENT_FINAL_20261006.md').read_text(),'Actual full closing body mismatch')
stamp=now()
core={'schema':'pr117-core-closure-completion/v1','UTC':stamp,'actual_operator_PID':os.getpid(),
 'PR':117,'original_head':closed['original_head'],'same_head_closed_without_merge':True,
 'closing_comment_url':closed['closing_comment_url'],'actual_full_comment_body_verified':True,
 'native_checkpoint_commit':BASE,'native_checkpoint_changed_body_count':len(native['changed_members']),
 'all_native_checkpoint_changed_bodies_reverified_from_fetched_main':True,
 'status':'already_solved','scope':'Exact original target explicitly answered by same Takagi2011/2013 counterexample.',
 'mathematical_clearance':True,'exact_prior_same_example_authenticated':True,'substantive_novel_resolution_established':False,
 'original_budget':'1/5','new_central_proof_turns':0,'paper_Zenodo_DOI_tracker_merge_actions':False,
 'workflow_percent':100,'program_completed':20,'dated_eligible_total':99,'program_percent':20/99*100,
 'published':11,'persistent_goal_status':'active','completion_metadata_checkpoint_pending':True,'writer_release_pending':True}
dump(A/'ROOT_CLOSURE_COMPLETION_20261006.json',core)
path=P/'CURRENT_PROGRESS.json';progress=json.loads(path.read_text())
require(progress['current_PR']==117 and progress['fully_completed_count']==19,'Unexpected completion cursor')
progress['fully_completed_eligible_PRs'].append(117)
progress.update({'UTC':stamp,'updated_UTC':stamp,'fully_completed_count':20,'fully_completed_fraction_percent':20/99*100,'workflow_estimate_percent':20/99*100,
 'current_core_disposition_complete':True,'current_PR_workflow_percent':100,'current_workflow_estimate_percent':100,
 'current_native_correction_checkpoint_pending':False,'current_native_disposition_checkpoint_commit':BASE,
 'current_source_catalog_openness_correction_committed':True,'current_completion_metadata_checkpoint_pending':True,
 'current_remaining_required_steps':'Actual completion metadata push/readback, final body/head/index readback and explicit writer release; no scientific or publication work remains for117.',
 'last_completed_PR':117,'last_completed_DOI':None,'last_completed_PR_workflow_percent':100,
 'last_completed_outcome':'already_solved_exact_Takagi_2011_2013_same_example',
 'last_completed_record':'audits/pr117_30001234/ROOT_CLOSURE_COMPLETION_20261006.json',
 'last_completed_actual_final_gate':'audits/pr117_30001234/ROOT_CLOSURE_COMPLETION_20261006.json',
 'last_completed_final_completion_readback':'audits/pr117_30001234/ROOT_CLOSURE_COMPLETION_20261006.json',
 'last_completed_closing_comment_url':closed['closing_comment_url'],'last_completed_native_correction_commit':BASE,
 'last_completed_metadata_checkpoint_commit':None,'last_completed_merge_commit':None,'last_completed_tracker_range':None,
 'last_completed_full_source_solved':False,'last_completed_mathematical_counterexample_valid':True,
 'last_completed_source_resolution_scope':'Exact original negative answer explicitly present in Takagi2011/2013; direct full-face exposition valid, no substantive new resolution.',
 'last_completed_priority_clearance':False,'last_completed_publication_authorization':False,
 'last_completed_audit_checkpoint_push_pending':True,'last_completed_late_release_audit_checkpoint_pending':True,
 'last_completed_late_release_audit_checkpoint_commit':json.loads((A/'actual_math_checkpoint_20261006/RECEIPT.json').read_text())['commit'],
 'completion_metadata_checkpoint_pending_at_snapshot':True,'advance_to_next_PR_authorized_now':False,
 'next_step':'Verify PR117 completion metadata and release writer; then fresh ascending status-only intake118.',
 'remaining_current_step':'PR117 completion metadata/readback/release.',
 'main_writer_owner_at_snapshot':'This chat: completion metadata checkpoint; release pending actual final readback.',
 'persistent_goal_status':'active','persistent_goal_complete':False})
dump(path,progress)
line='\n'+stamp+': PR117 exact already_solved disposition complete: same-head CLOSED/unmerged and full explanatory comment reverified; native correction '+BASE+' all'+str(len(native['changed_members']))+' changed bodies read back from fetched main. Valid proof/source/ledger1/5 preserved, new proof turns0; no paper/Zenodo/DOI/tracker/merge. Workflow100%, program20/99=20.20%,11published; metadata/final readback/release still operationally pending at snapshot; goal active.\n'
for f in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md']:
    with f.open('a') as h:h.write(line)
selected={path,P/'RESEARCH_LOG.md',P/'CURRENT_PROGRESS.md',A/'RESEARCH_LOG.md',A/'ROOT_CLOSURE_COMPLETION_20261006.json',Path(__file__).resolve(),A/'actual_native_checkpoint_20261006/RECEIPT.json',A/'actual_native_checkpoint_20261006/PROCESS_JOURNAL.json'}
selection=A/'COMPLETION_METADATA_SELECTION_20261006.json'
dump(selection,{'schema':'pr117-completion-metadata-selection/v1','UTC':now(),'base':BASE,'members':[pin(x) for x in sorted(selected)],'self_hash_omitted':True,'goal_active':True})
selected.add(selection);pins={str(x.relative_to(C)):pin(x) for x in selected}
changes=set(git('diff','--name-only','--diff-filter=ACMRTUXB','-z').decode().split('\0'))-{''}
require(changes<=set(pins),'Foreign materialized tracked changes')
git('add','--',*sorted(pins))
staged=set(git('diff','--cached','--name-only','-z').decode().split('\0'))-{''}
require(staged<=set(pins) and len(staged)>=7,'Metadata staged scope')
require(not git('diff','--cached','--diff-filter=D','--name-only'),'Deletion staged')
for p in staged:
    b=git('show',':'+p);require(len(b)==pins[p]['bytes'] and sha(b)==pins[p]['sha256'],'Staged metadata mismatch')
git('commit','-m','Record completed PR117 exact-prior disposition')
commit=git('rev-parse','HEAD').decode().strip();require(git('rev-parse','HEAD^').decode().strip()==BASE,'Metadata parent mismatch')
changed=set(git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).decode().split('\0'))-{''}
require(changed==staged,'Metadata committed scope mismatch')
for p in staged:
    b=git('show',commit+':'+p);require(len(b)==pins[p]['bytes'] and sha(b)==pins[p]['sha256'],'Committed metadata mismatch')
git('push','origin','HEAD:refs/heads/main')
require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit,'Metadata remote mismatch')
git('fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main')
require(git('rev-parse','origin/main').decode().strip()==commit,'Fetched metadata main mismatch')
for p in staged:
    b=git('show','origin/main:'+p);require(len(b)==pins[p]['bytes'] and sha(b)==pins[p]['sha256'],'Remote metadata mismatch')
require(not git('diff','--cached','--name-only'),'Post-metadata index not empty')
receipt={'schema':'pr117-actual-completion-metadata-checkpoint/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'base':BASE,'commit':commit,'changed_count':len(staged),'changed_members':[pins[p] for p in sorted(staged)],
 'actual_nonforce_push_passed':True,'actual_full_changed_metadata_bodies_verified':True,
 'program_completed':20,'program_percent':20/99*100,'published':11,'persistent_goal_status':'active','final_readback_and_writer_release_pending':True}
dump(D/'RECEIPT.json',receipt)
print(json.dumps({k:v for k,v in receipt.items() if k!='changed_members'},sort_keys=True))

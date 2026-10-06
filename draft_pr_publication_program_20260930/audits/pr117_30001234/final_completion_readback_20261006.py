"""Final actual body/head/index readback; writer release remains separate."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
A=Path(__file__).resolve().parent;C=A.parents[2]
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git';GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
BASE=sys.argv[1];D=A/'actual_final_completion_readback_20261006';events=[]
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
      'small_stdout':out.decode('utf-8','replace') if len(out)<1000 else None,'stderr':err.decode('utf-8','replace')})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,'Actual final readback failed; inspect journal before retry')
    return out
def git(*args):return run(GIT,list(args))
require(not D.exists(),'Existing final readback; inspect rather than repeat')
D.mkdir()
metadata=json.loads((A/'actual_completion_metadata_20261006/RECEIPT.json').read_text())
native=json.loads((A/'actual_native_checkpoint_20261006/RECEIPT.json').read_text())
closed=json.loads((A/'actual_closure_20261006/RECEIPT.json').read_text())
require(metadata['commit']==BASE,'Metadata base mismatch')
require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==BASE,'Final local main mismatch')
require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==BASE,'Final remote main mismatch')
require(git('rev-parse','origin/main').decode().strip()==BASE,'Final fetched main mismatch')
pins={x['path']:x for x in native['changed_members']}
pins.update({x['path']:x for x in metadata['changed_members']})
for path,item in pins.items():
    body=git('show','origin/main:'+path)
    require(len(body)==item['bytes'] and sha(body)==item['sha256'],'Final complete changed body mismatch '+path)
    current=C/path;require(current.exists() and current.read_bytes()==body,'Materialized selected body mismatch '+path)
require(not git('diff','--cached','--name-only'),'Final index not empty')
require(not git('diff','--name-only','--diff-filter=ACMRTUXB'),'Foreign materialized tracked changes')
live=json.loads(run(GH,['pr','view','117','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,closedAt,mergedAt,url']))
require(live['state']=='CLOSED' and live['headRefOid']==closed['original_head'] and live['mergedAt'] is None and live['closedAt'],'Final same-head closure mismatch')
comment=json.loads(run(GH,['api','repos/AlecKriebel/Math/issues/comments/'+str(closed['closing_comment_id'])]))
require(comment['body']==(A/'CLOSURE_COMMENT_FINAL_20261006.md').read_text(),'Final exact comment body mismatch')
prepared=json.loads((A/'native_exact_prior_disposition_20261006/PREPARED_RECEIPT.json').read_text())
for item in prepared['native_pins']:
    body=(C/item['path']).read_bytes();require(len(body)==item['bytes'] and sha(body)==item['sha256'],'Prepared native body mismatch')
state=json.loads((C/'unsolved_math_prioritization/state.json').read_text())['30001234']
require(state['status']=='already_solved' and state['turns_used']==1,'Native final target state/effort mismatch')
progress=json.loads((C/'draft_pr_publication_program_20260930/CURRENT_PROGRESS.json').read_text())
require(progress['fully_completed_count']==20 and progress['current_PR']==117 and progress['last_completed_PR']==117 and progress['persistent_goal_status']=='active','Final program cursor mismatch')
receipt={'schema':'pr117-actual-final-completion-readback/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'PR':117,'remote_main':BASE,'native_checkpoint_commit':native['commit'],'metadata_checkpoint_commit':BASE,
 'same_head_closed_without_merge':True,'actual_full_comment_body_verified':True,
 'all_latest_native_and_metadata_changed_bodies_verified':True,'latest_combined_body_count':len(pins),
 'native_target_status':'already_solved','original_budget':'1/5','new_central_proof_turns':0,
 'index_empty_and_materialized_non_deletion_tracked_changes_empty':True,
 'writer_release_pending':True,'goal_active':True,'program_completed':20,'program_percent':20/99*100,
 'published':11,'next_numeric_cursor':118,'paper_Zenodo_tracker_merge_actions':False,
 'closing_comment_url':closed['closing_comment_url']}
dump(D/'RECEIPT.json',receipt)
print(json.dumps(receipt,sort_keys=True))

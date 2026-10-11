"""Full final readback; release itself uses the authorized app API afterwards."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent
C=A.parents[2]
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
D=A/'actual_final_completion_readback_20261006'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise RuntimeError(label)
def sha(body):return hashlib.sha256(body).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(argv):
    child=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    events.append({'argv':argv,'PID':child.pid,'ended_UTC':now(),'exit_code':child.returncode,
        'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,'Actual readback failed')
    return out
def git(*args):return run([GIT,*args])
require(not D.exists(),'Existing readback: inspect before retry')
D.mkdir()
meta=json.loads((A/'actual_completion_metadata_20261006/RECEIPT.json').read_text())
native=json.loads((A/'actual_disposition_checkpoint_20261006/RECEIPT.json').read_text())
require(meta['actual_nonforce_push_and_full_remote_body_readback_passed'],'Metadata incomplete')
commit=meta['commit']
require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==commit,'Wrong local main')
require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit,'Wrong actual remote main')
require(git('rev-parse',commit+'^').decode().strip()==native['commit'],'Metadata parent mismatch')
for batch,ref in [(native['changed_members'],native['commit']),(meta['changed_members'],commit)]:
    for item in batch:
        body=git('show',ref+':'+item['path'])
        require(len(body)==item['bytes'] and sha(body)==item['sha256'],'Final full Git body mismatch')
require(not git('diff','--cached','--name-only'),'Final index not empty')
require(not git('diff','--name-only','--diff-filter=ACMRTUXB'),'Final materialized tracked changes')
closed=json.loads((A/'actual_closure_20261006/RECEIPT.json').read_text())
live=json.loads(run([GH,'pr','view','111','--repo','AlecKriebel/Math','--json','state,headRefOid,closedAt,mergedAt,url']))
require(live['state']=='CLOSED' and live['headRefOid']==closed['original_head'] and live['mergedAt'] is None,'Final closure mismatch')
comment=json.loads(run([GH,'api','repos/AlecKriebel/Math/issues/comments/'+str(closed['closing_comment_id'])]))
require(comment['body']==(A/'PROPOSED_CLOSURE_COMMENT_20261006.md').read_text(),'Final comment body mismatch')
progress=json.loads(git('show',commit+':draft_pr_publication_program_20260930/CURRENT_PROGRESS.json'))
require(progress['fully_completed_count']==19 and 111 in progress['fully_completed_eligible_PRs']
    and len(progress['published_PRs'])==11 and progress['persistent_goal_status']=='active'
    and not progress['advance_to_next_PR_authorized_now'],'Completion accounting/gating')
record={'schema':'pr111-final-completion-readback/v1','UTC':now(),'actual_operator_PID':os.getpid(),'PR':111,
    'native_checkpoint_commit':native['commit'],'completion_metadata_commit':commit,
    'all115_native_priority_and10_metadata_bodies_reverified':len(native['changed_members'])==115 and len(meta['changed_members'])==10,
    'native_priority_body_count':len(native['changed_members']),'metadata_body_count':len(meta['changed_members']),
    'actual_same_head_closed_without_merge':True,'actual_full_comment_body_matches':True,
    'actual_remote_main_verified':True,'index_empty_and_materialized_tracked_changes_empty':True,
    'status_scope':'Broad imported manifold target only; stronger R5 valid, identical prior and novelty unresolved.',
    'workflow_percent':100,'program_completed':19,'dated_eligible_total':99,'program_estimate_percent':19/99*100,
    'published':11,'DOI':None,'tracker_actions':False,'persistent_goal_status':'active',
    'writer_release_pending':True,'next_numeric_cursor':112,'next_intake_after_actual_writer_release_only':True}
dump(D/'RECEIPT.json',record)
print(json.dumps(record,sort_keys=True))

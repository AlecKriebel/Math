"""Verify actual closure/native push, then ordinary completion metadata checkpoint."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent
C=A.parents[2]
P=A.parent.parent
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
D=A/'actual_completion_metadata_20261006'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise RuntimeError(label)
def sha(body):return hashlib.sha256(body).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(argv):
    start=now();child=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    events.append({'argv':argv,'PID':child.pid,'start_UTC':start,'end_UTC':now(),'exit_code':child.returncode,
        'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err),
        'small_stdout':out.decode('utf-8','replace') if len(out)<12000 else None,'stderr':err.decode('utf-8','replace')})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,'Action failed; inspect journal/state before retry')
    return out
def git(*args):return run([GIT,*args])
def pin(path):
    body=path.read_bytes()
    return {'path':str(path.relative_to(C)),'bytes':len(body),'sha256':sha(body)}
require(not D.exists(),'Existing completion run: inspect before retry')
D.mkdir()
actual=json.loads((A/'actual_disposition_checkpoint_20261006/RECEIPT.json').read_text())
base=actual['commit']
require(actual['actual_nonforce_push_passed'] and actual['actual_remote_fetch_and_full_selected_changed_body_readback_passed'],'Actual checkpoint incomplete')
require(git('branch','--show-current').strip()==b'main' and git('rev-parse','HEAD').decode().strip()==base,'Wrong branch/base')
require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==base,'Remote advanced')
require(not git('diff','--cached','--name-only'),'Index not empty')
for item in actual['changed_members']:
    body=git('show',base+':'+item['path'])
    require(len(body)==item['bytes'] and sha(body)==item['sha256'],'Native/priority committed body mismatch')
closed=json.loads((A/'actual_closure_20261006/RECEIPT.json').read_text())
live=json.loads(run([GH,'pr','view','111','--repo','AlecKriebel/Math','--json','state,isDraft,headRefOid,baseRefName,closedAt,mergedAt,url']))
require(live['state']=='CLOSED' and live['headRefOid']==closed['original_head'] and live['mergedAt'] is None and live['closedAt'],'Closure live readback')
comment=json.loads(run([GH,'api','repos/AlecKriebel/Math/issues/comments/'+str(closed['closing_comment_id'])]))
require(comment['body']==(A/'PROPOSED_CLOSURE_COMMENT_20261006.md').read_text(),'Full comment live readback')
utc=now()
completion={'schema':'pr111-root-core-disposition-completion/v1','UTC':utc,'actual_operator_PID':os.getpid(),
    'PR':111,'problem_id':4900006,'original_head':closed['original_head'],'original_literal_status':'claimed_solved','original_budget':'2/5',
    'new_central_proof_search_turns':0,'mathematical_source_audit_percent':100,'bounded_priority_audit_percent':100,
    'fresh_disposition_review_PASS':True,'remaining_mandatory_disposition_findings':[],
    'status':'already_solved','classification_scope':'Only overbroad manifold-inclusive imported target/classical obstruction; valid stronger R5 theorem exact priority and substantive novelty unresolved.',
    'stronger_R5_math_valid':True,'stronger_R5_identical_prior_authenticated':False,'stronger_R5_novelty_established':False,
    'closed_without_merge':True,'same_original_head_live_readback':live,'closing_comment_url':closed['closing_comment_url'],
    'actual_full_comment_body_readback':True,'native_checkpoint_commit':base,'native_source_bound_correction_remotely_verified':True,
    'all_changed_public_bodies_reverified':len(actual['changed_members']),
    'all_scientific_service_and_native_action_requirements_complete':True,
    'DOI':None,'publication':False,'Zenodo_actions':False,'tracker_actions':False,
    'completion_metadata_checkpoint_pending':True,'writer_release_pending':True,'next_intake_authorized_now':False,
    'next_numeric_cursor':112,'workflow_best_guess_percent':100,'program_completed':19,'dated_eligible_total':99,
    'program_estimate_percent':19/99*100,'persistent_goal_status':'active','primary_checkout_mutated':False}
dump(A/'ROOT_CLOSURE_COMPLETION_20261006.json',completion)
progress_path=P/'CURRENT_PROGRESS.json'
o=json.loads(progress_path.read_text())
require(o['fully_completed_count']==18 and 111 not in o['fully_completed_eligible_PRs'],'Existing completion accounting')
o['fully_completed_eligible_PRs']=sorted(o['fully_completed_eligible_PRs']+[111])
o['closed_without_publication_PRs']=sorted(o['closed_without_publication_PRs']+[111])
o.update(updated_UTC=utc,fully_completed_count=19,fully_completed_fraction_percent=19/99*100,
    workflow_estimate_percent=19/99*100,current_PR_workflow_percent=100,current_workflow_estimate_percent=100,
    current_native_readback_pending=False,current_native_source_scope_correction_complete=True,
    current_core_disposition_complete=True,current_completion_metadata_checkpoint_pending=True,
    current_native_disposition_checkpoint_commit=base,current_completed_record='audits/pr111_4900006/ROOT_CLOSURE_COMPLETION_20261006.json',
    current_remaining_step='Completion metadata checkpoint/final readback and explicit writer release before fresh numeric intake112.',
    current_remaining_required_steps='Actual metadata push/readback and explicit writer release; no scientific/publication work remains for PR111.',
    last_completed_PR=111,last_completed_DOI=None,last_completed_PR_workflow_percent=100,
    last_completed_outcome=closed['disposition'],last_completed_full_source_solved=False,
    last_completed_mathematical_counterexample_valid=True,last_completed_priority_clearance=False,
    last_completed_publication_authorization=False,last_completed_source_resolution_scope=completion['classification_scope'],
    last_completed_record='audits/pr111_4900006/ROOT_CLOSURE_COMPLETION_20261006.json',
    last_completed_actual_final_gate='audits/pr111_4900006/ROOT_CLOSURE_COMPLETION_20261006.json',
    last_completed_final_completion_readback='audits/pr111_4900006/ROOT_CLOSURE_COMPLETION_20261006.json',
    last_completed_closing_comment_url=closed['closing_comment_url'],last_completed_merge_commit=None,
    last_completed_tracker_range=None,last_completed_native_correction_commit=base,
    last_completed_metadata_checkpoint_commit=None,last_completed_audit_checkpoint_push_pending=True,
    last_completed_late_release_audit_checkpoint_pending=True,completion_metadata_checkpoint_pending_at_snapshot=True,
    main_writer_owner_at_snapshot='This chat: completing PR111 metadata; release pending actual full remote readback.',
    next_step='Verify completion metadata and release writer; then next numeric claimed_solved intake112.',
    advance_to_next_PR_authorized_now=False)
o['workflow_estimate_definition']='Eleven published workflows, three legacy prior-result dispositions, one legacy verified partial disposition and four priority/source-based closures divided by dated99-PR census.'
dump(progress_path,o)
line='\n'+utc+': PR111 core disposition complete: same-head CLOSED without merge/comment full-body re-read; native already_solved correction and all115 public changed bodies actually pushed/fetched/reverified at'+base+'. Narrow scope only; stronger R5 theorem remains valid, exact prior/substantive novelty unresolved. Math/source100%, bounded priority100%, fresh dispositionPASS; workflow100% estimate with metadata push/final readback/writer release still pending. Program19/99=19.19%;11 published, goal active. Original2/5, new proof turns0; no paper/DOI/tracker. Next112 held until actual final metadata/release.\n'
native_log=C/'unsolved_math_prioritization/attempts/4900006/RESEARCH_LOG.md'
for path in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md',native_log]:
    with path.open('a') as handle:handle.write(line)
paths=[progress_path,P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md',native_log,A/'ROOT_CLOSURE_COMPLETION_20261006.json',
    A/'complete_source_scope_disposition_20261006.py',A/'final_completion_readback_20261006.py',
    A/'actual_disposition_checkpoint_20261006/PROCESS_JOURNAL.json',A/'actual_disposition_checkpoint_20261006/RECEIPT.json']
members=[pin(path) for path in paths]
selection=A/'COMPLETION_METADATA_SELECTION_20261006.json'
dump(selection,{'schema':'pr111-completion-metadata-selection/v1','UTC':utc,'base_commit':base,'members':members,
    'core_disposition_complete':True,'writer_release_pending':True,'self_hash_omitted':True})
paths.append(selection)
pins={str(path.relative_to(C)):pin(path) for path in paths}
tracked=set(git('diff','--name-only','--diff-filter=ACMRTUXB','-z').decode().split('\0'))-{''}
require(tracked<=set(pins),'Unexpected tracked metadata scope')
git('add','--',*sorted(pins))
staged=set(git('diff','--cached','--name-only','-z').decode().split('\0'))-{''}
require(staged==set(pins),'Unexpected staged metadata paths')
require(not git('diff','--cached','--diff-filter=D','--name-only'),'Deletion staged')
for path,item in pins.items():
    body=git('show',':'+path)
    require(len(body)==item['bytes'] and sha(body)==item['sha256'],'Staged metadata mismatch')
git('commit','-m','Record PR111 verified closure and program completion accounting')
commit=git('rev-parse','HEAD').decode().strip()
require(git('rev-parse','HEAD^').decode().strip()==base,'Wrong metadata parent')
changed=set(git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).decode().split('\0'))-{''}
require(changed==staged,'Unexpected metadata commit paths')
git('push','origin','HEAD:refs/heads/main')
require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==commit,'Post-push metadata mismatch')
git('fetch','--no-tags','--no-write-fetch-head','origin','refs/heads/main')
require(git('rev-parse','origin/main').decode().strip()==commit,'Fetched metadata mismatch')
for path,item in pins.items():
    body=git('show','origin/main:'+path)
    require(len(body)==item['bytes'] and sha(body)==item['sha256'],'Remote fetched metadata mismatch')
require(not git('diff','--cached','--name-only'),'Metadata index not empty')
record={'schema':'pr111-completion-metadata-actual/v1','UTC':now(),'actual_operator_PID':os.getpid(),'parent':base,
    'commit':commit,'changed_members':[pins[x] for x in sorted(pins)],'actual_nonforce_push_and_full_remote_body_readback_passed':True,
    'program_completed':19,'dated_eligible_total':99,'program_estimate_percent':19/99*100,
    'persistent_goal_status':'active','PR_workflow_percent':100,'writer_release_pending':True,'final_readback_pending':True}
dump(D/'RECEIPT.json',record)
print(json.dumps({k:v for k,v in record.items() if k!='changed_members'},sort_keys=True))

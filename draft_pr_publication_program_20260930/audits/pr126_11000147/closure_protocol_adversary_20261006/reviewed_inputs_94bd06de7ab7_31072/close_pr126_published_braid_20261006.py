"""Execute only the exact reviewed PR126 remote closure under a fresh peer resource grant."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
A=Path(__file__).resolve().parent
C=A.parents[2]
R=Path('/Users/alec/Documents/Math')
D=A/'actual_closure_20261006'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
HEAD='a1df84a64fa96d53f3a8c6fec9db8bc48bd1533c'
BASE='4c4e6450fd9aa479a54bb6d098f923b02cafa5f5'
PRIMARY_HEAD='6144d964777214c6963a915288c18fcf97b42026'
MARKER='<!-- pr126-old-published-braid-disposition-20261006 -->'
events=[]
def now(): return datetime.datetime.now(datetime.timezone.utc)
def require(value,label):
    if not value: raise ValueError(label)
def sha(body): return hashlib.sha256(body).hexdigest()
def load(path): return json.loads(path.read_text())
def dump(path,obj): path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def valid_grant():
    require(now()<datetime.datetime.fromisoformat(grant['expires_at_utc'].replace('Z','+00:00')),'Fresh resource grant expired')
    require(now()>=datetime.datetime.fromisoformat(grant['granted_at_utc'].replace('Z','+00:00')),'Grant not yet effective')
def run(argv,cwd=C):
    start=now().isoformat()
    child=subprocess.Popen(argv,cwd=cwd,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    events.append({'argv':argv,'cwd':str(cwd),'PID':child.pid,'UTC_start':start,'UTC_end':now().isoformat(),
        'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),
        'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf-8','replace')[:1600]})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,'Actual operation failed; inspect the journal and service outcome before any retry')
    return out
def git(*args,cwd=C): return run([GIT,*args],cwd)
def api(*args): return run([GH,'api','--hostname','github.com',*args])
def live():
    p=json.loads(api('repos/AlecKriebel/Math/pulls/126'))
    return {k:p[k] for k in ['number','state','draft','closed_at','merged_at','merged']}|{'head_sha':p['head']['sha'],'head_ref':p['head']['ref'],'base_ref':p['base']['ref'],'url':p['html_url']}
def open_original(p):
    return p['number']==126 and p['state']=='open' and p['draft'] and p['head_sha']==HEAD and p['base_ref']=='main' and p['url']=='https://github.com/AlecKriebel/Math/pull/126' and not p['merged']
def file_pin(path):
    require(path.is_file() and not path.is_symlink(),'Missing or redirected protected file')
    b=path.read_bytes()
    return {'path':str(path),'bytes':len(b),'sha256':sha(b),'mode':path.stat().st_mode&0o7777}
def protected():
    ref=A.parent/'pr124_10400231/ACTUAL_PRIMARY_GRANT_INVARIANTS_FINAL_20261006.json'
    saved=load(ref)['verified']
    observed=[]
    for x in saved:
        y=file_pin(Path(x['path']))
        require(y==x,'Primary index or held body changed')
        observed.append(y)
    require(observed==plan['protected_primary_full_index_and_eight_held_body_pins'],'Concrete protected primary pins changed')
    own_pin=file_pin(C/'.git/index')
    require(own_pin==plan['protected_isolated_full_index_pin'],'Concrete isolated full physical index changed')
    observed.append(own_pin)
    return observed
require(len(sys.argv)==2,'Exactly one fresh peer grant path is required')
require(not D.exists(),'Existing actual closure: inspect and recover receipts without repeating service writes')
ready_path=A/'ROOT_PUBLISHED_BRAID_DISPOSITION_READY_20261006.json'
ready=load(ready_path)
require(ready['fresh_disposition_review_PASS'] and ready['mathematical_clearance'] and ready['published_whole_narrow_result_verified'],'Completed fresh scientific gates required')
require(not ready['publication_authorization'],'This is a no-publication prior-content disposition')
note=A/ready['closing_comment_file']
require(sha(note.read_bytes())==ready['closing_comment_sha256'],'Reviewed comment changed')
body=note.read_text()
require(MARKER in body,'Idempotency marker absent')
plan_path=A/'CLOSURE_ONLY_PLAN_20261006.json'
plan=load(plan_path)
require(plan['original_head']==HEAD and plan['expected_remote_main']==BASE and plan['primary_HEAD']==PRIMARY_HEAD,'Wrong concrete plan target/base')
require(plan['closing_comment_sha256']==sha(note.read_bytes()),'Plan comment changed')
require(plan['operator_sha256']==sha(Path(__file__).read_bytes()),'Actual operator changed')
require(plan['ready_science_sha256']==sha(ready_path.read_bytes()),'Reviewed science authority changed')
fresh_manifest_path=A/ready['fresh_review_manifest']
require(sha(fresh_manifest_path.read_bytes())==ready['fresh_review_manifest_sha256'],'Fresh scientific seal changed')
fresh_manifest=load(fresh_manifest_path)
for name,pin in fresh_manifest['public_artifacts'].items():
    member=fresh_manifest_path.parent/name
    require(member.is_file() and not member.is_symlink() and member.stat().st_size==pin['bytes'] and sha(member.read_bytes())==pin['sha256'],'Fresh scientific member changed '+name)
auth_path=A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json'
require(sha(auth_path.read_bytes())==ready['original_authentication_sha256'],'Original source authority changed')
for pin in load(auth_path)['original_files']:
    member=auth_path.parent/'original_attempt'/pin['path']
    require(member.is_file() and not member.is_symlink() and member.stat().st_size==pin['bytes'] and sha(member.read_bytes())==pin['sha256'],'Submitted original changed '+pin['path'])
grant_path=Path(sys.argv[1])
grant=load(grant_path)
require(grant['source_thread_id']=='01a0ff30-7e80-7053-abb4-4a9c45f2fd62' and grant['scope']=='PR126_remote_closure_only','Wrong peer grant authority/scope')
require(grant['closure_plan_sha256']==sha(plan_path.read_bytes()) and grant['operator_sha256']==sha(Path(__file__).read_bytes()) and grant['comment_sha256']==sha(note.read_bytes()) and grant['head_sha']==HEAD,'Grant not bound to complete concrete plan')
valid_grant()
D.mkdir()
dump(D/'COMMENT_PAYLOAD.json',{'body':body})
dump(D/'CLOSE_PAYLOAD.json',{'state':'closed'})
before_pins=protected()
require(git('branch','--show-current').strip()==b'main','Stay on main')
require(git('rev-parse','HEAD').decode().strip()==BASE,'Local main advanced')
require(git('rev-parse','HEAD',cwd=R).decode().strip()==PRIMARY_HEAD,'Primary HEAD advanced')
require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==BASE,'Remote main advanced')
before=live()
require(open_original(before),'PR changed; re-evaluate before action')
pages=json.loads(api('repos/AlecKriebel/Math/issues/126/comments','--paginate','--slurp'))
matches=[x for page in pages for x in page if MARKER in x['body']]
require(len(matches)<=1,'Duplicate closing-comment markers')
comment_POSTs=0
if matches:
    comment=matches[0]
    require(comment['body']==body,'Existing marker comment differs')
else:
    require(open_original(live()),'PR changed before comment')
    valid_grant()
    comment=json.loads(api('repos/AlecKriebel/Math/issues/126/comments','--method','POST','--input',str(D/'COMMENT_PAYLOAD.json')))
    comment_POSTs=1
    require(comment['body']==body and comment['id'],'Comment creation outcome ambiguous; inspect before retry')
comment_read=json.loads(api('repos/AlecKriebel/Math/issues/comments/'+str(comment['id'])))
require(comment_read['body']==body,'Actual full comment readback mismatch')
require(open_original(live()),'PR changed after comment; do not close')
valid_grant()
api('repos/AlecKriebel/Math/pulls/126','--method','PATCH','--input',str(D/'CLOSE_PAYLOAD.json'))
after=live()
require(after['url']=='https://github.com/AlecKriebel/Math/pull/126' and after['base_ref']=='main' and after['state']=='closed' and after['head_sha']==HEAD and after['merged_at'] is None and not after['merged'] and after['closed_at'],'Same-head unmerged closure not verified')
require(git('rev-parse','HEAD').decode().strip()==BASE and git('rev-parse','HEAD',cwd=R).decode().strip()==PRIMARY_HEAD,'Local or primary HEAD changed')
require(git('ls-remote','origin','refs/heads/main').decode().split()[0]==BASE,'Remote main changed')
after_pins=protected()
require(before_pins==after_pins,'Full physical indices or held bodies changed')
record={'schema':'pr126-actual-qualified-published-braid-closure/v1','UTC':now().isoformat(),'actual_operator_PID':os.getpid(),
    'PR':126,'original_head':HEAD,'before':before,'after':after,'same_head_closed_without_merge':True,
    'closing_comment_url':comment_read['html_url'],'closing_comment_id':comment_read['id'],'closing_comment_sha256':sha(note.read_bytes()),
    'actual_comment_full_body_readback_exact':True,'actual_comment_POST_count':comment_POSTs,'actual_close_PATCH_count':1,
    'closure_plan_sha256':sha(plan_path.read_bytes()),'grant_path':str(grant_path),'grant_sha256':sha(grant_path.read_bytes()),
    'disposition':'already_solved_published_mathematical_content_consequence_express_application_priority_unresolved',
    'mathematics_valid':True,'published_whole_narrow_result_verified':True,'substantive_novel_resolution_established':False,
    'express_historical_named_target_answer_established':False,'native_correction_pending':True,'original_budget':'1/5','new_central_proof_search_turns':0,
    'DOI':None,'Zenodo_actions':False,'tracker_actions':False,'merge_actions':False,'branch_deleted':False,
    'main_writer_actions':False,'index_writer_actions':False,'native_writer_actions':False,'author_branch_writer_actions':False,
    'protected_primary_and_full_indices_before_after_exact':True,'protected_pins':after_pins,'workflow_estimate_percent':85,'persistent_goal_status':'active'}
dump(D/'RECEIPT.json',record)
print(json.dumps({k:v for k,v in record.items() if k!='protected_pins'},sort_keys=True))

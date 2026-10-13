"""Same-head authorized closure after actual fresh independent disposition gate."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent
C=A.parents[2]
D=A/'actual_closure_20261006'
GH='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
HEAD='8163ee0dc7a0f944570925984cef2dc0fb291ad8'
MARKER='<!-- pr117-exact-takagi-prior-disposition-20261006 -->'
events=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(value,label):
    if not value:raise ValueError(label)
def sha(body):return hashlib.sha256(body).hexdigest()
def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def run(args):
    start=now();child=subprocess.Popen([GH,*args],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    events.append({'argv':[GH,*args],'PID':child.pid,'UTC_start':start,'UTC_end':now(),
      'exit_code':child.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),
      'stderr_bytes':len(err),'stderr_sha256':sha(err),'stderr':err.decode('utf-8','replace')})
    dump(D/'PROCESS_JOURNAL.json',{'actual_operator_PID':os.getpid(),'events':events})
    require(child.returncode==0,'GitHub action failed; inspect actual journal/state before any retry')
    return out
def live():
    return json.loads(run(['pr','view','117','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,url,closedAt,mergedAt']))
require(not D.exists(),'Existing actual closure run; inspect rather than repeat')
ready=json.loads((A/'ROOT_DISPOSITION_READY_20261006.json').read_text())
require(ready['fresh_disposition_review_PASS'] and ready['mathematical_clearance'] and ready['exact_prior_same_example_authenticated'] and not ready['publication_authorization'],'Actual fresh disposition gate required')
note=A/ready['closing_comment_file']
require(sha(note.read_bytes())==ready['closing_comment_sha256'],'Final reviewed comment changed')
body=note.read_text()
require(MARKER in body,'Idempotency marker absent')
D.mkdir()
before=live()
require(before['state']=='OPEN' and before['isDraft'] and before['headRefOid']==HEAD and before['baseRefName']=='main','PR changed; re-evaluate before action')
pages=json.loads(run(['api','repos/AlecKriebel/Math/issues/117/comments','--paginate','--slurp']))
matches=[x for page in pages for x in page if MARKER in x['body']]
require(len(matches)<=1,'Duplicate disposition comments')
if matches:
    comment=matches[0];require(comment['body']==body,'Existing disposition comment differs')
else:
    result=run(['pr','comment','117','--repo','AlecKriebel/Math','--body-file',str(note)]).decode().strip()
    cid=result.rsplit('issuecomment-',1)[-1]
    require(cid.isdigit(),'Comment creation outcome ambiguous: inspect before retry')
    comment=json.loads(run(['api','repos/AlecKriebel/Math/issues/comments/'+cid]))
    require(comment['body']==body,'Actual comment body readback mismatch')
again=live()
require(again['state']=='OPEN' and again['headRefOid']==HEAD,'PR changed after comment')
run(['pr','close','117','--repo','AlecKriebel/Math'])
after=live()
require(after['state']=='CLOSED' and after['headRefOid']==HEAD and after['mergedAt'] is None and after['closedAt'],'Same-head unmerged closure not verified')
record={'schema':'pr117-actual-exact-prior-closure/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'PR':117,'original_head':HEAD,'before':before,'after':after,'same_head_closed_without_merge':True,
 'closing_comment_url':comment['html_url'],'closing_comment_id':comment['id'],
 'closing_comment_sha256':sha(note.read_bytes()),'actual_comment_full_body_readback_exact':True,
 'disposition':'already_solved_exact_Takagi_2011_2013_same_example','mathematics_valid':True,
 'exact_prior_same_example_authenticated':True,'substantive_novel_resolution_established':False,
 'native_correction_pending':True,'original_budget':'1/5','new_central_proof_search_turns':0,
 'DOI':None,'Zenodo_actions':False,'tracker_actions':False,'branch_deleted':False,
 'primary_checkout_mutated':False,'workflow_estimate_percent':85,'persistent_goal_status':'active'}
dump(D/'RECEIPT.json',record)
print(json.dumps(record,sort_keys=True))

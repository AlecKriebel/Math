from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent;C=A.parents[2]
D=A/'actual_closure_20261006';D.mkdir(exist_ok=False);records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(argv):
    start=now();p=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate();i=len(records)
    (D/(str(i)+'.stdout.bin')).write_bytes(out);(D/(str(i)+'.stderr.bin')).write_bytes(err)
    records.append({'argv':argv,'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,
        'stdout_file':str(i)+'.stdout.bin','stderr_file':str(i)+'.stderr.bin',
        'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()})
    (D/'PROCESS_JOURNAL.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'records':records},indent=2)+'\n')
    require(p.returncode==0,err.decode('utf8','replace')[:1500]);return out
gh='/opt/homebrew/bin/gh';HEAD='4d8ba8e9438c9c8a463721adc1102dee821b11df'
def live():return json.loads(run([gh,'pr','view','104','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,url,closedAt,mergedAt']))
ready=json.loads((A/'ROOT_DISPOSITION_READY_20261006.json').read_text())
require(ready['fresh_final_disposition_review_authenticated'] and ready['no_substantive_new_contribution_established']
        and ready['verified_prior_analytic_criterion_recovered'],'disposition gate')
note=A/ready['closing_comment_file'];body=note.read_text();require(sha(note)==ready['closing_comment_sha256'],'note changed')
before=live();require(before['state']=='OPEN' and before['isDraft'] and before['headRefOid']==HEAD
    and before['baseRefName']=='main','PR changed')
queue=C/'unsolved_math_prioritization/QUEUE.md';require(sha(queue)==ready['global_queue_sha256_before'],'queue changed before closure')
pages=json.loads(run([gh,'api','repos/AlecKriebel/Math/issues/104/comments','--paginate','--slurp']))
matches=[r for page in pages for r in page if '<!-- pr104-analytic-prior-disposition-20261006 -->' in r['body']]
require(len(matches)<=1,'duplicate disposition comments')
if matches:
    comment=matches[0];require(comment['body']==body,'existing body differs')
else:
    result=run([gh,'pr','comment','104','--repo','AlecKriebel/Math','--body-file',str(note)]).decode().strip()
    cid=result.rsplit('issuecomment-',1)[-1];require(cid.isdigit(),'no comment id; inspect before retry')
    comment=json.loads(run([gh,'api','repos/AlecKriebel/Math/issues/comments/'+cid]))
    require(comment['body']==body,'comment readback differs')
again=live();require(again['state']=='OPEN' and again['headRefOid']==HEAD,'PR changed after note')
run([gh,'pr','close','104','--repo','AlecKriebel/Math'])
after=live();require(after['state']=='CLOSED' and after['headRefOid']==HEAD and after['mergedAt'] is None
    and after['closedAt'],'same-head unmerged closure not verified')
require(sha(queue)==ready['global_queue_sha256_before'],'queue changed during closure')
record={'schema':'pr104-actual-prior-analytic-closure/v1','UTC':now(),'actual_operator_PID':os.getpid(),
 'PR':104,'original_head':HEAD,'PR_before':before,'PR_after':after,
 'same_head_closed_without_merge':True,'closing_comment_url':comment['html_url'],
 'closing_comment_id':comment['id'],'closing_comment_sha256':sha(note),'comment_body_readback_exact':True,
 'disposition':'already_solved_analytic_via_verified_reconstruction','native_correction_pending':True,
 'original_budget':'1/5','extra_central_proof_search_turns':0,'DOI':None,
 'Zenodo_actions':False,'tracker_actions':False,'branch_deleted':False,'primary_checkout_mutated':False}
(D/'RECEIPT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))

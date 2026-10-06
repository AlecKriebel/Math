"""Execute the human-directed closure after exact evidence and same-head checks."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess
A=Path(__file__).resolve().parent
C=A.parents[2]
D=A/'actual_closure_20261006'
D.mkdir(exist_ok=False)
records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def run(argv):
    start=now();proc=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=proc.communicate();i=len(records)
    (D/(str(i)+'.stdout.bin')).write_bytes(out);(D/(str(i)+'.stderr.bin')).write_bytes(err)
    records.append({'argv':argv,'PID':proc.pid,'UTC_start':start,'UTC_end':now(),'exit_code':proc.returncode,
                    'stdout_file':str(i)+'.stdout.bin','stderr_file':str(i)+'.stderr.bin',
                    'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()})
    (D/'PROCESS_JOURNAL.json').write_text(json.dumps({'operator_PID':os.getpid(),'records':records},indent=2)+'\n')
    require(proc.returncode==0,err.decode('utf-8','replace')[:2000]);return out
gh='/opt/homebrew/bin/gh'
head='fb50facb2a7389bb272bbf0b5cbd80c24c79b992'
def live():
    return json.loads(run([gh,'pr','view','97','--repo','AlecKriebel/Math','--json',
                          'number,state,isDraft,headRefOid,baseRefName,url,closedAt,mergedAt']))
ready=json.loads((A/'ROOT_NOVELTY_CLOSURE_READY_20261006.json').read_text())
require(ready['independent_disposition_review_authenticated'] and ready['no_established_novel_contribution']
        and not ready['global_queue_status_change_proposed'],'closure premise')
note=A/ready['closing_comment_file'];body=note.read_text()
require(hashlib.sha256(note.read_bytes()).hexdigest()==ready['closing_comment_sha256'],'comment changed')
before=live()
require(before['number']==97 and before['state']=='OPEN' and before['isDraft']
        and before['headRefOid']==head and before['baseRefName']=='main','PR changed before disposition')
queue=C/'unsolved_math_prioritization/QUEUE.md'
require(hashlib.sha256(queue.read_bytes()).hexdigest()==ready['global_queue_sha256_before'],'queue changed')
pages=json.loads(run([gh,'api','repos/AlecKriebel/Math/issues/97/comments','--paginate','--slurp']))
comments=[row for page in pages for row in page]
matches=[row for row in comments if '<!-- pr97-novelty-disposition-20261006 -->' in row['body']]
require(len(matches)<=1,'duplicate disposition comments')
if matches:
    require(matches[0]['body']==body,'existing disposition body differs')
    comment=matches[0]
else:
    result=run([gh,'pr','comment','97','--repo','AlecKriebel/Math','--body-file',str(note)]).decode().strip()
    comment_id=result.rsplit('issuecomment-',1)[-1]
    require(comment_id.isdigit(),'comment URL absent; inspect actual output before any retry')
    comment=json.loads(run([gh,'api','repos/AlecKriebel/Math/issues/comments/'+comment_id]))
    require(comment['body']==body,'comment readback differs')
just_before_close=live()
require(just_before_close['state']=='OPEN' and just_before_close['headRefOid']==head,'PR changed after note')
run([gh,'pr','close','97','--repo','AlecKriebel/Math'])
after=live()
require(after['state']=='CLOSED' and after['headRefOid']==head and after['closedAt']
        and after['mergedAt'] is None,'closure readback does not prove nonmerged same-head closure')
require(hashlib.sha256(queue.read_bytes()).hexdigest()==ready['global_queue_sha256_before'],'queue changed during closure')
receipt={'schema':'pr97-actual-novelty-closure/v1','UTC':now(),'operator_PID':os.getpid(),
         'PR':97,'original_head':head,'PR_before':before,'PR_after':after,
         'closing_comment_url':comment['html_url'],'closing_comment_id':comment['id'],
         'closing_comment_sha256':ready['closing_comment_sha256'],'comment_body_readback_exact':True,
         'same_head_closed_without_merge':True,'disposition':'no_established_novel_contribution_classical_corollary',
         'global_historical_status_unchanged':True,'global_queue_sha256':ready['global_queue_sha256_before'],
         'native_attempts_not_imported':True,'paper_unpublished':True,'Zenodo_service_actions':False,
         'DOI':None,'tracker_update':False,'original_author_effort':'2/5','new_central_proof_search_turns':0,
         'branch_not_deleted':True,'primary_checkout_mutated':False}
(D/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'UTC':receipt['UTC'],'operator_PID':os.getpid(),'PR':97,'state':after['state'],
                  'merged':False,'comment_url':comment['html_url'],'global_historical_status_unchanged':True}))

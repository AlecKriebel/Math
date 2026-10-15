"""Read-only exact-current-head eligibility check after completing PR50."""
from pathlib import Path
import base64
import datetime as dt
import hashlib
import json
import os
import subprocess

F=Path(__file__).resolve().parent; R=F.parents[3]
HEAD='85c78d0cf3959d9d492a637cb90835ebc6a0e828'
private=F/'private';private.mkdir()
commands=[]
def run(argv,name):
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    (private/(name+'.stdout')).write_bytes(out);(private/(name+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_utc':start,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,
      'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()})
    (F/'COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
    assert child.returncode==0
    return json.loads(out)
pr=run(['gh','pr','view','55','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,url'],'current-pr')
assert pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==HEAD
reply=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+HEAD],'exact-head-queue')
assert reply['path']=='unsolved_math_prioritization/QUEUE.md' and reply['encoding']=='base64'
body=base64.b64decode(reply['content']);(private/'QUEUE.md').write_bytes(body)
git_blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest();assert git_blob==reply['sha']
rows=[x for x in body.decode().splitlines() if '| 30006309 /' in x];assert len(rows)==1
cells=rows[0].split('|');assert cells[8].strip()=='claimed_solved' and cells[9].strip()=='1/5'
record={'schema':'pr55-goal-resumption-current-eligibility/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),
 'PR':55,'actual_current_head':HEAD,'actual_current_queue_status':cells[8].strip(),'original_budget':cells[9].strip(),'exact_current_queue_row':rows[0],
 'literal_claimed_solved_eligible':True,'queue_SHA256':hashlib.sha256(body).hexdigest(),'queue_git_blob_SHA1':git_blob,
 'PR50_completion_record':'../pr50_10600042/qualified_publication_20261004/FULLY_COMPLETED_AND_RECONCILED.json',
 'original_priority_requirement_applies':True,'PR50_exception_extended':False,
 'review_status':'Resume checked earlier source/math families and stronger-prior-theorem priority finding before any disposition; corrected SOURCE already_solved recommendation is not a native/current PR status.',
 'published_or_merged_PR55':False,'native_state_changed':False,'new_central_proof_attempts':0,
 'PR55_workflow_percent':15,'dated_program_percent':4.040404,'persistent_goal_complete':False}
with (F/'CURRENT_ELIGIBILITY.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
with (F/'RESEARCH_LOG.md').open('x') as f:f.write(record['UTC']+' — PR50 workflow complete and exact current PR55 claimed_solved1/5 independently rechecked. Resume scientific/priority audit; earlier corrected SOURCE recommendation is not promoted to native status. PR55 workflow15%; dated completed program4/99=4.040404%; no new substantive attempts.\n')
print(json.dumps(record,indent=2))

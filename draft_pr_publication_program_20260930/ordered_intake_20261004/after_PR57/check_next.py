"""Fresh literal-status-only ascending intake after the completed PR57 outcome."""
from pathlib import Path
import base64
import datetime as dt
import hashlib
import json
import os
import subprocess

F=Path(__file__).resolve().parent; P=F.parents[1]; R=P.parent
commands=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def run(argv):
    start=dt.datetime.now(dt.timezone.utc).isoformat(); child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE); out,err=child.communicate(timeout=60)
    commands.append({'argv':argv,'actual_pid':child.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err),'output_retention':'Hash only for status projection; no excluded findings/science retained.'}); assert child.returncode==0; return json.loads(out)
completed=json.loads((P/'audits/pr57_30003354/root_ordered_resumption_20261004/FULLY_COMPLETED_PUBLISHED_RESULT.json').read_bytes())
assert completed['all_mathematical_package_priority_publication_tracker_and_native_steps_verified'] is True
rows=[]; next_pr=None
for number in range(58,66):
    pr=run(['gh','pr','view',str(number),'--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,url,title'])
    assert pr['number']==number and pr['baseRefName']=='main' and pr['headRefName'].startswith('dot/math-')
    pid=pr['headRefName'].split('dot/math-',1)[1]; q=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['headRefOid']])
    body=base64.b64decode(q['content']); blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest(); assert blob==q['sha']
    selected=[s for s in body.decode().splitlines() if '| '+pid+' /' in s]; assert len(selected)==1
    cells=selected[0].split('|'); status=cells[8].strip(); turns=cells[9].strip(); eligible=status=='claimed_solved' and pr['state']=='OPEN' and pr['isDraft'] is True
    rows.append({'PR':number,'problem_id':pid,'current_GitHub_metadata':pr,'literal_submitted_status':status,'original_budget':turns,'eligible':eligible,'QUEUE_blob_SHA1':blob,'whole_QUEUE_bytes':len(body),'whole_QUEUE_sha256':sha(body),'selected_row_sha256':sha(selected[0].encode()),'excluded_science_reviewed_or_retained':False,'action':'CONTINUE_ORDERED_REVIEW' if eligible else 'SKIP_ENTIRELY_NONCLAIM_STATUS' if status!='claimed_solved' else 'SKIP_NOT_OPEN_DRAFT'})
    if eligible: next_pr=number; break
assert next_pr==65 and [r['PR'] for r in rows if not r['eligible']]==list(range(58,65))
now=dt.datetime.now(dt.timezone.utc).isoformat(); record={'schema':'ordered-intake-after-PR57-status-only/v1','UTC':now,'actual_pid':os.getpid(),'previous_completed_PR':57,'observations':rows,'next_eligible_PR':next_pr,'all_excluded_science_processed':False,'actual_commands':commands,'new_central_proof_attempts':0,'dated_completed_program_fraction_percent':6/99*100,'goal_complete':False}
with (F/'INTAKE_AFTER_PR57.json').open('x') as f: json.dump(record,f,indent=2); f.write('\n')
progress=json.loads((P/'CURRENT_PROGRESS.json').read_bytes()); assert progress['fully_completed_eligible_PRs']==[9,16,18,50,55,57]
progress.update({'UTC':now,'current_PR':next_pr,'current_PR_workflow_percent':0,'remaining_current_step':'Authenticate and read the exact currently eligible PR65 full mathematical/source result, independently reproduce and adversarially audit it, then priority and publication steps if valid. PR58-64 skipped entirely.','next_eligible_PR_after_current_completion':None,'latest_ordered_intake_record':'ordered_intake_20261004/after_PR57/INTAKE_AFTER_PR57.json','skipped_since_last_completion':list(range(58,65))})
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
(F/'RESEARCH_LOG.md').write_text(now+' — Fresh status-only immutable-head intake after completed PR57 verified next eligible65;58,59,61 already_solved and60,62,63,64 unsolved skipped entirely. No excluded mathematical review or PR/native/publication mutation. Program6/99='+str(6/99*100)+'%; next65 workflow0%.\n')
print(json.dumps(record,indent=2))

"""Fresh status-only intake. Never read or retain excluded PR56 science."""
from pathlib import Path
import base64
import datetime as dt
import hashlib
import json
import os
import subprocess

F=Path(__file__).resolve().parent; P=F.parent; R=P.parent
F.mkdir(exist_ok=True)
commands=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def run(argv):
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    commands.append({'argv':argv,'actual_pid':child.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
                     'exit_code':child.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err),
                     'output_retention':'Hash only; QUEUE notes/scientific bodies not saved by this status-only intake.'})
    assert child.returncode==0
    return out
goal=Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
assert sha(goal.read_bytes())=='1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04'
rows=[]
for number, pid in [(56,'10300016'),(57,'30003354')]:
    pr=json.loads(run(['gh','pr','view',str(number),'--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,url,title']))
    assert pr['number']==number and pr['baseRefName']=='main' and pr['headRefName']=='dot/math-'+pid
    q=json.loads(run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['headRefOid']]))
    body=base64.b64decode(q['content'])
    blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
    assert blob==q['sha']
    target=[s for s in body.decode().splitlines() if '| '+pid+' /' in s]
    assert len(target)==1
    cells=target[0].split('|'); status=cells[8].strip(); budget=cells[9].strip()
    eligible=pr['state']=='OPEN' and pr['isDraft'] is True and status=='claimed_solved'
    rows.append({'PR':number,'problem_id':pid,'current_GitHub_metadata':pr,'literal_submitted_status':status,
                 'original_budget':budget,'eligible':eligible,'action':'CONTINUE_ORDERED_REVIEW' if eligible else 'SKIP_ENTIRELY_NONCLAIM_STATUS',
                 'QUEUE_blob_SHA1':blob,'whole_QUEUE_bytes':len(body),'whole_QUEUE_sha256':sha(body),
                 'selected_row_sha256':sha(target[0].encode()),'excluded_science_reviewed_or_retained':False,
                 'native_PR_Git_publication_mutation':False})
assert rows[0]['eligible'] is False and rows[0]['literal_submitted_status']=='unsolved'
assert rows[1]['eligible'] is True
now=dt.datetime.now(dt.timezone.utc).isoformat()
result={'schema':'ordered-intake-status-only-56-57/v1','UTC':now,'actual_pid':os.getpid(),'observations':rows,
        'next_eligible_PR':57,'PR56_science_processed':False,'goal_complete':False,
        'PR50_exception_extended':False,'new_central_proof_attempts':0,'dated_completed_program_fraction_percent':5/99*100,
        'actual_commands':commands}
with (F/'INTAKE_56_57.json').open('x') as out: json.dump(result,out,indent=2);out.write('\n')
progress=json.loads((P/'CURRENT_PROGRESS.json').read_bytes())
assert progress['fully_completed_eligible_PRs']==[9,16,18,50,55]
progress.update({'UTC':now,'current_PR':57,'current_PR_workflow_percent':0,
                 'remaining_current_step':'Resume existing PR57 scientific/preprint package after fresh literal claimed_solved head eligibility. PR56 skipped entirely as unsolved.',
                 'next_eligible_PR_after_current_completion':None,
                 'next_eligible_order_requires_fresh_status_check':True,
                 'latest_ordered_intake_record':'ordered_intake_20261004/INTAKE_56_57.json',
                 'skipped_since_last_completion':[56]})
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
(F/'RESEARCH_LOG.md').write_text(f'{now} — Corrected the next numeric intake cursor56 to the next eligible PR57. Fresh immutable-head QUEUE projection verifies56 unsolved2/5: skipped without science processing;57 claimed_solved1/5: eligible for resumed review. Dated completed workflows5/99={5/99*100:.6f}%; no new proof attempts or native/Git/PR/publication changes.\n')
print(json.dumps(result,indent=2))

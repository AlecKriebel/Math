"""Fresh literal-status-only ascending intake after the completed PR66 attributed outcome."""
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
completed=json.loads((P/'audits/pr66_10400033/ROOT_FULLY_COMPLETED_ATTRIBUTED_RESULT_20261004.json').read_bytes())
assert completed['all_current_native_merge_acceptance_corrected_metadata_and_audit_checkpoint_steps_verified'] is True
rows=[]; next_pr=None
for number in range(67,74):
    pr=run(['gh','pr','view',str(number),'--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,url,title'])
    assert pr['number']==number and pr['baseRefName']=='main' and pr['headRefName'].startswith('dot/math-')
    pid=pr['headRefName'].split('dot/math-',1)[1]; q=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['headRefOid']])
    body=base64.b64decode(q['content']); blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest(); assert blob==q['sha']
    selected=[s for s in body.decode().splitlines() if '| '+pid+' /' in s]; assert len(selected)==1
    cells=selected[0].split('|'); status=cells[8].strip(); turns=cells[9].strip(); eligible=status=='claimed_solved' and pr['state']=='OPEN' and pr['isDraft'] is True
    rows.append({'PR':number,'problem_id':pid,'current_GitHub_metadata':pr,'literal_submitted_status':status,'original_budget':turns,'eligible':eligible,'QUEUE_blob_SHA1':blob,'whole_QUEUE_bytes':len(body),'whole_QUEUE_sha256':sha(body),'selected_row_sha256':sha(selected[0].encode()),'excluded_science_reviewed_or_retained':False,'action':'CONTINUE_ORDERED_REVIEW' if eligible else 'SKIP_ENTIRELY_NONCLAIM_STATUS' if status!='claimed_solved' else 'SKIP_NOT_OPEN_DRAFT'})
    if eligible: next_pr=number; break
assert next_pr is not None
now=dt.datetime.now(dt.timezone.utc).isoformat(); record={'schema':'ordered-intake-after-PR66-status-only/v1','UTC':now,'actual_pid':os.getpid(),'previous_completed_PR':66,'observations':rows,'next_eligible_PR':next_pr,'all_excluded_science_processed':False,'actual_commands':commands,'new_central_proof_attempts':0,'dated_completed_program_fraction_percent':8/99*100,'goal_complete':False}
with (F/'INTAKE_AFTER_PR66.json').open('x') as f: json.dump(record,f,indent=2); f.write('\n')
progress=json.loads((P/'CURRENT_PROGRESS.json').read_bytes()); assert progress['fully_completed_eligible_PRs']==[9,16,18,50,55,57,65,66]
progress.update({'UTC':now,'current_PR':next_pr,'current_PR_workflow_percent':0,'current_DOI':None,'current_merge_commit':None,'current_acceptance_commit':None,'current_mathematical_audit_percent':0,'current_priority_audit_percent':0,'current_priority_audit_complete':False,'current_priority_clearance':False,'current_publication_authorization':False,'current_package':None,'current_qualified_package_ready':False,'remaining_current_step':'Authenticate and read the exact currently eligible PR'+str(next_pr)+' full mathematical/source result, independently reproduce and adversarially audit it, then priority and publication steps if valid. Only literal claimed_solved heads are processed.','next_eligible_PR_after_current_completion':None,'latest_ordered_intake_record':'ordered_intake_20261004/after_PR66/INTAKE_AFTER_PR66.json','skipped_since_last_completion':[r['PR'] for r in rows if not r['eligible']],'next_numeric_intake_cursor':next_pr,'advance_to_next_PR_authorized_now':False})
for key in list(progress):
    if key.startswith('current_') and key not in {'current_PR','current_PR_workflow_percent','current_DOI','current_merge_commit','current_acceptance_commit','current_mathematical_audit_percent','current_priority_audit_percent','current_priority_audit_complete','current_priority_clearance','current_publication_authorization','current_package','current_qualified_package_ready'}: del progress[key]
(P/'CURRENT_PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
(F/'RESEARCH_LOG.md').write_text(now+' — Fresh status-only immutable-head intake after completed PR66 verified next eligible'+str(next_pr)+'; exclusions'+str([r['PR'] for r in rows if not r['eligible']])+' skipped entirely. No excluded mathematical review or PR/native/publication mutation. Program8/99='+str(8/99*100)+'%; next workflow0%.\n')
print(json.dumps(record,indent=2))

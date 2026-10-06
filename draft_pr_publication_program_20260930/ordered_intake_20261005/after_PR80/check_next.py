"""Fresh ascending draft eligibility only, after verified PR80 completion/release.

No excluded mathematical findings are examined or retained. This writes only
new intake files, never CURRENT_PROGRESS or other tracked files, and performs
no Git mutation, PR action, publication or proof search.
"""
from pathlib import Path
from datetime import datetime, timezone
import base64, hashlib, json, os, re, subprocess, sys

F=Path(__file__).resolve().parent; P=F.parents[1]; R=P.parent
A=P/'audits/pr80_30000177'; commands=[]
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sys.flags.ignore_environment and not sys.flags.optimize and sys.dont_write_bytecode
assert Path.cwd().resolve()==R.resolve()
release=json.loads((A/'ROOT_FINAL_COMPLETION_RELEASE_20261005.json').read_bytes())
assert release['status']=='PASS_NATIVE_COMPLETION_AND_WRITER_RELEASE' and release['explicit_writer_release_sent'] is True
rp=release['successful_completion_checkpoint_receipt']; raw=(R/rp['path']).read_bytes()
assert len(raw)==rp['bytes'] and sha(raw)==rp['sha256']
receipt=json.loads(raw)
assert receipt['status']=='PASS_FINAL_COMPLETION_CHECKPOINT' and receipt['phase']=='completion-checkpoint' and receipt['PR']==80
assert receipt['current_commit']==release['completion_checkpoint_commit'] and receipt['remote_main_exact'] is True
assert not (F/'INTAKE_AFTER_PR80.json').exists()

def run(argv):
    start=utc(); child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate(timeout=60)
    commands.append(dict(argv=argv,actual_pid=child.pid,started_UTC=start,finished_UTC=utc(),exit_code=child.returncode,
        stdout_sha256=sha(out),stderr_sha256=sha(err),output_retention='Hash-only status projection; excluded findings and science are not retained.'))
    assert child.returncode==0,(argv,err.decode(errors='replace'))
    return json.loads(out)

listing=run(['/opt/homebrew/bin/gh','pr','list','--repo','AlecKriebel/Math','--state','open','--limit','1000','--json','number,isDraft'])
numbers=sorted({x['number'] for x in listing if x['isDraft'] and x['number']>80 and x['number']!=8})
assert len(listing)<1000, 'Listing may be truncated; preserve and stop instead of skipping a page'
rows=[]; next_pr=None
for number in numbers:
    pr=run(['/opt/homebrew/bin/gh','pr','view',str(number),'--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,url'])
    assert pr['number']==number and pr['baseRefName']=='main'
    match=re.fullmatch(r'(?:dot/math-|math/)(\d+)(?:[-/].*)?',pr['headRefName'])
    assert match, 'Target ID is ambiguous; do not infer from scientific prose'
    pid=match[1]
    q=run(['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['headRefOid']])
    assert q['encoding']=='base64' and q['path']=='unsolved_math_prioritization/QUEUE.md'
    body=base64.b64decode(q['content']); blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
    assert blob==q['sha'] and len(body)==q['size']
    selected=[s for s in body.splitlines() if len(s.split(b'|'))>12 and s.split(b'|')[2].strip().split(b' / ')[0]==pid.encode()]
    assert len(selected)==1
    cells=selected[0].split(b'|'); status=cells[8].strip().decode(); turns=cells[9].strip().decode()
    eligible=status=='claimed_solved' and pr['state']=='OPEN' and pr['isDraft'] is True
    rows.append(dict(PR=number,problem_id=pid,current_GitHub_metadata=pr,literal_submitted_status=status,
        original_budget=turns,eligible=eligible,QUEUE_blob_SHA1=blob,whole_QUEUE_bytes=len(body),whole_QUEUE_sha256=sha(body),
        selected_row_sha256=sha(selected[0]),excluded_science_reviewed_or_retained=False,
        action='CONTINUE_ORDERED_REVIEW' if eligible else 'SKIP_ENTIRELY_NONCLAIM_STATUS' if status!='claimed_solved' else 'SKIP_NOT_OPEN_DRAFT'))
    if eligible: next_pr=number; break
now=utc()
record=dict(schema='ordered-intake-after-PR80-status-only/v1',UTC=now,actual_pid=os.getpid(),previous_completed_PR=80,
    completion_release_evidence_sha256=sha((A/'ROOT_FINAL_COMPLETION_RELEASE_20261005.json').read_bytes()),
    observations=rows,next_eligible_PR=next_pr,all_excluded_science_processed=False,actual_commands=commands,
    new_central_proof_attempts=0,dated_completed_program_fraction_percent=10/99*100,goal_complete=False,
    current_progress_tracked_file_edited=False,remaining_inventory_empty=(next_pr is None))
with (F/'INTAKE_AFTER_PR80.json').open('x') as f: json.dump(record,f,indent=2); f.write('\n')
(F/'RESEARCH_LOG.md').write_text(now+' — Fresh immutable-head eligibility after verified PR80 completion and explicit writer release. Next eligible '+str(next_pr)+'; skipped '+str([x['PR'] for x in rows if not x['eligible']])+'. Only status/budget/identity columns examined; no excluded science or PR/native/publication mutation. Program10/99='+str(10/99*100)+'%; next mathematical workflow0%.\n')
print(json.dumps(record,indent=2))

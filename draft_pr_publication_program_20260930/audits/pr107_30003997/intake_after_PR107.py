"""Inspect current draft-head QUEUE status only, after verified PR107 closure."""
from pathlib import Path
import base64,datetime,hashlib,json,os,re,subprocess
A=Path(__file__).resolve().parent
C=A.parents[2]
P=A.parents[1]
D=P/'ordered_intake_20261006/after_PR107'
D.mkdir(parents=True,exist_ok=False)
records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def run(argv):
    start=now();proc=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=proc.communicate()
    records.append({'argv':argv,'actual_PID':proc.pid,'UTC_start':start,'UTC_end':now(),'exit_code':proc.returncode,
                    'stdout_bytes':len(out),'stdout_sha256':hashlib.sha256(out).hexdigest(),
                    'stderr_bytes':len(err),'stderr_sha256':hashlib.sha256(err).hexdigest(),
                    'retention':'Status/identity projection only; excluded mathematical prose is not retained.'})
    (D/'ACTUAL_COMMANDS.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'records':records},indent=2)+'\n')
    require(proc.returncode==0,err.decode('utf-8','replace')[:1000]);return out
release_path=A/'ROOT_CLOSURE_RELEASE_ACTUAL_READBACK_20261006.json'
release=json.loads(release_path.read_text())
require(release['same_head_closed_without_merge'] and release['remote_verified']
        and release['human_PR107_disposition_resolved'],'closure gate')
require(run(['git','symbolic-ref','--short','HEAD']).strip()==b'main','branch')
require(run(['git','rev-parse','HEAD']).strip().decode()==release['commit'],'private main changed')
prs=json.loads(run(['/opt/homebrew/bin/gh','pr','list','--repo','AlecKriebel/Math','--state','open',
                   '--limit','1000','--json','number,isDraft,headRefOid,headRefName,baseRefName,url']))
prs=sorted((r for r in prs if r['number']>107 and r['isDraft']),key=lambda r:r['number'])
observations=[];next_pr=None
for pr in prs:
    match=re.fullmatch(r'dot/math-(\d+)',pr['headRefName'])
    if not match:continue
    pid=match[1]
    response=json.loads(run(['/opt/homebrew/bin/gh','api',
             'repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+pr['headRefOid']]))
    require(response['encoding']=='base64','queue encoding')
    body=base64.b64decode(response['content'])
    require(hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==response['sha'],'queue blob identity')
    rows=[]
    for line in body.decode().splitlines():
        if line.startswith('|'):
            cells=line.split('|')
            if len(cells)>12 and cells[2].strip().split('/')[0].strip()==pid:rows.append((line,cells))
    require(len(rows)==1,'unique queue status row '+pid)
    row,cells=rows[0];status=cells[8].strip();eligible=status=='claimed_solved'
    observations.append({'PR':pr['number'],'problem_id':pid,'current_GitHub_metadata':pr,
      'literal_submitted_status':status,'original_budget':cells[9].strip(),'eligible':eligible,
      'QUEUE_blob_SHA1':response['sha'],'whole_QUEUE_bytes':len(body),
      'whole_QUEUE_sha256':hashlib.sha256(body).hexdigest(),'selected_row_sha256':hashlib.sha256(row.encode()).hexdigest(),
      'excluded_science_reviewed_or_retained':False,
      'action':'CONTINUE_ORDERED_REVIEW' if eligible else 'SKIP_ENTIRELY_NONCLAIM_STATUS'})
    if eligible:next_pr=pr['number'];break
result={'schema':'ordered-status-intake-after-PR107/v1','UTC':now(),'actual_reader_PID':os.getpid(),
        'previous_completed_PR':107,'completed_metadata_commit':release['commit'],
        'completion_release_sha256':hashlib.sha256(release_path.read_bytes()).hexdigest(),
        'observations':observations,'next_eligible_PR':next_pr,'actual_commands':records,
        'excluded_science_processed':False,'previous_goal_turn_classification':'progress: actual closure and verified main release',
        'blocking_condition_absent':True}
(D/'INTAKE_AFTER_PR107.json').write_text(json.dumps(result,indent=2)+'\n')
(D/'RESEARCH_LOG.md').write_text('# Ordered intake after PR107\n\n'+result['UTC']+
 ' — status-only intake complete (100%). PR107 closure/release complete; dated program16/99 (16.16%). Only current draft-head QUEUE status and identity were parsed. Excluded mathematics was not reviewed or retained. Next eligible PR: '+str(next_pr)+'. Goal continues; no human clarification is pending.\n')
print(json.dumps({'next_eligible_PR':next_pr,'observations':[{'PR':r['PR'],'problem_id':r['problem_id'],
          'literal_status':r['literal_submitted_status'],'original_budget':r['original_budget']} for r in observations]}))
